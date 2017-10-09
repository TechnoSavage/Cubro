#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.
#Import necessary Python libraries for interacting with the REST API
#!/usr/bin/python
import requests, json, re
from getpass import getpass
from requests.exceptions import ConnectionError
from packetmasterEX_rest import PacketmasterEX
# Add code to handle case and verify input in all areas where needed


if __name__ == '__main__':
    #Welcome statement
    print '''
        Welcome to my interactive Cubro Packetmaster REST API demo.
        All Packetmaster interaction in this program is accomplished via
        the Cubro REST API. \n'''

    #IP address to access REST data of device
    address = raw_input('What is the IP address of the Packetmaster you want to access?: ')
    #Write a check against valid IPv4 address
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
            address = raw_input('What is the IP address of the Packetmaster you want to access: ')
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
                 19 - Temerature and Fans
                 20 - ID LED Status
                 21 - OS and CPU Load Averages
                 22 - TCAM Flows
                 23 - Memory Usage
                 24 - CCH Server Revision
                 25 - Web Log
                 26 - UAC
                 27 - RADIUS settings
                 28 - DNS settings
                 29 - Telnet service status
                 30 - Go back to Top Menu \n'''
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
            access = packetmaster.user_uac()
            print access
            topmenu()
        elif choice == 27:
            radius = packetmaster.get_radius()
            print radius
            topmenu()
        elif choice == 28:
            dns = packetmaster.get_dns()
            print dns
            topmenu()
        elif choice == 29:
            telnet = packetmaster.get_telnet()
            print telnet
            topmenu()
        elif choice == 30:
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
                 5 - Delete Port Counters
                 6 - Reset Rule Counters
                 7 - Add Rule
                 8 - Add Group
                 9 - Delete all active groups and associated rules
                10 - Set Load Balancing Group Hash Algorithms
                11 - Activate a save point for ports
                12 - Activate a save point for rules
                13 - Set the rule save point to be loaded on boot
                14 - Export a save point
                15 - Modify a save point for port configuration
                16 - Modify a save point for rules
                17 - Create save point from current port configuration
                18 - Create a quicksave point from current configuration
                19 - Create a save point from current rules
                20 - Delete a port save point
                21 - Delete a rule save point
                22 - Call a custom app action
                23 - Rule permanence on/off
                24 - Change Rule Storage Mode
                25 - Delete Web Logs
                26 - Enable of Disable UAC
                27 - Configure RADIUS settings
                28 - Enable or Disable HTTPS secure web interface
                29 - Enable or Disable Telnet service
                30 - Set DNS servers
                31 - ID LED on/off
                32 - Restart Web Server
                33 - Reboot Packetmaster
                34 - Go back to Top Menu \n'''
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
            countersdelete = packetmaster.delete_counters()
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
            groupadd = packetmaster.add_group_guided()
            print groupadd
            topmenu()
        elif change == 9:
            delete_groups = packetmaster.delete_groups_all()
            print delete_groups
            topmenu()
        elif change == 10:
            hashes = packetmaster.set_hash_algorithms_guided()
            print hashes
            topmenu()
        elif change == 11:
            portspactive = packetmaster.set_port_savepoint_guided()
            print portspactive
            topmenu()
        elif change == 12:
            rulespactive = packetmaster.set_rule_savepoint_guided()
            print rulespactive
            topmenu()
        elif change == 13:
            spset = packetmaster.set_boot_savepoint_guided()
            print spset
            topmenu()
        elif change == 14:
            spexport = packetmaster.export_savepoint_guided()
            print spexport
            topmenu()
        elif change == 15:
            portspmod = packetmaster.modify_port_savepoint_guided()
            print portspmod
            topmenu()
        elif change == 16:
            rulepsmod = packetmaster.modify_rule_savepoint_guided()
            print rulepsmod
            topmenu()
        elif change == 17:
            portspcreate = packetmaster.create_port_savepoint_guided()
            print portspcreate
            topmenu()
        elif change == 18:
            quickcreate = packetmaster.create_quick_savepoint()
            print quickcreate
            topmenu()
        elif change == 19:
            rulespcreate = packetmaster.create_rule_savepoint_guided()
            print rulespcreate
            topmenu()
        elif change == 20:
            portspdelete = packetmaster.delete_port_savepoint_guided()
            print portspdelete
            topmenu()
        elif change == 21:
            rulespdelete = packetmaster.delete_rule_savepoint_guided()
            print rulespdelete
            topmenu()
        elif change == 22:
            action = packetmaster.call_app_action_guided()
            print action
            topmenu()
        elif change == 23:
            ruleperm = packetmaster.set_rule_permanence_guided()
            print ruleperm
            topmenu()
        elif change == 24:
            storagemode = packetmaster.set_storage_mode_guided()
            print storagemode
            topmenu()
        elif change == 25:
            logdelete = packetmaster.del_web_log()
            print logdelete
            topmenu()
        elif change == 26:
            changeaccess = packetmaster.set_uac_guided()
            print changeaccess
            topmenu()
        elif change == 27:
            setradius = packetmaster.set_radius_guided()
            print setradius
            topmenu()
        elif change == 28:
            secure = packetmaster.set_https_guided()
            print secure
            topmenu()
        elif change == 29:
            settelnet = packetmaster.set_telnet_guided()
            print settelnet
            topmenu()
        elif change == 30:
            setdns = packetmaster.set_dns_guided()
            print setdns
            topmenu()
        elif change == 31:
            led = packetmaster.set_id_led_guided()
            print led
            topmenu()
        elif change == 32:
            restartweb = packetmaster.restart_webserver()
            print restartweb
            topmenu()
        elif change == 33:
            restart = packetmaster.reboot()
            print restart
            topmenu()
        elif change == 34:
            topmenu()
        else:
            print 'That is not a valid choice \n'
            changemenu()

    topmenu()
