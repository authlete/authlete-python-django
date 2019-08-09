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


import unittest
from authlete.django.web.basic_credentials import BasicCredentials


class TestBasicCredentials(unittest.TestCase):
    def setUp(self):
        self.userId       = "user"
        self.password     = "password"
        self.base64       = "dXNlcjpwYXNzd29yZA=="
        self.basic_base64 = "Basic {}".format(self.base64)


    def test_001(self):
        actual = BasicCredentials(self.userId, self.password).formatted
        self.assertEqual(actual, self.basic_base64)


    def test_002(self):
        actual = BasicCredentials(self.userId, self.password).formattedParameter
        self.assertEqual(actual, self.base64)


    def test_003(self):
        credentials = BasicCredentials.parse(self.basic_base64)
        actual      = credentials.formatted

        self.assertEqual(actual, self.basic_base64)


    def test_004(self):
        header      = "Dummy {}".format(self.base64)
        credentials = BasicCredentials.parse(header)

        self.assertIsNone(credentials.userId)
        self.assertIsNone(credentials.password)
