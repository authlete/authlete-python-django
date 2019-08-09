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


from .authorization_request_decision_handler_spi         import AuthorizationRequestDecisionHandlerSpi
from .authorization_request_decision_handler_spi_adapter import AuthorizationRequestDecisionHandlerSpiAdapter
from .authorization_request_handler_spi                  import AuthorizationRequestHandlerSpi
from .authorization_request_handler_spi_adapter          import AuthorizationRequestHandlerSpiAdapter
from .no_interaction_handler_spi                         import NoInteractionHandlerSpi
from .no_interaction_handler_spi_adapter                 import NoInteractionHandlerSpiAdapter
from .token_request_handler_spi                          import TokenRequestHandlerSpi
from .token_request_handler_spi_adapter                  import TokenRequestHandlerSpiAdapter
from .user_claim_provider_spi                            import UserClaimProviderSpi
from .user_claim_provider_spi_adapter                    import UserClaimProviderSpiAdapter
from .userinfo_request_handler_spi                       import UserInfoRequestHandlerSpi
from .userinfo_request_handler_spi_adapter               import UserInfoRequestHandlerSpiAdapter
