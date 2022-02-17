#!/usr/bin/python

"""A script to demonstrate concept of C2 detection in Custos. Script automates initial steps
   of capture analysis with Zeek and RITA. Script assumes Custos will be the source of PCAP
   files in the future."""

import json
import requests
import subprocess
from datetime import datetime
from requests import ConnectionError


def get_nonce():
    '''Retrieve seed & nonce from Custos.'''
    uri = 'https://loaclhost/v1/auth/nonce/admin@custos.com?'
    headers = {'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/json'}
    try:
        response = requests.get(uri, headers=headers)
        content = response.content
        data = json.loads(content)
        return json.dumps(data, indent=4)
    except ConnectionError as error:
        content = 'No Response'
        raise error

def get_token():
    '''Authenticate to Custos and retrieve bearer token.'''
    uri = 'https://loaclhost/v1/auth/login/admin@custos.com?'
    headers = {'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/json'}
    try:
        response = requests.get(uri, headers=headers)
        content = response.content
        data = json.loads(content)
        return json.dumps(data, indent=4)
    except ConnectionError as error:
        content = 'No Response'
        raise error

def create_pcap(token, time, name):
    '''Create PCAP for previous 24 hours.'''
    uri = 'https://loaclhost/v1/capture/rolling/start?'
    headers = {'X-Requested-With': 'XMLHttpRequest',
               'Content-Type': 'application/json'}
    start_time = ''
    end_time = ''
    payload = {"startTime": start_time,
              "endTime": end_time,
              "name":"rolling-export-2022-01-19_14-55-27.pcap",
              "filter":""}   #tcpdump filter
    try:
        response = requests.post(uri, headers=headers, data=payload)
        content = response.content
        data = json.loads(content)
        return json.dumps(data, indent=4)
    except ConnectionError as error:
        content = 'No Response'
        raise error

if __name__ == '__main__':
    #API to export PCAP for previous day. Note: API calls to Custos
    #suspended due to Custos PCAP export file limit of 500MB being 
    #unsuitable to the use case concept. 

    #year = datetime.now().year
    #month = datetime.now().month
    #day = datetime.now().day

    #Use Custos API to generate PCAP file

    #nonce = get_nonce()
    #token = get_token()

    #Verify file exists

    #Create folder for all following actions

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
    if rita_db_name not in db_list:
        print('Failed to import Zeek logs to RITA')
        exit()

    #Execute RITA detection methods and create dict object for each entry that meets score threshold

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
    beacons.pop(0)
    for beacon in beacons:
        fields = beacon.split(',')
        score = float(fields[0])
        if score >= confidence:
            hits = []    #Change to Dict so values can be iterated
            hits.append(beacon) #Change to add each value to appropriate key e.g. score, src_ip, dst_ip, proto
    detections['beacons'] = hits 

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
    beacons_fqdn.pop(0)
    hits = []
    for beacon in beacons_fqdn:
        fields = beacon.split(',')
        score = float(fields[0])
        if score >= confidence:
            hits.append(beacon)
    detections['beacons_fqdn'] = hits

    print(detections) #remove after functional code is finished, write to file instead

    #Add further info to detections e.g. Custos app detection, reverse DNS, cert info