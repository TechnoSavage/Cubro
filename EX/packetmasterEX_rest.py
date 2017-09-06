#Packetmaster EX device class for REST API interaction

import requests, json, re
from requests.exceptions import ConnectionError
#TO-DO Add code to handle case and verify input in all areas where needed
#Change methods including menus for user input to 'guided' methods; make necessary changes in restapicli2_2
#Finish deleting unnecessary variables and use 'self.x'
#Create methods that accept arguments to post changes 

# devicelabel = '/device/customident?' #add post
# devicehash = '/device/grouphash?' #Add post
# users = '/users?' #add
# raduser = '/users/radius?' #add
# uac = '/users/uac?' #add
# weblog = '/weblog?' #add
# deviceperm = '/device/permanentrulesmode?' #Add post
# devicestor = '/device/rulestoragemode?' #Add post
# deviceidled = '/device/idled?' #add post
# devicehttps = '/device/https?' #Add post
# appsact = '/apps/action?' #add
# groups = '/groups?' #add
# allgroup = '/groups/all?' #add
# rule = '/rules?' #change
# flows = '/flownumbers?' #change/add
class PacketmasterEX(object):

    def __init__(self, address, username=None, password=None):
        self.address = address
        self.username = username
        self.password = password

    def get_port_count(self):
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
            self.ports = len(ports)
            return len(ports)
        except ConnectionError as e:
            raise e

    #Retrieve firmware version
    def firmware_version(self):
        uri = 'http://' + self.address + '/rest/device/imageversion?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            self.firmware = data['version']
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve IP configuration
    def ip_config(self):
        uri = 'http://' + self.address + '/rest/device/ipconfig?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            self.netmask = data['current_netmask']
            self.gateway = data['current_gateway']
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve Packetmaster model
    def device_model(self):
        uri = 'http://' + self.address + '/rest/device/model?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            self.model = data['model']
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e
        self.model = data['model']

    #Retrieve Packetmaster name
    def device_name(self):
        uri = 'http://' + self.address + '/rest/device/name?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            self.name = data['name']
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve Packetmaster Name plus Notes
    def device_label(self):
        uri = 'http://' + self.address + '/rest/device/customident?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            self.name = data['name']
            self.notes = data['notes']
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve hardware generation of the device
    def hardware_generation(self):
        uri = 'http://' + self.address + '/rest/device/generation?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            self.hardware = data['generation']
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve Packetmaster serial number
    def serial_number(self):
        uri = 'http://' + self.address + '/rest/device/serialno?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            self.serial = data['serial']
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve current port configuration
    def port_config(self):
        uri = 'http://' + self.address + '/rest/ports/config?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve port information
    def port_info(self):
        uri = 'http://' + self.address + '/rest/ports/info?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve port counters
    def port_statistics(self):
        uri = 'http://' + self.address + '/rest/ports/stats?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve SFP information
    def sfp_info(self):
        uri = 'http://' + self.address + '/rest/ports/sfpstatus?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            result = data['result']
            return json.dumps(result, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve active rules
    def rules_active(self):
        uri = 'http://' + self.address + '/rest/rules/all?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #List all available apps
    def device_apps(self):
        uri = 'http://' + self.address + '/rest/apps?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve running apps
    def apps_active(self):
        uri = 'http://' + self.address + '/rest/apps/running?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve hash algorithm information
    def hash_algorithms(self):
        uri = 'http://' + self.address + '/rest/device/grouphash?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve rule permanence mode
    def rule_permanence(self):
        uri = 'http://' + self.address + '/rest/device/permanentrulesmode?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve rule storage model
    def storage_model(self):
        uri = 'http://' + self.address + '/rest/device/rulestoragemode?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve environment information
    def env_info(self):
        uri = 'http://' + self.address + '/rest/device/environment?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve deice ID LED status_code
    def id_led(self):
        uri = 'http://' + self.address + '/rest/device/idled?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve load information
    def load_info(self):
        uri = 'http://' + self.address + '/rest/device/loadaverage?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve memory usage
    def mem_free(self):
        uri = 'http://' + self.address + '/rest/device/memoryusage?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Retrieve cch machinery server revision
    def server_revision(self):
        uri = 'http://' + self.address + '/rest/device/serverrevision?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #List all save points
    def save_points(self):
        uri = 'http://' + self.address + '/rest/savepoints?'
        try:
            response = requests.get(uri, auth=(self.username, self.password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Change the management IP configuration
    def set_ip_config(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/device/ipconfig?'
        newip = raw_input('Enter IP Address (e.g. 192.168.0.200): ').strip()
        newmask = raw_input('Enter Subnet Mask (e.g. 255.255.255.0): ').strip()
        newgate = raw_input('Enter gateway (e.g. 192.168.0.1): ').strip()
        #Implement checks to validate IP input
        params = {'ip': newip, 'mask': newmask, 'gw': newgate}
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Change the device name
    def set_name(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/device/name?'
        newname = raw_input('Enter device name: ')
        params = {'devicename': newname}
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Change the configuration of a port
    def set_port_config(self):
        address = self.address
        username = self.username
        password = self.password
        #Add additional parameters, add function to change multiple ports without exiting
        #Add provision to handle devices which require reboot for speed change e.g. EX2 (10G is XG)
        #Add shutdown true/false parameter for EX2 (more?)
        uri = 'http://' + address + '/rest/ports/config?'
        interface = raw_input('Enter the interface name of the port you want to change: ').strip()
        port_no = re.find('[1-9]+.*[1-4]', interface)
        interface = 'eth-0-' + port_no
        speed = raw_input('Enter the desired interface speed; options are  "10", "100", "1000", "10G", "40G", "100G", or "auto": ').strip()
        if speed.lower() == 'auto':
            speed = 'auto'
        else:
            speed = speed.upper() #More checks needed here
        duplex = raw_input('Enter the Duplex of the interface; options are "full", "half, or "auto": ').strip()
        if duplex.lower() =='auto' or duplex.lower() == 'full' or duplex.lower() == 'half':
            duplex = duplex.lower()
        else:
            print "That is not a valid duplex; defaulting to auto"
            duplex = 'auto'
        forcetx = raw_input('Force TX?  Enter "true" for yes and "false" for no: ').strip()
        forcetx = forcetx.lower()
        check = raw_input('Perform CRC check?  Enter "true" for yes and "false" for no: ').strip()
        check = check.lower()
        recalc = raw_input('Perform CRC recalculation?  Enter "true" for yes and "false" for no: ').strip()
        recalc = recalc.lower
        params = {
            'if_name': interface,
            'speed': speed,
            'duplex': duplex,
            'unidirectional': forcetx,
            'crc_check': check,
            'crc_recalculation': recalc }
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Activate or deactivate a port
    def port_on_off(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/ports/config?'
        interface = raw_input('Enter the interface name of the port you want to change: ').strip()
        port_no = re.find('[1-9]+.*[1-4]', interface)
        interface = 'eth-0-' + port_no
        updown = raw_input('Enter "true" to shut port down; Enter "false" to reactivate port: ').strip()
        updown = updown.lower()
        params = {'if_name': interface, 'shutdown': updown}
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Reset Port Counters
    def delete_counters(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/ports/counters?'
        try:
            requests.delete(uri, auth=(username, password))
            success = 'Counters deleted successfully'
            return success
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Reset Rule Counters
    def reset_rule_counters(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/rules/counters?'
        try:
            requests.delete(uri, auth=(username, password))
            success = 'Counters deleted successfully'
            return success
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Add a rule
    def add_rule(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/rules?'
        params = {}
        rulename = raw_input('Enter a name for the rule [none]: ')
        if rulename != '':
            params['name'] = rulename
        ruledescrip = raw_input('Enter a description for the rule [none]: ')
        if ruledescrip != '':
            params['description'] = ruledescrip
        priority = raw_input('Enter the priority level of the rule; 0 - 65535 higher number = higher priority [32768]: ')
        if priority != '':
            params['priority'] = int(priority)
        else:
            params['priority'] = 32768
        portin = raw_input('Enter the port number or numbers for incoming traffic; multiple ports separated by a comma: ')
        params['match[in_port]'] = portin
        print '''\nMatch VLAN tag?
                1 - No, match all tagged and untagged traffic
                2 - No, match only untagged traffic
                3 - Yes, match a VLAN tag \n'''
        trafmatch = raw_input('Enter the number of your selection [1]: ')
        if trafmatch == '' or int(trafmatch) == 1:
            pass
        elif int(trafmatch) == 2:
            params['match[vlan]'] = 'neg_match'
        elif int(trafmatch) == 3:
            params['match[vlan]'] = 'match'
            matchid = raw_input('Enter the VLAN ID to filter on: ')
            params['match[vlan_id]'] = matchid
            vpri = raw_input('Enter the VLAN priority (Enter 0-7) [0]: ')
            if vpri == '':
                params['match[vlan_priority]'] = '0'
            else:
                vpri != ''
                try:
                    if int(vpri) >= 0 or int(vpri) <= 7:
                        params['match[vlan_priority]'] = vpri
                    else:
                        print "That is not a valid selection; VLAN priority defaulting to '0'"
                        params['match[vlan_priority]'] = '0'
                except:
                    print "That is not a valid selection; VLAN priority defaulting to '0'"
                    params['match[vlan_priority]'] = '0'
        else:
            print 'That is not a valid selection; restarting add rule\n'
            addrule(ip, uri, auth)
        macsrc = raw_input('Filter by source MAC address?  Leave blank for no or enter MAC address: ')
        if macsrc != '':
            params['dl_src'] = macsrc
        macdst = raw_input('Filter by destination MAC address?  Leave blank for no or enter MAC address: ')
        if macdst != '':
            params['dl_dst'] = macdst
        print '''\nFilter on protocol?
                1 - No Protocol Filtering
                2 - ip
                3 - tcp
                4 - udp
                5 - sctp
                6 - icmp
                7 - arp
                8 - Enter Ethertype\n'''
        proto = raw_input('Enter the number of your selection [1]: ')
        if proto == '' or int(proto) == 1:
            pass
        elif int(proto) == 2:
            params['match[protocol]'] = 'ip'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            if nwsrc != '':
                params['match[nw_src]'] = nwsrc
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
            if nwdst != '':
                params['match[nw_dst]'] = nwdst
        elif int(proto) == 3:
            params['match[protocol]'] = 'tcp'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            if nwsrc != '':
                params['match[nw_src]'] = nwsrc
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
            if nwdst != '':
                params['match[nw_dst]'] = nwdst
            tcpsrc = raw_input('Filter on source port?  Leave blank for no or enter port number: ')
            if tcpsrc != '':
                params['match[tcp_src]'] = tcpsrc
            tcpdst = raw_input('Filter on destination port?  Leave blank for no or enter port number: ')
            if tcpdst != '':
                params['match[tcp_dst]'] = tcpdst
        elif int(proto) == 4:
            params['match[protocol]'] = 'udp'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            if nwsrc != '':
                params['match[nw_src]'] = nwsrc
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
            if nwdst != '':
                params['match[nw_dst]'] = nwdst
            udpsrc = raw_input('Filter on source port?  Leave blank for no or enter port number: ')
            if udpsrc != '':
                params['match[udp_src]'] = udpsrc
            udpdst = raw_input('Filter on destination port?  Leave blank for no or enter port number: ')
            if udpdst != '':
                params['match[udp_dst]'] = udpdst
        elif int(proto) == 5:
            params['match[protocol]'] = 'sctp'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            if nwsrc != '':
                params['match[nw_src]'] = nwsrc
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
            if nwdst != '':
                params['match[nw_dst]'] = nwdst
            sctpsrc = raw_input('Filter on source port?  Leave blank for no or enter port number: ')
            if sctpsrc != '':
                params['match[sctp_src]'] = sctpsrc
            sctpdst = raw_input('Filter on destination port?  Leave blank for no or enter port number: ')
            if sctpdst != '':
                params['match[sctp_dst]'] = sctpdst
        elif int(proto) == 6:
            params['match[protocol]'] = 'icmp'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            if nwsrc != '':
                params['match[nw_src]'] = nwsrc
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
            if nwdst != '':
                params['match[nw_dst]'] = nwdst
            icmpt = raw_input('Flter on ICMP type?  Leave blank for no or enter ICMP type number: ')
            if icmpt != '':
                params['match[icmp_type]'] = icmpt
            icmpc = raw_input('Flter on ICMP code?  Leave blank for no or enter ICMP code number: ')
            if icmpc != '':
                params['match[icmp_code]'] = icmpc
        elif int(proto) == 7:
            params['match[protocol]'] = 'arp'
        elif int(proto) == 8:
            params['match[protocol]'] = 'custom'
            ether = raw_input('Enter Ethertype e.g. 0x800: ')
            if ether != '':
                params['match[dl_type]'] = ether
            nwproto = raw_input('Enter protocol number (protocol number in IPv4, header type in IPv6, opcode in ARP) or leave blank for none: ')
            if nwproto != '':
                params['match[nw_proto]'] = nwproto
        else:
            print 'That is not a valid selection; restarting add rule \n'
            addrule(ip, uri, auth)
        print '''\nAdd Custom Extra Match?
        e.g. hard_timeout, idle_timeout, tcp_flags, QinQ
        Leave blank for none
        Improper syntax will cause Add Rule to fail \n'''
        extra = raw_input('Enter Extra Custom Match String: ')
        if extra != '':
            params['match[extra]'] = extra
        ruleaction = raw_input('Enter the desired output actions separated by commas; order matters - improper syntax will cause add rule to fail: ')
        params['actions'] = ruleaction
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Make a port save point active
    def set_port_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/activeportsavepoint?'
        savename = raw_input('What is the name of the port save point to make active?: ')
        params = {'name': savename}
        try:
            response = requests.put(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Make a rule save point active
    def set_rule_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/activerulesavepoint?'
        savename = raw_input('What is the name of the rule save point to make active?: ')
        params = {'name': savename}
        try:
            response = requests.put(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Set a save point as the default boot configuration
    def set_boot_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/defaultrulesavepoint?'
        savename = raw_input('What is the name of the save point to make the default at boot configuration?: ')
        params = {'name': savename}
        try:
            response = requests.put(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Export a save point from the Packetmaster
    def export_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/export?'
        rspname = raw_input('What is the name of the rule save point to export? (leave blank for none): ')
        rspname = '[' + rspname + ']'
        pspname = raw_input('What is the name of the port save point to export? (leave blank for none): ')
        pspname = '[' + pspname + ']'
        params = {'rule_save_point_names': rspname, 'port_save_point_names': pspname} #Change to JSON encoding
        try:
            response = requests.get(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
            filename = raw_input("Enter a file name for the savepoint: ")
            try:
                with open(filename, "w") as f:
                    f.write(r) #Try json.dump(r, f)?
            except:
                print "Invalid filename\n"
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Modify a port save point
    def modify_port_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/modportsavepoint?'
        oldname = raw_input("What is the name of the save point you would like to modify?")
        newname = raw_input("What would you like to rename this save point to?")
        desc = raw_input("What is the description of the save point?")
        saveports = raw_input('Hit enter to save the current active ports to this save point; type "false" to not save them (This overwrites port configuration of the save point): ')
        params = {'oldname': oldname, 'newname': newname, 'description': desc, 'saveports': saveports}
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Modify a rule save point
    def modify_rule_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/modrulesavepoint?'
        oldname = raw_input("What is the name of the save point you would like to modify?")
        newname = raw_input("What would you like to rename this save point to?")
        desc = raw_input("What is the description of the save point?")
        saverules = raw_input('Hit enter to save the current active rules to this save point; type "false" to not save them (This overwrites rule configuration of the save point): ')
        params = {'oldname': oldname, 'newname': newname, 'description': desc, 'saverules': saverules}
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Create a port save point from current configuration
    def create_port_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/portsavepoint?'
        name = raw_input("What would you like to name the port save point?")
        desc = raw_input("Enter a description for the port save point")
        params = {'name': name, 'description': desc}
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Create a quicksave point of current configuration
    def create_quick_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/quicksaverules?'
        try:
            response = requests.put(uri, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Create a rule save point from current configuration
    def create_rule_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/rulesavepoint?'
        name = raw_input("What would you like to name the rule save point?")
        desc = raw_input("Enter a description for the rule save point")
        params = {'name': name, 'description': desc}
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Delete a port save point
    def delete_port_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/portsavepoint?'
        name = raw_input("What is the name of the port save point you would like to delete?")
        params = {'name': name}
        try:
            response = requests.delete(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Delete a rule save point
    def delete_rule_savepoint(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints/rulesavepoint?'
        name = raw_input("What is the name of the rule save point you would like to delete?")
        params = {'name': name}
        try:
            response = requests.delete(uri, data=params, auth=(username, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

    #Reboot the Packetmaster
    def reboot(self):
        address = self.address
        username = self.username
        password = self.password
        uri = 'http://' + address + '/rest/savepoints?'

        try:
            requests.post(uri, auth=(username, password))
            message = 'Device is rebooting...please allow 2 to 3 minutes for it to complete'
            return message
        except ConnectionError as e:
            r = 'No Response'
            raise e
