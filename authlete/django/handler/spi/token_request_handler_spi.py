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


from abc import ABCMeta, abstractmethod


class TokenRequestHandlerSpi(metaclass=ABCMeta):
    """Service Provider Interface for TokenRequestHandler.

    An implementation of this interface needs to be given to the constructor of
    TokenRequestHandler.

    TokenRequestHandlerSpiAdapter is an empty implementation of this interface.
    """


    @abstractmethod
    def authenticateUser(self, username, password):
        """Authenticate a user.

        This method is called only when Resource Owner Password Credentials
        Grant (RFC 6749, 4.3) was used. Therefore, if you have no plan to
        support the flow, always return None. In most cases, you don't
        have to support the flow. RFC 6749 says "The authorization server
        should take special care when enabling this grant type and only
        allow it when other flows are not viable."

        Args:
            username (str) :  The value of the "username" request parameter of the token request.
            password (str) :  The value of the "password" request parameter of the token request.

        Returns:
            str : The subject (= unique identifier) of the authenticated user. None if not authenticated.
        """
        pass


    @abstractmethod
    def getProperties(self):
        """Get arbitrary key-value pairs to be associated with an access token.

        Properties returned from this method will appear as top-level entries
        (unless they are marked as hidden) in a JSON response from the
        authorization server as shown in RFC 6749, 5.1.

        Returns:
            list : list of authlete.dto.Property.
        """
        pass


    @abstractmethod
    def tokenExchange(self, tokenResponse):
        """Handle a token exchange request.

        This method is called when the grant type of the token request is
        'urn:ietf:params:oauth:grant-type:token-exchange'. The grant type is
        defined in 'RFC 8693: OAuth 2.0 Token Exchange'.

        RFC 8693 is very flexible. In other words, the specification does not
        define details that are necessary for secure token exchange. Therefore,
        implementations have to complement the specifications with their own
        rules.

        The argument passed to this method is an instance of
        'authlete.dto.TokenResponse' that represents a response from Authlete's
        /auth/token API. The instance contains information about the token
        exchange request such as the value of the 'subject_token' request
        parameter. Implementations of this 'tokenExchange' method are supposed
        to (1) validate the information based on their own rules, (2) generate
        a token (e.g. an access token) using the information, and (3) prepare
        a token response in the JSON format that conforms to Section 2.2 of
        RFC 8693.

        Authlete's /auth/token API performs validation of token exchange
        requests to some extent. Therefore, authorization server implementations
        don't have to repeat the same validation steps. See the JavaDoc of the
        'TokenResponse' class for details about the validation steps.
        ( https://authlete.github.io/authlete-java-common/ )

        This method should return a django.http.HttpResponse instance that
        conforms to RFC 8693. If this method returns 'None', 'TokenRequestHandler'
        will generate an HTTP response with 400 Bad Request and
        {"error":"unsupported_grant_type"}.

        NOTE: Token Exchange is supported by Authlete 2.3 and newer versions.
        If the Authlete server of your system is older than version 2.3, the
        grant type 'urn:ietf:params:oauth:grant-type:token-exchange' is not
        supported and so this method is never called.

        Args:
            tokenResponse (authlete.dto.TokenResponse)

        Returns:
            django.http.HttpResponse : A response from the token endpoint.
        """
        pass


    @abstractmethod
    def jwtBearer(self, tokenResponse):
        """Handle a token request that uses the grant type
        'urn:ietf:params:oauth:grant-type:jwt-bearer'.

        This method is called when the grant type of the token request is
        'urn:ietf:params:oauth:grant-type:jwt-bearer'. The grant type is defined
        in 'RFC 7523: JSON Web Token (JWT) Profile for OAuth 2.0 Client
        Authentication and Authorization Grants'.

        The grant type utilizes a JWT as an authorization grant, but the
        specification does not define details about how the JWT is generated by
        whom. As a result, it is not defined in the specification how to obtain
        the key whereby to verify the signature of the JWT. Therefore, each
        deployment has to define their own rules which are necessary to determine
        the key for signature verification.

        The argument passed to this method is an instance of
        'authlete.dto.TokenResponse' that represents a response from Authlete's
        /auth/token API. The instance contains information about the token request
        such as the value of the 'assertion' request parameter. Implementations
        of this method are supposed to (1) validate the authorization grant
        (= the JWT specified by the 'assertion' request parameter), (2) generate
        an access token, and (3) prepare a token response in the JSON format that
        conforms to RFC 6749.

        Authlete's /auth/token API performs validation of token requests to some
        extent. Therefore, authorization server implementations don't have to
        repeat the same validation steps. Basically, what implementations have to
        do is to verify the signature of the JWT. See the JavaDoc of the
        'TokenResponse' class for details about the validation steps.
        ( https://authlete.github.io/authlete-java-common/ )

        This method should return a django.http.HttpResponse instance that
        conforms to RFC 6749. If this method returns 'None', 'TokenRequestHandler'
        will generate an HTTP response with 400 Bad Request and
        {"error":"unsupported_grant_type"}.

        NOTE: JWT Authorization Grant is supported by Authlete 2.3 and newer
        versions. If the Authlete server of your system is older than version 2.3,
        the grant type 'urn:ietf:params:oauth:grant-type:jwt-bearer' is not
        supported and so this method is never called.

        Args:
            tokenResponse (authlete.dto.TokenResponse)

        Returns:
            django.http.HttpResponse : A response from the token endpoint.
        """
        pass
