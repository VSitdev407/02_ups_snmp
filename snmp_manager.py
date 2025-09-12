"""
SNMP Manager for UPS monitoring
"""
import logging
from typing import Dict, Any, Optional
try:
    from pysnmp.hlapi import (
        getCmd,
        SnmpEngine,
        CommunityData,
        UdpTransportTarget,
        ContextData,
        ObjectType,
        ObjectIdentity
    )
except ImportError:
    print("Error: pysnmp not installed. Please run: pip install pysnmp==4.4.12")
    raise
from datetime import datetime

from ups_oids import ESSENTIAL_OIDS, BATTERY_STATUS, OUTPUT_SOURCE

logger = logging.getLogger(__name__)


class UPSSNMPManager:
    def __init__(self, ip: str, port: int = 161, community: str = 'public', 
                 version: int = 2, timeout: int = 5, retries: int = 3):
        """
        Initialize SNMP manager for a UPS device
        
        Args:
            ip: IP address of the UPS
            port: SNMP port (default 161)
            community: SNMP community string
            version: SNMP version (1 or 2)
            timeout: SNMP timeout in seconds
            retries: Number of retries for failed requests
        """
        self.ip = ip
        self.port = port
        self.community = community
        self.version = version
        self.timeout = timeout
        self.retries = retries
        
        # Set up SNMP version
        if version == 1:
            self.snmp_version = 0  # SNMPv1
        else:
            self.snmp_version = 1  # SNMPv2c
            
    def get_oid(self, oid: str) -> Optional[Any]:
        """
        Get a single OID value from the UPS
        
        Args:
            oid: OID string to query
            
        Returns:
            The value of the OID or None if failed
        """
        try:
            error_indication, error_status, _, var_binds = next(
                getCmd(
                    SnmpEngine(),
                    CommunityData(self.community, mpModel=self.snmp_version),
                    UdpTransportTarget(
                        (self.ip, self.port),
                        timeout=self.timeout,
                        retries=self.retries
                    ),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid))
                )
            )
            
            if error_indication:
                logger.error(f"SNMP error for {self.ip}: {error_indication}")
                return None
                
            if error_status:
                logger.error(f"SNMP error status for {self.ip}: {error_status.prettyPrint()}")
                return None
                
            for var_bind in var_binds:
                return var_bind[1].prettyPrint()
                
        except Exception as e:
            logger.error(f"Exception getting OID {oid} from {self.ip}: {e}")
            return None
            
    def get_multiple_oids(self, oids: Dict[str, str]) -> Dict[str, Any]:
        """
        Get multiple OID values from the UPS
        
        Args:
            oids: Dictionary of {name: oid} to query
            
        Returns:
            Dictionary of {name: value} results
        """
        results = {}
        
        # Create ObjectType list for bulk request
        oid_objects = [ObjectType(ObjectIdentity(oid)) for oid in oids.values()]
        
        try:
            error_indication, error_status, _, var_binds = next(
                getCmd(
                    SnmpEngine(),
                    CommunityData(self.community, mpModel=self.snmp_version),
                    UdpTransportTarget(
                        (self.ip, self.port),
                        timeout=self.timeout,
                        retries=self.retries
                    ),
                    ContextData(),
                    *oid_objects
                )
            )
            
            if error_indication:
                logger.error(f"SNMP error for {self.ip}: {error_indication}")
                return results
                
            if error_status:
                logger.error(f"SNMP error status for {self.ip}: {error_status.prettyPrint()}")
                return results
                
            # Map results back to names
            oid_names = list(oids.keys())
            for i, var_bind in enumerate(var_binds):
                if i < len(oid_names):
                    value = var_bind[1].prettyPrint()
                    results[oid_names[i]] = self._parse_value(oid_names[i], value)
                    
        except Exception as e:
            logger.error(f"Exception getting multiple OIDs from {self.ip}: {e}")
            
        return results
        
    def get_ups_status(self) -> Dict[str, Any]:
        """
        Get essential UPS status information
        
        Returns:
            Dictionary containing UPS status data
        """
        data = {
            'timestamp': datetime.now().isoformat(),
            'ip': self.ip,
            'status': 'online',
            'error': None
        }
        
        try:
            # Get all essential OIDs
            raw_data = self.get_multiple_oids(ESSENTIAL_OIDS)
            
            if not raw_data:
                data['status'] = 'offline'
                data['error'] = 'No SNMP response'
                return data
                
            # Process and format the data
            data.update(self._process_ups_data(raw_data))
            
        except Exception as e:
            data['status'] = 'error'
            data['error'] = str(e)
            logger.error(f"Error getting UPS status from {self.ip}: {e}")
            
        return data
        
    def _parse_value(self, name: str, value: str) -> Any:
        """
        Parse SNMP values based on their type
        
        Args:
            name: Name of the value
            value: Raw SNMP value
            
        Returns:
            Parsed value
        """
        if value == 'No Such Object currently exists at this OID' or \
           value == 'No Such Instance currently exists at this OID':
            return None
            
        try:
            # Handle specific value types
            if 'status' in name.lower():
                return int(value) if value.isdigit() else value
            elif any(x in name.lower() for x in ['voltage', 'current', 'power', 'frequency', 'temperature']):
                return float(value) if value.replace('.', '').replace('-', '').isdigit() else value
            elif any(x in name.lower() for x in ['percent', 'charge']):
                return int(value) if value.isdigit() else value
            elif any(x in name.lower() for x in ['time', 'minutes', 'seconds']):
                return int(value) if value.isdigit() else value
            else:
                return value
        except:
            return value
            
    def _process_ups_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process raw SNMP data into meaningful values
        
        Args:
            raw_data: Raw SNMP data
            
        Returns:
            Processed data dictionary
        """
        processed = {}
        
        for key, value in raw_data.items():
            if value is None:
                continue
                
            # Convert status codes to text
            if key == 'status' and isinstance(value, int):
                processed['battery_status'] = BATTERY_STATUS.get(value, f'unknown ({value})')
                processed['battery_status_code'] = value
            elif key == 'output_source' and isinstance(value, int):
                processed['output_source'] = OUTPUT_SOURCE.get(value, f'unknown ({value})')
                processed['output_source_code'] = value
            # Convert scaled values
            elif key == 'voltage' and isinstance(value, (int, float)):
                processed[key] = value / 10.0  # 0.1V units to V
            elif key == 'current' and isinstance(value, (int, float)):
                processed[key] = value / 10.0  # 0.1A units to A
            elif key == 'frequency' and isinstance(value, (int, float)):
                processed[key] = value / 10.0  # 0.1Hz units to Hz
            else:
                processed[key] = value
                
        return processed
        
    def test_connection(self) -> bool:
        """
        Test SNMP connection to the UPS
        
        Returns:
            True if connection successful, False otherwise
        """
        try:
            # Try to get system description (standard OID)
            result = self.get_oid('1.3.6.1.2.1.1.1.0')
            return result is not None
        except:
            return False