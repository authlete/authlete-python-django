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


import re
from django.conf import settings


class RequestUtility(object):
    BEARER_PATTERN = re.compile('^Bearer *(?P<parameter>[^ ]+) *$', re.I)


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
