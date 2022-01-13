#!/usr/bin/python

""" Drop SMB traffic on a Packetmaster starting at a specified time for a
    set duration of time.
    Use with firmware version 2.2.5 or later. Python2.7. """

#Import necessary libraries
from __future__ import print_function #Requires Python 2.6 or later
import time
from getpass import getpass
from datetime import datetime
from six import moves
from packetmaster_ex_rest import PacketmasterEX

#Check system time
def checktime(packetmaster, drop_time, interface, duration):
    """ Check current time against specified time to drop SMB trafficself.
        Call 'dropsmb' function if current time matches drop time."""
    current_time = datetime.now().strftime('%H:%M')
    print("Current time is %s; SMB traffic will be dropped "
           "starting at %s." % (current_time, drop_time))
    if str(current_time) == drop_time:
        dropsmb(packetmaster, interface, duration)

def dropsmb(packetmaster, interface, duration):
    """ Sets rule on Packetmaster to drop SMB traffic for specified duration
        of time. """
    timeout = "hard_timeout=" + duration
    data = {"name": "dropsmb temporary",
            "description": "This rule will drop SMB traffic for the specified duration",
            "priority": 65535,
            "match[in_port]": interface,
            "match[protocol]": "tcp",
            "match[tcp_dst]": "445",
            "match[extra]": timeout,
            "actions": "drop"}
    run = packetmaster.add_rule(data)
    print(run)

if __name__ == '__main__':
    ADDRESS = moves.input('IP of Packetmaster: ')
    USERNAME = moves.input('Username for Packetmaster if required: ')
    PASSWORD = getpass()
    PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
    DROP_TIME = moves.input("Enter time at which to start dropping SMB traffic "
                          "(24 hour format e.g. '1:00', '16:30'): ")
    INTERFACE = moves.input("""What is(are) the port number(s) or range of ports
                             on which to drop SMB traffic at the specified time?
                             e.g. '5' or '1,2,5' or '5-10': """)
    DURATION = moves.input("""Enter the length of time in seconds for which SMB
                            traffic should be dropped.
                            e.g. 43200 equals 12 hours (65535 maximum): """)

    while True:
        checktime(PACKETMASTER, DROP_TIME, INTERFACE, DURATION)
        time.sleep(30)
