#!/usr/bin/env python3
"""
Quick network connectivity test for UPS devices
"""
import socket
import subprocess
import platform
from config import UPS_DEVICES

def ping_test(ip):
    """Test if IP is reachable via ping"""
    param = '-n' if platform.system().lower() == 'windows' else '-c'
    command = ['ping', param, '1', '-W', '2', ip]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=3)
        return result.returncode == 0
    except:
        return False

def snmp_port_test(ip, port=161):
    """Test if SNMP port is open"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        # Send a simple SNMP get request for sysDescr
        # This is a basic SNMP v1 GetRequest for OID 1.3.6.1.2.1.1.1.0
        snmp_packet = bytes.fromhex('302902010004067075626c6963a01c020400020100020100300e300c06082b060102010101000500')
        sock.sendto(snmp_packet, (ip, port))
        data, addr = sock.recvfrom(1024)
        sock.close()
        return True
    except socket.timeout:
        return False
    except:
        return False

def main():
    print("=" * 60)
    print("UPS Network Connectivity Test")
    print("=" * 60)
    print()
    
    for device in UPS_DEVICES:
        name = device['name']
        ip = device['ip']
        port = device.get('port', 161)
        
        print(f"{name} ({ip}):")
        
        # Ping test
        ping_result = ping_test(ip)
        if ping_result:
            print(f"  ✓ Ping successful")
        else:
            print(f"  ✗ Ping failed - device may be down or blocking ICMP")
        
        # SNMP port test
        snmp_result = snmp_port_test(ip, port)
        if snmp_result:
            print(f"  ✓ SNMP port {port} appears open")
        else:
            print(f"  ⚠ SNMP port {port} not responding (may need correct community string)")
        
        print()
    
    print("=" * 60)
    print("Note: Even if ping fails, SNMP may still work.")
    print("Run 'python3 main.py --test' for full SNMP test")

if __name__ == "__main__":
    main()