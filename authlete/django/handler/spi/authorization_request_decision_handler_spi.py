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
from .authorization_request_handler_spi import AuthorizationRequestHandlerSpi


class AuthorizationRequestDecisionHandlerSpi(AuthorizationRequestHandlerSpi):
    """Service Provider Interface for AuthorizationRequestDecisionHandler.

    An implementation of this interface needs to be given to the constructor of
    AuthorizationRequestDecisionHandler.

    AuthorizationRequestDecisionHandlerSpiAdapter is an empty implementation of
    this interface.
    """


    @abstractmethod
    def isClientAuthorized(self):
        """Get the user's decision on the authorization request.

        Returns:
            bool : True if the user has decided to grant authorization to the client.
        """
        pass
