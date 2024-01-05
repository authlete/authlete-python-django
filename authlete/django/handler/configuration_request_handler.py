#
# Copyright (C) 2019-2024 Authlete, Inc.
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
from authlete.dto.service_configuration_request   import ServiceConfigurationRequest


class ConfigurationRequestHandler(BaseRequestHandler):
    """Handler for requests to a configuration endpoint.

    An OpenID Provider that supports "OpenID Connect Discovery 1.0" provides an
    endpoint that returns its configuration information in JSON format. Details
    about the format are described in "3. OpenId Provider Metadata" of
    "OpenID Connect Discovery 1.0".

    Note that the URI of an OpenID Provider configuration endpoint is defined
    in "4.1. OpenID Provider Configuration Request". In short, the URI must be
    "{Issue-Identifier}/.well-known/openid-configuration".

    "{Issuer-Identifier}" is a URL that identifies an OpenID Provider. For
    example, "https://example.com". For details about Issuer Identifier, see
    the description about the "issuer" metadata defined in "3. OpenID Provider
    Metadata" (OpenID Connecto Discovery 1.0) and the "iss" claim in
    "2. ID Token" (OpenID Connect Core 1.0).
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def handle(self, request, pretty=True):
        """Handle a request to a configuration endpoint.

        This method calls Authlete's /service/configuration API.

        Args:
            request (django.http.HttpRequest)
            pretty (bool)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Call Authlete's /service/configuration API. The API returns
        # JSON that complies with OpenID Connect Discovery 1.0.
        req = ServiceConfigurationRequest()
        req.pretty = pretty

        jsn = self.api.getServiceConfiguration(req)

        # 200 OK, application/json;charset=UTF-8
        return ResponseUtility.okJson(jsn)
