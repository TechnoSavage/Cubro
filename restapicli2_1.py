#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.  Written by Derek Burke 12/2016
#Import necessary Python libraries for interacting with the REST API
import urllib, requests, json
from requests.exceptions import ConnectionError

#Welcome statement
print '''
Welcome to my interactive Cubro Packetmaster REST API demo.
All Packetmaster interaction in this program is accomplished via
the Cubro REST API. \n'''

#IP address to access REST data of device
deviceip = raw_input('What is the IP address of the Packetmaster you want to access: ')
ip = 'http://' + deviceip + '/rest'
#Device credentials
username = raw_input('Enter your username: ')
password = raw_input('Enter your password: ')
auth = urllib.urlencode({
    'username': username,
    'password': password
})

#options to append to device URL
version = '/device/imageversion?' #good
address = '/device/ipconfig?' #good
devicemodel = '/device/model?' #good
devicename = '/device/name?' #good
devicelabel = '/device/customident?' #Add
devicegen = '/device/generation?' #Add
deviceenv = '/device/environment?' #Add
deviceidled = '/device/idled?' #Add
deviceload = '/device/loadaverage?' #Add
devicemem = '/device/memoryusage?' #Add
devicehash = '/device/grouphash?' #Add
devicehttps = 'device/https?' #Add
deviceserver = 'device/serverrevision?' #Add
deviceperm = '/device/permanentrulesmode?' #Add
devicestor = '/device/rulestoragemode?' #Add
serial = '/device/serialno?' #good
portconfig = '/ports/config?'
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
weblog = 'weblog?' #add

