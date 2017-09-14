import requests, json, re
from requests.exceptions import ConnectionError

class CubroEXDriverHandler(object):

    def __init__(self):
        #DriverHandlerBase.__init__(self)
        self._switch_model = "Cubroex"
        self._blade_model = "Cubroex Blade"
        self._port_model = "Cubroex Port"

    def model(self):
        #URI to retrieve Packetmaster device model
        uri = 'http://' + self.address + '/rest/device/model?'
        #GET request to retrieve the model
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['model']
        except ConnectionError as e:
            raise e

    def generation(self):
        uri = 'http://' + self.address + '/rest/device/generation?'

        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['generation']
        except ConnectionError as e:
            raise e

    def version(self):
        #URI to retrieve firmware version from Packetmaster
        uri = 'http://' + self.address + '/rest/device/imageversion?'
        #Get request to retrieve firmware version
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['version']
        except ConnectionError as e:
            raise e

    def label(self):
        uri = 'http://' + self.address + '/rest/device/customident?'

        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return (data['name'], data['notes'])
        except ConnectionError as e:
            raise e

    def port_config(self):
        uri = 'http://' + self.address + '/rest/ports/config?'

        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['port_config']
        except ConnectionError as e:
            raise e

    def port_count(self):
        #Define URI to retrieve the Packetmaster port configuration
        uri = 'http://' + self.address + '/rest/ports/config?'
        #list to store interface names of switch ports retrieved
        ports = list()
        #GET request to retrieve the port configuration
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            count = 0
            #Iterate over the port interfaces returned
            for port in data['port_config']:
                ports.append(data['port_config'][count]['if_name'])
                count += 1
            #Return the number of entries in the ports list
            interfaces = list()
            for item in ports:
                interfaces.append(re.findall('[1-9][0-9/]*', item))
            number_ports = len(interfaces)
            return (number_ports, interfaces)
        except ConnectionError as e:
            raise e

    def interface_description(self, interface):
        uri = 'http://' + self.address + '/rest/ports/config?'
        port_count = self.port_count()
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
        uri = 'http://' + self.address + '/rest/ports/sfpstatus?'
        port_count = self.port_count()
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            r = response.content
            data = json.loads(r)
            return data['result']
        except ConnectionError as e:
            raise e

    def login(self, address, username, password, command_logger=None):
        """Perform login operation on the device

        :param address: (str) address attribute from the CloudShell portal
        :param username: (str) username to login on the device
        :param password: (str) password for username
        :param command_logger: logging.Logger instance
        :return: None"""

        #Set object IP address, username, and password
        self.address = address
        self.username = username
        self.password = password

    # def get_resource_description(self, address, command_logger):
    #     """Auto-load function to retrieve all information from the device
    #
    #     :param address: (str) address attribute from the CloudShell portal
    #     :param command_logger: logging.Logger instance
    #     :return: xml.etree.ElementTree.Element instance with all switch sub-resources (blades, ports)"""
    #
    #     # Create root element
    #     depth = 0
    #     resource_info = ResourceInfo()
    #     resource_info.set_depth(depth)
    #     resource_info.set_address(address)
    #     resource_info.set_index(self.model())
    #     resource_info.add_attribute("Software Version", self.version())
    #     # Create child resources for the root element (blades):
    #     for blade_no in xrange(1):
    #         blade_resource = ResourceInfo()
    #         blade_resource.set_depth(depth + 1)
    #         blade_resource.set_index(str(blade_no))
    #         resource_info.add_child(blade_no, blade_resource)
    #     # Create child resources for each root sub-resource (ports in blades)
    #     for port_no in xrange(self.port_count()):
    #         port_resource = ResourceInfo()
    #         port_resource.set_depth(depth + 2)
    #         port_resource.set_index(str(port_no + 1))
    #         blade_resource.add_child(port_no, port_resource)
    #
    #     return resource_info.convert_to_xml()

    def map_bidi(self, src_port, dst_port, command_logger=None):
        """Create a bidirectional connection between source and destination ports

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None"""

        #Isolate source and destination port numbers from list provided by Cloudshell
        source = src_port[2]
        dest = dst_port[2]
        #Define URI to set rules via REST
        uri = 'http://' + self.address + '/rest/rules?'
        #Define rule names for the Packetmaster
        rulenameA = source + ' to ' + dest
        rulenameB = dest + ' to ' + source
        #Create the parameters for each rule to be added to the Packetmaster
        paramsA = {'name': rulenameA,
                  'priority': 32768,
                  'match[in_port]': source,
                  'actions': dest}
        paramsB = {'name': rulenameB,
                  'priority': 32768,
                  'match[in_port]': dest,
                  'actions': source}
        #Make REST post requests for each rule to be created
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
        :return: None"""

        #Isolate source and destination port numbers from list provided by Cloudshell
        source = src_port[2]
        dest = dst_port[2]
        #Define URI to set rules via REST
        uri = 'http://' + self.address + '/rest/rules?'
        #Define rule names for the Packetmaster
        rulename = source + ' to ' + dest
        #Create the parameters for the rule to be added to the Packetmaster
        params = {'name': rulename,
                  'priority': 32768,
                  'match[in_port]': source,
                  'actions': dest}
        #Make REST post request for the rule to be created
        try:
            response = requests.post(uri, data=params, auth=(self.username, self.password))
        except ConnectionError as e:
            raise e

    def map_clear_to(self, src_port, dst_port, command_logger=None):
        """Remove simplex/multi-cast/duplex connection ending on the destination port

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None"""

        #Isolate source port number from list provided by Cloudshell
        source = src_port[2]
        #Define URI to delete rules via REST
        uri = 'http://' + self.address + '/rest/rules?'
        #Create the parameters for the rule to be deleted from the Packetmaster
        params = {'priority': 32768,
                  'match[in_port]': source}
        #Make REST delete request for the rule to be deleted
        try:
             response = requests.delete(uri, params=params, auth=(self.username, self.password))
        except ConnectionError as e:
            raise e

    def map_clear(self, src_port, dst_port, command_logger=None):
        """Remove simplex/multi-cast/duplex connection ending on the destination port

        :param src_port: (list) source port in format ["<address>", "<blade>", "<port>"]
        :param dst_port: (list) destination port in format ["<address>", "<blade>", "<port>"]
        :param command_logger: logging.Logger instance
        :return: None"""

        #Isolate source and destination port numbers from list provided by Cloudshell
        source = src_port[2]
        dest = dst_port[2]
        #Define URI to delete rules via REST
        uri = 'http://' + self.address + '/rest/rules?'
        #Create the parameters for the rules to be deleted from the Packetmaster
        paramsA = {'priority': 32768,
                  'match[in_port]': source}
        paramsB = {'priority': 32768,
                  'match[in_port]': dest}
        #Make REST delete requests for the rules to be deleted
        try:
             responseA = requests.delete(uri, params=paramsA, auth=(self.username, self.password))
             responseB = requests.delete(uri, params=paramsB, auth=(self.username, self.password))
        except ConnectionError as e:
            raise e

    def set_speed_manual(self, command_logger=None):
        """Set speed manual - legacy command, do not delete, no need to change

        :param command_logger: logging.Logger instance
        :return: None
        """
        pass

if __name__ == '__main__':
    address = '192.168.1.222'
    username = 'admin'
    password = 'cubro'
    # src_port = raw_input('Enter port A: ')
    # dst_port = raw_input('Enter port B: ')

    packetmaster = CubroEXDriverHandler()
    login = packetmaster.login(address, username, password)
    ports = packetmaster.port_count()
    print "This is ports[0] %r" % (ports[0])
    print "This is ports[1] %r" % (ports[1])
    print "This is the for loop of ports[1]"
    for item in ports[1]:
        print item[0]
