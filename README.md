# UPS SNMP Monitoring System

A comprehensive Python-based SNMP monitoring framework for UPS (Uninterruptible Power Supply) devices. This system allows you to monitor multiple UPS devices simultaneously, collect critical metrics, and log data for analysis.

## Features

- **Multi-device Support**: Monitor up to 5 UPS devices simultaneously (easily expandable)
- **Multi-threaded**: Each UPS is monitored in its own thread for optimal performance
- **Comprehensive Metrics**: Collects battery status, load percentage, voltage, current, alarms, and more
- **Flexible Logging**: Support for CSV and JSON formats with automatic rotation
- **RFC 1628 Compliant**: Uses standard UPS MIB OIDs for wide compatibility
- **Command-line Tools**: Test connections, export data, and check status

## Quick Start

### 1. Installation

```bash
# Install required packages
pip install -r requirements.txt
```

### 2. Configuration

Edit `config.py` to add your UPS devices:

```python
UPS_DEVICES = [
    {
        'name': 'UPS_1',
        'ip': '192.168.1.100',  # Your UPS IP
        'port': 161,
        'community': 'public',  # SNMP community string
        'snmp_version': 2,
    },
    # Add up to 5 devices...
]
```

### 3. Test Connections

```bash
# Test SNMP connectivity to all configured devices
python main.py --test
```

### 4. Start Monitoring

```bash
# Start the monitoring system
python main.py

# The system will:
# - Poll each UPS every 60 seconds (configurable)
# - Log data to CSV files in the 'logs' directory
# - Display real-time status in the console
# - Handle graceful shutdown with Ctrl+C
```

## Usage Examples

### Check Current Status
```bash
python main.py --show-status
```

### Export Historical Data
```bash
python main.py --export output.csv --device UPS_1
```

### Custom Monitoring Script
```python
from snmp_manager import UPSSNMPManager

# Create manager for a single UPS
manager = UPSSNMPManager(
    ip='192.168.1.100',
    community='public'
)

# Get current status
status = manager.get_ups_status()
print(f"Battery: {status['charge_remaining']}%")
print(f"Load: {status['output_load']}%")
```

## Data Collected

The system collects the following metrics (when available):

- **Battery Information**: Status, charge %, time on battery, voltage, temperature
- **Power Metrics**: Input/output voltage, current, frequency, power (watts)
- **Load Information**: Output load percentage
- **System Status**: Output source (normal/battery/bypass), active alarms
- **Device Info**: Manufacturer, model, software version

## Log Files

Data is stored in the `logs` directory:
- **CSV Format**: `UPS_NAME_YYYYMMDD.csv` (default)
- **JSON Format**: `UPS_NAME_YYYYMMDD.json` (optional)
- **Automatic Rotation**: Daily rotation with configurable size limits

## Configuration Options

In `config.py`:

- `POLL_INTERVAL`: Seconds between polls (default: 60)
- `LOG_FORMAT`: 'csv' or 'json' (default: 'csv')
- `LOG_ROTATION`: Enable daily log rotation (default: True)
- `MAX_LOG_SIZE_MB`: Maximum log file size before rotation (default: 100)
- `DEBUG`: Enable debug logging (default: False)

## Troubleshooting

### No SNMP Response
- Verify the IP address is correct
- Check SNMP is enabled on the UPS
- Confirm the community string (usually 'public' or 'private')
- Ensure port 161 (UDP) is not blocked by firewall

### Permission Errors
- Run with appropriate permissions for network access
- Ensure write permissions for the logs directory

### Missing OIDs
- Some UPS models may not support all RFC 1628 OIDs
- The system will gracefully handle missing values

## Requirements

- Python 3.6+
- pysnmp 4.4.12
- Network access to UPS devices (port 161/UDP)

## Architecture

```
main.py                 # Entry point and CLI interface
├── config.py          # Configuration file with UPS definitions
├── snmp_manager.py    # SNMP communication layer
├── ups_oids.py        # RFC 1628 OID definitions
├── data_logger.py     # Data logging and export functionality
└── logs/              # Generated log files directory
```

## License

This project is provided as-is for UPS monitoring purposes.