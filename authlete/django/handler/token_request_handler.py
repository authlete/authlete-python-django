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


from authlete.django.handler.token_request_base_handler import TokenRequestBaseHandler
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

        This method calls Authlete's /auth/token API and conditionally
        either /auth/token/issue API or /auth/token/fail API.

        Args:
            request (django.http.HttpRequest)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Call Authlete's /auth/token API.
        res = self.__callTokenApi(request)

        # 'action' in the response denotes the next action which the
        # implementation of the token endpoint should take.
        action = res.action

        # The content of the response to the client application.
        content = res.responseContent

        # Additional HTTP headers.
        headers = self.__prepareHeaders(res)

        if action == TokenAction.INVALID_CLIENT:
            # 401 Unauthorized.
            return ResponseUtility.unauthorized(
                'Basic realm="token"', content, headers)
        elif action == TokenAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content, headers)
        elif action == TokenAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content, headers)
        elif action == TokenAction.PASSWORD:
            # Process the token request whose flow is "Resource OWner
            # Password Credentials".
            return self.__handlePassword(res, headers)
        elif action == TokenAction.OK:
            # 200 OK
            return ResponseUtility.okJson(content, headers)
        elif action == TokenAction.TOKEN_EXCHANGE:
            # Process the token exchange request (RFC 8693)
            return self.__handleTokenExchange(res, headers)
        elif action == TokenAction.JWT_BEARER:
            # Process the token request which uses the grant type
            # urn:ietf:params:oauth:grant-type:jwt-bearer (RFC 7523).
            return self.__handleJwtBearer(res, headers)
        elif action == TokenAction.ID_TOKEN_REISSUABLE:
            # The flow of the token request is the refresh token flow
            # and an ID token can be reissued.
            return self.__handleIdTokenReissuable(res, headers)
        else:
            # 500 Internal Server Error
            # /auth/token API returns an unknown action.
            return self.unknownAction('/auth/token')


    def __callTokenApi(self, request):
        req = TokenRequest()

        # The request parameters.
        req.parameters = RequestUtility.extractRequestBody(request) or ''

        # The request may contain the basic authentication for client_secret_basic.
        credentials      = RequestUtility.extractBasicCredentials(request)
        req.clientId     = credentials.userId
        req.clientSecret = credentials.password

        # The request may contain a client certificate.
        req.clientCertificate = RequestUtility.extractClientCert(request)

        # The request may contain a DPoP proof JWT.
        req.dpop = request.headers.get('DPoP')

        # Other parameters
        req.properties = self._spi.getProperties()

        # Call /api/auth/token API.
        return self.api.token(req)


    def __prepareHeaders(self, res):
        if res.dpopNonce is not None:
            return { 'DPoP-Nonce': res.dpopNonce }

        return None


    def __handlePassword(self, response, headers):
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
                ticket, TokenFailReason.INVALID_RESOURCE_OWNER_CREDENTIALS, headers)

        # Issue tokens.
        return self.tokenIssue(ticket, subject, self._spi.getProperties(), headers)


    def __handleTokenExchange(self, tokenResponse, headers):
        # Let the SPI implementation handle the token request.
        response = self._spi.tokenExchange(tokenResponse)

        # If the SPI implementation has prepared a token response, it is used.
        # Otherwise, a token response with "error":"unsupported_grant_type" is
        # returned.
        return self.__useOrUnsupported(response)


    def __handleJwtBearer(self, tokenResponse, headers):
        # Let the SPI implementation handle the token request.
        response = self._spi.jwtBearer(tokenResponse)

        # If the SPI implementation has prepared a token response, it is used.
        # Otherwise, a token response with "error":"unsupported_grant_type" is
        # returned.
        return self.__useOrUnsupported(response)


    def __handleIdTokenReissuable(self, tokenResponse, headers):
        # TODO: Support ID token reissuance.

        # Note that calling ResponseUtility.ok() here will result in that the
        # token endpoint behaves in the same way as before and no ID token is
        # returned.
        return ResponseUtility.ok(tokenResponse.responseContent, headers)


    def __useOrUnsupported(self, response):
        if response is not None:
            return response

        # Generate a token response that indicates that the grant type is not
        # supported.
        #
        #     400 Bad Request
        #     Content-Type: application/json
        #
        #     {"error":"unsupported_grant_type"}
        #
        return ResponseUtility.badRequest('{"error":"unsupported_grant_type"}')
