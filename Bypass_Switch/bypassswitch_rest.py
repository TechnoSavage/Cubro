#Bypass Switch device class for REST API interaction

import requests, json
from requests.exceptions import ConnectionError

#TO-DO Implement chacks against valid input for config settings
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

        #Method to disengage the bypass
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

        #Method to disengage bypass for timeout period
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

        #Method to change device configuration with guided choices
        def set_config_guided(self):
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

        #Method to change device configuration with arguments
        def set_config(self, address, subnet, gateway, mac, timeout):
            uri = 'http://' + self.address + '/setConfig?'
            try:
                params = {
                'ip': address,
                'subnet': subnet,
                'gateway': gateway,
                'mac': mac,
                'timeout': timeout
                }
                response = requests.post(uri, data=params)
                code = response.status_code
                r = response.content
                return code
            except ConnectionError as e:
                r = 'No Response'
                raise e
