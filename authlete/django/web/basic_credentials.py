#
# Copyright (C) 2019 Authlete, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific
# language governing permissions and limitations under the
# License.


import base64
import re


class BasicCredentials(object):
    BASIC_PATTERN = re.compile('^Basic *(?P<parameter>[^ ]+) *$', re.I)


    def __init__(self, userId, password):
        self._userId             = userId
        self._password           = password
        self._formattedParameter = self.__class__.__formatParameter(userId, password)
        self._formatted          = 'Basic {}'.format(self._formattedParameter)


    @property
    def userId(self):
        return self._userId


    @property
    def password(self):
        return self._password


    @property
    def formatted(self):
        return self._formatted


    @property
    def formattedParameter(self):
        return self._formattedParameter


    @classmethod
    def __formatParameter(cls, userId, password):
        if userId is None:
            userId = ''

        if password is None:
            password = ''

        plain = '{}:{}'.format(userId, password)

        return cls.__b64encode(plain)


    @classmethod
    def __bytes_io(cls, input, func):
        return func(input.encode('utf-8')).decode('utf-8')


    @classmethod
    def __b64encode(cls, input):
        return cls.__bytes_io(input, base64.b64encode)


    @classmethod
    def __b64decode(cls, input):
        return cls.__bytes_io(input, base64.b64decode)


    @classmethod
    def parse(cls, input):
        """Create a BasicCredentials instance from the given string.

        The format of the input string should be "Basic {base64-encoded-string}".
        If the given string is None or it does not match the pattern, a
        BasicCredentials instance whose userId and password are both None is
        returned.

        Args:
            input (str): The value of the Authorization header.

        Returns:
            authlete.django.web.BasicCredentials
        """

        if input is None:
            # userId = None, password = None
            return BasicCredentials(None, None)

        # Expecting the input matches "Basic {base64string}"
        mo = cls.BASIC_PATTERN.match(input)

        # If the input string does not match the pattern.
        if mo is None:
            # userId = None, password = None
            return BasicCredentials(None, None)

        # BASE64-encoded "userId:password"
        base64string = mo.group('parameter')

        # Build a BasicCredentials instance from the BASE64 string.
        return cls.__buildFromParameter(base64string)


    @classmethod
    def __buildFromParameter(cls, base64string):
        if base64string is None or len(base64string) == 0:
            # userId = None, password = None
            return BasicCredentials(None, None)

        # Decode the BASE64 string
        plain = cls.__b64decode(base64string)

        # Split "userId:password" into "userId" and "password"
        elements = plain.split(':', 2)
        count    = len(elements)

        userId   = None
        password = None

        # User ID
        if 1 <= count:
            userId = elements[0]

        # Password
        if 2 <= count:
            password = elements[1]

        return BasicCredentials(userId, password)
