#Python2.7 Cubro Copper Bypass Switch REST API demo.  Written by Derek Burke 12/2016
#Import necessary Python libraries for interacting with the REST API
import requests, json
from requests.exceptions import ConnectionError

class BypassSwitch(object):
    
        def __init__(self, address):
            self.address = address
#Function to engage the bypass
        def engage(self):
            uri = 'http://' + self.address + '/takeDown?'
            try:
                response = requests.get(uri)
                code = response.status_code
                r = response.content
                return code
            except ConnectionError as e:
                r = 'No Response'
                raise e

        #Function to disengage the bypass
        def disengage(self):
            uri = 'http://' + self.address + '/takeUp?'
            try:
                response = requests.get(uri)
                code = response.status_code
                r = response.content
                return code
            except ConnectionError as e:
                r = 'No Response'
                raise e

        #Function to disengage bypass for timeout period
        def timeout(self):
            uri = 'http://' + self.address + '/setTimeout?'
            try:
                response = requests.get(uri)
                code = response.status_code
                r = response.content
                return code
            except ConnectionError as e:
                r = 'No Response'
                raise e

        #Function to change Management IP
        def set_config(self):
            ipadd = raw_input("Enter the Management IP Address; leave blank for factory default 192.168.0.201: ")
            if len(ipadd) <= 0:
                ipadd = '192.168.0.201'
            sub = raw_input("Enter the Subnet Mask; leave blank for a default Mask of 255.255.255.0: ")
            if len(sub) <= 0:
                sub = '255.255.255.0'
            gw = raw_input("Enter the Managment Default Gateway; leave blank for default of 192.168.0.1: ")
            if len(gw) <= 0:
                gw = '192.168.0.1'
            mac = raw_input("Enter a new MAC Address; leave blank for default: ")
            if len(mac) <= 0:
                mac = 'D8-20-9F-00-01-64'
            to = raw_input("Enter a Timeout; leave blank for a default timeout of 10: ")
            if len(to) <= 0:
                to = '10'
            uri = 'http://' + self.address + '/setConfig?'
            try:
                params = {
                'ip': ipadd,
                'subnet': sub,
                'gateway': gw,
                'mac': mac,
                'timeout': to
                }
                response = requests.post(uri, data=params)
                code = response.status_code
                r = response.content
                return code
            except ConnectionError as e:
                r = 'No Response'
                raise e

if __name__ == '__main__':
    #Print welcome statement
    print 'Welcome to the Cubro Bypass Switch REST Demo\n'
    #Define IP address of the Bypass Switch
    address = raw_input('Enter the IP Address of the Bypass Switch you want to manage: ')
    bypass = BypassSwitch(address)
    #Main menu
    def menu():
        global address
        print '\nWorking with Bypass Switch at', address,'\n'
        print '''Make Selection:
                1 - Engage Bypass
                2 - Disengage Bypass
                3 - Timeout
                4 - Set Management Configuration
                5 - Change working device
                6 - Quit\n'''
        choice = raw_input('Enter the number of your selection: ')
        #Evaluate user selection
        if int(choice) == 1:
            on = bypass.engage()
            print on
        elif int(choice) == 2:
            off = bypass.disengage()
            print off
        elif int(choice) == 3:
            timeout = bypass.timeout()
            print timeout
        elif int(choice) == 4:
            mgmt = bypass.set_config()
        elif int(choice) == 5:
            address = raw_input('Enter the IP Address of the Bypass Switch you want to manage: ')
        elif int(choice) == 6:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid choice"
        menu()

    menu()
