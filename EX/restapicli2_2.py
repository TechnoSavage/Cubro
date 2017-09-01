#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Import necessary Python libraries for interacting with the REST API
#!/usr/bin/python
import requests, json
from getpass import getpass
from requests.exceptions import ConnectionError

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

#Retrieve firmware version
def getversion(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/imageversion?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve IP configuration
def getip(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/ipconfig?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve Packetmaster model
def getmodel(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/model?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve Packetmaster name
def getname(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/name?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve Packetmaster Name plus Notes
def getlabel(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/customident?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve hardware generation of the device
def getgen(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/generation?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve Packetmaster serial number
def getserial(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/serialno?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve current port configuration
def getportconfig(address, username=None, password=None):
    uri = 'http://' + address + '/rest/ports/config?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve port information
def getportinfo(address, username=None, password=None):
    uri = 'http://' + address + '/rest/ports/info?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve port counters
def getportstat(address, username=None, password=None):
    uri = 'http://' + address + '/rest/ports/stats?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve SFP information
def getsfp(address, username=None, password=None):
    uri = 'http://' + address + '/rest/ports/sfpstatus?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve active rules
def getrulesrun(address, username=None, password=None):
    uri = 'http://' + address + '/rest/rules/all?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#List all available apps
def getapps(address, username=None, password=None):
    uri = 'http://' + address + '/rest/apps?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve running apps
def getappsrun(address, username=None, password=None):
    uri = 'http://' + address + '/rest/apps/running?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve hash algorithm information
def gethash(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/grouphash?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve rule permanence mode
def getperm(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/permanentrulesmode?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve rule storage model
def getstor(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/rulestoragemode?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve environment information
def getenv(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/environment?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve deice ID LED status_code
def getidled(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/idled?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve load information
def getload(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/loadaverage?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve memory usage
def getmem(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/memoryusage?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Retrieve cch machinery server revision
def getserver(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/serverrevision?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#List all save points
def getsaves(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints?'
    try:
        response = requests.get(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Change the management IP configuration
def changeip(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/ipconfig?'
    newip = raw_input('Enter IP Address (e.g. 192.168.0.200): ')
    newmask = raw_input('Enter Subnet Mask (e.g. 255.255.255.0): ')
    newgate = raw_input('Enter gateway (e.g. 192.168.0.1): ')
    #Implement checks to validate IP input
    params = {'ip': newip, 'mask': newmask, 'gw': newgate}
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Change the device name
def changename(address, username=None, password=None):
    uri = 'http://' + address + '/rest/device/name?'
    newname = raw_input('Enter device name: ')
    params = {'devicename': newname}
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Change the configuration of a port
def changeportconfig(address, username=None, password=None): #Add additional parameters, add function to change multiple ports without exiting
    uri = 'http://' + address + '/rest/ports/config?'
    interface = raw_input('Enter the interface name of the port you want to change: ')
    speed = raw_input('Enter the desired interface speed; options are  "10", "100", "1000", "10G", "40G", "100G", or "auto": ')
    duplex = raw_input('Enter the Duplex of the interface; options are "full", "half, or "auto": ')
    forcetx = raw_input('Force TX?  Enter "true" for yes and "false" for no: ')
    check = raw_input('Perform CRC check?  Enter "true" for yes and "false" for no: ')
    recalc = raw_input('Perform CRC recalculation?  Enter "true" for yes and "false" for no: ')
    params = {
        'if_name': interface,
        'speed': speed,
        'duplex': duplex,
        'unidirectional': forcetx,
        'crc_check': check,
        'crc_recalculation': recalc }
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Activate or deactivate a port
def portonoff(address, username=None, password=None):
    uri = 'http://' + address + '/rest/ports/config?'
    interface = raw_input('Enter the interface name of the port you want to change: ')
    updown = raw_input('Enter "true" to shut port down; Enter "false" to reactivate port: ')
    params = {'if_name': interface, 'shutdown': updown}
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Reset Port Counters
def deletecounters(address, username=None, password=None):
    uri = 'http://' + address + '/rest/ports/counters?'
    try:
        requests.delete(uri, auth=(username, password))
        print 'Counters deleted successfully'
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Reset Rule Counters
def resetrulecounter(address, username=None, password=None):
    uri = 'http://' + address + '/rest/rules/counters?'
    try:
        requests.delete(uri, auth=(username, password))
        print 'Counters deleted successfully'
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Add a rule
def addrule(address, username=None, password=None):
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
        if vpri != '' and int(vpri) >= 0 or int(vpri) <= 7:
            params['match[vlan_priority]'] = vpri
        elif vpri != '' and int(vpri) <0 or int(vpri) >7:
            print "That is not a valid selection; VLAN priority defaulting to '0'"
            params['match[vlan_priority]'] = '0'
        else:
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
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Make a port save point active
def actspport(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/activeportsavepoint?'
    savename = raw_input('What is the name of the port save point to make active?: ')
    params = {'name': savename}
    try:
        response = requests.put(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Make a rule save point active
def actsprule(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/activerulesavepoint?'
    savename = raw_input('What is the name of the rule save point to make active?: ')
    params = {'name': savename}
    try:
        response = requests.put(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Set a save point as the default boot configuration
def setbootsp(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/defaultrulesavepoint?'
    savename = raw_input('What is the name of the save point to make the default at boot configuration?: ')
    params = {'name': savename}
    try:
        response = requests.put(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Export a save point from the Packetmaster
def exportsp(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/export?'
    rspname = raw_input('What is the name of the rule save point to export? (leave blank for none): ')
    rspname = '[' + rspname + ']'
    pspname = raw_input('What is the name of the port save point to export? (leave blank for none): ')
    pspname = '[' + pspname + ']'
    params = {'rule_save_point_names': rspname, 'port_save_point_names': pspname} #Change to JSON encoding
    try:
        response = requests.get(uri, data=params, auth=(username, password))
        print response.status_code
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
def modportsp(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/modportsavepoint?'
    oldname = raw_input("What is the name of the save point you would like to modify?")
    newname = raw_input("What would you like to rename this save point to?")
    desc = raw_input("What is the description of the save point?")
    saveports = raw_input('Hit enter to save the current active ports to this save point; type "false" to not save them (This overwrites port configuration of the save point): ')
    params = {'oldname': oldname, 'newname': newname, 'description': desc, 'saveports': saveports}
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Modify a rule save point
def modrulesp(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/modrulesavepoint?'
    oldname = raw_input("What is the name of the save point you would like to modify?")
    newname = raw_input("What would you like to rename this save point to?")
    desc = raw_input("What is the description of the save point?")
    saverules = raw_input('Hit enter to save the current active rules to this save point; type "false" to not save them (This overwrites rule configuration of the save point): ')
    params = {'oldname': oldname, 'newname': newname, 'description': desc, 'saverules': saverules}
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Create a port save point from current configuration
def createportsp(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/portsavepoint?'
    name = raw_input("What would you like to name the port save point?")
    desc = raw_input("Enter a description for the port save point")
    params = {'name': name, 'description': desc}
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Create a quicksave point of current configuration
def createquick(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/quicksaverules?'
    try:
        response = requests.put(uri, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Create a rule save point from current configuration
def createrulesp(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/rulesavepoint?'
    name = raw_input("What would you like to name the rule save point?")
    desc = raw_input("Enter a description for the rule save point")
    params = {'name': name, 'description': desc}
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Delete a port save point
def deleteportsp(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/portsavepoint?'
    name = raw_input("What is the name of the port save point you would like to delete?")
    params = {'name': name}
    try:
        response = requests.delete(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Delete a rule save point
def deleterulesp(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints/rulesavepoint?'
    name = raw_input("What is the name of the rule save point you would like to delete?")
    params = {'name': name}
    try:
        response = requests.delete(uri, data=params, auth=(username, password))
        print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Reboot the Packetmaster
def reboot(address, username=None, password=None):
    uri = 'http://' + address + '/rest/savepoints?'

    try:
        requests.post(uri, auth=(username, password))
        message = 'Device is rebooting...please allow 2 to 3 minutes for it to complete'
        return message
    except ConnectionError as e:
        r = 'No Response'
        raise e

if __name__ == '__main__':
    #Welcome statement
    print '''
        Welcome to my interactive Cubro Packetmaster REST API demo.
        All Packetmaster interaction in this program is accomplished via
        the Cubro REST API. \n'''

    #IP address to access REST data of device
    address = raw_input('What is the IP address of the Packetmaster you want to access?: ')
    #Write a check against valid IPv4 address
    #Device credentials
    username = raw_input('Enter your username: ')
    password = getpass()

    #Initial menu to check or change settings
    def topmenu():
        global address, address, username, password
        print 'Options for device at', address,'acting as User', username
        print '''
            1 - Change My working device
            2 - Change My user credentials
            3 - Check Packetmaster Settings
            4 - Change Packetmaster Settings
            5 - Quit \n'''

        option = raw_input('Enter the number of the action you would like to perform: ')
        try:
            option = int(option)
        except:
            topmenu()
        if option == 1:
            address = raw_input('What is the IP address of the Packetmaster you want to access: ')
            topmenu()
        elif option == 2:
            username = raw_input('Enter your username: ')
            password = getpass()
            topmenu()
        elif option == 3:
            checkmenu()
        elif option == 4:
            changemenu()
        elif option == 5:
            print 'Goodbye'
            exit()
        else:
            print 'That is not a valid selection \n'
            topmenu()

    #Check settings menu
    def checkmenu():
        print 'Check settings for device at', address,'acting as User', username
        print '''
                  1 - Software Version
                  2 - IP Configuration
                  3 - Model
                  4 - Name + Notes
                  5 - Serial Number
                  6 - Hardware Generation
                  7 - Port Configuration
                  8 - Port Status
                  9 - Port Counters
                 10 - SFP Status
                 11 - Show Rules
                 12 - List Apps
                 13 - List Running Apps
                 14 - Print Save Points
                 15 - Show Active Load-Balancing Hashes
                 16 - Permanence Mode
                 17 - Rule Storage Mode
                 18 - Environment
                 19 - ID LED Status
                 20 - OS and CPU Load Averages
                 21 - Memory Usage
                 22 - CCH Server Revision
                 23 - Go back to Top Menu \n'''
        choice = raw_input('Enter the number of the selection to check: ')
        try:
            choice = int(choice)
        except:
            checkmenu()
        if choice == 1:
            version = getversion(address, username, password)
            print version
            topmenu()
        elif choice == 2:
            ip = getip(address, username, password)
            print ip
            topmenu()
        elif choice == 3:
            model = getmodel(address, username, password)
            print model
            topmenu()
        elif choice == 4:
            label = getlabel(address, username, password)
            print label
            topmenu()
        elif choice == 5:
            serial = getserial(address, username, password)
            print serial
            topmenu()
        elif choice == 6:
            gen = getgen(address, username, password)
            print gen
            topmenu()
        elif choice == 7:
            config = getportconfig(address, username, password)
            print config
            topmenu()
        elif choice == 8:
            info = getportinfo(address, username, password)
            print info
            topmenu()
        elif choice == 9:
            stat = getportstat(address, username, password)
            print stat
            topmenu()
        elif choice == 10:
            spf = getsfp(address, username, password)
            print sfp
            topmenu()
        elif choice == 11:
            rulesrun = getrulesrun(address, username, password)
            print rulesrun
            topmenu()
        elif choice == 12:
            apps = getapps(address, username, password)
            print apps
            topmenu()
        elif choice == 13:
            appsrun = getappsrun(address, username, password)
            print appsrun
            topmenu()
        elif choice == 14:
            saves = getsaves(address, username, password)
            print saves
            topmenu()
        elif choice == 15:
            hashes = gethash(address, username, password)
            print hashes
            topmenu()
        elif choice == 16:
            perm = getperm(address, username, password)
            print perm
            topmenu()
        elif choice == 17:
            storage = getstor(address, username, password)
            print storage
            topmenu()
        elif choice == 18:
            env = getenv(address, username, password)
            print env
            topmenu()
        elif choice == 19:
            led = getidled(address, username, password)
            print led
            topmenu()
        elif choice == 20:
            load = getload(address, username, password)
            print load
            topmenu()
        elif choice == 21:
            memory = getmem(address, username, password)
            print memory
            topmenu()
        elif choice == 22:
            server = getserver(address, username, password)
            print server
            topmenu()
        elif choice == 23:
            topmenu()
        else:
            print 'That is not a valid choice \n'
            checkmenu()

    #Change settings menu
    def changemenu():
        print 'Change settings for device at', address,'acting as User', username
        print '''
                 1 - Change IP Configuration
                 2 - Change Device Name
                 3 - Change Port Configuration
                 4 - Shut Down or Activate Port
                 5 - Delete Port Counters
                 6 - Reset Rule Counters
                 7 - Add Rule
                 8 - Activate a save point for ports
                 9 - Activate a save point for rules
                10 - Set the rule save point to be loaded on boot
                11 - Export a save point
                12 - Modify a save point for port configuration
                13 - Modify a save point for rules
                14 - Create save point from current port configuration
                15 - Create a quicksave point from current configuration
                16 - Create a save point from current rules
                17 - Delete a port save point
                18 - Delete a rule save point
                19 - Reboot Packetmaster
                20 - Go back to Top Menu \n'''
        change = raw_input('Enter the number of the setting you would like to change: ')
        try:
            change = int(change)
        except:
            changemenu()
        if change == 1:
            ipchange = changeip(address, username, password)
            print ipchange
            topmenu()
        elif change == 2:
            namechange = changename(address, username, password)
            print namechange
            topmenu()
        elif change == 3:
            configchange = changeportconfig(address, username, password)
            print configchange
            topmenu()
        elif change == 4:
            onoff = portonoff(address, username, password)
            print onoff
            topmenu()
        elif change == 5:
            countersdelete = deletecounters(address, username, password)
            print countersdelete
            topmenu()
        elif change == 6:
            rulereset = resetrulecounter(address, username, password)
            print rulereset
            topmenu()
        elif change == 7:
            ruleadd = addrule(address, username, password)
            print ruleadd
            topmenu()
        elif change == 8:
            portspactive = actspport(address, username, password)
            print portspactive
            topmenu()
        elif change == 9:
            rulespactive = actsprule(address, username, password)
            print rulespactive
            topmenu()
        elif change == 10:
            spset = setbootsp(address, username, password)
            print spset
            topmenu()
        elif change == 11:
            spexport = exportsp(address, username, password)
            print spexport
            topmenu()
        elif change == 12:
            portspmod = modportsp(address, username, password)
            print portspmod
            topmenu()
        elif change == 13:
            rulepsmod = modrulesp(address, username, password)
            print rulepsmod
            topmenu()
        elif change == 14:
            portspcreate = createportsp(address, username, password)
            print portspcreate
            topmenu()
        elif change == 15:
            quickcreate = createquick(address, username, password)
            print quickcreate
            topmenu()
        elif change == 16:
            rulespcreate = createrulesp(address, username, password)
            print rulespcreate
            topmenu()
        elif change == 17:
            portspdelete = deleteportsp(address, username, password)
            print portspdelete
            topmenu()
        elif change == 18:
            rulepsdelete = deleterulesp(address, username, password)
            print rulespdelete
            topmenu()
        elif change == 19:
            restart = reboot(address, username, password)
            print restart
            topmenu()
        elif change == 20:
            topmenu()
        else:
            print 'That is not a valid choice \n'
            changemenu()

    topmenu()
