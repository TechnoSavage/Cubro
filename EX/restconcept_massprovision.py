#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Shows conceptually how the ReST API can  be used to mass provision a set of devices and/or apply a preset
# baseline configuration

#!/usr/bin/python

#Import necessary Python libraries
import json, time, sys, re
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX

def usage():
    print """Usage:
             -r, --read <file name> Use a list of IP addresses from a text file to provision Packetmasters.
             -l, --list <ip address> <ip address> Enter IP addresses separated by spaces to provision Packetmasters.

             This script will apply a preset baseline configuration to each Packetmaster IP address provided.
             This script assumes that the Packetmasters do not have UAC enabled."""

def read_file(filename):
    return filename
    #open file, regex search IP addresses, iterate over IPs and apply ReST commands

def iter_list(ip_list):
    return ip_list
    #Iterate over given IP addresses and apply ReST commands

if __name__ == '__main__':
    if len(sys.argv) == 3 and str(sys.argv[1]) == '-r' or len(sys.argv) == 3 and str(sys.argv[1]) == '--read':
        filename = sys.argv[2]
        run = read_file(filename)
        print run
    elif len(sys.argv) > 1 and str(sys.argv[1]) == '-l' or len(sys.argv) > 1 and str(sys.argv[1]) == '--list':
        ip_list = sys.argv[2:]
        run = iter_list(ip_list)
        print run
    else:
        usage()
