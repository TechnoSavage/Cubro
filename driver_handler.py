from common.configuration_parser import ConfigurationParser
from common.resource_info import ResourceInfo
import requests, json, re
from requests.exceptions import ConnectionError

class EXDriverHandler(DriverHandlerBase):

    def __init__(self):
        DriverHandlerBase.__init__(self)
        self._switch_model = 'EX'
        self._blade_model = "Ex Blade"
        self._port_model = "Ex Port"

    def model(self):
        """retrieve the model of the EX unit

        :return: unicode
        """

        uri = 'http://' + self.address + '/rest/device/model?'

        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['model']
        except ConnectionError as e:
            raise e

    def generation(self):
        """Retrieve the hardware generation of the EX unit

        :return: unicode
        """
        uri = 'http://' + self.address + '/rest/device/generation?'

        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['generation']
        except ConnectionError as e:
            raise e

    def version(self):
        """Retrieve the software version of the EX unit

        :return: unicode
        """
        uri = 'http://' + self.address + '/rest/device/imageversion?'

        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['version']
        except ConnectionError as e:
            raise e

    def label(self):
        """Retrieve the custome device label and notes of the EX unit

        :return: tuple
        """
        uri = 'http://' + self.address + '/rest/device/customident?'

        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return (data['name'], data['notes'])
        except ConnectionError as e:
            raise e

    def port_config(self):
        """Retrieve the port configuration of the EX unit

        :return: string
        """
        uri = 'http://' + self.address + '/rest/ports/config?'

        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['port_config']
        except ConnectionError as e:
            raise e

    def port_count(self):
        """Retrieve the port configuration of the EX unit

        :return: string
        """
        uri = 'http://' + self.address + '/rest/ports/config?'
        ports = list()
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            count = 0
            for port in data['port_config']:
                ports.append(data['port_config'][count]['if_name'])
                count += 1
            return str(len(ports))
        except ConnectionError as e:
            raise e

    def interface_description(self, interface):
        """Retrieve interface description of a specified interface

        :param interface: (str) interface about which to get information
        :return: string
        """
        uri = 'http://' + self.address + '/rest/ports/config?'
        port_count = self.port_count(address, self.username, self.password)
        if_name = 'eth-0-' + interface
        error = "That interface does not exist on this device"
        if int(interface) <= 0 or int(interface) > int(port_count):
            return error
        else:
            try:
                response = requests.get(uri, auth=(self.username, self.password))
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

    def sfp_status(self, interface):
        """Retrieve transceiver status of all interfaces

        :param interface: (str) interface about which to get information
        :return: unicode
        """
        uri = 'http://' + self.address + '/rest/ports/sfpstatus?'
        port_count = self.port_count()
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['result']
        except ConnectionError as e:
            raise e

    def login(self, address, username=None, password=None, command_logger=None):
        """Perform login operation on the device

        :param address: (str) address attribute from the CloudShell portal
        :param username: (str) username to login on the device
        :param password: (str) password for username
        :param command_logger: logging.Logger instance
        :return: None
        """
        self.address = address
        self.username = username
        self.password = password

    def get_resource_description(self, address, command_logger=None):
        """Auto-load function to retrieve all information from the device

        :param address: (str) address attribute from the CloudShell portal
        :param username: (str) username to login on the device
        :param password: (str) password for username (required)
        :param command_logger: logging.Logger instance
        :return: xml.etree.ElementTree.Element instance with all switch sub-resources (blades, ports)

        """
        # Create root element
        port_count = self.port_count()
        depth = 0
        resource_info = ResourceInfo()
        resource_info.set_depth(depth)
        resource_info.set_address(address)
        resource_info.set_index(self.model())
        resource_info.add_attribute("Software Version", self.version())
        # Create child resources for the root element (blades):
        for blade_no in xrange(1):
            blade_resource = ResourceInfo()
            blade_resource.set_depth(depth + 1)
            blade_resource.set_index(str(blade_no))
            resource_info.add_child(blade_no, blade_resource)
        # Create child resources for each root sub-resource (ports in blades)
        for port_no in xrange(port_count):
            port_resource = ResourceInfo()
            port_resource.set_depth(depth + 2)
            port_resource.set_index(str(port_no))
            blade_resource.add_child(port_no, port_resource)

        return resource_info.convert_to_xml()

    def map_bidi(self, src_port, dst_port):
        """Create a bidirectional connection between source and destination ports

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        # Locate any existing rules that use the source port as a destination port or vice versa in order to delete them

        uri_existing = 'http://' + self.address + '/rest/rules/all?'

        src_dst = []

        activerules = requests.get(uri_existing, auth=(self.username, self.password))
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
                delete_preexisting = requests.delete(uri_existing, params=params_delete, auth=(self.username, self.password))
            except ConnectionError as e:
                raise e

        uri = 'http://' + self.address + '/rest/rules?'
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
            responseA = requests.post(uri, data=paramsA, auth=(self.username, self.password))
            responseB = requests.post(uri, data=paramsB, auth=(self.username, self.password))
        except ConnectionError as e:
            raise e

    def map_uni(self, src_port, dst_port, command_logger=None):
        """Create a unidirectional connection between source and destination ports

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        uri_existing = 'http://' + self.address + '/rest/rules/all?'

        src_dst = []

        activerules = requests.get(uri_existing, auth=(self.username, self.password))
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
                delete_preexisting = requests.delete(uri_existing, params=params_delete, auth=(self.username, self.password))
            except ConnectionError as e:
                raise e

        uri = 'http://' + self.address + '/rest/rules?'
        rulename = src_port + ' to ' + dst_port
        params = {'name': rulename,
                  'priority': 32768,
                  'match[in_port]': src_port,
                  'actions': dst_port}
        try:
            response = requests.post(uri, data=params, auth=(self.username, self.password))
        except ConnectionError as e:
            raise e

    def map_clear_to(self, src_port, dst_port, command_logger=None):
        """Remove simplex/multi-cast/duplex connection ending on the destination port

        :param src_port: (str) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        uri = 'http://' + self.address + '/rest/rules?'
        params = {'priority': 32768,
                  'match[in_port]': src_port}
        try:
             response = requests.delete(uri, params=params, auth=(self.username, self.password))
        except ConnectionError as e:
            raise e

    def map_clear(self, src_port, dst_port, command_logger=None):
        """Remove simplex/multi-cast/duplex connection ending on the destination port

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None
        """
        uri = 'http://' + self.address + '/rest/rules?'
        paramsA = {'priority': 32768,
                  'match[in_port]': src_port}
        paramsB = {'priority': 32768,
                  'match[in_port]': dst_port}
        try:
             responseA = requests.delete(uri, params=paramsA, auth=(self.username, self.password))
             responseB = requests.delete(uri, params=paramsB, auth=(self.username, self.password))
        except ConnectionError as e:
            raise e

    def set_speed_manual(self, command_logger):
        """Set speed manual - legacy command, do not delete, no need to change

        :param command_logger: logging.Logger instance
        :return: None
        """
        pass
