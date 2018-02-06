#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Shows conceptually how the ReST API can  be used to mass provision a set of devices.

#!/usr/bin/python

#Import necessary Python libraries
import json, time, sys, re
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX

def usage():
    print """Usage:
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

             This script will apply a preset baseline configuration to each Packetmaster IP address provided."""

def apply_config(device_ip, admin_user=None, admin_password=None):
    for address in ip_list:
        ex = PacketmasterEX(address, admin_user, admin_password)
        #Enter ReST API calls for configuration below this line.  See packetmasterEX_rest object class for methods.
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

if __name__ == '__main__':
    if len(sys.argv) == 3 and str(sys.argv[1]) in ('-f', '--filename'):
        filename = sys.argv[2]
        device_list = []
        with open(filename) as f:
            device_file = json.load(f)
            for item in device_file["packetmaster"]:
                ip = item["ip"]
                admin_user = item["admin"]
                admin_password = item["passwd"]
                run = apply_config(ip, admin_user, admin_password)
                print run
    elif len(sys.argv) > 1 and str(sys.argv[1]) in ('-l', '--list'):
        if '-u' in sys.argv or '--username' in sys.argv:
            admin_user = raw_input("Administrator Username: ")
            admin_pass = getpass()
        ip_list = sys.argv[2:]
        addresses = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', sys.argv)
        for ip in addresses:
            if admin_user:
                run = apply_config(ip, admin_user, admin_pass)
            else:
                run = apply_config(ip)
            print run
    else:
        usage()
