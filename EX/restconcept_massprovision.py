#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Shows conceptually how the ReST API can  be used to mass provision a set of devices and/or apply a preset
# baseline configuration from a savepoint file

#!/usr/bin/python

#Import necessary Python libraries
import json, time, sys, re
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX

def usage():
    print """Usage:
             -r, --read <file name> Use a list of IP addresses from a text file to provision Packetmasters.
             -l, --list <ip address> <ip address> Enter IP addresses separated by spaces to provision Packetmasters.
             -sr, --saveread <savepoint name> <file name> Specify a save point file to upload
                              and a list of IP addresses from a text file to provision Packetmasters.
             -sl, --savelist <savepoint name> <file name> Specify a save point file to upload
                              and enter IP addresses separated by spaces to provision Packetmasters.

             This script will apply a preset baseline configuration to each Packetmaster IP address provided.
             This script assumes that the Packetmasters do not have UAC enabled."""

def apply_save(ip_list, savename=None):
    #Iterate over IP list and set baseline config for each IP

if __name__ == '__main__':
    if len(sys.argv) == 3 and str(sys.argv[1]) == '-r' or len(sys.argv) == 3 and str(sys.argv[1]) == '--read':
        filename = sys.argv[2]
        text = filename.rstrip()
        ip_list = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', text)
        run = apply_save(ip_list)
        print run
    elif len(sys.argv) > 1 and str(sys.argv[1]) == '-l' or len(sys.argv) > 1 and str(sys.argv[1]) == '--list':
        ip_list = sys.argv[2:]
        run = apply_save(ip_list)
        print run
    elif len(sys.argv) == 4 and str(sys.argv[1]) == '-sr' or len(sys.argv) == 4 and str(sys.argv[1]) == '--saveread':
        savename = sys.argv[2]
        filename = sys.argv[3]
        text = filename.rstrip()
        ip_list = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', text)
        run = apply_save(ip_list, savename)
        print run
    elif len(sys.argv) > 1 and str(sys.argv[1]) == '-sl' or len(sys.argv) > 1 and str(sys.argv[1]) == '--savelist':
        savename = sys.argv[2]
        ip_list = sys.argv[3:]
        run = apply_save(ip_list, savename)
        print run
    else:
        usage()
