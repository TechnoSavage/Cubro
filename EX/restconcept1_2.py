#Use with firmware version 2.1.0.x or later. Python2.7 Cubro Packetmaster REST proof of concept v2.1.
#Use Packetmaster A to detect the presence of a given IP address and, upon detection, issue a rule to Packetmaster B: see below for Packetmaster Confguration.
# Packetmaster A must be configured with the following rules:
# A higher priority rule set to filter traffic based on the IP one wishes to have activate the the REST program.
# One may have to experiment with the list sub entries to track the txpkts field that corresponds to the rule looking for the IP
# One can configure flows in such a way as to transmit traffic carrying IP to Packetmaster B so that the added rule outputs to
# a tool.
#!/usr/bin/python

#Build this out further with more user input and cleaner code

#Import necessary Python libraries for interacting with the REST API
import requests, json, time
from getpass import getpass
from requests.exceptions import ConnectionError

def reset_rule_counters(address, username=None, password=None):
    uri = 'http://' + address + '/rest/rules/counters?'
    try:
        requests.delete(uri, auth=(username, password))
        success = 'Counters deleted successfully'
        return success
    except ConnectionError as e:
        r = 'No Response'
        raise e

#Define function 'query' which will check the REST status every second for an hour for a specific event
#rewrite txpkts search to more reliably detect the IP in question
def query(address, username=None, password=None):
    global ttl, address_rule, username_rule, password_rule
    l = list()
    uri = 'http://' + address + '/rest/ports/stats?'
    try:
        response = requests.get(uri, auth=(username, password))
        r = response.content
        data = json.loads(r)
    except ConnectionError as e:
        r = 'No Response'
        raise e
    for item in data:
        l.append(item['txpkts'])
    if l[5] > 0:
        print 'IP address has been detected'
        execute(address_rule, username_rule, password_rule)
    ttl = ttl - 1

#Define function 'execute' which will run if match in 'query' is found and then end the program
def execute(address, username=None, password=None):
    global ttl
    uri = 'http://' + address + '/rest/rules?'
    priority = 32768
    params = {'name': 'REST rule',
              'description': 'This rule was created by Python via REST API',
              'priority': priority,
              'match[in_port]': '3',
              'actions': '5'}
    try:
        response = requests.post(uri, data=params, auth=(username, password))
        # print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
        print 'Detection rule has been added'
    except ConnectionError as e:
        r = 'No Response'
        raise e
    ttl = 0


if __name__ == '__main__':
    #ttl represents that this program will run for an hour until it expires or the match criteria is found
    ttl = 3600
    address_detector = raw_input('What is the IP address of the Packetmaster detecting the IP Address: ')
    username_detector = raw_input('What is the username for detecting Packetmaster (if required): ')
    password_detector = getpass()
    address_rule = raw_input('What is the IP address of the Packetmaster where the detection rule will be created: ')
    username_rule = raw_input('What is the username for the Packetmaster where the detection rule will be created (if required): ')
    password_rule = getpass()

    #reset port counters if any exist
    reset_rule_counters(address_detector, username_detector, password_detector)

    #while loop executes 'query' so long as ttl value is greater than zero
    while ttl > 0:
        query(address_detector, username_detector, password_detector)
        print ttl
        time.sleep(1)

    #Once ttl value reaches zero the program will close
    print 'Program has expired'
    exit()
