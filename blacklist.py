#Use with firmware version 2.1.0.x or later. Python2.7 Cubro Packetmaster Blacklist REST API demo.  Written by Derek Burke 12/2016
#Import necessary Python libraries for interacting with the REST API
import urllib, requests, json, re
from getpass import getpass
from requests.exceptions import ConnectionError

#Drop the retrieved IPs on the Packetmaster
def createblacklist(match, uri, auth):
    count = 0
    priority = 65536
    for m in match:
        print m
        count += 1
        priority -= 1
        connection = uri + auth
        rulename = 'Auto Blacklist ' + str(count)
        rulepriority = str(priority)
        params = {
            'name': rulename,
            'description': 'This rule was created by blacklist.py',
            'priority': rulepriority,
            'match[in_port]': '1,2',
            'match[protocol]': 'ip',
            'match[nw_src]': m,
            'match[extra]': 'idle_timeout=65535',
            'actions': 'drop'
        }
        try:
            response = requests.post(connection, data=params)
            print response.status_code
            r = response.content
            data = json.loads(r)
            print json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            print 'Device is unavailable \n'

if __name__ == '__main__':
    #IP address to access REST data of device
    deviceip = raw_input('What is the IP address of the Packetmaster you want to apply the black list to?: ')
    uri = 'http://' + deviceip + '/rest/rules?'
    #Device credentials
    username = raw_input('Enter your username: ')
    password = getpass()
    auth = urllib.urlencode({
        'username': username,
        'password': password
    })
    try:
        blacklist = urllib.urlopen('https://isc.sans.edu/block.txt?').read()
        text = blacklist.rstrip()
        for l in text:
            match = re.findall('(\S[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+)', text)
    except:
        print 'Site is unavailable \n'
    createblacklist(match, uri, auth)
