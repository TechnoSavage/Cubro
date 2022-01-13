#!/usr/bin/python

""" Use with firmware version 2.2.5 or later.
Cubro Packetmaster REST API demo. Shows conceptually how the ReST API can
be used to mass provision a set of devices."""

#Import necessary Python libraries
from __future__ import print_function #Requires Python 2.6 or later
import json
import sys
import re
from getpass import getpass
from six import moves
from packetmaster_ex_rest import PacketmasterEX

def usage():
    """ Display usage and help. """
    print("""Usage:
             -f, --filename FILE   Provide a JSON formatted text file of device IPs and admin credentials
                                   that the configuration should be applied to.
                                 Format:
                                 {
                                   "packetmaster": [
                                     {"ip": "192.168.0.2", "admin": "username", "passwd": "password"},
                                     {"ip": "192.168.0.3", "admin": "username", "passwd": "password"}
                                     ]
                                 }
             -l, --list 192.168.1.2 [192.168.1.3][...]   Enter IP addresses separated by spaces to
                                                         provision Packetmasters. If UAC is enabled
                                                         must provide -u option (see -u).
             -u, --username   Tells the script to prompt for an admin username and password for the
                              IP addresses passed to -l option.

             This script will apply a preset baseline configuration to each
             Packetmaster IP address provided.""")

def apply_config(device_ip, admin_username=None, password=None):
    """ Applies all 'PacketmasterEX' method calls listed to Packetmaster device.
        See packetmaster_ex_rest object class for methods. """
    ex = PacketmasterEX(device_ip, admin_username, password)
    #Enter ReST API calls for configuration below this line.
    ex.set_port_config('1', '10G', 'full', False, False, False)
    ex.set_port_config('2', '10G', 'full', False, False, False)
    ex.set_port_config('3', '10G', 'full', False, False, False)
    ex.set_port_config('4', '10G', 'full', False, False, False)
    ex.add_rule({'name': '1 & 2 to 3',
                 'description': 'Inbound traffic on ports 1 and 2 is output on port 3',
                 'priority': 32768,
                 'match[in_port]': '1,2',
                 'actions': '3'})
    ex.add_rule({'name': '10.0.0.5 to 4',
                 'description': 'Filter IP 10.0.0.5 out of inbound traffic on ports 1 and 2 and output on port 4; reinsert into traffic on port 3',
                 'priority': 50000,
                 'match[in_port]': '1,2',
                 'match[protocol]': 'ip',
                 'match[nw_src]': '10.0.0.5',
                 'actions': '3,4'})
    ex.start_app_ntp('0.north-america.pool.ntp.org', '', 'Use pool.ntp.org for NTP')
    ex.set_hash_algorithms(False, False, False, False, True, True, True, True)
    ex.set_rule_permanence('y')
    ex.add_user('Bob', '7', 'bobby boy!', 'Network Engineer', False)
    ex.add_user('Jim', '7', 'Jimminy Cricket', 'Security Guy', False)
    ex.set_dns('9.9.9.9', '149.112.112.112')
    ex.set_uac('t')
    return "Configuration Applied."

if __name__ == '__main__':
    if len(sys.argv) == 3 and str(sys.argv[1]) in ('-f', '--filename'):
        FILENAME = sys.argv[2]
        DEVICE_LIST = []
        with open(FILENAME) as f:
            DEVICE_FILE = json.load(f)
            for item in DEVICE_FILE["packetmaster"]:
                ip = item["ip"]
                admin_user = item["admin"]
                admin_password = item["passwd"]
                run = apply_config(ip, admin_user, admin_password)
                print(run)
    elif len(sys.argv) > 1 and str(sys.argv[1]) in ('-l', '--list'):
        if '-u' in sys.argv or '--username' in sys.argv:
            ADMIN_USER = moves.input("Administrator Username: ")
            ADMIN_PASS = getpass()
        IP_LIST = sys.argv[2:]
        for item in IP_LIST:
            address = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', item)
            if ADMIN_USER:
                run = apply_config(address[0], ADMIN_USER, ADMIN_PASS)
            else:
                run = apply_config(address[0])
            print(run)
    else:
        usage()
