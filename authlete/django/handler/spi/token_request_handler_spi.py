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


from abc import ABCMeta, abstractmethod


class TokenRequestHandlerSpi(metaclass=ABCMeta):
    """Service Provider Interface for TokenRequestHandler.

    An implementation of this interface needs to be given to the constructor of
    TokenRequestHandler.

    TokenRequestHandlerSpiAdapter is an empty implementation of this interface.
    """


    @abstractmethod
    def authenticateUser(self, username, password):
        """Authenticate a user.

        This method is called only when Resource Owner Password Credentials
        Grant (RFC 6749, 4.3) was used. Therefore, if you have no plan to
        supporte the flow, always return None. In mose cases, you don't
        have to support the flow. RFC 6749 says "The authorization server
        should take special care when enabling this grant type and only
        allow it when other flows are not viable."

        Args:
            username (str) :  The value of the "username" request parameter of the token request.
            password (str) :  The value of the "password" request parameter of the token request.

        Returns:
            str : The subject (= unique identifier) of the authenticated user. None if not authenticated.
        """
        pass


    @abstractmethod
    def getProperties(self):
        """Get arbitrary key-value pairs to be associated with an access token.

        Properties returned from this method will appear as top-level entries
        (unless they are marked as hidden) in a JSON response from the
        authorization server as shown in RFC 6749, 5.1.

        Returns:
            list : list of authlete.dto.Property.
        """
        pass
