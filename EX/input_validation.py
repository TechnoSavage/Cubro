#!/usr/bin/python3

""" A collection of functions to perform input validation on various arguments
passed to the Packetmaster ReST API. """

import re
from datetime import datetime

def mac(test):
    '''Check for valid MAC address.
       
       :param test: A string, string to test if valid MAC address format.
       :returns: A string, if input contains a regular expression match the first match is returned.
       :returns: An int, if input contains no valid MAC address format 0 is returned.
       :raises: TypeError: if regular expression match cannot be run on test variable.'''
    try:
        mac = re.findall("((?:[\da-fA-F]{2}[:\-]){5}[\da-fA-F]{2})", test)
        if len(mac) == 1:
            return mac[0]
    except TypeError as reason:
        log_event(reason)
        return 0
    return 0

def vlan(test):
    '''Check for valid VLAN tag number.
    
       :param test: A string or int, input to test if valid VLAN number.
       :returns: A bool, True is valid VLAN, False if not.
       :raises: ValueError: if test variable cannot be converted to int.'''
    try:
        test = int(test)
        if test in range(0, 4097):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def vlan_pri(test):
    '''Check for valid VLAN priority number.
    
       :param test: A string or int, input to test for valid VLAN priority number.
       :returns: A bool, True if valid; False if invalid.
       :raises: ValueError: if test variable cannot be converted to int.'''
    try:
        test = int(test)
        if test in range(0, 8):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def ipv4(test):
    '''Check for valid IPv4 address and return if found.
    
       :param test: A string, string to test for valid IP address format.
       :returns: A string, if input contains a regular expression match the first match is returned.
       :returns: An int, if input contains no valid IP address format 0 is returned.
       :raises: TypeError: if regular expression match cannot be run on test variable.'''
    try:
        ipv4_address = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', test)
        if len(ipv4_address) == 1:
            return ipv4_address[0]
    except TypeError as reason:
        log_event(reason)
        return 0
    return 0

def ipv4_mask(test):
    '''Check for valid IPv4 address with optional decimal subnet mask.
       
       :param test: A string, string to test for valid IP address and Subnet mask/CIDR format.
       :returns: A string, if input contains a valid match the match is returned in proper format.
       :returns: An int, if input contains no valid IP + subnet/CIDR format 0 is returned.
       :raises: TypeError: if regular expression match cannot be run on test variable.'''
    try:
        ipv4_address = re.findall('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', test)
        if "/" in test and len(ipv4_address) == 1:
            cidr = re.findall('/([1-9][0-9]*)', test)
            if int(cidr[0]) in range(1, 33):
                ipv4_subnet = ipv4_address[0] + '/' + cidr[0]
                return ipv4_subnet
            else:
                pass
        elif len(ipv4_address) == 1:
            return ipv4_address[0]
        elif len(ipv4_address) > 1:
            ipv4_subnet = ipv4_address[0] + '/' + ipv4_address[1]
            return ipv4_subnet
    except TypeError as reason:
        log_event(reason)
        return 0
    return 0

def ipv6(test):
    '''Check for valid IPv6 address and return if found.
    
       :param test: A string, string to test for IPv6 address format.
       :returns: NoneType, this test is not yet implemented.'''
    return None

def port(test):
    '''Test if input is a valid TCP or UDP port number.

       :param test: A string or int, input to check if valid TCP/UDP port number. 
       :returns: A bool, True if valid; False if not.
       :raises: ValueError: if test variable cannot be converted to int.'''
    try:
        test = int(test)
        if test in range(1, 65536):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def pm_pri(test):
    '''Test if input is valid for Packetmaster G1-G4 Rule Priority value.
    
       :param test: A string or int, string or value to test for valid Packetmaster Rule Priority.
       :returns: A bool, True if valid; False if invalid.
       :raises: ValueError: if test variable cannot be converted to int.'''
    try:
        test = int(test)
        if test in range(0, 65536):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def group_id(test):
    '''Test if input is a valid group ID number for the Packetmaster.
    
       :param test: A string or int, string or value to test for valid Group ID.
       :returns: A bool, True if valid, False if invalid.
       :raises: ValueError: if test variable cannot be converted to int.'''
    try:
        test = int(test)
        if test in range(0, 4294967041):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def icmp_type(test):
    '''Test if input is a valid ICMP Type value.
    
       :param test: A string or int, string or value to test for valid ICMP type.
       :returns: A bool, True if valid; False if invalid.
       :raises: ValueError: if test variable cannot be converted to int.'''
    try:
        test = int(test)
        if test in range(0, 256):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def icmp_code(test):
    '''Test if input is a valid ICMP Code value.
    
       :param test: A string or int, string or value to test for valid ICMP Code.
       :returns: A bool, True if valid; False if invalid.
       :raises: ValueError: if test variable cannot be converted to int.'''
    try:
        test = int(test)
        if test in range(0, 16):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def ethertype(test):
    '''Test if input is a valid Ethertype.
    
       :param test: A string, string to test for valid Ethertype.'''
    pass

def log_event(reason):
    '''Write errors to file if logging is enabled.
    
       :param reason: A string, message to be written to file.'''
    #Change logging to True to write errors to log file specified under log_location variable
    logging = False
    #Alter log_location to reflect desired file path and name
    log_location = "pm_rest_log"
    if logging:
        with open(log_location, 'a') as f:
            f.write(datetime.now() + ': ' + reason)