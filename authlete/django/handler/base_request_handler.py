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


from authlete.django.web.response_utility import ResponseUtility


class BaseRequestHandler(object):
    """The base class for request handlers.
    """


    def __init__(self, api):
        self._api = api


    @property
    def api(self):
        return self._api


    def unknownAction(self, apiPath):
        """Create a response indicating that an unknown action was received.

        Args:
            apiPath (str) : The path of an Authlete API.

        Returns:
            django.http.HttpResponse
        """

        content = \
            '{"error":"server_error","error_description":"Authlete\'s " + \
            "{} API returned an unknown action."}'.format(apiPath)

        return ResponseUtility.internalServerError(content)
