#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#This script will generate a report at 12am daily showing the peak traffic load on a per
#port basis

#!/usr/bin/python

#Import necessary Python libraries for interacting with the REST API
import json, time, pickle, yaml
from getpass import getpass
from packetmaster_ex_rest import PacketmasterEX

def query(packetmaster):
    stats = packetmaster.port_statistics()
    return stats

def parse(stats):
    table = {}
    data = json.loads(stats)
    for item in data:
        portnum = item["portnum"]
        txrate = item["txrate"]
        rxrate = item["rxrate"]
        table[portnum] = {"txrate": txrate,
                          "rxrate": rxrate}
    return table

def compare(table, current):
    for item in table:
        portnum = item["portnum"]
        if portnum not in current:
            txrate = item["txrate"]
            rxrate = item["rxrate"]
            current[portnum] = {"txrate": txrate,
                                "rxrate": rxrate}
        else:     #This must account for kb/s, mb/s, and gb/s
            if item["txrate"] > current[portnum]["txrate"]:
                current[portnum]["txrate"] = item["txrate"]
            if item["rxrate"] > current[portnum]["rxrate"]:
                current[portnum]["rxrate"] = item["rxrate"]
    return current

def write_file(choice, current):
    report = current #make filename the date
    if choice == 1:
        f = open(report + '.pkl', "rb")
        a = pickle.load(f)
    elif choice == 2:
        with open(report + '.json') as f:
            a = json.load(f)
    elif choice == 3:
        with open(report + '.yml') as f:
            a = yaml.load(f)
    else:
        print "Something went horribly wrong"
        exit()

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
    current = {}
    marker = False

    while True:
        stats = query(packetmaster)
        table = parse(stats)
        current = compare(table, current)
        if time == "12:00" and marker == False:
            write_file(choice, current)
            marker = True
        elif time == "12:00" and marker == True:
            pass
        elif time != "12:00" and marker == True:
            marker = False
        else:
            pass
