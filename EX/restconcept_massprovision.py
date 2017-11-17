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
             -r, --read <savepoint name> <file name> Use a list of IP addresses from a text file to provision Packetmasters with a specified save point file.
             -l, --list <savepoint name> <ip address> <ip address> Enter IP addresses separated by spaces to provision Packetmasters with a specified save point file.

             This script will apply a preset baseline configuration to each Packetmaster IP address provided.
             This script assumes that the Packetmasters do not have UAC enabled."""

def apply_save(savename, ip_list):
    #Iterate over IP list and upload and set savepoint

if __name__ == '__main__':
    if len(sys.argv) == 4 and str(sys.argv[1]) == '-r' or len(sys.argv) == 4 and str(sys.argv[1]) == '--read':
        savename = sys.argv[2]
        filename = sys.argv[3]
        text = filename.rstrip()
        ip_list = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', text)
        run = apply_save(savename, ip_list)
        print run
    elif len(sys.argv) > 1 and str(sys.argv[1]) == '-l' or len(sys.argv) > 1 and str(sys.argv[1]) == '--list':
        savename = sys.argv[2]
        ip_list = sys.argv[3:]
        run = apply_save(savename, ip_list)
        print run
    else:
        usage()
