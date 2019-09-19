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
from authlete.django.handler.claim_collector                    import ClaimCollector
from authlete.dto.authorization_fail_reason                     import AuthorizationFailReason


class AuthorizationRequestDecisionHandler(AuthorizationRequestBaseHandler):
    """Handler for the user's decision on the authorization request.

    An authorization endpoint returns an authorization page (HTML) to the user,
    and the user will either authorize or deny the authorization request. The
    handle() method handles the decision and calls Authlete's
    /api/auth/authorization/issue API or /api/auth/authorization/fail API.
    """


    def __init__(self, api, spi):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
            spi (authlete.django.handler.spi.AuthorizationRequestDecisionHandlerSpi)
        """

        super().__init__(api)
        self._spi = spi


    def handle(self, ticket, claimNames, claimLocales):
        """Handle the user's decision on the authorization request.

        Args:
            ticket (str)        : The ticket which has been issued previously by /api/auth/authorization API.
            claimNames (list)   : list of str. The value of 'claims' in the response from /api/auth/authorization API.
            claimLocales (list) : list of str. The value of 'claimsLocales' in the response from /api/auth/authorization API.

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        spi = self._spi

        # If the user did not grant authorization to the client application.
        if spi.isClientAuthorized() == False:
            # The user denied the authorization request.
            return self.authorizationFail(ticket, AuthorizationFailReason.DENIED)

        # The subject (= unique idnetifier) of the user.
        subject = spi.getUserSubject()

        # If the subject of the user is not available.
        if subject is None:
            # The user is not authenticated.
            return self.authorizationFail(ticket, AuthorizationFailReason.NOT_AUTHENTICATED)

        # Get the value of the "sub" claim. This is optional. When "sub" is None,
        # the value of "subject" will be used as the value of the "sub" claim.
        sub = spi.getSub()

        # The time when the user was authenticated.
        authTime = spi.getUserAuthenticatedAt()

        # The ACR (Authentication Context Class Reference) of the user authentication.
        acr = spi.getAcr()

        # Collect claim values.
        claims = ClaimCollector(subject, claimNames, claimLocales, spi).collect()

        # Properties to be associated with an access token and/or an authorization code.
        properties = spi.getProperties()

        # Scopes associated with an access token and/or an authorization code.
        # If the value returned from spi.getScopes() is not None, the scope set
        # replaces the scopes that were given by the original authorization request.
        scopes = spi.getScopes()

        # Issue required tokens by calling /api/auth/authorization/issue API.
        return self.authorizationIssue(
            ticket, subject, authTime, acr, claims, properties, scopes, sub)
