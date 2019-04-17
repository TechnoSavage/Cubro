#!/usr/bin/python
''' For testing port masking on packetmasters; creates 1000 TCP filters
    for source ports 1000 through 1999.'''

import json
from sys import argv
import requests
from requests.exceptions import ConnectionError

def usage():
    ''' Explain use of script.'''
    print ''' Supply arguments IP address, Username, and Password.
              e.g. mask_test.py 192.168.1.200 admin cubro'''

def rules(ip, user=None, passwd=None):
    ''' Add rules for port mask test.'''
    uri = 'http://' + ip + '/rest/rules?'
    for n in range(1000, 2000):
        params = {'priority': 32768,
                  'in_port': '1',
                  'match[vlan]': 'neg_match',
                  'match[protocol]': 'tcp',
                  'match[nw_src]': '',
                  'match[tcp_src]': n,
                  'actions': 'output:4'}
        try:
            response = requests.post(uri, data=params, auth=(user, passwd))
            content = response.content
            data = json.loads(content)
            print json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

if __name__ == "__main__":
    if len(argv) == 0:
        usage()
    else:
        IP, USER, PASSWD = argv
        rules(IP, USER, PASSWD)
