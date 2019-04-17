#!/usr/bin/python

""" A collection of fucntions to perform input validation on various
 networking parameters. """

import re
#Implement logging
def mac(test):
    '''Check for valid MAC address and return if found.'''
    mac = re.findall("pattern", test)
    return None

def vlan(test):
    '''Check for valid VLAN tag number.'''
    try:
        test = int(test)
        if test in range(0, 4097):
            return True
    except ValueError as reason:
        return False
    return False

def vlan_pri(test):
    '''Check for valid VLAN priority number.'''
    try:
        test = int(test)
        if test in range(0, 8):
            return True
    except ValueError as reason:
        return False
    return False

def ipv4(test):
    '''Check for valid IPv4 address and return if found.'''
    try:
        ipv4_address = re.findall('\A(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$', test)
        if len(ipv4_address) == 1:
            return ipv4_address[0]
    except TypeError as reason:
        return 0
    return 0

def ipv4_mask(test):
    '''Check for valid IPv4 address with optional decimal subnet mask.'''
    try:
        ipv4_address = re.findall('(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)', test)
        if "/" in test and len(ipv4_address) == 1:
            cidr = re.findall('/([1-9][0-9]*)', test)
            print cidr
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
        return 0
    return 0

def ipv6(test):
    '''Check for valid IPv6 address and return if found.'''
    return None

def port(test):
    '''Test if input is a valid port number: return "True" if valid and "False" if not.'''
    try:
        test = int(test)
        if test in range(1, 65536):
            return True
    except ValueError as reason:
        return False
    return False

def pm_pri(test):
    '''Test if input is valid for Packetmaster G1-G4 Rule Priority value.'''
    try:
        test = int(test)
        if test in range(0, 65536):
            return True
    except ValueError as reason:
        return False
    return False

def icmp_type(test):
    '''Test if input is a valid ICMP Type value.'''
    try:
        test = int(test)
        if test in range(0, 256):
            return True
    except ValueError as reason:
        return False
    return False

def icmp_code(test):
    '''Test if input is a valid ICMP Code value.'''
    try:
        test = int(test)
        if test in range(0, 16):
            return True
    except ValueError as reason:
        return False
    return False

def ethertype(test):
    '''Test if input is a valid Ethertype.'''
    pass
