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
try:
    cmd = 'zeek -C -r %s "tcp_inactivity_timeout = 60min;"' % pcap_file
    #cmd = 'zeek -C -r %s local' % pcap_file

    sp = subprocess.Popen(cmd, shell=True)
    rc = sp.wait()
except OSError as e:
    print(e)

#Create RITA database from Zeek logs
try:
    rita_db_name = 'th_concept'
    cmd = 'rita import ./*.log %s' % rita_db_name
    sp = subprocess.Popen(cmd, shell=True)
    rc = sp.wait()
except OSError as e:
    print(e)

#verify creation of RITA database
try:
    cmd = 'rita list'
    sp = subprocess.Popen(cmd,
                          shell = True,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.STDOUT)
    rc = sp.wait()
    output = sp.stdout.read()
except OSError as e:
    print(e)
db_list = output.decode(encoding='utf-8').splitlines()
print(db_list)
if rita_db_name not in db_list:
    print('Failed to import Zeek logs to RITA')
    exit()

#Execute RITA detection mothods and create dict object for each entry that meets score threshold

confidence = 0.80  #Define confidence score threshold
detections = {}

#RITA 'show-beacons' block
try:
    cmd = 'rita show-beacons %s' % rita_db_name
    sp = subprocess.Popen(cmd, 
                          shell=True,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.STDOUT)
    rc = sp.wait()
    output = sp.stdout.read()
except OSError as e:
    print(e)
beacons = output.decode(encoding='utf-8').splitlines()
beacons = beacons.pop(0)
hits = []
for beacon in beacons:
    fields = beacon.split(',')
    score = float(fields[0])
    if score >= confidence:
        hits.append(beacon)
detections[beacons] = hits

#RITA 'show-beacons-fqdn' block
try:
    cmd = 'rita show-beacons-fqdn %s' % rita_db_name
    sp = subprocess.Popen(cmd, 
                          shell=True,
                          stdout = subprocess.PIPE,
                          stderr = subprocess.STDOUT)
    rc = sp.wait()
    output = sp.stdout.read()
except OSError as e:
    print(e)
beacons_fqdn = output.decode(encoding='utf-8').splitlines()
beacons_fqdn = beacons_fqdn.pop(0)
hits = []
for beacon in beacons_fqdn:
    fields = beacon.split(',')
    score = float(fields[0])
    if score >= confidence:
        hits.append(beacon)
detections[beacons_fqdn] = hits

print(detections)
