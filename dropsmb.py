#drop SMB traffic script
import urllib, requests, json, time
from datetime import datetime

#IP address to access REST data of device
deviceip = raw_input('What is the IP address of the Packetmaster you want to access: ')
ip = 'http://' + deviceip + '/rest'
#Device credentials
username = raw_input('Enter your username: ')
password = raw_input('Enter your password: ')
auth = urllib.urlencode({
    'username': username,
    'password': password
})

#options to append to device urllib
rule = '/flows?'

#Check system time
def checktime():
    time = datetime.now().strftime('%H:%M')
    print time
    if time == '17:00':
        try:
            addrule()
            addruletwo()
        except:
            print "Unable to execute drop SMB rules"

def addrule():
    url = ip + rule + auth
    params = {"name": "dropsmb temporary", "description": "This rule will drop SMB traffic for the specified duration", "priority": "75000", "match[in_port]": "1", "match[protocol]": "tcp", "match[tcp_dst]": "445", "match[match_extra]": "hard_timeout=43200", "actions": "drop"}
    try:
        response = requests.post(url, data=params)
        print response.status_code
        r = response.content
        data = json.loads(r)
        print json.dumps(data, indent=4)
    except:
        print 'Device is unavailable'
    checktime()

def addruletwo():
    def addrule():
        url = ip + rule + auth
        params = {"name": "dropsmb temporary", "description": "This rule will drop SMB traffic for the specified duration", "priority": "75000", "match[in_port]": "2", "match[protocol]": "tcp", "match[tcp_dst]": "445", "match[match_extra]": "hard_timeout=43200", "actions": "drop"}
        try:
            response = requests.post(url, data=params)
            print response.status_code
            r = response.content
            data = json.loads(r)
            print json.dumps(data, indent=4)
        except:
            print 'Device is unavailable'
        checktime()

checktime(60)
time.sleep(3600)
