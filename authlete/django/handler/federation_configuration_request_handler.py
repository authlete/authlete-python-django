#
# Copyright (C) 2024 Authlete, Inc.
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


from authlete.django.handler.base_request_handler  import BaseRequestHandler
from authlete.django.web.response_utility          import ResponseUtility
from authlete.dto.federation_configuration_action  import FederationConfigurationAction
from authlete.dto.federation_configuration_request import FederationConfigurationRequest


class FederationConfigurationRequestHandler(BaseRequestHandler):
    """Handler for requests to a federation configuration endpoint.

    An entity that supports "OpenID Federation 1.0" provides an endpoint that
    returns its entity configuration in the JWT format. The URL of the endpoint
    is "{Entity-Identifier}/.well-known/openid-federation".
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def handle(self, request=None):
        """Handle a request to a federation configuration endpoint.

        This method calls Authlete's /federation/configuration API.

        Args:
            request (authlete.dto.FederationConfigurationRequest)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        if request is None:
            request = FederationConfigurationRequest()

        # Call Authlete's /federation/configuration API.
        res = self.api.federationConfiguration(request)

        # 'action' in the response denotes the next action which
        # the implementation of the endpoint should take.
        action = res.action

        # The content of the response.
        content = res.responseContent

        if action == FederationConfigurationAction.OK:
            # 200 OK; application/entity-statement+jwt
            return ResponseUtility.entityStatement(content)
        elif action == FederationConfigurationAction.NOT_FOUND:
            # 404 Not Found
            return ResponseUtility.notFound(content)
        elif action == FederationConfigurationAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        else:
            # 500 Internal Server Error
            # /federation/configuration API returns an unknown action.
            return self.unknownAction('/federation/configuration')
