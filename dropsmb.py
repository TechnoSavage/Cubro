#Drop SMB traffic script.  Drop SMB traffic starting at a specified time for a duration of time.
#Use with firmware version 2.0.0.x or earlier. Python2.7.  Written by Derek Burke 12/2016
#Import necessary libraries
import urllib, requests, json, time
from datetime import datetime
from requests.exceptions import ConnectionError

#IP address to access REST data of device
deviceip = raw_input('What is the IP address of the Packetmaster you want to access: ')
ip = 'http://' + deviceip + '/rest'
#Device credentials
username = raw_input('Enter your username: ')
password = raw_input('Enter your password: ')
auth = urllib.urlencode({
    'username': username,
    'password': password
})

#Options to append to device url
rule = '/flows?'

#Check system time
def checktime():
    currenttime = datetime.now().strftime('%H:%M')
    print currenttime
    if str(currenttime) == '11:39':
        try:
            addrule()
        except ConnectionError as e:
            r = 'No Response'
            print 'Device is unavailable \n'

def addrule():
    url = ip + rule + auth
    params = {"name": "dropsmb temporary",
    "description": "This rule will drop SMB traffic for the duration from 5:00PM to 5:00AM",
    "priority": "65535", "match[in_port]": "1",
    "match[protocol]": "tcp",
    "match[tcp_dst]": "445",
    "match[match_extra]": "hard_timeout=43200",
    "actions": "drop"}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    addruletwo()

def addruletwo():
        url = ip + rule + auth
        params = {"name": "dropsmb temporary",
        "description": "This rule will drop SMB traffic for the specified duration",
        "priority": "65535",
        "match[in_port]": "2",
        "match[protocol]": "tcp",
        "match[tcp_dst]": "445",
        "match[match_extra]": "hard_timeout=43200",
        "actions": "drop"}
        try:
            response = requests.post(url, data=params)
            print response.status_code
            r = response.content
            data = json.loads(r)
            print json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            print 'Device is unavailable \n'

while True:
    checktime()
    time.sleep(30)
