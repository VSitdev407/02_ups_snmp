"""
Data logging functionality for UPS monitoring
"""
import os
import csv
import json
import logging
from datetime import datetime, date
from typing import Dict, Any, List
from pathlib import Path
import threading

logger = logging.getLogger(__name__)


class DataLogger:
    def __init__(self, log_directory: str = 'logs', log_format: str = 'csv',
                 rotation: bool = True, max_size_mb: int = 100):
        """
        Initialize data logger
        
        Args:
            log_directory: Directory to store log files
            log_format: Format for logs ('csv' or 'json')
            rotation: Enable daily rotation
            max_size_mb: Maximum log file size in MB
        """
        self.log_directory = Path(log_directory)
        self.log_format = log_format
        self.rotation = rotation
        self.max_size_mb = max_size_mb
        self.lock = threading.Lock()
        
        # Create log directory if it doesn't exist
        self.log_directory.mkdir(parents=True, exist_ok=True)
        
        # Track current log files
        self.current_files = {}
        
    def log_data(self, device_name: str, data: Dict[str, Any]):
        """
        Log UPS data to file
        
        Args:
            device_name: Name of the UPS device
            data: Data dictionary to log
        """
        with self.lock:
            try:
                if self.log_format == 'csv':
                    self._log_csv(device_name, data)
                elif self.log_format == 'json':
                    self._log_json(device_name, data)
                else:
                    logger.error(f"Unsupported log format: {self.log_format}")
            except Exception as e:
                logger.error(f"Error logging data for {device_name}: {e}")
                
    def _get_log_filename(self, device_name: str) -> Path:
        """
        Get the appropriate log filename
        
        Args:
            device_name: Name of the UPS device
            
        Returns:
            Path to the log file
        """
        if self.rotation:
            date_str = date.today().strftime('%Y%m%d')
            filename = f"{device_name}_{date_str}.{self.log_format}"
        else:
            filename = f"{device_name}.{self.log_format}"
            
        filepath = self.log_directory / filename
        
        # Check file size for rotation
        if filepath.exists() and filepath.stat().st_size > self.max_size_mb * 1024 * 1024:
            # Create a new file with timestamp
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"{device_name}_{timestamp}.{self.log_format}"
            filepath = self.log_directory / filename
            
        return filepath
        
    def _log_csv(self, device_name: str, data: Dict[str, Any]):
        """
        Log data in CSV format
        
        Args:
            device_name: Name of the UPS device
            data: Data dictionary to log
        """
        filepath = self._get_log_filename(device_name)
        file_exists = filepath.exists()
        
        # Flatten nested dictionaries
        flat_data = self._flatten_dict(data)
        
        with open(filepath, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=flat_data.keys())
            
            # Write header if file is new
            if not file_exists:
                writer.writeheader()
                
            writer.writerow(flat_data)
            
    def _log_json(self, device_name: str, data: Dict[str, Any]):
        """
        Log data in JSON format
        
        Args:
            device_name: Name of the UPS device
            data: Data dictionary to log
        """
        filepath = self._get_log_filename(device_name)
        
        # Append to JSON lines format
        with open(filepath, 'a') as f:
            json.dump(data, f)
            f.write('\n')
            
    def _flatten_dict(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """
        Flatten a nested dictionary
        
        Args:
            d: Dictionary to flatten
            parent_key: Parent key for nested items
            sep: Separator for keys
            
        Returns:
            Flattened dictionary
        """
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(self._flatten_dict(v, new_key, sep=sep).items())
            else:
                items.append((new_key, v))
        return dict(items)
        
    def get_latest_data(self, device_name: str, num_records: int = 10) -> List[Dict[str, Any]]:
        """
        Get the latest logged data for a device
        
        Args:
            device_name: Name of the UPS device
            num_records: Number of records to retrieve
            
        Returns:
            List of data dictionaries
        """
        records = []
        
        try:
            # Find the most recent log file for this device
            pattern = f"{device_name}*.{self.log_format}"
            files = sorted(self.log_directory.glob(pattern), key=lambda x: x.stat().st_mtime, reverse=True)
            
            if not files:
                return records
                
            filepath = files[0]
            
            if self.log_format == 'csv':
                with open(filepath, 'r') as f:
                    reader = csv.DictReader(f)
                    all_records = list(reader)
                    records = all_records[-num_records:] if len(all_records) > num_records else all_records
                    
            elif self.log_format == 'json':
                with open(filepath, 'r') as f:
                    lines = f.readlines()
                    for line in lines[-num_records:]:
                        records.append(json.loads(line))
                        
        except Exception as e:
            logger.error(f"Error reading latest data for {device_name}: {e}")
            
        return records
        
    def export_data(self, device_name: str, start_date: datetime = None, 
                   end_date: datetime = None, output_file: str = None) -> bool:
        """
        Export data for a specific time range
        
        Args:
            device_name: Name of the UPS device
            start_date: Start date for export
            end_date: End date for export
            output_file: Output file path
            
        Returns:
            True if successful, False otherwise
        """
        try:
            all_data = []
            pattern = f"{device_name}*.{self.log_format}"
            files = sorted(self.log_directory.glob(pattern))
            
            for filepath in files:
                if self.log_format == 'csv':
                    with open(filepath, 'r') as f:
                        reader = csv.DictReader(f)
                        for row in reader:
                            # Filter by date if specified
                            if 'timestamp' in row:
                                timestamp = datetime.fromisoformat(row['timestamp'])
                                if start_date and timestamp < start_date:
                                    continue
                                if end_date and timestamp > end_date:
                                    continue
                            all_data.append(row)
                            
                elif self.log_format == 'json':
                    with open(filepath, 'r') as f:
                        for line in f:
                            data = json.loads(line)
                            # Filter by date if specified
                            if 'timestamp' in data:
                                timestamp = datetime.fromisoformat(data['timestamp'])
                                if start_date and timestamp < start_date:
                                    continue
                                if end_date and timestamp > end_date:
                                    continue
                            all_data.append(data)
                            
            # Write to output file
            if output_file:
                output_path = Path(output_file)
                if output_path.suffix == '.csv':
                    with open(output_path, 'w', newline='') as f:
                        if all_data:
                            writer = csv.DictWriter(f, fieldnames=all_data[0].keys())
                            writer.writeheader()
                            writer.writerows(all_data)
                elif output_path.suffix == '.json':
                    with open(output_path, 'w') as f:
                        json.dump(all_data, f, indent=2)
                        
            return True
            
        except Exception as e:
            logger.error(f"Error exporting data for {device_name}: {e}")
            return False