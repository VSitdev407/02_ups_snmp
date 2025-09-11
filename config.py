"""
Configuration file for UPS SNMP monitoring
"""

# List of UPS devices to monitor
UPS_DEVICES = [
    {
        'name': 'UPS_1',
        'ip': '192.168.1.100',  # Replace with your actual IP
        'port': 161,
        'community': 'public',  # SNMP community string
        'snmp_version': 2,  # SNMP version (1, 2, or 3)
    },
    {
        'name': 'UPS_2',
        'ip': '192.168.1.101',  # Replace with your actual IP
        'port': 161,
        'community': 'public',
        'snmp_version': 2,
    },
    {
        'name': 'UPS_3',
        'ip': '192.168.1.102',  # Replace with your actual IP
        'port': 161,
        'community': 'public',
        'snmp_version': 2,
    },
    {
        'name': 'UPS_4',
        'ip': '192.168.1.103',  # Replace with your actual IP
        'port': 161,
        'community': 'public',
        'snmp_version': 2,
    },
    {
        'name': 'UPS_5',
        'ip': '192.168.1.104',  # Replace with your actual IP
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