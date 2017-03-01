#Python2.7 Cubro Copper Bypass Switch REST API demo.  Written by Derek Burke 12/2016
#Import necessary Python libraries for interacting with the REST API
import urllib, requests, json
from requests.exceptions import ConnectionError

#Function to engage the bypass
def eng(url):
    try:
        response = requests.get(url + '/takeDown?')
        print response.status_code
        r = response.content
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Function to disengage the bypass
def dis(url):
    try:
        response = requests.get(url + '/takeUp?')
        print response.status_code
        r = response.content
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Function to disengage bypass for timeout period
def timeout(url):
    try:
        response = requests.get(url + '/setTimeout?')
        print response.status_code
        r = response.content
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Function to change Management IP
def mgmt(url):
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
    try:
        params = {
        'ip': ipadd,
        'subnet': sub,
        'gateway': gw,
        'mac': mac,
        'timeout': to
        }
        response = requests.post(url + '/setConfig?', data=params)
        print response.status_code
        r = response.content
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

if __name__ == '__main__':
    #Print welcome statement
    print 'Welcome to the Cubro Bypass Switch REST Demo\n'
    #Define IP address of the Bypass Switch
    ip = raw_input('Enter the IP Address of the Bypass Switch you want to manage: ')
    url = 'http://' + ip

    #Main menu
    def menu():
        global ip, url
        print '\nWorking with Bypass Switch at', ip,'\n'
        print '''Make Selection:
                1 - Engage Bypass
                2 - Disengage Bypass
                3 - Timeout
                4 - Change Management IP
                5 - Change working device
                6 - Quit\n'''
        choice = raw_input('Enter the number of your selection: ')
        #Evaluate user selection
        if int(choice) == 1:
            eng(url)
        elif int(choice) == 2:
            dis(url)
        elif int(choice) == 3:
            timeout(url)
        elif int(choice) == 4:
            mgmt(url)
        elif int(choice) == 5:
            ip = raw_input('Enter the IP Address of the Bypass Switch you want to manage: ')
            url = 'http://' + ip
        elif int(choice) == 6:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid choice"
        menu()

    menu()
