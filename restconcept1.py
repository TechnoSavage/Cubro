#Python2.7 Cubro Packetmaster REST proof of concept v2.0.  Written by Derek Burke 11/2016
#Use Packetmaster A to detect the presence of a given IP address and, upon detection, issue a rule to Packetmaster B: see below for Packetmaster Confguration.
#Import necessary Python libraries for interacting with the REST API
import urllib, requests, json, time

#ttl represents that this program will run for an hour until it expires or the match criteria is found
ttl = 3600
ipa = raw_input('What is the IP address of Packetmaster A (This Packetmaster detecting the known IP address)?: ')
ipb = raw_input('What is the IP address of Packetmaster B (The Packetmaster where the detection rule will be created)?: ')
PMA = 'http://' + ipa + '/rest'
PMB = 'http://' + ipb + '/rest'
usera = raw_input('What is the username for Packetmaster A?: ')
passa = raw_input('What is the password for Packetmaster A?: ')
autha = urllib.urlencode({
'username': usera,
'password': passa
})
userb = raw_input('What is the username for Packetmaster B?: ')
passb = raw_input('What is the password for Packetmaster B?: ')
authb = urllib.urlencode({
'username': userb,
'password': passb
})
pcounters = '/ports/counters?'
pstats = '/ports/stats?'
rule = '/flows?'

#Delete port counters if any exist
delcount = PMA + pcounters + autha
try:
    requests.delete(delcount)
    print 'Counters deleted successfully'
except:
    print 'Unable to delete counters'

#Define function 'query' which will check the REST status every second for an hour for a specific event
def query():
    global ttl
    l = list()
    try:
        url = PMA + pstats + autha
        response = requests.get(url)
        r = response.content
        data = json.loads(r)
    except:
        print 'Device is unavailable'
    for item in data:
        l.append(item['txpkts'])
    if l[5] > 0:
        print 'IP address has been detected'
        execute()
    ttl = ttl - 1

#Define function 'execute' which will run if match in 'query' is found and then end the program
def execute():
    global ttl
    url = PMB + rule + authb
    priority = 32768
    params = {'name': 'REST rule', 'description': 'This rule was created by Python via REST API', 'priority': priority, 'match[in_port]': '3', 'actions': '5'}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
        print 'Detection rule has been added'
    except:
        print 'Unable to add rule'
    ttl = 0

#while loop executes 'query' so long as ttl value is greater than zero
while ttl > 0:
    query()
    print ttl
    time.sleep(1)

#Once ttl value reaches zero the program will close
print 'Program has expired'
exit()

# Packetmaster A must be configured with the following rules:
# A higher priority rule set to filter traffic based on the IP one wishes to have activate the the REST program.
# One may have to experiment with the list sub entries to track the txpkts field that corresponds to the rule looking for the IP
# One can configure flows in such a way as to transmit traffic carrying IP to Packetmaster B so that the added rule outputs to
# a tool.
