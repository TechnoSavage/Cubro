#This program uses an untested version of the Cubro API
#Use with firmware version 2.1.0.x or later. Python2.7 Cubro Packetmaster REST API demo.  Written by Derek Burke 10/2016
#Import necessary Python libraries for interacting with the REST API
import urllib, requests, json

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
version = '/device/imageversion?'
address = '/device/ipconfig?'
devicemodel = '/device/model?'
devicename = '/device/name?'
serial = '/device/serialno?'
portconfig = '/ports/config?'
portinfo = '/ports/info?'
portstat = '/ports/stats?'
sfp = '/ports/sfpstatus?'
rulesrun = '/rules/all?'
counters = '/ports/counters?'
rulecount = '/rules/counters?'
flownumber = '/flownumbers?'
rule = '/rules?'
apps = '/apps?'
appsrun = '/apps/running?'
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

    menuselect = raw_input('Enter the number of what you would like to do: ')
    option = menuselect
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
        print 'That is not a valid selection'
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
             11 - Show TCAM flow numbers
             12 - List Apps
             13 - List Running Apps
             14 - Print Save Points \n'''
    userselect = raw_input('Enter the number of the selection to check: ')
    choice = userselect
    if int(choice) >= 1 and int(choice) <= 14:
        choice = int(choice)
        print 'Working'
        if choice == 1:
            getversion()
        elif choice == 2:
            getip()
        elif choice == 3:
            getmodel()
        elif choice == 4:
            getname()
        elif choice == 5:
            getserial()
        elif choice == 6:
            getportconfig()
        elif choice == 7:
            getportinfo()
        elif choice == 8:
            getportstat()
        elif choice == 9:
            getsfp()
        elif choice == 10:
            getrulesrun()
        elif choice == 11:
            getflows()
        elif choice == 12:
            getapps()
        elif choice == 13:
            getappsrun()
        elif choice == 14:
            getsaves()
        else:
            print 'Something went horribly wrong'
            exit()
    else:
        print 'That is not a valid choice'

#Change settings menu
def changemenu():
    print 'Change settings for device at', deviceip,'acting as User', username
    print '''
             1 - Change IP Configuration
             2 - Change Device Name
             3 - Change Port Configuration
             4 - Shut Down or Activate Port
             5 - Delete Port Counters
             6 - Reset rule counters
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
            19 - Reboot Packetmaster \n'''
    userchange = raw_input('Enter the number of the setting you would like to change: ')
    change = userchange
    if int(change) >= 1 and int(change) <= 19:
        change = int(change)
        print 'Working'
        if change == 1:
            changeip()
        elif change == 2:
            changename()
        elif change == 3:
            changeportconfig()
        elif change == 4:
            portonoff()
        elif change == 5:
            deletecounters()
        elif change == 6:
            resetrulecounter()
        elif change == 7:
            addrule()
        elif change == 8:
            actspport()
        elif change == 9:
            actsprule()
        elif change == 10:
            setbootsp()
        elif change == 11:
            exportsp()
        elif change == 12:
            modportsp()
        elif change == 13:
            modrulesp()
        elif change == 14:
            createportsp()
        elif change == 15:
            createquick()
        elif change == 16:
            createrulesp()
        elif change == 17:
            deleteportsp()
        elif change == 18:
            deleterulesp()
        elif change == 19:
            reboot()
        else:
            print 'Something went horribly wrong'
            exit()
    else:
        print 'That is not a valid choice'
        topmenu()

#Retrieve firmware version
def getversion():
    try:
        url = ip + version + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
    topmenu()

#Retrieve TCAM flow numbers
def getflows():
    try:
        url = ip + flownumber + auth
        response = requests.get(url)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
    topmenu()

#Change the configuration of a port
def changeportconfig(): #Add additional parameters, add function to change multiple ports without exiting
    interface = raw_input('Enter the interface name of the port you want to change: ')
    speed = raw_input('Enter the desired interface speed; options are  "10", "100", "1000", "10G", "40G", "100G", or "auto": ')
    duplex = raw_input('Enter the Duplex of the interface; options are "full", "half, or "auto": ')
    url = ip + portconfig + auth
    params = {'if_name': interface, 'speed': speed, 'duplex': duplex}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
    topmenu()

#Reset Port Counters
def deletecounters():
    url = ip + counters + auth
    try:
        requests.delete(url)
        print 'Counters deleted successfully'
    except:
        print 'Unable to delete counters'
    topmenu()

#Reset Rule Counters
def resetrulecounter():
        url = ip + rulecount + auth
        try:
            requests.delete(url)
            print 'Counters deleted successfully'
        except:
            print 'Unable to delete counters'
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
    matchtraf = trafmatch
    if int(trafmatch) >= 1 and int(trafmatch) <=3:
        matchtraf = int(trafmatch)
        if matchtraf == 1:
            matchvlan = ''
        elif matchtraf == 2:
            matchvlan = 'neg_match'
        elif matchtraf == 3:
            matchvlan = 'match'
            matchid = raw_input('Enter the VLAN ID to filter on: ')
            vpri = raw_input('Enter the VLAN priority (Enter 0-7): ')
        else:
            print 'Something went horribly wrong'
            exit()
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
    filt = proto
    if int(proto) >= 1 and int(proto) <= 8:
        filt = int(proto)
        if filt == 1:
            profil = ''
        elif filt == 2:
            profil = 'ip'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
        elif filt == 3:
            profil = 'tcp'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
            tcpsrc = raw_input('Filter on source port?  Leave blank for no or enter port number: ')
            tcpdst = raw_input('Filter on destination port?  Leave blank for no or enter port number: ')
        elif filt == 4:
            profil = 'udp'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
            udpsrc = raw_input('Filter on source port?  Leave blank for no or enter port number: ')
            udpdst = raw_input('Filter on destination port?  Leave blank for no or enter port number: ')
        elif filt == 5:
            profil = 'sctp'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
            sctpsrc = raw_input('Filter on source port?  Leave blank for no or enter port number: ')
            sctpdst = raw_input('Filter on destination port?  Leave blank for no or enter port number: ')
        elif filt == 6:
            profil = 'icmp'
            nwsrc = raw_input('Filter on source IP address?  Leave blank for no or enter IP address: ')
            nwdst = raw_input('Filter on destination IP address?  Leave blank for no or enter IP address: ')
            icmpt = raw_input('Flter on ICMP type?  Leave blank for no or enter ICMP type number: ')
            icmpc = raw_input('Flter on ICMP code?  Leave blank for no or enter ICMP code number: ')
        elif filt == 7:
            profil = 'arp'
        elif filt == 8:
            profil = 'custom'
            ether = raw_input('Enter Ethertype e.g. 0x800: ')
            nwproto = raw_input('Enter protocol number (protocol number in IPv4, header type in IPv6, opcode in ARP) or leave blank for none: ')
        else:
            print 'Something went horribly wrong.'
            exit()
    else:
        print 'That is not a valid selection; restarting add rule'
        addrule()
    print '''Add rule timout?
            1 - No
            2 - Hard Timeout
            3 - Idle Timeout'''
    xsel = raw_input('Enter the number of your selection: ')
    if xsel == '':
        xsel = 1
    selx = xsel
    if int(xsel) >= 1 and int(xsel) <= 3:
        selx = int(xsel)
        if selx == 1:
            extra = ''
        elif selx == 2: #Does this work?
            time = raw_input('Enter the time in seconds for the rule to exist: ')
            extra = 'hard_timeout=', time
        elif selx == 3:
            time = raw_input('Enter the time in seconds for the rule to exist while not idle: ')
            extra = 'idle_timeout=', time
        else:
            print 'Something went horribly wrong.'
            exit()
    else:
        print 'That is not a valid selection; defaulting to no timout.'
    ruleaction = raw_input('Enter the desired output actions separated by commas; order matters - imporoper syntax will cause add rule to fail: ')
    if matchtraf != 3 and filt == 1:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf == 3 and filt == 1:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf != 3 and filt == 2:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf == 3 and filt == 2:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf != 3 and filt == 3:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[tcp_src]': tcpsrc, 'match[tcp_dst]': tcpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf == 3 and filt == 3:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[tcp_src]': tcpsrc, 'match[tcp_dst]': tcpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf != 3 and filt == 4:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[udp_src]': udpsrc, 'match[udp_dst]': udpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf == 3 and filt == 4:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[sctp_src]': sctpsrc, 'match[sctp_dst]': sctpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf != 3 and filt == 5:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[sctp_src]': sctpsrc, 'match[sctp_dst]': sctpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf == 3 and filt == 5:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[udp_src]': udpsrc, 'match[udp_dst]': udpdst, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf != 3 and filt == 6:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[icmp_type]': icmpt, 'match[icmp_code]': icmpc, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf == 3 and filt == 6:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[nw_src]': nwsrc, 'match[nw_dst]': nwdst, 'match[icmp_type]': icmpt, 'match[icmp_code]': icmpc, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf != 3 and filt == 7:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf == 3 and filt == 7:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf != 3 and filt == 8:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[dl_type]': ether, 'match[nw_proto]': nwproto, 'match[match_extra]': extra, 'actions': ruleaction}
    elif matchtraf == 3 and  filt == 8:
        params = {'name': rulename, 'description': ruledescrip, 'priority': priority, 'match[in_port]': portin, 'match[vlan]': matchvlan, 'match[vlan_id]': matchid, 'match[vlan_priority]': vpri, 'match[dl_src]': macsrc, 'match[dl_dst]': macdst, 'match[protocol]': profil, 'match[dl_type]': ether, 'match[nw_proto]': nwproto, 'match[match_extra]': extra, 'actions': ruleaction}
    else:
        print 'Something went horribly wrong.'
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
    topmenu()

#Export a save point from the Packetmaster
def exportsp(): #Write code to save object accompanying response to file
    rspname = raw_input('What is the name of the rule save point to export? (leave blank for none): ')
    pspname = raw_input('What is the name of the port save point to export? (leave blank for none): ')
    url = ip + spexport + auth
    params = {'ruleSavePointNames': rspname, 'portSavePointNames': pspname}
    try:
        response = requests.get(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
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
    except:
        print 'Device is unavailable'
    topmenu()

#Reboot the Packetmaster
def reboot():
    url = ip + reboot + auth
    try:
        requests.post(url)
        print 'Device is rebooting...please allow 2 to 3 minutes for it to complete'
    except:
        print 'Unable to reboot device'
    topmenu()

topmenu()
