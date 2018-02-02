#Use with firmware version 2.1.0.x or later. Python2.7 Cubro Packetmaster Blacklist REST API demo.
#Import necessary Python libraries for interacting with the REST API

#!/usr/bin/python

import requests, json, re
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX
from requests.exceptions import ConnectionError

#Drop the retrieved IPs on the Packetmaster
def createblacklist(match, pm, interface):
    count = 0
    priority = 65536
    for m in match:
        print m
        count += 1
        priority -= 1
        rulename = 'Auto Blacklist ' + str(count)
        rulepriority = str(priority)
        params = {
            'name': rulename,
            'description': 'This rule was created by blacklist.py',
            'priority': rulepriority,
            'match[in_port]': interface,
            'match[protocol]': 'ip',
            'match[nw_src]': m + '/24',
            'match[extra]': 'idle_timeout=65535',
            'actions': 'drop'
        }
        pm.add_rule(params)

if __name__ == '__main__':
    address = raw_input('IP address of Packetmaster to apply blacklist to: ')
    username = raw_input('Username for Packetmaster: ')
    password = getpass()
    pm = PacketmasterEX(address, username, password)
    interface = raw_input(""""What is(are) the port number(s) or range of ports on which to block malicious IPs?
                              e.g. '5' or '1,2,5' or '5-10': """)
    print "Retrieving malicious IP list from sans.edu."
    try:
        blacklist = requests.get('https://isc.sans.edu/block.txt?').text
        text = blacklist.rstrip()
        match = re.findall('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', text)
    except ConnectionError as e:
        print 'Site is unavailable \n'
        exit()
    createblacklist(match, pm, interface)