#Initial menu to check or change settings
def topmenu():
    global deviceip, ip, username, password, auth
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
        ip = 'http://' + deviceip + '/rest'
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
              4 - Name
              5 - Serial Number
              6 - Port Configuration
              7 - Port Status
              8 - Port Counters
              9 - SFP Status
             10 - Show Rules
             11 - List Apps
             12 - List Running Apps
             13 - Print Save Points
             14 - Go back to Top Menu \n'''
    choice = raw_input('Enter the number of the selection to check: ')
    if int(choice) == 1:
        getversion()
    elif int(choice) == 2:
        getip()
    elif int(choice) == 3:
        getmodel()
    elif int(choice) == 4:
        getname()
    elif int(choice) == 5:
        getserial()
    elif int(choice) == 6:
        getportconfig()
    elif int(choice) == 7:
        getportinfo()
    elif int(choice) == 8:
        getportstat()
    elif int(choice) == 9:
        getsfp()
    elif int(choice) == 10:
        getrulesrun()
    elif int(choice) == 11:
        getapps()
    elif int(choice) == 12:
        getappsrun()
    elif int(choice) == 13:
        getsaves()
    elif int(choice) == 14:
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
        changeip()
    elif int(change) == 2:
        changename()
    elif int(change) == 3:
        changeportconfig()
    elif int(change) == 4:
        portonoff()
    elif int(change) == 5:
        deletecounters()
    elif int(change) == 6:
        resetrulecounter()
    elif int(change) == 7:
        addrule()
    elif int(change) == 8:
        actspport()
    elif int(change) == 9:
        actsprule()
    elif int(change) == 10:
        setbootsp()
    elif int(change) == 11:
        exportsp()
    elif int(change) == 12:
        modportsp()
    elif int(change) == 13:
        modrulesp()
    elif int(change) == 14:
        createportsp()
    elif int(change) == 15:
        createquick()
    elif int(change) == 16:
        createrulesp()
    elif int(change) == 17:
        deleteportsp()
    elif int(change) == 18:
        deleterulesp()
    elif int(change) == 19:
        reboot()
    elif int(change) == 20:
        topmenu()
    else:
        print 'That is not a valid choice \n'
        changemenu()

#Retrieve firmware version
def getversion():
    try:
        url = ip + version + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve IP configuration
def getip():
    try:
        url = ip + address + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve Packetmaster model
def getmodel():
    try:
        url = ip + devicemodel + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve Packetmaster name
def getname():
    try:
        url = ip + devicename + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve Packetmaster serial number
def getserial():
    try:
        url = ip + serial + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve current port configuration
def getportconfig():
    try:
        url = ip + portconfig + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve port statistics
def getportinfo():
    try:
        url = ip + portinfo + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve port counters
def getportstat():
    try:
        url = ip + portstat + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve SFP information
def getsfp():
    try:
        url = ip + sfp + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve active rules
def getrulesrun():
    try:
        url = ip + rulesrun + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#List all available apps
def getapps():
    try:
        url = ip + apps + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Retrieve running apps
def getappsrun():
    try:
        url = ip + appsrun + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#List all save points
def getsaves():
    try:
        url = ip + sp + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Change the management IP configuration
def changeip():
    newip = raw_input('Enter IP Address (e.g. 192.168.0.200): ')
    newmask = raw_input('Enter Subnet Mask (e.g. 255.255.255.0): ')
    newgate = raw_input('Enter gateway (e.g. 192.168.0.1): ')
    url = ip + address + auth
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
    topmenu()

#Change the device name
def changename():
    newname = raw_input('Enter device name: ')
    url = ip + devicename + auth
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
    topmenu()

#Change the configuration of a port
def changeportconfig(): #Add additional parameters, add function to change multiple ports without exiting
    interface = raw_input('Enter the interface name of the port you want to change: ')
    speed = raw_input('Enter the desired interface speed; options are  "10", "100", "1000", "10G", "40G", "100G", or "auto": ')
    duplex = raw_input('Enter the Duplex of the interface; options are "full", "half, or "auto": ')
    url = ip + portconfig + auth
    params = {'ifName': interface, 'speed': speed, 'duplex': duplex}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Activate or deactivate a port
def portonoff():
    interface = raw_input('Enter the interface name of the port you want to change: ')
    updown = raw_input('Enter "true" to shut port down; Enter "false" to reactivate port: ')
    url = ip + portconfig + auth
    params = {'ifName': interface, 'shutdown': updown}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Reset Port Counters
def deletecounters():
    url = ip + counters + auth
    try:
        requests.delete(url)
        print 'Counters deleted successfully'
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Reset Rule Counters
def resetrulecounter():
    url = ip + rulecount + auth
    try:
        requests.delete(url)
        print 'Counters deleted successfully'
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Add a rule
def addrule():
    url = ip + rule + auth
    rulename = raw_input('Enter a name for the rule: ')
    ruledescrip = raw_input('Enter a description for the rule: ')
    priority = int(raw_input('Enter the priority level of the rule; 0 - 65535 higher number = higher priority: '))
    portin = raw_input('Enter the port number or numbers for incoming traffic; multiple ports separated by a comma: ')
    print '''Match VLAN tag?
            1 - No, match all tagged and untagged traffic
            2 - No, match only untagged traffic
            3 - Yes, match a VLAN tag'''
    trafmatch = raw_input('Enter the number of your selection: ')
    if trafmatch == '':
        trafmatch = 1
    if int(trafmatch) == 1:
        matchvlan = ''
    elif int(trafmatch) == 2:
        matchvlan = 'neg_match'
    elif int(trafmatch) == 3:
        matchvlan = 'match'
        matchid = raw_input('Enter the VLAN ID to filter on: ')
        vpri = raw_input('Enter the VLAN priority (Enter 0-7): ')
    else:
        print 'That is not a valid selection; restarting add rule'
        addrule()
    macsrc = raw_input('Filter by source MAC address?  Leave blank for no or enter MAC address: ')
    macdst = raw_input('Filter by destination MAC address?  Leave blank for no or enter MAC address: ')
    print '''Filter on protocol?
            1 - No Protocol Filtering
            2 - ip
            3 - tcp
            4 - udp
            5 - sctp
            6 - icmp
            7 - arp
            8 - Enter Ethertype'''
    proto = raw_input('Enter the number of your selection: ')
    if proto == '':
        proto = 1
    if int(proto) == 1:
        profil = ''
    elif int(proto) == 2:
        profil = 'ip'
        nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
        nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
    elif int(proto) == 3:
        profil = 'tcp'
        nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
        nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
        tcpsrc = raw_input('Filter on source port?  Leave blank for no or enter port number: ')
        tcpdst = raw_input('Filter on destination port?  Leave blank for no or enter port number: ')
    elif int(proto) == 4:
        profil = 'udp'
        nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
        nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
        udpsrc = raw_input('Filter on source port?  Leave blank for no or enter port number: ')
        udpdst = raw_input('Filter on destination port?  Leave blank for no or enter port number: ')
    elif int(proto) == 5:
        profil = 'sctp'
        nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
        nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
        sctpsrc = raw_input('Filter on source port?  Leave blank for no or enter port number: ')
        sctpdst = raw_input('Filter on destination port?  Leave blank for no or enter port number: ')
    elif int(proto) == 6:
        profil = 'icmp'
        nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
        nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
        icmpt = raw_input('Flter on ICMP type?  Leave blank for no or enter ICMP type number: ')
        icmpc = raw_input('Flter on ICMP code?  Leave blank for no or enter ICMP code number: ')
    elif int(proto) == 7:
        profil = 'arp'
    elif int(proto) == 8:
        profil = 'custom'
        ether = raw_input('Enter Ethertype e.g. 0x800: ')
        nwproto = raw_input('Enter protocol number (protocol number in IPv4, header type in IPv6, opcode in ARP) or leave blank for none: ')
    else:
        print 'That is not a valid selection; restarting add rule'
        addrule()
    print '''Add rule timeout?
            1 - No
            2 - Hard Timeout
            3 - Idle Timeout'''
    xsel = raw_input('Enter the number of your selection: ')
    if xsel == '':
        xsel = 1
    if int(xsel) == 1:
        extra = ''
    elif int(xsel) == 2:
        time = raw_input('Enter the time in seconds for the rule to exist: ')
        extra = 'hard_timeout=' + time
    elif int(xsel) == 3:
        time = raw_input('Enter the time in seconds for the rule to exist while not idle: ')
        extra = 'idle_timeout=' + time
    else:
        print 'That is not a valid selection; no timeout will be applied'
        extra = ''
    ruleaction = raw_input('Enter the desired output actions separated by commas; order matters - imporoper syntax will cause add rule to fail: ')
    if int(trafmatch) != 3 and int(proto) == 1:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) == 3 and int(proto) == 1:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) != 3 and int(proto) == 2:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) == 3 and int(proto) == 2:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) != 3 and int(proto) == 3:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[tcp_src]': tcpsrc, 'match[tcp_dst]': tcpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) == 3 and int(proto) == 3:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[tcp_src]': tcpsrc, 'match[tcp_dst]': tcpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) != 3 and int(proto) == 4:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[udp_src]': udpsrc, 'match[udp_dst]': udpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) == 3 and int(proto) == 4:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[sctp_src]': sctpsrc, 'match[sctp_dst]': sctpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) != 3 and int(proto) == 5:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[sctp_src]': sctpsrc, 'match[sctp_dst]': sctpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) == 3 and int(proto) == 5:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[udp_src]': udpsrc, 'match[udp_dst]': udpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) != 3 and int(proto) == 6:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[icmp_type]': icmpt, 'match[icmp_code]': icmpc, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) == 3 and int(proto) == 6:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[icmp_type]': icmpt, 'match[icmp_code]': icmpc, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) != 3 and int(proto) == 7:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) == 3 and int(proto) == 7:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) != 3 and int(proto) == 8:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[dl_type]': ether, 'match[nw_proto]': nwproto, 'match[match_extra]': extra, 'actions': ruleaction}
    elif int(trafmatch) == 3 and int(proto) == 8:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[dl_type]': ether, 'match[nw_proto]': nwproto, 'match[match_extra]': extra, 'actions': ruleaction}
    else:
        print 'Something went horribly wrong.'
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Make a port save point active
def actspport():
    savename = raw_input('What is the name of the port save point to make active?: ')
    url = ip + spaports + auth
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
    topmenu()

#Make a rule save point active
def actsprule():
    savename = raw_input('What is the name of the rule save point to make active?: ')
    url = ip + sparules + auth
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
    topmenu()

#Set a save point as the default boot configuration
def setbootsp():
    savename = raw_input('What is the name of the save point to make the default at boot configuration?: ')
    url = ip + spset + auth
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
    topmenu()

#Export a save point from the Packetmaster
def exportsp(): #Write code to save object accompanying response to file
    rspname = raw_input('What is the name of the rule save point to export? (leave blank for none): ')
    pspname = raw_input('What is the name of the port save point to export? (leave blank for none): ')
    url = ip + spexport + auth
    params = {'rule_save_point_names': rspname, 'port_save_point_names': pspname}
    try:
        response = requests.get(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
        filename = raw_input('Enter a file name for the exported savepoint: ')
        with open(filename) as filename:
            f.write(r)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Modify a port save point
def modportsp():
    oldname = raw_input("What is the name of the save point you would like to modify?")
    newname = raw_input("What would you like to rename this save point to?")
    desc = raw_input("What is the description of the save point?")
    saveports = raw_input('Hit enter to save the current active ports to this save point; type "false" to not save them (This overwrites port configuration of the save point): ')
    url = ip + spmodport + auth
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
    topmenu()

#Modify a rule save point
def modrulesp():
    oldname = raw_input("What is the name of the save point you would like to modify?")
    newname = raw_input("What would you like to rename this save point to?")
    desc = raw_input("What is the description of the save point?")
    saverules = raw_input('Hit enter to save the current active rules to this save point; type "false" to not save them (This overwrites rule configuration of the save point): ')
    url = ip + spmodrule + auth
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
    topmenu()

#Create a port save point from current configuration
def createportsp():
    name = raw_input("What would you like to name the port save point?")
    desc = raw_input("Enter a description for the port save point")
    url = ip + spportsave + auth
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
    topmenu()

#Create a quicksave point of current configuration
def createquick():
    url = ip + spquick + auth
    try:
        response = requests.put(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

#Create a rule save point from current configuration
def createrulesp():
    name = raw_input("What would you like to name the rule save point?")
    desc = raw_input("Enter a description for the rule save point")
    url = ip + sprulesave + auth
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
    topmenu()

#Delete a port save point
def deleteportsp():
    name = raw_input("What is the name of the port save point you would like to delete?")
    url = ip + spportsave + auth
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
    topmenu()

#Delete a rule save point
def deleterulesp():
    name = raw_input("What is the name of the rule save point you would like to delete?")
    url = ip + sprulesave + auth
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
    topmenu()

#Reboot the Packetmaster
def reboot():
    url = ip + reboot + auth
    try:
        requests.post(url)
        print 'Device is rebooting...please allow 2 to 3 minutes for it to complete'
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    topmenu()

topmenu()
