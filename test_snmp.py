#!/usr/bin/env python3
"""
Test script to verify SNMP functionality
"""
import sys
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def test_pysnmp_import():
    """Test if pysnmp can be imported"""
    try:
        from pysnmp.hlapi import getCmd, SnmpEngine
        logger.info("✓ pysnmp imported successfully")
        return True
    except ImportError as e:
        logger.error(f"✗ Failed to import pysnmp: {e}")
        logger.info("\nPlease install pysnmp:")
        logger.info("  pip install pysnmp==4.4.12")
        return False

def test_snmp_manager():
    """Test the SNMP manager module"""
    try:
        from snmp_manager import UPSSNMPManager
        logger.info("✓ UPSSNMPManager imported successfully")
        
        # Create a test instance
        manager = UPSSNMPManager(
            ip='127.0.0.1',
            community='public'
        )
        logger.info("✓ UPSSNMPManager instance created")
        
        return True
    except Exception as e:
        logger.error(f"✗ Failed to create UPSSNMPManager: {e}")
        return False

def test_config():
    """Test the configuration module"""
    try:
        from config import UPS_DEVICES
        logger.info(f"✓ Configuration loaded: {len(UPS_DEVICES)} devices configured")
        
        for i, device in enumerate(UPS_DEVICES, 1):
            logger.info(f"  Device {i}: {device['name']} - {device['ip']}")
        
        return True
    except Exception as e:
        logger.error(f"✗ Failed to load configuration: {e}")
        return False

def main():
    logger.info("=" * 50)
    logger.info("SNMP Manager Debug Test")
    logger.info("=" * 50)
    
    tests = [
        ("PySnmp Library", test_pysnmp_import),
        ("SNMP Manager Module", test_snmp_manager),
        ("Configuration", test_config),
    ]
    
    results = []
    for name, test_func in tests:
        logger.info(f"\nTesting {name}...")
        results.append(test_func())
    
    logger.info("\n" + "=" * 50)
    if all(results):
        logger.info("✓ All tests passed!")
        logger.info("\nYou can now run the main monitoring system:")
        logger.info("  python main.py")
    else:
        logger.error("✗ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()