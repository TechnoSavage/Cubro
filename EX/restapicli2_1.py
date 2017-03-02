#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.  Written by Derek Burke 12/2016
#Import necessary Python libraries for interacting with the REST API
import urllib, requests, json
from getpass import getpass
from requests.exceptions import ConnectionError

#Retrieve firmware version
def getversion(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve IP configuration
def getip(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve Packetmaster model
def getmodel(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve Packetmaster name
def getname(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve Packetmaster Name plus Notes
def getlabel(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve hardware generation of the device
def getgen(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve Packetmaster serial number
def getserial(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve current port configuration
def getportconfig(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve port statistics
def getportinfo(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve port counters
def getportstat(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve SFP information
def getsfp(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve active rules
def getrulesrun(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#List all available apps
def getapps(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve running apps
def getappsrun(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve hash algorithm information
def gethash(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve rule permanence mode
def getperm(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve rule storage model
def getstor(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve environment information
def getenv(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve deice ID LED status_code
def getidled(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve load information
def getload(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve memory usage
def getmem(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Retrieve cch machinery server revision
def getserver(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#List all save points
def getsaves(address, uri, auth):
    try:
        url = address + uri + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Change the management IP configuration
def changeip(address, uri, auth):
    newip = raw_input('Enter IP Address (e.g. 192.168.0.200): ')
    newmask = raw_input('Enter Subnet Mask (e.g. 255.255.255.0): ')
    newgate = raw_input('Enter gateway (e.g. 192.168.0.1): ')
    url = address + uri + auth
    params = {'ip': newip, 'mask': newmask, 'gw': newgate}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Change the device name
def changename(address, uri, auth):
    newname = raw_input('Enter device name: ')
    url = address + uri + auth
    params = {'devicename': newname}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Change the configuration of a port
def changeportconfig(address, uri, auth): #Add additional parameters, add function to change multiple ports without exiting
    interface = raw_input('Enter the interface name of the port you want to change: ')
    speed = raw_input('Enter the desired interface speed; options are  "10", "100", "1000", "10G", "40G", "100G", or "auto": ')
    duplex = raw_input('Enter the Duplex of the interface; options are "full", "half, or "auto": ')
    forcetx = raw_input('Force TX?  Enter "true" for yes and "false" for no: ')
    check = raw_input('Perform CRC check?  Enter "true" for yes and "false" for no: ')
    recalc = raw_input('Perform CRC recalculation?  Enter "true" for yes and "false" for no: ')
    url = address + uri + auth
    params = {
        'if_name': interface,
        'speed': speed,
        'duplex': duplex,
        'unidirectional': forcetx,
        'crc_check': check,
        'crc_recalculation': recalc }
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Activate or deactivate a port
def portonoff(address, uri, auth):
    interface = raw_input('Enter the interface name of the port you want to change: ')
    updown = raw_input('Enter "true" to shut port down; Enter "false" to reactivate port: ')
    url = address + uri + auth
    params = {'if_name': interface, 'shutdown': updown}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Reset Port Counters
def deletecounters(address, uri, auth):
    url = address + uri + auth
    try:
        requests.delete(url)
        print 'Counters deleted successfully'
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Reset Rule Counters
def resetrulecounter(address, uri, auth):
    url = address + uri + auth
    try:
        requests.delete(url)
        print 'Counters deleted successfully'
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Add a rule
def addrule(address, uri, auth):
    url = address + uri + auth
    params = {}
    rulename = raw_input('Enter a name for the rule: ')
    if rulename != '':
        params['name'] = rulename
    ruledescrip = raw_input('Enter a description for the rule: ')
    if ruledescrip != '':
        params['description'] = ruledescrip
    priority = int(raw_input('Enter the priority level of the rule; 0 - 65535 higher number = higher priority: '))
    params['priority'] = priority
    portin = raw_input('Enter the port number or numbers for incoming traffic; multiple ports separated by a comma: ')
    params['match[in_port]'] = portin
    print '''\nMatch VLAN tag?
            1 - No, match all tagged and untagged traffic
            2 - No, match only untagged traffic
            3 - Yes, match a VLAN tag \n'''
    trafmatch = raw_input('Enter the number of your selection: ')
    if trafmatch == '' or int(trafmatch) == 1:
        pass
    elif int(trafmatch) == 2:
        params['match[vlan]'] = 'neg_match'
    elif int(trafmatch) == 3:
        params['match[vlan]'] = 'match'
        matchid = raw_input('Enter the VLAN ID to filter on: ')
        params['match[vlan_id]'] = matchid
        vpri = raw_input('Enter the VLAN priority (Enter 0-7): ')
        params['match[vlan_priority]'] = vpri
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
    proto = raw_input('Enter the number of your selection: ')
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
    ruleaction = raw_input('Enter the desired output actions separated by commas; order matters - imporoper syntax will cause add rule to fail: ')
    params['actions'] = ruleaction
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Make a port save point active
def actspport(address, uri, auth):
    savename = raw_input('What is the name of the port save point to make active?: ')
    url = address + uri + auth
    params = {'name': savename}
    try:
        response = requests.put(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Make a rule save point active
def actsprule(address, uri, auth):
    savename = raw_input('What is the name of the rule save point to make active?: ')
    url = address + uri + auth
    params = {'name': savename}
    try:
        response = requests.put(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Set a save point as the default boot configuration
def setbootsp(address, uri, auth):
    savename = raw_input('What is the name of the save point to make the default at boot configuration?: ')
    url = address + uri + auth
    params = {'name': savename}
    try:
        response = requests.put(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Export a save point from the Packetmaster
def exportsp(address, uri, auth):
    rspname = raw_input('What is the name of the rule save point to export? (leave blank for none): ')
    rspname = '[' + rspname + ']'
    pspname = raw_input('What is the name of the port save point to export? (leave blank for none): ')
    pspname = '[' + pspname + ']'
    url = address + uri + auth
    params = {'rule_save_point_names': rspname, 'port_save_point_names': pspname} #Change to JSON encoding
    try:
        response = requests.get(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
        filename = raw_input("Enter a file name for the savepoint: ")
        try:
            with open(filename, "w") as f:
                f.write(r) #Try json.dump(r, f)?
        except:
            print "Invalid filename\n"
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Modify a port save point
def modportsp(address, uri, auth):
    oldname = raw_input("What is the name of the save point you would like to modify?")
    newname = raw_input("What would you like to rename this save point to?")
    desc = raw_input("What is the description of the save point?")
    saveports = raw_input('Hit enter to save the current active ports to this save point; type "false" to not save them (This overwrites port configuration of the save point): ')
    url = address + uri + auth
    params = {'oldname': oldname, 'newname': newname, 'description': desc, 'saveports': saveports}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Modify a rule save point
def modrulesp(address, uri, auth):
    oldname = raw_input("What is the name of the save point you would like to modify?")
    newname = raw_input("What would you like to rename this save point to?")
    desc = raw_input("What is the description of the save point?")
    saverules = raw_input('Hit enter to save the current active rules to this save point; type "false" to not save them (This overwrites rule configuration of the save point): ')
    url = address + uri + auth
    params = {'oldname': oldname, 'newname': newname, 'description': desc, 'saverules': saverules}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Create a port save point from current configuration
def createportsp(address, uri, auth):
    name = raw_input("What would you like to name the port save point?")
    desc = raw_input("Enter a description for the port save point")
    url = address + uri + auth
    params = {'name': name, 'description': desc}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Create a quicksave point of current configuration
def createquick(address, uri, auth):
    url = address + uri + auth
    try:
        response = requests.put(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Create a rule save point from current configuration
def createrulesp(address, uri, auth):
    name = raw_input("What would you like to name the rule save point?")
    desc = raw_input("Enter a description for the rule save point")
    url = address + uri + auth
    params = {'name': name, 'description': desc}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Delete a port save point
def deleteportsp(address, uri, auth):
    name = raw_input("What is the name of the port save point you would like to delete?")
    url = address + uri + auth
    params = {'name': name}
    try:
        response = requests.delete(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Delete a rule save point
def deleterulesp(address, uri, auth):
    name = raw_input("What is the name of the rule save point you would like to delete?")
    url = address + uri + auth
    params = {'name': name}
    try:
        response = requests.delete(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Reboot the Packetmaster
def reboot(address, uri, auth):
    url = address + uri + auth
    try:
        requests.post(url)
        print 'Device is rebooting...please allow 2 to 3 minutes for it to complete'
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

if __name__ == '__main__':
    #Welcome statement
    print '''
        Welcome to my interactive Cubro Packetmaster REST API demo.
        All Packetmaster interaction in this program is accomplished via
        the Cubro REST API. \n'''

    #IP address to access REST data of device
    deviceip = raw_input('What is the IP address of the Packetmaster you want to access: ')
    address = 'http://' + deviceip + '/rest'
    #Device credentials
    username = raw_input('Enter your username: ')
    password = getpass()
    auth = urllib.urlencode({
        'username': username,
        'password': password
        })

    #options to append to device URL
    version = '/device/imageversion?' #good
    ipconfig = '/device/ipconfig?' #good
    devicemodel = '/device/model?' #good
    devicename = '/device/name?' #good
    devicelabel = '/device/customident?' #add post
    devicegen = '/device/generation?' #good
    deviceenv = '/device/environment?' #good
    deviceidled = '/device/idled?' #add post
    deviceload = '/device/loadaverage?' #good
    devicemem = '/device/memoryusage?' #good
    devicehash = '/device/grouphash?' #Add post
    devicehttps = '/device/https?' #Add post
    deviceserver = '/device/serverrevision?' #good
    deviceperm = '/device/permanentrulesmode?' #Add post
    devicestor = '/device/rulestoragemode?' #Add post
    serial = '/device/serialno?' #good
    portconfig = '/ports/config?' #good
    portinfo = '/ports/info?'
    portstat = '/ports/stats?'
    sfp = '/ports/sfpstatus?'
    counters = '/ports/counters?'
    rulecount = '/rules/counters?'
    rule = '/rules?' #change
    allrule = '/rules/all?' #change/add
    flows = '/flownumbers?' #change/add
    apps = '/apps?'
    appsrun = '/apps/running?'
    appsact = '/apps/action?' #add
    groups = '/groups?' #add
    allgroup = '/groups/all?' #add
    sp = '/savepoints?'
    spaports = '/savepoints/activeportsavepoint?'
    sparules = '/savepoints/activerulesavepoint?'
    spset = '/savepoints/defaultrulesavepoint?'
    spexport = '/savepoints/export?'
    spmodport = '/savepoints/modportsavepoint?'
    spmodrule = '/savepoints/modrulesavepoint?'
    spportsave = '/savepoints/portsavepoint?'
    spquick = '/savepoints/quicksaverules?'
    sprulesave = '/savepoints/rulesavepoint?'
    reboot = '/device/reboot?'
    users = '/users?' #add
    raduser = '/users/radius?' #add
    uac = '/users/uac?' #add
    weblog = '/weblog?' #add

    #Initial menu to check or change settings
    def topmenu():
        global deviceip, address, username, password, auth
        print 'Options for device at', deviceip,'acting as User', username
        print '''
            1 - Change My working device
            2 - Change My user credentials
            3 - Check Packetmaster Settings
            4 - Change Packetmaster Settings
            5 - Quit \n'''

        option = raw_input('Enter the number of what you would like to do: ')
        if int(option) == 1:
            deviceip = raw_input('What is the IP address of the Packetmaster you want to access: ')
            address = 'http://' + deviceip + '/rest'
            topmenu()
        elif int(option) == 2:
            username = raw_input('Enter your username: ')
            password = raw_input('Enter your password: ')
            auth = urllib.urlencode({
                'username': username,
                'password': password
            })
            topmenu()
        elif int(option) == 3:
            checkmenu()
        elif int(option) == 4:
            changemenu()
        elif int(option) == 5:
            print 'Goodbye'
            exit()
        else:
            print 'That is not a valid selection \n'
            topmenu()

    #Check settings menu
    def checkmenu():
        print 'Check settings for device at', deviceip,'acting as User', username
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
        if int(choice) == 1:
            getversion(address, version, auth)
            topmenu()
        elif int(choice) == 2:
            getip(address, ipconfig, auth)
            topmenu()
        elif int(choice) == 3:
            getmodel(address, devicemodel, auth)
            topmenu()
        elif int(choice) == 4:
            getlabel(address, devicelabel, auth)
            topmenu()
        elif int(choice) == 5:
            getserial(address, serial, auth)
            topmenu()
        elif int(choice) == 6:
            getgen(address, devicegen, auth)
            topmenu()
        elif int(choice) == 7:
            getportconfig(address, portconfig, auth)
            topmenu()
        elif int(choice) == 8:
            getportinfo(address, portinfo, auth)
            topmenu()
        elif int(choice) == 9:
            getportstat(address, portstat, auth)
            topmenu()
        elif int(choice) == 10:
            getsfp(address, sfp, auth)
            topmenu()
        elif int(choice) == 11:
            getrulesrun(address, rulesrun, auth)
            topmenu()
        elif int(choice) == 12:
            getapps(address, apps, auth)
            topmenu()
        elif int(choice) == 13:
            getappsrun(address, appsrun, auth)
            topmenu()
        elif int(choice) == 14:
            getsaves(address, sp, auth)
            topmenu()
        elif int(choice) == 15:
            gethash(address, devicehash, auth)
            topmenu()
        elif int(choice) == 16:
            getperm(address, deviceperm, auth)
            topmenu()
        elif int(choice) == 17:
            getstor(address, devicestor, auth)
            topmenu()
        elif int(choice) == 18:
            getenv(address, deviceenv, auth)
            topmenu()
        elif int(choice) == 19:
            getidled(address, deviceidled, auth)
            topmenu()
        elif int(choice) == 20:
            getload(address, deviceload, auth)
            topmenu()
        elif int(choice) == 21:
            getmem(address, devicemem, auth)
            topmenu()
        elif int(choice) == 22:
            getserver(address, deviceserver, auth)
            topmenu()
        elif int(choice) == 23:
            topmenu()
        else:
            print 'That is not a valid choice \n'
            checkmenu()

    #Change settings menu
    def changemenu():
        print 'Change settings for device at', deviceip,'acting as User', username
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
        if int(change) == 1:
            changeip(address, ipconfig, auth)
            topmenu()
        elif int(change) == 2:
            changename(address, devicename, auth)
            topmenu()
        elif int(change) == 3:
            changeportconfig(address, portconfig, auth)
            topmenu()
        elif int(change) == 4:
            portonoff(address, portconfig, auth)
            topmenu()
        elif int(change) == 5:
            deletecounters(address, counters, auth)
            topmenu()
        elif int(change) == 6:
            resetrulecounter(address, rulecount, auth)
            topmenu()
        elif int(change) == 7:
            addrule(address, rule, auth)
            topmenu()
        elif int(change) == 8:
            actspport(address, spaports, auth)
            topmenu()
        elif int(change) == 9:
            actsprule(address, sparules, auth)
            topmenu()
        elif int(change) == 10:
            setbootsp(address, spset, auth)
            topmenu()
        elif int(change) == 11:
            exportsp(address, spexport, auth)
            topmenu()
        elif int(change) == 12:
            modportsp(address, spmodport, auth)
            topmenu()
        elif int(change) == 13:
            modrulesp(address, spmodrule, auth)
            topmenu()
        elif int(change) == 14:
            createportsp(address, spportsave, auth)
            topmenu()
        elif int(change) == 15:
            createquick(address, spquick, auth)
            topmenu()
        elif int(change) == 16:
            createrulesp(address, sprulesave, auth)
            topmenu()
        elif int(change) == 17:
            deleteportsp(address, spportsave, auth)
            topmenu()
        elif int(change) == 18:
            deleterulesp(address, sprulesave, auth)
            topmenu()
        elif int(change) == 19:
            reboot(address, reboot, auth)
            topmenu()
        elif int(change) == 20:
            topmenu()
        else:
            print 'That is not a valid choice \n'
            changemenu()

    topmenu()
