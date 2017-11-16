#Drop SMB traffic script.  Drop SMB traffic starting at a specified time for a duration of time.
#Use with firmware version 2.1.0.x or later. Python2.7.
#!/usr/bin/python

#Import necessary libraries
import json, time
from getpass import getpass
from datetime import datetime
from packetmasterEX_rest import PacketmasterEX

#Check system time
def checktime(pm, drop_time, interface, duration):
    current_time = datetime.now().strftime('%H:%M')
    print "Current time is %s; SMB traffic will be dropped starting at %s." % (current_time, drop_time)
    if str(current_time) == drop_time:
        dropsmb(pm, interface, duration)

def dropsmb(pm, interface, duration):
    timeout = "hard_timeout=" + duration
    params = {"name": "dropsmb temporary",
              "description": "This rule will drop SMB traffic for the specified duration",
              "priority": 65535,
              "match[in_port]": interface,
              "match[protocol]": "tcp",
              "match[tcp_dst]": "445",
              "match[extra]": timeout,
              "actions": "drop"}
    run = pm.add_rule(params)
    print run

if __name__ == '__main__':
    address = raw_input('IP of Packetmaster: ')
    username = raw_input('Username for Packetmaster if required: ')
    password = getpass()
    pm = PacketmasterEX(address, username, password)
    drop_time = raw_input("Enter time at which to start dropping SMB traffic (24 hour format e.g. '1:00', '16:30'): ")
    interface = raw_input("""What is(are) the port number(s) or range of ports on which to drop SMB traffic at the specified time?
                              e.g. '5' or '1,2,5' or '5-10': """)
    duration = raw_input("""Enter the length of time in seconds for which SMB traffic should be dropped
                            e.g. 43200 equals 12 hours (65535 maximum): """)

    while True:
        checktime(pm, drop_time, interface, duration)
        time.sleep(30)
