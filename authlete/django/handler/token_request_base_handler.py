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
from authlete.django.web.response_utility         import ResponseUtility
from authlete.dto.token_fail_action               import TokenFailAction
from authlete.dto.token_fail_request              import TokenFailRequest
from authlete.dto.token_issue_action              import TokenIssueAction
from authlete.dto.token_issue_request             import TokenIssueRequest


class TokenRequestBaseHandler(BaseRequestHandler):
    """The base class for request handlers that are used in the implementation of a token endpoint.
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def tokenIssue(self, ticket, subject, properties, headers=None):
        """Call /auth/token/issue API.

        Args:
            ticket (str)  : The ticket which has been issued previously from /auth/token API.
            subject (str) : The unique identifier of the resource owner.
            properties (list of authlete.dto.Property)
            headers (dict) : Additional HTTP headers.

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Call /api/auth/token/issue API.
        res = self.__callTokenIssue(ticket, subject, properties)

        # 'action' in the response denotes the next action which the
        # implementation of the token endpoint should take.
        action = res.action

        # The content of the response to the client application.
        content = res.responseContent

        if action == TokenIssueAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content, headers)
        elif action == TokenIssueAction.OK:
            # 200 OK
            return ResponseUtility.okJson(content, headers)
        else:
            # 500 Internal Server Error
            # The /api/auth/token/issue API returned an unknown action.
            return self.unknownAction('/api/auth/token/issue')


    def __callTokenIssue(self, ticket, subject, properties):
        # Prepare a request for /api/auth/token/issue API.
        req = TokenIssueRequest()
        req.ticket     = ticket
        req.subject    = subject
        req.properties = properties

        # Call /api/auth/token/issue API.
        return self.api.tokenIssue(req)


    def tokenFail(self, ticket, reason, headers=None):
        """Call /api/auth/authorization/fail API.

        Args:
            ticket (str) : The ticket which has been issued previously from /api/auth/token API.
            reason (authlete.dto.TokenFailReason) : The reason of the failure of the request.

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Call /api/auth/token/fail API.
        res = self.__callTokenFail(ticket, reason)

        # 'action' in the response denotes the next action which the
        # implementation of the token endpoint should take.
        action = res.action

        # The content of the response to the client application.
        content = res.responseContent

        if action == TokenFailAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content, headers)
        elif action == TokenFailAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content, headers)
        else:
            # 500 Internal Server Error
            # The /api/auth/token/fail API returned an unknown action.
            return self.unknownAction('/api/auth/token/fail')


    def __callTokenFail(self, ticket, reason):
        # Prepare a request for /api/auth/token/fail API.
        req = TokenFailRequest()
        req.ticket = ticket
        req.reason = reason

        # Call /api/auth/token/fail API.
        return self.api.tokenFail(req)
