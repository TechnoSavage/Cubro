#!/usr/bin/python

"""A script to demonstrate concept of C2 detection in Custos"""

import subprocess
from datetime import datetime

#API to export PCAP for previous 24 hours
pcap_file = 'athlab4.pcap'
#Generate Zeek logs from PCAP, comment next line and uncomment the line after to use local Zeek config
cmd = 'zeek -C -r ' + pcap_file + ' tcp_inactivity_timeout = 60min;'
#cmd = 'zeek -C -r ' + pcap_file + ' local'

sp = subprocess.Popen(cmd, shell=True)
rc = sp.wait()
print(rc)

#Create RITA database from Zeek logs
rita_db_name = ''
cmd = 'rita import ./*.log' + rita_db_name


#Execute RITA detection mothods and create dict object for each entry that meets score threshold

confidence = 0.80  #Define confidence score threshold

#RITA 'show-beacons' block

#RITA 'show-beacons-fqdn' block




