#Python2.7 Cubro Copper Bypass Switch REST API demo.
#Import necessary Python libraries for interacting with the REST API
import requests, json
from requests.exceptions import ConnectionError
from bypassswitch_rest import BypassSwitch

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
            mgmt = bypass.set_config_guided()
        elif int(choice) == 5:
            address = raw_input('Enter the IP Address of the Bypass Switch you want to manage: ')
        elif int(choice) == 6:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid choice"
        menu()

    menu()
