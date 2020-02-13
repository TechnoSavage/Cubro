#!/usr/bin/python

""" Use with firmware version x.x.x or newer of Cubro TAP/AGG/Capture firmware. 
Cubro EXA8 REST API demo. Menu driven interface for interacting with
a Cubro EXA8 via the REST API. """

#Import necessary Python libraries for interacting with the REST API
from __future__ import print_function #Requires Python 2.6 or later
from getpass import getpass
from six import moves
import exa8_input_check
from exa8_rest import SessionmasterEXA8

def set_ip():
    """Validates then sets an IP address for a Cubro EXA8 device."""
    fail_count = 0
    while fail_count < 3:
        address = moves.input('What is the IP address of the EXA8 you want to access?: ')
        if exa8_input_check.ipv4(address) != 0:
            address = exa8_input_check.ipv4(address)
            return address
        else:
            print("That is not a valid IPv4 address.")
            fail_count += 1
    print("That is not a valid IPv4 address. Exiting")
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
    #Initialize SessionmasterEXA8 object
    EXA8 = SessionmasterEXA8(ADDRESS, USERNAME, PASSWORD)

    def topmenu():
        """Top menu in hierarchy for device management."""
        global ADDRESS, USERNAME, PASSWORD, EXA8
        try:
            print('\nOptions for %s at %s acting as user %s' % (EXA8.model, ADDRESS, USERNAME))
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
            EXA8 = SessionmasterEXA8(ADDRESS, USERNAME, PASSWORD)
            topmenu()
        elif option == 2:
            USERNAME = moves.input('Username: ')
            PASSWORD = getpass()
            EXA8 = SessionmasterEXA8(ADDRESS, USERNAME, PASSWORD)
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
        """Menu for managing Cubro SessionmasterEXA8 device."""
        print('''\n%s at %s acting as user %s
\nDevice Management Menu''' % (EXA8.get_model, ADDRESS, USERNAME))
        choice = moves.input('''
                  1 - Hardware Configuration Menu
                  2 - Tapping and Aggregation Configuration Menu
                  3 - Capture File Menu
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
                 2: tapconfig,
                 3: capconfig,
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
\nHardware Configuration Menu''' % (EXA8.get_model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Model
                 2 - Serial Number
                 3 - Image version
                 4 - System Information
                 5 - Memory Usage
                 6 - CCH Server Revision
                 7 - Device Name
                 8 - Change Device Name
                 9 - IP Configuration Submenu
                10 - Port Configuration Submenu
                11 - Reboot EXA8
                12 - Back
                13 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            hardwareconfig()
        execute = {1: EXA8.get_model,
                   2: EXA8.get_serial,
                   3: EXA8.get_imageversion,
                   4: EXA8.get_sysinfo,
                   5: EXA8.get_memusage,
                   6: EXA8.get_serverrevision,
                   7: EXA8.get_name,
                   8: EXA8.set_name,#_guided,
                   9: ipconfig,
                   10: portconfig,
                   11: EXA8.reboot,
                   12: manage,
                   13: exit}
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

    def ipconfig():
        """Submenu for IP configuration settings."""
        print('''\n%s at %s acting as user %s
\nIP Configuration Menu''' % (EXA8.get_model, ADDRESS, USERNAME))
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
        execute = {1: EXA8.get_ip,
                   2: EXA8.set_ip,#_guided,
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

    def portconfig():
        """Submenu for port configuration settings."""
        print('''\n%s at %s acting as user %s
\nPort Configuration Menu''' % (EXA8.get_model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Get inteface names
                 2 - Get current port configuration
                 3 - Get current port information
                 4 - Get port statistics
                 5 - Get SFP status
                 6 - Change port configuration
                 7 - Reset Port Counters
                 8 - Back
                 9 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            portconfig()
        execute = {1: EXA8.get_interfacenames,
                   2: EXA8.get_portconfig,
                   3: EXA8.get_portinfo,
                   4: EXA8.get_portstats,
                   5: EXA8.get_sfpstatus,
                   6: EXA8.set_portconfig,#_guided,
                   7: EXA8.del_stats,
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

    def tapconfig():
        '''Menu for configuring tapping and aggregation sessions.'''
        print('''\n%s at %s acting as user %s
\nTapping and Aggregation Configuration Menu''' % (EXA8.get_model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Retrieve number of active monitoring (tapping) sessions
                 2 - Retrieve active monitoring (tapping) sessions
                 3 - Retrieve VLAN tags for G1-G8 interfaces
                 4 - Retrieve VLAN tags for X1, X2, and Xv interfaces
                 5 - Retrieve tag forwarding status
                 6 - Create a monitor (tapping) session
                 7 - Delete a monitor (tapping) session
                 8 - Set a VLAN tag on G1-G8 interface
                 9 - Set a VLAN tag on X1, X2, or Xv interface
                10 - Remove a VLAN tag on X1, X2, or Xv interface
                11 - Set tag forwarding status
                12 - Back
                13 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            tapconfig()
        execute = {1: EXA8.get_moncount,
                   2: EXA8.get_monsessions,
                   3: EXA8.get_inputagg,
                   4: EXA8.get_outputagg,
                   5: EXA8.get_tagforwarding,
                   6: EXA8.set_monsession,#_guided,
                   7: EXA8.del_monsession,#_guided,
                   8: EXA8.set_inputvlan,#_guided,
                   9: EXA8.set_outputvlan_agg,#_guided,
                   10: EXA8.del_outputvlan_agg,#_guided,
                   11: EXA8.set_tagforwarding,#_guided,
                   12: manage,
                   13: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print(run)
                tapconfig()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            tapconfig()

    def capconfig():
        '''Menu for packet capture operations.'''
        print('''\n%s at %s acting as user %s
\nPacket Capture Configuration Menu''' % (EXA8.get_model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Retrieve list of capture files
                 2 - Start a capture
                 3 - Stop a running capture
                12 - Back
                13 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            capconfig()
        execute = {1: EXA8.get_pcaps,
                   2: EXA8.start_capture,#_guided,
                   3: EXA8.stop_capture,#_guided,
                   12: manage,
                   13: exit}
        if choice in execute:
            try:
                select = execute[choice]
                run = select()
                print(run)
                capconfig()
            except KeyError as reason:
                print(reason)
        else:
            print("That is not a valid selection.")
            capconfig()

    def saveconfig():
        '''Menu for saving and restoring configuration.'''
        print('''\n%s at %s acting as user %s
\nSave and Restore Configuration Menu''' % (EXA8.get_model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Reset device to defaults
                 2 - Save current configuration
                 3 - Restore a configuration
                 4 - Back
                 5 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            saveconfig()
        execute = {1: EXA8.reset,
                   2: EXA8.save_config,#_guided,
                   3: EXA8.restore_config,#_guided,
                   4: manage,
                   5: exit}
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
        '''Menu for configuring user accounts.'''
        print('''\n%s at %s acting as user %s
\nUser Configuration Menu''' % (EXA8.get_model, ADDRESS, USERNAME))
        choice = moves.input('''
                 1 - Back
                 2 - Quit \n
                 Enter selection number: ''')
        try:
            choice = int(choice)
        except ValueError as reason:
            print("That is not a valid selection.", reason)
            userconfig()
        execute = {1: manage,
                   2: exit}
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