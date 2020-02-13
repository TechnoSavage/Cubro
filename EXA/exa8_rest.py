""" EXA8 device class for REST API interaction,
    Use with firmware version x.x.x or newer of Cubro TAP/AGG/Capture firmware."""

from __future__ import print_function #Requires Python 2.6 or later
import json
import requests
from requests.exceptions import ConnectionError
from six import moves
import exa8_input_check

class SessionmasterEXA8(object):
    """Object class representing a Cubro Sessionmaster EXA8.

    :param address: A string, Management IP of EXA8.
    :param username: A string, Username of an account on the EXA8.
    :param password: A string, Password for user account.
    """

    def __init__(self, address, username=None, password=None):
        #add certificate validation
        self._address = address
        self.username = username
        self.password = password
        self.session = requests.session()
        self.__https = True
        conn_test = self.conn_test()
        print(conn_test)

    def conn_test(self):
        """Test if device is reachable and assign properties.
        Assigns additional properties.
        """
        try:
            connect = self.login_request()
            if connect == 'Unauthorized':
                return "Invalid Credentials"
            else:
                return "Connection Established"
        except ConnectionError as fail:
            print(fail, 'Attempting connection via HTTP.')
            try:
                self.__https = False
                connect = self.login_request()
                if connect == 'Unauthorized':
                    return "Invalid Credentials"
                else:
                    return "Connection Established"
            except ConnectionError as fail:
                print(fail, 'Device is unreachable.')

    def login_request(self):
        """ Send authenticated login request to retrieve session cookie."""
        if self.__https:
            uri = 'https://' + self._address + '/loginreq?'
        else:
            uri = 'http://' + self._address + '/loginreq?'
        params = {"username": self.username, "password": self.password}
        try:
            response = self.session.post(uri, data=params, verify=False)
            if response == 'Unauthorized':
                return response
            else:
                content = response.content
                info = json.loads(content)
                self.user_id = info['id']
                self.user_role = info['role']
                self.session_cookie = response.cookies
                return json.dumps(info, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_imageversion(self):
        """Retrieve firmware image version.

           :returns: A string"""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/imageversion?'
        else:
            uri = 'http://' + self._address + '/api/device/imageversion?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_ip(self):
        """Retrieve management IP address.
        
           :returns: A string"""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/management_ip?'
        else:
            uri = 'http://' + self._address + '/api/device/management_ip?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_ip(self, ip, netmask, gateway):
        """Set the management IP address, netmask, and gateway.

           :param ip: A string, management IP address in decimal notation.
           :param netmask: A string, subnet mask in decimal notation.
           :param gateway: A string, gateway address in decimal notation.
           :returns: A string, "status": 1 success"""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/management_ip?'
        else:
            uri = 'http://' + self._address + '/api/device/management_ip?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        if exa8_input_check.ipv4(ip) != 0:
            ip = exa8_input_check.ipv4(ip)
        else:
            return "ip argument is not a valid IP address; no changes made. \n"
        if exa8_input_check.ipv4_mask(netmask) != 0:
            netmask = exa8_input_check.ipv4_mask(netmask)
        else:
            return "netmask argument is not a valid subnet mask; no changes made. \n"
        if exa8_input_check.ipv4(gateway) != 0:
            gateway = exa8_input_check.ipv4(gateway)
        else:
            return "gateway argument is not a valid IP address; no changes made. \n"
        params = {'ip': ip,
                  'netmask': netmask,
                  'gateway': gateway}
        try:
            response = self.session.post(uri, params=params, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_sysinfo(self):
        """Retrieve system information.
        
           :returns: A string"""
        if self.__https:
            uri = 'https://' + self._address + '/rest/systeminfo?'
        else:
            uri = 'http://' + self._address + '/rest/systeminfo?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_memusage(self):
        """Retrieve memory usage information.
        
           :returns: A string"""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/memoryusage?'
        else:
            uri = 'http://' + self._address + '/api/device/memoryusage?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_model(self):
        """Retrieve device model.
        
           :returns: A string"""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/model?'
        else:
            uri = 'http://' + self._address + '/api/device/model?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_name(self):
        """Retrieve device name.
        
           :returns: A string"""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/name?'
        else:
            uri = 'http://' + self._address + '/api/device/name?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_name(self, name):
        """Set a new name for the device.

           :param name: A string, new name of the device.
           :returns: A string, "status": 1 success"""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/name?'
        else:
            uri = 'http://' + self._address + '/api/device/name?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        params = {'device_name': name}
        try:
            response = self.session.post(uri, params=params, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error
    
    def get_serial(self):
        """Retrieve device serial number.
        
           :returns: A string """
        if self.__https:
            uri = 'https://' + self._address + '/api/device/serialno?'
        else:
            uri = 'http://' + self._address + '/api/device/serialno?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error
    
    def get_serverrevision(self):
        """Retrieve cch server revision number.
        
           :returns: A string"""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/serverrevision?'
        else:
            uri = 'http://' + self._address + '/api/device/serverrevision?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error
    
    def get_interfacenames(self):
        """Retrieve interface names.
        
           :returns: A string """
        if self.__https:
            uri = 'https://' + self._address + '/api/monitor/interfaceNames?'
        else:
            uri = 'http://' + self._address + '/api/monitor/interfaceNames?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_portconfig(self): #Not providing proper values
        """Retrieve port configurations.
        
           :returns: A string """
        if self.__https:
            uri = 'https://' + self._address + '/api/ports/config?'
        else:
            uri = 'http://' + self._address + '/api/ports/config?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_portconfig(self, interface, speed, status):
        """Set port configuration for the device.

           :param interface: A string, name of interface to be configured.
           :param speed: A string, '10m-half', '10m-full', '100m-half', '100m-full', '1g', '10g' or 'auto'.
           :param status: A string, administrative status for interface; 'Up' or 'Down'.
           :returns: A string, "result": "ok" equals success"""
        if self.__https:
            uri = 'https://' + self._address + '/api/ports/config?'
        else:
            uri = 'http://' + self._address + '/api/ports/config?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        if not exa8_input_check.interface(interface):
            return "Source interface argument is not a valid interface; no changes made. \n"
        if not exa8_input_check.interface_speed(speed):
            return "Speed argument is not a valid speed option; no changes made. \n"
        if status.lower() not in ('up', 'down'):
            return "Status argument is not a valid option; no changes made."
        params = {'if_name': interface.title(),
                  'admin_speed': speed.lower(),
                  'admin_status': status.title()}
        try:
            response = self.session.post(uri, params=params, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_portinfo(self):
        """Retrieve port information e.g. status, speed, MAC."""
        if self.__https:
            uri = 'https://' + self._address + '/api/ports/info?'
        else:
            uri = 'http://' + self._address + '/api/ports/info?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_portstats(self):
        """Retrieve port statistics."""
        if self.__https:
            uri = 'https://' + self._address + '/api/ports/stats?'
        else:
            uri = 'http://' + self._address + '/api/ports/stats?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_sfpstatus(self):
        """Retrieve status information regarding SFPs."""
        if self.__https:
            uri = 'https://' + self._address + '/api/ports/sfpstatus?'
        else:
            uri = 'http://' + self._address + '/api/ports/sfpstatus?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error
    
    def get_moncount(self):
        """Retrieve number of active monitor (tapping) sessions."""
        if self.__https:
            uri = 'https://' + self._address + '/api/monitor/monitorSessionCount?'
        else:
            uri = 'http://' + self._address + '/api/monitor/monitorSessionCount?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_monsessions(self):
        """Retrieve active monitor (tapping) sessions."""
        if self.__https:
            uri = 'https://' + self._address + '/api/monitor/activeSession?'
        else:
            uri = 'http://' + self._address + '/api/monitor/activeSession?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_inputagg(self):
        """Retrieve aggregation VLAN information for G1-G8 interfaces."""
        if self.__https:
            uri = 'https://' + self._address + '/api/aggregation/showlan?'
        else:
            uri = 'http://' + self._address + '/api/aggregation/showlan?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_outputagg(self):
        """Retrieve aggregation VLAN information for X1, X2, Xv interfaces."""
        if self.__https:
            uri = 'https://' + self._address + '/api/aggregation/showvlan?'
        else:
            uri = 'http://' + self._address + '/api/aggregation/showvlan?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_pcaps(self):
        """Retrieve a list of pcap files currently on the device."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/pcap-running?'
        else:
            uri = 'http://' + self._address + '/rest/pcap-running?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_monsession(self, session, src, dst):
        """Create a monitor (tapping) session.
           :param session: A string, values 1-12 to specify monitor session.
           :param src: A string, values G1-G8 to indicate source copper port.
           :param dst: A string, values G1-G8 to indicate destination copper port."""
        if self.__https:
            uri = 'https://' + self._address + '/api/monitor/createMonitorSession?'
        else:
            uri = 'http://' + self._address + '/api/monitor/createMonitorSession?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        if not exa8_input_check.mon_session(session):
            return "Monitor session value is invalid; no changes made."
        if not exa8_input_check.interface(src):
            return "Source interface argument is not a valid interface; no changes made. \n"
        if not exa8_input_check.interface(dst):
            return "Destination interface argument is not a valid interface; no changes made. \n"
        params = {'monitorSessionName': session,
                  'sourceInterfaces': src,
                  'destinationInterfaces': dst}
        try:
            response = self.session.post(uri, params=params, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def del_monsession(self, session):
        """Clear a specified monitor (tapping) session.
           :param session: A string, values 1-12 to specify monitor session."""
        if self.__https:
            uri = 'https://' + self._address + '/api/monitor/clearMonitorSession?'
        else:
            uri = 'http://' + self._address + '/api/monitor/clearMonitorSession?'
        if not exa8_input_check.mon_session(session):
            return "Monitor session value is invalid; no changes made."
        headers = {"X-Requested-With": "XMLHttpRequest"}
        params = {'monitorSessionName': session}
        try:
            response = self.session.post(uri, params=params, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_inputvlan(self, interface, vlan):
        """Assign an aggregation VLAN tag to a copper input interface.
           :param interface: A string, output interface (G1-G8).
           :param vlan: A string, VLAN ID to add to interface."""
        if self.__https:
            uri = 'https://' + self._address + '/api/aggregation/createlanaggregation?'
        else:
            uri = 'http://' + self._address + '/api/aggregation/createlanaggregation?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        #add input validation for intf and vlan
        if not exa8_input_check.interface(interface):
            return "Source interface argument is not a valid interface; no changes made. \n"
        if not exa8_input_check.vlan(vlan):
            return "vlan argument is not a valid vlan ID; no changes made. \n"
        params = {'intf': interface,
                  'vlan': vlan}
        try:
            response = self.session.post(uri, params=params, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_outputvlan_agg(self, interface, vlan):
        """Assign an aggregation VLAN tag to an SFP+ aggregation interface.
           :param interface: A string, output interface (X1, X2, Xv).
           :param vlan: A string, VLAN ID to add to interface."""
        if self.__https:
            uri = 'https://' + self._address + '/api/aggregation/createlanmonitoraggregation?'
        else:
            uri = 'http://' + self._address + '/api/aggregation/createlanmonitoraggregation?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        if not exa8_input_check.interface(interface):
            return "Source interface argument is not a valid interface; no changes made. \n"
        if not exa8_input_check.vlan(vlan):
            return "vlan argument is not a valid vlan ID; no changes made. \n"
        params = {'intf': interface,
                  'vlan': vlan}
        try:
            response = self.session.post(uri, params=params, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error
        
    def del_outputvlan_agg(self, interface, vlan):
        """Delete an aggregation VLAN tag from output interface.
           :param interface: A string, output interface (X1, X2, or Xv).
           :param vlan: A string, VLAN ID to delete from interface."""
        if self.__https:
            uri = 'https://' + self._address + '/api/aggregation/dellanmonitoraggregation?'
        else:
            uri = 'http://' + self._address + '/api/aggregation/dellanmonitoraggregation?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        if not exa8_input_check.interface(interface):
            return "Source interface argument is not a valid interface; no changes made. \n"
        if not exa8_input_check.vlan(vlan):
            return "vlan argument is not a valid vlan ID; no changes made. \n"
        params = {'intf': interface,
                  'vlan': vlan}
        try:
            response = self.session.post(uri, params=params, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_tagforwarding(self):
        """Retrieve status of VLAN tag forwarding from the output interfaces."""
        if self.__https:
            uri = 'https://' + self._address + '/api/ports/getStripForwardingTag?'
        else:
            uri = 'http://' + self._address + '/api/ports/getStripForwardingTag?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def set_tagforwarding(self, mode):
        """Enable or disable VLAN tag forwarding from the output interfacesw.
           :param mode: A string, "true" to enable; "false" to disable."""
        if self.__https:
            uri = 'https://' + self._address + '/api/ports/setStripForwardingTag?'
        else:
            uri = 'http://' + self._address + '/api/ports/setStripForwardingTag?'
        if mode.lower() not in ("true", "false"):
            return "That is not a valid input for mode; no changes will be made."
        headers = {"X-Requested-With": "XMLHttpRequest"}
        params = {'mode': mode.lower()}
        try:
            response = self.session.post(uri, params=params, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error
           
    def del_stats(self):
        """Clear all statistics."""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/clearStatisticsAll?'
        else:
            uri = 'http://' + self._address + '/api/device/clearStatisticsAll?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.post(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def start_capture(self, filename, filter_rule):
        """Initiate a packet capture on Xv interface.
           :param filename: A string, filename for the save capture.
           :param filter_rule: A string, capture filter in tcpdump syntax."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/pcap-running?'
        else:
            uri = 'http://' + self._address + '/rest/pcap-running?'
        headers = {"X-Requested-With": "XMLHttpRequest",
                   "Content-Type": "application/json"}
        json_form = {'action': 'start',
                     'name': filename,
                     'filter': filter_rule}
        try:
            response = self.session.post(uri, headers=headers, json=json_form)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def stop_capture(self):
        """Stop packet capture on Xv interface."""
        if self.__https:
            uri = 'https://' + self._address + '/rest/pcap-running?'
        else:
            uri = 'http://' + self._address + '/rest/pcap-running?'
        headers = {"X-Requested-With": "XMLHttpRequest",
                   "Content-Type": "application/json"}
        json_form = {'action': 'stop'}
        try:
            response = self.session.post(uri, headers=headers, json=json_form)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def reset(self):
        """Reset the device configuration to defaults."""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/resetconfig?'
        else:
            uri = 'http://' + self._address + '/api/device/resetconfig?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.post(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def save_config(self):
        """Save the device configuration."""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/saveconfig?'
        else:
            uri = 'http://' + self._address + '/api/device/saveconfig?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.post(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def restore_config(self):
        """Restore the device configuration."""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/restorconfig?'
        else:
            uri = 'http://' + self._address + '/api/device/restorconfig?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.post(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def reboot(self):
        """Reboot the device."""
        if self.__https:
            uri = 'https://' + self._address + '/api/device/reboot?'
        else:
            uri = 'http://' + self._address + '/api/device/reboot?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.post(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error



