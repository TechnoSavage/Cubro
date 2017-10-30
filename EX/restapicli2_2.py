#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Import necessary Python libraries for interacting with the REST API
#!/usr/bin/python
import requests, json, re
from getpass import getpass
from requests.exceptions import ConnectionError
from packetmasterEX_rest import PacketmasterEX
# Add code to handle case and verify input in all areas where needed

def set_ip():
    fail_count = 0
    while fail_count < 3:
        address = raw_input('What is the IP address of the Packetmaster you want to access?: ')
        try:
            ip_address = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', address)
            address = ip_address[0]
            return address
        except:
            print "That is not a valid IPv4 address."
            fail_count += 1
    print "That is not a valid IPv4 address.  Exiting"
    exit()

if __name__ == '__main__':
    #Welcome statement
    print '''
        Welcome to my interactive Cubro Packetmaster REST API demo.
        All Packetmaster interaction in this program is accomplished via
        the Cubro REST API. \n'''

    #IP address to access REST data of device
    address = set_ip()
    #Device credentials
    username = raw_input('Enter your username: ')
    password = getpass()
    packetmaster = PacketmasterEX(address, username, password)
    #Initial menu to check or change settings
    def topmenu():
        global address, username, password, packetmaster
        print 'Options for device at', address,'acting as User', username
        print '''
            1 - Change My working device
            2 - Change My user credentials
            3 - Check Packetmaster Settings
            4 - Change Packetmaster Settings
            5 - Quit \n'''

        option = raw_input('Enter the number of the action you would like to perform: ')
        try:
            option = int(option)
        except:
            topmenu()
        if option == 1:
            address = set_ip()
            packetmaster = PacketmasterEX(address, username, password)
            topmenu()
        elif option == 2:
            username = raw_input('Enter your username: ')
            password = getpass()
            packetmaster = PacketmasterEX(address, username, password)
            topmenu()
        elif option == 3:
            checkmenu()
        elif option == 4:
            changemenu()
        elif option == 5:
            print 'Goodbye'
            exit()
        else:
            print 'That is not a valid selection \n'
            topmenu()

    #Check settings menu
    def checkmenu():
        print 'Check settings for device at', address,'acting as User', username
        print '''
                  1 - Software Version
                  2 - IP Configuration
                  3 - Model
                  4 - Name + Notes
                  5 - Serial Number
                  6 - Hardware Generation
                  7 - Port Configuration
                  8 - Port Status
                  9 - Port Counters
                 10 - SFP Status
                 11 - Show Rules
                 12 - Show Groups
                 13 - List Apps
                 14 - List Running Apps
                 15 - Print Save Points
                 16 - Show Active Load-Balancing Hashes
                 17 - Permanence Mode
                 18 - Rule Storage Mode
                 19 - Temperature and Fans
                 20 - ID LED Status
                 21 - OS and CPU Load Averages
                 22 - TCAM Flows
                 23 - Memory Usage
                 24 - CCH Server Revision
                 25 - Web Log
                 26 - Users
                 27 - UAC
                 28 - RADIUS settings
                 29 - DNS settings
                 30 - Telnet service status
                 31 - Go back to Top Menu \n'''
        choice = raw_input('Enter the number of the selection to check: ')
        try:
            choice = int(choice)
        except:
            checkmenu()
        if choice == 1:
            version = packetmaster.firmware_version()
            print version
            topmenu()
        elif choice == 2:
            ip = packetmaster.ip_config()
            print ip
            topmenu()
        elif choice == 3:
            model = packetmaster.device_model()
            print model
            topmenu()
        elif choice == 4:
            label = packetmaster.device_label()
            print label
            topmenu()
        elif choice == 5:
            serial = packetmaster.serial_number()
            print serial
            topmenu()
        elif choice == 6:
            gen = packetmaster.hardware_generation()
            print gen
            topmenu()
        elif choice == 7:
            config = packetmaster.port_config()
            print config
            topmenu()
        elif choice == 8:
            info = packetmaster.port_info()
            print info
            topmenu()
        elif choice == 9:
            stat = packetmaster.port_statistics()
            print stat
            topmenu()
        elif choice == 10:
            sfp = packetmaster.sfp_info()
            print sfp
            topmenu()
        elif choice == 11:
            rules_active = packetmaster.rules_active()
            print rules_active
            topmenu()
        elif choice == 12:
            groups_active = packetmaster.groups_active()
            print groups_active
            topmenu()
        elif choice == 13:
            apps = packetmaster.device_apps()
            print apps
            topmenu()
        elif choice == 14:
            appsrun = packetmaster.apps_active()
            print appsrun
            topmenu()
        elif choice == 15:
            saves = packetmaster.save_points()
            print saves
            topmenu()
        elif choice == 16:
            hashes = packetmaster.hash_algorithms()
            print hashes
            topmenu()
        elif choice == 17:
            perm = packetmaster.rule_permanence()
            print perm
            topmenu()
        elif choice == 18:
            storage = packetmaster.storage_mode()
            print storage
            topmenu()
        elif choice == 19:
            env = packetmaster.env_info()
            print env
            topmenu()
        elif choice == 20:
            led = packetmaster.id_led()
            print led
            topmenu()
        elif choice == 21:
            load = packetmaster.load_info()
            print load
            topmenu()
        elif choice == 22:
            tcam = packetmaster.tcam()
            print tcam
            topmenu()
        elif choice == 23:
            memory = packetmaster.mem_free()
            print memory
            topmenu()
        elif choice == 24:
            server = packetmaster.server_revision()
            print server
            topmenu()
        elif choice == 25:
            log = packetmaster.web_log()
            print log
            topmenu()
        elif choice == 26:
            users = packetmaster.get_users()
            print users
            topmenu()
        elif choice == 27:
            access = packetmaster.user_uac()
            print access
            topmenu()
        elif choice == 28:
            radius = packetmaster.get_radius()
            print radius
            topmenu()
        elif choice == 29:
            dns = packetmaster.get_dns()
            print dns
            topmenu()
        elif choice == 30:
            telnet = packetmaster.get_telnet()
            print telnet
            topmenu()
        elif choice == 31:
            topmenu()
        else:
            print 'That is not a valid choice \n'
            checkmenu()

    #Change settings menu
    def changemenu():
        print 'Change settings for device at', address,'acting as User', username
        print '''
                 1 - Change IP Configuration
                 2 - Change Device Name + Notes
                 3 - Change Port Configuration
                 4 - Shut Down or Activate Port
                 5 - Reset Port Counters
                 6 - Reset Rule Counters
                 7 - Add Rule
                 8 - Modify Rule
                 9 - Delete Rule
                10 - Delete All Rules
                11 - Add Group
                12 - Modify Group
                13 - Delete Group
                14 - Delete all active groups and associated rules
                15 - Set Load Balancing Group Hash Algorithms
                16 - Activate a save point for ports
                17 - Activate a save point for rules
                18 - Set the rule save point to be loaded on boot
                19 - Export a save point
                20 - Modify a save point for port configuration
                21 - Modify a save point for rules
                22 - Create save point from current port configuration
                23 - Create a quicksave point from current configuration
                24 - Create a save point from current rules
                25 - Delete a port save point
                26 - Delete a rule save point
                27 - Start an App instance
                28 - Kill an App instance
                29 - Call a custom App action
                30 - Rule permanence on/off
                31 - Change Rule Storage Mode
                32 - Delete Web Logs
                33 - Add User
                34 - Modify User
                35 - Delete User
                36 - Enable or Disable UAC
                37 - Configure RADIUS settings
                38 - Enable or Disable HTTPS secure web interface
                39 - Enable or Disable Telnet service
                40 - Set DNS servers
                41 - ID LED on/off
                42 - Restart Web Server
                43 - Reboot Packetmaster
                44 - Go back to Top Menu \n'''
        change = raw_input('Enter the number of the setting you would like to change: ')
        try:
            change = int(change)
        except:
            changemenu()
        if change == 1:
            ipchange = packetmaster.set_ip_config_guided()
            print ipchange
            topmenu()
        elif change == 2:
            namechange = packetmaster.set_label_guided()
            print namechange
            topmenu()
        elif change == 3:
            configchange = packetmaster.set_port_config_guided()
            print configchange
            topmenu()
        elif change == 4:
            onoff = packetmaster.port_on_off_guided()
            print onoff
            topmenu()
        elif change == 5:
            countersdelete = packetmaster.reset_port_counters()
            print countersdelete
            topmenu()
        elif change == 6:
            rulereset = packetmaster.reset_rule_counters()
            print rulereset
            topmenu()
        elif change == 7:
            ruleadd = packetmaster.add_rule_guided()
            print ruleadd
            topmenu()
        elif change == 8:
            modrule = packetmaster.mod_rule_guided()
            print modrule
            topmenu()
        elif change == 9:
            ruledelete = packetmaster.del_rule_guided()
            print ruledelete
            topmenu()
        elif change == 10:
            allruledelete = packetmaster.del_rule_all()
            print allruledelete
            topmenu()
        elif change == 11:
            groupadd = packetmaster.add_group_guided()
            print groupadd
            topmenu()
        elif change == 12:
            modgroup = packetmaster.modify_group_guided()
            print modgroup
            topmenu()
        elif change == 13:
            delgroup = packetmaster.delete_group_guided()
            print delgroup
            topmenu()
        elif change == 14:
            delete_groups = packetmaster.delete_groups_all()
            print delete_groups
            topmenu()
        elif change == 15:
            hashes = packetmaster.set_hash_algorithms_guided()
            print hashes
            topmenu()
        elif change == 16:
            portspactive = packetmaster.set_port_savepoint_guided()
            print portspactive
            topmenu()
        elif change == 17:
            rulespactive = packetmaster.set_rule_savepoint_guided()
            print rulespactive
            topmenu()
        elif change == 18:
            spset = packetmaster.set_boot_savepoint_guided()
            print spset
            topmenu()
        elif change == 19:
            spexport = packetmaster.export_savepoint_guided()
            print spexport
            topmenu()
        elif change == 20:
            portspmod = packetmaster.modify_port_savepoint_guided()
            print portspmod
            topmenu()
        elif change == 21:
            rulepsmod = packetmaster.modify_rule_savepoint_guided()
            print rulepsmod
            topmenu()
        elif change == 22:
            portspcreate = packetmaster.create_port_savepoint_guided()
            print portspcreate
            topmenu()
        elif change == 23:
            quickcreate = packetmaster.create_quick_savepoint()
            print quickcreate
            topmenu()
        elif change == 24:
            rulespcreate = packetmaster.create_rule_savepoint_guided()
            print rulespcreate
            topmenu()
        elif change == 25:
            portspdelete = packetmaster.delete_port_savepoint_guided()
            print portspdelete
            topmenu()
        elif change == 26:
            rulespdelete = packetmaster.delete_rule_savepoint_guided()
            print rulespdelete
            topmenu()
        elif change == 27:
            startapp = packetmaster.start_app_guided()
            print startapp
            topmenu()
        elif change == 28:
            killapp = packetmaster.kill_app_guided()
            print killapp
            topmenu()
        elif change == 29:
            action = packetmaster.call_app_action_guided()
            print action
            topmenu()
        elif change == 30:
            ruleperm = packetmaster.set_rule_permanence_guided()
            print ruleperm
            topmenu()
        elif change == 31:
            storagemode = packetmaster.set_storage_mode_guided()
            print storagemode
            topmenu()
        elif change == 32:
            logdelete = packetmaster.del_web_log()
            print logdelete
            topmenu()
        elif change == 33:
            adduser = packetmaster.add_user_guided()
            print adduser
            topmenu()
        elif change == 34:
            moduser = packetmaster.mod_user_guided()
            print moduser
            topmenu()
        elif change == 35:
            deluser = packetmaster.delete_user_guided()
            print deluser
            topmenu()
        elif change == 36:
            changeaccess = packetmaster.set_uac_guided()
            print changeaccess
            topmenu()
        elif change == 37:
            setradius = packetmaster.set_radius_guided()
            print setradius
            topmenu()
        elif change == 38:
            secure = packetmaster.set_https_guided()
            print secure
            topmenu()
        elif change == 39:
            settelnet = packetmaster.set_telnet_guided()
            print settelnet
            topmenu()
        elif change == 40:
            setdns = packetmaster.set_dns_guided()
            print setdns
            topmenu()
        elif change == 41:
            led = packetmaster.set_id_led_guided()
            print led
            topmenu()
        elif change == 42:
            restartweb = packetmaster.restart_webserver()
            print restartweb
            topmenu()
        elif change == 43:
            restart = packetmaster.reboot()
            print restart
            topmenu()
        elif change == 44:
            topmenu()
        else:
            print 'That is not a valid choice \n'
            changemenu()

    topmenu()
