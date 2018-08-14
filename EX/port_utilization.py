#!/usr/bin/python

""" Monitor the bandwidth utlilization of a Packetmaster on a per port basis
and notify an admin in the event that port utlilization rises above 50%. """

from getpass import getpass
import json
from packetmaster_ex_rest import PacketmasterEX
