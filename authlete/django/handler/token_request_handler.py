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


from authlete.django.handler.token_request_base_handler import TokenRequestBaseHandler
from authlete.django.web.basic_credentials              import BasicCredentials
from authlete.django.web.request_utility                import RequestUtility
from authlete.django.web.response_utility               import ResponseUtility
from authlete.dto.token_action                          import TokenAction
from authlete.dto.token_fail_reason                     import TokenFailReason
from authlete.dto.token_request                         import TokenRequest


class TokenRequestHandler(TokenRequestBaseHandler):
    """Handler for token requests to a token endpoint.
    """


    def __init__(self, api, spi):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
            spi (authlete.django.handler.spi.TokenRequestHandlerSpi)
        """

        super().__init__(api)
        self._spi = spi


    def handle(self, request):
        """Handle a token request.

        This method calls Authlete's /api/auth/token API and conditionally
        either /api/auth/token/issue API or /api/auth/token/fail API.

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

        # Call Authlete's /api/auth/token API.
        res = self.__callTokenApi(params, credentials)

        # 'action' in the response denotes the next action which the
        # implementation of the token endpoint should take.
        action = res.action

        # The content of the response to the client application.
        content = res.responseContent

        if action == TokenAction.INVALID_CLIENT:
            # 401 Unauthorized.
            return ResponseUtility.unauthorized(
                'Basic realm="token"', content)
        elif action == TokenAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        elif action == TokenAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content)
        elif action == TokenAction.PASSWORD:
            # Process the token request whose flow is "Resource OWner
            # Password Credentials".
            return self.__handlePassword(res)
        elif action == TokenAction.OK:
            # 200 OK
            return ResponseUtility.okJson(content)
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


    def __callTokenApi(self, parameters, credentials):
        if parameters is None:
            # Authlete returns different error coes for None and an empty
            # string. None is regarded as a caller's error. An empty string
            # is regarded as a client application's error.
            parameters = ''

        # Create a request for /api/auth/token API.
        req = TokenRequest()
        req.parameters   = parameters
        req.clientId     = credentials.userId
        req.clientSecret = credentials.password
        req.properties   = self._spi.getProperties()

        # Call /api/auth/token API.
        return self.api.token(req)


    def __handlePassword(self, response):
        # The ticket to call Authelte's /api/auth/token/* API.
        ticket = response.ticket

        # The credentials of the resource owner.
        username = response.username
        password = response.password

        # Validate the credentials.
        subject = self._spi.authenticateUser(username, password)

        # If the credentials of the resource owner are invalid.
        if subject is None:
            # The credentials are invalid. Nothing is issued.
            return self.tokenFail(
                ticket, TokenFailReason.INVALID_RESOURCE_OWNER_CREDENTIALS)

        # Issue tokens.
        return self.tokenIssue(ticket, subject, self._spi.getProperties())
