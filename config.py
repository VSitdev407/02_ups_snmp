"""
Configuration file for UPS SNMP monitoring
"""

# List of UPS devices to monitor
UPS_DEVICES = [
    {
        'name': '10F_UPS',
        'ip': '172.21.2.13',
        'port': 161,
        'community': 'public',  # SNMP community string
        'snmp_version': 2,  # SNMP version (1, 2, or 3)
    },
    {
        'name': '9F_UPS',
        'ip': '172.21.3.11',
        'port': 161,
        'community': 'public',
        'snmp_version': 2,
    },
    {
        'name': '8F_UPS',
        'ip': '172.21.4.10',
        'port': 161,
        'community': 'public',
        'snmp_version': 2,
    },
    {
        'name': '7F_UPS',
        'ip': '172.21.6.10',
        'port': 161,
        'community': 'public',
        'snmp_version': 2,
    },
    {
        'name': '3F_UPS',
        'ip': '172.21.5.14',
        'port': 161,
        'community': 'public',
        'snmp_version': 2,
    },
]

# Polling interval in seconds
POLL_INTERVAL = 60

# Data storage settings
LOG_DIRECTORY = 'logs'
LOG_FORMAT = 'csv'  # Options: 'csv', 'json'
LOG_ROTATION = True  # Create new log file daily
MAX_LOG_SIZE_MB = 100  # Maximum log file size before rotation

# SNMP timeout settings
SNMP_TIMEOUT = 5  # seconds
SNMP_RETRIES = 3

# Enable debug mode
DEBUG = False