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


import time
from authlete.django.handler.authorization_request_base_handler import AuthorizationRequestBaseHandler
from authlete.django.handler.claim_collector                    import ClaimCollector
from authlete.dto.authorization_action                          import AuthorizationAction
from authlete.dto.authorization_fail_reason                     import AuthorizationFailReason


class NoInteractionHandler(AuthorizationRequestBaseHandler):
    """Handler for the case where an authorization request should be processed without user interaction.

    A response from Authlete's /api/auth/authorization API contains an
    'action' response parameter. When the value of the response parameter
    is "NO_INTERACTION", the authorization request needs to be processed
    without user interaction. This class is a handler for the case.
    """


    def __init__(self, api, spi):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
            spi (authlete.django.handler.spi.NoInteractionHandlerSpi)
        """

        super().__init__(api)
        self._spi = spi


    def handle(self, response):
        """Handle an authorization request without user interaction.

        This method calls Authlete's /api/auth/authorization/issue API or
        /api/auth/authorization/fail API.

        Args:
            response (authlete.dto.AuthorizationResponse)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        spi = self._spi

        # If the value of the "action" parameter in the response from Authlete's
        # /api/auth/authorization API is not "NO_INTERACTION".
        if response.action != AuthorizationAction.NO_INTERACTION:
            # This handler does not handle other cases than NO_INTERACTION.
            return None

        # Check 1: User Authentication
        if self.__checkUserAuthentication() == False:
            # A user must have logged in.
            return self.authorizationFail(
                response.ticket, AuthorizationFailReason.NOT_LOGGED_IN)

        # Get the last time when the user was authenticated.
        authTime = spi.getUserAuthenticatedAt()

        # Check 2: Max Age
        if self.__checkMaxAge(response, authTime) == False:
            # The maximum authentication age has elapsed since the last time
            # when the user was authenticated.
            return self.authorizationFail(
                response.ticket, AuthorizationFailReason.EXCEEDS_MAX_AGE)

        # The subject (unique ID) of the current user.
        subject = spi.getUserSubject()

        # Check 3: Subject
        if self.__checkSubject(response, subject) == False:
            # The requested subject and that of the current user don't match.
            return self.authorizationFail(
                response.ticket, AuthorizationFailReason.DIFFERENT_SUBJECT)

        # Get the value of the "sub" claim. This is optional. When "sub" is None,
        # the value of "subject" will be used as the value of the "sub" claim.
        sub = spi.getSub()

        # Get the ACR that was satisfied when the current user was authenticated.
        acr = spi.getAcr()

        # Check 4: ACR
        if self.__checkAcr(response, acr) == False:
            # None of the requested ACRs is satisfied.
            return self.authorizationFail(
                response.ticket, AuthorizationFailReason.ACR_NOT_SATISFIED)

        # Collect claim values.
        claims = ClaimCollector(
            subject, response.claims, response.claimsLocales, spi).collect()

        # Properties to be associated with an access token and/or an authorization code.
        properties = spi.getProperties()

        # Scopes associated with an access token and/or an authorization code.
        # If the value returned from spi.getScopes() is not None, the scope set
        # replaces the scopes that were given by the original authorization request.
        scopes = spi.getScopes()

        # Issue tokens without user interaction.
        return self.authorizationIssue(
            response.ticket, subject, authTime, acr, claims, properties, scopes, sub)


    def __checkUserAuthentication(self):
        return self._spi.isUserAuthenticated()


    def __checkMaxAge(self, response, authTime):
        # Get the requested maximum authentication age.
        maxAge = response.maxAge

        # If no maximum authentication age is requested.
        if maxAge == 0:
            # No need to care about the maximum authentication age.
            return True

        # The time in seconds when the authentication expires.
        expiresAt = authTime + maxAge

        # If the authentication has not expired yet.
        if time.time() < expiresAt:
            # Not exceed.
            return True

        # Exceeded
        return False


    def __checkSubject(self, response, subject):
        # Get the requested subject.
        requestedSubject = response.subject

        # If no subject is requested.
        if requestedSubject is None:
            # Ne need to care about the subject.
            return True

        # If the requested subject matches that of the current user.
        if requestedSubject == subject:
            # The subjects match.
            return True

        # The subjects don't match.
        return False


    def __checkAcr(self, response, acr):
        # Get the list of requested ACRs.
        requestedAcrs = response.acrs

        # if no ACR is requested.
        if requestedAcrs is None or len(requestedAcrs) == 0:
            # No need to care about ACR.
            return True

        # For each requested ACR.
        for requestedAcr in requestedAcrs:
            if requestedAcr == acr:
                # OK. The ACR satisfied when the current user was authenticated
                # matches one of the requested ACRs.
                return True

        # If one of the requested ACRs must be satisfied.
        if response.acrEssential:
            # None of the requested ACRs is satisfied.
            return False

        # The ACR satisfied when the current user was authenticated does not
        # match any one of the requested ACRs, but the authorization request
        # from the client application did not request ACR as essential.
        # Therefore, it is not necessary to raise an error here.
        return True
