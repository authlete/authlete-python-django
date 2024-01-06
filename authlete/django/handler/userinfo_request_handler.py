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


from json import dumps
from authlete.django.handler.base_request_handler import BaseRequestHandler
from authlete.django.handler.claim_collector      import ClaimCollector
from authlete.django.web.request_utility          import RequestUtility
from authlete.django.web.response_utility         import ResponseUtility
from authlete.dto.userinfo_action                 import UserInfoAction
from authlete.dto.userinfo_issue_action           import UserInfoIssueAction
from authlete.dto.userinfo_issue_request          import UserInfoIssueRequest
from authlete.dto.userinfo_request                import UserInfoRequest


class UserInfoRequestHandler(BaseRequestHandler):
    """Handler for userinfo requests to a userinfo endpoint.
    """


    def __init__(self, api, spi):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
            spi (authlete.django.handler.spi.UserInfoRequestHandlerSpi)
        """

        super().__init__(api)
        self._spi = spi


    def handle(self, request):
        """Handle a userinfo request.

        This method calls Authlete's /auth/userinfo API and conditionally
        /auth/userinfo/issue API.

        Args:
            request (django.http.HttpRequest)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Extract the access token from the request.
        accessToken = RequestUtility.extractAccessToken(request)

        if accessToken is None:
            # 400 Bad Request with a WWW-Authenticate header.
            return ResponseUtility.wwwAuthenticate(400,
                'Bearer error="invalid_token",error_description="An access token is required."')

        # Call Authlete's /api/auth/userinfo API.
        res = self.__callUserInfoApi(request, accessToken)

        # 'action' in the response denotes the next action which the
        # implementation of the userinfo endpoint should take.
        action = res.action

        # The content of the response to the client application.
        content = res.responseContent

        # Additional HTTP headers.
        headers = self.__prepareHeaders(res)

        if action == UserInfoAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.wwwAuthenticate(500, content, headers)
        elif action == UserInfoAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.wwwAuthenticate(400, content, headers)
        elif action == UserInfoAction.UNAUTHORIZED:
            # 401 Unauthorized
            return ResponseUtility.wwwAuthenticate(401, content, headers)
        elif action == UserInfoAction.FORBIDDEN:
            # 403 Forbidden
            return ResponseUtility.wwwAuthenticate(403, content, headers)
        elif action == UserInfoAction.OK:
            # Return the user information.
            return self.__getUserInfo(res, headers)
        else:
            # 500 Internal Server Error
            # /auth/userinfo API returns an unknown action.
            return self.unknownAction('/auth/userinfo')


    def __callUserInfoApi(self, request, accessToken):
        req = UserInfoRequest()

        # The access token.
        req.token = accessToken

        # The request may contain a client certificate.
        req.clientCertificate = RequestUtility.extractClientCert(request)

        # The request may contain a DPoP proof JWT.
        req.dpop = request.headers.get('DPoP')

        # Call /api/auth/userinfo API.
        return self.api.userinfo(req)


    def __prepareHeaders(self, res):
        if res.dpopNonce is not None:
            return { 'DPoP-Nonce': res.dpopNonce }

        return None


    def __getUserInfo(self, response, headers):
        # Collect information about the user.
        claims = ClaimCollector(
            response.subject, response.claims, None, self._spi).collect()

        # The value of the 'sub' claim (optional)
        sub = self._spi.getSub()

        # Generate a response from the userinfo endpoint.
        return self.__userInfoIssue(response.token, claims, sub, headers)


    def __userInfoIssue(self, token, claims, sub, headers):
        # Call Authlete's /api/auth/userinfo/issue API.
        res = self.__callUserInfoIssueApi(token, claims, sub)

        # 'action' in the response denotes the next action which the
        # implementation of the userinfo endpoint should take.
        action = res.action

        # The content of the response to the client application.
        content = res.responseContent

        if action == UserInfoIssueAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.wwwAuthenticate(500, content, headers)
        elif action == UserInfoIssueAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.wwwAuthenticate(400, content, headers)
        elif action == UserInfoIssueAction.UNAUTHORIZED:
            # 401 Unauthorized
            return ResponseUtility.wwwAuthenticate(401, content, headers)
        elif action == UserInfoIssueAction.FORBIDDEN:
            # 403 Forbidden
            return ResponseUtility.wwwAuthenticate(403, content, headers)
        elif action == UserInfoIssueAction.JSON:
            # 200 OK, application/json; charset=UTF-8
            return ResponseUtility.okJson(content, headers)
        elif action == UserInfoIssueAction.JWT:
            # 200 OK, application/jwt
            return ResponseUtility.okJwt(content, headers)
        else:
            # 500 Internal Server Error
            # /auth/userinfo/issue API returns an unknown action.
            return self.unknownAction('/auth/userinfo/issue')


    def __callUserInfoIssueApi(self, token, claims, sub):
        # Prepare a request for /api/auth/userinfo/issue API.
        req = UserInfoIssueRequest()
        req.token = token
        req.sub   = sub

        if claims is not None:
            req.claims = dumps(claims)

        # Call /api/auth/userinfo/issue API.
        return self.api.userinfoIssue(req)
