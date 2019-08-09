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


class UserInfoRequestHandlerSpi(UserClaimProviderSpi):
    """Service Provider Interface for UserInfoRequestHandler.

    An implementation of this interface needs to be given to the constructor of
    UserInfoRequestHandler.

    UserInfoRequestHandlerSpiAdapter is an empty implementation of this interface.
    """


    @abstractmethod
    def getSub(self):
        """Get the value of the "sub" claim that will be embedded in the response from the userinfo endpoint.

        If this method returns None, the subject associated with the access
        token (which was presented by the client application at the userinfo
        endpoint) will be used as the value of the "sub" claim.

        Returns:
            str : The value of the "sub" claim.
        """
        pass
