#!/usr/bin/python

""" Use with firmware version 2.2.5 or later.
Cubro Packetmaster Blacklist REST API demo. """

#Import necessary Python libraries for interacting with the REST API.
from __future__ import print_function #Requires Python 2.6 or later
from getpass import getpass
import re
import requests
from requests.exceptions import ConnectionError
from six import moves
from packetmaster_ex_rest import PacketmasterEX

def createblacklist(match, packet_master, interface):
    """Apply the IP rule filters on Packetmaster based on blacklist."""
    count = 0
    priority = 65536
    for ip_address in match:
        print(ip_address)
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
            'match[nw_src]': ip_address + '/24',
            'match[extra]': 'idle_timeout=65535',
            'actions': 'drop'
        }
        packet_master.add_rule(params)

if __name__ == '__main__':
    ADDRESS = moves.input('IP address of Packetmaster to apply blacklist to: ')
    USERNAME = moves.input('Username for Packetmaster: ')
    PASSWORD = getpass()
    PM = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
    INTERFACE = moves.input("""What is(are) the port number(s) or range of ports
                            on which to block malicious IPs?
                            e.g. '5' or '1,2,5' or '5-10': """)
    print("Retrieving malicious IP list from sans.edu.")
    try:
        BLACKLIST = requests.get('https://isc.sans.edu/block.txt?').text
        TEXT = BLACKLIST.rstrip()
        MATCH = re.findall('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', TEXT)
    except ConnectionError as error:
        print('Site is unavailable \n')
        exit()
    createblacklist(MATCH, PM, INTERFACE)
