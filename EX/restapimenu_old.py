#!/usr/bin/python

""" Use with firmware version 2.2.5 or later. Python2.7
Cubro Packetmaster REST API demo. Menu driven interface for interacting with
a Cubro Packetmaster via the REST API. """

#Import necessary Python libraries for interacting with the REST API
import re
from getpass import getpass
from packetmaster_ex_rest import PacketmasterEX
# Add code to handle case and verify input in all areas where needed

def set_ip():
    """ Establish Packetmaster can be reached and set Administrative parameters. """
    fail_count = 0
    while fail_count < 3:
        address = raw_input('What is the IP address of the Packetmaster you want to access?: ')
        try:
            ip_address = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', address)
            address = ip_address[0]
            return address
        except TypeError as reason:
            print ("That is not a valid IPv4 address.", reason)
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
    ADDRESS = set_ip()
    #Device credentials
    USERNAME = raw_input('Enter your username: ')
    PASSWORD = getpass()
    PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
    #Initial menu to check or change settings
    def topmenu():
        """ Top level menu for interacting with Packetmaster. """
        global ADDRESS, USERNAME, PASSWORD, PACKETMASTER
        print 'Options for device at', ADDRESS, 'acting as User', USERNAME
        print '''
            1 - Change My working device
            2 - Change My user credentials
            3 - Check Packetmaster Settings
            4 - Change Packetmaster Settings
            5 - Quit \n'''

        option = raw_input('Enter the number of the action you would like to perform: ')
        try:
            option = int(option)
        except ValueError as reason:
            print reason
            topmenu()
        if option == 1:
            ADDRESS = set_ip()
            PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
            topmenu()
        elif option == 2:
            USERNAME = raw_input('Enter your username: ')
            PASSWORD = getpass()
            PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
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
        """ Menu for querying and checking Packetmaster settings and data. """
        print 'Check settings for device at', ADDRESS, 'acting as User', USERNAME
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
        except ValueError as reason:
            print reason
            checkmenu()
        if choice == 1:
            version = PACKETMASTER.firmware_version()
            print version
            topmenu()
        elif choice == 2:
            ip_address = PACKETMASTER.ip_config()
            print ip_address
            topmenu()
        elif choice == 3:
            model = PACKETMASTER.device_model()
            print model
            topmenu()
        elif choice == 4:
            label = PACKETMASTER.device_label()
            print label
            topmenu()
        elif choice == 5:
            serial = PACKETMASTER.serial_number()
            print serial
            topmenu()
        elif choice == 6:
            gen = PACKETMASTER.hardware_generation()
            print gen
            topmenu()
        elif choice == 7:
            config = PACKETMASTER.port_config()
            print config
            topmenu()
        elif choice == 8:
            info = PACKETMASTER.port_info()
            print info
            topmenu()
        elif choice == 9:
            stat = PACKETMASTER.port_statistics()
            print stat
            topmenu()
        elif choice == 10:
            sfp = PACKETMASTER.sfp_info()
            print sfp
            topmenu()
        elif choice == 11:
            rules_active = PACKETMASTER.rules_active()
            print rules_active
            topmenu()
        elif choice == 12:
            groups_active = PACKETMASTER.groups_active()
            print groups_active
            topmenu()
        elif choice == 13:
            apps = PACKETMASTER.device_apps()
            print apps
            topmenu()
        elif choice == 14:
            appsrun = PACKETMASTER.apps_active()
            print appsrun
            topmenu()
        elif choice == 15:
            saves = PACKETMASTER.save_points()
            print saves
            topmenu()
        elif choice == 16:
            hashes = PACKETMASTER.hash_algorithms()
            print hashes
            topmenu()
        elif choice == 17:
            perm = PACKETMASTER.rule_permanence()
            print perm
            topmenu()
        elif choice == 18:
            storage = PACKETMASTER.storage_mode()
            print storage
            topmenu()
        elif choice == 19:
            env = PACKETMASTER.env_info()
            print env
            topmenu()
        elif choice == 20:
            led = PACKETMASTER.id_led()
            print led
            topmenu()
        elif choice == 21:
            load = PACKETMASTER.load_info()
            print load
            topmenu()
        elif choice == 22:
            tcam = PACKETMASTER.tcam()
            print tcam
            topmenu()
        elif choice == 23:
            memory = PACKETMASTER.mem_free()
            print memory
            topmenu()
        elif choice == 24:
            server = PACKETMASTER.server_revision()
            print server
            topmenu()
        elif choice == 25:
            log = PACKETMASTER.web_log()
            print log
            topmenu()
        elif choice == 26:
            users = PACKETMASTER.get_users()
            print users
            topmenu()
        elif choice == 27:
            access = PACKETMASTER.user_uac()
            print access
            topmenu()
        elif choice == 28:
            radius = PACKETMASTER.get_radius()
            print radius
            topmenu()
        elif choice == 29:
            dns = PACKETMASTER.get_dns()
            print dns
            topmenu()
        elif choice == 30:
            telnet = PACKETMASTER.get_telnet()
            print telnet
            topmenu()
        elif choice == 31:
            topmenu()
        else:
            print 'That is not a valid choice \n'
            checkmenu()

    #Change settings menu
    def changemenu():
        """ Menu for changing Packetmaster settings. """
        print 'Change settings for device at', ADDRESS, 'acting as User', USERNAME
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
                28 - Modify an App instance
                29 - Kill an App instance
                30 - Call a custom App action
                31 - Rule permanence on/off
                32 - Change Rule Storage Mode
                33 - Delete Web Logs
                34 - Add User
                35 - Modify User
                36 - Delete User
                37 - Enable or Disable UAC
                38 - Configure RADIUS settings
                39 - Enable or Disable HTTPS secure web interface
                40 - Enable or Disable Telnet service
                41 - Set DNS servers
                42 - ID LED on/off
                43 - Restart Web Server
                44 - Reboot Packetmaster
                45 - Go back to Top Menu \n'''
        change = raw_input('Enter the number of the setting you would like to change: ')
        try:
            change = int(change)
        except ValueError as reason:
            print reason
            changemenu()
        if change == 1:
            ipchange = PACKETMASTER.set_ip_config_guided()
            print ipchange
            topmenu()
        elif change == 2:
            namechange = PACKETMASTER.set_label_guided()
            print namechange
            topmenu()
        elif change == 3:
            configchange = PACKETMASTER.set_port_config_guided()
            print configchange
            topmenu()
        elif change == 4:
            onoff = PACKETMASTER.port_on_off_guided()
            print onoff
            topmenu()
        elif change == 5:
            countersdelete = PACKETMASTER.reset_port_counters()
            print countersdelete
            topmenu()
        elif change == 6:
            rulereset = PACKETMASTER.reset_rule_counters()
            print rulereset
            topmenu()
        elif change == 7:
            ruleadd = PACKETMASTER.add_rule_guided()
            print ruleadd
            topmenu()
        elif change == 8:
            modrule = PACKETMASTER.mod_rule_guided()
            print modrule
            topmenu()
        elif change == 9:
            ruledelete = PACKETMASTER.del_rule_guided()
            print ruledelete
            topmenu()
        elif change == 10:
            allruledelete = PACKETMASTER.del_rule_all()
            print allruledelete
            topmenu()
        elif change == 11:
            groupadd = PACKETMASTER.add_group_guided()
            print groupadd
            topmenu()
        elif change == 12:
            modgroup = PACKETMASTER.modify_group_guided()
            print modgroup
            topmenu()
        elif change == 13:
            delgroup = PACKETMASTER.delete_group_guided()
            print delgroup
            topmenu()
        elif change == 14:
            delete_groups = PACKETMASTER.delete_groups_all()
            print delete_groups
            topmenu()
        elif change == 15:
            hashes = PACKETMASTER.set_hash_algorithms_guided()
            print hashes
            topmenu()
        elif change == 16:
            portspactive = PACKETMASTER.set_port_savepoint_guided()
            print portspactive
            topmenu()
        elif change == 17:
            rulespactive = PACKETMASTER.set_rule_savepoint_guided()
            print rulespactive
            topmenu()
        elif change == 18:
            spset = PACKETMASTER.set_boot_savepoint_guided()
            print spset
            topmenu()
        elif change == 19:
            spexport = PACKETMASTER.export_savepoint_guided()
            print spexport
            topmenu()
        elif change == 20:
            portspmod = PACKETMASTER.modify_port_savepoint_guided()
            print portspmod
            topmenu()
        elif change == 21:
            rulepsmod = PACKETMASTER.modify_rule_savepoint_guided()
            print rulepsmod
            topmenu()
        elif change == 22:
            portspcreate = PACKETMASTER.create_port_savepoint_guided()
            print portspcreate
            topmenu()
        elif change == 23:
            quickcreate = PACKETMASTER.create_quick_savepoint()
            print quickcreate
            topmenu()
        elif change == 24:
            rulespcreate = PACKETMASTER.create_rule_savepoint_guided()
            print rulespcreate
            topmenu()
        elif change == 25:
            portspdelete = PACKETMASTER.delete_port_savepoint_guided()
            print portspdelete
            topmenu()
        elif change == 26:
            rulespdelete = PACKETMASTER.delete_rule_savepoint_guided()
            print rulespdelete
            topmenu()
        elif change == 27:
            startapp = PACKETMASTER.start_app_guided()
            print startapp
            topmenu()
        elif change == 28:
            modapp = PACKETMASTER.mod_app_guided()
            print modapp
            topmenu()
        elif change == 29:
            killapp = PACKETMASTER.kill_app_guided()
            print killapp
            topmenu()
        elif change == 30:
            action = PACKETMASTER.call_app_action_guided()
            print action
            topmenu()
        elif change == 31:
            ruleperm = PACKETMASTER.set_rule_permanence_guided()
            print ruleperm
            topmenu()
        elif change == 32:
            storagemode = PACKETMASTER.set_storage_mode_guided()
            print storagemode
            topmenu()
        elif change == 33:
            logdelete = PACKETMASTER.del_web_log()
            print logdelete
            topmenu()
        elif change == 34:
            adduser = PACKETMASTER.add_user_guided()
            print adduser
            topmenu()
        elif change == 35:
            moduser = PACKETMASTER.mod_user_guided()
            print moduser
            topmenu()
        elif change == 36:
            deluser = PACKETMASTER.delete_user_guided()
            print deluser
            topmenu()
        elif change == 37:
            changeaccess = PACKETMASTER.set_uac_guided()
            print changeaccess
            topmenu()
        elif change == 38:
            setradius = PACKETMASTER.set_radius_guided()
            print setradius
            topmenu()
        elif change == 39:
            secure = PACKETMASTER.set_https_guided()
            print secure
            topmenu()
        elif change == 40:
            settelnet = PACKETMASTER.set_telnet_guided()
            print settelnet
            topmenu()
        elif change == 41:
            setdns = PACKETMASTER.set_dns_guided()
            print setdns
            topmenu()
        elif change == 42:
            led = PACKETMASTER.set_id_led_guided()
            print led
            topmenu()
        elif change == 43:
            restartweb = PACKETMASTER.restart_webserver()
            print restartweb
            topmenu()
        elif change == 44:
            restart = PACKETMASTER.reboot()
            print restart
            topmenu()
        elif change == 45:
            topmenu()
        else:
            print 'That is not a valid choice \n'
            changemenu()

    topmenu()
