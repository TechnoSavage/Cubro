#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#This script will generate a graph representing the overall bandwidth throughput of
#a Packetmaster at 1 hour intervals over the course of a 24 hour period.

#!/usr/bin/python

#Import necessary Python libraries for interacting with the REST API
import json, time, pygal
from getpass import getpass
from packetmaster_ex_rest import PacketmasterEX


if __name__ == '__main__':
    #Device credentials
    address = raw_input('Enter IP address of Packetmaster: ')
    username = raw_input('Enter your username: ')
    password = getpass()
    packetmaster = PacketmasterEX(address, username, password)
    duration = 24
    title = ''
    interface = ''

    #Generate input/output octets line chart
	chartoctets = pygal.Line()
	chartoctets.title = title + interface + ' Octets'
	chartoctets.x_labels = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
	chartoctets.add('InOctets', in_octets_diff[1:24])
	chartoctets.add('OutOctets', out_octets_diff[1:24])
	chartoctets.render_to_file('octets.svg')
