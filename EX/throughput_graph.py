#!/usr/bin/python

""" Use with firmware version 2.2.5 or later. Python2.7
Cubro Packetmaster REST API demo. This script will generate a graph
representing the overall bandwidth throughput of a Packetmaster at 1 hour
intervals over the course of a 24 hour period. """

#Import necessary Python libraries for interacting with the REST API
from getpass import getpass
import json
import time
import pygal
from packetmaster_ex_rest import PacketmasterEX


if __name__ == '__main__':
    #Device credentials
    ADDRESS = raw_input('Enter IP address of Packetmaster: ')
    USERNAME = raw_input('Enter your username: ')
    PASSWORD = getpass()
    PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
    DURATION = 24
    TITLE = ''
    INTERFACE = ''

    #Generate input/output octets line chart
    CHARTOCTETS = pygal.Line()
    CHARTOCTETS.title = TITLE + INTERFACE + ' Octets'
    CHARTOCTETS.x_labels = ['5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60']
    CHARTOCTETS.add('InOctets', in_octets_diff[1:24])
    CHARTOCTETS.add('OutOctets', out_octets_diff[1:24])
    CHARTOCTETS.render_to_file('octets.svg')
