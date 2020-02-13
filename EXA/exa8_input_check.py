#!/usr/bin/python

""" A collection of fucnctions to perform input validation on arguments passed
to the Sessionmaster EXA8 ReST API. """

import re
from datetime import datetime

def interface(test):
    '''Check if interface argument is a valid interface.
       :param: test, A String, '''
    try:
        if test.lower() in ('g1', 'g2', 'g3', 'g4', 'g5', 'g6', 'g7', 'g8', 'x1', 'x2', 'xv'):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def interface_speed(test):
    '''Check if interface speed argument is valid.'''
    try:
        if test.lower() in ('10m-half', '10m-full', '100m-half', '100m-full', '1g', '10g', 'auto'):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def mon_session(test):
    '''Check if input is a valid monitor session number.'''
    try:
        session = int(test)
        if session in range(1,13):
            return True
        else:
            log_event("Monitor Session number does not exist.")
            return False
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def vlan(test):
    '''Check for valid VLAN tag number.'''
    try:
        test = int(test)
        if test in range(0, 4097):
            return True
    except ValueError as reason:
        log_event(reason)
        return False
    return False

def ipv4(test):
    '''Check for valid IPv4 address and return if found.'''
    try:
        ipv4_address = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', test)
        if len(ipv4_address) == 1:
            return ipv4_address[0]
    except TypeError as reason:
        log_event(reason)
        return 0
    return 0

def ipv4_mask(test):
    '''Check for valid IPv4 address with optional decimal subnet mask.'''
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
    '''Check for valid IPv6 address and return if found.'''
    return None

def log_event(reason):
    '''Write errors to file if logging is enabled.'''
    #Change logging to True to write errors to log file specified under log_location variable
    logging = False
    #Alter log_location to reflect desired file path and name
    log_location = "exa8_rest_log"
    if logging:
        with open(log_location, 'a') as f:
            f.write(datetime.now() + ': ' + reason)
