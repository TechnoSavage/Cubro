#Written by Derek Burke 9/2016
#Import necessary Python libraries for interacting with the REST API
import urllib
import urllib2
import json
import time

#Initiate variable for EX authentication, EX IP address and needed rest paths
auth = urllib.urlencode({
'username': 'admin',
'password': 'cubro'
})
EX2 = 'http://192.168.1.205/rest'
rulestats = '/flows/all?'
rule = '/flows?'

#Function that repeatedly queries flow statisctics and parses the JSON response down to the datarate of a rule passing ICMP packets.  Calls dropicmp function if daterate exceeds 50kbps
def query():
    l = list()
    try:
        uh = urllib.urlopen(EX2 + rulestats + auth)
    except:
        print 'unavailable'
    response = uh.read()
    try:
        data = json.loads(response)
    except:
        print 'No Data Available'
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

#Function that creates two rules: One that drops all ICMP packets and another that passes all other traffic.  Calls recreate function after 60 seconds.
def dropicmp():
    print 'ICMP flood detected; blocking ICMP packets for the next 60 seconds'
    url = EX2 + rule + auth
    priority1 = 50000
    priority2 = 32768
    params1 = urllib.urlencode({
    'name': 'ICMP Flood Mode',
    'description': 'Drop all ICMP packets for 5 minutes following creation of rule',
    'priority': priority1,
    'match[in_port]': '1,2,3',
    'match[protocol]': 'icmp',
    'actions': 'drop'
    })
    params2 = urllib.urlencode({
    'name': 'ICMP Flood Mode traffic',
    'description': 'Pass remaining traffic after ICMP drop to standard output port',
    'priority': priority2,
    'match[in_port]': '1,2,3',
    'actions': '4'
    })
    response1 = urllib2.urlopen(url, params1).read()
    response2 = urllib2.urlopen(url, params2).read()
    print response1
    print response2
    time.sleep(60)
    recreate()

#Function that recreates the original rules present on the EX device prior to dropicmp function.  Calls query function.
def recreate():
    url = EX2 + rule + auth
    priority1 = 50000
    priority2 = 32768
    params1 = urllib.urlencode({
    'name': 'Watch ICMP',
    'description': 'Pass ICMP packets',
    'priority': priority1,
    'match[in_port]': '1,2,3',
    'match[protocol]': 'icmp',
    'actions': '4'
    })
    params2 = urllib.urlencode({
    'name': 'Pass traffic',
    'description': 'Pass all non-ICMP traffic',
    'priority': priority2,
    'match[in_port]': '1,2,3',
    'actions': '4'
    })
    response2 = urllib2.urlopen(url, params2).read()
    response1 = urllib2.urlopen(url, params1).read()
    print response1
    print response2
    print 'Returning to standard traffic flow'
    time.sleep(10)
    query()

query()
