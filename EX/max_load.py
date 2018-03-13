#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#This script will generate a report showing the peak traffic load per port on a Packetmaster
#over a 24 hour period.

#!/usr/bin/python

#Import necessary Python libraries for interacting with the REST API
import json, time, pickle, yaml
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX

if __name__ == '__main__':
    #Device credentials
    address = raw_input('Enter IP address of Packetmaster: ')
    username = raw_input('Enter your username: ')
    password = getpass()
    packetmaster = PacketmasterEX(address, username, password)
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
