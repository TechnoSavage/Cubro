#!/usr/bin/python
''' created for testing purpose; creates 1000 TCP filters
    for source ports 1000 through 1999.'''

from sys import argv
from packetmaster_ex_rest import PacketmasterEX

def usage():
    ''' Explain use of script.'''
    print ''' Supply arguments IP address, Username, and Password.
              e.g. mask_test.py 192.168.1.200 admin cubro'''

if __name__ == '__main__':
    if len(argv) <= 0:
        usage()
    else:
        PACKETMASTER = PacketmasterEX(argv[1], argv[2], argv[3])
        for n in range(1000, 2000):
            params = {'name': 'test' + str(n),
                      'priority': 32768,
                      'match[in_port]': '1',
                      'match[protocol]': 'tcp',
                      'match[nw_src]': '131.151.32.129',
                      'match[tcp_src]': n,
                      'actions': 'output:4'}
            result = PACKETMASTER.add_rule(params)
            print result
