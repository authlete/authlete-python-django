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
from authlete.dto.credential_issuer_jwks_action   import CredentialIssuerJwksAction
from authlete.dto.credential_issuer_jwks_request  import CredentialIssuerJwksRequest


class CredentialIssuerJwksRequestHandler(BaseRequestHandler):
    """Handler for requests to a JWK Set endpoint of the credential issuer.
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def handle(self, request=None):
        """Handle a request to a JWK Set endpoint of the credential issuer.

        This method calls Authlete's /vci/jwks API.

        Args:
            request (authlete.dto.CredentialIssuerJwksRequest)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        if request is None:
            request = CredentialIssuerJwksRequest()
            request.pretty = True

        # Call Authlete's /vci/jwks API.
        res = self.api.credentialIssuerJwks(request)

        # 'action' in the response denotes the next action which
        # the implementation of the endpoint should take.
        action = res.action

        # The content of the response.
        content = res.responseContent

        if action == CredentialIssuerJwksAction.OK:
            # 200 OK
            return ResponseUtility.okJson(content)
        elif action == CredentialIssuerJwksAction.NOT_FOUND:
            # 404 Not Found
            return ResponseUtility.notFound(content)
        elif action == CredentialIssuerJwksAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        else:
            # 500 Internal Server Error
            # /vci/jwks API returns an unknown action.
            return self.unknownAction('/vci/jwks')
