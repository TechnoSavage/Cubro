#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Shows conceptually how the ReST API can  be used to perform a mass password reset for all users
#across all provided device IPs and output a text file containing the users and new passwords.
#Secondary functionality is to apply new passwords to users from a provided password file.

#!/usr/bin/python

#Import necessary Python libraries
import json, sys, re, string, random
from getpass import getpass
from packetmasterEX_rest import PacketmasterEX

def usage():
    print """Usage:
             -r, --random FILE   Provide a JSON formatted text file of device IPs.  All users on provided devices
                            will have current password replaced with a random password.  A file of usernames
                            and correspnding new passwords will be generated.
                            Format:
                            {
                            "packetmaster": [
                                            {"ip": "192.168.0.2", "admin": "username", "pass": "passwd"},
                                            {"ip": "192.168.0.3", "admin": "username", "pass": "passwd"}
                                            ]
                            }
             -f, --fromfile FILE   Provide a JSON formatted text file of device IPs, usernames, and new passwords.
                              Current passwords will be replaced with passwords provided in the file.
                              Format:
                              {
                              "packetmaster": [
                                {"ip": "192.168.1.221", "admin": "username", "passwd": "password"},
                                {"ip": "192.168.1.222", "admin": "username", "passwd": "password"}
                                ],
                              "users": [
                                {"username": "user1", "password": "passwd1"},
                                {"username": "user2", "password": "passwd2"}
                              ]
                              }"""

def rand_reset(ip, admin_username, admin_password):
    ex = PacketmasterEX(ip, admin_username, admin_password)
    results = {}
    changes = {}
    if ex.conn_test() == "Connection established":
        results["conn"] = True
    else:
        results["conn"] = False
    user_list = ex.get_users()
    data = json.loads(user_list)
    for user in data:
        passwd = rand_generator()
        changes[user] = passwd 
        reset = ex.mod_user(user, user, data[user]["accesslevel"], passwd, data[user]["description"], data[user]["radius"])
    return results, changes

def file_reset(ip, admin_username, admin_password, user_list):
    ex = PacketmasterEX(ip, admin_username, admin_password)
    results = {}
    if ex.conn_test() == "Connection established":
        results["conn"] = True
    else:
        results["conn"] = False
    for user in user_list:
        print user["username"], user["password"]
    return results

def rand_generator(size=16, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    passwd = ''.join(random.choice(chars) for char in range(size))
    return passwd

if __name__ == '__main__':
    if len(sys.argv) == 3 and str(sys.argv[1]) == '-r' or len(sys.argv) == 3 and str(sys.argv[1]) == '--random':
        filename = sys.argv[2]
        device_list = []
        success = []
        failed = []
        user_list = []
        with open(filename) as f:
            device_file = json.load(f)
            for item in device_file["packetmaster"]:
                ip = item["ip"]
                user = item["admin"]
                passwd = item["passwd"]
                run = rand_reset(ip, user, passwd)
                if run["conn"] == True:
                    success.append(ip)
                else:
                    failed.append(ip)
                user_list.append(run["users"])
    elif len(sys.argv) > 1 and str(sys.argv[1]) == '-f' or len(sys.argv) > 1 and str(sys.argv[1]) == '--fromfile':
        filename = sys.argv[2]
        device_list = []
        success = []
        failed = []
        with open(filename) as f:
            device_file = json.load(f)
            user_list = device_file["users"]
            for item in device_file["packetmaster"]:
                ip = item["ip"]
                user = item["admin"]
                passwd = item["passwd"]
                run = file_reset(ip, user, passwd, user_list)
                if run["conn"] == True:
                    success.append(ip)
                else:
                    failed.append(ip)
    else:
        usage()
