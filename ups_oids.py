"""
UPS SNMP OID definitions
Based on RFC 1628 (UPS-MIB) and common vendor-specific MIBs
"""

# RFC 1628 UPS-MIB OIDs
UPS_MIB_BASE = '1.3.6.1.2.1.33'

# UPS Identification
UPS_IDENT = {
    'manufacturer': f'{UPS_MIB_BASE}.1.1.1.0',
    'model': f'{UPS_MIB_BASE}.1.1.2.0',
    'ups_software_version': f'{UPS_MIB_BASE}.1.1.3.0',
    'agent_software_version': f'{UPS_MIB_BASE}.1.1.4.0',
    'name': f'{UPS_MIB_BASE}.1.1.5.0',
    'attached_devices': f'{UPS_MIB_BASE}.1.1.6.0',
}

# Battery Information
UPS_BATTERY = {
    'status': f'{UPS_MIB_BASE}.1.2.1.0',  # 1=unknown, 2=normal, 3=low, 4=depleted
    'time_on_battery': f'{UPS_MIB_BASE}.1.2.2.0',  # seconds
    'minutes_remaining': f'{UPS_MIB_BASE}.1.2.3.0',
    'charge_remaining': f'{UPS_MIB_BASE}.1.2.4.0',  # percent
    'voltage': f'{UPS_MIB_BASE}.1.2.5.0',  # 0.1 Volt DC
    'current': f'{UPS_MIB_BASE}.1.2.6.0',  # 0.1 Amp DC
    'temperature': f'{UPS_MIB_BASE}.1.2.7.0',  # degrees Celsius
}

# Input Information
UPS_INPUT = {
    'num_lines': f'{UPS_MIB_BASE}.1.3.1.0',
    'line_index': f'{UPS_MIB_BASE}.1.3.3.1.1',  # append .1, .2, .3 for each line
    'frequency': f'{UPS_MIB_BASE}.1.3.3.1.2',  # 0.1 Hertz
    'voltage': f'{UPS_MIB_BASE}.1.3.3.1.3',  # RMS Volts
    'current': f'{UPS_MIB_BASE}.1.3.3.1.4',  # 0.1 RMS Amp
    'true_power': f'{UPS_MIB_BASE}.1.3.3.1.5',  # Watts
}

# Output Information
UPS_OUTPUT = {
    'source': f'{UPS_MIB_BASE}.1.4.1.0',  # 1=other, 2=none, 3=normal, 4=bypass, 5=battery, 6=booster, 7=reducer
    'frequency': f'{UPS_MIB_BASE}.1.4.2.0',  # 0.1 Hertz
    'num_lines': f'{UPS_MIB_BASE}.1.4.3.0',
    'line_index': f'{UPS_MIB_BASE}.1.4.4.1.1',  # append .1, .2, .3 for each line
    'voltage': f'{UPS_MIB_BASE}.1.4.4.1.2',  # RMS Volts
    'current': f'{UPS_MIB_BASE}.1.4.4.1.3',  # 0.1 RMS Amp
    'power': f'{UPS_MIB_BASE}.1.4.4.1.4',  # Watts
    'percent_load': f'{UPS_MIB_BASE}.1.4.4.1.5',  # percent
}

# Bypass Information
UPS_BYPASS = {
    'frequency': f'{UPS_MIB_BASE}.1.5.1.0',  # 0.1 Hertz
    'num_lines': f'{UPS_MIB_BASE}.1.5.2.0',
    'line_index': f'{UPS_MIB_BASE}.1.5.3.1.1',
    'voltage': f'{UPS_MIB_BASE}.1.5.3.1.2',  # RMS Volts
    'current': f'{UPS_MIB_BASE}.1.5.3.1.3',  # 0.1 RMS Amp
    'power': f'{UPS_MIB_BASE}.1.5.3.1.4',  # Watts
}

