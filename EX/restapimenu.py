#Use with firmware version 2.1.x.x or later. Python2.7 Cubro Packetmaster REST API demo.

#!/usr/bin/python

#Import necessary Python libraries for interacting with the REST API
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
                ________  ______  ____  ____     _____  ______ _____ _______   ____   ____   __
               / ____/ / / / __ )/ __ \/ __ \   / __  \/ ____//  __//_  ___/  / __ \ / __ \ / /
              / /   / / / / /_/ / /_/ / / / /  / /_/  / __/  / /__   / /     / /_/ // /_/ // /
             / /___/ /_/ / /_/ / _, _/ /_/ /  / _,  _/ /___  \__  \ / /     / __  //  ___// /
             \____/\____/_____/_/ |_|\____/  /_/ \_\/_____//______//_/     /_/ /_//_/    /_/
           ###################################################################################
        \n'''

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
            3 - Manage Device
            4 - Quit \n'''

        option = raw_input('Enter selection number: ')
        try:
            option = int(option)
        except:
            topmenu()
        if option == 1:
            address = set_ip()
            packetmaster = PacketmasterEX(address, username, password)
            topmenu()
        elif option == 2:
            username = raw_input('Username: ')
            password = getpass()
            packetmaster = PacketmasterEX(address, username, password)
            topmenu()
        elif option == 3:
            manage()
        elif option == 4:
            print 'Goodbye'
            exit()
        else:
            print 'That is not a valid selection \n'
            topmenu()

    def manage():
        print 'Device management menu for device at', address,'acting as User', username
        choice = raw_input('''
                  1 - Hardware Configuration Menu
                  2 - Rule and Port Group Configuration Menu
                  3 - App Configuration Menu
                  4 - Savepoint Configuration Menu
                  5 - User Management Menu
                  6 - Back \n
                 Enter the number of the selection to check: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            manage()
        if choice == 1:
            hardwareconfig()
        elif choice == 2:
            ruleconfig()
        elif choice == 3:
            appconfig()
        elif choice == 4:
            saveconfig()
        elif choice == 5:
            userconfig()
        elif choice == 6:
            topmenu()
        else:
            print "That is not a valid selection."
            manage()

    def hardwareconfig():
        print 'Hardware configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Model
                 2 - Serial Number
                 3 - Hardware Generation
                 4 - Firmware version
                 5 - Temperature and Fans
                 6 - ID LED Status
                 7 - ID LED on/off
                 8 - OS and CPU Load Averages
                 9 - TCAM Flows
                10 - Memory Usage
                11 - CCH Server Revision
                12 - Device Label and Notes Submenu
                13 - IP Configuration Submenu
                14 - DNS Configuration Submenu
                15 - Port Configuration Submenu
                16 - Telnet service submenu
                17 - Webserver Submenu
                18 - Reboot Packetmaster
                19 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            hardwareconfig()
        if choice == 1:
            run = packetmaster.device_model()
            print run
            hardwareconfig()
        elif choice == 2:
            run = packetmaster.serial_number()
            print run
            hardwareconfig()
        elif choice == 3:
            run = packetmaster.hardware_generation()
            print run
            hardwareconfig()
        elif choice == 4:
            run = packetmaster.firmware_version()
            print run
            hardwareconfig()
        elif choice == 5:
            run = packetmaster.env_info()
            print run
            hardwareconfig()
        elif choice == 6:
            run = packetmaster.id_led()
            print run
            hardwareconfig()
        elif choice == 7:
            run = packetmaster.set_id_led_guided()
            print run
            hardwareconfig()
        elif choice == 8:
            run = packetmaster.load_info()
            print run
            hardwareconfig()
        elif choice == 9:
            run = packetmaster.tcam()
            print run
            hardwareconfig()
        elif choice == 10:
            run = packetmaster.mem_free()
            print run
            hardwareconfig()
        elif choice == 11:
            run = packetmaster.server_revision()
            print run
            hardwareconfig()
        elif choice == 12:
            notesmenu()
        elif choice == 13:
            ipconfig()
        elif choice == 14:
            dns()
        elif choice == 15:
            portconfig()
        elif choice == 16:
            telnet()
        elif choice == 17:
            web()
        elif choice == 18:
            run = packetmaster.reboot()
            print run
            hardwareconfig()
        elif choice == 19:
            manage()
        else:
            print "That is not a valid selection."
            hardwareconfig()

    def notesmenu():
        print 'Device label and notes menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get Label and Notes
                 2 - Change Label only
                 3 - Change Label and Notes
                 4 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            notesmenu()
        if choice == 1:
            run = packetmaster.device_label()
            print run
            notesmenu()
        elif choice == 2:
            run = packetmaster.set_name_guided()
            print run
            notesmenu()
        elif choice == 3:
            run = packetmaster.set_label_guided()
            print run
            notesmenu()
        elif choice == 4:
            hardwareconfig()
        else:
            print "That is not a valid selection."
            notes()

    def ipconfig():
        print 'Device label and notes menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get current IP configuration
                 2 - Change IP configuration
                 3 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            ipconfig()
        if choice == 1:
            run = packetmaster.ip_config()
            print run
            ipconfig()
        elif choice == 2:
            run = packetmaster.set_ip_config_guided()
            print run
            ipconfig()
        elif choice == 3:
            hardwareconfig()
        else:
            print "That is not a valid selection."
            ipconfig()

    def dns():
        print 'DNS configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get current DNS configuration
                 2 - Change DNS configuration
                 3 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            dns()
        if choice == 1:
            run = packetmaster.get_dns()
            print run
            dns()
        elif choice == 2:
            run = packetmaster.set_dns_guided()
            print run
            dns()
        elif choice == 3:
            hardwareconfig()
        else:
            print "That is not a valid selection."
            dns()

    def portconfig():
        print 'Port configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get current port configuration
                 2 - Get current port status
                 3 - Get current port counters
                 4 - Get SFP status
                 5 - Change Port Configuration
                 6 - Shut Down or Activate Port
                 7 - Reset Port Counters
                 8 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            portconfig()
        if choice == 1:
            run = packetmaster.port_config()
            print run
            portconfig()
        elif choice == 2:
            run = packetmaster.port_info()
            print run
            portconfig()
        elif choice == 3:
            run = packetmaster.port_statistics()
            print run
            portconfig()
        elif choice == 4:
            run = packetmaster.sfp_info()
            print run
            portconfig()
        elif choice == 5:
            run = packetmaster.set_port_config_guided()
            print run
            portconfig()
        elif choice == 6:
            run = packetmaster.port_on_off_guided()
            print run
            portconfig()
        elif choice == 7:
            run = packetmaster.reset_port_counters()
            print run
            portconfig()
        elif choice == 8:
            hardwareconfig()
        else:
            print "That is not a valid selection."
            portconfig()

    def web():
        print 'Webserver menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Web logs
                 2 - Delete web Logs
                 3 - Restart webserver
                 4 - Enable or Disable HTTPS secure web interface
                 5 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            web()
        if choice == 1:
            run = packetmaster.web_log()
            print run
            web()
        elif choice == 2:
            run = packetmaster.del_web_log()
            print run
            web()
        elif choice == 3:
            run = packetmaster.restart_webserver()
            print run
            web()
        elif choice == 4:
            run = packetmaster.set_https_guided()
            print run
            web()
        elif choice == 5:
            hardwareconfig()
        else:
            print "That is not a valid selection."
            web()

    def telnet():
        print 'Telnet service menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Get current Telnet status
                 2 - Enable or Disable Telnet service
                 3 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            telnet()
        if choice == 1:
            run = packetmaster.get_telnet()
            print run
            telnet()
        elif choice == 2:
            run = packetmaster.set_telnet_guided()
            print run
            telnet()
        elif choice == 3:
            hardwareconfig()
        else:
            print "That is not a valid selection."
            telnet()

    def ruleconfig():
        print 'Rule and Port Group configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - Show Rules and Rule Counters
                 2 - Add Rule
                 3 - Modify Rule
                 4 - Delete Rule
                 5 - Delete All Rules
                 6 - Reset Rule Counters
                 7 - Show Groups
                 8 - Add Group
                 9 - Modify Group
                10 - Delete Group
                11 - Delete all active groups and associated rules
                12 - Show Active Load-Balancing Hashes
                13 - Set Load Balancing Group Hash Algorithms
                14 - Show Rule Permanence Mode
                15 - Set Rule Permanence Mode
                16 - Show Rule Storage Mode
                17 - Set Rule Storage Mode
                18 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            ruleconfig()
        if choice == 1:
            run = packetmaster.rules_active()
            print run
            ruleconfig()
        elif choice == 2:
            run = packetmaster.add_rule_guided()
            print run
            ruleconfig()
        elif choice == 3:
            run = packetmaster.mod_rule_guided()
            print run
            ruleconfig()
        elif choice == 4:
            run = packetmaster.del_rule_guided()
            print run
            ruleconfig()
        elif choice == 5:
            run = packetmaster.del_rule_all()
            print run
            ruleconfig()
        elif choice == 6:
            run = packetmaster.reset_rule_counters()
            print run
            ruleconfig()
        elif choice == 7:
            run = packetmaster.groups_active()
            print run
            ruleconfig()
        elif choice == 8:
            run = packetmaster.add_group_guided()
            print run
            ruleconfig()
        elif choice == 9:
            run = packetmaster.modify_group_guided()
            print run
            ruleconfig()
        elif choice == 10:
            run = packetmaster.delete_group_guided()
            print run
            ruleconfig()
        elif choice == 11:
            run = packetmaster.delete_groups_all()
            print run
            ruleconfig()
        elif choice == 12:
            run = packetmaster.hash_algorithms()
            print run
            ruleconfig()
        elif choice == 13:
            run = packetmaster.set_hash_algorithms_guided()
            print run
            ruleconfig()
        elif choice == 14:
            run = packetmaster.rule_permanence()
            print run
            ruleconfig()
        elif choice == 15:
            run = packetmaster.set_rule_permanence_guided()
            print run
            ruleconfig()
        elif choice == 16:
            run = packetmaster.storage_mode()
            print run
            ruleconfig()
        elif choice == 17:
            run = packetmaster.set_storage_mode_guided()
            print run
            ruleconfig()
        elif choice == 18:
            manage()
        else:
            print "That is not a valid selection."
            ruleconfig()

    def appconfig():
        print 'App configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - List Apps
                 2 - List Running Apps
                 3 - Start an App instance
                 4 - Modify an App instance
                 5 - Kill an App instance
                 6 - Call a custom App action
                 7 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            appconfig()
        if choice == 1:
            run = packetmaster.device_apps()
            print run
            appconfig()
        elif choice == 2:
            run = packetmaster.apps_active()
            print run
            appconfig()
        elif choice == 3:
            run = packetmaster.start_app_guided()
            print run
            appconfig()
        elif choice == 4:
            run = packetmaster.mod_app_guided()
            print run
            appconfig()
        elif choice == 5:
            run = packetmaster.kill_app_guided()
            print run
            appconfig()
        elif choice == 6:
            run = packetmaster.call_app_action_guided()
            print run
            appconfig()
        elif choice == 7:
            manage()
        else:
            print "That is not a valid selection."
            appconfig()

    def saveconfig():
        print 'Save Point configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - List Save Points
                 2 - Activate a save point for ports
                 3 - Activate a save point for rules
                 4 - Set the rule save point to be loaded on boot
                 5 - Export a save point
                 6 - Modify a save point for port configuration
                 7 - Modify a save point for rules
                 8 - Create save point from current port configuration
                 9 - Create a quicksave point from current configuration
                10 - Create a save point from current rules
                11 - Delete a port save point
                12 - Delete a rule save point
                13 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            saveconfig()
        if choice == 1:
            run = packetmaster.save_points()
            print run
            saveconfig()
        elif choice == 2:
            run = packetmaster.set_port_savepoint_guided()
            print run
            saveconfig()
        elif choice == 3:
            run = packetmaster.set_rule_savepoint_guided()
            print run
            saveconfig()
        elif choice == 4:
            run = packetmaster.set_boot_savepoint_guided()
            print run
            saveconfig()
        elif choice == 5:
            run = packetmaster.export_savepoint_guided()
            print run
            saveconfig()
        elif choice == 6:
            run = packetmaster.modify_port_savepoint_guided()
            print run
            saveconfig()
        elif choice == 7:
            run = packetmaster.modify_rule_savepoint_guided()
            print run
            saveconfig()
        elif choice == 8:
            run = packetmaster.create_port_savepoint_guided()
            print run
            saveconfig()
        elif choice == 9:
            run = packetmaster.create_quick_savepoint()
            print run
            saveconfig()
        elif choice == 10:
            run = packetmaster.create_rule_savepoint_guided()
            print run
            saveconfig()
        elif choice == 11:
            run = packetmaster.delete_port_savepoint_guided()
            print run
            saveconfig()
        elif choice == 12:
            run = packetmaster.delete_rule_savepoint_guided()
            print run
            saveconfig()
        elif choice == 13:
            manage()
        else:
            print "That is not a valid selection."
            saveconfig()

    def userconfig():
        print 'User configuration menu for device at', address,'acting as User', username
        choice = raw_input('''
                 1 - List Users
                 2 - Add User
                 3 - Modify User
                 4 - Delete User
                 5 - UAC Status
                 6 - Enable or Disable UAC
                 7 - Show RADIUS Settings
                 8 - Configure RADIUS settings
                 9 - Back \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except:
            print "That is not a valid selection."
            userconfig()
        if choice == 1:
            run = packetmaster.get_users()
            print run
            userconfig()
        elif choice == 2:
            run = packetmaster.add_user_guided()
            print run
            userconfig()
        elif choice == 3:
            run = packetmaster.mod_user_guided()
            print run
            userconfig()
        elif choice == 4:
            run = packetmaster.delete_user_guided()
            print run
            userconfig()
        elif choice == 5:
            run = packetmaster.user_uac()
            print run
            userconfig()
        elif choice == 6:
            run = packetmaster.set_uac_guided()
            print run
            userconfig()
        elif choice == 7:
            run = packetmaster.get_radius()
            print run
            userconfig()
        elif choice == 8:
            run = packetmaster.set_radius_guided()
            print run
            userconfig()
        elif choice == 9:
            manage()
        else:
            print "That is not a valid selection."
            userconfig()
topmenu()
