#!/usr/bin/python

""" Use with firmware version 2.2.5 or later. Python2.7
    Cubro Packetmaster REST API demo. Use a Packetmaster to detect the presence
    of an excessive amount of ICMP packets on a link and drop ICMP packets for
    one minute if they exceed threshold. Prerequisites for using this script
    are that the Packetmaster has two rules set: one to pass imcp traffic
    from inputs to outputs and another lower priority rule passing all other
    traffic from the identical set of inputs to the identical set of outputs. """


#Import necessary Python libraries for interacting with the REST API
import json
import time
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX

def query(packetmaster, interface, priority1, priority2, limit):
    """ Function that repeatedly queries flow statisctics and parses the JSON
        response down to the datarate of a rule passing ICMP packets at a
        specific port. Calls dropicmp function if daterate exceeds
        specified limit. """
    rules = packetmaster.rules_active()
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
        dropicmp(packetmaster, interface, output, priority1, priority2, limit)
    else:
        print datarate
        query(packetmaster, interface, priority1, priority2, limit)

def dropicmp(packetmaster, interface, output, priority1, priority2, limit):
    """ Creates two rules: One that drops all ICMP packets and another that
        passes all other traffic.  Calls recreate function after 60 seconds. """
    print 'ICMP flood detected; blocking ICMP packets for the next 60 seconds'
    params1 = {'name': 'ICMP Flood Mode',
               'description': 'Drop all ICMP packets for 60 seconds following creation of rule',
               'priority': priority1,
               'match[in_port]': interface,
               'match[protocol]': 'icmp',
               'actions': 'drop'}
    params2 = {'name': 'ICMP Flood Mode traffic',
               'description': 'Pass remaining traffic after ICMP drop to standard output port',
               'priority': priority2,
               'match[in_port]': interface,
               'actions': output}
    packetmaster.add_rule(params1)
    packetmaster.add_rule(params2)
    time.sleep(60)
    recreate(packetmaster, interface, output, priority1, priority2, limit)

def recreate(packetmaster, interface, output, priority1, priority2, limit):
    """ Recreates the original rules present on the EX device prior to dropicmp
        function.  Calls query function. """
    params1 = {'name': 'Watch ICMP',
               'description': 'Pass ICMP packets',
               'priority': priority1,
               'match[in_port]': interface,
               'match[protocol]': 'icmp',
               'actions': output}
    params2 = {'name': 'Pass traffic',
               'description': 'Pass all non-ICMP traffic',
               'priority': priority2,
               'match[in_port]': interface,
               'actions': output}
    packetmaster.add_rule(params1)
    packetmaster.add_rule(params2)
    print 'Returning to standard traffic flow'
    time.sleep(10)
    query(packetmaster, interface, priority1, priority2, limit)

if __name__ == '__main__':
    ADDRESS = raw_input('IP address of the Packetmaster to monitor: ')
    USERNAME = raw_input('Username for Packetmaster: ')
    PASSWORD = getpass()
    PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
    INTERFACE = raw_input(""""What is(are) the port number(s) or range of ports
                              for the ICMP monitoring rule set
                              e.g. '5' or '1,2,5' or '5-10'
                              (Must match the rule set on the Packetmaster exactly): """)
    PRIORITY1 = raw_input("What is the priority of the rule monitoring ICMP traffic: ")
    try:
        PRIORITY1 = int(PRIORITY1)
    except ValueError as reason:
        print ("That is not a valid input for ICMP monitor priority; canceling program.", reason)
        exit()
    PRIORITY2 = raw_input("What is the priority of the rule passing all "
                          "other traffic (Must be lower): ")
    try:
        PRIORITY2 = int(PRIORITY2)
    except ValueError as reason:
        print ("That is not a valid input for rule priority; canceling program.", reason)
        exit()
    LIMIT = raw_input("""What is the datarate limit in Kbits/sec for allowable
                        ICMP traffic on these ports
                        e.g. '10.0' or '250.7': """)
    try:
        LIMIT = float(LIMIT)
    except ValueError as reason:
        print ("That is not a valid input for datarate limit; canceling program.", reason)
        exit()
    query(PACKETMASTER, INTERFACE, PRIORITY1, PRIORITY2, LIMIT)
