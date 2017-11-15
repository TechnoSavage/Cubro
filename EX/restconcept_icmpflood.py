#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Use a Packetmaster to detect the presence of an excessive amount of ICMP packets on a link and drop ICMP packets for one minute if they exceed threshold.
#Prerequisites for using this script are that the Packetmaster has two rules set; one to pass imcp traffic from inputs to outputs and another lower priority
# passing all other traffic from the identical set of inputs to the identical set of outputs

#!/usr/bin/python

#Import necessary Python libraries for interacting with the REST API
import requests, json, time
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX
from requests.exceptions import ConnectionError

#Function that repeatedly queries flow statisctics and parses the JSON response down to the datarate of a rule passing ICMP packets at a specific port.  Calls dropicmp function if daterate exceeds 2.5Kbps
def query(pm, interface, priority1, priority2, limit):
    l = list()
    rules = pm.rules_active()
    rules_json = json.loads(rules)
    count = 0
    for rule in rules_json['rules']:
        for field in rule:
            if field == 'match':
                for criteria in rules_json['rules'][count]['match']:
                    if 'protocol' in criteria and rules_json['rules'][count]['match']['protocol'] == 'icmp' and rules_json['rules'][count]['match']['in_port'] == interface:
                        datarate = rules_json['rules'][count]['datarate']
                        output = rules_json['rules'][count]['actions_raw']
            else:
                continue
        count += 1
    field = datarate.split()
    if float(field[0]) > limit and 'Kbit' in datarate:
        dropicmp(pm, interface, output, priority1, priority2)
    else:
        print datarate
        query(pm, interface, priority1, priority2, limit)

#Function that creates two rules: One that drops all ICMP packets and another that passes all other traffic.  Calls recreate function after 60 seconds.
def dropicmp(pm, interface, output, priority1, priority2):
    print 'ICMP flood detected; blocking ICMP packets for the next 60 seconds'
    params1 = {
    'name': 'ICMP Flood Mode',
    'description': 'Drop all ICMP packets for 60 seconds following creation of rule',
    'priority': priority1,
    'match[in_port]': interface,
    'match[protocol]': 'icmp',
    'actions': 'drop'
    }
    params2 = {
    'name': 'ICMP Flood Mode traffic',
    'description': 'Pass remaining traffic after ICMP drop to standard output port',
    'priority': priority2,
    'match[in_port]': interface,
    'actions': output
    }
    pm.add_rule(params1)
    pm.add_rule(params2)
    time.sleep(60)
    recreate(pm, interface, ouput, priority1, priority2)

#Function that recreates the original rules present on the EX device prior to dropicmp function.  Calls query function.
def recreate(pm, interface, ouput, priority1, priority2):
    params1 = {
    'name': 'Watch ICMP',
    'description': 'Pass ICMP packets',
    'priority': priority1,
    'match[in_port]': interface,
    'match[protocol]': 'icmp',
    'actions': output
    }
    params2 = {
    'name': 'Pass traffic',
    'description': 'Pass all non-ICMP traffic',
    'priority': priority2,
    'match[in_port]': interface,
    'actions': output
    }
    pm.add_rule(params1)
    pm.add_rule(params2)
    print 'Returning to standard traffic flow'
    time.sleep(10)
    query(pm, interface, priority1, priority2, limit)

if __name__ == '__main__':
    address = raw_input('IP address of the Packetmaster to monitor: ')
    username = raw_input('Username for Packetmaster if required: ')
    password = getpass()
    pm = PacketmasterEX(address, username, password)
    interface = raw_input(""""What is the port number(s) or range of ports for the ICMP monitoring rule set
                          e.g. '5' or '1,2,5' or '5-10'
                          (Must match the rule set on the Packetmaster exactly): """)
    priority1 = raw_input("What is the priority of the rule monitoring ICMP traffic: ")
    try:
        priority1 = int(priority1)
    except:
        print "That is not a valid input for ICMP monitor priority; canceling program."
        exit()
    priority2 = raw_input("What is the priority of the rule passing all other traffic (Must be lower): ")
    try:
        priority2 = int(priority2)
    except:
        print "That is not a valid input for rule priority; canceling program."
        exit()
    limit = raw_input("""What is the datarate limit in Kbits/sec for allowable ICMP traffic on these ports
                      e.g. '10.0' or '250.7': """)
    try:
        limit = float(limit)
    except:
        print "That is not a valid input for datarate limit; canceling program."
        exit()
    query(pm, interface, priority1, priority2, limit)
