#!/usr/bin/python

""" Use with firmware version 2.2.5 or later.
    Cubro Packetmaster REST API demo. Shows conceptually how the ReST API can
    be used to perform a mass password reset for all users across all provided
    device IPs and output a text file containing the users and new passwords.
    Secondary functionality is to apply new passwords to users from a provided
    password file. """

#Import necessary Python libraries
from __future__ import print_function #Requires Python 2.6 or later
import json
import sys
import string
import random
from packetmaster_ex_rest import PacketmasterEX

def usage():
    """ Display usage and help. """
    print("""Usage:
             -r, --random FILE   Provide a JSON formatted text file of device IPs and admin credentials.
                                 All users on provided devices will have current password replaced with
                                 a random password.  A file of usernames and corresponding new passwords
                                 will be created on this device.  This will NOT change the provided
                                 admin user's password to insure proper execution (see -a option).
                            Format:
                            {
                            "packetmaster": [
                                            {"ip": "192.168.0.2", "admin": "username", "passwd": "password"},
                                            {"ip": "192.168.0.3", "admin": "username", "passwd": "password"}
                                            ]
                            }

             -f, --fromfile FILE   Provide a JSON formatted text file of device IPs, usernames, and new passwords.
                                   Current passwords will be replaced with passwords provided in the file.  This will
                                   NOT change the provided admin user's password to insure proper execution (see -a option).
                              Format:
                              {
                              "packetmaster": [
                                {"ip": "192.168.1.221", "admin": "username", "passwd": "password"},
                                {"ip": "192.168.1.222", "admin": "username", "passwd": "password"}
                                ],
                              "users": [
                                {"username": "user1", "passwd": "passwd1"},
                                {"username": "user2", "passwd": "passwd2"}
                              ]
                              }

            -a, --admin FILE   Provide a JSON formatted text file of device IPs and admin credentials.
                               This option will replace ONLY the provided device admin's password with
                               a randomly generated password.  A file containing the admin's new password
                               will be created on this device.
                             Format:
                             {
                             "packetmaster": [
                                             {"ip": "192.168.0.2", "admin": "username", "passwd": "password"},
                                             {"ip": "192.168.0.3", "admin": "username", "passwd": "password"}
                                             ]
                             }""")

def rand_reset(device_ip, admin_username, admin_pass):
    """ Replace all non-admin users passwords with randomly generated
        passwords. Return the changed passwords. """
    ex = PacketmasterEX(device_ip, admin_username, admin_pass)
    results = {}
    changes = {}
    if ex.conn_test() == "Connection established":
        results["conn"] = True
    else:
        results["conn"] = False
        return results
    user_list = ex.get_users()
    data = json.loads(user_list)
    for user in data:
        if user != admin_username:
            rand_pass = rand_generator()
            changes[user + "@" + device_ip] = {"device": device_ip,
                                               "username": user,
                                               "password": rand_pass}
            ex.mod_user(data[user]["username"],
                        data[user]["username"],
                        data[user]["accesslevel"],
                        rand_pass,
                        data[user]["description"],
                        data[user]["radius"])
    results["users"] = changes
    return results

def file_reset(device_ip, admin_username, admin_pass, user_list):
    """ Reset non-admin user passwords using a provided username and password
        list. """
    ex = PacketmasterEX(device_ip, admin_username, admin_pass)
    results = {}
    if ex.conn_test() == "Connection established":
        results["conn"] = True
    else:
        results["conn"] = False
        return results
    to_change = []
    cur_users = ex.get_users()
    data = json.loads(cur_users)
    for user in data:
        to_change.append(user)
    for user in user_list:
        if user["username"] in to_change and user["username"] != admin_username:
            key = user["username"]
            ex.mod_user(data[key]["username"],
                        data[key]["username"],
                        data[key]["accesslevel"],
                        user["passwd"],
                        data[key]["description"],
                        data[key]["radius"])
    return results

