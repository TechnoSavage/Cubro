#!/usr/bin/python

""" Use with firmware version 2.2.5 or later. Cubro
Packetmaster REST API demo. This script will generate a report at 12am daily
showing the peak traffic load on a per port basis. """

#Import necessary Python libraries for interacting with the REST API
from __future__ import print_function #Requires Python 2.6 or later
from getpass import getpass
import json
import time
import pickle
import yaml
from six import moves
from packetmaster_ex_rest import PacketmasterEX

def query(packetmaster):
    """ Query the Packetmaster for current port statistics. """
    stats = packetmaster.port_statistics()
    return stats

def parse(stats):
    """ Create a JSON formatted data table from Packetmaster port stats."""
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
    """ Compare previously saved port stat data to new data and replace lower
        values with higher ones. """
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
    """ Write the data held in 'current' to a file of type 'choice'. """
    report = current #make filename the date
    if choice == 1:
        save_file = open(report + '.pkl', "rb")
        pickle.load(save_file)
    elif choice == 2:
        with open(report + '.json') as save_file:
            json.load(save_file)
    elif choice == 3:
        with open(report + '.yml') as save_file:
            yaml.load(save_file)
    else:
        print("Something went horribly wrong")
        exit()

if __name__ == '__main__':
    #Device credentials
    ADDRESS = moves.input('Enter IP address of Packetmaster: ')
    USERNAME = moves.input('Enter your username: ')
    PASSWORD = getpass()
    PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
    print('''Save data in which format?
	1 - Pickle
	2 - JSON
	3 - YAML \n''')
    OPTION = moves.input("Enter the number of your selection: ")
    if int(OPTION) >= 1 and int(OPTION) <= 3:
        CHOICE = int(OPTION)
    else:
        print("That is not a valid choice; defaulting to Pickle")
        CHOICE = 1
    CURRENT = {}
    MARKER = False #MARKER is to ensure that file is written only once
                   #during each occurrence of 12:00

    while True:
        STATS = query(PACKETMASTER)
        TABLE = parse(STATS)
        CURRENT = compare(TABLE, CURRENT)
        if time == "12:00" and not MARKER: #MARKER as false means no file is yet written
            write_file(CHOICE, CURRENT)    #for this occurrence of 12:00 so stats can be 
            MARKER = True                  #written to file
        elif time == "12:00" and MARKER:   #Queries continue through the minute of 12:00
            pass                           #MARKER TRUE prevents file write
        elif time != "12:00" and MARKER:   #When minute no longer equals 12:00 remove 
            MARKER = False                 #MARKER to start cycle over again
        else:
            pass
