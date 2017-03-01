#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST proof of concept v2.1.  Written by Derek Burke 12/2016
#Use a Packetmaster to detect the presence of an excessive amount of ICMP packets on a link and drop ICMP packets for one minute if they exceed threshold.
#Import necessary Python libraries for interacting with the REST API
import urllib, requests, json, time
from requests.exceptions import ConnectionError

#Initiate variable for EX authentication, EX IP address and needed rest paths
auth = urllib.urlencode({
'username': 'admin',
'password': 'cubro'
})
ip = raw_input('What is the IP address of the Packetmaster?: ')
ipadd = 'http://' + ip + '/rest'
rulestats = '/flows/all?'
rule = '/flows?'

#Function that repeatedly queries flow statisctics and parses the JSON response down to the datarate of a rule passing ICMP packets at a specific port.  Calls dropicmp function if daterate exceeds 2.5Kbps
def query():
    l = list()
    try:
        url = ipadd + rulestats + auth
        response = requests.get(url)
        r = response.content
        data = json.loads(r)
        count = 0
        for item in data['rules']:
            for item in data['rules'][count]['match']:
                if 'protocol' in item and data['rules'][count]['match']['protocol'] == 'icmp' and data['rules'][count]['match']['in_port'] == '1': #change in_port at end to match in port of monitored rule
                    datarate = data['rules'][count]['datarate']
                else:
                    continue
            count = count + 1
        field = datarate.split()
        if float(field[0]) > 2.5 and 'Kbit' in datarate:
            print line
            dropicmp()
        else:
            print datarate
            query()
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'

#Function that creates two rules: One that drops all ICMP packets and another that passes all other traffic.  Calls recreate function after 60 seconds.
def dropicmp():
    print 'ICMP flood detected; blocking ICMP packets for the next 60 seconds'
    url = ipadd + rule + auth
    priority1 = 50000
    priority2 = 32768
    params1 = {
    'name': 'ICMP Flood Mode',
    'description': 'Drop all ICMP packets for 60 seconds following creation of rule',
    'priority': priority1,
    'match[in_port]': '1,2,3',
    'match[protocol]': 'icmp',
    'actions': 'drop'
    }
    params2 = {
    'name': 'ICMP Flood Mode traffic',
    'description': 'Pass remaining traffic after ICMP drop to standard output port',
    'priority': priority2,
    'match[in_port]': '1,2,3',
    'actions': '4'
    }
    try:
        response1 = requests.post(url, data=params1)
        print response1.status_code
        r1 = response1.content
        data1 = json.loads(r1)
        print json.dumps(data1, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    try:
        response2 = requests.post(url, data=params2)
        print response2.status_code
        r2 = response2.content
        data2 = json.loads(r2)
        print json.dumps(data2, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    time.sleep(60)
    recreate()

#Function that recreates the original rules present on the EX device prior to dropicmp function.  Calls query function.
def recreate():
    url = ipadd + rule + auth
    priority1 = 50000
    priority2 = 32768
    params1 = {
    'name': 'Watch ICMP',
    'description': 'Pass ICMP packets',
    'priority': priority1,
    'match[in_port]': '1,2,3',
    'match[protocol]': 'icmp',
    'actions': '4'
    }
    params2 = {
    'name': 'Pass traffic',
    'description': 'Pass all non-ICMP traffic',
    'priority': priority2,
    'match[in_port]': '1,2,3',
    'actions': '4'
    }
    try:
        response1 = requests.post(url, data=params1)
        print response1.status_code
        r1 = response1.content
        data1 = json.loads(r1)
        print json.dumps(data1, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    try:
        response2 = requests.post(url, data=params2)
        print response2.status_code
        r2 = response2.content
        data2 = json.loads(r2)
        print json.dumps(data2, indent=4)
    except ConnectionError as e:
        r = 'No Response'
        print 'Device is unavailable \n'
    print 'Returning to standard traffic flow'
    time.sleep(10)
    query()

query()
