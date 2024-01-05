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
from authlete.django.web.request_utility          import RequestUtility
from authlete.django.web.response_utility         import ResponseUtility
from authlete.dto.pushed_auth_req_action          import PushedAuthReqAction
from authlete.dto.pushed_auth_req_request         import PushedAuthReqRequest


class ParRequestHandler(BaseRequestHandler):
    """Handler for PAR requests to a PAR endpoint (RFC 9126).
    """


    def __init__(self, api):
        """Constructor

        Args:
            api (authlete.api.AuthleteApi)
        """

        super().__init__(api)


    def handle(self, request):
        """Handle a PAR request.

        Args:
            request (django.http.HttpRequest)

        Returns:
            django.http.HttpResponse

        Raises:
            authlete.api.AuthleteApiException
        """

        # Call Authlete's /pushed_auth_req API.
        res = self.__callPushedAuthReqApi(request)

        # 'action' in the response denotes the next action which the
        # implementation of the PAR endpoint should take.
        action = res.action

        # The content of the response to the client application.
        content = res.responseContent

        # Additional HTTP headers.
        headers = self.__prepareHeaders(res)

        if action == PushedAuthReqAction.CREATED:
            # 201 Created
            return ResponseUtility.created(content, headers)
        elif action == PushedAuthReqAction.BAD_REQUEST:
            # 400 Bad Request
            return ResponseUtility.badRequest(content, headers)
        elif action == PushedAuthReqAction.UNAUTHORIZED:
            # 401 Unauthorized
            return ResponseUtility.unauthorized(
                'Basic realm="par"', content, headers)
        elif action == PushedAuthReqAction.FORBIDDEN:
            # 403 Forbidden
            return ResponseUtility.forbidden(content, headers)
        elif action == PushedAuthReqAction.PAYLOAD_TOO_LARGE:
            # 413 Too Large
            return ResponseUtility.tooLarge(content, headers)
        elif action == PushedAuthReqAction.INTERNAL_SERVER_ERROR:
            # 500 Internal Server Error
            return ResponseUtility.internalServerError(content, headers)
        else:
            # 500 Internal Server Error
            # /pushed_auth_req API returns an unknown action.
            return self.unknownAction('/pushed_auth_req')


    def __callPushedAuthReqApi(self, request):
        req = PushedAuthReqRequest();

        # The request parameters.
        req.parameters = RequestUtility.extractRequestBody(request) or ''

        # The request may contain the basic authentication for client_secret_basic.
        credentials      = RequestUtility.extractBasicCredentials(request)
        req.clientId     = credentials.userId
        req.clientSecret = credentials.password

        # The request may contain a client certificate.
        req.clientCertificate = RequestUtility.extractClientCert(request)

        # The request may contain a DPoP proof JWT.
        req.dpop = request.headers.get('DPoP')

        # Call Authlete's /pushed_auth_req API.
        return self.api.pushAuthorizationRequest(req)


    def __prepareHeaders(self, res):
        if res.dpopNonce is not None:
            return { 'DPoP-Nonce': res.dpopNonce }

        return None
