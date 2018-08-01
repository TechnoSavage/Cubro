#Bypass Switch device class for REST API interaction

import requests
from requests.exceptions import ConnectionError

#TO-DO Implement chacks against valid input for config settings
class BypassSwitch(object):
    """Object class representing Cubro Bypass Switch.

    :param address: A string, managment IP of Bypass Switch.
    """

    def __init__(self, address):
        self.address = address

    def engage(self):
        """Engage bypass mode."""
        uri = 'http://' + self.address + '/takeDown?'
        try:
            response = requests.get(uri)
            code = response.status_code
            content = response.content
            return (code, content)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def disengage(self):
        """Disengage bypass mode."""
        uri = 'http://' + self.address + '/takeUp?'
        try:
            response = requests.get(uri)
            code = response.status_code
            content = response.content
            return (code, content)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def timeout(self):
        """Disengage bypass mode for the Timeout period."""
        uri = 'http://' + self.address + '/setTimeout?'
        try:
            response = requests.get(uri)
            code = response.status_code
            content = response.content
            return (code, content)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_config_guided(self):
        """Interactive menu to set management configuration."""
        ip_address = raw_input("Enter Management IP Address [192.168.0.201]: ")
        if len(ip_address) <= 0:
            ip_address = '192.168.0.201'
        subnet_mask = raw_input("Enter Subnet Mask [255.255.255.0]: ")
        if len(subnet_mask) <= 0:
            subnet_mask = '255.255.255.0'
        gateway = raw_input("Enter Management Gateway [192.168.0.1]: ")
        if len(gateway) <= 0:
            gateway = '192.168.0.1'
        mac = raw_input("Enter a new MAC Address [D8-20-9F-00-01-64]: ")
        if len(mac) <= 0:
            mac = 'D8-20-9F-00-01-64'
        time_out = raw_input("Enter a Timeout value [10]: ")
        if len(time_out) <= 0:
            time_out = '10'
        uri = 'http://' + self.address + '/setConfig?'
        try:
            params = {
                'ip': ip_address,
                'subnet': subnet_mask,
                'gateway': gateway,
                'mac': mac,
                'timeout': time_out
                }
            response = requests.post(uri, data=params)
            code = response.status_code
            content = response.content
            return (code, content)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_config(self, address, subnet, gateway, mac, timeout):
        """Set management configuration of Bypass Switch."""
        uri = 'http://' + self.address + '/setConfig?'
        try:
            params = {
                'ip': address,
                'subnet': subnet,
                'gateway': gateway,
                'mac': mac,
                'timeout': timeout
                }
            response = requests.post(uri, data=params)
            code = response.status_code
            content = response.content
            return (code, content)
        except ConnectionError as error:
            content = 'No Response'
            raise error
