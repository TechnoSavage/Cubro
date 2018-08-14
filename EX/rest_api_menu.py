#!/usr/bin/python

""" Use with firmware version 2.2.5 or later. Python2.7
Cubro Packetmaster REST API demo. Menu driven interface for interacting with
a Cubro Packetmaster via the REST API. """

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
        menus = {1: hardwareconfig,
                 2: ruleconfig,
                 3: appconfig,
                 4: saveconfig,
                 5: userconfig,
                 6: topmenu,
                 7: exit}
        try:
            select = menus[choice]
            select()
        except KeyError as reason:
            print ("That is not a valid selection.", reason)
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
        execute = {1: PACKETMASTER.device_model,
                   2: PACKETMASTER.serial_number,
                   3: PACKETMASTER.hardware_generation,
                   4: PACKETMASTER.firmware_version,
                   5: PACKETMASTER.env_info,
                   6: PACKETMASTER.id_led,
                   7: PACKETMASTER.set_id_led_guided,
                   8: PACKETMASTER.load_info,
                   9: PACKETMASTER.tcam,
                   10: PACKETMASTER.mem_free,
                   11: PACKETMASTER.server_revision,
                   12: PACKETMASTER.get_dpid,
                   13: PACKETMASTER.set_license_guided,
                   14: notesmenu,
                   15: ipconfig,
                   16: dns,
                   17: portconfig,
                   18: telnet,
                   19: web,
                   20: controller,
                   21: PACKETMASTER.reboot,
                   22: manage,
                   23: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                hardwareconfig()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.device_label,
                   2: PACKETMASTER.set_name_guided,
                   3: PACKETMASTER.set_label_guided,
                   4: hardwareconfig,
                   5: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                notesmenu()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.ip_config,
                   2: PACKETMASTER.set_ip_config_guided,
                   3: hardwareconfig,
                   4: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                ipconfig()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.get_dns,
                   2: PACKETMASTER.set_dns_guided,
                   3: hardwareconfig,
                   4: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                dns()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.port_config,
                   2: PACKETMASTER.port_info,
                   3: PACKETMASTER.port_statistics,
                   4: PACKETMASTER.sfp_info,
                   5: PACKETMASTER.set_port_config_guided,
                   6: PACKETMASTER.port_on_off_guided,
                   7: PACKETMASTER.reset_port_counters,
                   8: hardwareconfig,
                   9: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                portconfig()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.web_log,
                   2: PACKETMASTER.del_web_log,
                   3: PACKETMASTER.restart_webserver,
                   4: PACKETMASTER.set_https_guided,
                   5: hardwareconfig,
                   6: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                web()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.get_telnet,
                   2: PACKETMASTER.set_telnet_guided,
                   3: hardwareconfig,
                   4: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                telnet()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.get_controller,
                   2: PACKETMASTER.set_controller_guided,
                   3: PACKETMASTER.del_controller_guided,
                   4: hardwareconfig,
                   5: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                controller()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.rules_active,
                   2: PACKETMASTER.add_rule_guided,
                   3: PACKETMASTER.mod_rule_guided,
                   4: PACKETMASTER.del_rule_guided,
                   5: PACKETMASTER.del_rule_all,
                   6: PACKETMASTER.reset_rule_counters,
                   7: PACKETMASTER.groups_active,
                   8: PACKETMASTER.add_group_guided,
                   9: PACKETMASTER.mod_group_guided,
                   10: PACKETMASTER.delete_group_guided,
                   11: PACKETMASTER.delete_groups_all,
                   12: PACKETMASTER.hash_algorithms,
                   13: PACKETMASTER.set_hash_algorithms_guided,
                   14: PACKETMASTER.rule_permanence,
                   15: PACKETMASTER.set_rule_permanence_guided,
                   16: PACKETMASTER.storage_mode,
                   17: PACKETMASTER.set_storage_mode_guided,
                   18: manage,
                   19: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                ruleconfig()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.device_apps,
                   2: PACKETMASTER.apps_active,
                   3: PACKETMASTER.start_app_guided,
                   4: PACKETMASTER.mod_app_guided,
                   5: PACKETMASTER.kill_app_guided,
                   6: PACKETMASTER.call_app_action_guided,
                   7: manage,
                   8: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                appconfig()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.save_points,
                   2: PACKETMASTER.set_port_savepoint_guided,
                   3: PACKETMASTER.set_rule_savepoint_guided,
                   4: PACKETMASTER.set_boot_savepoint_guided,
                   5: PACKETMASTER.export_savepoint_guided,
                   6: PACKETMASTER.mod_port_savepoint_guided,
                   7: PACKETMASTER.mod_rule_savepoint_guided,
                   8: PACKETMASTER.create_port_savepoint_guided,
                   9: PACKETMASTER.create_quick_savepoint,
                   10: PACKETMASTER.create_rule_savepoint_guided,
                   11: PACKETMASTER.delete_port_savepoint_guided,
                   12: PACKETMASTER.delete_rule_savepoint_guided,
                   13: manage,
                   14: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                saveconfig()
            except KeyError as reason:
                print reason
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
        execute = {1: PACKETMASTER.get_users,
                   2: PACKETMASTER.add_user_guided,
                   3: PACKETMASTER.mod_user_guided,
                   4: PACKETMASTER.delete_user_guided,
                   5: PACKETMASTER.user_uac,
                   6: PACKETMASTER.set_uac_guided,
                   7: PACKETMASTER.get_radius,
                   8: PACKETMASTER.set_radius_guided,
                   9: manage,
                   10: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print run
                userconfig()
            except KeyError as reason:
                print reason
        else:
            print "That is not a valid selection."
            userconfig()
topmenu()