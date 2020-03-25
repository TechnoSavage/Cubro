""" Packetmaster EX device class for REST API interaction,
    Use with firmware version 2.2.5 or newer and up to G4 NPB."""

from __future__ import print_function #Requires Python 2.6 or later
from getpass import getpass
import json
import re
import requests
from requests.exceptions import ConnectionError
from six import moves
import pm_input_check


#TO-DO Add code to handle case and verify input in all areas where needed
#add_rule_guided requires many input checks
#Add code to validate input for IPv6 as well as IPv4
#Integrate new REST rules for 2.2.5 device/setlicense
#restrict all bool input to only bool


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
            port_test = self.get_port_count()
            if not isinstance(port_test, (int, long)):
                print(port_test['error'])
                return "Connection test failed"
            self.hardware_generation()
            self.device_model()
            return "Connection established"
        except ConnectionError as fail:
            print(fail)
            try:
                self.__https = True
                port_test = self.get_port_count()
                if not isinstance(port_test, (int, long)):
                    print(port_test['error'])
                    return "Connection test failed"
                self.hardware_generation()
                self.device_model()
                return "Connection established"
            except ConnectionError as fail:
                print("Unable to establish connection; check if IP address is correct.", fail)

    #This will currently return both Physical and Logical ports.
    #Find way to list Physical ports only.
    def get_port_count(self):
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

    def firmware_version(self):
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

    def api_level(self):
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

    def ip_config(self):
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

    def device_model(self):
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

    def device_name(self):
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

    def device_label(self):
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

    def hardware_generation(self):
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
            self.hardware = info['generation']
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def serial_number(self):
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

    def port_config(self):
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

    def port_info(self):
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

    def port_statistics(self):
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

    def sfp_info(self):
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

    def rules_active(self):
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

    def groups_active(self):
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

    def device_apps(self):
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

    def apps_active(self):
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

    def hash_algorithms(self):
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

    def rule_permanence(self):
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

    def storage_mode(self):
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

    def env_info(self):
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

    def id_led(self):
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

    def load_info(self):
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

    def tcam(self):
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

    def mem_free(self):
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

    def server_revision(self):
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

    def save_points(self):
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

    def web_log(self):
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

    def user_uac(self):
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
        conn = moves.input("""What is the connection type of the controller?
                1 - TCP
                2 - SSL
                Enter the number of your selection: """)
        if int(conn) == 1 or conn.lower() == "tcp":
            conn = "tcp"
        elif int(conn) == 2 or conn.lower() == "ssl":
            conn = "ssl"
        else:
            return "That is not a valid selection; canceling Set Controller. \n"
        ipadd = moves.input("What is the IP address of the controller: ")
        if pm_input_check.ipv4(ipadd) != 0:
            ipadd = pm_input_check.ipv4(ipadd)
        else:
            return "That is not a valid IP address; canceling Set Controller. \n"
        port = moves.input("What is the TCP Port of the controller: ")
        if not pm_input_check.port(port):
            return "That is not a valid TCP port number; canceling Set Controller. \n"
        confirm = moves.input("""Configuration change summary:
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
        if pm_input_check.ipv4(ipadd) != 0:
            ipadd = pm_input_check.ipv4(ipadd)
        else:
            return "That is not a valid IP address; canceling Set Controller. \n"
        if not pm_input_check.port(port):
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
        conn = moves.input("""What is the connection type of the controller?
                1 - TCP
                2 - SSL
                Enter the number of your selection: """)
        if int(conn) == 1 or conn.lower() == "tcp":
            conn = "tcp"
        elif int(conn) == 2 or conn.lower() == "ssl":
            conn = "ssl"
        else:
            return "That is not a valid selection; canceling Delete Controller. \n"
        ipadd = moves.input("What is the IP address of the controller: ")
        if pm_input_check.ipv4(ipadd) != 0:
            ipadd = pm_input_check.ipv4(ipadd)
        else:
            return "That is not a valid IP address; canceling Delete Controller. \n"
        port = moves.input("What is the TCP Port of the controller: ")
        if not pm_input_check.port(port):
            return "That is not a valid TCP port number; canceling Delete Controller. \n"
        confirm = moves.input("""Configuration change summary:
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
        if pm_input_check.ipv4(ipadd) != 0:
            ipadd = pm_input_check.ipv4(ipadd)
        else:
            return "That is not a valid IP address; canceling Delete Controller. \n"
        if not pm_input_check.port(port):
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
        pass

    def set_ip_config_guided(self):
        """Interactive menu for configuring management IP settings."""
        address = moves.input('Enter IP Address (e.g. 192.168.0.200): ')
        if pm_input_check.ipv4(address) != 0:
            address = pm_input_check.ipv4(address)
        #elif pm_input_check.ipv6(address) != 0:
        #   address = pm_input_check.ipv6(address)
        else:
            return "That is not a valid IP address; canceling Set IP Configuration. \n"
        netmask = moves.input('Enter Subnet Mask (e.g. 255.255.255.0): ')
        if pm_input_check.ipv4(netmask) != 0:
            netmask = pm_input_check.ipv4(netmask)
        else:
            return "That is not a valid Subnet Mask; canceling Set IP Configuration. \n"
        gateway = moves.input('Enter gateway (e.g. 192.168.0.1): ')
        if pm_input_check.ipv4(gateway) != 0:
            gateway = pm_input_check.ipv4(gateway)
        else:
            return "That is not a valid Gateway Address; canceling Set IP Configuration. \n"
        confirm = moves.input("""Configuration change summary:
                            New management IP: %s
                            New Subnet Mask: %s
                            New Gateway: %s
                            Confirm changes [y/n]: """ % (address, netmask, gateway))
        if confirm.lower() in ('y', 'yes'):
            run = self.set_ip_config(address, netmask, gateway)
            return run
        return "Canceling; no changes made.\n"

    def set_ip_config(self, address, netmask, gateway):
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
        if pm_input_check.ipv4(address) != 0:
            address = pm_input_check.ipv4(address)
        #elif pm_input_check.ipv6(address) != 0:
        #   address = pm_input_check.ipv6(address)
        else:
            return "That is not a valid IP address; canceling Set IP Configuration. \n"
        if pm_input_check.ipv4(netmask) != 0:
            netmask = pm_input_check.ipv4(netmask)
        else:
            return "That is not a valid Subnet Mask; canceling Set IP Configuration. \n"
        if pm_input_check.ipv4(gateway) != 0:
            gateway = pm_input_check.ipv4(gateway)
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

    def set_name_guided(self):
        """Interactive menu for setting Packetmaster name."""
        newname = moves.input('Enter device name: ')
        confirm = moves.input("""Configuration change summary:
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
        data = {'name': name}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_label_guided(self):
        """Interactive menu for setting Packetmaster name and notes."""
        newname = moves.input('Enter device name: ')
        newnotes = moves.input('Enter device notes: ')
        confirm = moves.input("""Configuration change summary:
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

    def set_port_config_guided(self):
        """Interactive menu for setting port configuration on Packetmaster."""
        interface = moves.input('Enter the interface name of the port you want to change: ')
        if self.hardware == '4':
            speed = moves.input('Enter interface speed; e.g. "1000", "10G", "40G", "100G": ').strip()
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
            speed = moves.input(': ').strip()
            if speed.lower() == 'auto':
                speed = 'auto'
            elif speed in ('10', '100', '1000', 'XG', 'xg', 'Xg', 'xG', '1g', '1G'):
                speed = speed.upper()
            else:
                return "That is not a valid input for port speed; canceling Set Port Config."
        if speed in ('10', '100', '1000', 'auto'):
            duplex = moves.input('Enter the Duplex of the interface;'
                               'options are "full", "half, or "auto" [auto]: ')
            if duplex == '':
                duplex = 'auto'
        else:
            duplex = 'full'
        if speed in ('40G', '100G'):
            split = moves.input('Split to breakout cable?'
                              'Enter "yes" for yes and "no" for no [no]: ')
            if split == '':
                split = 'no'
        description = moves.input('Enter description for this port; leave blank for none: ')
        if self.hardware == '4' and speed in ('40G', '100G'):
            forcetx = moves.input('Force TX?  Enter "true" for yes and "false" for no [false]: ')
            if forcetx == '':
                forcetx = False
            check = moves.input('Perform CRC check?'
                              'Enter "true" for yes and "false" for no [false]: ')
            if check == '':
                check = False
            recalc = moves.input('Perform CRC recalculation?'
                               'Enter "true" for yes and "false" for no [false]: ')
            if recalc == '':
                recalc = False
            confirm = moves.input("""Configuration change summary:
                                Interface: %s
                                New Speed: %s
                                New Duplex: %s
                                New Description: %s
                                Force TX (unidirectional): %s
                                CRC Check: %s
                                CRC Recalculation: %s
                                Split Interface: %s
                                Confirm changes [y/n]: """ % (interface,
                                                              speed,
                                                              duplex,
                                                              description,
                                                              forcetx,
                                                              check,
                                                              recalc,
                                                              split))
            if confirm.lower() in ('y', 'yes'):
                run = self.set_port_config(interface, speed, duplex,
                                           description, forcetx, check,
                                           recalc, split)
            else:
                return "Canceling; no changes made.\n"
        elif self.hardware == '4':
            forcetx = moves.input('Force TX? Enter "true" for yes and "false" for no [false]: ')
            if forcetx == '':
                forcetx = False
            check = moves.input('Perform CRC check? '
                              'Enter "true" for yes and "false" for no [false]: ')
            if check == '':
                check = False
            recalc = moves.input('Perform CRC recalculation? '
                               'Enter "true" for yes and "false" for no [false]: ')
            if recalc == '':
                recalc = False
            confirm = moves.input("""Configuration change summary:
                                Interface: %s
                                New Speed: %s
                                New Duplex: %s
                                New Description: %s
                                Force TX (unidirectional): %s
                                CRC Check: %s
                                CRC Recalculation: %s
                                Confirm changes [y/n]: """ % (interface,
                                                              speed,
                                                              duplex,
                                                              description,
                                                              forcetx,
                                                              check,
                                                              recalc))
            if confirm.lower() in ('y', 'yes'):
                run = self.set_port_config(interface, speed, duplex,
                                           description, forcetx, check, recalc)
            else:
                return "Canceling; no changes made.\n"
        else:
            confirm = moves.input("""Configuration change summary:
                                Interface: %s
                                New Speed: %s
                                New Duplex: %s
                                New Description: %s
                                Confirm changes [y/n]: """ % (interface,
                                                              speed,
                                                              duplex,
                                                              description))
            if confirm.lower() in ('y', 'yes'):
                run = self.set_port_config(interface, speed, duplex, description)
            else:
                return "Canceling; no changes made.\n"
        print("""\nA device reboot is required for changes to take effect when changing
between 1G and 10G on pre-G4 devices and when changing to or from breakout cables
on QSFP ports of G4 devices. \n""")
        return run

    def set_port_config(self, interface, speed, duplex, description='',
                        forcetx=False, check=False, recalc=False, split=False):
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
        if self.hardware == '4':
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
        if forcetx in (True, 'True', 'true', 't', 'Yes', 'yes', 'y', 'T', 'Y'):
            forcetx = True
        else:
            forcetx = False
        if check in (True, 'True', 'true', 't', 'Yes', 'yes', 'y', 'T', 'Y'):
            check = True
        else:
            check = False
        if recalc in (True, 'True', 'true', 't', 'Yes', 'yes', 'y', 'T', 'Y'):
            recalc = True
        else:
            recalc = False
        if split in (True, 'True', 'true', 't', 'Yes', 'yes', 'y', 'T', 'Y'):
            split = 'break-out'
        else:
            split = 'no'
        if self.hardware == '4' and speed in ('40G', '100G'):
            data = {'if_name': interface,
                    'description': description,
                    'unidirectional': forcetx,
                    'crc_check': check,
                    'crc_recalculation': recalc,
                    'shutdown': 'false',
                    'split': split}
        elif self.hardware == '4':
            data = {'if_name': interface,
                    'description': description,
                    'speed': speed,
                    'duplex': duplex,
                    'unidirectional': forcetx,
                    'crc_check': check,
                    'crc_recalculation': recalc}
        elif self.hardware == '3.1' and speed in ('1G', 'XG'):
            data = {'if_name': interface,
                    'description': description,
                    'speed': 'auto',
                    'duplex': duplex,
                    'xg_speed': speed,
                    'shutdown': 'false'}
        else:
            data = {'if_name': interface,
                    'description': description,
                    'speed': speed,
                    'duplex': duplex,
                    'shutdown': 'false'}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def port_on_off_guided(self):
        """Interactive menu for enabling/disabling a port on the Packetmaster."""
        if_name = moves.input('Enter the interface name of the port you want to change: ')
        shutdown = moves.input('Enter "true" to shut port down; '
                             'Enter "false" to activate port [false]: ')
        confirm = moves.input("""Configuration change summary:
                            Interface: %s
                            Shutdown: %s
                            Confirm changes [y/n]: """ % (if_name, shutdown))
        if confirm.lower() in ('y', 'yes'):
            run = self.port_on_off(if_name, shutdown)
            return run
        return "Canceling; no changes made.\n"

    def port_on_off(self, if_name, shutdown):
        """Enable/disable a port on the Packetmaster.

           :param if_name: A string, interface name e.g. eth-0-1.
           :param shutdown: A bool, 'True' to disable, 'False' to enable.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/ports/config?'
        else:
            uri = 'http://' + self._address + '/rest/ports/config?'
        if_name = str(if_name).strip()
        port_no = re.findall('[1-9][0-9/]*', if_name)
        interface = 'eth-0-' + port_no[0]
        if shutdown.lower() in ('true', 't', 'yes', 'y'):
            updown = True
        else:
            updown = False
        data = {'if_name': interface, 'shutdown': updown}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def reset_port_counters(self):
        """Reser all port counters to zero.
        
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

    def reset_rule_counters(self):
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

    def add_rule_guided(self):
        """Interactive menu to add a rule/filter.
        
           :raises: ValueError: If proto variable not an int in the range of 2-9."""
        data = {}
        rulename = moves.input('Enter a name for the rule [none]: ')
        data['name'] = rulename
        ruledescrip = moves.input('Enter a description for the rule [none]: ')
        data['description'] = ruledescrip
        priority = moves.input('Enter the priority level of the rule; '
                             '0 - 65535 higher number = higher priority [32768]: ')
        if priority != '':
            if pm_input_check.pm_pri(priority):
                data['priority'] = int(priority)
            else:
                return "That is not a valid input for priority; canceling Add Rule."
        else:
            data['priority'] = 32768
        portin = moves.input('Enter the port number or numbers for incoming traffic; '
                           'multiple ports separated by a comma: ')
        #Implement valid port number check against device
        data['match[in_port]'] = portin
        print('''\nMatch VLAN tag?
                1 - No, match all tagged and untagged traffic
                2 - No, match only untagged traffic
                3 - Yes, match a VLAN tag \n''')
        trafmatch = moves.input('Enter the number of your selection [1]: ')
        if trafmatch == '' or int(trafmatch) == 1:
            pass
        elif int(trafmatch) == 2:
            data['match[vlan]'] = 'neg_match'
        elif int(trafmatch) == 3:
            data['match[vlan]'] = 'match'
            matchid = moves.input('Enter the VLAN ID to filter on: ')
            if pm_input_check.vlan(matchid):
                data['match[vlan_id]'] = matchid
            else:
                return "That is not a valid VLAN ID; canceling Add Rule."
            vpri = moves.input('Enter a VLAN priority? Enter 0-7 orleave blank for none: ')
            if vpri != '' and pm_input_check.vlan_pri(vpri):
                data['match[vlan_priority]'] = vpri
            elif vpri == '':
                data['match[vlan_priority]'] = '0'
            else:
                return "That is not a valid VLAN Priority; canceling Add Rule."
        else:
            return "That is not a valid selection; canceling Add Rule \n"
        macsrc = moves.input('Filter by source MAC address? '
                           'Leave blank for no or enter MAC address: ')
        if macsrc != '':
            if pm_input_check.mac(macsrc) != 0:
                data['match[dl_src]'] = pm_input_check.mac(macsrc)
            else:
                return "That is not a valid MAC address; canceling Add Rule."
        macdst = moves.input('Filter by destination MAC address? '
                           'Leave blank for no or enter MAC address: ')
        if macdst != '':
            if pm_input_check.mac(macdst) != 0:
                data['match[dl_dst]'] = pm_input_check.mac(macdst)
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
        proto = moves.input('Enter the number of your selection [1]: ')
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
                nwsrc = moves.input('Filter on source IP address? '
                                  'Leave blank for no or enter IP address + optional mask'
                                  '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                                  'or "192.168.1.5/24"): ')
                if nwsrc != '':
                    if pm_input_check.ipv4_mask(nwsrc) != 0:
                        data['match[nw_src]'] = pm_input_check.ipv4_mask(nwsrc)
                    else:
                        return "That is not a valid IP address; canceling Add Rule."
                nwdst = moves.input('Filter on destination IP address? '
                                  'Leave blank for no or enter IP address + optional mask'
                                  '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                                  'or "192.168.1.5/24"): ')
                if nwdst != '':
                    if pm_input_check.ipv4_mask(nwdst) != 0:
                        data['match[nw_dst]'] = pm_input_check.ipv4_mask(nwdst)
                    else:
                        return "That is not a valid IP address; canceling Add Rule."
            if data['match[protocol]'] == 'ip':
                nwproto = moves.input('Enter protocol number '
                                    '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                    'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
            if data['match[protocol]'] in ('tcp', 'udp', 'sctp'):
                tp_src = moves.input('Filter on source port? '
                                   'Leave blank for no or enter port number: ')
                if tp_src != '':
                    if pm_input_check.port(tp_src):
                        data['match[' + data['match[protocol]'] + '_src]'] = tp_src
                    else:
                        return "That is not a valid port number; canceling Add Rule."
                tp_dst = moves.input('Filter on destination port? '
                                   'Leave blank for no or enter port number: ')
                if tp_dst != '':
                    if pm_input_check.port(tp_dst):
                        data['match[' + data['match[protocol]'] + '_dst]'] = tp_dst
                    else:
                        return "That is not a valid port number; canceling Add Rule."
            if data['match[protocol]'] == 'icmp':
                icmpt = moves.input('Filter on ICMP type? '
                                  'Leave blank for no or enter ICMP type number: ')
                if icmpt != '':
                    if pm_input_check.icmp_type(icmpt):
                        data['match[icmp_type]'] = icmpt
                    else:
                        return "That is not a valid ICMP Type; canceling Add Rule."
                icmpc = moves.input('Filter on ICMP code? '
                                  'Leave blank for no or enter ICMP code number: ')
                if icmpc != '':
                    if pm_input_check.icmp_code(icmpc):
                        data['match[icmp_code]'] = icmpc
                    else:
                        return "That is not a valid ICMP Code; canceling Add Rule."
            if data['match[protocol]'] == 'custom':
                ether = moves.input('Enter Ethertype e.g. 0x0800: ')
                if ether != '':
                    data['match[dl_type]'] = ether
                nwproto = moves.input('Enter protocol number '
                                    '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                    'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
        print('''\nAdd Custom Extra Match?
        e.g. hard_timeout, idle_timeout, tcp_flags, Q in Q
        Leave blank for none
        Improper syntax will cause Add Rule to fail \n''')
        extra = moves.input('Enter Extra Custom Match String: ')
        if extra != '':
            data['match[extra]'] = extra
        ruleaction = moves.input('\nEnter the desired output actions separated by commas; '
                               'order matters - improper syntax will cause Add Rule to fail: ')
        data['actions'] = ruleaction
        check_data = json.dumps(data, indent=4)
        confirm = moves.input("""Configuration change summary:
                            Rule Parameters: %s
                            Confirm changes [y/n]: """ % check_data)
        if confirm.lower() in ('y', 'yes'):
            run = self.add_rule(data)
            return run
        return "Canceling; no changes made.\n"

    def add_rule(self, data):
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
        
           :raises: ValueError: If proto variable not an int in the range of 2-9."""
        data = {}
        name = moves.input('Enter a new name for the rule: ')
        data['name'] = name
        cookie = moves.input('Enter the cookie of the rule to modify: ')
        data['cookie'] = cookie
        description = moves.input('Enter a new description for the rule: ')
        data['description'] = description
        priority = moves.input('Enter the priority of the rule (priority cannot be changed; '
                             'must match rule to be modified)[32768]: ')
        if priority != '':
            if pm_input_check.pm_pri(priority):
                data['priority'] = int(priority)
            else:
                return "That is not a valid input for priority; canceling Modify Rule."
        else:
            priority = 32768
        in_port = moves.input("What is (are) the input port(s)for the rule separated by commas: ")
        data['match[in_port]'] = in_port
        print("For the following input filters the selected option must match "
              "the rule being modified; these fields cannot be changed.")
        print('''\nIs the rule matching a VLAN tag?
                1 - No, matching all tagged and untagged traffic
                2 - No, matching only untagged traffic
                3 - Yes, matching a VLAN tag \n''')
        trafmatch = moves.input('Enter the number of your selection [1]: ')
        if trafmatch == '' or int(trafmatch) == 1:
            pass
        elif int(trafmatch) == 2:
            data['match[vlan]'] = 'neg_match'
        elif int(trafmatch) == 3:
            data['match[vlan]'] = 'match'
            matchid = moves.input('Enter the VLAN ID the rule is filtering: ')
            if pm_input_check.vlan(matchid):
                data['match[vlan_id]'] = matchid
            else:
                return "That is not a valid VLAN ID; canceling Modify Rule."
            vpri = moves.input('Enter the VLAN priority? Enter 0-7 or leave blank for none: ')
            if vpri != '' and pm_input_check.vlan_pri(vpri):
                data['match[vlan_priority]'] = vpri
            elif vpri == '':
                data['match[vlan_priority]'] = '0'
            else:
                return "That is not a valid VLAN Priority; canceling Modify Rule."
        else:
            return "That is not a valid selection; canceling Modify Rule \n"
        macsrc = moves.input('Filtering by source MAC address? '
                           'Leave blank for no or enter MAC address: ')
        if macsrc != '':
            if pm_input_check.mac(macsrc) != 0:
                data['match[dl_src]'] = pm_input_check.mac(macsrc)
            else:
                return "That is not a valid MAC address; canceling Modify Rule."
        macdst = moves.input('Filtering by destination MAC address? '
                           'Leave blank for no or enter MAC address: ')
        if macdst != '':
            if pm_input_check.mac(macdst) != 0:
                data['match[dl_dst]'] = pm_input_check.mac(macdst)
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
        proto = moves.input('Enter the number of your selection [1]: ')
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
                nwsrc = moves.input('Filtering on a source IP address? '
                                  'Leave blank for no or enter IP address + optional mask'
                                  '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                                  'or "192.168.1.5/24"): ')
                if nwsrc != '':
                    if pm_input_check.ipv4_mask(nwsrc) != 0:
                        data['match[nw_src]'] = pm_input_check.ipv4_mask(nwsrc)
                    else:
                        return "That is not a valid IP address; canceling Modify Rule."
                nwdst = moves.input('Filtering on a destination IP address? '
                                  'Leave blank for no or enter IP address + optional mask'
                                  '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                                  'or "192.168.1.5/24"): ')
                if nwdst != '':
                    if pm_input_check.ipv4_mask(nwdst) != 0:
                        data['match[nw_dst]'] = pm_input_check.ipv4_mask(nwdst)
                    else:
                        return "That is not a valid IP address; canceling Modify Rule."
            if data['match[protocol]'] == 'ip':
                nwproto = moves.input('Filtering on a protocol number? '
                                    '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                    'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
            if data['match[protocol]'] in ('tcp', 'udp', 'sctp'):
                tp_src = moves.input('Filtering on a source port? '
                                   'Leave blank for no or enter port number: ')
                if tp_src != '':
                    if pm_input_check.port(tp_src):
                        data['match[' + data['match[protocol]'] + '_src]'] = tp_src
                    else:
                        return "That is not a valid port number; canceling Modify Rule."
                tp_dst = moves.input('Filtering on a destination port? '
                                   'Leave blank for no or enter port number: ')
                if tp_dst != '':
                    if pm_input_check.port(tp_dst):
                        data['match[' + data['match[protocol]'] + '_dst]'] = tp_dst
                    else:
                        return "That is not a valid port number; canceling Modify Rule."
            if data['match[protocol]'] == 'icmp':
                icmpt = moves.input('Filtering on ICMP type? '
                                  'Leave blank for no or enter ICMP type number: ')
                if icmpt != '':
                    if pm_input_check.icmp_type(icmpt):
                        data['match[icmp_type]'] = icmpt
                    else:
                        return "That is not a valid ICMP Type; canceling Modify Rule."
                icmpc = moves.input('Filtering on ICMP code? '
                                  'Leave blank for no or enter ICMP code number: ')
                if icmpc != '':
                    if pm_input_check.icmp_code(icmpc):
                        data['match[icmp_code]'] = icmpc
                    else:
                        return "That is not a valid ICMP Code; canceling Modify Rule."
            if data['match[protocol]'] == 'custom':
                ether = moves.input('Enter Ethertype e.g. 0x0800: ')
                if ether != '':
                    data['match[dl_type]'] = ether
                nwproto = moves.input('Enter protocol number '
                                    '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                    'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
        print('''\nUsing Custom Extra Match?
        e.g. hard_timeout, idle_timeout, tcp_flags, Q in Q
        Leave blank for none
        Improper syntax will cause Delete Rule to fail \n''')
        extra = moves.input('Enter Extra Custom Match String: ')
        if extra != '':
            data['match[extra]'] = extra
        ruleaction = moves.input('Enter the new output actions separated by commas; '
                               'order matters - improper syntax will cause Modify Rule to fail: ')
        data['actions'] = ruleaction
        check_data = json.dumps(data, indent=4)
        confirm = moves.input("""Configuration change summary:
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
        priority = moves.input("What is the priority of the rule to delete: ")
        try:
            priority = int(priority)
        except ValueError as reason:
            return ("That is not a valid input for rule priority; canceling Delete Rule.", reason)
        if priority < 0 or priority > 65535:
            print("That is not a valid input for rule priority; canceling Delete Rule.")
        in_port = moves.input("What is (are) the input port(s)for the rule separated by commas: ")
        data = {'priority': priority,
                  'match[in_port]': in_port}
        print('''\nIs the rule matching a VLAN tag?
                1 - No, matching all tagged and untagged traffic
                2 - No, matching only untagged traffic
                3 - Yes, matching a VLAN tag \n''')
        trafmatch = moves.input('Enter the number of your selection [1]: ')
        if trafmatch == '' or int(trafmatch) == 1:
            pass
        elif int(trafmatch) == 2:
            data['match[vlan]'] = 'neg_match'
        elif int(trafmatch) == 3:
            data['match[vlan]'] = 'match'
            matchid = moves.input('Enter the VLAN ID the rule is filtering: ')
            if pm_input_check.vlan(matchid):
                data['match[vlan_id]'] = matchid
            else:
                return "That is not a valid VLAN ID; canceling Delete Rule."
            vpri = moves.input('Enter the VLAN priority? Enter 0-7 or leave blank for none: ')
            if vpri != '' and pm_input_check.vlan_pri(vpri):
                data['match[vlan_priority]'] = vpri
            elif vpri == '':
                data['match[vlan_priority]'] = '0'
            else:
                return "That is not a valid VLAN Priority; canceling Delete Rule."
        else:
            return "That is not a valid selection; canceling Delete Rule \n"
        macsrc = moves.input('Filtering by source MAC address? '
                           'Leave blank for no or enter MAC address: ')
        if macsrc != '':
            data['match[dl_src]'] = macsrc
        macdst = moves.input('Filtering by destination MAC address? '
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
        proto = moves.input('Enter the number of your selection [1]: ')
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
                nwsrc = moves.input('Filtering on a source IP address? '
                                  'Leave blank for no or enter IP address + optional mask'
                                  '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                                  'or "192.168.1.5/24"): ')
                if nwsrc != '':
                    if pm_input_check.ipv4_mask(nwsrc) != 0:
                        data['match[nw_src]'] = pm_input_check.ipv4_mask(nwsrc)
                    else:
                        return "That is not a valid IP address; canceling Delete Rule."
                nwdst = moves.input('Filtering on a destination IP address? '
                                  'Leave blank for no or enter IP address + optional mask'
                                  '(e.g. "192.168.1.5" or "192.168.1.5/255.255.255.0"'
                                  'or "192.168.1.5/24"): ')
                if nwdst != '':
                    if pm_input_check.ipv4_mask(nwdst) != 0:
                        data['match[nw_dst]'] = pm_input_check.ipv4_mask(nwdst)
                    else:
                        return "That is not a valid IP address; canceling Delete Rule."
            if data['match[protocol]'] == 'ip':
                nwproto = moves.input('Filtering on a protocol number? '
                                    '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                    'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
            if data['match[protocol]'] in ('tcp', 'udp', 'sctp'):
                tp_src = moves.input('Filtering on a source port? '
                                   'Leave blank for no or enter port number: ')
                if tp_src != '':
                    if pm_input_check.port(tp_src):
                        data['match[' + data['match[protocol]'] + '_src]'] = tp_src
                    else:
                        return "That is not a valid port number; canceling Delete Rule."
                tp_dst = moves.input('Filtering on a destination port? '
                                   'Leave blank for no or enter port number: ')
                if tp_dst != '':
                    if pm_input_check.port(tp_dst):
                        data['match[' + data['match[protocol]'] + '_dst]'] = tp_dst
                    else:
                        return "That is not a valid port number; canceling Delete Rule."
            if data['match[protocol]'] == 'icmp':
                icmpt = moves.input('Filtering on ICMP type? '
                                  'Leave blank for no or enter ICMP type number: ')
                if icmpt != '':
                    if pm_input_check.icmp_type(icmpt):
                        data['match[icmp_type]'] = icmpt
                    else:
                        return "That is not a valid ICMP Type; canceling Delete Rule."
                icmpc = moves.input('Filtering on ICMP code? '
                                  'Leave blank for no or enter ICMP code number: ')
                if icmpc != '':
                    if pm_input_check.icmp_code(icmpc):
                        data['match[icmp_code]'] = icmpc
                    else:
                        return "That is not a valid ICMP Code; canceling Delete Rule."
            if data['match[protocol]'] == 'custom':
                ether = moves.input('Enter Ethertype e.g. 0x0800: ')
                if ether != '':
                    data['match[dl_type]'] = ether
                nwproto = moves.input('Enter protocol number '
                                    '(protocol number in IPv4, header type in IPv6, opcode in ARP) '
                                    'or leave blank for none: ')
                if nwproto != '':
                    data['match[nw_proto]'] = nwproto
        print('''\nUsing Custom Extra Match?
        e.g. hard_timeout, idle_timeout, tcp_flags, Q in Q
        Leave blank for none
        Improper syntax will cause Delete Rule to fail \n''')
        extra = moves.input('Enter Extra Custom Match String: ')
        if extra != '':
            data['match[extra]'] = extra
        check_data = json.dumps(data, indent=4)
        confirm = moves.input("""Configuration change summary:
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

    def add_group_guided(self):
        """Interactive menu for adding a port group.
        
           :raises: ValueError: If group_type variable cannot be converted to int.
           :raises: ValueError: If buckets variable cannot be converted to int.
           :raises: ValueError: If output variable cannot be converted to int.
           :raises: ValueError: If watch variable cannot be converted to int."""
        gid = moves.input("Enter the group ID: ")
        if not pm_input_check.group_id(gid):
            return "That is not a valid group ID, canceling Add Group."
        existing = []
        all_groups = self.groups_active()
        json_groups = json.loads(all_groups)
        count = 0
        for group in json_groups['groups']:
            existing.append(json_groups['groups'][count]['group_id'])
            count += 1
        if gid in existing:
            return ("A group with this group ID already exists; "
                    "use Modify Group or select a different group ID. Canceling Add Group")
        description = moves.input("Enter the group description: ")
        group_type = moves.input(""" Select the group type:
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
        buckets = moves.input("How many buckets in this port group? "
                            "Must be at least 2 and no more than 16: ")
        try:
            buckets = int(buckets)
        except ValueError as reason:
            return ("That is not a valid bucket number; canceling Add Group.", reason)
        if buckets >= 2 and buckets <= 16:
            for bucket in xrange(buckets):
                print("\nConfigure settings for bucket %s" % bucket)
                #Add check against number of ports on device
                output = moves.input("Output on which port: ")
                #Validate if port exists on device
                try:
                    int(output)
                    output = 'output:' + output
                except ValueError as reason:
                    return ("That is not a valid port number; canceling Add Group", reason)
                actions = output
                if self.hardware != '4' or group_type == 3:
                    watch = moves.input("Set watch port to: ")
                    try:
                        int(watch)
                    except ValueError as reason:
                        return ("That is not a valid port number; canceling Add Group", reason)
                push_vlan = moves.input('Push VLAN ID to outout traffic? '
                                      'Enter VLAN ID or leave blank for no: ').strip()
                if push_vlan != '':
                    if pm_input_check.vlan(push_vlan):
                        vlan = str(int(push_vlan) + 4096)
                        vlan = 'push_vlan:0x8100,set_field:' + vlan + '->vlan_vid,'
                        actions = vlan + actions
                    else:
                        return "That is not a valid VLAN ID, canceling Add Group."
                else:
                    mod_vlan = moves.input('Modify VLAN ID of output traffic? '
                                         'Enter VLAN ID or leave blank for no: ').strip()
                    if mod_vlan != '':
                        if pm_input_check.vlan(mod_vlan):
                            vlan = str(int(mod_vlan) + 4096)
                            vlan = 'set_field:' + vlan + '->vlan_vid,'
                            actions = vlan + actions
                        else:
                            return ("That is not a valid input for VLAN ID, "
                                    "canceling Add Group.")
                    else:
                        strip_vlan = moves.input('Strip VLAN ID from output traffic? '
                                               'Y or N [N]: ').lower()
                        if strip_vlan in ('y', 'yes'):
                            actions = 'strip_vlan,' + actions
                if self.hardware == '4':
                    pop_l2 = moves.input('Pop all L2 information from packet?  Y or N [N]: ').lower()
                    if pop_l2 in ('y', 'yes'):
                        actions = 'pop_l2,' + actions
                if self.hardware == '4':
                    pop_mpls = moves.input('Pop MPLS tags? In most cases you should also push L2. '
                                         'Y or N [N]: ').lower()
                    if pop_mpls in ('y', 'yes'):
                        actions = 'pop_all_mpls,' + actions
                if self.hardware == '4':
                    push_l2 = moves.input('Push L2 information to output packets? '
                                        'Y or N [N]: ').lower()
                    if push_l2 in ('y', 'yes'):
                        print ("Be sure to modify destination MAC when prompted, "
                               "else an error will occur.")
                        actions = 'push_l2,' + actions
                src_mac = moves.input('Modify source MAC address? '
                                    'Enter new MAC address or leave blank for no: ').strip()
                if src_mac != '':
                    if pm_input_check.mac(src_mac) != 0:
                        src_mac = pm_input_check.mac(src_mac)
                        actions = 'set_field:' + src_mac + '->eth_src,' + actions
                    else:
                        return "That is not a valid MAC address, canceling Add Group."
                dst_mac = moves.input('Modify destination MAC address? '
                                    'Enter new MAC address or leave blank for no: ').strip()
                if dst_mac != '':
                    if pm_input_check.mac(dst_mac) != 0:
                        src_mac = pm_input_check.mac(dst_mac)
                        actions = 'set_field:' + dst_mac + '->eth_dst,' + actions
                    else:
                        return "That is not a valid MAC address, canceling Add Group."
                dst_ip = moves.input('Modify destination IP address? '
                                   'Enter new IP address or leave blank for no: ').strip()
                if dst_ip != '':
                    if pm_input_check.ipv4_mask(dst_ip) != 0:
                        actions = 'set_field:' + pm_input_check.ipv4_mask(dst_ip) + \
                                  '->ip_dst,' + actions
                    else:
                        return ("That is not a valid input for IP address, "
                                "canceling Add Group.")
                if self.hardware == '4':
                    src_udp = moves.input('Modify source UDP port? '
                                        'Enter new port number or leave blank for no: ').strip()
                    if src_udp != '':
                        if pm_input_check.port(src_udp):
                            actions = 'set_field:' + src_udp + '->udp_src,' + actions
                        else:
                            return ("That is not a valid input for port number; "
                                    "canceling Add Group.")
                dst_udp = moves.input('Modify destination UDP port? '
                                    'Enter new port number or leave blank for no: ').strip()
                if dst_udp != '':
                    if pm_input_check.port(dst_udp):
                        actions = 'set_field:' + dst_udp + '->udp_dst,' + actions
                    else:
                        return ("That is not a valid input for port number; "
                                "canceling Add Group.")
                if self.hardware == '4':
                    src_tcp = moves.input('Modify source TCP port? '
                                        'Enter new port number or leave blank for no: ').strip()
                    if src_tcp != '':
                        if pm_input_check.port(src_tcp):
                            actions = 'set_field:' + src_tcp + '->tcp_src,' + actions
                        else:
                            return ("That is not a valid input for port number; "
                                    "canceling Add Group.")
                dst_tcp = moves.input('Modify destination TCP port? '
                                    'Enter new port number or leave blank for no: ').strip()
                if dst_tcp != '':
                    if pm_input_check.port(dst_tcp):
                        actions = 'set_field:' + dst_tcp + '->tcp_dst,' + actions
                    else:
                        return ("That is not a valid input for port number; "
                                "canceling Add Group.")
                if self.hardware != '4' or group_type == 3:
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
        confirm = moves.input("""Configuration change summary:
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
        if not pm_input_check.group_id(gid):
            return "That is not a valid group ID, canceling Add Group."
        existing = []
        all_groups = self.groups_active()
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
        gid = moves.input("Enter the group ID of the group you would like to modify: ")
        if not pm_input_check.group_id(gid):
            return "That is not a valid group ID, canceling Modify Group."
        existing = []
        all_groups = self.groups_active()
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
        description = moves.input("Enter the new group description or "
                                "leave blank to retain original: ")
        bucket_list = []
        buckets = moves.input("How many buckets in this port group? "
                            "Must be at least 2 and no more than 16: ")
        try:
            buckets = int(buckets)
        except ValueError as reason:
            return ("That is not a valid bucket number; canceling Modify Group.", reason)
        if buckets >= 2 and buckets <= 16:
            for bucket in xrange(buckets):
                print("\nConfigure settings for bucket %s" % bucket)
                #Add check against number of ports on device
                output = moves.input("Output on which port: ")
                try:
                    int(output)
                    output = 'output:' + output
                except ValueError as reason:
                    return ("That is not a valid port number; canceling Modify Group", reason)
                actions = output
                if self.hardware != '4' or group_type == 'ff':
                    watch = moves.input("Set watch port to: ")
                    try:
                        int(watch)
                    except ValueError as reason:
                        return ("That is not a valid port number; canceling Modify Group", reason)
                push_vlan = moves.input('Push VLAN ID to outout traffic? '
                                      'Enter VLAN ID or leave blank for no: ').strip()
                if push_vlan != '':
                    if pm_input_check.vlan(push_vlan):
                        vlan = str(int(push_vlan) + 4096)
                        vlan = 'push_vlan:0x8100,set_field:' + vlan + '->vlan_vid,'
                        actions = vlan + actions
                    else:
                        return "That is not a valid VLAN ID, canceling Modify Group."
                else:
                    mod_vlan = moves.input('Modify VLAN ID of output traffic? '
                                         'Enter VLAN ID or leave blank for no: ').strip()
                    if mod_vlan != '':
                        if pm_input_check.vlan(mod_vlan):
                            vlan = str(int(mod_vlan) + 4096)
                            vlan = 'set_field:' + vlan + '->vlan_vid,'
                            actions = vlan + actions
                        else:
                            return ("That is not a valid input for VLAN ID, "
                                    "canceling Modify Group.")
                    else:
                        strip_vlan = moves.input('Strip VLAN ID from output traffic? '
                                               'Y or N [N]: ').lower()
                        if strip_vlan == 'y' or strip_vlan == 'yes':
                            actions = 'strip_vlan,' + actions
                if self.hardware == '4':
                    pop_l2 = moves.input('Pop all L2 information from packet?  Y or N [N]: ').lower()
                    if pop_l2 == 'y' or pop_l2 == 'yes':
                        actions = 'pop_l2,' + actions
                if self.hardware == '4':
                    pop_mpls = moves.input('Pop MPLS tags? In most cases you should also push L2. '
                                         'Y or N [N]: ').lower()
                    if pop_mpls == 'y' or pop_mpls == 'yes':
                        actions = 'pop_all_mpls,' + actions
                if self.hardware == '4':
                    push_l2 = moves.input('Push L2 information to output packets? '
                                        'Y or N [N]: ').lower()
                    if push_l2 == 'y' or push_l2 == 'yes':
                        print ("Be sure to modify destination MAC when prompted, "
                               "else an error will occur.")
                        actions = 'push_l2,' + actions
                src_mac = moves.input('Modify source MAC address? '
                                    'Enter new MAC address or leave blank for no: ').strip()
                if src_mac != '':
                    if pm_input_check.mac(src_mac) != 0:
                        src_mac = pm_input_check.mac(src_mac)
                        actions = 'set_field:' + src_mac + '->eth_src,' + actions
                    else:
                        return "That is not a valid MAC address, canceling Modify Group."
                dst_mac = moves.input('Modify destination MAC address? '
                                    'Enter new MAC address or leave blank for no: ').strip()
                if dst_mac != '':
                    if pm_input_check.mac(dst_mac) != 0:
                        src_mac = pm_input_check.mac(dst_mac)
                        actions = 'set_field:' + dst_mac + '->eth_dst,' + actions
                    else:
                        return "That is not a valid MAC address, canceling Modify Group."
                dst_ip = moves.input('Modify destination IP address? '
                                   'Enter new IP address or leave blank for no: ').strip()
                if dst_ip != '':
                    if pm_input_check.ipv4_mask(dst_ip) != 0:
                        actions = 'set_field:' + pm_input_check.ipv4_mask(dst_ip) + \
                                  '->ip_dst,' + actions
                    else:
                        return ("That is not a valid input for IP address, "
                                "canceling Modify Group.")
                if self.hardware == '4':
                    src_udp = moves.input('Modify source UDP port? '
                                        'Enter new port number or leave blank for no: ').strip()
                    if src_udp != '':
                        if pm_input_check.port(src_udp):
                            actions = 'set_field:' + src_udp + '->udp_src,' + actions
                        else:
                            return ("That is not a valid input for port number; "
                                    "canceling Modify Group.")
                dst_udp = moves.input('Modify destination UDP port? '
                                    'Enter new port number or leave blank for no: ').strip()
                if dst_udp != '':
                    if pm_input_check.port(dst_udp):
                        actions = 'set_field:' + dst_udp + '->udp_dst,' + actions
                    else:
                        return ("That is not a valid input for port number; "
                                "canceling Modify Group.")
                if self.hardware == '4':
                    src_tcp = moves.input('Modify source TCP port? '
                                        'Enter new port number or leave blank for no: ').strip()
                    if src_tcp != '':
                        if pm_input_check.port(src_tcp):
                            actions = 'set_field:' + src_tcp + '->tcp_src,' + actions
                        else:
                            return ("That is not a valid input for port number; "
                                    "canceling Modify Group.")
                dst_tcp = moves.input('Modify destination TCP port? '
                                    'Enter new port number or leave blank for no: ').strip()
                if dst_tcp != '':
                    if pm_input_check.port(dst_tcp):
                        actions = 'set_field:' + dst_tcp + '->tcp_dst,' + actions
                    else:
                        return ("That is not a valid input for port number; "
                                "canceling Modify Group.")
                if self.hardware != '4' or group_type == 'ff':
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
        confirm = moves.input("""Configuration change summary:
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
        if not pm_input_check.group_id(gid):
            return "That is not a valid group ID, canceling Modify Group."
        existing = []
        all_groups = self.groups_active()
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
        gid = moves.input("Enter the group ID of the group to be deleted: ")
        try:
            int(gid)
        except ValueError as reason:
            return ("That is not a valid group ID, canceling Delete Group.", reason)
        confirm = moves.input("""Configuration Change Summary:
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
        if not pm_input_check.group_id(gid):
            return "That is not a valid group ID, canceling Delete Group."
        existing = []
        all_groups = self.groups_active()
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

    def set_port_savepoint_guided(self):
        """Interactive menu to activate a port save point.
        
           :returns: A string, JSON-formatted."""
        savename = moves.input('Name of port save point to make active: ')
        confirm = moves.input("""Configuration Change Summary:
                            You are about to make port save point %s active.
                            Confirm changes [y/n]: """ % savename)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_port_savepoint(savename)
            return run
        return "Canceling; no changes made.\n"

    def set_port_savepoint(self, savename):
        """Activate a port save point.
        
           :param savename: A string, name of port save point to make active.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make PUT request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/activeportsavepoint?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/activeportsavepoint?'
        #Add check against system savepoints
        data = {'name': savename}
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_rule_savepoint_guided(self):
        """Interactive menu to activate a rule save point.
        
           :returns: A string, JSON-formatted."""
        savename = moves.input('Name of rule save point to make active: ')
        confirm = moves.input("""Configuration Change Summary:
                            You are about to make rule save point "%s" active.
                            Confirm changes [y/n]: """ % savename)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_rule_savepoint(savename)
            return run
        return "Canceling; no changes made.\n"

    def set_rule_savepoint(self, savename):
        """Activate a rule save point.
        
           :param savename: A string, name of rule save point to make active.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make PUT request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/activerulesavepoint?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/activerulesavepoint?'
        #Add check against system savepoints
        data = {'name': savename}
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_boot_savepoint_guided(self):
        """Interactive menu to set a save point as default boot configuration.
        
           :returns: A string, JSON-formatted."""
        savename = moves.input('Save point to set to default boot configuration: ')
        confirm = moves.input("""Configuration Change Summary:
                            You are about to set save point "%s" the default boot configuration.
                            Confirm changes [y/n]: """ % savename)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_boot_savepoint(savename)
            return run
        return "Canceling; no changes made.\n"

    def set_boot_savepoint(self, savename):
        """Set a save point as default boot configuration.
        
           :param savename: A string, name of rule save point to load on boot.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make PUT request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/defaultrulesavepoint?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/defaultrulesavepoint?'
        #Add check against system savepoints
        data = {'name': savename}
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def export_savepoint_guided(self):
        """Interactive menu to download a save point from the Packetmaster.
        
           :returns: A string, JSON-formatted."""
        rspname = moves.input('Name of rule save point(s) to export (leave blank for none)'
                              'to enter multiple save points separate names by "," with no spaces: ')
        rspname = rspname.split(',')
        pspname = moves.input('Name of port save point(s) to export (leave blank for none): '
                              'to enter multiple save points separate names by "," with no spaces: ')
        pspname = pspname.split(',')
        filename = moves.input("File name for savepoint export: ")
        confirm = moves.input("""Savepoint Export Summary:
                            Rule Save Point: %s
                            Port Save Point: %s
                            Saved to file: %s
                            Confirm changes [y/n]: """ % (rspname, pspname, filename))
        if confirm.lower() in ('y', 'yes'):
            run = self.export_savepoint(rspname, pspname, filename)
            return run
        return "Canceling; save points not exported.\n"

    def export_savepoint(self, rspname, pspname, filename):
        """Download a save point from the Packetmaster.
        
           :param rspname: A string, rule save point name to export.
           :param pspname: A string, port save point name to export.
           :param filename: A string, name to give to exported save point.
           :returns: A string, JSON-formatted.
           :raises: NameError: if filename varaible is unrecognized.
           :raises: TypeError: if filename variable is not a string.
           :raises: IOError: if unable to write file due to permissions, path, or other reason.
           :raises: OSError: if unable to write file due to permissions, path, or other reason.
           :raises: ConnectionError: if unable to successfully make GET request to device."""
        if self.__https:
            base_uri = 'https://' + self._address + '/rest/savepoints/export?'
        else:
            base_uri = 'http://' + self._address + '/rest/savepoints/export?'
        #Add checks to see if names exist and if names are lists
        if not rspname == "" and pspname == "":
            uri = base_uri + 'rule_save_point_names=' + json.dumps(rspname)  
        elif rspname == "" and not pspname == "":
            uri = base_uri + 'port_save_point_names=' + json.dumps(pspname)
        else:
            uri = base_uri + 'rule_save_point_names=' + json.dumps(rspname) + '&port_save_point_names=' + json.dumps(pspname)
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            try:
                with open(filename, "w") as save:
                    save.write(content)
            except (NameError, TypeError, IOError, OSError) as reason:
                return ("Invalid filename.", reason)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_port_savepoint_guided(self):
        """Interactive menu to modify a port save point.
        
           :returns: A string, JSON-formatted."""
        oldname = moves.input("Name of port save point to modify: ")
        newname = moves.input("New name for port save point: ")
        desc = moves.input("Description of save point: ")
        override = moves.input('Hit enter to save the current active ports '
                             'to this save point; type "false" to not save '
                             'them (This overwrites port '
                             'configuration of the save point): ')
        if override.lower() in ('false', 'f', 'n', 'no'):
            override = False
        else:
            override = True
        confirm = moves.input("""Modify Port Save Point Summary:
                            Save Point to Modify: %s
                            New Save Point Name: %s
                            New Description: %s
                            Save Active Ports: %s
                            Confirm changes [y/n]: """ % (oldname, newname, desc, override))
        if confirm.lower() in ('y', 'yes'):
            run = self.mod_port_savepoint(oldname, newname, desc, override)
            return run
        return "Canceling; no changes made.\n"

    def mod_port_savepoint(self, oldname, newname, description, override=True):
        """Modify a port save point.
        
           :param oldname: A string, name of port save point to modify.
           :param newname: A string, new name for modified port save point.
           :param description: A string, description for port save point.
           :param override: A bool, 'True' saves current port config; 'False' does not overwrite prior port config. 
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/modportsavepoint?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/modportsavepoint?'
        if override is False:
            override = False
        elif override.lower() in ('false', 'f', 'n', 'no'):
            override = False
        else:
            override = True
        data = {'old_name': oldname,
                'new_name': newname,
                'description': description,
                'override': override}
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_rule_savepoint_guided(self):
        """Interactive menu to modify a rule save point.
        
           :returns: A string, JSON-formatted."""
        oldname = moves.input("Name of rule save point to modify: ")
        newname = moves.input("New name for rule save point: ")
        desc = moves.input("Description for save point: ")
        override = moves.input('Hit enter to save the current active rules to this save point; '
                             'type "false" to not save them '
                             '(This overwrites rule configuration of the save point): ')
        if override.lower() in ('false', 'f', 'n', 'no'):
            override = False
        else:
            override = True
        confirm = moves.input("""Modify Rule Save Point Summary:
                            Save Point to Modify: %s
                            New Save Point Name: %s
                            New Description: %s
                            Save Active Rules: %s
                            Confirm changes [y/n]: """ % (oldname, newname, desc, override))
        if confirm.lower() in ('y', 'yes'):
            run = self.mod_rule_savepoint(oldname, newname, desc, override)
            return run
        return "Canceling; no changes made.\n"

    def mod_rule_savepoint(self, oldname, newname, description, override=True):
        """Modify a rule save point on the Packetmaster.
        
           :param oldname: A string, name of rule save point to modify.
           :param newname: A string, new name for modified rule save point.
           :param description: A string, description for rule save point.
           :param override: A bool, 'True' saves current rule config; 'False' does not overwrite prior rule config. 
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/modrulesavepoint?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/modrulesavepoint?'
        if not override:
            override = False
        elif override.lower() in ('false', 'f', 'n', 'no'):
            override = False
        else:
            override = True
        data = {'old_name': oldname,
                'new_name': newname,
                'description': description,
                'override': override}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def create_port_savepoint_guided(self):
        """Interactive menu to create port save point from current config.
        
           :returns: A string, JSON-formatted."""
        name = moves.input("Name for  newly created port savepoint: ")
        desc = moves.input("Description for the port save point: ")
        confirm = moves.input("""Create Port Save Point:
                            Save Point Name: %s
                            Description: %s
                            Confirm changes [y/n]: """ % (name, desc))
        if confirm.lower() in ('y', 'yes'):
            run = self.create_port_savepoint(name, desc)
            return run
        return "Canceling; no changes made.\n"

    def create_port_savepoint(self, name, description):
        """Create port save point from current configuration.
        
           :param name: A string, new name for port save point.
           :param description: A string, description for port save point.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/portsavepoint?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/portsavepoint?'
        data = {'name': name, 'description': description}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def create_quick_savepoint(self):
        """Create a Quicksave save point from current configuration.
           
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make PUT request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/quicksaverules?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/quicksaverules?'
        try:
            response = requests.put(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def create_rule_savepoint_guided(self):
        """Interactive menu to create rule save point from current config.
        
           :returns: A string, JSON-formatted."""
        name = moves.input("Name for newly created rule save point: ")
        desc = moves.input("Description for the rule save point: ")
        confirm = moves.input("""Create Rule Save Point:
                            Save Point Name: %s
                            Description: %s
                            Confirm changes [y/n]: """ % (name, desc))
        if confirm.lower() in ('y', 'yes'):
            run = self.create_rule_savepoint(name, desc)
            return run
        return "Canceling; no changes made.\n"

    def create_rule_savepoint(self, name, description):
        """Create a rule save point from current configuration.
        
           :param name: A string, new name for rule save point.
           :param description: A string, description for rule save point.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/rulesavepoint?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/rulesavepoint?'
        data = {'name': name, 'description': description}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def delete_port_savepoint_guided(self):
        """Interactive menu to delete a port save point.
        
           :returns: A string, JSON-formatted."""
        name = moves.input("Port save point to delete: ")
        confirm = moves.input("""Delete Port Save Point Summary:
                            Save Point Name: %s
                            Confirm changes [y/n]: """ % name)
        if confirm.lower() in ('y', 'yes'):
            run = self.delete_port_savepoint(name)
            return run
        return "Canceling; no changes made.\n"

    def delete_port_savepoint(self, name):
        """Delete a port save point from the Packetmaster.
        
           :param name: A string, name of port save point to delete.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make DELETE request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/portsavepoint?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/portsavepoint?'
        #Add check to see if port savepoint exists
        data = {'name': name}
        try:
            response = requests.delete(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def delete_rule_savepoint_guided(self):
        """Interactive menu to delete a rule save point.
        
           returns: A string, JSON-formatted."""
        name = moves.input("Rule save point to delete:  ")
        confirm = moves.input("""Delete Rule Save Point Summary:
                            Save Point Name: %s
                            Confirm changes [y/n]: """ % name)
        if confirm.lower() in ('y', 'yes'):
            run = self.delete_rule_savepoint(name)
            return run
        return "Canceling; no changes made.\n"

    def delete_rule_savepoint(self, name):
        """Delete a rule save point from the Packetmaster.
        
           :param name: A string, name of rule save point to delete.
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make DELETE request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/savepoints/rulesavepoint?'
        else:
            uri = 'http://' + self._address + '/rest/savepoints/rulesavepoint?'
        #Add check to see if rule savepoint exists
        data = {'name': name}
        try:
            response = requests.delete(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def start_app_guided(self):
        """Interactive menu to start a new app instance.
        
           :returns: A string, JSON-formatted.
           :raises: ValueError: if app variable cannot be converted to int."""
           #add input validation here? Break selections out to individual methods?
        app = moves.input("""Select the App instance to start:
                            1 - NTP
                            2 - Arp Responder
                            3 - SNMP
                            4 - Heartbeat Bypass (control Bypass Switch)
                            5 - Syslog
                            6 - Bypass Keepalive (control Bypass Switch)
                            7 - Heartbeat
                           Enter the number of the App selection: """)
        try:
            app = int(app)
        except ValueError as reason:
            return ("That is not a valid input for App selection; canceling Start App.", reason)
        description = moves.input("Custom description for the new App instance: ")
        if app == 1:
            server1 = moves.input("Enter NTP target IP or Host Name: ")
            server2 = moves.input("Enter NTP backup IP or Host Name: ")
            confirm = moves.input("""Start NTP App Summary:
                                Server 1: %s
                                Server 2: %s
                                Description: %s
                                Confirm changes [y/n]: """ % (server1, server2, description))
            if confirm.lower() in ('y', 'yes'):
                run = self.start_app_ntp(server1, server2, description)
            else:
                return "Canceling; no changes made.\n"
        elif app == 2:
            interval = moves.input("Enter the check interval in milliseconds [5000]: ")
            if interval == '':
                interval = '5000'
            in_port = moves.input("Physical source port of incoming ARP request (optional): ")
            out_port = moves.input("Physical port for sending ARP response: ")
            match_mac = moves.input("Enter source MAC address of incoming ARP request (optional): ")
            src_mac = moves.input("Source MAC address of outgoing ARP response: ")
            dst_mac = moves.input("Destination MAC address of outgoing ARP response: ")
            src_ip = moves.input("Source IP address of outgoing ARP response: ")
            dst_ip = moves.input("Destination IP of outgoing ARP response: ")
            confirm = moves.input("""Start ARP Responder App Summary:
                                Check Interval: %s
                                Port of incoming ARP packets: %s
                                Port to send ARP packets: %s
                                Source MAC of incoming ARPs: %s
                                Source MAC of outgoing ARPs: %s
                                Destinaton MAC of outgoing ARPs: %s
                                Source IP of outgoing ARPs: %s
                                Destination IP of outgoing ARPs: %s
                                Description: %s
                                Confirm changes [y/n]: """ % (interval,
                                                              in_port,
                                                              out_port,
                                                              match_mac,
                                                              src_mac,
                                                              dst_mac,
                                                              src_ip,
                                                              dst_ip,
                                                              description))
            if confirm.lower() in ('y', 'yes'):
                run = self.start_app_arpresponder(out_port, src_mac, dst_mac,
                                                  src_ip, dst_ip, interval,
                                                  in_port, match_mac,
                                                  description)
            else:
                return "Canceling; no changes made.\n"
        elif app == 3:
            interval = moves.input("Enter the check interval in milliseconds [5000]: ")
            if interval == '':
                interval = '5000'
            snmp_port = moves.input("Enter the SNMP port [161]: ")
            if snmp_port == '':
                snmp_port = '161'
            community = moves.input("Enter the SNMP community [public]: ")
            if community == '':
                community = 'public'
            trap_enable = moves.input("Enter SNMP traps?  Enter 'true' to enable "
                                    "or 'false' to keep disabled [true]: ")
            if trap_enable.lower() in ('false', 'f', 'n', 'no'):
                trap_enable = False
            else:
                trap_enable = True
            if trap_enable:
                trap1 = moves.input('Enter IP address of SNMP trap: ')
                trap1_port = moves.input('Enter port number for SNMP trap [162]: ')
                if trap1_port == '':
                    trap1_port = '162'
                trap2 = moves.input('Enter IP address for additional SNMP trap '
                                  'or leave blank for none: ')
                trap2_port = moves.input('Enter port number for additional SNMP trap [162]: ')
                if trap2_port == '':
                    trap2_port = '162'
                confirm = moves.input("""Start SNMP App Summary:
                                    Check Interval: %s
                                    SNMP Port: %s
                                    SNMP Community: %s
                                    Trap Enabled: %s
                                    Trap 1 IP: %s
                                    Trap 1 Port: %s
                                    Trap 2 IP: %s
                                    Trap 2 Port: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (interval,
                                                                  snmp_port,
                                                                  community,
                                                                  trap_enable,
                                                                  trap1,
                                                                  trap1_port,
                                                                  trap2,
                                                                  trap2_port,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_snmp(interval, snmp_port, community,
                                              description, trap_enable, trap1,
                                              trap1_port, trap2, trap2_port)
                else:
                    return "Canceling; no changes made.\n"
            else:
                confirm = moves.input("""Start SNMP App Summary:
                                    Check Interval: %s
                                    SNMP Port: %s
                                    SNMP Community: %s
                                    Trap Enabled: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (interval,
                                                                  snmp_port,
                                                                  community,
                                                                  trap_enable,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_snmp(interval, snmp_port, community,
                                              description, trap_enable)
                else:
                    return "Canceling; no changes made.\n"
        elif app == 4:
            conn_type = moves.input('''Control Bypass Switch using:
                                    1 - IP Address
                                    2 - RS232 Console Cable
                                    Enter selection [1]: ''')
            if conn_type in ('', '1'):
                conn_type = 'IP'
                bypass_ip = moves.input("IP address of Bypass Switch: ")
            elif int(conn_type) == 2:
                conn_type = 'RS232'
            else:
                return "That is not a valid input for Connection Type; canceling HeartbeatBypass."
            bypass_port1 = moves.input("Port number of first port connected to the Bypass Switch: ")
            bypass_port2 = moves.input("Port number of the second port "
                                     "connected to the Bypass Switch: ")
            hb_in = moves.input("Port number on which the App expects heartbeat packets to arrive: ")
            hb_out = moves.input("Port number on which the App sends heartbeat packets: ")
            interval = moves.input("Check interval time in milliseconds that the "
                                 "App should check for heartbeat packets [2000]: ")
            if interval == '':
                interval = '2000'
            proto = moves.input('''Protocol to use for heartbeat packets:
                                 1 - UDP
                                 2 - ICMP
                                 Enter selection [1]: ''')
            if proto in ('', '1'):
                proto = 'UDP'
                src_port = moves.input("Enter source port for UDP heartbeat packets [5555]: ")
                if src_port == '':
                    src_port = '5555'
                dst_port = moves.input("Enter destination port for UDP heartbeat packets [5556]: ")
                if dst_port == '':
                    dst_port = '5556'
            elif int(proto) == 2:
                proto = 'ICMP'
            else:
                return "That is not a valid input for Protocol; canceling HeartbeatBypass."
            src_mac = moves.input("Enter source MAC address for heartbeat "
                                "packets [00:00:00:00:00:01]: ")
            if src_mac == '':
                src_mac = '00:00:00:00:00:01'
            dst_mac = moves.input("Enter destination MAC address for heartbeat "
                                "packets [00:00:00:00:00:02]: ")
            if dst_mac == '':
                dst_mac = '00:00:00:00:00:02'
            src_ip = moves.input("Enter source IP address for heartbeat packets [0.0.0.1]: ")
            if src_ip == '':
                src_ip = '0.0.0.1'
            dst_ip = moves.input("Enter destination IP address for heartbeat packets [0.0.0.2]: ")
            if dst_ip == '':
                dst_ip = '0.0.0.2'
            if conn_type == 'IP' and proto == 'UDP':
                confirm = moves.input("""Start Heartbeat Bypass App Summary:
                                    First Port connected to Bypass Switch: %s
                                    Second Port connected to Bypass Switch: %s
                                    Port to receive Heartbeat packets: %s
                                    Port to send Heartbeat packets: %s
                                    Connection Type: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Heartbeat Source Port: %s
                                    Heartbeat Destination Port: %s
                                    Bypass Switch IP: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (bypass_port1,
                                                                  bypass_port2,
                                                                  hb_in, hb_out,
                                                                  conn_type,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  src_port,
                                                                  dst_port,
                                                                  bypass_ip,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_heartbeatbypass(bypass_port1,
                                                         bypass_port2,
                                                         hb_in, hb_out,
                                                         conn_type, interval,
                                                         description, proto,
                                                         src_mac, dst_mac,
                                                         src_ip, dst_ip,
                                                         src_port, dst_port,
                                                         bypass_ip)
                else:
                    return "Canceling; no changes made.\n"
            elif conn_type == 'IP' and proto == 'ICMP':
                confirm = moves.input("""Start Heartbeat Bypass App Summary:
                                    First Port connected to Bypass Switch: %s
                                    Second Port connected to Bypass Switch: %s
                                    Port to receive Heartbeat packets: %s
                                    Port to send Heartbeat packets: %s
                                    Connection Type: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Bypass Switch IP: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (bypass_port1,
                                                                  bypass_port2,
                                                                  hb_in,
                                                                  hb_out,
                                                                  conn_type,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  bypass_ip,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_heartbeatbypass(bypass_port1,
                                                         bypass_port2, hb_in,
                                                         hb_out, conn_type,
                                                         interval, description,
                                                         proto, src_mac,
                                                         dst_mac, src_ip,
                                                         dst_ip, bypass_ip)
                else:
                    return "Canceling; no changes made.\n"
            elif conn_type == 'RS232' and proto == 'UDP':
                confirm = moves.input("""Start Heartbeat Bypass App Summary:
                                    First Port connected to Bypass Switch: %s
                                    Second Port connected to Bypass Switch: %s
                                    Port to receive Heartbeat packets: %s
                                    Port to send Heartbeat packets: %s
                                    Connection Type: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Heartbeat Source Port: %s
                                    Heartbeat Destination Port: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (bypass_port1,
                                                                  bypass_port2,
                                                                  hb_in,
                                                                  hb_out,
                                                                  conn_type,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  src_port,
                                                                  dst_port,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_heartbeatbypass(bypass_port1,
                                                         bypass_port2, hb_in,
                                                         hb_out, conn_type,
                                                         interval, description,
                                                         proto, src_mac,
                                                         dst_mac, src_ip,
                                                         dst_ip, src_port,
                                                         dst_port)
                else:
                    return "Canceling; no changes made.\n"
            elif conn_type == 'RS232' and proto == 'ICMP':
                confirm = moves.input("""Start Heartbeat Bypass App Summary:
                                    First Port connected to Bypass Switch: %s
                                    Second Port connected to Bypass Switch: %s
                                    Port to receive Heartbeat packets: %s
                                    Port to send Heartbeat packets: %s
                                    Connection Type: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (bypass_port1,
                                                                  bypass_port2,
                                                                  hb_in,
                                                                  hb_out,
                                                                  conn_type,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_heartbeatbypass(bypass_port1,
                                                         bypass_port2, hb_in,
                                                         hb_out, conn_type,
                                                         interval, description,
                                                         proto, src_mac,
                                                         dst_mac, src_ip,
                                                         dst_ip)
                else:
                    return "Canceling; no changes made.\n"
            else:
                return "Something went wrong."
        elif app == 5:
            server_ip = moves.input("IP address of the syslog server: ")
            port = moves.input("Server port [514]: ")
            if port == '':
                port = '514'
            confirm = moves.input("""Start Syslog App Summary:
                                Syslog Server IP: %s
                                Syslog Server Port: %s
                                Description: %s
                                Confirm changes [y/n]: """ % (server_ip, port, description))
            if confirm.lower() in ('y', 'yes'):
                run = self.start_app_syslog(server_ip, port, description)
            else:
                return "Canceling; no changes made.\n"
        elif app == 6:
            conn_type = moves.input('''Bypass Switch connection type:
                                    1 - IP Address
                                    2 - RS232 Console Cable
                                    Enter selection [1]: ''')
            if conn_type in ('', '1'):
                conn_type = 'IP'
                bypass_ip = moves.input("IP address of Bypass Switch: ")
            elif int(conn_type) == 2:
                conn_type = 'RS232'
            else:
                return "That is not a valid input for Connection Type; canceling Bypass Keepalive."
            interval = moves.input("Check interval time in milliseconds that the "
                                 "App should check for heartbeat packets [2000]: ")
            if interval == '':
                interval = '2000'
            if conn_type == 'IP':
                confirm = moves.input('''Start Bypass Keepalive Summary:
                                    Connection Type: %s
                                    Bypass Switch IP: %s
                                    Check Interval: %s
                                    Description: %s
                                    Confirm changes [y/n]''' % (conn_type,
                                                                bypass_ip,
                                                                interval,
                                                                description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_bypasskeepalive(conn_type, interval,
                                                         description, bypass_ip)
                else:
                    return "Canceling; no changes made.\n"
            else:
                confirm = moves.input('''Start Bypass Keepalive Summary:
                                    Connection Type: %s
                                    Check Interval: %s
                                    Description: %s
                                    Confirm changes [y/n]''' % (conn_type, interval, description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_bypasskeepalive(conn_type, interval, description)
                else:
                    return "Canceling; no changes made.\n"
        elif app == 7:
            hb_in = moves.input("Port number on which the App expects heartbeat packets to arrive: ")
            act_comm = moves.input("Command to run when heartbeat packets are detected: ")
            hb_out = moves.input("Port number on which the App sends heartbeat packets: ")
            deact_comm = moves.input("Command to run when heartbeat packets are not detected: ")
            interval = moves.input("Check interval time in milliseconds that the "
                                 "App should check for heartbeat packets [2000]: ")
            if interval == '':
                interval = '2000'
            proto = moves.input('''Protocol to use for heartbeat packets:
                                 1 - UDP
                                 2 - ICMP
                                 Enter selection [1]: ''')
            if proto in ('', '1'):
                proto = 'UDP'
                src_port = moves.input("Enter source port for UDP heartbeat packets [5555]: ")
                if src_port == '':
                    src_port = '5555'
                dst_port = moves.input("Enter destination port for UDP heartbeat packets [5556]: ")
                if dst_port == '':
                    dst_port = '5556'
            elif int(proto) == 2:
                proto = 'ICMP'
            else:
                return "That is not a valid input for Protocol; canceling Heartbeat."
            src_mac = moves.input("Enter source MAC address for heartbeat "
                                "packets [00:00:00:00:00:01]: ")
            if src_mac == '':
                src_mac = '00:00:00:00:00:01'
            dst_mac = moves.input("Enter destination MAC address for heartbeat "
                                "packets [00:00:00:00:00:02]: ")
            if dst_mac == '':
                dst_mac = '00:00:00:00:00:02'
            src_ip = moves.input("Enter source IP address for heartbeat packets [0.0.0.1]: ")
            if src_ip == '':
                src_ip = '0.0.0.1'
            dst_ip = moves.input("Enter destination IP address for heartbeat packets [0.0.0.2]: ")
            if dst_ip == '':
                dst_ip = '0.0.0.2'
            if proto == 'UDP':
                confirm = moves.input("""Start Heartbeat App Summary:
                                    Port to receive Heartbeat packets: %s
                                    Activation Command: %s
                                    Port to send Heartbeat packets: %s
                                    Deactivation Command: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Heartbeat Source Port: %s
                                    Heartbeat Destination Port: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (hb_in,
                                                                  act_comm,
                                                                  hb_out,
                                                                  deact_comm,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  src_port,
                                                                  dst_port,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_heartbeat(hb_in, act_comm, hb_out,
                                                   deact_comm, interval,
                                                   description, proto, src_mac,
                                                   dst_mac, src_ip, dst_ip,
                                                   src_port, dst_port)
                else:
                    return "Canceling; no changes made.\n"
            elif proto == 'ICMP':
                confirm = moves.input("""Start Heartbeat App Summary:
                                    Port to receive Heartbeat packets: %s
                                    Activation Command: %s
                                    Port to send heartbeat packets: %s
                                    Deactivation Command: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (hb_in,
                                                                  act_comm,
                                                                  hb_out,
                                                                  deact_comm,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.start_app_heartbeat(hb_in, act_comm, hb_out,
                                                   deact_comm, interval,
                                                   description, proto, src_mac,
                                                   dst_mac, src_ip, dst_ip)
                else:
                    return "Canceling; no changes made.\n"
            else:
                return "Something went wrong."
        else:
            return "That is not a valid input for App selection; canceling Start App."
        return run

    def start_app_ntp(self, server1, server2=None, user_description=''):
        """Start an NTP app instance.
        
           :param server1: A string, IP address or Domain Name of NTP server.
           :param server2: A string, IP address or Domain Name of NTP server (optional).
           :param user_description: A string, description for app instance (optional).
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        data = {'name': 'NTP',
                'description': 'Syncs time with remote NTP servers.',
                'server1': server1,
                'server2': server2,
                'userDescription': user_description}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def start_app_arpresponder(self, outport, src_mac, dst_mac, src_ip, dst_ip,
                               interval='5000', inport=None, match_srcmac=None,
                               user_description=''):
        """Start an ArpResponder app instance.
        
           :param outport: A string, physical interface to send ARP responses on.
           :param src_mac: A string, source MAC address for ARP response.
           :param dst_mac: A string, destination MAC for ARP response.
           :param src_ip: A string, source IP address for ARP response.
           :param dst_ip: A string, destination IP address for ARP response.
           :param interval: A string, check interval in milliseconds; default 5000
           :param inport: A string, physical source port of incoming ARP request (optional).
           :param match_srcmac: A string, source MAC address of incoming ARP request (optional).
           :param user_description: A string, description for app instance.
           :returns: A string, JSON-formatted.
           :raises: ValueError: if interval variable cannot be converted to int.
           :raises: ValueError: if outport variable cannot be converted to int.
           :raises: ValueError: if inport variable cannot be converted to int.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not an valid input for interval "
                    "(number in milliseconds); canceling Start ArpResponder.", reason)
        try:
            outport_test = int(outport)
            if outport_test > self.ports:
                return "Physical port does not exist on device."
        except ValueError as reason:
            return ("That is not an valid input for output port; "
                    "canceling start ArpResponder.", reason)
        if pm_input_check.mac(src_mac) != 0:
            src_mac = pm_input_check.mac(src_mac)
        else:
            return "That is not a valid MAC address for source MAC; canceling Start ArpResponder."
        if pm_input_check.mac(dst_mac) != 0:
            dst_mac = pm_input_check.mac(dst_mac)
        else:
            return "That is not a valid MAC address for destination MAC; canceling Start ArpResponder."
        if pm_input_check.ipv4(src_ip) != 0:
            src_ip = pm_input_check.ipv4(src_ip)
        else:
            return "That is not a valid IP address for source IP; canceling Start ArpResponder."
        if pm_input_check.ipv4(dst_ip) != 0:
            dst_ip = pm_input_check.ipv4(dst_ip)
        else:
            return "That is not a valid IP address for destination IP; canceling Start ArpResponder."
        data = {'name': 'ArpResponder',
                'description': 'Responds to an arbotrary packet with an ARP response',
                'interval': interval,
                'outPort': outport,
                'macSrc': src_mac,
                'macDst': dst_mac,
                'ipSrc': src_ip,
                'ipDst': dst_ip}
        if inport:
            try:
                inport_test = int(inport)
                if inport_test > self.ports:
                    return "Physical port does not exist on device."
            except ValueError as reason:
                return ("That is not a valid input for input port; "
                        "canceling ArpResponder.", reason)
            data['inPort'] = inport
        if match_srcmac:
            if pm_input_check.mac(match_srcmac) != 0:
                data['matchMacSrc'] = pm_input_check.mac(match_srcmac)
            else:
                return "That is not a valid MAC address for Match Source MAC; canceling Start ArpResponder."
        if user_description:
            data['userDescription'] = user_description
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def start_app_snmp(self, interval='5000', snmp_port='161',
                       community='public', user_description='',
                       trap_enable=True, trap1='1.1.1.1', trap1_port='162',
                       trap2='', trap2_port='162'):
        """Start an SNMP app instance.

           :param interval: A string, check interval in milliseconds; default is 5000.
           :param snmp_port: A string, SNMP port; default 161.
           :param community: A string, SNMP community; default 'public'.
           :param user_description: description for app instance (optional).
           :param trap_enable: A bool, 'True' to enable; 'False' to disable; default True.
           :param trap1: A string, A string, primary trap receiver IP; default 1.1.1.1.
           :param trap1_port: A string, A string, primary trap receiver port; default 162.
           :param trap2: A string, secondary trap receiver IP (optional).
           :param trap2_port: A string, secondary trap receiver port; default 162.
           :returns: A string, JSON-formatted.
           :raises: ValueError: if interval variable cannot be converted to int.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not valid input for Check Interval; canceling SNMP.", reason)
        if not pm_input_check.port(snmp_port):
            return "That is not a valid SNMP port number; canceling SNMP. \n"
        if trap_enable:
            if pm_input_check.ipv4(trap1) != 0:
                trap1 = pm_input_check.ipv4(trap1)
            else:
                return "That is not a valid IP address for Trap 1; canceling SNMP. \n"
            if not pm_input_check.port(trap1_port):
                return "That is not a valid TCP port number for Trap 1; canceling SNMP. \n"
            if trap2 != '':
                if pm_input_check.ipv4(trap2) != 0:
                    trap2 = pm_input_check.ipv4(trap2)
                else:
                    return "That is not a valid IP address for Trap 2; canceling SNMP. \n"
            if not pm_input_check.port(trap2_port):
                return "That is not a valid TCP port number for Trap 2; canceling SNMP. \n"
            data = {'name': 'SNMP',
                    'description': 'Runs an SNMP Server.  The server uses [url=',
                    'interval': interval,
                    'snmpCommunity': community,
                    'snmpPort': snmp_port,
                    'trapEnabled': trap_enable,
                    'trapPort': trap1_port,
                    'trapPort2': trap2_port,
                    'trapReceiver': trap1,
                    'trapReceiver2': trap2,
                    'userDescription': user_description}
        elif not trap_enable:
            data = {'name': 'SNMP',
                    'description': 'Runs an SNMP Server.  The server uses [url=',
                    'interval': interval,
                    'snmpCommunity': community,
                    'snmpPort': snmp_port,
                    'trapEnabled': trap_enable,
                    'userDescription': user_description}
        else:
            return "That is not a valid input for Enable Trap; canceling SNMP."
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def start_app_heartbeatbypass(self, bypass_port1, bypass_port2, hb_in,
                                  hb_out, conn_type='ip', interval='2000',
                                  user_description='', proto='udp',
                                  src_mac='00:00:00:00:00:01',
                                  dst_mac='00:00:00:00:00:02',
                                  src_ip='0.0.0.1', dst_ip='0.0.0.2',
                                  src_port='5555', dst_port='5556',
                                  bypass_ip='1.1.1.1'):
        """Start a HeartbeatBypass app instance.
        
           :param bypass_port1: A string, first port connected to the bypass switch.
           :param bypass_port2: A string, second port connected to the bypass switch.
           :param hb_in: A string, interface on which to expect heartbeat packets.
           :param hb_out: A string, interface on which to send heartbeat packets.
           :param conn_type: A string, connection to bypass management port, either 'ip' or 'rs232'; default ip.
           :param interval: A string, check interval in milliseconds; dedault 2000
           :param user_description: A string, user description for the app instance (optional).
           :param proto: A string, either 'tcp' or 'udp'; default udp.
           :param src_mac: A string, source MAC address for heartbeat; default 00:00:00:00:00:01.
           :param dst_mac: A string, destination MAC address for heartbeat; default 00:00:00:00:00:02.
           :param src_ip: A string, source IP address for heartbeat; default 0.0.0.1
           :param dst_ip: A string, destination IP address for heartbeat; default 0.0.0.2
           :param src_port: A string, source UDP port for hearbeat; default 5555
           :param dst_port: A string, destination UDP for heartbeat; default 5556
           :param bypass_ip: A string, management IP address of bypass switch; default 1.1.1.1.
           :returns: A string, JSON-formatted.
           :raises: ValueError: if bypass_port1 variable cannot be converted to int.
           :raises: ValueError: if bypass_port2 variable cannot be converted to int.
           :raises: ValueError: if hb_in variable cannot be converted to int.
           :raises: ValueError: if hb_out variable cannot be converted to int.
           :raises: ValueError: if interval variable cannot be converted to int.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            pm_port_test = int(bypass_port1)
            if pm_port_test > self.ports:
                return "Physical port does not exist on device."
        except ValueError as reason:
            return ("That is not an valid input for Bypass Port 1; "
                    "canceling HeartbeatBypass.", reason)
        try:
            pm_port_test = int(bypass_port2)
            if pm_port_test > self.ports:
                return "Physical port does not exist on device."
        except ValueError as reason:
            return ("That is not an valid input for Bypass Port 2; "
                    "canceling HeartbeatBypass.", reason)
        try:
            pm_port_test = int(hb_in)
            if pm_port_test > self.ports:
                return "Physical port does not exist on device."
        except ValueError as reason:
            return ("That is not an valid input for Heartbeat In; "
                    "canceling HeartbeatBypass.", reason)
        try:
            pm_port_test = int(hb_out)
            if pm_port_test > self.ports:
                return "Physical port does not exist on device."
        except ValueError as reason:
            return ("That is not an valid input for Heartbeat Out; "
                    "canceling HeartbeatBypass.", reason)
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not a valid input for Check Interval; "
                    "canceling HeartbeatBypass.", reason)
        if proto.upper() in ('UDP', 'ICMP'):
            proto = proto.upper()
        else:
            return ("That is not a valid input for Protocol; "
                    "must be UDP or ICMP.  Canceling HeartbeatBypass.")
        if pm_input_check.mac(src_mac) != 0:
            src_mac = pm_input_check.mac(src_mac)
        else:
            return "That is not a valid MAC address for Source MAC; canceling HeartbeatBypass."
        if pm_input_check.mac(dst_mac) != 0:
            dst_mac = pm_input_check.mac(dst_mac)
        else:
            return "That is not a valid MAC address for Destination MAC; canceling HeartbeatBypass."
        if pm_input_check.ipv4(src_ip) != 0:
                src_ip = pm_input_check.ipv4(src_ip)
        else:
            return "That is not a valid IP address for Source IP; canceling HeartbeatBypass. \n"
        if pm_input_check.ipv4(dst_ip) != 0:
                dst_ip = pm_input_check.ipv4(dst_ip)
        else:
             return "That is not a valid IP address for Destination IP; canceling HeartbeatBypass. \n"
        data = {'bypassPort1': bypass_port1,
                'bypassPort2': bypass_port2,
                'connectionType': conn_type,
                'description': 'This app is used to control a Cubro Bypass Switch device.',
                'inport': hb_in,
                'interval': interval,
                'ipDst': dst_ip,
                'ipSrc': src_ip,
                'macDst': dst_mac,
                'macSrc': src_mac,
                'name': 'HeartbeatBypass',
                'outport': hb_out,
                'protocol': proto,
                'userDescription': user_description}
        if conn_type.upper() in ('IP', 'RS232'):
            data['connectionType'] = conn_type.upper()
            if conn_type.upper() == 'RS232' and self.hardware_generation == '4':
                return ("Controlling a Bypass Switch with RS232 is not "
                        "supported on Gen 4 hardware; please use IP instead.")
            if conn_type.upper() == 'IP':
                if pm_input_check.ipv4(bypass_ip) != 0:
                    data['bypassIP'] = pm_input_check.ipv4(bypass_ip)
                else:
                    return "That is not a valid IP address for Bypass Switch IP; canceling HeartbeatBypass. \n"
        else:
            return ("That is not a valid input for Connection Type; "
                    "must be IP or RS232.  Canceling HeartbeatBypass.")
        if proto == 'UDP':
            if pm_input_check.port(src_port):
                data['portSrc'] = src_port
            else:
                return "That is not a valid UDP port number for Heartbeat Source Port; canceling HeartbeatBypass. \n"
            if pm_input_check.port(dst_port):
                data['portDst'] = dst_port
            else:
                return "That is not a valid UDP port number for Heartbeat Destination Port; canceling HeartbeatBypass. \n"
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def start_app_syslog(self, server_ip, port='514', user_description=''):
        """Start a Syslog app instance.
        
           :param server_ip: A string, IP address of syslog server.
           :param port: A string, A string, syslog port; defaults to 514.
           :param user_description: A string, description for syslog app instance (optional).
           :returns: A string, JSON-formatted.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        if pm_input_check.ipv4(server_ip) != 0:
            server_ip = pm_input_check.ipv4(server_ip)
        else:
            return "That is not a valid server IP address; canceling Start Syslog."
        if not pm_input_check.port(port):
            return "That is not a valid TCP/UDP port number; canceling Start Syslog."
        data = {'description': 'Logs syslog data to a remote server',
                'name': 'Syslog',
                'port': port,
                'server': server_ip,
                'userDescription': user_description}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def start_app_bypasskeepalive(self, conn_type='ip', interval='2000',
                                  description='', bypass_ip='1.1.1.1'):
        """Start a Bypass BypassKeepalive app instance.
        
           :param conn_type: A string, ip or rs232; default is ip.
           :param interval: A string, check interval in milliseconds; default is 2000.
           :param description: A string, description for app instance (optional).
           :param bypass_ip: A string, IP address of bypass switch; default is 1.1.1.1.
           :returns: A string, JSON-formatted.
           :raises: ValueError: if interval variable cannot be converted to int.
           :raises: ConnectionError: if unable to successfully make POST request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not a valid input for Check Interval; "
                    "canceling Bypass Keepalive.", reason)
        data = {'description': 'This app is used to control a Cubro Bypass Switch device.',
                'interval': interval,
                'userDescription': description,
                'name': 'BypassKeepalive'}
        if conn_type.upper() in ('IP', 'RS232'):
            data['connectionType'] = conn_type.upper()
            if conn_type.upper() == 'RS232' and self.hardware_generation == '4':
                return ("Controlling a Bypass Switch with RS232 is not "
                        "supported on Gen 4 hardware; please use IP instead.")
            if conn_type.upper() == 'IP':
                if pm_input_check.ipv4(bypass_ip) != 0:
                    data['bypassIP'] = pm_input_check.ipv4(bypass_ip)
                else:
                    return "That is not a valid input for Bypass Switch IP; canceling Bypass Keepalive."
        else:
            return ("That is not a valid input for Connection Type; "
                    "must be IP or RS232.  Canceling Bypass Keepalive.")
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def start_app_heartbeat(self, hb_in, act_comm, hb_out, deact_comm,
                            interval='2000', user_description='', proto='udp',
                            src_mac='00:00:00:00:00:01',
                            dst_mac='00:00:00:00:00:02', src_ip='0.0.0.1',
                            dst_ip='0.0.0.2', src_port='5555', dst_port='5556'):
        """Start a Heartbeat app instance.
        
           :param hb_in: A string, port on which to expect heartbeat packets.
           :param act_comm: A string, command to execute when heartbeats are detected.
           :param hb_out: A string, port on which to send heartbeat packets.
           :param deact_comm: A string, command to execute when heartbeats are not detected.
           :param interval: A string, intercal in milliseconds; default is 2000.
           :param user_description: A string, user description for app instance (optional).
           :param proto: A string, transport protocol (tcp or udp); default is udp.
           :param src_mac: A string, source MAC address to assign to heartbeat; default is 00:00:00:00:00:01.
           :param dst_mac: A string, destination MAC address to assign to heartbeat; default is 00:00:00:00:00:02.
           :param src_ip: A string, source IP address to assign to heartbeat; default is 0.0.0.1.
           :param dst_ip: A string, destination IP address to assign to heartbeat; default is 0.0.0.2.
           :param src_port: A string, source port to assign to heartbeat; default is 5555.
           :param dst_port: A string, destination port to assign to heartbeat; default is 5556.
           :returns: A string, JSON-formatted.
           :raises: ValueError: if hb_in variable cannot be converted to int.
           :raises: ValueError: if hb_out variable cannot be converted to int.
           :raises: ValueError: if interval variable cannot be converted to int."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            pm_port_test = int(hb_in)
            if pm_port_test > self.ports:
                return "Physical port does not exist on device."
        except ValueError as reason:
            return ("That is not a valid port number for Heartbeat In Port; "
                    "canceling Heartbeat.", reason)
        try:
            pm_port_test = int(hb_out)
            if pm_port_test > self.ports:
                return "Physical port does not exist on device."
        except ValueError as reason:
            return ("That is not a valid port number for Heartbeat Out Port; "
                    "canceling Heartbeat.", reason)
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not a valid input for Check Interval; "
                    "canceling Heartbeat.", reason)
        if proto.upper() in ('UDP', 'ICMP'):
            proto = proto.upper()
        else:
            return ("That is not a valid input for Protocol; "
                    "must be UDP or ICMP.  Canceling Heartbeat.")
        if pm_input_check.mac(src_mac) != 0:
            src_mac = pm_input_check.mac(src_mac)
        else:
            return "That is not a valid input for Source MAC; canceling Heartbeat."
        if pm_input_check.mac(dst_mac) != 0:
            dst_mac = pm_input_check.mac(dst_mac)
        else:
            return "That is not a valid input for Destination MAC; canceling Heartbeat."
        if pm_input_check.ipv4(src_ip) != 0:
            src_ip = pm_input_check.ipv4(src_ip)
        else:
            return "That is not a valid input for Source IP; canceling Heartbeat."
        if pm_input_check.ipv4(dst_ip) != 0:
            dst_ip = pm_input_check.ipv4(dst_ip)
        else:
            return "That is not a valid input for Destination IP; canceling Heartbeat."
        if not pm_input_check.port(src_port):
            return "That is not a valid input for Source Port; canceling Heartbeat."
        if not pm_input_check.port(dst_port):
            return "That is not a valid input for Destination Port; canceling Heartbeat."
        data = {'activateCommand': act_comm,
                'deactivateCommand': deact_comm,
                'description': 'Periodically sends a heartbeat to check if a connection is alive.  Runs a command if the connection goes up or down.',
                'inport': hb_in,
                'interval': interval,
                'ipDst': dst_ip,
                'ipSrc': src_ip,
                'macDst': dst_mac,
                'macSrc': src_mac,
                'name': 'Heartbeat',
                'outport': hb_out,
                'protocol': proto,
                'portSrc': src_port,
                'portDst': dst_port,
                'userDescription': user_description}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_app_guided(self):
        """Interactive menu to modify an app instance.
           
           :returns: A string, JSON-formatted.
           :raises: ValueError: if pid variable can't be converted to int."""
        pid = moves.input("What is the PID of the app instance: ")
        try:
            app = int(pid)
        except ValueError as reason:
            return ("That is not a valid input for PID; canceling modify app.", reason)
        active = self.apps_active()
        active = json.loads(active)
        for app in active:
            if pid == app:
                instance = active[pid]['name']
                break
            else:
                instance = None
        if not instance:
            return "That PID doesn't exist; use Start App to start an app instance."
        description = moves.input("New description for the modified App instance: ")
        if instance == 'NTP':
            server1 = moves.input("Enter NTP target IP or Host Name: ")
            server2 = moves.input("Enter NTP backup IP or Host Name: ")
            confirm = moves.input("""Modify NTP App Summary:
                                Server 1: %s
                                Server 2: %s
                                Description: %s
                                Confirm changes [y/n]: """ % (server1, server2, description))
            if confirm.lower() in ('y', 'yes'):
                run = self.mod_app_ntp(pid, server1, server2, description)
            else:
                return "Canceling; no changes made.\n"
        elif instance == 'ArpResponder':
            interval = moves.input("Enter the check interval in milliseconds [5000]: ")
            if interval == '':
                interval = '5000'
            in_port = moves.input("Physical source port of incoming ARP request (optional): ")
            out_port = moves.input("Physical port for sending ARP response: ")
            match_mac = moves.input("Enter source MAC address of incoming ARP request (optional): ")
            src_mac = moves.input("Source MAC address of outgoing ARP response: ")
            dst_mac = moves.input("Destination MAC address of outgoing ARP response: ")
            src_ip = moves.input("Source IP address of outgoing ARP response: ")
            dst_ip = moves.input("Destination IP of outgoing ARP response: ")
            confirm = moves.input("""Modify ARP Responder App Summary:
                                Check Interval: %s
                                Port of incoming ARP packets: %s
                                Port to send ARP packets: %s
                                Source MAC of incoming ARPs: %s
                                Source MAC of outgoing ARPs: %s
                                Destinaton MAC of outgoing ARPs: %s
                                Source IP of outgoing ARPs: %s
                                Destination IP of outgoing ARPs: %s
                                Description: %s
                                Confirm changes [y/n]: """ % (interval,
                                                              in_port,
                                                              out_port,
                                                              match_mac,
                                                              src_mac,
                                                              dst_mac,
                                                              src_ip,
                                                              dst_ip,
                                                              description))
            if confirm.lower() in ('y', 'yes'):
                run = self.mod_app_arpresponder(pid, out_port, src_mac,
                                                dst_mac, src_ip, dst_ip,
                                                interval, in_port, match_mac,
                                                description)
            else:
                return "Canceling; no changes made.\n"
        elif instance == 'SNMP':
            interval = moves.input("Enter the check interval in milliseconds [5000]: ")
            if interval == '':
                interval = '5000'
            snmp_port = moves.input("Enter the SNMP port [161]: ")
            if snmp_port == '':
                snmp_port = '161'
            community = moves.input("Enter the SNMP community [public]: ")
            if community == '':
                community = 'public'
            trap_enable = moves.input("Enter SNMP traps?  Enter 'true' to "
                                    "enable or 'false' to keep disabled [true]: ")
            if trap_enable.lower() in ('false', 'f', 'n', 'no'):
                trap_enable = False
            else:
                trap_enable = True
            if trap_enable:
                trap1 = moves.input('Enter IP address of SNMP trap: ')
                trap1_port = moves.input('Enter port number for SNMP trap [162]: ')
                if trap1_port == '':
                    trap1_port = '162'
                trap2 = moves.input('Enter IP address for additional SNMP trap '
                                  'or leave blank for none: ')
                trap2_port = moves.input('Enter port number for additional SNMP trap [162]: ')
                if trap2_port == '':
                    trap2_port = '162'
                confirm = moves.input("""Modify SNMP App Summary:
                                    Check Interval: %s
                                    SNMP Port: %s
                                    SNMP Community: %s
                                    Trap Enabled: %s
                                    Trap 1 IP: %s
                                    Trap 1 Port: %s
                                    Trap 2 IP: %s
                                    Trap 2 Port: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (interval,
                                                                  snmp_port,
                                                                  community,
                                                                  trap_enable,
                                                                  trap1,
                                                                  trap1_port,
                                                                  trap2,
                                                                  trap2_port,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.mod_app_snmp(pid, interval, snmp_port,
                                            community, description,
                                            trap_enable, trap1, trap1_port,
                                            trap2, trap2_port)
                else:
                    return "Canceling; no changes made.\n"
            else:
                confirm = moves.input("""Modify SNMP App Summary:
                                    Check Interval: %s
                                    SNMP Port: %s
                                    SNMP Community: %s
                                    Trap Enabled: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (interval,
                                                                  snmp_port,
                                                                  community,
                                                                  trap_enable,
                                                                  description))
                if confirm in ('y', 'yes'):
                    run = self.mod_app_snmp(pid, interval, snmp_port,
                                            community, description, trap_enable)
                else:
                    return "Canceling; no changes made.\n"
        elif instance == 'HeartbeatBypass':
            conn_type = moves.input('''Control Bypass Switch using:
                                    1 - IP Address
                                    2 - RS232 Console Cable
                                    Enter selection [1]: ''')
            if conn_type in ('', '1'):
                conn_type = 'IP'
                bypass_ip = moves.input("IP address of Bypass Switch: ")
            elif int(conn_type) == 2:
                conn_type = 'RS232'
            else:
                return ("That is not a valid input for Connection Type; "
                        "canceling Modify HeartbeatBypass.")
            bypass_port1 = moves.input("Port number of first port connected to the Bypass Switch: ")
            bypass_port2 = moves.input("Port number of the second port "
                                     "connected to the Bypass Switch: ")
            hb_in = moves.input("Port number on which the App expects heartbeat packets to arrive: ")
            hb_out = moves.input("Port number on which the App sends heartbeat packets: ")
            interval = moves.input("Check interval time in milliseconds that the "
                                 "App should check for heartbeat packets [2000]: ")
            if interval == '':
                interval = '2000'
            proto = moves.input('''Protocol to use for heartbeat packets:
                                 1 - UDP
                                 2 - ICMP
                                 Enter selection [1]: ''')
            if proto in ('', '1'):
                proto = 'UDP'
                src_port = moves.input("Enter source port for UDP heartbeat packets [5555]: ")
                if src_port == '':
                    src_port = '5555'
                dst_port = moves.input("Enter destination port for UDP heartbeat packets [5556]: ")
                if dst_port == '':
                    dst_port = '5556'
            elif int(proto) == 2:
                proto = 'ICMP'
            else:
                return "That is not a valid input for Protocol; canceling modify HeartbeatBypass."
            src_mac = moves.input("Enter source MAC address for "
                                "heartbeat packets [00:00:00:00:00:01]: ")
            if src_mac == '':
                src_mac = '00:00:00:00:00:01'
            dst_mac = moves.input("Enter destination MAC address for "
                                "heartbeat packets [00:00:00:00:00:02]: ")
            if dst_mac == '':
                dst_mac = '00:00:00:00:00:02'
            src_ip = moves.input("Enter source IP address for heartbeat packets [0.0.0.1]: ")
            if src_ip == '':
                src_ip = '0.0.0.1'
            dst_ip = moves.input("Enter destination IP address for heartbeat packets [0.0.0.2]: ")
            if dst_ip == '':
                dst_ip = '0.0.0.2'
            if conn_type == 'IP' and proto == 'UDP':
                confirm = moves.input("""Modify Heartbeat Bypass App Summary:
                                    First Port connected to Bypass Switch: %s
                                    Second Port connected to Bypass Switch: %s
                                    Port to receive Heartbeat packets: %s
                                    Port to send Heartbeat packets: %s
                                    Connection Type: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Heartbeat Source Port: %s
                                    Heartbeat Destination Port: %s
                                    Bypass Switch IP: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (bypass_port1,
                                                                  bypass_port2,
                                                                  hb_in,
                                                                  hb_out,
                                                                  conn_type,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  src_port,
                                                                  dst_port,
                                                                  bypass_ip,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.mod_app_heartbeatbypass(pid, bypass_port1,
                                                       bypass_port2, hb_in,
                                                       hb_out, conn_type,
                                                       interval, description,
                                                       proto, src_mac, dst_mac,
                                                       src_ip, dst_ip,
                                                       src_port, dst_port,
                                                       bypass_ip)
                else:
                    return "Canceling; no changes made.\n"
            elif conn_type == 'IP' and proto == 'ICMP':
                confirm = moves.input("""Modify Heartbeat Bypass App Summary:
                                    First Port connected to Bypass Switch: %s
                                    Second Port connected to Bypass Switch: %s
                                    Port to receive Heartbeat packets: %s
                                    Port to send Heartbeat packets: %s
                                    Connection Type: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Bypass Switch IP: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (bypass_port1,
                                                                  bypass_port2,
                                                                  hb_in,
                                                                  hb_out,
                                                                  conn_type,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  bypass_ip,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.mod_app_heartbeatbypass(pid, bypass_port1,
                                                       bypass_port2, hb_in,
                                                       hb_out, conn_type,
                                                       interval, description,
                                                       proto, src_mac, dst_mac,
                                                       src_ip, dst_ip, bypass_ip)
                else:
                    return "Canceling; no changes made.\n"
            elif conn_type == 'RS232' and proto == 'UDP':
                confirm = moves.input("""Modify Heartbeat Bypass App Summary:
                                    First Port connected to Bypass Switch: %s
                                    Second Port connected to Bypass Switch: %s
                                    Port to receive Heartbeat packets: %s
                                    Port to send Heartbeat packets: %s
                                    Connection Type: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Heartbeat Source Port: %s
                                    Heartbeat Destination Port: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (bypass_port1,
                                                                  bypass_port2,
                                                                  hb_in,
                                                                  hb_out,
                                                                  conn_type,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  src_port,
                                                                  dst_port,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.mod_app_heartbeatbypass(pid, bypass_port1,
                                                       bypass_port2, hb_in,
                                                       hb_out, conn_type,
                                                       interval, description,
                                                       proto, src_mac, dst_mac,
                                                       src_ip, dst_ip, src_port,
                                                       dst_port)
                else:
                    return "Canceling; no changes made.\n"
            elif conn_type == 'RS232' and proto == 'ICMP':
                confirm = moves.input("""Modify Heartbeat Bypass App Summary:
                                    First Port connected to Bypass Switch: %s
                                    Second Port connected to Bypass Switch: %s
                                    Port to receive Heartbeat packets: %s
                                    Port to send Heartbeat packets: %s
                                    Connection Type: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (bypass_port1,
                                                                  bypass_port2,
                                                                  hb_in,
                                                                  hb_out,
                                                                  conn_type,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.mod_app_heartbeatbypass(pid, bypass_port1,
                                                       bypass_port2, hb_in,
                                                       hb_out, conn_type,
                                                       interval, description,
                                                       proto, src_mac, dst_mac,
                                                       src_ip, dst_ip)
                else:
                    return "Canceling; no changes made.\n"
            else:
                return "Something went wrong."
        elif instance == 'Syslog':
            server_ip = moves.input("IP address of the syslog server: ")
            port = moves.input("Server port [514]: ")
            if port == '':
                port = '514'
            confirm = moves.input("""Modify Syslog App Summary:
                                Syslog Server IP: %s
                                Syslog Server Port: %s
                                Description: %s
                                Confirm changes [y/n]: """ % (server_ip, port, description))
            if confirm.lower() in ('y', 'yes'):
                run = self.mod_app_syslog(pid, server_ip, port, description)
            else:
                return "Canceling; no changes made.\n"
        elif instance == 'BypassKeepalive':
            conn_type = moves.input('''Bypass Switch connection type:
                                    1 - IP Address
                                    2 - RS232 Console Cable
                                    Enter selection [1]: ''')
            if conn_type in ('', '1'):
                conn_type = 'IP'
                bypass_ip = moves.input("IP address of Bypass Switch: ")
            elif int(conn_type) == 2:
                conn_type = 'RS232'
            else:
                return "That is not a valid input for Connection Type; canceling Bypass Keepalive."
            interval = moves.input("Check interval time in milliseconds that the "
                                 "App should check for heartbeat packets [2000]: ")
            if interval == '':
                interval = '2000'
            if conn_type == 'IP':
                confirm = moves.input('''Modify Bypass Keepalive Summary:
                                    Connection Type: %s
                                    Bypass Switch IP: %s
                                    Check Interval: %s
                                    Description: %s
                                    Confirm changes [y/n]''' % (conn_type,
                                                                bypass_ip,
                                                                interval,
                                                                description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.mod_app_bypasskeepalive(pid, conn_type,
                                                       interval, description,
                                                       bypass_ip)
                else:
                    return "Canceling; no changes made.\n"
            else:
                confirm = moves.input('''Modify Bypass Keepalive Summary:
                                    Connection Type: %s
                                    Check Interval: %s
                                    Description: %s
                                    Confirm changes [y/n]''' % (conn_type, interval, description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.mod_app_bypasskeepalive(pid, conn_type, interval, description)
                else:
                    return "Canceling; no changes made.\n"
        elif instance == 'Heartbeat':
            hb_in = moves.input("Port number on which the App expects heartbeat packets to arrive: ")
            act_comm = moves.input("Command to run when heartbeat packets are detected: ")
            hb_out = moves.input("Port number on which the App sends heartbeat packets: ")
            deact_comm = moves.input("Command to run when heartbeat packets are not detected: ")
            interval = moves.input("Check interval time in milliseconds that the "
                                 "App should check for heartbeat packets [2000]: ")
            if interval == '':
                interval = '2000'
            proto = moves.input('''Protocol to use for heartbeat packets:
                                 1 - UDP
                                 2 - ICMP
                                 Enter selection [1]: ''')
            if proto in ('', '1'):
                proto = 'UDP'
                src_port = moves.input("Enter source port for UDP heartbeat packets [5555]: ")
                if src_port == '':
                    src_port = '5555'
                dst_port = moves.input("Enter destination port for UDP heartbeat packets [5556]: ")
                if dst_port == '':
                    dst_port = '5556'
            elif int(proto) == 2:
                proto = 'ICMP'
            else:
                return "That is not a valid input for Protocol; canceling Modify Heartbeat."
            src_mac = moves.input("Enter source MAC address for "
                                "heartbeat packets [00:00:00:00:00:01]: ")
            if src_mac == '':
                src_mac = '00:00:00:00:00:01'
            dst_mac = moves.input("Enter destination MAC address for "
                                "heartbeat packets [00:00:00:00:00:02]: ")
            if dst_mac == '':
                dst_mac = '00:00:00:00:00:02'
            src_ip = moves.input("Enter source IP address for heartbeat packets [0.0.0.1]: ")
            if src_ip == '':
                src_ip = '0.0.0.1'
            dst_ip = moves.input("Enter destination IP address for heartbeat packets [0.0.0.2]: ")
            if dst_ip == '':
                dst_ip = '0.0.0.2'
            if proto == 'UDP':
                confirm = moves.input("""Modify Heartbeat App Summary:
                                    Port to receive Heartbeat packets: %s
                                    Activation Command: %s
                                    Port to send Heartbeat packets: %s
                                    Deactivation Command: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Heartbeat Source Port: %s
                                    Heartbeat Destination Port: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (hb_in,
                                                                  act_comm,
                                                                  hb_out,
                                                                  deact_comm,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  src_port,
                                                                  dst_port,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.mod_app_heartbeat(pid, hb_in, act_comm, hb_out,
                                                 deact_comm, interval,
                                                 description, proto, src_mac,
                                                 dst_mac, src_ip, dst_ip,
                                                 src_port, dst_port)
                else:
                    return "Canceling; no changes made.\n"
            elif proto == 'ICMP':
                confirm = moves.input("""Modify Heartbeat App Summary:
                                    Port to receive Heartbeat packets: %s
                                    Activation Command: %s
                                    Port to send heartbeat packets: %s
                                    Deactivation Command: %s
                                    Check Interval: %s
                                    Heartbeat Protocol: %s
                                    Heartbeat Source MAC: %s
                                    Heartbeat Destination MAC: %s
                                    Heartbeat Source IP: %s
                                    Heartbeat Destination IP: %s
                                    Description: %s
                                    Confirm changes [y/n]: """ % (hb_in,
                                                                  act_comm,
                                                                  hb_out,
                                                                  deact_comm,
                                                                  interval,
                                                                  proto,
                                                                  src_mac,
                                                                  dst_mac,
                                                                  src_ip,
                                                                  dst_ip,
                                                                  description))
                if confirm.lower() in ('y', 'yes'):
                    run = self.mod_app_heartbeat(pid, hb_in, act_comm, hb_out,
                                                 deact_comm, interval,
                                                 description, proto, src_mac,
                                                 dst_mac, src_ip, dst_ip)
                else:
                    return "Canceling; no changes made.\n"
            else:
                return "Something went wrong."
        else:
            return "That is not a valid input for PID; canceling Modify App."
        return run

    def mod_app_ntp(self, pid, server1, server2=None, user_description=''):
        """Modify an NTP app instance.

           :param pid: A string, Process ID of app instance to modify.
           :param server1: A string, IP address or Domain Name of NTP server.
           :param server2: A string, IP address or Domain Name of NTP server (optional).
           :param user_description: A string, description for app instance (optional).
           :returns: A string, JSON-formatted.
           :raises: ValueError: if pid variable cannot be converted to int.
           :raises: ConnectionError: if unable to successfully make PUT request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(pid)
        except ValueError as reason:
            return ("That is not a valid input for PID; canceling Modify NTP.", reason)
        data = {'name': 'NTP',
                'description': 'Syncs time with remote NTP servers.',
                'pid': pid,
                'server1': server1,
                'server2': server2,
                'userDescription': user_description}
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_app_arpresponder(self, pid, outport, src_mac, dst_mac, src_ip,
                             dst_ip, interval='5000', inport=None,
                             match_srcmac=None, user_description=''):
        """Modify an ArpResponder app instance.

           :param pid: A string, process ID of app instance to modify.
           :param outport: A string, physical interface to send ARP responses on.
           :param src_mac: A string, source MAC address for ARP response.
           :param dst_mac: A string, destination MAC for ARP response.
           :param src_ip: A string, source IP address for ARP response.
           :param dst_ip: A string, destination IP address for ARP response.
           :param interval: A string, check interval in milliseconds; default 5000
           :param inport: A string, physical source port of incoming ARP request (optional).
           :param match_srcmac: A string, source MAC address of incoming ARP request (optional).
           :param user_description: A string, description for app instance.
           :returns: A string, JSON-formatted.
           :raises: ValueError: if pid variable cannot be converted to int.
           :raises: ValueError: if interval variable cannot be converted to int.
           :raises: ValueError: if outport variable cannot be converted to int.
           :raises: ValueError: if inport variable cannot be converted to int.
           :raises: ConnectionError: if unable to successfully make PUT request to device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(pid)
        except ValueError as reason:
            return ("That is not a valid input for PID; canceling Modify ArpResponder.", reason)
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not an valid input for interval "
                    "(number in milliseconds); canceling Modify ArpResponder.", reason)
        try:
            pm_port_check = int(outport)
            if pm_port_check > self.ports:
                return "Physical port does not exist on device."
        except ValueError as reason:
            return ("That is not an valid input for output port; "
                    "canceling Modify ArpResponder.", reason)
        if pm_input_check.mac(src_mac) != 0:
            src_mac = pm_input_check.mac(src_mac)
        else:
            return "That is not a valid MAC address for source MAC; canceling Modify ArpResponder."
        if pm_input_check.mac(dst_mac) != 0:
            dst_mac = pm_input_check.mac(dst_mac)
        else:
            return "That is not a valid MAC address for destination MAC; canceling Modify ArpResponder."
        if pm_input_check.ipv4(src_ip) != 0:
            src_ip = pm_input_check.ipv4(src_ip)
        else:
            return "That is not a valid IP address for source IP; canceling Modify ArpResponder."
        if pm_input_check.ipv4(dst_ip) != 0:
            dst_ip = pm_input_check.ipv4(dst_ip)
        else:
            return "That is not a valid IP address for destination IP; canceling Modify ArpResponder."
        data = {'name': 'ArpResponder',
                'description': 'Responds to an arbitrary packet with an ARP response',
                'pid': pid,
                'interval': interval,
                'outPort': outport,
                'macSrc': src_mac,
                'macDst': dst_mac,
                'ipSrc': src_ip,
                'ipDst': dst_ip}
        if inport:
            try:
                pm_port_check = int(inport)
                if pm_port_check > self.ports:
                    return "Physical port does not exist on device."
            except ValueError as reason:
                return ("That is not a valid input for input port; "
                        "canceling Modify ArpResponder.", reason)
            data['inPort'] = inport
        if match_srcmac:
            if pm_input_check.mac(match_srcmac) != 0:
                data['matchMacSrc'] = pm_input_check.mac(match_srcmac)
        if user_description:
            data['userDescription'] = user_description
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_app_snmp(self, pid, interval='5000', snmp_port='161',
                     community='public', user_description='', trap_enable=True,
                     trap1='1.1.1.1', trap1_port='162', trap2='',
                     trap2_port='162'):
        """Modify an SNMP app instance.

           :param pid: A string, process ID of app instance to modify.
           :param interval: A string, check interval in milliseconds; default is 5000.
           :param snmp_port: A string, SNMP port; default 161.
           :param community: A string, SNMP community; default 'public'.
           :param user_description: description for app instance (optional).
           :param trap_enable: A bool, 'True' to enable; 'False' to disable; default True.
           :param trap1: A string, A string, primary trap receiver IP; default 1.1.1.1.
           :param trap1_port: A string, A string, primary trap receiver port; default 162.
           :param trap2: A string, secondary trap receiver IP (optional).
           :param trap2_port: A string, secondary trap receiver port; default 162.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(pid)
        except ValueError as reason:
            return ("That is not a valid input for PID; canceling Modify SNMP.", reason)
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not valid input for Check Interval; canceling Modify SNMP.", reason)
        try:
            int(snmp_port)
        except ValueError as reason:
            return ("That is not valid input for SNMP Port; canceling Modify SNMP.", reason)
        if trap_enable or isinstance(trap_enable, str) and trap_enable.lower() in ('true', 't', 'yes', 'y'):
            trap_enable = True
            try:
                ip1 = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', trap1)
                trap1 = ip1[0]
            except TypeError as reason:
                return ("That is not a valid IP address for Trap 1; canceling Modify SNMP.", reason)
            try:
                int(trap1_port)
            except ValueError as reason:
                return ("That is not valid input for Trap Port 1; canceling Modify SNMP.", reason)
            if trap2 != '':
                try:
                    ip2 = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', trap2)
                    trap2 = ip2[0]
                except TypeError as reason:
                    return ("That is not a valid IP address for Trap 2; "
                            "canceling Modify SNMP.", reason)
            try:
                int(trap2_port)
            except ValueError as reason:
                return ("That is not valid input for Trap Port 2; canceling Modify SNMP.", reason)
            data = {'name': 'SNMP',
                    'description': 'Runs an SNMP Server.  The server uses [url=',
                    'pid': pid,
                    'interval': interval,
                    'snmpCommunity': community,
                    'snmpPort': snmp_port,
                    'trapEnabled': trap_enable,
                    'trapPort': trap1_port,
                    'trapPort2': trap2_port,
                    'trapReceiver': trap1,
                    'trapReceiver2': trap2,
                    'userDescription': user_description}
        elif trap_enable is False or trap_enable.lower() in ('false', 'f', 'no', 'n'):
            trap_enable = False
            data = {'name': 'SNMP',
                    'description': 'Runs an SNMP Server.  The server uses [url=',
                    'pid': pid,
                    'interval': interval,
                    'snmpCommunity': community,
                    'snmpPort': snmp_port,
                    'trapEnabled': trap_enable,
                    'userDescription': user_description}
        else:
            return "That is not a valid input for Enable Trap; canceling SNMP."
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_app_heartbeatbypass(self, pid, bypass_port1, bypass_port2, hb_in,
                                hb_out, conn_type='ip', interval='2000',
                                user_description='', proto='udp',
                                src_mac='00:00:00:00:00:01',
                                dst_mac='00:00:00:00:00:02', src_ip='0.0.0.1',
                                dst_ip='0.0.0.2', src_port='5555',
                                dst_port='5556', bypass_ip='1.1.1.1'):
        """Modify a HeartbeatBypass app instance.

           :param pid: A string, process ID of app instance to modify.
           :param bypass_port1: A string, first port connected to the bypass switch.
           :param bypass_port2: A string, second port connected to the bypass switch.
           :param hb_in: A string, interface on which to expect heartbeat packets.
           :param hb_out: A string, interface on which to send heartbeat packets.
           :param conn_type: A string, connection to bypass management port, either 'ip' or 'rs232'; default ip.
           :param interval: A string, check interval in milliseconds; dedault 2000
           :param user_description: A string, user description for the app instance (optional).
           :param proto: A string, either 'tcp' or 'udp'; default udp.
           :param src_mac: A string, source MAC address for heartbeat; default 00:00:00:00:00:01.
           :param dst_mac: A string, destination MAC address for heartbeat; default 00:00:00:00:00:02.
           :param src_ip: A string, source IP address for heartbeat; default 0.0.0.1
           :param dst_ip: A string, destination IP address for heartbeat; default 0.0.0.2
           :param src_port: A string, source TCP or UDP port for hearbeat; default 5555
           :param dst_port: A string, destination TCP or UDP for heartbeat; default 5556
           :param bypass_ip: A string, management IP address of bypass switch; default 1.1.1.1.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(pid)
        except ValueError as reason:
            return ("That is not a valid input for PID; canceling Modify HeartbeatBypass.", reason)
        try:
            int(bypass_port1)
        except ValueError as reason:
            return ("That is not a valid port number for Bypass Port 1; "
                    "canceling Modify HeartbeatBypass.", reason)
        try:
            int(bypass_port2)
        except ValueError as reason:
            return ("That is not a valid port number for Bypass Port 2; "
                    "canceling Modify HeartbeatBypass.", reason)
        try:
            int(hb_in)
        except ValueError as reason:
            return ("That is not a valid port number for Heartbeat In Port; "
                    "canceling Modify HeartbeatBypass.", reason)
        try:
            int(hb_out)
        except ValueError as reason:
            return ("That is not a valid port number for Heartbeat Out Port; "
                    "canceling Modify HeartbeatBypass.", reason)
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not a valid input for Check Interval; "
                    "canceling Modify HeartbeatBypass.", reason)
        if proto.upper() in ('UDP', 'ICMP'):
            proto = proto.upper()
        else:
            return ("That is not a valid input for Protocol; must be UDP or "
                    "ICMP.  Canceling Modify HeartbeatBypass.")
        #MAC address regex check
        try:
            src_ip_check = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', src_ip)
            src_ip = src_ip_check[0]
        except TypeError as reason:
            return ("That is not a valid input for Source IP; "
                    "canceling Modify HeartbeatBypass.", reason)
        try:
            dst_ip_check = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', dst_ip)
            dst_ip = dst_ip_check[0]
        except TypeError as reason:
            return ("That is not a valid input for Destination IP; "
                    "canceling Modify HeartbeatBypass.", reason)
        data = {'bypassPort1': bypass_port1,
                'bypassPort2': bypass_port2,
                'connectionType': conn_type,
                'description': 'This app is used to control a Cubro Bypass Switch device.',
                'inport': hb_in,
                'interval': interval,
                'ipDst': dst_ip,
                'ipSrc': src_ip,
                'macDst': dst_mac,
                'macSrc': src_mac,
                'name': 'HeartbeatBypass',
                'outport': hb_out,
                'pid': pid,
                'protocol': proto,
                'userDescription': user_description}
        if conn_type.upper() in ('IP', 'RS232'):
            data['connectionType'] = conn_type.upper()
            if conn_type.upper() == 'RS232' and self.hardware_generation == '4':
                return ("Controlling a Bypass Switch with RS232 is not "
                        "supported on Gen 4 hardware; please use IP instead.")
            if conn_type.upper() == 'IP':
                try:
                    ip_check = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', bypass_ip)
                    data['bypassIP'] = ip_check[0]
                except TypeError as reason:
                    return ("That is not a valid input for Bypass Switch IP; "
                            "canceling Modify HeartbeatBypass.", reason)
        else:
            return ("That is not a valid input for Connection Type; must be "
                    "IP or RS232.  Canceling Modify HeartbeatBypass.")
        if proto == 'UDP':
            try:
                int(src_port)
            except ValueError as reason:
                return ("That is not a valid input for Source Port; "
                        "canceling Modify HeartbeatBypass.", reason)
            data['portSrc'] = src_port
            try:
                int(dst_port)
            except ValueError as reason:
                return ("That is not a valid input for Destination Port; "
                        "canceling Modify HeartbeatBypass.", reason)
            data['portDst'] = dst_port
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_app_syslog(self, pid, server_ip, port='514', user_description=''):
        """Modify a Syslog app instance.
        
           :param pid: A string, process ID of the app instance to modify.
           :param server_ip: A string, IP address of syslog server.
           :param port: A string, A string, syslog port; defaults to 514.
           :param user_description: A string, description for syslog app instance (optional).
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(pid)
        except ValueError as reason:
            return ("That is not a valid input for PID; canceling Modify Syslog.", reason)
        try:
            ip_check = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', server_ip)
            server = ip_check[0]
        except TypeError as reason:
            return ("That is not a valid server IP address; canceling Modify Syslog.", reason)
        try:
            int(port)
        except ValueError as reason:
            return ("That is not a valid input for port number; canceling Modify Syslog.", reason)
        data = {'description': 'Logs syslog info to a remote server',
                'name': 'Syslog',
                'pid': pid,
                'port': port,
                'server': server,
                'userDescription': user_description}
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_app_bypasskeepalive(self, pid, conn_type='ip', interval='2000',
                                description='', bypass_ip='1.1.1.1'):
        """Modify a BypassKeepalive app instance.
        
           :param pid: A string, process ID of the app instance to modify.
           :param conn_type: A string, ip or rs232; default is ip.
           :param interval: A string, check interval in milliseconds; default is 2000.
           :param description: A string, description for app instance (optional).
           :param bypass_ip: A string, IP address of bypass switch; default is 1.1.1.1.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(pid)
        except ValueError as reason:
            return ("That is not a valid input for PID; canceling Modify Bypass Keepalive.", reason)
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not a valid input for Check Interval; "
                    "canceling Bypass Keepalive.", reason)
        data = {'pid': pid,
                'description': 'This app is used to control a Cubro Bypass Switch device.',
                'interval': interval,
                'userDescription': description,
                'name': 'BypassKeepalive'}
        if conn_type.upper() in ('IP', 'RS232'):
            data['connectionType'] = conn_type.upper()
            if conn_type.upper() == 'RS232' and self.hardware_generation == '4':
                return ("Controlling a Bypass Switch with RS232 is not "
                        "supported on Gen 4 hardware; please use IP instead.")
            if conn_type.upper() == 'IP':
                try:
                    ip_check = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', bypass_ip)
                    data['bypassIP'] = ip_check[0]
                except TypeError as reason:
                    return ("That is not a valid input for Bypass Switch IP; "
                            "canceling Modify Bypass Keepalive.", reason)
        else:
            return ("That is not a valid input for Connection Type; "
                    "must be IP or RS232.  Canceling Modify Bypass Keepalive.")
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_app_heartbeat(self, pid, hb_in, act_comm, hb_out, deact_comm,
                          interval='2000', user_description='', proto='udp',
                          src_mac='00:00:00:00:00:01',
                          dst_mac='00:00:00:00:00:02', src_ip='0.0.0.1',
                          dst_ip='0.0.0.2', src_port='5555', dst_port='5556'):
        """Modify a Heartbeat app instance.
        
           :param pid: A string, process ID of app instance to modify.
           :param hb_in: A string, port on which to expect heartbeat packets.
           :param act_comm: A string, command to execute when heartbeats are detected.
           :param hb_out: A string, port on which to send heartbeat packets.
           :param deact_comm: A string, command to execute when heartbeats are not detected.
           :param interval: A string, intercal in milliseconds; default is 2000.
           :param user_description: A string, user description for app instance (optional).
           :param proto: A string, transport protocol (tcp or udp); default is udp.
           :param src_mac: A string, source MAC address to assign to heartbeat; default is 00:00:00:00:00:01.
           :param dst_mac: A string, destination MAC address to assign to heartbeat; default is 00:00:00:00:00:02.
           :param src_ip: A string, source IP address to assign to heartbeat; default is 0.0.0.1.
           :param dst_ip: A string, destination IP address to assign to heartbeat; default is 0.0.0.2.
           :param src_port: A string, source port to assign to heartbeat; default is 5555.
           :param dst_port: A string, destination port to assign to heartbeat; default is 5556.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            int(pid)
        except ValueError as reason:
            return ("That is not a valid input for PID; "
                    "canceling Modify Heartbeat.", reason)
        try:
            int(hb_in)
        except ValueError as reason:
            return ("That is not a valid port number for Heartbeat In Port; "
                    "canceling Modify Heartbeat.", reason)
        try:
            int(hb_out)
        except ValueError as reason:
            return ("That is not a valid port number for Heartbeat Out Port; "
                    "canceling Modify Heartbeat.", reason)
        try:
            int(interval)
        except ValueError as reason:
            return ("That is not a valid input for Check Interval; "
                    "canceling Modify Heartbeat.", reason)
        if proto.upper() in ('UDP', 'ICMP'):
            proto = proto.upper()
        else:
            return ("That is not a valid input for Protocol; "
                    "must be UDP or ICMP.  Canceling Modify Heartbeat.")
        #MAC address regex check
        try:
            src_ip_check = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', src_ip)
            src_ip = src_ip_check[0]
        except TypeError as reason:
            return ("That is not a valid input for Source IP; "
                    "canceling Modify Heartbeat.", reason)
        try:
            dst_ip_check = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', dst_ip)
            dst_ip = dst_ip_check[0]
        except TypeError as reason:
            return ("That is not a valid input for Destination IP; "
                    "canceling Modify Heartbeat.", reason)
        try:
            int(src_port)
        except ValueError as reason:
            return ("That is not a valid input for Source Port; "
                    "canceling Modify Heartbeat.", reason)
        try:
            int(dst_port)
        except ValueError as reason:
            return ("That is not a valid input for Destination Port; "
                    "canceling Modify Heartbeat.", reason)
        data = {'activateCommand': act_comm,
                'deactivateCommand': deact_comm,
                'description': 'Periodically sends a heartbeat to check if a connection is alive.  Runs a command if the connection goes up or down.',
                'inport': hb_in,
                'interval': interval,
                'ipDst': dst_ip,
                'ipSrc': src_ip,
                'macDst': dst_mac,
                'macSrc': src_mac,
                'name': 'Heartbeat',
                'outport': hb_out,
                'pid': pid,
                'protocol': proto,
                'portSrc': src_port,
                'portDst': dst_port,
                'userDescription': user_description}
        try:
            response = requests.put(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def call_app_action_guided(self):
        """Interactive menu to call a custom app action."""
        pid = moves.input('Enter the PID of the app instance: ')
        name = moves.input('Enter the name of the custom app action: ')
        confirm = moves.input("""Call App Action Summary:
                            Process ID: %s
                            Action Name: %s
                            Confirm changes [y/n]: """ % (pid, name))
        if confirm.lower() in ('y', 'yes'):
            run = self.call_app_action(pid, name)
            return run
        return "Canceling; no changes made.\n"

    def call_app_action(self, pid, name):
        """Call a custom app action.
        
           :param pid: A string, process ID of the app instance.
           :param name: A string, name of custom app action.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps/action?'
        else:
            uri = 'http://' + self._address + '/rest/apps/action?'
        try:
            pid = int(pid)
        except ValueError as reason:
            return ("That is not a valid PID; canceling Call App Action.", reason)
        data = {'pid': pid,
                'action_name': name}
        try:
            response = requests.post(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def kill_app_guided(self):
        """Interactive menu to stop an active app instance."""
        pid = moves.input('What is the process ID of the app to kill: ')
        confirm = moves.input("""Kill App Summary:
                            Process ID: %s
                            Confirm changes [y/n]: """ % pid)
        if confirm.lower() in ('y', 'yes'):
            run = self.kill_app(pid)
            return run
        return "Canceling; no changes made.\n"

    def kill_app(self, pid):
        """Stop an active app instance.
        
           :param pid: A string, process ID of app instance to terminate.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/apps?'
        else:
            uri = 'http://' + self._address + '/rest/apps?'
        try:
            pid = int(pid)
        except ValueError as reason:
            return ("That is not a valid input for PID; canceling Kill App.", reason)
        data = {'pid': pid}
        try:
            response = requests.delete(uri, data=data, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_hash_algorithms_guided(self):
        """Interactive menu to set group hash algorithms."""
        if self.hardware in ('4', '2'):
            macsa = moves.input('Type "true" to use MAC source address; '
                              'type "false" to ignore [true]: ')
            macda = moves.input('Type "true" to use MAC destination address; '
                              'type "false" to ignore [true]: ')
            ether = moves.input('Type "true" to use ether type; type '
                              '"false" to ignore [true]: ')
            ipsa = moves.input('Type "true" to use IP source address; '
                             'type "false" to ignore [true]: ')
            ipda = moves.input('Type "true" to use IP destination address; '
                             'type "false" to ignore [true]: ')
            proto = moves.input('Type "true" to use IP protocol; type "false" to ignore [true]: ')
            src = moves.input('Type "true" to use source port; type "false" to ignore [true]: ')
            dst = moves.input('Type "true" to use destination port; type "false" to ignore [true]: ')
            confirm = moves.input("""Set Hash Algorithms Summary:
                                Use Source MAC Address: %s
                                Use Destination MAC Address: %s
                                Use Ethertype:%s
                                Use Source IP Address: %s
                                Use Destination IP Address: %s
                                Use IP Protocol: %s
                                Use Source Port: %s
                                Use Destination Port: %s
                                Confirm changes [y/n]: """ % (macsa,
                                                              macda,
                                                              ether,
                                                              ipsa,
                                                              ipda,
                                                              proto,
                                                              src,
                                                              dst))
            if confirm.lower() in ('y', 'yes'):
                run = self.set_hash_algorithms(macsa, macda, ether, ipsa, ipda, proto, src, dst)
            else:
                return "Canceling; no changes made.\n"
        else:
            ipsa = moves.input('Type "true" to use IP source address; '
                             'type "false" to ignore [true]: ')
            ipda = moves.input('Type "true" to use IP destination address; '
                             'type "false" to ignore [true]: ')
            proto = moves.input('Type "true" to use IP protocol; type "false" to ignore [true]: ')
            src = moves.input('Type "true" to use source port; type "false" to ignore [true]: ')
            dst = moves.input('Type "true" to use destination port; type "false" to ignore [true]: ')
            confirm = moves.input("""Set Hash Algorithms Summary:
                                Use Source IP Address: %s
                                Use Destination IP Address: %s
                                Use IP Protocol: %s
                                Use Source Port: %s
                                Use Destination Port: %s
                                Confirm changes [y/n]: """ % (ipsa,
                                                              ipda,
                                                              proto,
                                                              src,
                                                              dst))
            if confirm.lower() in ('y', 'yes'):
                run = self.set_hash_algorithms('', '', '', ipsa,
                                               ipda, proto, src, dst)
            else:
                return "Canceling; no changes made.\n"
        return run

    def set_hash_algorithms(self, macsa, macda, ether,
                            ipsa, ipda, proto, src, dst):
        """Set group hash algorithms on the Packetmaster.
           
           :param macsa: A bool, True to enable, False to disable.
           :param macda: A bool, True to enable, False to disable.
           :param ether: A bool, True to enable, False to disable.
           :param ipsa: A bool, True to enable, False to disable.
           :param ipda: A bool, True to enable, False to disable.
           :param proto: A bool, True to enable, False to disable.
           :param src: A bool, True to enable, False to disable.
           :param dst: A bool, True to enable, False to disable.
           :returns: A string, JSON-formatted."""
        #EX2 has only 'ipsa', 'ipda', 'ip_protocol', 'scp_port', 'dst_port'
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/grouphash?'
        else:
            uri = 'http://' + self._address + '/rest/device/grouphash?'
        if macsa in (False, 'False', 'false', 'f', 'No', 'no', 'n', 'F', 'N'):
            macsa = False
        else:
            macsa = True
        if macda in (False, 'False', 'false', 'f', 'No', 'no', 'n', 'F', 'N'):
            macda = False
        else:
            macda = True
        if ether in (False, 'False', 'false', 'f', 'No', 'no', 'n', 'F', 'N'):
            ether = False
        else:
            ether = True
        if ipsa in (False, 'False', 'false', 'f', 'No', 'no', 'n', 'F', 'N'):
            ipsa = False
        else:
            ipsa = True
        if ipda in (False, 'False', 'false', 'f', 'No', 'no', 'n', 'F', 'N'):
            ipda = False
        else:
            ipda = True
        if proto in (False, 'False', 'false', 'f', 'No', 'no', 'n', 'F', 'N'):
            proto = False
        else:
            proto = True
        if src in (False, 'False', 'false', 'f', 'No', 'no', 'n', 'F', 'N'):
            src = False
        else:
            src = True
        if dst in (False, 'False', 'false', 'f', 'No', 'no', 'n', 'F', 'N'):
            dst = False
        else:
            dst = True
        if self.hardware in ('4', '2'):
            data = {'macsa': macsa,
                    'macda': macda,
                    'ether_type': ether,
                    'ipsa': ipsa,
                    'ipda': ipda,
                    'ip_protocol': proto,
                    'src_port': src,
                    'dst_port': dst}
        else:
            #May need to become 'elif self.hardware == '3.1'' with new
            #elif statements for gen 3.  Need EX5-2 and EX12 to verify
            data = {'ipsa': ipsa,
                      'ipda': ipda,
                      'ip_protocol': proto,
                      'src_port': src,
                      'dst_port': dst}
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_rule_permanence_guided(self):
        """Interactive menu to set Rule Mode Permanance."""
        perm = moves.input('type "true" to enable permanent rules; '
                         'type "false" disable them [false]: ').lower()
        confirm = moves.input("""Set Rule Permamence Summary:
                            Permanance Enabled: %s
                            Confirm changes [y/n]: """ % perm)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_rule_permanence(perm)
            return run
        return "Canceling; no changes made.\n"

    def set_rule_permanence(self, permanence):
        """Set Rule Mode Permanance on the Packetmaster.
        
           :param permanence: A bool, True to enable, False to disable.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/permanentrulesmode?'
        else:
            uri = 'http://' + self._address + '/rest/device/permanentrulesmode?'
        if isinstance(permanence, bool) and permanence:
            permanence = True
        elif isinstance(permanence, str) and permanence.lower() in ('true', 'yes',
                                                                    'y', 't'):
            permanence = True
        else:
            permanence = False
        data = {'state': permanence}
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_storage_mode_guided(self):
        """Interactive menu to set Rule Storage Mode."""
        mode = moves.input('''Select the rule storage mode:
                        1 - Simple
                        2 - IPv6
                        Enter the number of your selection: ''')
        try:
            mode = int(mode)
        except ValueError as reason:
            return ("That is not a valid selection; "
                    "canceling set rule storage mode.", reason)
        if mode == 1:
            mode = 'simple'
        elif mode == 2:
            mode = 'ipv6'
        else:
            return ("That is not a valid selection; "
                    "canceling set rule storage mode.")
        confirm = moves.input("""Set Rule Storage Summary:
                            Rule Storage Mode: %s
                            Confirm changes [y/n]: """ % mode)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_storage_mode(mode)
            return run
        return "Canceling; no changes made.\n"

    def set_storage_mode(self, mode):
        """Set Rule Storage Mode of the Packetmaster.
        
           :param mode: A string, 'simple' for more rules but no ipv6 support, 'ipv6' for ipv6 support and fewer rules.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/rulestoragemode?'
        else:
            uri = 'http://' + self._address + '/rest/device/rulestoragemode?'
        try:
            mode = mode.lower()
        except AttributeError as reason:
            return ("That is not a valid setting; "
                    "canceling set rule storage mode.", reason)
        if mode == 'simple':
            data = {'mode': 'simple'}
        elif mode == 'ipv6':
            data = {'mode': 'ipv6'}
        else:
            return ("That is not a valid selection; "
                    "canceling set rule storage mode.")
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def add_user_guided(self):
        """Interactive menu to add a user account to the Packetmaster."""
        username = moves.input('Enter a username: ').strip()
        access_level = moves.input("""Choose an access level for the user:
                                1 - Read only
                                7 - Write
                               31 - Super User
                               Enter the numeric value for the access level: """).strip()
        passwd = moves.input("Enter a password for the user: ")
        description = moves.input("Add a description for this user: ")
        rad = moves.input("Use RADIUS authentication?  Y or N [N]: ").lower()
        confirm = moves.input("""Add User Summary:
                            Username: %s
                            Access Level: %s
                            Password Hidden
                            Description: %s
                            Use RADIUS AAA: %s
                            Confirm changes [y/n]: """ % (username,
                                                          access_level,
                                                          description,
                                                          rad))
        if confirm.lower() in ('y', 'yes'):
            run = self.add_user(username, access_level,
                                passwd, description, rad)
            return run
        return "Canceling; no changes made.\n"

    def add_user(self, username, access_level,
                 passwd, description='', rad=False):
        """Add a user account to the Packetmaster.
        
           :param username: A string, username for new user.
           :param access_level: An int, 1 = read only, 7 = write, 31 = super user.
           :param passwd: A string, user password.
           :param description: A string, description for user (optional).
           :param rad: A bool, True for RADIUS authentication, False for local auth; default is False.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/users?'
        else:
            uri = 'http://' + self._address + '/rest/users?'
        user_list = []
        if username == '':
            return "That is not a valid username; canceling Add User."
        active_users = self.get_users()
        json_users = json.loads(active_users)
        for user in json_users:
            user_list.append(json_users[user]['username'])
        if username in user_list:
            return ("That username is already in use; "
                    "use Modify User; canceling Add User.")
        try:
            access_level = int(access_level)
        except ValueError as reason:
            return ("That is not a valid user access level; canceling Add User.", reason)
        if access_level not in (1, 7, 31):
            return "That is not a valid user access level; canceling Add User."
        if isinstance(rad, bool) and rad:
            rad = True
        elif isinstance(rad, str) and rad.lower() in ('true', 'y', 'yes', 't'):
            rad = True
        else:
            rad = False
        data = {'username': username,
                'accesslevel': access_level,
                'password': passwd,
                'description': description,
                'radius': rad}
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def mod_user_guided(self):
        """Interactive menu to modify a user account on the Packetmaster."""
        cur_name = moves.input('What is the username you would like to modify: ')
        new_name = moves.input('Enter a new username: ')
        description = moves.input("Enter a new description; "
                                "this will overwrite the old description: ")
        access_level = moves.input("""Choose an access level for the user:
                                1 - Read only
                                7 - Write
                               31 - Super User
                               Enter the numeric value for the access level: """).strip()
        passwd = moves.input("Enter a new password for the user: ")
        rad = moves.input("Use RADIUS authentication?  Y or N [N]: ").lower()
        confirm = moves.input("""Modify User Summary:
                            Modify User: %s
                            New Username: %s
                            Access Level: %s
                            Password Hidden
                            Description: %s
                            Use RADIUS AAA: %s
                            Confirm changes [y/n]: """ % (cur_name,
                                                          new_name,
                                                          access_level,
                                                          description,
                                                          rad))
        if confirm.lower() in ('y', 'yes'):
            run = self.mod_user(cur_name, new_name,
                                access_level, passwd, description, rad)
            return run
        return "Canceling; no changes made.\n"

    def mod_user(self, cur_name, new_name,
                 access_level, passwd, description='', rad=False):
        """Modify a user account on the Packetmaster.
        
           :param cur_name: A string, username for user to edit.
           :param new_name: A string, new username for user.
           :param access_level: An int, 1 = read only, 7 = write, 31 = super user.
           :param passwd: A string, user password.
           :param description: A string, description for user (optional).
           :param rad: A bool, True for RADIUS authentication, False for local auth; default is False.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/users?'
        else:
            uri = 'http://' + self._address + '/rest/users?'
        user_list = []
        active_users = self.get_users()
        json_users = json.loads(active_users)
        for user in json_users:
            user_list.append(json_users[user]['username'])
        if cur_name not in user_list:
            return ("That username does not exist; "
                    "please use Add User.  Canceling Modify User.")
        if new_name == '':
            return "That is not a valid username; canceling Modify User."
        try:
            access_level = int(access_level)
        except ValueError as reason:
            return ("That is not a valid user access level; "
                    "canceling Modify User.", reason)
        if access_level not in (1, 7, 31):
            return ("That is not a valid user access level; "
                    "canceling Modify User.")
        if isinstance(rad, bool) and rad:
            rad = True
        elif isinstance(rad, str) and rad.lower() in ('true', 'y', 'yes', 't'):
            rad = True
        else:
            rad = False
        data = {'username': cur_name,
                'new_username': new_name,
                'accesslevel': access_level,
                'password': passwd,
                'description': description,
                'radius': rad}
        try:
            response = requests.put(uri, data=data,
                                    auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def delete_user_guided(self):
        """Interactive menu to delete a user account from the Packetmaster."""
        username = moves.input('What is the user name to delete: ')
        confirm = moves.input("""Delete User Summary:
                            Delete User: %s
                            Confirm changes [y/n]: """ % username)
        if confirm.lower() in ('y', 'yes'):
            run = self.delete_user(username)
            return run
        return "Canceling; no changes made.\n"

    def delete_user(self, username):
        """Delete a user account from the Packetmaster.
        
           param username: A string, username of user to delete.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/users?'
        else:
            uri = 'http://' + self._address + '/rest/users?'
        user_list = []
        active_users = self.get_users()
        json_users = json.loads(active_users)
        for user in json_users:
            user_list.append(json_users[user]['username'])
        if username not in user_list:
            return "That username does not exist"
        data = {'name': username}
        try:
            response = requests.delete(uri, data=data,
                                       auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_uac_guided(self):
        """Interactive menu to enable/disable user authentication."""
        access = moves.input(('type "true" to turn on UAC; '
                            'type "false" to turn it off [false]: ').lower())
        confirm = moves.input("""UAC Summary:
                            User Access Control On: %s
                            Confirm changes [y/n]: """ % access)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_uac(access)
            return run
        return "Canceling; no changes made.\n"

    def set_uac(self, uac):
        """Enable/disable user authentication on the Packetmaster.
        
           :param uac: A bool, True for enable, False for disable.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/users/uac?'
        else:
            uri = 'http://' + self._address + '/rest/users/uac?'
        if isinstance(uac, bool) and uac:
            uac = True
        elif isinstance(uac, str) and uac.lower() in ('true', 'yes', 't', 'y'):
            uac = True
        else:
            uac = False
        data = {'state': uac}
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_radius_guided(self):
        """Interactive menu to set RADIUS configuration."""
        server = moves.input('Enter the IP address '
                           'of the RADIUS server: ').strip()
        print("Enter the RADIUS secret.")
        secret = getpass()
        refresh = moves.input("Enter the refresh rate of the "
                            "RADIUS session in seconds: ")
        level = moves.input('''Enter the RADIUS login level.
        Determines the user access level that a user has
        logging in via RADIUS but without a local user account.
                             0 - no access
                             1 - read access
                             7 - write access
                            31 - super user access
                            [0]: ''')
        port = moves.input('Enter the UDP port of the RADIUS server [1812]: ')
        if port == '':
            port = 1812
        confirm = moves.input("""RADIUS Summary:
                            RADIUS Server: %s
                            Secret Hidden
                            Refresh Rate: %s
                            Default RADIUS Login Level: %s
                            RADIUS Port: %s
                            Confirm changes [y/n]: """ % (server, refresh,
                                                          level, port))
        if confirm.lower() in ('y', 'yes'):
            run = self.set_radius(server, secret, refresh, level, port)
            return run
        return "Canceling; no changes made.\n"

    def set_radius(self, server, secret, refresh, level, port=1812):
        """Set RADIUS configuration.
        
           :param server: A string, IP address or Domain Name of RADIUS server.
           :param secret: A string, RADIUS secret.
           :param refresh: An int, refresh rate in milliseconds.
           :param level: An int, default login level for RADIUS. 0 for None, 1 for read, 7 for write, 31 for super user.
           :param port: An int, RADIUS port number; default is 1812.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/users/radius?'
        else:
            uri = 'http://' + self._address + '/rest/users/radius?'
        server = server.strip()
        try:
            refresh = int(refresh)
        except ValueError as reason:
            return ("That is not a valid input for refresh rate; "
                    "canceling Set Radius.", reason)
        try:
            level = int(level)
        except ValueError as reason:
            return ("That is not a valid input for login level; "
                    "canceling Set Radius.", reason)
        if level not in (0, 1, 7, 31):
            return ("That is not a valid input for RADIUS login level; "
                    "canceling Set Radius.")
        try:
            port = int(port)
        except ValueError as reason:
            return ("That is not a valid port input; "
                    "canceling RADIUS settings call.", reason)
        data = {'server': server,
                'port': port,
                'secret': secret,
                'radius_login_level': level,
                'refresh_rate': refresh}
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_https_guided(self):
        """Interactive menu to enable/disable HTTPS web interface."""
        enabled = moves.input(('Type "true" to enable HTTPS on web interface; '
                             'type "false" to turn it off [false]: ').lower())
        if enabled == 'true':
            print("Please enter the SSL password")
            ssl = getpass()
        else:
            enabled = False
            ssl = 'none'
        confirm = moves.input("""Set HTTPS Summary:
                            HTTPS Secure Web Server On: %s
                            Confirm changes [y/n]: """ % enabled)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_https(enabled, ssl)
            return run
        return "Canceling; no changes made.\n"

    def set_https(self, enabled=False, ssl=None):
        """Enable/disable HTTPS web interface.
        
           :param enabled: A bool, True to enable, False to disable. Default is False.
           :param ssl: A string, SSL/TLS password. Default None.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/https?'
        else:
            uri = 'http://' + self._address + '/rest/device/https?'
        if enabled.lower() == 'true' or enabled is True:
            enabled = True
        else:
            enabled = False
        data = {'https_enabled': enabled,
                'ssl_password': ssl}
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = "No Response"
            raise error

    def set_telnet_guided(self):
        """Interactive menu to enable/disable Telnet service."""
        enabled = moves.input(('Type "true" to enable Telnet; '
                             'type "false" to turn it off [false]: ').lower())
        confirm = moves.input("""Set Telnet Summary:
                            Telnet Service On: %s
                            Confirm changes [y/n]: """ % enabled)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_telnet(enabled)
            return run
        return "Canceling; no changes made.\n"

    def set_telnet(self, enabled=False):
        """Enable/disable Telnet service on the Packetmaster.
        
           :param enabled: A bool, True for enable, False for disable. Default is False.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/telnet?'
        else:
            uri = 'http://' + self._address + '/rest/device/telnet?'
        if enabled.lower() == 'true' or enabled is True:
            enabled = True
        else:
            enabled = False
        data = {'activated': enabled}
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return (json.dumps(info, indent=4),
                    "Device must be rebooted for change to take effect")
        except ConnectionError as error:
            content = "No Response"
            raise error

    def del_web_log(self):
        """Delete Webserver logs.
        
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/weblog?'
        else:
            uri = 'http://' + self._address + '/rest/weblog?'
        try:
            response = requests.delete(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_dns_guided(self):
        """Interactive menu to set DNS configuration."""
        print('You may set up to three DNS servers.')
        dns1 = moves.input(('Enter the IP address of the first DNS '
                          'server or leave blank for none [none]: ').strip())
        dns2 = moves.input(('Enter the IP address of the second DNS '
                          'server or leave blank for none [none]: ').strip())
        dns3 = moves.input(('Enter the IP address of the third DNS '
                          'server or leave blank for none [none]: ').strip())
        confirm = moves.input("""Set DNS Summary:
                            DNS Server 1: %s
                            DNS Server 2: %s
                            DNS Server 3: %s
                            Confirm changes [y/n]: """ % (dns1, dns2, dns3))
        if confirm.lower() in ('y', 'yes'):
            run = self.set_dns(dns1, dns2, dns3)
            return run
        return "Canceling; no changes made.\n"

    def set_dns(self, dns1='', dns2='', dns3=''):
        """Set DNS configuration.
        
           :param dns1: A string, IP address or Domaine Name of DNS server (optional).
           :param dns2: A string, IP address or Domaine Name of DNS server (optional).
           :param dns3: A string, IP address or Domaine Name of DNS server (optional).
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/nameresolution?'
        else:
            uri = 'http://' + self._address + '/rest/device/nameresolution?'
        data = {}
        if dns1 != '':
            data['dns1'] = dns1
        if dns2 != '':
            data['dns2'] = dns2
        if dns3 != '':
            data['dns3'] = dns3
        if len(data) > 0:
            try:
                response = requests.post(uri, data=data,
                                         auth=(self.username, self.password))
                content = response.content
                info = json.loads(content)
                return json.dumps(info, indent=4)
            except ConnectionError as error:
                content = 'No Response'
                raise error
        else:
            return 'No valid DNS server addresses given; DNS entries cleared.'

    def set_id_led_guided(self):
        """Interactive menu to enable/disable ID LED."""
        led = moves.input(('type "true" to turn the ID LED on; '
                         'type "false" to turn it off [false]: ').lower())
        confirm = moves.input("""Set ID LED Summary:
                            ID LED On: %s
                            Confirm changes [y/n]: """ % led)
        if confirm.lower() in ('y', 'yes'):
            run = self.set_id_led(led)
            return run
        return "Canceling; no changes made.\n"

    def set_id_led(self, led):
        """Enable/disable ID LED on the face of the Packetmaster.
        
           :param led: A bool, True to enable, False to disable.
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/idled?'
        else:
            uri = 'http://' + self._address + '/rest/device/idled?'
        led = led.lower()
        if led == 'true' or led is True:
            led = True
        else:
            led = False
        data = {'activated': led}
        try:
            response = requests.post(uri, data=data,
                                     auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def restart_webserver(self):
        """Restart the Packetmaster Web Server. Does not reboot device.
        
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/restartwebserver?'
        else:
            uri = 'http://' + self._address + '/rest/device/restartwebserver?'
        try:
            response = requests.post(uri, auth=(self.username, self.password))
            content = response.content
            info = json.loads(content)
            return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def reboot(self):
        """Reboot the Packetmaster.
        
           :returns: A string, JSON-formatted."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/device/reboot?'
        else:
            uri = 'http://' + self._address + '/rest/device/reboot?'

        try:
            requests.post(uri, auth=(self.username, self.password))
            message = ('Device is rebooting...'
                       'please allow 2 to 3 minutes for it to complete')
            return message
        except ConnectionError as error:
            raise error
