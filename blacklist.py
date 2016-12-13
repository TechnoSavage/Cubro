#Use with firmware version 2.0.0.x or earlier. Python2.7 Cubro Packetmaster Blacklist REST API demo.  Written by Derek Burke 12/2016
#Import necessary Python libraries for interacting with the REST API
import urllib, requests, json
from requests.exceptions import ConnectionError

#IP address to access REST data of device
deviceip = raw_input('What is the IP address of the Packetmaster you want to apply the black list to?: ')
ip = 'http://' + deviceip + '/rest'
#Device credentials
username = raw_input('Enter your username: ')
password = raw_input('Enter your password: ')
auth = urllib.urlencode({
    'username': username,
    'password': password
})

try:
    blacklist = urllib.urlopen('https://isc.sans.edu/block.txt?').read()
    print blacklist
except:
    print 'Device is unavailable \n'
