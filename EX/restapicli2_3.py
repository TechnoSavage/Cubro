#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.

#!/usr/bin/python

#Import necessary Python libraries for interacting with the REST API
import requests, json, re
from getpass import getpass
from requests.exceptions import ConnectionError
from packetmasterEX_rest import PacketmasterEX
# Add code to handle case and verify input in all areas where needed

def set_ip():
    fail_count = 0
    while fail_count < 3:
        address = raw_input('What is the IP address of the Packetmaster you want to access?: ')
        try:
            ip_address = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', address)
            address = ip_address[0]
            return address
        except:
            print "That is not a valid IPv4 address."
            fail_count += 1
    print "That is not a valid IPv4 address.  Exiting"
    exit()

if __name__ == '__main__':
    #Welcome statement
    print '''
                ________  ______  ____  ____     _____  ______ _____ _______   ____   ____   __
               / ____/ / / / __ )/ __ \/ __ \   / __  \/ ____//  __//_  ___/  / __ \ / __ \ / /
              / /   / / / / /_/ / /_/ / / / /  / /_/  / __/  / /__   / /     / /_/ // /_/ // /
             / /___/ /_/ / /_/ / _, _/ /_/ /  / _,  _/ /___  \__  \ / /     / __  //  ___// /
             \____/\____/_____/_/ |_|\____/  /_/ \_\/_____//______//_/     /_/ /_//_/    /_/
           ###################################################################################
        \n'''

    #IP address to access REST data of device
    address = set_ip()
    #Device credentials
    username = raw_input('Enter your username: ')
    password = getpass()
    packetmaster = PacketmasterEX(address, username, password)

    #Initial menu to check or change settings
    def topmenu():
        global address, username, password, packetmaster
        print 'Options for device at', address,'acting as User', username
        print '''
            1 - Change My working device
            2 - Change My user credentials
            3 - Manage Device
            4 - Quit \n'''

        option = raw_input('Enter selection number: ')
        try:
            option = int(option)
        except:
            topmenu()
        if option == 1:
            address = set_ip()
            packetmaster = PacketmasterEX(address, username, password)
            topmenu()
        elif option == 2:
            username = raw_input('Username: ')
            password = getpass()
            packetmaster = PacketmasterEX(address, username, password)
            topmenu()
        elif option == 3:
            manage()
        elif option == 4:
            print 'Goodbye'
            exit()
        else:
            print 'That is not a valid selection \n'
            topmenu()

    def manage():
        print 'Device management menu for device at', address,'acting as User', username
        choice = raw_input('''
                  1 - Hardware Configuration Menu
                  2 - Rule and Port Group Configuration Menu
                  3 - App Configuration Menu
                  4 - Savepoint Configuration Menu
                  5 - User Management Menu
                  6 - Back \n
                 Enter the number of the selection to check: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            manage()
        if choice == 1:
            hardwareconfig()
        elif choice == 2:
            ruleconfig()
        elif choice == 3:
            appconfig()
        elif choice == 4:
            saveconfig()
        elif choice == 5:
            userconfig()
        elif choice == 6:
            topmenu()
        else:
            print "That is not a valid selection."
            manage()

    def hardwareconfig():
        print 'Hardware configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Model
                 2 - Serial Number
                 3 - Hardware Generation
                 4 - Firmware version
                 5 - Temperature and Fans
                 6 - ID LED Status
                 7 - ID LED on/off
                 8 - OS and CPU Load Averages
                 9 - TCAM Flows
                10 - Memory Usage
                11 - CCH Server Revision
                12 - Device Label and Notes Submenu
                13 - IP Configuration Submenu
                14 - DNS Configuration Submenu
                15 - Port Configuration Submenu
                16 - Telnet service submenu
                17 - Webserver Submenu
                18 - Reboot Packetmaster
                19 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            hardwareconfig()

    def notesmenu():
        print 'Device label and notes menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get Label and Notes
                 2 - Change Label only
                 3 - Change Label and Notes
                 4 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            notesmenu()

    def ipconfig():
        print 'Device label and notes menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get current IP configuration
                 2 - Change IP configuration
                 3 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            ipconfig()

    def dns():
        print 'DNS configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get current DNS configuration
                 2 - Change DNS configuration
                 3 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            dns()

    def portconfig():
        print 'Port configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get current port configuration
                 2 - Get current port status
                 3 - Get current port counters
                 4 - Get SFP status
                 5 - Change Port Configuration
                 6 - Shut Down or Activate Port
                 7 - Reset Port Counters
                 8 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            portconfig()

    def web():
        print 'Webserver menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Web logs
                 2 - Delete web Logs
                 3 - Restart webserver
                 4 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            web()
        if choice == 1:
            run = packetmaster.web_log()
            print run
            web()
        elif choice == 2:
            run = packetmaster.del_web_log()
            print run
            web()
        elif choice == 3:
            run = packetmaster.restart_webserver()
            print run
            web()
        elif choice == 4:
            hardwareconfig()
        else:
            print "That is not a valid selection."
            web()

    def telnet():
        print 'Telnet service menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get current Telnet status
                 2 - Enable or Disable Telnet service
                 3 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            telnet()
        if choice == 1:
            run = packetmaster.get_telnet()
            print run
            telnet()
        elif choice == 2:
            run = packetmaster.set_telnet_guided()
            print run
            telnet()
        elif choice == 3:
            hardwareconfig()
        else:
            print "That is not a valid selection."
            telnet()

    def ruleconfig():
        print 'Rule and Port Group configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Show Rules
                 2 - Add Rule
                 3 - Modify Rule
                 4 - Delete Rule
                 5 - Delete All Rules
                 6 - Reset Rule Counters
                 7 - Show Groups
                 8 - Add Group
                 9 - Modify Group
                10 - Delete Group
                11 - Delete all active groups and associated rules
                12 - Show Active Load-Balancing Hashes
                13 - Set Load Balancing Group Hash Algorithms
                14 - Permanence Mode
                15 - Rule Storage Mode
                16 - Reset Rule Counters
                17 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            ruleconfig()

    def appconfig():
        print 'App configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 -
                 2 -
                 3 -
                 4 -
                 5 -
                17 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            appconfig()

    def saveconfig():
        print 'Save Point configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 -
                 2 -
                 3 -
                 4 -
                 5 -
                17 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            saveconfig()

    def userconfig():
        print 'User configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 -
                 2 -
                 3 -
                 4 -
                 5 -
                17 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            userconfig()

topmenu()
