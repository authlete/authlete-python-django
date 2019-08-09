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


from authlete.api.authlete_api_exception          import AuthleteApiException
from authlete.django.handler.base_request_handler import BaseRequestHandler
from authlete.django.web.response_utility         import ResponseUtility


class JwksRequestHandler(BaseRequestHandler):
    """Handler for requests to an endpoint that exposes JSON Web Key Set document (RFC 7517).

    An OpenID Provider is required to expose its JSON web Key Set document so
    that client applications can (1) verify signatures by the OpenID Provider
    and (2) encrypt their requests to the OpenID Provider. The URI of a JWK
    Set endpoint can be found as the value of the "jwks_uri" metadata which is
    defined in "3. OpenID Provider Metadata" of "OpenID Connect Discovery 1.0"
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def handle(self, request, pretty=True):
        """Handle a request to a JWK Set document endpoint.

        This method calls Authlete's /api/service/jwks/get API.

        Args:
            request (django.http.HttpRequest)
            pretty (bool) : True to format the JWK Set document in pretty format.

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        cause = None

        try:
            # Call Authlete's /api/service/jwks/get API. The API returns the
            # JWK Set (RFC 7517) of the service. The second argument given
            # to getServiceJwks() is False not to include private keys.
            jwks = self.api.getServiceJwks(pretty, False)

            # If no JWK Set for the service is registered.
            if jwks is None or len(jwks) == 0:
                # 204 No Content.
                return ResponseUtility.noContent()

            # 200 OK, application/json;charset=UTF-8
            return ResponseUtility.okJson(jwks)
        except AuthleteApiException as e:
            cause = e

        if cause.response is None or cause.response.status_code != 302:
            # Something wrong happend.
            raise cause

        # The value of the Location header of the response from the Authlete API.
        location = cause.response.headers.get('Location')

        # 302 Found with a Location header.
        return ResponseUtility.location(location)
