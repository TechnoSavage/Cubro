#Drop SMB traffic script.  Drop SMB traffic starting at a specified time for a duration of time.
#Use with firmware version 2.1.0.x or later. Python2.7.
#!/usr/bin/python

#Import necessary libraries
import requests, json, time
from getpass import getpass
from datetime import datetime
from requests.exceptions import ConnectionError

#Check system time
def checktime(address, username=None, password=None):
    currenttime = datetime.now().strftime('%H:%M')
    # print currenttime
    if str(currenttime) == '01:00': #Edit this time to match your use case
        try:
            addrule(address, username, password)
        except ConnectionError as e:
            r = 'No Response'
            raise e

def addrule(address, username=None, password=None):
    uri = 'http://' + address + '/rest/rules?'
    params = {"name": "dropsmb temporary",
    "description": "This rule will drop SMB traffic for the specified duration",
    "priority": 65535, "match[in_port]": "1",
    "match[protocol]": "tcp",
    "match[tcp_dst]": "445",
    "match[match_extra]": "hard_timeout=43200",
    "actions": "drop"}
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        # print response.status_code
        r = response.content
        data = json.loads(r)
        return json.dumps(data, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        raise e
    addruletwo()

def addruletwo(address, username=None, password=None):
        uri = 'http://' + address + '/rest/rules?'
        params = {"name": "dropsmb temporary",
        "description": "This rule will drop SMB traffic for the specified duration",
        "priority": 65535,
        "match[in_port]": "2",
        "match[protocol]": "tcp",
        "match[tcp_dst]": "445",
        "match[match_extra]": "hard_timeout=43200",
        "actions": "drop"}
        try:
            response = requests.post(uri, data=params, auth=(uername, password))
            # print response.status_code
            r = response.content
            data = json.loads(r)
            return json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            raise e

if __name__ == '__main__':
    deviceip = raw_input('What is the IP address of the Packetmaster you want to access: ')
    username = raw_input('Username for Packetmaster if required: ')
    password = getpass()

    while True:
        checktime(address, username, password)
        time.sleep(30)
