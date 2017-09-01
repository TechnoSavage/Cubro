from common.configuration_parser import ConfigurationParser
from common.resource_info import ResourceInfo
import requests, json, re
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError

class EXDriverHandler(object):

    def __init__(self):
        #DriverHandlerBase.__init__(self)
        self._switch_model = 'EX'
        self._blade_model = "Ex Blade"
        self._port_model = "Ex Port"

    def model(self, address, username=None, password=None):
        """retrieve the model of the EX unit

        :param address: (str) address attribute from the CloudShell portal
        :param username: (str) username to login on the device (required if authentication is enabled in the Web UI)
        :param password: (str) password for username (required if authentication is enabled in the Web UI)
        :return: string
        """

        uri = 'http://' + address + '/rest/device/model?'

        try:
            response = requests.get(uri, auth=(username, password))
            r = response.content
            data = json.loads(r)
            return data['model']
        except ConnectionError as e:
            raise e

    def generation(self, address, username=None, password=None):
        """Retrieve the hardware generation of the EX unit

        :param address: (str) address attribute from the CloudShell portal
        :param username: (str) username to login on the device (required if authentication is enabled in the Web UI)
        :param password: (str) password for username (required if authentication is enabled in the Web UI)
        :return: string
        """
        uri = 'http://' + address + '/rest/device/generation?'

        try:
            response = requests.get(uri, auth=(username, password))
            r = response.content
            data = json.loads(r)
            return data['generation']
        except ConnectionError as e:
            raise e

    def version(self, address, username=None, password=None):
        """Retrieve the software version of the EX unit

        :param address: (str) address attribute from the CloudShell portal
        :param username: (str) username to login on the device (required if authentication is enabled in the Web UI)
        :param password: (str) password for username (required if authentication is enabled in the Web UI)
        :return: string
        """
        uri = 'http://' + address + '/rest/device/imageversion?'

        try:
            response = requests.get(uri, auth=(username, password))
            r = response.content
            data = json.loads(r)
            return data['version']
        except ConnectionError as e:
            raise e

    def label(self, address, username=None, password=None):
        """Retrieve the custome device label and notes of the EX unit

        :param address: (str) address attribute from the CloudShell portal
        :param username: (str) username to login on the device (required if authentication is enabled in the Web UI)
        :param password: (str) password for username (required if authentication is enabled in the Web UI)
        :return: string
        """
        uri = 'http://' + address + '/rest/device/customident?'

        try:
            response = requests.get(uri, auth=(username, password))
            r = response.content
            data = json.loads(r)
            return (data['name'], data['notes'])
        except ConnectionError as e:
            raise e

    def port_count(self, address, username=None, password=None):
        """Retrieve the port configuration of the EX unit

        :param address: (str) address attribute from the CloudShell portal
        :param username: (str) username to login on the device (required if authentication is enabled in the Web UI)
        :param password: (str) password for username (required if authentication is enabled in the Web UI)
        :return: int
        """
        uri = 'http://' + address + '/rest/ports/config?'
        ports = list()
        try:
            response = requests.get(uri, auth=(username, password))
            r = response.content
            data = json.loads(r)
            count = 0
            for port in data['port_config']:
                ports.append(data['port_config'][count]['if_name'])
                count += 1
            return len(ports)
        except ConnectionError as e:
            raise e

    def interface_description(self, address, interface, username=None, password=None):
        """Retrieve interface description of a specified interface

        :param address: (str) address attribute from the CloudShell portal
        :param interface: (str) interface about which to get information
        :param username: (str) username to login on the device (required if authentication is enabled in the Web UI)
        :param password: (str) password for username (required if authentication is enabled in the Web UI)
        :return: JSON
        """
        uri = 'http://' + address + '/rest/ports/config?'
        port_count = self.port_count(address, username, password)
        if_name = 'eth-0-' + interface
        if int(interface) <= 0 or int(interface) > port_count:
            return "That interface does not exist on this device"
        else:
            try:
                response = requests.get(uri, auth=(username, password))
                r = response.content
                data = json.loads(r)
                count = 0
                for port in data['port_config']:
                    if data['port_config'][count]['if_name'] == if_name:
                        status = data['port_config'][count]
                        return json.dumps(status, indent=4)
                    else:
                        count += 1
            except ConnectionError as e:
                return e

    def sfp_status(self, address, username=None, password=None):
        """Retrieve transceiver status of all interfaces

        :param address: (str) address attribute from the CloudShell portal
        :param interface: (str) interface about which to get information
        :param username: (str) username to login on the device (required if authentication is enabled in the Web UI)
        :param password: (str) password for username (required if authentication is enabled in the Web UI)
        :return: JSON
        """
        uri = 'http://' + address + '/rest/ports/sfpstatus?'
        port_count = self.port_count(address, username, password)
        try:
            response = requests.get(uri, auth=(username, password))
            r = response.content
            data = json.loads(r)
            return data['result']
        except ConnectionError as e:
            raise e

    # example: get variable from the configuration/runtime_configuration files:
    # self.example_driver_setting = ConfigurationParser.get("driver_variable", "example_driver_setting")
    def get_resource_description(self, address, username=None, password=None, command_logger=None):
        """Auto-load function to retrieve all information from the device

        :param address: (str) address attribute from the CloudShell portal
        :param username: (str) username to login on the device
        :param password: (str) password for username (required)
        :param command_logger: logging.Logger instance
        :return: xml.etree.ElementTree.Element instance with all switch sub-resources (blades, ports)

        Example usage:
        # Step 1. Create root element (switch):
        depth = 0
        resource_info = ResourceInfo()
        resource_info.set_depth(depth)
        resource_info.set_address(address)
        resource_info.set_index("Switch model name")
        resource_info.add_attribute("Software Version", "1.0.0")

        # Step 2. Create child resources for the root element (blades):
        for blade_no in xrange(2):
            blade_resource = ResourceInfo()
            blade_resource.set_depth(depth + 1)
            blade_resource.set_index(str(blade_no))
            resource_info.add_child(blade_no, blade_resource)

            # Step 3. Create child resources for each root sub-resource (ports in blades)
            for port_no in xrange(5):
                port_resource = ResourceInfo()
                port_resource.set_depth(depth + 2)
                port_resource.set_index(str(port_no))
                blade_resource.add_child(port_no, port_resource)

        return resource_info.convert_to_xml()
        """
        #create root element
        depth = 0
        resource_info = ResourceInfo()
        resource_info.set_depth(depth)
        resource_info.set_address(address)
        resource_info.set_index(self.model(address, username, password))
        resource_info.add_attribute("Software Version", self.version(address, username, password))

    def map_bidi(self, address, src_port, dst_port, username=None, password=None):
        """Create a bidirectional connection between source and destination ports

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        # Locate any existing rules that use the source port as a destination port or vice versa in order to delete them

        uri_existing = 'http://' + address + '/rest/rules/all?'

        src_dst = []

        activerules = requests.get(uri_existing, auth=(username, password))
        existing = activerules.content
        load_existing = json.loads(existing)
        for item in load_existing['rules']:
            name = item['name']
            dest = re.findall('to ([0-9]+)', name)
            if dest[0] == src_port or dest[0] == dst_port:
                src_dst.append(item['name'][0])

        for port in src_dst:
            params_delete = {'priority': 32768,
                             'match[in_port]': port}
            try:
                delete_preexisting = requests.delete(uri_existing, params=params_delete, auth=(username, password))
            except ConnectionError as e:
                raise e

        uri = 'http://' + address + '/rest/rules?'
        rulenameA = src_port + ' to ' + dst_port
        rulenameB = dst_port + ' to ' + src_port


        #Add the cross-connect rules with source and destination ports
        paramsA = {'name': rulenameA,
                  'priority': 32768,
                  'match[in_port]': src_port,
                  'actions': dst_port}
        paramsB = {'name': rulenameB,
                  'priority': 32768,
                  'match[in_port]': dst_port,
                  'actions': src_port}
        try:
            responseA = requests.post(uri, data=paramsA, auth=(username, password))
            responseB = requests.post(uri, data=paramsB, auth=(username, password))
        except ConnectionError as e:
            raise e

    def map_uni(self, address, src_port, dst_port, username=None, password=None):
        """Create a unidirectional connection between source and destination ports

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        uri_existing = 'http://' + address + '/rest/rules/all?'

        src_dst = []

        activerules = requests.get(uri_existing, auth=(username, password))
        existing = activerules.content
        load_existing = json.loads(existing)
        for item in load_existing['rules']:
            name = item['name']
            dest = re.findall('to ([0-9]+)', name)
            if dest[0] == src_port or dest[0] == dst_port:
                src_dst.append(item['name'][0])

        for port in src_dst:
            params_delete = {'priority': 32768,
                             'match[in_port]': port}
            try:
                delete_preexisting = requests.delete(uri_existing, params=params_delete, auth=(username, password))
            except ConnectionError as e:
                raise e

        uri = 'http://' + address + '/rest/rules?'
        rulename = src_port + ' to ' + dst_port
        params = {'name': rulename,
                  'priority': 32768,
                  'match[in_port]': src_port,
                  'actions': dst_port}
        try:
            response = requests.post(uri, data=params, auth=(username, password))
        except ConnectionError as e:
            raise e

    def map_clear_to(self, src_port, dst_port, command_logger=None):
        """Remove simplex/multi-cast/duplex connection ending on the destination port

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        uri = 'http://' + address + '/rest/rules?'
        paramsA = {'priority': 32768,
                  'match[in_port]': src_port}
        paramsB = {'priority': 32768,
                  'match[in_port]': dst_port}
        try:
             responseA = requests.delete(uri, params=paramsA, auth=(username, password))
             responseB = requests.delete(uri, params=paramsB, auth=(username, password))
        except ConnectionError as e:
            raise e

if __name__ == '__main__':
    address = '10.90.100.244'
    username = 'admin'
    password = 'cubro'
    src_port = raw_input('Enter port A: ')
    dst_port = raw_input('Enter port B: ')

    EX2 = EXDriverHandler()

    #model = EX2.model(address, username, password)
    #print type(model)
    #software = EX2.version(address, username, password)
    #print type(software)
    #hardware = EX2.generation(address, username, password)
    #print type(hardware)
    #name = EX2.label(address, username, password)
    #print type(name)
    #portcount = EX2.port_count(address, username, password)
    #print type(portcount)
    #config = EX2.interface_description(address, src_port)
    #print type(config)
    bidi = EX2.map_bidi(address, src_port, dst_port,username, password)
    print bidi
    # uni = EX2.map_uni(address, src_port, dst_port,username, password)
    # print uni
    #interfaces = EX2.interface_description(address, src_port)
    #print type(interfaces)
    #port_count = EX2.port_count(address, username, password)
    #print port_count
    #for port_no in xrange(port_count):
        #print port_no
