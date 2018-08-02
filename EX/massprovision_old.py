#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Shows conceptually how the ReST API can  be used to mass provision a set of devices and/or apply a preset
# baseline configuration from a savepoint file

#!/usr/bin/python

#Import necessary Python libraries
import json, time, sys, re
from getpass import getpass
from packetmaster_ex_rest import PacketmasterEX

def usage():
    print """Usage:
             -r, --read FILE   Use a list of IP addresses from a text file to provision Packetmasters.
             -l, --list 192.168.1.2 [192.168.1.3][...]   Enter IP addresses separated by spaces to
                                                         provision Packetmasters.

             This script will apply a preset baseline configuration to each Packetmaster IP address provided.
             This script assumes that the Packetmasters do not have UAC enabled."""

             #  -sr, --saveread <savepoint name> <file name> Specify a save point file to upload
             #                   and a list of IP addresses from a text file to provision Packetmasters.
             #  -sl, --savelist <savepoint name> <file name> Specify a save point file to upload
             #                   and enter IP addresses separated by spaces to provision Packetmasters.

def apply_config(ip_list, savename=None):
    for address in ip_list:
        pm = PacketmasterEX(address)
        if savename:
            pass
        #Enter ReST calls for configuration below this line
        pm.set_port_config('1', '10G', 'full', False, False, False)
        pm.set_port_config('2', '10G', 'full', False, False, False)
        pm.set_port_config('3', '10G', 'full', False, False, False)
        pm.set_port_config('4', '10G', 'full', False, False, False)
        pm.add_rule({'name': '1 & 2 to 3',
                     'description': 'Inbound traffic on ports 1 and 2 is output on port 3',
                     'priority': 32768,
                     'match[in_port]': '1,2',
                     'actions': '3'})
        pm.add_rule({'name': '10.0.0.5 to 4',
                     'description': 'Filter IP 10.0.0.5 out of inbound traffic on ports 1 and 2 and output on port 4; reinsert into traffic on port 3',
                     'priority': 50000,
                     'match[in_port]': '1,2',
                     'match[protocol]': 'ip',
                     'match[nw_src]': '10.0.0.5',
                     'actions': '3,4'})
        pm.start_app_ntp('0.north-america.pool.ntp.org', '', 'Use pool.ntp.org for NTP')
        pm.set_hash_algorithms(False, False, False, False, True, True, True, True)
        pm.set_rule_permanence('y')
        pm.add_user('Bob', '7', 'bobby boy!', 'Network Engineer', False)
        pm.set_dns('9.9.9.9', '8.8.8.8', '8.8.4.4')
        pm.set_uac('t')

if __name__ == '__main__':
    if len(sys.argv) == 3 and str(sys.argv[1]) == '-r' or len(sys.argv) == 3 and str(sys.argv[1]) == '--read':
        filename = sys.argv[2]
        ip_list = []
        with open(filename, 'r') as f:
            for line in f:
                stuff = line.rstrip() #Provide capability to read usernames and passwords in order to use with UAC on
                ip = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', stuff)
                for item in ip:
                    ip_list.append(item)
        run = apply_config(ip_list)
        print run
    elif len(sys.argv) > 1 and str(sys.argv[1]) == '-l' or len(sys.argv) > 1 and str(sys.argv[1]) == '--list':
        ip_list = sys.argv[2:]
        run = apply_config(ip_list)
        print run
    # elif len(sys.argv) == 4 and str(sys.argv[1]) == '-sr' or len(sys.argv) == 4 and str(sys.argv[1]) == '--saveread':
    #     savename = sys.argv[2]
    #     filename = sys.argv[3]
    #     text = filename.rstrip()
    #     ip_list = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', text)
    #     run = apply_save(ip_list, savename)
    #     print run
    # elif len(sys.argv) > 1 and str(sys.argv[1]) == '-sl' or len(sys.argv) > 1 and str(sys.argv[1]) == '--savelist':
    #     savename = sys.argv[2]
    #     ip_list = sys.argv[3:]
    #     run = apply_save(ip_list, savename)
    #     print run
    else:
        usage()