# Alarm Information
UPS_ALARM = {
    'present_alarms': f'{UPS_MIB_BASE}.1.6.1.0',  # number of active alarms
    'alarms_table': f'{UPS_MIB_BASE}.1.6.2',  # alarm table
    'alarm_id': f'{UPS_MIB_BASE}.1.6.2.1.1',
    'alarm_desc': f'{UPS_MIB_BASE}.1.6.2.1.2',
    'alarm_time': f'{UPS_MIB_BASE}.1.6.2.1.3',
}

# Test Information
UPS_TEST = {
    'test_id': f'{UPS_MIB_BASE}.1.7.1.0',
    'spin_lock': f'{UPS_MIB_BASE}.1.7.2.0',
    'results_summary': f'{UPS_MIB_BASE}.1.7.3.0',  # 1=done/passed, 2=done/warning, 3=done/error, 4=aborted, 5=in progress, 6=no test initiated
    'results_detail': f'{UPS_MIB_BASE}.1.7.4.0',
    'start_time': f'{UPS_MIB_BASE}.1.7.5.0',
    'elapsed_time': f'{UPS_MIB_BASE}.1.7.6.0',  # seconds
}

# Control Operations
UPS_CONTROL = {
    'shutdown_type': f'{UPS_MIB_BASE}.1.8.1.0',  # 1=output, 2=system
    'shutdown_after_delay': f'{UPS_MIB_BASE}.1.8.2.0',  # seconds, -1=cancel
    'startup_after_delay': f'{UPS_MIB_BASE}.1.8.3.0',  # seconds, -1=cancel
    'reboot_with_duration': f'{UPS_MIB_BASE}.1.8.4.0',  # seconds
    'auto_restart': f'{UPS_MIB_BASE}.1.8.5.0',  # 1=on, 2=off
}

# Configuration
UPS_CONFIG = {
    'input_voltage': f'{UPS_MIB_BASE}.1.9.1.0',  # RMS Volts
    'input_frequency': f'{UPS_MIB_BASE}.1.9.2.0',  # 0.1 Hertz
    'output_voltage': f'{UPS_MIB_BASE}.1.9.3.0',  # RMS Volts
    'output_frequency': f'{UPS_MIB_BASE}.1.9.4.0',  # 0.1 Hertz
    'output_va': f'{UPS_MIB_BASE}.1.9.5.0',  # Volt-Amps
    'output_power': f'{UPS_MIB_BASE}.1.9.6.0',  # Watts
    'low_battery_time': f'{UPS_MIB_BASE}.1.9.7.0',  # minutes
    'audible_alarm': f'{UPS_MIB_BASE}.1.9.8.0',  # 1=disabled, 2=enabled, 3=muted
    'low_voltage_transfer_point': f'{UPS_MIB_BASE}.1.9.9.0',  # RMS Volts
    'high_voltage_transfer_point': f'{UPS_MIB_BASE}.1.9.10.0',  # RMS Volts
}

# Common data collection groups
ESSENTIAL_OIDS = {
    **UPS_BATTERY,
    'output_source': UPS_OUTPUT['source'],
    'output_voltage': UPS_OUTPUT['voltage'] + '.1',  # Line 1
    'output_power': UPS_OUTPUT['power'] + '.1',  # Line 1
    'output_load': UPS_OUTPUT['percent_load'] + '.1',  # Line 1
    'input_voltage': UPS_INPUT['voltage'] + '.1',  # Line 1
    'input_frequency': UPS_INPUT['frequency'] + '.1',  # Line 1
    'present_alarms': UPS_ALARM['present_alarms'],
}

# Status code mappings
BATTERY_STATUS = {
    1: 'unknown',
    2: 'batteryNormal',
    3: 'batteryLow',
    4: 'batteryDepleted'
}

OUTPUT_SOURCE = {
    1: 'other',
    2: 'none',
    3: 'normal',
    4: 'bypass',
    5: 'battery',
    6: 'booster',
    7: 'reducer'
}

TEST_RESULT = {
    1: 'donePass',
    2: 'doneWarning',
    3: 'doneError',
    4: 'aborted',
    5: 'inProgress',
    6: 'noTestsInitiated'
}