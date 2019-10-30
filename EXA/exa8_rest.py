""" EXA8 device class for REST API interaction,
    Use with firmware version x.x.x or newer and Cubro TAP/AGG/Capture firmware."""

from __future__ import print_function #Requires Python 2.6 or later
import json
import re
import requests
from requests.exceptions import ConnectionError
from six import moves
import input_check

class SessionmasterEXA8(object):
    """Object class representing a Cubro Sessionmaster EXA8.

    :param address: A string, Management IP of EXA8.
    :param username: A string, Username of an account on the EXA8.
    :param password: A string, Password for user account.
    """

    def __init__(self, address, username=None, password=None):
        self._address = address
        self.username = username
        self.password = password
        self.session = requests.session()
        self.__https = True
        conn_test = self.conn_test()
        print(conn_test)

    def conn_test(self):
        """Test if device is reachable and assign properties.
        Assigns additional properties.
        """
        try:
            connect = self.login_request()
            if connect == 'Unauthorized':
                return "Invalid Credentials"
            else:
                return "Connection Established"
        except ConnectionError as fail:
            print(fail, 'Attempting connection via HTTP.')
            try:
                self.__https = False
                connect = self.login_request()
                if connect == 'Unauthorized':
                    return "Invalid Credentials"
                else:
                    return "Connection Established"
            except ConnectionError as fail:
                print(fail, 'Device is unreachable.')

    def login_request(self):
        """ Send authenticated login request to retrieve session cookie."""
        if self.__https:
            uri = 'https://' + self._address + '/loginreq?'
        else:
            uri = 'http://' + self._address + '/loginreq?'
        params = {"username": self.username, "password": self.password}
        try:
            response = self.session.post(uri, data=params, verify=False)
            if response == 'Unauthorized':
                return response
            else:
                content = response.content
                data = json.loads(content)
                self.user_id = data['id']
                self.user_role = data['role']
                self.session_cookie = response.cookies
                return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error

    def get_port_info(self):
        """Retrieve port information e.g. status, speed, MAC. """
        if self.__https:
            uri = 'https://' + self._address + '/api/ports/info?'
        else:
            uri = 'http://' + self._address + '/api/ports/info?'
        headers = {"X-Requested-With": "XMLHttpRequest"}
        try:
            response = self.session.get(uri, headers=headers)
            content = response.content
            data = json.loads(content)
            return json.dumps(data, indent=4)
        except ConnectionError as error:
            content = 'No Response'
            raise error







