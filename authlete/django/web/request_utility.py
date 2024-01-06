#
# Copyright (C) 2019-2024 Authlete, Inc.
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


import re
import urllib.parse
from django.conf import settings
from authlete.django.web.basic_credentials import BasicCredentials


class RequestUtility(object):
    BEARER_PATTERN = re.compile('^Bearer *(?P<parameter>[^ ]+) *$', re.I)
    DPOP_PATTERN   = re.compile('^DPoP *(?P<parameter>[^ ]+) *$', re.I)


    @classmethod
    def extractQueryString(cls, request):
        return request.META.get('QUERY_STRING')


    @classmethod
    def extractRequestBody(cls, request):
        body = request.body
        if body is None:
            return None

        encoding = request.encoding
        if encoding is None:
            encoding = settings.DEFAULT_CHARSET

        return body.decode(encoding)


    @classmethod
    def extractParameters(cls, request):
        if request.method == 'GET':
            return cls.extractQueryString(request)
        else:
            return cls.extractRequestBody(request)


    @classmethod
    def extractAuthorization(cls, request):
        return request.headers.get('Authorization')


    @classmethod
    def extractBearerToken(cls, request):
        # Get the value of the Authorization header.
        authorization = cls.extractAuthorization(request)
        if authorization is None:
            return None

        # Expecting the value matches "Bearer {token}"
        mo = cls.BEARER_PATTERN.match(authorization)

        # If the value does not match the pattern.
        if mo is None:
            return None

        return mo.group('parameter')


    @classmethod
    def extractDpopToken(cls, request):
        # Get the value of the Authorization header.
        authorization = cls.extractAuthorization(request)
        if authorization is None:
            return None

        # Expecting the value matches "DPoP {token}"
        mo = cls.DPOP_PATTERN.match(authorization)

        # If the value does not match the pattern.
        if mo is None:
            return None

        return mo.group('parameter')


    @classmethod
    def extractAccessToken(cls, request):
        # Try to extract a token from "Bearer {token}"
        accessToken = cls.extractBearerToken(request)
        if accessToken is not None:
            return accessToken

        # Try to extract a token from "DPoP {token}"
        accessToken = cls.extractDpopToken(request)
        if accessToken is not None:
            return accessToken

        # No access token is available.
        return None


    @classmethod
    def extractBasicCredentials(cls, request):
        return BasicCredentials.parse(request.headers.get('Authorization'))


    @classmethod
    def extractClientCert(cls, request):
        # RFC 9440 Client-Cert HTTP Header Field
        clientCert = request.headers.get('Client-Cert')

        if clientCert is not None:
            # The value of 'Client-Cert' should be 'sf-binary', which is
            # defined in RFC 8941 as follows.
            #
            #     sf-binary = ":" *(base64) ":"
            #     base64    = ALPHA / DIGIT / "+" / "/" / "="
            #

            # Remove the colons at the beginning and at the end.
            return clientCert[1:-1]

        # Try a well-known HTTP header, X-Ssl-Cert
        clientCert = request.headers.get('X-Ssl-Cert')

        if clientCert is None:
            return None

        # "(null)" is a value that misconfigured Apache servers will send
        # instead of a missing header. This happens when "SSLOptions" does
        # not include "+ExportCertData".
        if clientCert == '(null)':
            return None

        # Nginx's $ssl_client_escaped_cert holds a urlencoded client
        # certificate in the PEM format.
        if clientCert.startswith('-----BEGIN%20'):
            # URL-decode
            return urllib.parse.unquote(clientCert)

        return clientCert
