#!/usr/bin/python

""" Use with firmware version 2.2.5 or later. 
Cubro Packetmaster REST API demo. Menu driven interface for interacting with
a Cubro Packetmaster via the REST API. """

#Import necessary Python libraries for interacting with the REST API
from __future__ import print_function #Requires Python 2.6 or later
from getpass import getpass
from six import moves
import input_check
from packetmaster_ex_rest import PacketmasterEX
# Add code to handle case and verify input in all areas where needed

def set_ip():
    """Validates then sets an IP address for a Cubro PacketmasterEX device."""
    fail_count = 0
    while fail_count < 3:
        address = moves.input('What is the IP address of the Packetmaster you want to access?: ')
        if input_check.ipv4(address) != 0:
            address = input_check.ipv4(address)
            return address
        else:
            print("That is not a valid IPv4 address.")
            fail_count += 1
    print("That is not a valid IPv4 address.  Exiting")
    exit()

if __name__ == '__main__':
    #Welcome statement
    print('''
                ________  ______  ____  ____     _____  ______ _____ _______   ____   ____   __
               / ____/ / / / __ )/ __ \/ __ \   / __  \/ ____//  __//_  ___/  / __ \ / __ \ / /
              / /   / / / / /_/ / /_/ / / / /  / /_/  / __/  / /__   / /     / /_/ // /_/ // /
             / /___/ /_/ / /_/ / _, _/ /_/ /  / _,  _/ /___  \__  \ / /     / __  //  ___// /
             \____/\____/_____/_/ |_|\____/  /_/ \_\/_____//______//_/     /_/ /_//_/    /_/
           ###################################################################################
        \n''')

    #IP address to access REST data of device
    ADDRESS = set_ip()
    #Device credentials
    USERNAME = moves.input('Enter your username: ')
    PASSWORD = getpass()
    #Initialize Packetmaster object
    PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)

    def topmenu():
        """Top menu in hierarchy for device management."""
        global ADDRESS, USERNAME, PASSWORD, PACKETMASTER
        try:
            print('\nOptions for %s at %s acting as user %s' % (PACKETMASTER.model, ADDRESS, USERNAME))
        except AttributeError as error:
            exit()
        print('''
            1 - Change My working device
            2 - Change My user credentials
            3 - Manage Device
            4 - Quit \n''')

        option = moves.input('Enter selection number: ')
        try:
            option = int(option)
        except ValueError as reason:
            print(reason)
            topmenu()
        if option == 1:
            ADDRESS = set_ip()
            PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
            topmenu()
        elif option == 2:
            USERNAME = moves.input('Username: ')
            PASSWORD = getpass()
            PACKETMASTER = PacketmasterEX(ADDRESS, USERNAME, PASSWORD)
            topmenu()
        elif option == 3:
            manage()
        elif option == 4:
            print('Goodbye')
            exit()
        else:
            print('That is not a valid selection \n')
            topmenu()

    def manage():
        """Menu for managing Cubro PacketmasterEX device."""
        print('''\n%s at %s acting as user %s
\nDevice Management Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
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
            print("That is not a valid selection.", reason)
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
            print("That is not a valid selection.", reason)
            manage()

    def hardwareconfig():
        """Menu for configuring hardware and management related settings."""
        print('''\n%s at %s acting as user %s
\nHardware Configuration Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Model
                 2 - Serial Number
                 3 - Hardware Generation
                 4 - Firmware version
                 5 - API Level
                 6 - Temperature and Fans
                 7 - ID LED Status
                 8 - ID LED on/off
                 9 - OS and CPU Load Averages
                10 - TCAM Flows
                11 - Memory Usage
                12 - CCH Server Revision
                13 - Device OpenFlow Datapath ID
                14 - Set Vitrum License
                15 - Device Label and Notes Submenu
                16 - IP Configuration Submenu
                17 - DNS Configuration Submenu
                18 - Port Configuration Submenu
                19 - Telnet service submenu
                20 - Webserver Submenu
                21 - Controller Submenu
                22 - Reboot Packetmaster
                23 - Back
                24 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            hardwareconfig()
        execute = {1: PACKETMASTER.device_model,
                   2: PACKETMASTER.serial_number,
                   3: PACKETMASTER.hardware_generation,
                   4: PACKETMASTER.firmware_version,
                   5: PACKETMASTER.api_level,
                   6: PACKETMASTER.env_info,
                   7: PACKETMASTER.id_led,
                   8: PACKETMASTER.set_id_led_guided,
                   9: PACKETMASTER.load_info,
                   10: PACKETMASTER.tcam,
                   11: PACKETMASTER.mem_free,
                   12: PACKETMASTER.server_revision,
                   13: PACKETMASTER.get_dpid,
                   14: PACKETMASTER.set_license_guided,
                   15: notesmenu,
                   16: ipconfig,
                   17: dns,
                   18: portconfig,
                   19: telnet,
                   20: web,
                   21: controller,
                   22: PACKETMASTER.reboot,
                   23: manage,
                   24: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print(run)
                hardwareconfig()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            hardwareconfig()

    def notesmenu():
        """Submenu for device label and device notes settings."""
        print('''\n%s at %s acting as user %s
\nDevice Label and Notes Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Get Label and Notes
                 2 - Change Label only
                 3 - Change Label and Notes
                 4 - Back
                 5 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
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
                print(run)
                notesmenu()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            notesmenu()

    def ipconfig():
        """Submenu for IP configuration settings."""
        print('''\n%s at %s acting as user %s
\nIP Configuration Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Get current IP configuration
                 2 - Change IP configuration
                 3 - Back
                 4 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            ipconfig()
        execute = {1: PACKETMASTER.ip_config,
                   2: PACKETMASTER.set_ip_config_guided,
                   3: hardwareconfig,
                   4: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print(run)
                ipconfig()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            ipconfig()

    def dns():
        """Submenu for DNS settings."""
        print('''\n%s at %s acting as user %s
\nDNS Configuration Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Get current DNS configuration
                 2 - Change DNS configuration
                 3 - Back
                 4 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            dns()
        execute = {1: PACKETMASTER.get_dns,
                   2: PACKETMASTER.set_dns_guided,
                   3: hardwareconfig,
                   4: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print(run)
                dns()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            dns()

    def portconfig():
        """Submenu for port configuration settings."""
        print('''\n%s at %s acting as user %s
\nPort Configuration Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
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
            print("That is not a valid selection.", reason)
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
                print(run)
                portconfig()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            portconfig()

    def web():
        """Submenu for Web Server settings."""
        print('''\n%s at %s acting as user %s
\nWebserver Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
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
            print("That is not a valid selection.", reason)
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
                print(run)
                web()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            web()

    def telnet():
        """Submneu for Telnet service settings."""
        print('''\n%s at %s acting as user %s
\nTelnet Service Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Get current Telnet status
                 2 - Enable or Disable Telnet service
                 3 - Back
                 4 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            telnet()
        execute = {1: PACKETMASTER.get_telnet,
                   2: PACKETMASTER.set_telnet_guided,
                   3: hardwareconfig,
                   4: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print(run)
                telnet()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            telnet()

    def controller():
        """Submenu for Vitrum Controller settings."""
        print('''\n%s at %s acting as user %s
\nController Configuration Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Get current Controller configuration
                 2 - Configure Controller
                 3 - Delete Controller
                 4 - Back
                 5 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
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
                print(run)
                controller()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            controller()

    def ruleconfig():
        """Menu for configuring rules/filters and port groups."""
        print('''\n%s at %s acting as user %s
\nRule and Port Group Configuration Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
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
            print("That is not a valid selection.", reason)
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
                print(run)
                ruleconfig()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            ruleconfig()

    def appconfig():
        """Menu for configuring App settings."""
        print('''\n%s at %s acting as user %s
\nApp Configuration Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
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
            print("That is not a valid selection.", reason)
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
                print(run)
                appconfig()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            appconfig()

    def saveconfig():
        """Menu for save point configuration settings."""
        print('''\n%s at %s acting as user %s
\nSave Point Configuration Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
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
            print("That is not a valid selection.", reason)
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
                print(run)
                saveconfig()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            saveconfig()

    def userconfig():
        """Menu for user account related settings."""
        print('''\n%s at %s acting as user %s
\nUser Configuration Menu''' % (PACKETMASTER.model, ADDRESS, USERNAME))
        choice = moves.input('''
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
            print("That is not a valid selection.", reason)
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
                print(run)
                userconfig()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            userconfig()
topmenu()
