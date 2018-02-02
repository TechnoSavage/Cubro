#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Shows conceptually how the ReST API can  be used to perform a mass password reset for all users
#across all provided device IPs and output a text file containing the users and new passwords.
#Secondary functionality is to apply new passwords to users from a provided password file.

#!/usr/bin/python

#Import necessary Python libraries
import json, sys, string, random
from packetmasterEX_rest import PacketmasterEX

def usage():
    print """Usage:
             -r, --random FILE   Provide a JSON formatted text file of device IPs and admin credentials.
                                 All users on provided devices will have current password replaced with
                                 a random password.  A file of usernames and correspnding new passwords
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
                             }"""

def rand_reset(ip, admin_username, admin_password):
    ex = PacketmasterEX(ip, admin_username, admin_password)
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
            changes[user + "@" + ip] = {"device": ip,
                                        "username": user,
                                        "password": rand_pass}
            reset = ex.mod_user(data[user]["username"],
                                data[user]["username"],
                                data[user]["accesslevel"],
                                rand_pass,
                                data[user]["description"],
                                data[user]["radius"])
    results["users"] = changes
    return results

def file_reset(ip, admin_username, admin_password, user_list):
    ex = PacketmasterEX(ip, admin_username, admin_password)
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
            reset = ex.mod_user(data[key]["username"],
                                data[key]["username"],
                                data[key]["accesslevel"],
                                user["passwd"],
                                data[key]["description"],
                                data[key]["radius"])
    return results

def admin_reset(ip, admin_username, admin_password):
    ex = PacketmasterEX(ip, admin_username, admin_password)
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
    changes[admin_username + "@" + ip] = {"device": ip,
                                          "username": admin_user,
                                          "password": rand_pass}
    reset = ex.mod_user(data[admin_username]["username"],
                        data[admin_username]["username"],
                        data[admin_username]["accesslevel"],
                        rand_pass,
                        data[admin_username]["description"])
    results["users"] = changes
    return results

def rand_generator(size=16, chars=string.ascii_uppercase + string.ascii_lowercase + string.digits):
    passwd = ''.join(random.choice(chars) for char in range(size))
    return passwd

if __name__ == '__main__':
    if len(sys.argv) == 3 and str(sys.argv[1]) in ('-r','--random'):
        filename = sys.argv[2]
        device_list = []
        success = []
        failed = []
        user_list = []
        output_file = {}
        with open(filename) as f:
            device_file = json.load(f)
            for item in device_file["packetmaster"]:
                ip = item["ip"]
                admin_user = item["admin"]
                admin_password = item["passwd"]
                run = rand_reset(ip, admin_user, admin_password)
                if run["conn"] == True:
                    success.append(ip)
                else:
                    failed.append(ip)
                try:
                    user_list.append(run["users"])
                except:
                    pass
        output_file["Successfully Changed"] = success
        output_file["Failed to connect"] = failed
        output_file["New User Passwords"] = user_list
        output = json.dumps(output_file, indent=4)
        with open('random_password_reset.json', 'w') as o:
            o.write(output)
    elif len(sys.argv) > 1 and str(sys.argv[1]) in ('-f', '--fromfile'):
        filename = sys.argv[2]
        device_list = []
        success = []
        failed = []
        output_file = {}
        with open(filename) as f:
            device_file = json.load(f)
            user_list = device_file["users"]
            for item in device_file["packetmaster"]:
                ip = item["ip"]
                admin_user = item["admin"]
                admin_password = item["passwd"]
                run = file_reset(ip, admin_user, admin_password, user_list)
                if run["conn"] == True:
                    success.append(ip)
                else:
                    failed.append(ip)
        output_file["Successfully Changed"] = success
        output_file["Failed to connect"] = failed
        output = json.dumps(output_file, indent=4)
        with open('password_reset.json', 'w') as o:
            o.write(output)
    elif len(sys.argv) > 1 and str(sys.argv[1]) in ('-a', '--admin'):
        filename = sys.argv[2]
        device_list = []
        success = []
        failed = []
        user_list = []
        output_file = {}
        with open(filename) as f:
            device_file = json.load(f)
            for item in device_file["packetmaster"]:
                ip = item["ip"]
                admin_user = item["admin"]
                admin_password = item["passwd"]
                run = admin_reset(ip, admin_user, admin_password)
                if run["conn"] == True:
                    success.append(ip)
                else:
                    failed.append(ip)
                try:
                    user_list.append(run["users"])
                except:
                    pass
        output_file["Successfully Changed"] = success
        output_file["Failed to connect"] = failed
        output_file["New User Passwords"] = user_list
        output = json.dumps(output_file, indent=4)
        with open('admin_reset.json', 'w') as o:
            o.write(output)
    else:
        usage()
