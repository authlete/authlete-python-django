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


from authlete.django.handler.base_request_handler import BaseRequestHandler
from authlete.django.web.request_utility          import RequestUtility
from authlete.django.web.response_utility         import ResponseUtility
from authlete.dto.standard_introspection_action   import StandardIntrospectionAction
from authlete.dto.standard_introspection_request  import StandardIntrospectionRequest


class IntrospectionRequestHandler(BaseRequestHandler):
    """Handler for requests to an introspection endpoint (RFC 7662).
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def handle(self, request):
        """Handle an introspection request.

        This method calls Authlete's /api/auth/introspection/starndard API.

        Args:
            request (django.http.HttpRequest)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Request parameters in the request body.
        params = RequestUtility.extractRequestBody(request)

        # Call Authlete's /api/auth/introspection/standard API.
        res = self.__callStandardIntrospectionApi(params)

        # 'action' in the response denotes the next action which the
        # implementation of the introspection endpoint should take.
        action = res.action

        # The content of the response to the client application.
        content = res.responseContent

        if action == StandardIntrospectionAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        elif action == StandardIntrospectionAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content)
        elif action == StandardIntrospectionAction.OK:
            # 200 OK
            return ResponseUtility.okJson(content)
        else:
            # 500 Internal Server Error
            # /api/auth/introspection/standard API returns an unknown action.
            return self.unknownAction('/api/auth/introspection/standard')


    def __callStandardIntrospectionApi(self, parameters):
        if parameters is None:
            # Authlete returns different error coes for None and an empty
            # string. None is regarded as a caller's error. An empty string
            # is regarded as a client application's error.
            parameters = ''

        # Create a request for /api/auth/introspection/standard API.
        req = StandardIntrospectionRequest()
        req.parameters = parameters

        # Call /api/auth/introspection/standard API.
        return self.api.standardIntrospection(req)
