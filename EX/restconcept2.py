#Use with firmware version 2.0.0.x or earlier. Python2.7 Cubro Packetmaster REST proof of concept v2.0.  Written by Derek Burke 11/2016
#Use a Packetmaster to detect the presence of an excessive amount of ICMP packets on a link and drop ICMP packets for one minute if they exceed threshold.
#Import necessary Python libraries for interacting with the REST API
import urllib, requests, json, time

#Initiate variable for EX authentication, EX IP address and needed rest paths
auth = urllib.urlencode({
'username': 'admin',
'password': 'cubro'
})
EX2 = 'http://192.168.1.205/rest'
rulestats = '/flows/all?'
rule = '/flows?'

#Function that repeatedly queries flow statisctics and parses the JSON response down to the datarate of a rule passing ICMP packets.  Calls dropicmp function if daterate exceeds 2.5Kbps
def query():
    l = list()
    try:
        url = EX2 + rulestats + auth
        response = requests.get(url)
        r = response.content
        data = json.loads(r)
        for item in data['rules']:
            l.append(item['datarate'])
        line = l[1]
        field = line.split()
        if float(field[0]) > 2.5 and 'Kbit' in line:
            print line
            dropicmp()
        else:
            print line
            query()
    except Exception:
        print 'Device is unavailable'

#Function that creates two rules: One that drops all ICMP packets and another that passes all other traffic.  Calls recreate function after 60 seconds.
def dropicmp():
    print 'ICMP flood detected; blocking ICMP packets for the next 60 seconds'
    url = EX2 + rule + auth
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
    except Exception:
        print 'Unable to drop ICMP packets; add rule failed'
    try:
        response2 = requests.post(url, data=params2)
        print response2.status_code
        r2 = response2.content
        data2 = json.loads(r2)
        print json.dumps(data2, indent=4)
    except Exception:
        print 'Unable to pass all remaining traffic; add rule failed'
    time.sleep(60)
    recreate()

#Function that recreates the original rules present on the EX device prior to dropicmp function.  Calls query function.
def recreate():
    url = EX2 + rule + auth
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
    except Exception:
        print 'Unable to recreate rule 1'
    try:
        response2 = requests.post(url, data=params2)
        print response2.status_code
        r2 = response2.content
        data2 = json.loads(r2)
        print json.dumps(data2, indent=4)
    except Exception:
        print 'Unable to recreate rule 2'
    print 'Returning to standard traffic flow'
    time.sleep(10)
    query()

query()
