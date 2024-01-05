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


from authlete.django.handler.base_request_handler import BaseRequestHandler
from authlete.django.web.response_utility         import ResponseUtility
from authlete.dto.federation_registration_action  import FederationRegistrationAction


class FederationRegistrationRequestHandler(BaseRequestHandler):
    """Handler for requests to a federation registration endpoint.
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def handle(self, request):
        """Handle a request to a federation registration endpoint.

        This method calls Authlete's /federation/registration API.

        Args:
            request (authlete.dto.FederationRegistrationRequest)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Call Authlete's /federation/registration API.
        res = self.api.federationRegistration(request)

        # 'action' in the response denotes the next action which
        # the implementation of the endpoint should take.
        action = res.action

        # The content of the response.
        content = res.responseContent

        if action == FederationRegistrationAction.OK:
            # 200 OK; application/entity-statement+jwt
            return ResponseUtility.entityStatement(content)
        elif action == FederationRegistrationAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content)
        elif action == FederationRegistrationAction.NOT_FOUND:
            # 404 Not Found
            return ResponseUtility.notFound(content)
        elif action == FederationRegistrationAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        else:
            # 500 Internal Server Error
            # /federation/registration API returns an unknown action.
            return self.unknownAction('/federation/registration')
