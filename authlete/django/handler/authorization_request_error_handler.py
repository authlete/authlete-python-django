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


from authlete.django.handler.authorization_request_base_handler import AuthorizationRequestBaseHandler
from authlete.django.web.response_utility                       import ResponseUtility
from authlete.dto.authorization_action                          import AuthorizationAction


class AuthorizationRequestErrorHandler(AuthorizationRequestBaseHandler):
    """Handler for error cases of authorization reuqests.

    A response from Authlete's /api/auth/authorization API contains an "action"
    response parameter. When the value of the response parameter is neither
    "NO_INTERACTION" nor "INTERACTION", the authorization request should be
    handled as an error case. This class is a handler for such error cases.
    """


    def __init__(self):
        """Constructor"""
        super().__init__(None)


    def handle(self, response):
        """Handle an error case of an authorization request.

        This method returns None when response.action returns
        AuthorizationAction.INTERACTION or AuthorizationAction.NO_INTERACTION.
        In other cases, an instance of django.http.HttpResponse is returned.

        Args:
            response (authlete.dto.AuthorizationResponse)

        Returns:
            django.http.HttpResponse : An error response

        Raises:
            authlete.api.AuthleteApiException
        """

        # 'action' in the response denotes the next action which the
        # implementation of the authorization endpoint should take.
        action = response.action

        # The content of the response which should be returned to the
        # user agent. The format varies depending on the action.
        content = response.responseContent

        if action == AuthorizationAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        elif action == AuthorizationAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content)
        elif action == AuthorizationAction.LOCATION:
            # 302 Found
            return ResponseUtility.location(content)
        elif action == AuthorizationAction.FORM:
            # 200 OK
            return ResponseUtility.okHtml(content)
        elif action == AuthorizationAction.INTERACTION:
            # This is not an error case. The implementation of the
            # authorization endpoint should show an authorization
            # page to the user.
            return None
        elif action == AuthorizationAction.NO_INTERACTION:
            # This is not an error case. The implementation of the
            # authorization endpoint should handle the authorization
            # request without user interaction.
            return None
        else:
            # 500 Internal Server Error
            # Authlete's /api/auth/authorization API returned an unknown action.
            return self.unknownAction('/api/auth/authorization')
