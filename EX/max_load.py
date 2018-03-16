#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#This script will generate a report at 12am daily showing the peak traffic load on a per
#port basis

#!/usr/bin/python

#Import necessary Python libraries for interacting with the REST API
import json, time, pickle, yaml
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX

def query(packetmaster):
    stats = packetmaster.port_statistics()
    return stats

def parse(stats)

if __name__ == '__main__':
    #Device credentials
    address = raw_input('Enter IP address of Packetmaster: ')
    username = raw_input('Enter your username: ')
    password = getpass()
    packetmaster = PacketmasterEX(address, username, password)
    count = packetmaster.ports()
    print '''Save data in which format?
	1 - Pickle
	2 - JSON
	3 - YAML \n'''
	option = raw_input("Enter the number of your selection: ")
	if int(option) >=1 and int(option) <=3:
		choice = int(option)
	else:
		print "That is not a valid choice; defaulting to Pickle"
		choice = 1
    duration = 24

    if choice == 1:
        f = open(n + '.pkl', "rb")
        a = pickle.load(f)
    elif choice == 2:
        with open(n + '.json') as f:
            a = json.load(f)
    elif choice == 3:
        with open(n + '.yml') as f:
            a = yaml.load(f)
    else:
        print "Something went horribly wrong"
        exit()

    while true:
        # if time in range x and marker false:
        #     save reset
        #     set marker
        # else:
        #     unset marker
        stats = query(packetmaster)
        table = parse(stats)
