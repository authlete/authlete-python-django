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


from authlete.django.handler.base_request_handler    import BaseRequestHandler
from authlete.django.web.response_utility            import ResponseUtility
from authlete.dto.credential_issuer_metadata_action  import CredentialIssuerMetadataAction
from authlete.dto.credential_issuer_metadata_request import CredentialIssuerMetadataRequest


class CredentialIssuerMetadataRequestHandler(BaseRequestHandler):
    """Handler for requests to a credential issuer metadata endpoint.

    A credential issuer that supports "OpenID for Verifiable Credential Issuance"
    provides an endpoint that returns its metadata in the JSON format. The URL of
    the endpoint is "{Issuer-Identifier}/.well-known/openid-credential-issuer".
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def handle(self, request=None):
        """Handle a request to a credential issuer metadata endpoint.

        This method calls Authlete's /vci/metadata API.

        Args:
            request (authlete.dto.CredentialIssuerMetadataRequest)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        if request is None:
            request = CredentialIssuerMetadataRequest()
            request.pretty = True

        # Call Authlete's /vci/metadata API.
        res = self.api.credentialIssuerMetadata(request)

        # 'action' in the response denotes the next action which
        # the implementation of the endpoint should take.
        action = res.action

        # The content of the response.
        content = res.responseContent

        if action == CredentialIssuerMetadataAction.OK:
            # 200 OK
            return ResponseUtility.okJson(content)
        elif action == CredentialIssuerMetadataAction.NOT_FOUND:
            # 404 Not Found
            return ResponseUtility.notFound(content)
        elif action == CredentialIssuerMetadataAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content)
        else:
            # 500 Internal Server Error
            # /vci/metadata API returns an unknown action.
            return self.unknownAction('/vci/metadata')
