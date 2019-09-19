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


from json import dumps
from authlete.django.handler.base_request_handler import BaseRequestHandler
from authlete.django.web.response_utility         import ResponseUtility
from authlete.dto.authorization_fail_action       import AuthorizationFailAction
from authlete.dto.authorization_fail_request      import AuthorizationFailRequest
from authlete.dto.authorization_issue_action      import AuthorizationIssueAction
from authlete.dto.authorization_issue_request     import AuthorizationIssueRequest


class AuthorizationRequestBaseHandler(BaseRequestHandler):
    """The base class for request handlers that are used in the implementation of an authorization endpoint.
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def authorizationIssue(self, ticket, subject, authTime, acr, claims, properties, scopes, sub):
        """Call /api/auth/authorization/issue API.

        Args:
            ticket (str)      : The ticket which has been issued previously from /api/auth/authorization API.
            subject (str)     : The unique identifier of the user who has granted permissions to the client.
            authTime (int)    : The time at which the user was authenticated. Seconds since the Unix epoch.
            acr (str)         : The Authentication Context Class Reference performed for user authentication.
            claims (dict)     : Claims about the user.
            properties (list) : list of authlete.dto.Property. Arbitrary properties to be associated with tokens.
            scopes (list)     : list of str. Scopes to be associated with tokens.
            sub (str)         : The value of the "sub" claim in an ID token.

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Call /api/auth/authorization API.
        res = self.__callAuthorizationIssue(
            ticket, subject, authTime, acr, claims, properties, scopes, sub)

        # 'action' in the response denotes the next action which the
        # implementation of the authorization endpoint should take.
        action = res.action

        # The content of the response to the user agent. The format
        # of the content varies depending on the action.
        content = res.responseContent

        if action == AuthorizationIssueAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        elif action == AuthorizationIssueAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content)
        elif action == AuthorizationIssueAction.LOCATION:
            # 302 Found
            return ResponseUtility.location(content)
        elif action == AuthorizationIssueAction.FORM:
            # 200 OK
            return ResponseUtility.okHtml(content)
        else:
            # 500 Internal Server Error
            # The /api/auth/authorization/issue API returned an unknown action.
            return self.unknownAction('/api/auth/authorization/issue')


    def __callAuthorizationIssue(self, ticket, subject, authTime, acr, claims, properties, scopes, sub):
        # Prepare a request for /api/auth/authorization/issue API.
        req = AuthorizationIssueRequest()
        req.ticket     = ticket
        req.subject    = subject
        req.authTime   = authTime
        req.acr        = acr
        req.properties = properties
        req.scopes     = scopes
        req.sub        = sub

        if claims is not None:
            req.claims = dumps(claims)

        # Call /api/auth/authorization/issue API.
        return self.api.authorizationIssue(req)


    def authorizationFail(self, ticket, reason):
        """Call /api/auth/authorization/fail API.

        Args:
            ticket (str) : The ticket which has been issued previously from /api/auth/authorization API.
            reason (authlete.dto.AuthorizationFailReason) : The reason of the failure of the request.

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Call /api/auth/authorization/fail API.
        res = self.__callAuthorizationFail(ticket, reason)

        # 'action' in the response denotes the next action which the
        # implementation of the authorization endpoint should take.
        action = res.action

        # The content of the response to the user agent. The format
        # of the content varies depending on the action.
        content = res.responseContent

        if action == AuthorizationFailAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        elif action == AuthorizationFailAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content)
        elif action == AuthorizationFailAction.LOCATION:
            # 302 Found
            return ResponseUtility.location(content)
        elif action == AuthorizationFailAction.FORM:
            # 200 OK
            return ResponseUtility.okHtml(content)
        else:
            # 500 Internal Server Error
            # The /api/auth/authorization/fail API returned an unknown action.
            return self.unknownAction('/api/auth/authorization/fail')


    def __callAuthorizationFail(self, ticket, reason):
        # Prepare a request for /api/auth/authorization/fail API.
        req = AuthorizationFailRequest()
        req.ticket = ticket
        req.reason = reason

        # Call /api/auth/authorization/fail API.
        return self.api.authorizationFail(req)
