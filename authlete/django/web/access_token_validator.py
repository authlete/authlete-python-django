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
from authlete.dto.introspection_action    import IntrospectionAction
from authlete.dto.introspection_request   import IntrospectionRequest


class AccessTokenValidator(object):
    def __init__(self, api):
        super().__init__()
        self._api = api
        self.__resetValidation()


    def __resetValidation(self):
        self._valid                  = False
        self._introspectionResponse  = None
        self._introspectionException = None
        self._errorResponse          = None


    @property
    def api(self):
        return self._api


    @property
    def valid(self):
        """Get the result of the access token validation.

        After a call of `validate()` method, this property holds the same value
        as was returned from `validate()`.

        Returns:
            bool : The result of the access token validation.
        """
        return self._valid


    @property
    def introspectionResponse(self):
        """Get the response from Authlete's /api/auth/introspection API.

        `validate()` method internally calls /api/auth/introspection API and sets
        the response from the API to this property. Note that this property
        remains `None` if the API call threw an exception, and in that error case,
        the `introspectionException` property is set.

        On entry of `validate()` method, this property is reset to `None`.

        Returns:
            authlete.dto.IntrospectionResponse
        """
        return self._introspectionResponse


    @property
    def introspectionException(self):
        """Get the exception raised by a call to Authlete's /api/auth/introspection API.

        `validate()` method internally calls Authlete's /api/auth/introspection
        API. If the API call threw an exception, the exception would be set to
        this property. Note that this property remains `None` if the API call
        succeeds, and in that successful case, the `introspectionResponse`
        property is set.

        On entry of `validate()` method, this property is reset to `None`.

        Returns:
            Exception
        """
        return self._introspectionException


    @property
    def errorResponse(self):
        """Get the error response that should be sent back to the client.

        This property is internally set by `validate()` method when `validate()`
        returns `False`. This error response complies with RFC 6750 (The OAuth
        2.0 Authorization Framework: Bearer Token Usage).

        On entry of `validate()` method, this property is reset to `None`.

        Returns:
            django.http.HttpResponse
        """
        return self._errorResponse


    def validate(self, accessToken, requiredScopes=None, requiredSubject=None):
        """Validate an access token.

        On entry, as the first step, the following properties are reset to
        False or None: `valid`, `introspectionResponse`, `introspectionException`
        and `errorResponse`.

        Then, this method internally calls Authlete's /api/auth/introspection
        API to get information about the access token.

        If the API call failed, the exception thrown by the API call is set to
        the `introspectionException` property and an error response
        (`500 Internal Server Error`) that should be returned to the client
        application is set to the `errorResponse` property. Then, this method
        set `False` to the `valid` property and returns `False`.

        If the API call succeeded, the response from the API is set to the
        `introspectionResponse` property. Then, this method checks the value
        of the `action` parameter in the response from the API.

        If the value of the `action` parameter is `OK`, this method sets `True`
        to the `valid` property and returns `True`.

        If the value of the `action` parameter is not `OK`, this method builds
        an error response that should be returned to the client application and
        sets it to the `errorResponse` property. Then, this method sets `False`
        to the `valid` property and returns `False`.

        If the given access token exists and has not expired, and optionally
        if the access token covers all the required scopes (in case
        `requiredScopes` was given) and the access token is associated with
        the required subject (in case `requiredSubject` was given), this method
        returns `True`. In other cases, this method returns `False`.

        Args:
            accessToken (str): An access token to be validated.
            requiredScopes (list of str):
                Scopes that the access token should have. If this parameter is not
                `None`, the implementation of Authlete's /api/auth/introspection
                API checks whether the access token covers all the required scopes.
                On the other hand, if `None` is given, Authlete does not conduct
                the validation on scopes.
            requiredSubject (str):
                Subject (= unique identifier of an end-user) that the access
                token should be associated with. If this parameter is not `None`,
                the implementation of Authlete's /api/auth/introspection API checks
                whether the access token is associated with the required subject.
                On the other hand, if `None` is given, Authlete does not conduct
                the validation on subject.

        Returns:
            bool: The result of access token validation.
        """

        # Reset properties that may have been set by the previous call.
        self.__resetValidation()

        try:
            # Call Authlete's /api/auth/introspection API.
            self._introspectionResponse = self.__callIntrospectionApi(
                accessToken, requiredScopes, requiredSubject)
        except Exception as cause:
            self._introspectionException = cause
            self._errorResponse          = self.__buildErrorFromException(cause)
            self._valid                  = False
            return False

        # The 'action' parameter in the response from /api/auth/introspection
        # denotes the next action that the API caller should take.
        action = self._introspectionResponse.action

        if action == IntrospectionAction.OK:
            # The access token is valid.
            self._valid = True
            return True
        else:
            self._errorResponse = self.__buildErrorFromResponse(self._introspectionResponse)
            self._valid         = False
            return False


    def __callIntrospectionApi(self, accessToken, requiredScopes, requiredSubject):
        # Prepare a request to /api/auth/introspection API.
        req = IntrospectionRequest()
        req.token   = accessToken
        req.scopes  = requiredScopes
        req.subject = requiredSubject

        # Call /api/auth/introspection API.
        return self.api.introspection(req)


    def __buildErrorFromException(self, cause):
        # The value for the WWW-Authenticate header.
        challenge = 'Bearer error="server_error",error_description="Introspection API call failed."'

        # Build a response that complies with RFC 6749.
        return ResponseUtility.wwwAuthenticate(500, challenge)


    def __buildErrorFromResponse(self, response):
        action = response.action

        if action == IntrospectionAction.INTERNAL_SERVER_ERROR:
            statusCode = 500
        elif action == IntrospectionAction.BAD_REQUEST:
            statusCode = 400
        elif action == IntrospectionAction.UNAUTHORIZED:
            statusCode = 401
        elif action == IntrospectionAction.FORBIDDEN:
            statusCode = 403
        else:
            statusCode = 500

        # In error cases, the 'responseContent' parameter in the response
        # from Authlete's /api/auth/introspection API contains a value for
        # the WWW-Authenticate header.
        challenge = response.responseContent

        # Build a response that complies with RFC 6749.
        return ResponseUtility.wwwAuthenticate(statusCode, challenge)
