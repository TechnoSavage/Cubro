#!/usr/bin/python

""" Monitor the bandwidth utlilization of a Packetmaster on a per port basis
and notify an admin in the event that port utlilization rises above 50%. """

from __future__ import print_function #Requires Python 2.6 or later
from getpass import getpass
import json
from six import moves
from packetmaster_ex_rest import PacketmasterEX
import input_check
