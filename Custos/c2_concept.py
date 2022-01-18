#!/usr/bin/python

"""A script to demonstrate concept of C2 detection in Custos"""

import subprocess
from datetime import datetime

#API to export PCAP for previous 24 hours
#use datetime to name present days PCAP
#Use Custos API to generate PCAP file
#Verify file exists
#Create folder for all following commands

pcap_file = 'athlab4.pcap' #Use datetime to name variable
#Generate Zeek logs from PCAP, comment next line and uncomment the line after to use local Zeek config
cmd = 'zeek -C -r %s "tcp_inactivity_timeout = 60min;"' % pcap_file
#cmd = 'zeek -C -r %s local' % pcap_file

sp = subprocess.Popen(cmd, shell=True)
rc = sp.wait()
print(rc)

#Create RITA database from Zeek logs
rita_db_name = 'th_concept'
cmd = 'rita import ./*.log %s' % rita_db_name
sp = subprocess.Popen(cmd, shell=True)
rc = sp.wait()

#verify creation of RITA database
cmd = 'rita list'
sp = subprocess.Popen(cmd, capture_output=True)
rc = sp.wait()
print(sp.stdout)

#print(db_list)
#if rita_db_name not in db_list:
    #print('Failed to import Zeek logs to RITA')
    #exit()

#Execute RITA detection mothods and create dict object for each entry that meets score threshold

confidence = 0.80  #Define confidence score threshold

#RITA 'show-beacons' block
cmd = 'rita show-beacons %s' % rita_db_name
sp = subprocess.Popen(cmd, shell=True)
rc = sp.wait()
print(rc)

#RITA 'show-beacons-fqdn' block
cmd = 'rita show-beacons-fqdn %s' % rita_db_name


