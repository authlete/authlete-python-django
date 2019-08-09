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
from authlete.django.web.basic_credentials        import BasicCredentials
from authlete.django.web.request_utility          import RequestUtility
from authlete.django.web.response_utility         import ResponseUtility
from authlete.dto.revocation_action               import RevocationAction
from authlete.dto.revocation_request              import RevocationRequest


class RevocationRequestHandler(BaseRequestHandler):
    """Handler for revocation requests to a revocation endpoint (RFC 7009).
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def handle(self, request):
        """Handle a revocation request.

        This method calls Authlete's /api/auth/revocation API.

        Args:
            request (django.http.HttpRequest)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Request Body and Authorization Header
        params = RequestUtility.extractRequestBody(request)
        auth   = RequestUtility.extractAuthorization(request)

        # BasicCredentials that represents the value of the Authorization header.
        credentials = self.__parseCredentials(auth)

        # Call Authlete's /api/auth/revocation API.
        res = self.__callRevocationApi(params, credentials)

        # 'action' in the response denotes the next action which the
        # implementation of the revocation endpoint should take.
        action = res.action

        # The content of the response to the client application.
        content = res.responseContent

        if action == RevocationAction.INVALID_CLIENT:
            # 401 Unauthorized.
            return ResponseUtility.unauthorized(
                'Basic realm="revocation"', content)
        elif action == RevocationAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        elif action == RevocationAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content)
        elif action == RevocationAction.OK:
            # 200 OK
            return ResponseUtility.okJavaScript(content)
        else:
            # 500 Internal Server Error
            # /api/auth/revocation API returns an unknown action.
            return self.unknownAction('/api/auth/revocation')


    def __parseCredentials(self, auth):
        if isinstance(auth, BasicCredentials):
            return auth

        if isinstance(auth, str):
            return BasicCredentials.parse(auth)

        # userId = None, password = None
        return BasicCredentials(None, None)


    def __callRevocationApi(self, parameters, credentials):
        if parameters is None:
            # Authlete returns different error coes for None and an empty
            # string. None is regarded as a caller's error. An empty string
            # is regarded as a client application's error.
            parameters = ''

        # Create a request for /api/auth/revocation API.
        req = RevocationRequest()
        req.parameters   = parameters
        req.clientId     = credentials.userId
        req.clientSecret = credentials.password

        # Call /api/auth/revocation API.
        return self.api.revocation(req)
