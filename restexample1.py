#Use with firmware version 2.0.0.x or earlier. Written by Derek Burke 9/2016
#Import necessary Python libraries for interacting with the REST API
import urllib
import urllib2
import json
import time

#ttl represents that this program will run for an hour until it expires or the match criteria is found
ttl = 3600
auth = urllib.urlencode({
'username': 'admin',
'password': 'cubro'
})
EX2 = 'http://192.168.1.205/rest'
EX32 = 'http://192.168.1.221/rest'
pstats = '/ports/stats?'
rule = '/flows?'
#Define function 'query' which will check the REST status every second for an hour for a specific event
def query():
    global ttl
    l = list()
    try:
        uh = urllib.urlopen(EX2 + pstats + auth)
    except:
        print 'unavailable'
    response = uh.read()
    try:
        data = json.loads(response)
    except:
        print 'No Data Available'
    for item in data:
        l.append(item['txpkts'])
    if l[5] > 0:
        execute()
    ttl = ttl - 1

#Define function 'execute' which will run if match in 'query' is found and then end the program
def execute():
    global ttl
    url = EX32 + rule + auth
    priority = 32768
    params = urllib.urlencode({
    'name': 'REST rule',
    'description': 'This rule was created by Python via REST API',
    'priority': priority,
    'match[in_port]': '3',
    'actions': '5'
    })
    response = urllib2.urlopen(url, params).read()
    print response
    ttl = 0

#while loop executes 'query' so long as ttl value is greater than zero
while ttl > 0:
    query()
    print ttl
    time.sleep(1)

#Once ttl value reaches zero the program will close
print 'Program has expired'
exit()