def admin_reset(device_ip, admin_username, admin_pass):
    """ Replace only admin users password with randomly generated password and
        return the new password. """
    ex = PacketmasterEX(device_ip, admin_username, admin_pass)
    results = {}
    changes = {}
    if ex.conn_test() == "Connection established":
        results["conn"] = True
    else:
        results["conn"] = False
        return results
    cur_users = ex.get_users()
    data = json.loads(cur_users)
    rand_pass = rand_generator()
    changes[admin_username + "@" + device_ip] = {"device": device_ip,
                                                 "username": admin_user,
                                                 "password": rand_pass}
    ex.mod_user(data[admin_username]["username"],
                data[admin_username]["username"],
                data[admin_username]["accesslevel"],
                rand_pass,
                data[admin_username]["description"])
    results["users"] = changes
    return results

def rand_generator(size=16, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    """ Generates a random password. """
    passwd = ''.join(random.choice(chars) for char in range(size))
    return passwd

if __name__ == '__main__':
    if len(sys.argv) == 3 and str(sys.argv[1]) in ('-r', '--random'):
        FILENAME = sys.argv[2]
        DEVICE_LIST = []
        SUCCESS = []
        FAILED = []
        USER_LIST = []
        OUTPUT_FILE = {}
        with open(FILENAME) as f:
            DEVICE_FILE = json.load(f)
            for item in DEVICE_FILE["packetmaster"]:
                ip_address = item["ip"]
                admin_user = item["admin"]
                admin_password = item["passwd"]
                run = rand_reset(ip_address, admin_user, admin_password)
                if run["conn"]:
                    SUCCESS.append(ip_address)
                else:
                    FAILED.append(ip_address)
                try:
                    USER_LIST.append(run["users"])
                except (NameError, KeyError) as reason:
                    print(reason)
        OUTPUT_FILE["Successfully Changed"] = SUCCESS
        OUTPUT_FILE["Failed to connect"] = FAILED
        OUTPUT_FILE["New User Passwords"] = USER_LIST
        OUTPUT = json.dumps(OUTPUT_FILE, indent=4)
        with open('random_password_reset.json', 'w') as o:
            o.write(OUTPUT)
    elif len(sys.argv) > 1 and str(sys.argv[1]) in ('-f', '--fromfile'):
        FILENAME = sys.argv[2]
        DEVICE_LIST = []
        SUCCESS = []
        FAILED = []
        OUTPUT_FILE = {}
        with open(FILENAME) as f:
            DEVICE_FILE = json.load(f)
            USER_LIST = DEVICE_FILE["users"]
            for item in DEVICE_FILE["packetmaster"]:
                ip_address = item["ip"]
                admin_user = item["admin"]
                admin_password = item["passwd"]
                run = file_reset(ip_address, admin_user, admin_password, USER_LIST)
                if run["conn"]:
                    SUCCESS.append(ip_address)
                else:
                    FAILED.append(ip_address)
        OUTPUT_FILE["Successfully Changed"] = SUCCESS
        OUTPUT_FILE["Failed to connect"] = FAILED
        OUTPUT = json.dumps(OUTPUT_FILE, indent=4)
        with open('password_reset.json', 'w') as o:
            o.write(OUTPUT)
    elif len(sys.argv) > 1 and str(sys.argv[1]) in ('-a', '--admin'):
        FILENAME = sys.argv[2]
        DEVICE_LIST = []
        SUCCESS = []
        FAILED = []
        USER_LIST = []
        OUTPUT_FILE = {}
        with open(FILENAME) as f:
            DEVICE_FILE = json.load(f)
            for item in DEVICE_FILE["packetmaster"]:
                ip_address = item["ip"]
                admin_user = item["admin"]
                admin_password = item["passwd"]
                run = admin_reset(ip_address, admin_user, admin_password)
                if run["conn"]:
                    SUCCESS.append(ip_address)
                else:
                    FAILED.append(ip_address)
                try:
                    USER_LIST.append(run["users"])
                except (NameError, KeyError) as reason:
                    print(reason)
        OUTPUT_FILE["Successfully Changed"] = SUCCESS
        OUTPUT_FILE["Failed to connect"] = FAILED
        OUTPUT_FILE["New User Passwords"] = USER_LIST
        OUTPUT = json.dumps(OUTPUT_FILE, indent=4)
        with open('admin_reset.json', 'w') as o:
            o.write(OUTPUT)
    else:
        usage()
