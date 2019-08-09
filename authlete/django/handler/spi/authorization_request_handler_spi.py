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


from abc import abstractmethod
from .user_claim_provider_spi import UserClaimProviderSpi


class AuthorizationRequestHandlerSpi(UserClaimProviderSpi):
    """The base interface for Service Provider Interfaces for authorization request handlers.

    Common methods for NoInteractionHandlerSpi and AuthorizationRequestDecisionHandlerSpi.
    """


    @abstractmethod
    def getUserAuthenticatedAt(self):
        """Get the time when the user was authenticated.

        Returns:
            int :
                The time when the current user was authenticated. The number of
                seconds since the Unix epoch. 0 means that the time is unknown.
        """
        pass


    @abstractmethod
    def getUserSubject(self):
        """Get the subject (= unique identifier) of the user.

        It must consist of only ASCII letters and its length must not exceed 100.

        Returns:
            str : The subject of the user.
        """
        pass


    @abstractmethod
    def getSub(self):
        """Get the value of the "sub" claim that will be embedded in an ID token.

        If this method returns None, the value returned from getUserSubject() will
        be used.

        The main purpose of this method is to hide the actual value of the subject
        from client applications.

        Returns:
            str : The value of the "sub" claim.
        """
        pass


    @abstractmethod
    def getAcr(self):
        """Get the authentication context class referece (ACR) that was satisfied when the user was authenticated.

        The value returned from this method has an important meaning only when the
        "acr" claim is requested as an essential claim. See OIDC Core, 5.1.1.1.
        for details.

        Returns:
            str : The ACR that was satisfied when the user was authenticated.
        """
        pass


    @abstractmethod
    def getProperties(self):
        """Get arbitrary key-value pairs to be associated with an access token and/or an authorization code.

        Properties returned from this method will appear as top-level entries
        (unless they are marked as hidden) in a JSON response from the
        authorization server as shown in RFC 6749, 5.1.

        Returns:
            list : list of authlete.dto.Property.
        """
        pass


    @abstractmethod
    def getScopes(self):
        """Get scopes to be associated with an access token and/or an authorization code.

        If None is returned, the scopes specified in the original authorization
        request from the client application are used. In other cases, the
        specified scopes by this method will replace the original scopes.

        Even scopes that are not included in the original authorization request
        can be specified. However, as an exception, the "openid" scope is ignored
        on Authlete server side if it is not included in the original request.
        It is because the existence of the "openid" scope considerably changes
        the validation steps and because adding "openid" triggers generation of
        an ID token (although the client application has not requested it) and
        the behavior is a major violation against the specification.

        If you add "offline_access" scope although it is not included in the
        original request, keep in mind that the specification requires explicit
        consent from the user forthe scope (OIDC Core, 11). When "offline_access"
        is included in the original authorization request, the current
        implementation of Authlete's /api/auth/authorization API checks whether
        the authorization request has come along with the "prompt" request
        parameter and its value includes "consent". However, note that the
        implementation of Authlete's /api/auth/authorization/issue API does not
        perform the same validation even if the "offline_access" scope is newly
        added via this method.

        Returns:
            list : list of str. Scope names.
        """
        pass
