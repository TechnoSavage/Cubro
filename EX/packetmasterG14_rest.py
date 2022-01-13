""" Packetmaster EX device class for REST API interaction,
    Use with firmware version 2.2.5 or newer and up to G4 NPB."""

from getpass import getpass
import json
import re
import requests
from requests.exceptions import ConnectionError
import input_validation

class PacketmasterEX(object):
    """Object class representing a Cubro Packetmaster EX Network Packet Broker.

    :param address: A string, Management IP of Packetmaster.
    :param username: A string, username of an account on the Packetmaster.
    :param password: A string, password for the user account.
    """


    def __init__(self, address, username=None, password=None):
        self._address = address
        self.username = username
        self.password = password
        self.__https = False
        conn_test = self.conn_test()
        print(conn_test)

    def conn_test(self):
        """Test if device is reachable and assign properties.
        Assigns additional properties including connecting via HTTP or HTTPS,
        Total port count for device, Model of Packetmaster, Hardware generation of Packetmaster.

        :returns: A string, "Connection test failed" or "Connection established."
        :raises: ConnectionError: if unable to successfully make GET request to device."""
        try:
            port_test = self.get_portcount()
            if not isinstance(port_test, (int)):
                print(port_test['error'])
                return "Connection test failed"
            self.get_gen()
            self.get_model()
            return "Connection established"
        except ConnectionError as fail:
            print(fail)
            try:
                self.__https = True
                port_test = self.get_portcount()
                if not isinstance(port_test, (int, long)):
                    print(port_test['error'])
                    return "Connection test failed"
                self.get_gen()
                self.get_model()
                return "Connection established"
            except ConnectionError as fail:
                print("Unable to establish connection; check if IP address is correct.", fail)

    #This will currently return both Physical and Logical ports.
    #Find way to list Physical ports only.
    def get_portcount(self):
        """Return the number of ports on the device.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/ports/config?'
        else:
            uri = 'http://' + self._address + '/rest/ports/config?'
        ports = list()
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            for i in info:
                if 'error' in i:
                    return info
            count = 0
            for port in info['port_config']:
                ports.append(info['port_config'][count]['if_name'])
                count += 1
            #Exclude all logical ports
            self.ports = len(ports)
            return len(ports)
        except ConnectionError as error:
            raise error

    def get_firmware(self):
        """Return firmware version of Packetmaster and set as property.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/imageversion?'
        else:
            uri = 'http://' + self._address + '/rest/device/imageversion?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            self.firmware = info['version']
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_apilevel(self):
        """Return API level of Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/apilevel?'
        else:
            uri = 'http://' + self._address + '/rest/device/apilevel?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_ipconfig(self):
        """Return IP config of device and set netmask and gateway properties.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/ipconfig?'
        else:
            uri = 'http://' + self._address + '/rest/device/ipconfig?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            self.netmask = info['current_netmask']
            self.gateway = info['current_gateway']
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_ipconfig_guided(self):
        """Interactive menu for configuring management IP settings."""
        address = input('Enter IP Address (e.g. 192.168.0.200): ')
        if input_validation.ipv4(address) != 0:
            address = input_validation.ipv4(address)
        #elif input_validation.ipv6(address) != 0:
        #   address = input_validation.ipv6(address)
        else:
            return "That is not a valid IP address; canceling Set IP Configuration. \n"
        netmask = input('Enter Subnet Mask (e.g. 255.255.255.0): ')
        if input_validation.ipv4(netmask) != 0:
            netmask = input_validation.ipv4(netmask)
        else:
            return "That is not a valid Subnet Mask; canceling Set IP Configuration. \n"
        gateway = input('Enter gateway (e.g. 192.168.0.1): ')
        if input_validation.ipv4(gateway) != 0:
            gateway = input_validation.ipv4(gateway)
        else:
            return "That is not a valid Gateway Address; canceling Set IP Configuration. \n"
        confirm = input("""Configuration change summary:
                        New management IP: %s
                        New Subnet Mask: %s
                        New Gateway: %s
                        Confirm changes [y/n]: """ % (address, netmask, gateway))
        if confirm.lower() in ('y', 'yes'):
            run = self.set_ipconfig(address, netmask, gateway)
            return run
        return "Canceling; no changes made.\n"

    def set_ipconfig(self, address, netmask, gateway):
        """Set management IP configuration for Packetmaster.
        
           :param address: A string, management IP address.
           :param netmask: A string, managment IP subnet mask.
           :param gateway: A string, default gateway.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/ipconfig?'
        else:
            uri = 'http://' + self._address + '/rest/device/ipconfig?'
        if input_validation.ipv4(address) != 0:
            address = input_validation.ipv4(address)
        #elif input_validation.ipv6(address) != 0:
        #   address = input_validation.ipv6(address)
        else:
            return "That is not a valid IP address; canceling Set IP Configuration. \n"
        if input_validation.ipv4(netmask) != 0:
            netmask = input_validation.ipv4(netmask)
        else:
            return "That is not a valid Subnet Mask; canceling Set IP Configuration. \n"
        if input_validation.ipv4(gateway) != 0:
            gateway = input_validation.ipv4(gateway)
        else:
            return "That is not a valid Gateway Address; canceling Set IP Configuration. \n"
        data = {'ip': address, 'mask': netmask, 'gw': gateway}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_model(self):
        """Return model of Packetmaster and set model property.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/model?'
        else:
            uri = 'http://' + self._address + '/rest/device/model?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            self.model = info['model']
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error
        self.model = info['model']

    def get_name(self):
        """Return name of Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/name?'
        else:
            uri = 'http://' + self._address + '/rest/device/name?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            self.name = info['name']
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_name_guided(self):
        """Interactive menu for setting Packetmaster name."""
        newname = input('Enter device name: ')
        confirm = input("""Configuration change summary:
                        New Device Name: %s
                        Confirm changes [y/n]: """ % newname)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_name(newname)
            return run
        return "Canceling; no changes made.\n"

    def set_name(self, name):
        """Set Packetmaster name.
        
           :param name: A string, device name
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/name?'
        else:
            uri = 'http://' + self._address + '/rest/device/name?'
        data = {'device_name': name}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_label(self):
        """Return name and notes of Packetmaster and set them as properties.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/customident?'
        else:
            uri = 'http://' + self._address + '/rest/device/customident?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            self.name = info['name']
            self.notes = info['notes']
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_label_guided(self):
        """Interactive menu for setting Packetmaster name and notes."""
        newname = input('Enter device name: ')
        newnotes = input('Enter device notes: ')
        confirm = input("""Configuration change summary:
                        New Device Name: %s
                        New Device Notes: %s
                        Confirm changes [y/n]: """ % (newname, newnotes))
        if confirm.lower() in ('y', 'yes'):
            run = self.set_label(newname, newnotes)
            return run
        return "Canceling; no changes made.\n"

    def set_label(self, name, notes):
        """Set Packetmaster name and notes.
        
           :param name: A string, device name.
           :param notes: A string, device notes.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/customident?'
        else:
            uri = 'http://' + self._address + '/rest/device/customident?'
        data = {'name': name,
                'notes': notes}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_gen(self):
        """Return hardware generation of Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/generation?'
        else:
            uri = 'http://' + self._address + '/rest/device/generation?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            self.generation = info['generation']
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_sn(self):
        """Return serial number of Packetmaster and set as property.
           
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/serialno?'
        else:
            uri = 'http://' + self._address + '/rest/device/serialno?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            self.serial = info['serial']
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_portconfig(self):
        """Return port configuration of Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/ports/config?'
        else:
            uri = 'http://' + self._address + '/rest/ports/config?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_portconfig_guided(self):
        """Interactive menu for setting port configuration on Packetmaster."""
        interface = input('Enter the interface name of the port you want to change: ')
        if self.generation == '4':
            speed = input('Enter interface speed; e.g. "1000", "10G", "40G", "100G": ').strip()
            if speed in ('1000', '10g', '10G', '40g', '40G', '100g', '100G'):
                speed = speed.upper()
            else:
                return "That is not a valid input for port speed; canceling Set Port Config."
        else: #May need to become 'elif self.hardware == '3.1'' with new else
              #clause; need EX5-2,and EX12 to verify.  EX6 (Gen-2) does not
              #allow speed changes on SFP+ ports
            print("""Enter interface speed:
                     e.g. "10", "100", "1000", "auto" for copper or SFP ports;
                     "XG" (10G) or "1G" for SFP+ ports""")
            speed = input(': ').strip()
            if speed.lower() == 'auto':
                speed = 'auto'
            elif speed in ('10', '100', '1000', 'XG', 'xg', 'Xg', 'xG', '1g', '1G'):
                speed = speed.upper()
            else:
                return "That is not a valid input for port speed; canceling Set Port Config."
        if speed in ('10', '100', '1000', 'auto'):
            duplex = input('Enter the Duplex of the interface;'
                           'options are "full", "half, or "auto" [auto]: ')
            if duplex == '':
                duplex = 'auto'
        else:
            duplex = 'full'
        if speed in ('40G', '100G'):
            split = input('Split to breakout cable?'
                          'Enter "yes" for yes and "no" for no [no]: ')
            if split == '':
                split = 'no'
        description = input('Enter description for this port; leave blank for none: ')
        if self.generation == '4' and speed in ('40G', '100G'):
            forcetx = input('Force TX?  Enter "true" for yes and "false" for no [false]: ')
            if forcetx.lower() in ('true', 't', 'yes', 'y'):
                forcetx = True
            else:
                forcetx = False
            check = input('Perform CRC check?'
                          'Enter "true" for yes and "false" for no [false]: ')
            if check.lower() in ('true', 't', 'yes', 'y'):
                check = True
            else:
                check = False
            recalc = input('Perform CRC recalculation?'
                           'Enter "true" for yes and "false" for no [false]: ')
            if recalc.lower() in ('true', 't', 'yes', 'y'):
                recalc = True
            else:
                recalc = False
            confirm = input("""Configuration change summary:
                            Interface: %s
                            New Speed: %s
                            New Duplex: %s
                            New Description: %s
                            Force TX (unidirectional): %s
                            CRC Check: %s
                            CRC Recalculation: %s
                            Split Interface: %s
                            Confirm changes [y/n]: """ % (interface, speed,
                                                          duplex, description,
                                                          forcetx, check,
                                                          recalc, split))
            if confirm.lower() in ('y', 'yes'):
                run = self.set_portconfig(interface, speed, duplex,
                                           description, forcetx, check,
                                           recalc, split)
            else:
                return "Canceling; no changes made.\n"
        elif self.generation == '4':
            forcetx = input('Force TX? Enter "true" for yes and "false" for no [false]: ')
            if forcetx.lower() in ('true', 't', 'yes', 'y'):
                forcetx = True
            else:
                forcetx = False
            check = input('Perform CRC check? '
                          'Enter "true" for yes and "false" for no [false]: ')
            if check.lower() in ('true', 't', 'yes', 'y'):
                check = True
            else:
                check = False
            recalc = input('Perform CRC recalculation? '
                           'Enter "true" for yes and "false" for no [false]: ')
            if recalc.lower() in ('true', 't', 'yes', 'y'):
                recalc = True
            else:
                recalc = False
            confirm = input("""Configuration change summary:
                            Interface: %s
                            New Speed: %s
                            New Duplex: %s
                            New Description: %s
                            Force TX (unidirectional): %s
                            CRC Check: %s
                            CRC Recalculation: %s
                            Confirm changes [y/n]: """ % (interface, speed,
                                                          duplex, description,
                                                          forcetx, check,
                                                          recalc))
            if confirm.lower() in ('y', 'yes'):
                run = self.set_portconfig(interface, speed, duplex,
                                          description, forcetx, check, recalc)
            else:
                return "Canceling; no changes made.\n"
        else:
            confirm = input("""Configuration change summary:
                            Interface: %s
                            New Speed: %s
                            New Duplex: %s
                            New Description: %s
                            Confirm changes [y/n]: """ % (interface, speed,
                                                          duplex, description))
            if confirm.lower() in ('y', 'yes'):
                run = self.set_portconfig(interface, speed, duplex, description)
            else:
                return "Canceling; no changes made.\n"
        print("""\nA device reboot is required for changes to take effect when changing
              between 1G and 10G on pre-G4 devices and when changing to or from breakout cables
              on QSFP ports of G4 devices. \n""")
        return run

    def set_portconfig(self, interface, speed, duplex, description='',
                        forcetx=False, check=False, recalc=False, split='false'):
        """Set configuration of a port on the Packetmaster.
        
           :param interface: A string, interface to configure e.g. eth-0-1.
           :param speed: A string, bandwidth speed setting for interface.
           :param duplex: A string, link duplex setting for interface.
           :param description: A string, description for interface.
           :param forcetx: A bool, force tx transmit (unidirectional) of interface.
           :param check: A bool, 'True' to perform CRC checking; 'False' to skip.
           :param recalc: A bool, Recalculate frame CRC; enable if slicing packets.
           :param split: A bool, Configure port to use breakout cable; only availble on QSFP ports.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/ports/config?'
        else:
            uri = 'http://' + self._address + '/rest/ports/config?'
        if_name = str(interface).strip()
        port_no = re.findall('[1-9][0-9/]*', if_name)
        if len(port_no) == 1:
            interface = 'eth-0-' + port_no[0]
        else:
            return "That is not a valid port number; canceling Set Port Config."
        if '/' not in port_no[0] and int(port_no[0]) > self.ports:
            return ("Port number does not exist on this device; "
                    "this device has %s ports. Canceling Set Port Config.\n" % self.ports)
        if self.generation == '4':
            if speed.lower() == 'auto':
                speed = 'auto'
            elif speed in ('1000', '10g', '10G', '40g', '40G', '100g', '100G'):
                speed = speed.upper()
            else:
                return "That is not a valid input for port speed; canceling Set Port Config.\n"
        else:
            if speed.lower() == 'auto':
                speed = 'auto'
            elif speed in ('10', '100', '1000', 'XG', 'xg', 'Xg', 'xG', '1g', '1G'):
                speed = speed.upper()
            else:
                return "That is not a valid input for port speed; canceling Set Port Config.\n"
        if speed in ('10', '100', '1000', 'auto'):
            duplex = duplex
        else:
            duplex = 'full'
        if not isinstance( forcetx, bool):
            return "forcetx must be a bool; canceling Set Port Config.\n"
        if not isinstance( check, bool):
            return "check must be a bool; canceling Set Port Config.\n"
        if not isinstance( recalc, bool):
            return "recalc must be a bool; canceling Set Port Config.\n"
        if split.lower() in ('true', 't', 'yes', 'y', 'break-out') or split == True:
            split = 'break-out'
        else:
            split = 'no'
        if self.generation == '4' and speed in ('40G', '100G'):
            data = {'if_name': interface,
                    'description': description,
                    'unidirectional': forcetx,
                    'crc_check': check,
                    'crc_recalculation': recalc,
                    'shutdown': False,
                    'split': split}
        elif self.generation == '4':
            data = {'if_name': interface,
                    'description': description,
                    'speed': speed,
                    'duplex': duplex,
                    'unidirectional': forcetx,
                    'crc_check': check,
                    'crc_recalculation': recalc,
                    'shutdown': False}
        elif self.generation == '3.1' and speed in ('1G', 'XG'):
            data = {'if_name': interface,
                    'description': description,
                    'speed': 'auto',
                    'duplex': duplex,
                    'xg_speed': speed,
                    'shutdown': False}
        else:
            data = {'if_name': interface,
                    'description': description,
                    'speed': speed,
                    'duplex': duplex,
                    'shutdown': False}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_portenable_guided(self):
        """Interactive menu for enabling/disabling a port on the Packetmaster.
        
           :returns: A string, JSON-formatted."""
        if_name = input('Enter the interface name of the port you want to change: ')
        shutdown = input('Enter "true" to disable port; '
                         'Enter "false" to activate port [false]: ')
        if shutdown.lower() in ('true', 't', 'yes', 'y'):
            shutdown = True
        else:
            shutdown = False
        confirm = input("""Configuration change summary:
                        Interface: %s
                        Shutdown: %s
                        Confirm changes [y/n]: """ % (if_name, shutdown))
        if confirm.lower() in ('y', 'yes'):
            run = self.set_portenable(if_name, shutdown)
            return run
        return "Canceling; no changes made.\n"

    def set_portenable(self, if_name, shutdown=False):
        """Enable/disable a port on the Packetmaster.

           :param if_name: A string, interface name e.g. eth-0-1.
           :param shutdown: A bool, True to disable, False to enable.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/ports/config?'
        else:
            uri = 'http://' + self._address + '/rest/ports/config?'
        if_name = str(if_name).strip()
        port_no = re.findall('[1-9][0-9/]*', if_name)
        interface = 'eth-0-' + port_no[0]
        if not isinstance(shutdown, bool):
            return "shutdown must be a bool; canceling Set Port Enable."
        data = {'if_name': interface, 'shutdown': shutdown}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_portinfo(self):
        """Return port information of Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/ports/info?'
        else:
            uri = 'http://' + self._address + '/rest/ports/info?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_portstat(self):
        """Return port counters of Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/ports/stats?'
        else:
            uri = 'http://' + self._address + '/rest/ports/stats?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_sfpinfo(self):
        """Return SFP information of any installed transceivers.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/ports/sfpstatus?'
        else:
            uri = 'http://' + self._address + '/rest/ports/sfpstatus?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            result = info['result']
            return json.dumps(result, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def del_portcounters(self):
        """Reset all port counters to zero.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make DELETE request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/ports/counters?'
        else:
            uri = 'http://' + self._address + '/rest/ports/counters?'
        try:
            response = requests.delete(uri, auth=(self.username, self.password))
            code = response.status_code
            if int(code) == 200:
                return 'Counters deleted successfully.'
            return 'Unable to delete counters.'
        except ConnectionError as error:
            raise error

    def del_rulecounters(self):
        """Reset all rule counters to zero.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make DELETE request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/rules/counters?'
        else:
            uri = 'http://' + self._address + '/rest/rules/counters?'
        try:
            response = requests.delete(uri, auth=(self.username, self.password))
            code = response.status_code
            if int(code) == 200:
                return 'Counters deleted successfully.'
            return 'Unable to delete counters.'
        except ConnectionError as error:
            raise error

    def get_rules(self):
        """Return any active rules/filters on the Packetmaster.
           
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/rules/all?'
        else:
            uri = 'http://' + self._address + '/rest/rules/all?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_rule_guided(self):
        """Interactive menu to add a rule/filter.
           
           :returns: A string, JSON-formatted.
           :raises: ValueError: If proto variable not an int in the range of 2-9."""
        data = {}
        rulename = input('Enter a name for the rule [none]: ')
        data['name'] = rulename
        ruledescrip = input('Enter a description for the rule [none]: ')
        data['description'] = ruledescrip
        priority = input('Enter the priority level of the rule; '
                         '0 - 65535 higher number = higher priority [32768]: ')
        if priority != '':
            if input_validation.pm_pri(priority):
                data['priority'] = int(priority)
            else:
                return "That is not a valid input for priority; canceling Add Rule."
        else:
            data['priority'] = 32768
        portin = input('Enter the port number or numbers for incoming traffic; '
                       'multiple ports separated by a comma: ')
        #Implement valid port number check against device
        data['match[in_port]'] = portin
        print('''\nMatch VLAN tag?
                1 - No, match all tagged and untagged traffic
                2 - No, match only untagged traffic
                3 - Yes, match a VLAN tag \n''')
        trafmatch = input('Enter the number of your selection [1]: ')
        if trafmatch == '' or int(trafmatch) == 1:
            pass
        elif int(trafmatch) == 2:
            data['match[vlan]'] = 'neg_match'
        elif int(trafmatch) == 3:
            data['match[vlan]'] = 'match'
            matchid = input('Enter the VLAN ID to filter on: ')
            if input_validation.vlan(matchid):
                data['match[vlan_id]'] = matchid
            else:
                return "That is not a valid VLAN ID; canceling Add Rule."
            vpri = input('Enter a VLAN priority? Enter 0-7 orleave blank for none: ')
            if vpri != '' and input_validation.vlan_pri(vpri):
                data['match[vlan_priority]'] = vpri
            elif vpri == '':
                data['match[vlan_priority]'] = '0'
            else:
                return "That is not a valid VLAN Priority; canceling Add Rule."
        else:
            return "That is not a valid selection; canceling Add Rule \n"
        macsrc = input('Filter by source MAC address? '
                       'Leave blank for no or enter MAC address: ')
        if macsrc != '':
            if input_validation.mac(macsrc) != 0:
                data['match[dl_src]'] = input_validation.mac(macsrc)
            else:
                return "That is not a valid MAC address; canceling Add Rule."
        macdst = input('Filter by destination MAC address? '
                       'Leave blank for no or enter MAC address: ')
        if macdst != '':
            if input_validation.mac(macdst) != 0:
                data['match[dl_dst]'] = input_validation.mac(macdst)
            else:
                return "That is not a valid MAC address; canceling Add Rule."
        proto_options = {2: 'ip',
                         3: 'tcp',
                         4: 'udp',
                         5: 'sctp',
                         6: 'icmp',
                         7: 'arp',
                         8: 'custom'}
        print('''\nFilter on protocol?
                1 - No Protocol Filtering
                2 - IP
                3 - TCP
                4 - UDP
                5 - SCTP
                6 - ICMP
                7 - ARP
                8 - Enter Ethertype\n''')
                #Add MPLS for G4 devices
        proto = input('Enter the number of your selection [1]: ')
        if proto == '' or int(proto) == 1:
            pass
        else:
            try:
                if int(proto) in range(2, 9):
                    data['match[protocol]'] = proto_options[int(proto)]
                else:
                    return "That is not a valid selection; canceling Add Rule \n"
            except ValueError as reason:
                return("That is not a valid input; canceling Add Rule", reason)
            if data['match[protocol]'] in ('ip', 'tcp', 'udp', 'sctp', 'icmp'):
                nwsrc = input('Filter on source IP address? '
                              'Leave blank for no or enter IP address + optional mask'
                              '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                              'or "192.168.1.5/24"): ')
                if nwsrc != '':
                    if input_validation.ipv4_mask(nwsrc) != 0:
                        data['match[nw_src]'] = input_validation.ipv4_mask(nwsrc)
                    else:
                        return "That is not a valid IP address; canceling Add Rule."
                nwdst = input('Filter on destination IP address? '
                              'Leave blank for no or enter IP address + optional mask'
                              '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                              'or "192.168.1.5/24"): ')
                if nwdst != '':
                    if input_validation.ipv4_mask(nwdst) != 0:
                        data['match[nw_dst]'] = input_validation.ipv4_mask(nwdst)
                    else:
                        return "That is not a valid IP address; canceling Add Rule."
            if data['match[protocol]'] == 'ip':
                nwproto = input('Enter protocol number '
                                '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
            if data['match[protocol]'] in ('tcp', 'udp', 'sctp'):
                tp_src = input('Filter on source port? '
                               'Leave blank for no or enter port number: ')
                if tp_src != '':
                    if input_validation.port(tp_src):
                        data['match[' + data['match[protocol]'] + '_src]'] = tp_src
                    else:
                        return "That is not a valid port number; canceling Add Rule."
                tp_dst = input('Filter on destination port? '
                               'Leave blank for no or enter port number: ')
                if tp_dst != '':
                    if input_validation.port(tp_dst):
                        data['match[' + data['match[protocol]'] + '_dst]'] = tp_dst
                    else:
                        return "That is not a valid port number; canceling Add Rule."
            if data['match[protocol]'] == 'icmp':
                icmpt = input('Filter on ICMP type? '
                              'Leave blank for no or enter ICMP type number: ')
                if icmpt != '':
                    if input_validation.icmp_type(icmpt):
                        data['match[icmp_type]'] = icmpt
                    else:
                        return "That is not a valid ICMP Type; canceling Add Rule."
                icmpc = input('Filter on ICMP code? '
                              'Leave blank for no or enter ICMP code number: ')
                if icmpc != '':
                    if input_validation.icmp_code(icmpc):
                        data['match[icmp_code]'] = icmpc
                    else:
                        return "That is not a valid ICMP Code; canceling Add Rule."
            if data['match[protocol]'] == 'custom':
                ether = input('Enter Ethertype e.g. 0x0800: ')
                if ether != '':
                    data['match[dl_type]'] = ether
                nwproto = input('Enter protocol number '
                                '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
        print('''\nAdd Custom Extra Match?
        e.g. hard_timeout, idle_timeout, tcp_flags, Q in Q
        Leave blank for none
        Improper syntax will cause Add Rule to fail \n''')
        extra = input('Enter Extra Custom Match String: ')
        if extra != '':
            data['match[extra]'] = extra
        ruleaction = input('\nEnter the desired output actions separated by commas; '
                           'order matters - improper syntax will cause Add Rule to fail: ')
        data['actions'] = ruleaction
        check_data = json.dumps(data, indent=4)
        confirm = input("""Configuration change summary:
                        Rule Parameters: %s
                        Confirm changes [y/n]: """ % check_data)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_rule(data)
            return run
        return "Canceling; no changes made.\n"

    def set_rule(self, data):
        """Add a rule/filter to the Packetmaster.
        
           :param data: A dict, dictionary containing all valid rule parameters
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        #Need to validate input in dict
        if self.__https:
            uri = 'https://' + self._address + '/rest/rules?'
        else:
            uri = 'http://' + self._address + '/rest/rules?'
        if not isinstance(data, dict):
            return ("That is not a valid format for rule; "
                    "please provide a dictionary object with valid rule parameters.")
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_rule_guided(self):
        """Interactive menu to modify a rule/filter on the Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ValueError: If proto variable not an int in the range of 2-9."""
        data = {}
        name = input('Enter a new name for the rule: ')
        data['name'] = name
        cookie = input('Enter the cookie of the rule to modify: ')
        data['cookie'] = cookie
        description = input('Enter a new description for the rule: ')
        data['description'] = description
        priority = input('Enter the priority of the rule (priority cannot be changed; '
                         'must match rule to be modified)[32768]: ')
        if priority != '':
            if input_validation.pm_pri(priority):
                data['priority'] = int(priority)
            else:
                return "That is not a valid input for priority; canceling Modify Rule."
        else:
            priority = 32768
        in_port = input("What is (are) the input port(s)for the rule separated by commas: ")
        data['match[in_port]'] = in_port
        print("For the following input filters the selected option must match "
              "the rule being modified; these fields cannot be changed.")
        print('''\nIs the rule matching a VLAN tag?
                1 - No, matching all tagged and untagged traffic
                2 - No, matching only untagged traffic
                3 - Yes, matching a VLAN tag \n''')
        trafmatch = input('Enter the number of your selection [1]: ')
        if trafmatch == '' or int(trafmatch) == 1:
            pass
        elif int(trafmatch) == 2:
            data['match[vlan]'] = 'neg_match'
        elif int(trafmatch) == 3:
            data['match[vlan]'] = 'match'
            matchid = input('Enter the VLAN ID the rule is filtering: ')
            if input_validation.vlan(matchid):
                data['match[vlan_id]'] = matchid
            else:
                return "That is not a valid VLAN ID; canceling Modify Rule."
            vpri = input('Enter the VLAN priority? Enter 0-7 or leave blank for none: ')
            if vpri != '' and input_validation.vlan_pri(vpri):
                data['match[vlan_priority]'] = vpri
            elif vpri == '':
                data['match[vlan_priority]'] = '0'
            else:
                return "That is not a valid VLAN Priority; canceling Modify Rule."
        else:
            return "That is not a valid selection; canceling Modify Rule \n"
        macsrc = input('Filtering by source MAC address? '
                       'Leave blank for no or enter MAC address: ')
        if macsrc != '':
            if input_validation.mac(macsrc) != 0:
                data['match[dl_src]'] = input_validation.mac(macsrc)
            else:
                return "That is not a valid MAC address; canceling Modify Rule."
        macdst = input('Filtering by destination MAC address? '
                       'Leave blank for no or enter MAC address: ')
        if macdst != '':
            if input_validation.mac(macdst) != 0:
                data['match[dl_dst]'] = input_validation.mac(macdst)
            else:
                return "That is not a valid MAC address; canceling Modify Rule."
        proto_options = {2: 'ip',
                         3: 'tcp',
                         4: 'udp',
                         5: 'sctp',
                         6: 'icmp',
                         7: 'arp',
                         8: 'custom'}
        print('''\nFiltering on a protocol?
                1 - No Protocol Filtering
                2 - IP
                3 - TCP
                4 - UDP
                5 - SCTP
                6 - ICMP
                7 - ARP
                8 - Enter Ethertype\n''')
                #Add MPLS for G4 devices
        proto = input('Enter the number of your selection [1]: ')
        if proto == '' or int(proto) == 1:
            pass
        else:
            try:
                if int(proto) in range(2, 9):
                    data['match[protocol]'] = proto_options[int(proto)]
                else:
                    return "That is not a valid selection; canceling Modify Rule \n"
            except ValueError as reason:
                return("That is not a valid input; canceling Modify Rule", reason)
            if data['match[protocol]'] in ('ip', 'tcp', 'udp', 'sctp', 'icmp'):
                nwsrc = input('Filtering on a source IP address? '
                              'Leave blank for no or enter IP address + optional mask'
                              '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                              'or "192.168.1.5/24"): ')
                if nwsrc != '':
                    if input_validation.ipv4_mask(nwsrc) != 0:
                        data['match[nw_src]'] = input_validation.ipv4_mask(nwsrc)
                    else:
                        return "That is not a valid IP address; canceling Modify Rule."
                nwdst = input('Filtering on a destination IP address? '
                              'Leave blank for no or enter IP address + optional mask'
                              '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                              'or "192.168.1.5/24"): ')
                if nwdst != '':
                    if input_validation.ipv4_mask(nwdst) != 0:
                        data['match[nw_dst]'] = input_validation.ipv4_mask(nwdst)
                    else:
                        return "That is not a valid IP address; canceling Modify Rule."
            if data['match[protocol]'] == 'ip':
                nwproto = input('Filtering on a protocol number? '
                                '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
            if data['match[protocol]'] in ('tcp', 'udp', 'sctp'):
                tp_src = input('Filtering on a source port? '
                               'Leave blank for no or enter port number: ')
                if tp_src != '':
                    if input_validation.port(tp_src):
                        data['match[' + data['match[protocol]'] + '_src]'] = tp_src
                    else:
                        return "That is not a valid port number; canceling Modify Rule."
                tp_dst = input('Filtering on a destination port? '
                               'Leave blank for no or enter port number: ')
                if tp_dst != '':
                    if input_validation.port(tp_dst):
                        data['match[' + data['match[protocol]'] + '_dst]'] = tp_dst
                    else:
                        return "That is not a valid port number; canceling Modify Rule."
            if data['match[protocol]'] == 'icmp':
                icmpt = input('Filtering on ICMP type? '
                              'Leave blank for no or enter ICMP type number: ')
                if icmpt != '':
                    if input_validation.icmp_type(icmpt):
                        data['match[icmp_type]'] = icmpt
                    else:
                        return "That is not a valid ICMP Type; canceling Modify Rule."
                icmpc = input('Filtering on ICMP code? '
                              'Leave blank for no or enter ICMP code number: ')
                if icmpc != '':
                    if input_validation.icmp_code(icmpc):
                        data['match[icmp_code]'] = icmpc
                    else:
                        return "That is not a valid ICMP Code; canceling Modify Rule."
            if data['match[protocol]'] == 'custom':
                ether = input('Enter Ethertype e.g. 0x0800: ')
                if ether != '':
                    data['match[dl_type]'] = ether
                nwproto = input('Enter protocol number '
                                '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
        print('''\nUsing Custom Extra Match?
        e.g. hard_timeout, idle_timeout, tcp_flags, Q in Q
        Leave blank for none
        Improper syntax will cause Delete Rule to fail \n''')
        extra = input('Enter Extra Custom Match String: ')
        if extra != '':
            data['match[extra]'] = extra
        ruleaction = input('Enter the new output actions separated by commas; '
                           'order matters - improper syntax will cause Modify Rule to fail: ')
        data['actions'] = ruleaction
        check_data = json.dumps(data, indent=4)
        confirm = input("""Configuration change summary:
                        Modified Rule Parameters: %s
                        Confirm changes [y/n]: """ % check_data)
        if confirm.lower() in ('y', 'yes'):
            run = self.mod_rule(data)
            return run
        return "Canceling; no changes made.\n"

    def mod_rule(self, data):
        """Modify a rule/filter on the Packetmaster.
        
           :param data: A dict, dictionary containing all valid rule parameters.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make PUT request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/rules?'
        else:
            uri = 'http://' + self._address + '/rest/rules?'
        if not isinstance(data, dict):
            return ("That is not a valid format for rule; "
                    "please provide a dictionary object with valid rule parameters.")
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def del_rule_guided(self):
        """Interactive menu to delete a rule/filter.
        
           :raises: ValueError: If priority variable cannot be converted to int.
           :raises: ValueError: If proto variable cannot be converted to int in range 2 to 9."""
        priority = input("What is the priority of the rule to delete: ")
        try:
            priority = int(priority)
        except ValueError as reason:
            return ("That is not a valid input for rule priority; canceling Delete Rule.", reason)
        if priority < 0 or priority > 65535:
            print("That is not a valid input for rule priority; canceling Delete Rule.")
        in_port = input("What is (are) the input port(s)for the rule separated by commas: ")
        data = {'priority': priority,
                'match[in_port]': in_port}
        print('''\nIs the rule matching a VLAN tag?
                1 - No, matching all tagged and untagged traffic
                2 - No, matching only untagged traffic
                3 - Yes, matching a VLAN tag \n''')
        trafmatch = input('Enter the number of your selection [1]: ')
        if trafmatch == '' or int(trafmatch) == 1:
            pass
        elif int(trafmatch) == 2:
            data['match[vlan]'] = 'neg_match'
        elif int(trafmatch) == 3:
            data['match[vlan]'] = 'match'
            matchid = input('Enter the VLAN ID the rule is filtering: ')
            if input_validation.vlan(matchid):
                data['match[vlan_id]'] = matchid
            else:
                return "That is not a valid VLAN ID; canceling Delete Rule."
            vpri = input('Enter the VLAN priority? Enter 0-7 or leave blank for none: ')
            if vpri != '' and input_validation.vlan_pri(vpri):
                data['match[vlan_priority]'] = vpri
            elif vpri == '':
                data['match[vlan_priority]'] = '0'
            else:
                return "That is not a valid VLAN Priority; canceling Delete Rule."
        else:
            return "That is not a valid selection; canceling Delete Rule \n"
        macsrc = input('Filtering by source MAC address? '
                       'Leave blank for no or enter MAC address: ')
        if macsrc != '':
            data['match[dl_src]'] = macsrc
        macdst = input('Filtering by destination MAC address? '
                       'Leave blank for no or enter MAC address: ')
        if macdst != '':
            data['match[dl_dst]'] = macdst
        proto_options = {2: 'ip',
                         3: 'tcp',
                         4: 'udp',
                         5: 'sctp',
                         6: 'icmp',
                         7: 'arp',
                         8: 'custom'}
        print('''\nFiltering on a protocol?
                1 - No Protocol Filtering
                2 - IP
                3 - TCP
                4 - UDP
                5 - SCTP
                6 - ICMP
                7 - ARP
                8 - Enter Ethertype\n''')
                #Add MPLS for G4 devices
        proto = input('Enter the number of your selection [1]: ')
        if proto == '' or int(proto) == 1:
            pass
        else:
            try:
                if int(proto) in range(2, 9):
                    data['match[protocol]'] = proto_options[int(proto)]
                else:
                    return "That is not a valid selection; canceling Delete Rule \n"
            except ValueError as reason:
                return("That is not a valid input; canceling Delete Rule", reason)
            if data['match[protocol]'] in ('ip', 'tcp', 'udp', 'sctp', 'icmp'):
                nwsrc = input('Filtering on a source IP address? '
                              'Leave blank for no or enter IP address + optional mask'
                              '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                              'or "192.168.1.5/24"): ')
                if nwsrc != '':
                    if input_validation.ipv4_mask(nwsrc) != 0:
                        data['match[nw_src]'] = input_validation.ipv4_mask(nwsrc)
                    else:
                        return "That is not a valid IP address; canceling Delete Rule."
                nwdst = input('Filtering on a destination IP address? '
                              'Leave blank for no or enter IP address + optional mask'
                              '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                              'or "192.168.1.5/24"): ')
                if nwdst != '':
                    if input_validation.ipv4_mask(nwdst) != 0:
                        data['match[nw_dst]'] = input_validation.ipv4_mask(nwdst)
                    else:
                        return "That is not a valid IP address; canceling Delete Rule."
            if data['match[protocol]'] == 'ip':
                nwproto = input('Filtering on a protocol number? '
                                '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
            if data['match[protocol]'] in ('tcp', 'udp', 'sctp'):
                tp_src = input('Filtering on a source port? '
                               'Leave blank for no or enter port number: ')
                if tp_src != '':
                    if input_validation.port(tp_src):
                        data['match[' + data['match[protocol]'] + '_src]'] = tp_src
                    else:
                        return "That is not a valid port number; canceling Delete Rule."
                tp_dst = input('Filtering on a destination port? '
                               'Leave blank for no or enter port number: ')
                if tp_dst != '':
                    if input_validation.port(tp_dst):
                        data['match[' + data['match[protocol]'] + '_dst]'] = tp_dst
                    else:
                        return "That is not a valid port number; canceling Delete Rule."
            if data['match[protocol]'] == 'icmp':
                icmpt = input('Filtering on ICMP type? '
                              'Leave blank for no or enter ICMP type number: ')
                if icmpt != '':
                    if input_validation.icmp_type(icmpt):
                        data['match[icmp_type]'] = icmpt
                    else:
                        return "That is not a valid ICMP Type; canceling Delete Rule."
                icmpc = input('Filtering on ICMP code? '
                              'Leave blank for no or enter ICMP code number: ')
                if icmpc != '':
                    if input_validation.icmp_code(icmpc):
                        data['match[icmp_code]'] = icmpc
                    else:
                        return "That is not a valid ICMP Code; canceling Delete Rule."
            if data['match[protocol]'] == 'custom':
                ether = input('Enter Ethertype e.g. 0x0800: ')
                if ether != '':
                    data['match[dl_type]'] = ether
                nwproto = input('Enter protocol number '
                                '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
        print('''\nUsing Custom Extra Match?
        e.g. hard_timeout, idle_timeout, tcp_flags, Q in Q
        Leave blank for none
        Improper syntax will cause Delete Rule to fail \n''')
        extra = input('Enter Extra Custom Match String: ')
        if extra != '':
            data['match[extra]'] = extra
        check_data = json.dumps(data, indent=4)
        confirm = input("""Configuration change summary:
                        Delete Rule Matching: %s
                        Confirm changes [y/n]: """ % check_data)
        if confirm.lower() in ('y', 'yes'):
            run = self.del_rule(data)
            return run
        return "Canceling; no changes made.\n"

    def del_rule(self, data):
        """Delete a rule/filter from the Packetmaster.
        
           :param data: A dict, dictionary containing all valid rule parameters.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make DELETE request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/rules?'
        else:
            uri = 'http://' + self._address + '/rest/rules?'
        if not isinstance(data, dict):
            return ("That is not a valid format for rule; "
                    "please provide a dictionary object with valid rule parameters.")
        try:
            response = requests.delete(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def del_rule_all(self):
        """Delete all rules from the Packetmaster.
        
        :returns: A string, JSON-formatted.
        :raises: ConnectionError: if unable to successfully make DELETE request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/rules/all?'
        else:
            uri = 'http://' + self._address + '/rest/rules/all?'
        try:
            response = requests.delete(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_groups(self):
        """Return any active port groups on the Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/groups/all?'
        else:
            uri = 'http://' + self._address + '/rest/groups/all?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def add_group_guided(self):
        """Interactive menu for adding a port group.
        
           :raises: ValueError: If group_type variable cannot be converted to int.
           :raises: ValueError: If buckets variable cannot be converted to int.
           :raises: ValueError: If output variable cannot be converted to int.
           :raises: ValueError: If watch variable cannot be converted to int."""
        gid = input("Enter the group ID: ")
        if not input_validation.group_id(gid):
            return "That is not a valid group ID, canceling Add Group."
        existing = []
        all_groups = self.get_groups()
        json_groups = json.loads(all_groups)
        count = 0
        for group in json_groups['groups']:
            existing.append(json_groups['groups'][count]['group_id'])
            count += 1
        if gid in existing:
            return ("A group with this group ID already exists; "
                    "use Modify Group or select a different group ID. Canceling Add Group")
        description = input("Enter the group description: ")
        group_type = input(""" Select the group type:
                               1 - All
                               2 - Select
                               3 - Fast Failover
                               Enter the number of your selection: """)
        try:
            group_type = int(group_type)
        except ValueError as reason:
            return ("That is not a valid group type selection; canceling Add Group.", reason)
        if group_type == 1:
            type_group = 'all'
        elif group_type == 2:
            type_group = 'select'
        elif group_type == 3:
            type_group = 'ff'
        else:
            return "That is not a valid group type selection; canceling Add Group."
        bucket_list = []
        buckets = input("How many buckets in this port group? "
                        "Must be at least 2 and no more than 16: ")
        try:
            buckets = int(buckets)
        except ValueError as reason:
            return ("That is not a valid bucket number; canceling Add Group.", reason)
        if buckets >= 2 and buckets <= 16:
            for bucket in xrange(buckets):
                print("\nConfigure settings for bucket %s" % bucket)
                #Add check against number of ports on device
                output = input("Output on which port: ")
                #Validate if port exists on device
                try:
                    int(output)
                    output = 'output:' + output
                except ValueError as reason:
                    return ("That is not a valid port number; canceling Add Group", reason)
                actions = output
                if self.generation != '4' or group_type == 3:
                    watch = input("Set watch port to: ")
                    try:
                        int(watch)
                    except ValueError as reason:
                        return ("That is not a valid port number; canceling Add Group", reason)
                push_vlan = input('Push VLAN ID to outout traffic? '
                                  'Enter VLAN ID or leave blank for no: ').strip()
                if push_vlan != '':
                    if input_validation.vlan(push_vlan):
                        vlan = str(int(push_vlan) + 4096)
                        vlan = 'push_vlan:0x8100,set_field:' + vlan + '->vlan_vid,'
                        actions = vlan + actions
                    else:
                        return "That is not a valid VLAN ID, canceling Add Group."
                else:
                    mod_vlan = input('Modify VLAN ID of output traffic? '
                                     'Enter VLAN ID or leave blank for no: ').strip()
                    if mod_vlan != '':
                        if input_validation.vlan(mod_vlan):
                            vlan = str(int(mod_vlan) + 4096)
                            vlan = 'set_field:' + vlan + '->vlan_vid,'
                            actions = vlan + actions
                        else:
                            return ("That is not a valid input for VLAN ID, "
                                    "canceling Add Group.")
                    else:
                        strip_vlan = input('Strip VLAN ID from output traffic? '
                                           'Y or N [N]: ').lower()
                        if strip_vlan in ('y', 'yes'):
                            actions = 'strip_vlan,' + actions
                if self.generation == '4':
                    pop_l2 = input('Pop all L2 information from packet?  Y or N [N]: ').lower()
                    if pop_l2 in ('y', 'yes'):
                        actions = 'pop_l2,' + actions
                if self.generation == '4':
                    pop_mpls = input('Pop MPLS tags? In most cases you should also push L2. '
                                     'Y or N [N]: ').lower()
                    if pop_mpls in ('y', 'yes'):
                        actions = 'pop_all_mpls,' + actions
                if self.generation == '4':
                    push_l2 = input('Push L2 information to output packets? '
                                    'Y or N [N]: ').lower()
                    if push_l2 in ('y', 'yes'):
                        print ("Be sure to modify destination MAC when prompted, "
                               "else an error will occur.")
                        actions = 'push_l2,' + actions
                src_mac = input('Modify source MAC address? '
                                'Enter new MAC address or leave blank for no: ').strip()
                if src_mac != '':
                    if input_validation.mac(src_mac) != 0:
                        src_mac = input_validation.mac(src_mac)
                        actions = 'set_field:' + src_mac + '->eth_src,' + actions
                    else:
                        return "That is not a valid MAC address, canceling Add Group."
                dst_mac = input('Modify destination MAC address? '
                                'Enter new MAC address or leave blank for no: ').strip()
                if dst_mac != '':
                    if input_validation.mac(dst_mac) != 0:
                        src_mac = input_validation.mac(dst_mac)
                        actions = 'set_field:' + dst_mac + '->eth_dst,' + actions
                    else:
                        return "That is not a valid MAC address, canceling Add Group."
                dst_ip = input('Modify destination IP address? '
                               'Enter new IP address or leave blank for no: ').strip()
                if dst_ip != '':
                    if input_validation.ipv4_mask(dst_ip) != 0:
                        actions = 'set_field:' + input_validation.ipv4_mask(dst_ip) + \
                                  '->ip_dst,' + actions
                    else:
                        return ("That is not a valid input for IP address, "
                                "canceling Add Group.")
                if self.generation == '4':
                    src_udp = input('Modify source UDP port? '
                                    'Enter new port number or leave blank for no: ').strip()
                    if src_udp != '':
                        if input_validation.port(src_udp):
                            actions = 'set_field:' + src_udp + '->udp_src,' + actions
                        else:
                            return ("That is not a valid input for port number; "
                                    "canceling Add Group.")
                dst_udp = input('Modify destination UDP port? '
                                'Enter new port number or leave blank for no: ').strip()
                if dst_udp != '':
                    if input_validation.port(dst_udp):
                        actions = 'set_field:' + dst_udp + '->udp_dst,' + actions
                    else:
                        return ("That is not a valid input for port number; "
                                "canceling Add Group.")
                if self.generation == '4':
                    src_tcp = input('Modify source TCP port? '
                                    'Enter new port number or leave blank for no: ').strip()
                    if src_tcp != '':
                        if input_validation.port(src_tcp):
                            actions = 'set_field:' + src_tcp + '->tcp_src,' + actions
                        else:
                            return ("That is not a valid input for port number; "
                                    "canceling Add Group.")
                dst_tcp = input('Modify destination TCP port? '
                                'Enter new port number or leave blank for no: ').strip()
                if dst_tcp != '':
                    if input_validation.port(dst_tcp):
                        actions = 'set_field:' + dst_tcp + '->tcp_dst,' + actions
                    else:
                        return ("That is not a valid input for port number; "
                                "canceling Add Group.")
                if self.generation != '4' or group_type == 3:
                    bucket_data = {'actions': actions,
                                     'watch_port': watch}
                else:
                    bucket_data = {'actions': actions}
                bucket_list.append(bucket_data)
        else:
            return "That is not a valid bucket number; canceling Add Group."
        data = {'buckets': bucket_list,
                  'group_id': gid,
                  'type': type_group,
                  'description': description
                 }
        check_data = json.dumps(data, indent=4)
        confirm = input("""Configuration change summary:
                        Add Group Parameters: %s
                        Confirm changes [y/n]: """ % check_data)
        if confirm.lower() in ('y', 'yes'):
            run = self.add_group(gid, data)
            return run
        return "Canceling; no changes made.\n"

    def add_group(self, gid, json_app):
        """Add a port group to the Packetmaster.
        
           :param gid: A string, ID of group e.g. 0-4294967040.
           :param json_app: A dict, dictionary containing all valid group parameters.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/groups?'
        else:
            uri = 'http://' + self._address + '/rest/groups?'
        if not input_validation.group_id(gid):
            return "That is not a valid group ID, canceling Add Group."
        existing = []
        all_groups = self.get_groups()
        json_groups = json.loads(all_groups)
        count = 0
        for group in json_groups['groups']:
            existing.append(json_groups['groups'][count]['group_id'])
            count += 1
        if gid in existing:
            return ("A group with this group ID already exists; "
                    "use Modify Group or select a different group ID. Canceling Add Group")
        if not isinstance(json_app, dict):
            return "That is not a valid dictionary input for Add Group; canceling Add Group."
        try:
            response = requests.post(uri, json=json_app, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_group_guided(self):
        """Interactive menu to modify a port group.

           :raises: ValueError: If buckets variable cannot be converted to int.
           :raises: ValueError: If output variable cannot be converted to int.
           :raises: ValueError: If watch variable cannot be converted to int."""
        gid = input("Enter the group ID of the group you would like to modify: ")
        if not input_validation.group_id(gid):
            return "That is not a valid group ID, canceling Modify Group."
        existing = []
        all_groups = self.get_groups()
        json_groups = json.loads(all_groups)
        count = 0
        for group in json_groups['groups']:
            existing.append(json_groups['groups'][count]['group_id'])
            if json_groups['groups'][count]['group_id'] == gid:
                group_type = json_groups['groups'][count]['type']
            count += 1
        if gid not in existing:
            return ("A group with this group ID does not exist; "
                    "use Add Group. Canceling Modify Group")
        description = input("Enter the new group description or "
                            "leave blank to retain original: ")
        bucket_list = []
        buckets = input("How many buckets in this port group? "
                        "Must be at least 2 and no more than 16: ")
        try:
            buckets = int(buckets)
        except ValueError as reason:
            return ("That is not a valid bucket number; canceling Modify Group.", reason)
        if buckets >= 2 and buckets <= 16:
            for bucket in xrange(buckets):
                print("\nConfigure settings for bucket %s" % bucket)
                #Add check against number of ports on device
                output = input("Output on which port: ")
                try:
                    int(output)
                    output = 'output:' + output
                except ValueError as reason:
                    return ("That is not a valid port number; canceling Modify Group", reason)
                actions = output
                if self.generation != '4' or group_type == 'ff':
                    watch = input("Set watch port to: ")
                    try:
                        int(watch)
                    except ValueError as reason:
                        return ("That is not a valid port number; canceling Modify Group", reason)
                push_vlan = input('Push VLAN ID to outout traffic? '
                                  'Enter VLAN ID or leave blank for no: ').strip()
                if push_vlan != '':
                    if input_validation.vlan(push_vlan):
                        vlan = str(int(push_vlan) + 4096)
                        vlan = 'push_vlan:0x8100,set_field:' + vlan + '->vlan_vid,'
                        actions = vlan + actions
                    else:
                        return "That is not a valid VLAN ID, canceling Modify Group."
                else:
                    mod_vlan = input('Modify VLAN ID of output traffic? '
                                     'Enter VLAN ID or leave blank for no: ').strip()
                    if mod_vlan != '':
                        if input_validation.vlan(mod_vlan):
                            vlan = str(int(mod_vlan) + 4096)
                            vlan = 'set_field:' + vlan + '->vlan_vid,'
                            actions = vlan + actions
                        else:
                            return ("That is not a valid input for VLAN ID, "
                                    "canceling Modify Group.")
                    else:
                        strip_vlan = input('Strip VLAN ID from output traffic? '
                                           'Y or N [N]: ').lower()
                        if strip_vlan == 'y' or strip_vlan == 'yes':
                            actions = 'strip_vlan,' + actions
                if self.generation == '4':
                    pop_l2 = input('Pop all L2 information from packet?  Y or N [N]: ').lower()
                    if pop_l2 == 'y' or pop_l2 == 'yes':
                        actions = 'pop_l2,' + actions
                if self.generation == '4':
                    pop_mpls = input('Pop MPLS tags? In most cases you should also push L2. '
                                     'Y or N [N]: ').lower()
                    if pop_mpls == 'y' or pop_mpls == 'yes':
                        actions = 'pop_all_mpls,' + actions
                if self.generation == '4':
                    push_l2 = input('Push L2 information to output packets? '
                                    'Y or N [N]: ').lower()
                    if push_l2 == 'y' or push_l2 == 'yes':
                        print ("Be sure to modify destination MAC when prompted, "
                               "else an error will occur.")
                        actions = 'push_l2,' + actions
                src_mac = input('Modify source MAC address? '
                                'Enter new MAC address or leave blank for no: ').strip()
                if src_mac != '':
                    if input_validation.mac(src_mac) != 0:
                        src_mac = input_validation.mac(src_mac)
                        actions = 'set_field:' + src_mac + '->eth_src,' + actions
                    else:
                        return "That is not a valid MAC address, canceling Modify Group."
                dst_mac = input('Modify destination MAC address? '
                                'Enter new MAC address or leave blank for no: ').strip()
                if dst_mac != '':
                    if input_validation.mac(dst_mac) != 0:
                        src_mac = input_validation.mac(dst_mac)
                        actions = 'set_field:' + dst_mac + '->eth_dst,' + actions
                    else:
                        return "That is not a valid MAC address, canceling Modify Group."
                dst_ip = input('Modify destination IP address? '
                               'Enter new IP address or leave blank for no: ').strip()
                if dst_ip != '':
                    if input_validation.ipv4_mask(dst_ip) != 0:
                        actions = 'set_field:' + input_validation.ipv4_mask(dst_ip) + \
                                  '->ip_dst,' + actions
                    else:
                        return ("That is not a valid input for IP address, "
                                "canceling Modify Group.")
                if self.generation == '4':
                    src_udp = input('Modify source UDP port? '
                                    'Enter new port number or leave blank for no: ').strip()
                    if src_udp != '':
                        if input_validation.port(src_udp):
                            actions = 'set_field:' + src_udp + '->udp_src,' + actions
                        else:
                            return ("That is not a valid input for port number; "
                                    "canceling Modify Group.")
                dst_udp = input('Modify destination UDP port? '
                                'Enter new port number or leave blank for no: ').strip()
                if dst_udp != '':
                    if input_validation.port(dst_udp):
                        actions = 'set_field:' + dst_udp + '->udp_dst,' + actions
                    else:
                        return ("That is not a valid input for port number; "
                                "canceling Modify Group.")
                if self.generation == '4':
                    src_tcp = input('Modify source TCP port? '
                                    'Enter new port number or leave blank for no: ').strip()
                    if src_tcp != '':
                        if input_validation.port(src_tcp):
                            actions = 'set_field:' + src_tcp + '->tcp_src,' + actions
                        else:
                            return ("That is not a valid input for port number; "
                                    "canceling Modify Group.")
                dst_tcp = input('Modify destination TCP port? '
                                'Enter new port number or leave blank for no: ').strip()
                if dst_tcp != '':
                    if input_validation.port(dst_tcp):
                        actions = 'set_field:' + dst_tcp + '->tcp_dst,' + actions
                    else:
                        return ("That is not a valid input for port number; "
                                "canceling Modify Group.")
                if self.generation != '4' or group_type == 'ff':
                    bucket_data = {'actions': actions,
                                     'watch_port': watch}
                else:
                    bucket_data = {'actions': actions}
                bucket_list.append(bucket_data)
        else:
            return "That is not a valid bucket number; canceling Modify Group."
        data = {'buckets': bucket_list,
                  'group_id': gid,
                  'type': group_type,
                  'description': description}
        check_data = json.dumps(data, indent=4)
        confirm = input("""Configuration change summary:
                        Modified Group Parameters: %s
                        Confirm changes [y/n]: """ % check_data)
        if confirm.lower() in ('y', 'yes'):
            run = self.mod_group(gid, data)
            return run
        return "Canceling; no changes made.\n"

    def mod_group(self, gid, json_app):
        """Modify a port group on the Packetmaster.
        
           :param gid: A string, ID of group e.g. 0-4294967040.
           :param json_app: A dict, dictionary containing all valid group parameters.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make PUT request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/groups?'
        else:
            uri = 'http://' + self._address + '/rest/groups?'
        if not input_validation.group_id(gid):
            return "That is not a valid group ID, canceling Modify Group."
        existing = []
        all_groups = self.get_groups()
        json_groups = json.loads(all_groups)
        count = 0
        for group in json_groups['groups']:
            existing.append(json_groups['groups'][count]['group_id'])
            count += 1
        if gid not in existing:
            return ("A group with this group ID does not exist; use Add Group. "
                    "Canceling Modify Group.")
        if not isinstance(json_app, dict):
            return "That is not a valid dictionary input for Modify Group; canceling Modify Group."
        try:
            response = requests.put(uri, json=json_app, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def delete_group_guided(self):
        """Interactive menu to delete a port group.

           :returns: A string, JSON-formatted.
           :raises: ValueError: If gid variable cannot be converted to int."""
        gid = input("Enter the group ID of the group to be deleted: ")
        try:
            int(gid)
        except ValueError as reason:
            return ("That is not a valid group ID, canceling Delete Group.", reason)
        confirm = input("""Configuration Change Summary:
                        Delete Group ID: %s
                        Confirm changes [y/n]: """ % gid)
        if confirm.lower() in ('y', 'yes'):
            run = self.delete_group(gid)
            return run
        return "Canceling; no changes made.\n"

    def delete_group(self, gid):
        """Delete a port group from the Packetmaster.
        
           :param gid: A string, ID of group e.g. 1-4294967040
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make DELETE request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/groups?'
        else:
            uri = 'http://' + self._address + '/rest/groups?'
        if not input_validation.group_id(gid):
            return "That is not a valid group ID, canceling Delete Group."
        existing = []
        all_groups = self.get_groups()
        json_groups = json.loads(all_groups)
        count = 0
        for group in json_groups['groups']:
            existing.append(json_groups['groups'][count]['group_id'])
            count += 1
        if gid not in existing:
            return "A group with this group ID does not exist; canceling Delete Group"
        data = {'group_id': gid}
        try:
            response = requests.delete(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def delete_groups_all(self):
        """Delete all port groups from the Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make DELETE request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/groups/all?'
        else:
            uri = 'http://' + self._address + '/rest/groups/all?'
        try:
            response = requests.delete(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_apps(self):
        """Return all Apps on Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_appsrun(self):
        """Return any running Apps on Packetmaster.
           
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps/running?'
        else:
            uri = 'http://' + self._address + '/rest/apps/running?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_hash(self):
        """Return load balancing hash algorithm configuration.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/grouphash?'
        else:
            uri = 'http://' + self._address + '/rest/device/grouphash?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_perm(self):
        """Return state of Rule Permanance setting.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/permanentrulesmode?'
        else:
            uri = 'http://' + self._address + '/rest/device/permanentrulesmode?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_mode(self):
        """Return setting of Rule Storage Mode.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/rulestoragemode?'
        else:
            uri = 'http://' + self._address + '/rest/device/rulestoragemode?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_env(self):
        """Return environmental information of Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/environment?'
        else:
            uri = 'http://' + self._address + '/rest/device/environment?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_led(self):
        """Return status of ID LED setting.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/idled?'
        else:
            uri = 'http://' + self._address + '/rest/device/idled?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_load(self):
        """Return load information.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/loadaverage?'
        else:
            uri = 'http://' + self._address + '/rest/device/loadaverage?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_tcam(self):
        """Return the max and currently used TCAM flows.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/flownumbers?'
        else:
            uri = 'http://' + self._address + '/rest/flownumbers?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_mem(self):
        """Return memory usage.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/memoryusage?'
        else:
            uri = 'http://' + self._address + '/rest/device/memoryusage?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_servrev(self):
        """Return CCH machinery server revision.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/serverrevision?'
        else:
            uri = 'http://' + self._address + '/rest/device/serverrevision?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_savepoints(self):
        """Return all available save points.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_weblog(self):
        """Return web server log.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/weblog?'
        else:
            uri = 'http://' + self._address + '/rest/weblog?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_users(self):
        """Return all user accounts on Packetmaster.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/users?'
        else:
            uri = 'http://' + self._address + '/rest/users?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_uac(self):
        """Return status of User Authentication setting.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/users/uac?'
        else:
            uri = 'http://' + self._address + '/rest/users/uac?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_radius(self):
        """Return RADIUS settings.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/users/radius?'
        else:
            uri = 'http://' + self._address + '/rest/users/radius?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_dns(self):
        """Return DNS server settings.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/nameresolution?'
        else:
            uri = 'http://' + self._address + '/rest/device/nameresolution?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_telnet(self):
        """Return status of Telnet service setting.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/telnet?'
        else:
            uri = 'http://' + self._address + '/rest/device/telnet?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_controller(self):
        """Return Vitrum Controller configuration.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/controller?'
        else:
            uri = 'http://' + self._address + '/rest/device/controller?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_controller_guided(self):
        """Interactive menu for setting Vitrum Controller configuration."""
        conn = input("""What is the connection type of the controller?
                1 - TCP
                2 - SSL
                Enter the number of your selection: """)
        if int(conn) == 1 or conn.lower() == "tcp":
            conn = "tcp"
        elif int(conn) == 2 or conn.lower() == "ssl":
            conn = "ssl"
        else:
            return "That is not a valid selection; canceling Set Controller. \n"
        ipadd = input("What is the IP address of the controller: ")
        if input_validation.ipv4(ipadd) != 0:
            ipadd = input_validation.ipv4(ipadd)
        else:
            return "That is not a valid IP address; canceling Set Controller. \n"
        port = input("What is the TCP Port of the controller: ")
        if not input_validation.port(port):
            return "That is not a valid TCP port number; canceling Set Controller. \n"
        confirm = input("""Configuration change summary:
                        Controller connection type: %s
                        Controller IP Address: %s
                        Controller port: %s
                        Confirm changes [y/n]: """ % (conn, ipadd, port))
        if confirm.lower() in ('y', 'yes'):
            run = self.set_controller(conn, ipadd, port)
            return run
        return "Canceling; no changes made.\n"

    def set_controller(self, conn, ipadd, port):
        """Set Vitrum Controller configuration.

           :param conn: A string, connection type; either 'tcp' or 'ssl'.
           :param ipadd: A string, controller IP address.
           :param port: A string, TCP port number for controller.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/controller?'
        else:
            uri = 'http://' + self._address + '/rest/device/controller?'
        if conn.lower() not in ('tcp', 'ssl'):
            return "That is not a valid connection type; canceling Set Controller. \n"
        if input_validation.ipv4(ipadd) != 0:
            ipadd = input_validation.ipv4(ipadd)
        else:
            return "That is not a valid IP address; canceling Set Controller. \n"
        if not input_validation.port(port):
            return "That is not a valid TCP port number; canceling Set Controller. \n"
        data = {'connection': conn, 'ip': ipadd, 'port': port}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def del_controller_guided(self):
        """Interactive menu for removing a Vitrum Controller."""
        conn = input("""What is the connection type of the controller?
                1 - TCP
                2 - SSL
                Enter the number of your selection: """)
        if int(conn) == 1 or conn.lower() == "tcp":
            conn = "tcp"
        elif int(conn) == 2 or conn.lower() == "ssl":
            conn = "ssl"
        else:
            return "That is not a valid selection; canceling Delete Controller. \n"
        ipadd = input("What is the IP address of the controller: ")
        if input_validation.ipv4(ipadd) != 0:
            ipadd = input_validation.ipv4(ipadd)
        else:
            return "That is not a valid IP address; canceling Delete Controller. \n"
        port = input("What is the TCP Port of the controller: ")
        if not input_validation.port(port):
            return "That is not a valid TCP port number; canceling Delete Controller. \n"
        confirm = input("""Configuration change summary:
                        Controller connection type: %s
                        Controller IP Address: %s
                        Controller port: %s
                        Confirm changes [y/n]: """ % (conn, ipadd, port))
        if confirm.lower() in ('y', 'yes'):
            run = self.del_controller(conn, ipadd, port)
            return run
        return "Canceling; no changes made.\n"

    def del_controller(self, conn, ipadd, port):
        """Remove a Vitrum Controller.
        
           :param conn: A string, connection type; either 'tcp' or 'ssl'.
           :param ipadd: A string, controller IP address.
           :param port: A string, TCP port number for controller.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make DELETE request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/controller?'
        else:
            uri = 'http://' + self._address + '/rest/device/controller?'
        if conn.lower() not in ('tcp', 'ssl'):
            return "That is not a valid connection type; canceling Delete Controller. \n"
        if input_validation.ipv4(ipadd) != 0:
            ipadd = input_validation.ipv4(ipadd)
        else:
            return "That is not a valid IP address; canceling Delete Controller. \n"
        if not input_validation.port(port):
            return "That is not a valid TCP port number; canceling Delete Controller. \n"
        data = {'connection': conn, 'ip': ipadd, 'port': port}
        try:
            response = requests.delete(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_dpid(self):
        """Return Device OpenFlow Datapath ID.
        
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/dpid?'
        else:
            uri = 'http://' + self._address + '/rest/device/dpid?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    # def get_license(self):
    #     """Return Device Vitrum license.
        
    #        :returns: A string, JSON-formatted.
    #        :raises: ConnectionError: if unable to successfully make GET request to device. """
        

    def set_license_guided(self):
        """Interactive menu for setting a Vitrum License."""
        pass

    def set_license(self, controller_id, valid_until, serial_no, sig):
        """Set Vitrum License information.
        
           :param controller_id: A string, 
           :param valid_until: A string, 
           :param serial_no: A string,
           :param sig: A string, 
           :returns: A string, JSON-formatted"""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/setlicense?'
        else:
            uri = 'http://' + self._address + '/rest/device/setlicense?'
        pass