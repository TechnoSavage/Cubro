#Use with firmware version 2.1.0.x or later. Python2.7 Cubro Packetmaster Blacklist REST API demo.
#Import necessary Python libraries for interacting with the REST API
#!/usr/bin/python
import requests, json, re
from getpass import getpass
from requests.exceptions import ConnectionError

#Drop the retrieved IPs on the Packetmaster
def createblacklist(match, address, username=None, password=None):
    uri = 'http://' + address + '/rest/rules?'
    count = 0
    priority = 65536
    for m in match:
        print m
        count += 1
        priority -= 1
        rulename = 'Auto Blacklist ' + str(count)
        rulepriority = str(priority)
        params = {
            'name': rulename,
            'description': 'This rule was created by blacklist.py',
            'priority': rulepriority,
            'match[in_port]': '1,2',
            'match[protocol]': 'ip',
            'match[nw_src]': m + '/24',
            'match[extra]': 'idle_timeout=65535',
            'actions': 'drop'
        }
        try:
            response = requests.post(uri, data=params, auth=(username, password))
            print response.status_code
            r = response.content
            data = json.loads(r)
            print json.dumps(data, indent=4)
        except ConnectionError as e:
            r = 'No Response'
            return e

if __name__ == '__main__':
    address = raw_input('What is the IP address of the Packetmaster you want to apply the black list to?: ')
    username = raw_input('Enter your username: ')
    password = getpass()
    try:
        blacklist = requests.get('https://isc.sans.edu/block.txt?').text
        text = blacklist.rstrip()
        for l in text:
            #match = re.findall('(\S[0-9]+[.][0-9]+[.][0-9]+[.][0-9]+)', text)
            match = re.findall('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', text)
    except:
        print 'Site is unavailable \n'
    createblacklist(match, address, username, password)
