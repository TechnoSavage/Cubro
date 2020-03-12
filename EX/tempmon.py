#!/usr/bin/python

"""
Python 3 script to monitor the environment status on a Cubro Packetmaster over time
and write environment results to file. Use with firmware 2.2.5 or newer.
"""

import json
import requests
import time
from datetime import datetime
from requests.exceptions import ConnectionError

def env_check(ip, user, pword):
    '''Queries Packetmaster for environment stats.

       :param ip: A string, Managment IP address of PM.
       :param user: A string, Admin username for PM.
       :param pword: A string, Admin password for PM.
       :returns: A string, environment stats for PM.
       :raises: ConnectionError, if unable to make GET request to PM.'''
    uri = 'http://' + ip + '/rest/device/environment?'
    try:
        response = requests.get(uri, auth=(user, pword))
        content = response.content
        info = json.loads(content)
        return json.dumps(info, indent=4)
    except ConnectionError as error:
        return error

if __name__ == '__main__':
    ip = '192.168.0.200' # Management IP address of PM
    user = 'admin' # Admin username for PM
    pword = 'cubro' # Admin password for PM
    path = 'test.txt' # Absolute path to where file should be written or simply filename to write in same location as script
    while True:
        data = env_check(ip, user, pword)
        writetime = str(datetime.now())
        with open(path, 'a') as f:
            f.write(writetime + ': ' + data + '\n')
        time.sleep(1800)