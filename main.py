#!/usr/bin/env python3
"""
UPS SNMP Monitoring System
Main execution script with multi-threading support
"""
import sys
import time
import logging
import threading
from datetime import datetime
from typing import List, Dict, Any
import signal
import argparse

from config import UPS_DEVICES, POLL_INTERVAL, LOG_DIRECTORY, LOG_FORMAT, LOG_ROTATION, MAX_LOG_SIZE_MB, DEBUG
from snmp_manager import UPSSNMPManager
from data_logger import DataLogger

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if DEBUG else logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ups_monitor.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Global flag for graceful shutdown
shutdown_event = threading.Event()


class UPSMonitor:
    def __init__(self, device_config: Dict[str, Any], data_logger: DataLogger):
        """
        Initialize UPS monitor for a single device
        
        Args:
            device_config: Configuration dictionary for the UPS device
            data_logger: DataLogger instance for logging data
        """
        self.device_config = device_config
        self.device_name = device_config['name']
        self.data_logger = data_logger
        
        # Initialize SNMP manager
        self.snmp_manager = UPSSNMPManager(
            ip=device_config['ip'],
            port=device_config.get('port', 161),
            community=device_config.get('community', 'public'),
            version=device_config.get('snmp_version', 2)
        )
        
        self.thread = None
        self.last_status = None
        
    def start(self):
        """Start monitoring thread for this UPS"""
        self.thread = threading.Thread(target=self._monitor_loop, name=f"Monitor-{self.device_name}")
        self.thread.daemon = True
        self.thread.start()
        logger.info(f"Started monitoring thread for {self.device_name} ({self.device_config['ip']})")
        
    def _monitor_loop(self):
        """Main monitoring loop for this UPS"""
        logger.info(f"Monitoring loop started for {self.device_name}")
        
        # Test connection first
        if not self.snmp_manager.test_connection():
            logger.warning(f"Initial connection test failed for {self.device_name} ({self.device_config['ip']})")
        
        while not shutdown_event.is_set():
            try:
                # Collect data from UPS
                data = self.snmp_manager.get_ups_status()
                data['device_name'] = self.device_name
                
                # Log status changes
                if self.last_status != data.get('status'):
                    logger.info(f"{self.device_name}: Status changed from {self.last_status} to {data.get('status')}")
                    self.last_status = data.get('status')
                
                # Log data
                self.data_logger.log_data(self.device_name, data)
                
                # Display summary
                self._display_summary(data)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop for {self.device_name}: {e}")
                
            # Wait for next poll interval
            shutdown_event.wait(POLL_INTERVAL)
            
        logger.info(f"Monitoring loop stopped for {self.device_name}")
        
    def _display_summary(self, data: Dict[str, Any]):
        """Display summary of UPS status"""
        if data.get('status') == 'online':
            summary_parts = [
                f"{self.device_name}:",
                f"Battery: {data.get('charge_remaining', 'N/A')}%",
                f"Load: {data.get('output_load', 'N/A')}%",
                f"Output: {data.get('output_voltage', 'N/A')}V",
                f"Source: {data.get('output_source', 'N/A')}"
            ]
            
            if data.get('present_alarms', 0) > 0:
                summary_parts.append(f"ALARMS: {data.get('present_alarms')}")
                
            logger.info(" | ".join(summary_parts))
        else:
            logger.warning(f"{self.device_name}: {data.get('status')} - {data.get('error', 'Unknown error')}")


class UPSMonitoringSystem:
    def __init__(self):
        """Initialize the UPS monitoring system"""
        self.data_logger = DataLogger(
            log_directory=LOG_DIRECTORY,
            log_format=LOG_FORMAT,
            rotation=LOG_ROTATION,
            max_size_mb=MAX_LOG_SIZE_MB
        )
        self.monitors = []
        
    def start(self):
        """Start monitoring all configured UPS devices"""
        logger.info("=" * 60)
        logger.info("UPS SNMP Monitoring System Starting")
        logger.info(f"Monitoring {len(UPS_DEVICES)} UPS devices")
        logger.info(f"Poll interval: {POLL_INTERVAL} seconds")
        logger.info(f"Log format: {LOG_FORMAT}")
        logger.info(f"Log directory: {LOG_DIRECTORY}")
        logger.info("=" * 60)
        
        # Create and start monitors for each device
        for device_config in UPS_DEVICES:
            monitor = UPSMonitor(device_config, self.data_logger)
            monitor.start()
            self.monitors.append(monitor)
            time.sleep(0.5)  # Stagger thread starts
            
        logger.info(f"All {len(self.monitors)} monitoring threads started")
        
    def stop(self):
        """Stop all monitoring threads"""
        logger.info("Shutting down monitoring system...")
        shutdown_event.set()
        
        # Wait for all threads to complete
        for monitor in self.monitors:
            if monitor.thread and monitor.thread.is_alive():
                monitor.thread.join(timeout=5)
                
        logger.info("All monitoring threads stopped")
        
    def run(self):
        """Run the monitoring system"""
        self.start()
        
        try:
            # Keep the main thread alive
            while not shutdown_event.is_set():
                time.sleep(1)
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received")
        finally:
            self.stop()


def signal_handler(signum, frame):
    """Handle shutdown signals"""
    logger.info(f"Received signal {signum}")
    shutdown_event.set()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='UPS SNMP Monitoring System')
    parser.add_argument('--test', action='store_true', help='Test connection to all UPS devices')
    parser.add_argument('--export', type=str, help='Export data for a device to file')
    parser.add_argument('--device', type=str, help='Specific device name for export')
    parser.add_argument('--show-status', action='store_true', help='Show current status of all devices')
    
    args = parser.parse_args()
    
    if args.test:
        # Test mode - test connections to all devices
        logger.info("Testing connections to all UPS devices...")
        for device in UPS_DEVICES:
            manager = UPSSNMPManager(
                ip=device['ip'],
                port=device.get('port', 161),
                community=device.get('community', 'public'),
                version=device.get('snmp_version', 2)
            )
            
            if manager.test_connection():
                logger.info(f" {device['name']} ({device['ip']}): Connection successful")
            else:
                logger.error(f" {device['name']} ({device['ip']}): Connection failed")
                
    elif args.export and args.device:
        # Export mode - export data for a specific device
        data_logger = DataLogger(
            log_directory=LOG_DIRECTORY,
            log_format=LOG_FORMAT
        )
        
        if data_logger.export_data(args.device, output_file=args.export):
            logger.info(f"Data exported successfully to {args.export}")
        else:
            logger.error("Export failed")
            
    elif args.show_status:
        # Show current status of all devices
        logger.info("Current status of all UPS devices:")
        for device in UPS_DEVICES:
            manager = UPSSNMPManager(
                ip=device['ip'],
                port=device.get('port', 161),
                community=device.get('community', 'public'),
                version=device.get('snmp_version', 2)
            )
            
            status = manager.get_ups_status()
            if status.get('status') == 'online':
                logger.info(f"{device['name']}: Online | Battery: {status.get('charge_remaining', 'N/A')}% | Load: {status.get('output_load', 'N/A')}%")
            else:
                logger.warning(f"{device['name']}: {status.get('status', 'Unknown')}")
                
    else:
        # Normal operation - start monitoring system
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Create and run monitoring system
        monitoring_system = UPSMonitoringSystem()
        monitoring_system.run()


if __name__ == "__main__":
    main()