#Use with firmware version 2.2.5 or later. Python2.7 Cubro Packetmaster REST API demo.

#!/usr/bin/python

#Import necessary Python libraries for interacting with the REST API
from getpass import getpass
import re
from packetmaster_ex_rest import PacketmasterEX
# Add code to handle case and verify input in all areas where needed

def set_ip():
    """Validates then sets an IP address for a Cubro PacketmasterEX device."""
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
                ________  ______  ____  ____     _____  ______ _____ _______   ____   ____   __
               / ____/ / / / __ )/ __ \/ __ \   / __  \/ ____//  __//_  ___/  / __ \ / __ \ / /
              / /   / / / / /_/ / /_/ / / / /  / /_/  / __/  / /__   / /     / /_/ // /_/ // /
             / /___/ /_/ / /_/ / _, _/ /_/ /  / _,  _/ /___  \__  \ / /     / __  //  ___// /
             \____/\____/_____/_/ |_|\____/  /_/ \_\/_____//______//_/     /_/ /_//_/    /_/
           ###################################################################################
        \n'''

    #IP address to access REST data of device
    ADDRESS = set_ip()
    #Device credentials
    USERNAME = raw_input('Enter your username: ')
    PASSWORD = getpass()
    #Initialize Packetmaster object
    PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)

    def topmenu():
        """Top menu in hierarchy for device management."""
        global ADDRESS, USERNAME, PASSWORD, PACKETMASTER
        print 'Options for device at', ADDRESS, 'acting as User', USERNAME
        print '''
            1 - Change My working device
            2 - Change My user credentials
            3 - Manage Device
            4 - Quit \n'''

        option = raw_input('Enter selection number: ')
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
            USERNAME = raw_input('Username: ')
            PASSWORD = getpass()
            PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
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
        """Menu for managing Cubro PacketmasterEX device."""
        print 'Device management menu for device at', ADDRESS, 'acting as User', USERNAME
        choice = raw_input('''
                  1 - Hardware Configuration Menu
                  2 - Rule and Port Group Configuration Menu
                  3 - App Configuration Menu
                  4 - Savepoint Configuration Menu
                  5 - User Management Menu
                  6 - Back
                  7 - Quit \n
                 Enter the number of the selection to check: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
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
        elif choice == 7:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            manage()

    def hardwareconfig():
        """Menu for configuring hardware and management related settings."""
        print 'Hardware configuration menu for device at', ADDRESS, 'acting as User', USERNAME
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
                12 - Device OpenFlow Datapath ID
                13 - Set Vitrum License
                14 - Device Label and Notes Submenu
                15 - IP Configuration Submenu
                16 - DNS Configuration Submenu
                17 - Port Configuration Submenu
                18 - Telnet service submenu
                19 - Webserver Submenu
                20 - Controller Submenu
                21 - Reboot Packetmaster
                22 - Back
                23 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            hardwareconfig()
        if choice == 1:
            run = PACKETMASTER.device_model()
            print run
            hardwareconfig()
        elif choice == 2:
            run = PACKETMASTER.serial_number()
            print run
            hardwareconfig()
        elif choice == 3:
            run = PACKETMASTER.hardware_generation()
            print run
            hardwareconfig()
        elif choice == 4:
            run = PACKETMASTER.firmware_version()
            print run
            hardwareconfig()
        elif choice == 5:
            run = PACKETMASTER.env_info()
            print run
            hardwareconfig()
        elif choice == 6:
            run = PACKETMASTER.id_led()
            print run
            hardwareconfig()
        elif choice == 7:
            run = PACKETMASTER.set_id_led_guided()
            print run
            hardwareconfig()
        elif choice == 8:
            run = PACKETMASTER.load_info()
            print run
            hardwareconfig()
        elif choice == 9:
            run = PACKETMASTER.tcam()
            print run
            hardwareconfig()
        elif choice == 10:
            run = PACKETMASTER.mem_free()
            print run
            hardwareconfig()
        elif choice == 11:
            run = PACKETMASTER.server_revision()
            print run
            hardwareconfig()
        elif choice == 12:
            run = PACKETMASTER.get_dpid()
            print run
            hardwareconfig()
        elif choice == 13:
            run = PACKETMASTER.set_license_guided()
            print run
            hardwareconfig()
        elif choice == 14:
            notesmenu()
        elif choice == 15:
            ipconfig()
        elif choice == 16:
            dns()
        elif choice == 17:
            portconfig()
        elif choice == 18:
            telnet()
        elif choice == 19:
            web()
        elif choice == 20:
            controller()
        elif choice == 21:
            run = PACKETMASTER.reboot()
            print run
            hardwareconfig()
        elif choice == 22:
            manage()
        elif choice == 23:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            hardwareconfig()

    def notesmenu():
        """Submenu for device label and device notes settings."""
        print 'Device label and notes menu for device at', ADDRESS, 'acting as User', USERNAME
        choice = raw_input('''
                 1 - Get Label and Notes
                 2 - Change Label only
                 3 - Change Label and Notes
                 4 - Back
                 5 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            notesmenu()
        if choice == 1:
            run = PACKETMASTER.device_label()
            print run
            notesmenu()
        elif choice == 2:
            run = PACKETMASTER.set_name_guided()
            print run
            notesmenu()
        elif choice == 3:
            run = PACKETMASTER.set_label_guided()
            print run
            notesmenu()
        elif choice == 4:
            hardwareconfig()
        elif choice == 5:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            notesmenu()

    def ipconfig():
        """Submenu for IP configuration settings."""
        print 'Device label and notes menu for device at', ADDRESS, 'acting as User', USERNAME
        choice = raw_input('''
                 1 - Get current IP configuration
                 2 - Change IP configuration
                 3 - Back
                 4 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            ipconfig()
        if choice == 1:
            run = PACKETMASTER.ip_config()
            print run
            ipconfig()
        elif choice == 2:
            run = PACKETMASTER.set_ip_config_guided()
            print run
            ipconfig()
        elif choice == 3:
            hardwareconfig()
        elif choice == 4:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            ipconfig()

    def dns():
        """Submenu for DNS settings."""
        print 'DNS configuration menu for device at', ADDRESS, 'acting as User', USERNAME
        choice = raw_input('''
                 1 - Get current DNS configuration
                 2 - Change DNS configuration
                 3 - Back
                 4 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            dns()
        if choice == 1:
            run = PACKETMASTER.get_dns()
            print run
            dns()
        elif choice == 2:
            run = PACKETMASTER.set_dns_guided()
            print run
            dns()
        elif choice == 3:
            hardwareconfig()
        elif choice == 4:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            dns()

    def portconfig():
        """Submenu for port configuration settings."""
        print ''' Port Configuration Menu
        for device at %s acting as User %s''' % (ADDRESS, USERNAME)
        choice = raw_input('''
                 1 - Get current port configuration
                 2 - Get current port status
                 3 - Get current port counters
                 4 - Get SFP status
                 5 - Change Port Configuration
                 6 - Shut Down or Activate Port
                 7 - Reset Port Counters
                 8 - Back
                 9 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            portconfig()
        if choice == 1:
            run = PACKETMASTER.port_config()
            print run
            portconfig()
        elif choice == 2:
            run = PACKETMASTER.port_info()
            print run
            portconfig()
        elif choice == 3:
            run = PACKETMASTER.port_statistics()
            print run
            portconfig()
        elif choice == 4:
            run = PACKETMASTER.sfp_info()
            print run
            portconfig()
        elif choice == 5:
            run = PACKETMASTER.set_port_config_guided()
            print run
            portconfig()
        elif choice == 6:
            run = PACKETMASTER.port_on_off_guided()
            print run
            portconfig()
        elif choice == 7:
            run = PACKETMASTER.reset_port_counters()
            print run
            portconfig()
        elif choice == 8:
            hardwareconfig()
        elif choice == 9:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            portconfig()

    def web():
        """Submenu for Web Server settings."""
        print ''' Webserver Menu
        for device at %s acting as User %s ''' % (ADDRESS, USERNAME)
        choice = raw_input('''
                 1 - Web logs
                 2 - Delete web Logs
                 3 - Restart webserver
                 4 - Enable or Disable HTTPS secure web interface
                 5 - Back
                 6 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            web()
        if choice == 1:
            run = PACKETMASTER.web_log()
            print run
            web()
        elif choice == 2:
            run = PACKETMASTER.del_web_log()
            print run
            web()
        elif choice == 3:
            run = PACKETMASTER.restart_webserver()
            print run
            web()
        elif choice == 4:
            run = PACKETMASTER.set_https_guided()
            print run
            web()
        elif choice == 5:
            hardwareconfig()
        elif choice == 6:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            web()

    def telnet():
        """Submneu for Telnet service settings."""
        print ''' Telnet Service Menu
        for device at %s acting as User %s''' % (ADDRESS, USERNAME)
        choice = raw_input('''
                 1 - Get current Telnet status
                 2 - Enable or Disable Telnet service
                 3 - Back
                 4 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            telnet()
        if choice == 1:
            run = PACKETMASTER.get_telnet()
            print run
            telnet()
        elif choice == 2:
            run = PACKETMASTER.set_telnet_guided()
            print run
            telnet()
        elif choice == 3:
            hardwareconfig()
        elif choice == 4:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            telnet()

    def controller():
        """Submenu for Vitrum Controller settings."""
        print '''   Controller Configuration Menu
        for device at %s acting as User %s''' % (ADDRESS, USERNAME)
        choice = raw_input('''
                 1 - Get current Controller configuration
                 2 - Configure Controller
                 3 - Delete Controller
                 4 - Back
                 5 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            controller()
        if choice == 1:
            run = PACKETMASTER.get_controller()
            print run
            controller()
        elif choice == 2:
            run = PACKETMASTER.set_controller_guided()
            print run
            controller()
        elif choice == 3:
            run = PACKETMASTER.del_controller_guided()
            print run
            controller()
        elif choice == 4:
            hardwareconfig()
        elif choice == 5:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            controller()


    def ruleconfig():
        """Menu for configuring rules/filters and port groups."""
        print '''   Rule and Port Group configuration menu
        for device at %s acting as User %s''' % (ADDRESS, USERNAME)
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
                18 - Back
                19 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            ruleconfig()
        if choice == 1:
            run = PACKETMASTER.rules_active()
            print run
            ruleconfig()
        elif choice == 2:
            run = PACKETMASTER.add_rule_guided()
            print run
            ruleconfig()
        elif choice == 3:
            run = PACKETMASTER.mod_rule_guided()
            print run
            ruleconfig()
        elif choice == 4:
            run = PACKETMASTER.del_rule_guided()
            print run
            ruleconfig()
        elif choice == 5:
            run = PACKETMASTER.del_rule_all()
            print run
            ruleconfig()
        elif choice == 6:
            run = PACKETMASTER.reset_rule_counters()
            print run
            ruleconfig()
        elif choice == 7:
            run = PACKETMASTER.groups_active()
            print run
            ruleconfig()
        elif choice == 8:
            run = PACKETMASTER.add_group_guided()
            print run
            ruleconfig()
        elif choice == 9:
            run = PACKETMASTER.modify_group_guided()
            print run
            ruleconfig()
        elif choice == 10:
            run = PACKETMASTER.delete_group_guided()
            print run
            ruleconfig()
        elif choice == 11:
            run = PACKETMASTER.delete_groups_all()
            print run
            ruleconfig()
        elif choice == 12:
            run = PACKETMASTER.hash_algorithms()
            print run
            ruleconfig()
        elif choice == 13:
            run = PACKETMASTER.set_hash_algorithms_guided()
            print run
            ruleconfig()
        elif choice == 14:
            run = PACKETMASTER.rule_permanence()
            print run
            ruleconfig()
        elif choice == 15:
            run = PACKETMASTER.set_rule_permanence_guided()
            print run
            ruleconfig()
        elif choice == 16:
            run = PACKETMASTER.storage_mode()
            print run
            ruleconfig()
        elif choice == 17:
            run = PACKETMASTER.set_storage_mode_guided()
            print run
            ruleconfig()
        elif choice == 18:
            manage()
        elif choice == 19:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            ruleconfig()

    def appconfig():
        """Menu for configuring App settings."""
        print 'App configuration menu for device at', ADDRESS, 'acting as User', USERNAME
        choice = raw_input('''
                 1 - List Apps
                 2 - List Running Apps
                 3 - Start an App instance
                 4 - Modify an App instance
                 5 - Kill an App instance
                 6 - Call a custom App action
                 7 - Back
                 8 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            appconfig()
        if choice == 1:
            run = PACKETMASTER.device_apps()
            print run
            appconfig()
        elif choice == 2:
            run = PACKETMASTER.apps_active()
            print run
            appconfig()
        elif choice == 3:
            run = PACKETMASTER.start_app_guided()
            print run
            appconfig()
        elif choice == 4:
            run = PACKETMASTER.mod_app_guided()
            print run
            appconfig()
        elif choice == 5:
            run = PACKETMASTER.kill_app_guided()
            print run
            appconfig()
        elif choice == 6:
            run = PACKETMASTER.call_app_action_guided()
            print run
            appconfig()
        elif choice == 7:
            manage()
        elif choice == 8:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            appconfig()

    def saveconfig():
        """Menu for save point configuration settings."""
        print 'Save Point configuration menu for device at', ADDRESS, 'acting as User', USERNAME
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
                13 - Back
                14 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            saveconfig()
        if choice == 1:
            run = PACKETMASTER.save_points()
            print run
            saveconfig()
        elif choice == 2:
            run = PACKETMASTER.set_port_savepoint_guided()
            print run
            saveconfig()
        elif choice == 3:
            run = PACKETMASTER.set_rule_savepoint_guided()
            print run
            saveconfig()
        elif choice == 4:
            run = PACKETMASTER.set_boot_savepoint_guided()
            print run
            saveconfig()
        elif choice == 5:
            run = PACKETMASTER.export_savepoint_guided()
            print run
            saveconfig()
        elif choice == 6:
            run = PACKETMASTER.modify_port_savepoint_guided()
            print run
            saveconfig()
        elif choice == 7:
            run = PACKETMASTER.modify_rule_savepoint_guided()
            print run
            saveconfig()
        elif choice == 8:
            run = PACKETMASTER.create_port_savepoint_guided()
            print run
            saveconfig()
        elif choice == 9:
            run = PACKETMASTER.create_quick_savepoint()
            print run
            saveconfig()
        elif choice == 10:
            run = PACKETMASTER.create_rule_savepoint_guided()
            print run
            saveconfig()
        elif choice == 11:
            run = PACKETMASTER.delete_port_savepoint_guided()
            print run
            saveconfig()
        elif choice == 12:
            run = PACKETMASTER.delete_rule_savepoint_guided()
            print run
            saveconfig()
        elif choice == 13:
            manage()
        elif choice == 14:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            saveconfig()

    def userconfig():
        """Menu for user account related settings."""
        print 'User configuration menu for device at', ADDRESS, 'acting as User', USERNAME
        choice = raw_input('''
                 1 - List Users
                 2 - Add User
                 3 - Modify User
                 4 - Delete User
                 5 - UAC Status
                 6 - Enable or Disable UAC
                 7 - Show RADIUS Settings
                 8 - Configure RADIUS settings
                 9 - Back
                10 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print ("That is not a valid selection.", reason)
            userconfig()
        if choice == 1:
            run = PACKETMASTER.get_users()
            print run
            userconfig()
        elif choice == 2:
            run = PACKETMASTER.add_user_guided()
            print run
            userconfig()
        elif choice == 3:
            run = PACKETMASTER.mod_user_guided()
            print run
            userconfig()
        elif choice == 4:
            run = PACKETMASTER.delete_user_guided()
            print run
            userconfig()
        elif choice == 5:
            run = PACKETMASTER.user_uac()
            print run
            userconfig()
        elif choice == 6:
            run = PACKETMASTER.set_uac_guided()
            print run
            userconfig()
        elif choice == 7:
            run = PACKETMASTER.get_radius()
            print run
            userconfig()
        elif choice == 8:
            run = PACKETMASTER.set_radius_guided()
            print run
            userconfig()
        elif choice == 9:
            manage()
        elif choice == 10:
            print 'Goodbye'
            exit()
        else:
            print "That is not a valid selection."
            userconfig()
topmenu()
