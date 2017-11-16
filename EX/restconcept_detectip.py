#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Use a Packetmaster 'A' to detect the presence of traffic rom a specified IP address and, upon detection,
# create a rule on Packetmater 'B' to block all traffic from that IP address.
#Prerequisites are that Packetmaster 'A' must have a higher priority rule filtering on the IP address in question.
# User should edit the 'execute' function in this script as desired for his rule parameters.

#!/usr/bin/python

#Import necessary Python libraries
import json, time
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX

#Function to query for the existence of the specified IP address on Packetmaster 'A' (detector)
def query(detector, blocker, address):
    global ttl
    rules = detector.rules_active()
    rules_json = json.loads(rules)
    count = 0
    for rule in rules_json['rules']:
        for field in rule:
            if field == 'match':
                for criteria in rules_json['rules'][count]['match']:
                    if 'nw_src' in criteria and rules_json['rules'][count]['match']['nw_src'] == address:
                        if float(rules_json['rules'][count]['n_packets']) > 0:
                            execute(blocker, address)
        count += 1
    ttl = ttl - 1

#Function to instantiate a rule to block the IP address on Packetmaster 'B' (blocker)
def execute(blocker, address):
    global ttl
    priority = 65535 #Alter this value to match your level of blocking priority
    inport = '1' #Enter string value of ingress port number of traffic carrying the detected IP e.g. '5' or '2,3,6' or '5-10'
    name = 'Blocking detected IP: %s' % address
    params = {'name': name,
              'description': 'This rule was created by Python via REST API',
              'priority': priority,
              'match[in_port]': inport,
              'match[nw_src]': address,
              'actions': 'drop'}
    blocker.add_rule(params)
    ttl = 0

if __name__ == '__main__':
    #ttl represents that this program will run for an hour until it expires or the match criteria is found
    ttl = 3600
    detect_ip = raw_input("What is the IP address to be detected: ")
    address_detector = raw_input('What is the IP address of the Packetmaster detecting the IP Address: ')
    username_detector = raw_input('What is the username for detecting Packetmaster (if required): ')
    password_detector = getpass()
    detector = PacketmasterEX(address_detector, username_detector, password_detector)
    address_blocker = raw_input('What is the IP address of the Packetmaster where the blocking rule will be created: ')
    username_blocker = raw_input('What is the username for the Packetmaster where the blocking rule will be created (if required): ')
    password_blocker = getpass()
    blocker = PacketmasterEX(address_blocker, username_blocker, password_blocker)

    #reset port counters if any exist
    detector.reset_rule_counters()

    #while loop executes 'query' so long as ttl value is greater than zero
    while ttl > 0:
        query(detector, blocker, detect_ip)
        print ttl
        time.sleep(1)

    #Once ttl value reaches zero the program will close
    print 'Program has expired'
    exit()
