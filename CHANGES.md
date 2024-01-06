CHANGES
=======

1.1.0 (2024-01-07)
------------------

- `ConfigurationRequestHandler` class
  - Update to align with the argument change of `AuthleteApi.getServiceConfiguration`.

- `RequestUtility` class
  - Add the `extractAccessToken` method.
  - Add the `extractBasicCredentials` method.
  - Add the `extractClientCert` method.
  - Add the `extractDpopToken` method.

- `ResponseUtility` class
  - Add the `headers=None` argument to all the methods.
  - Add the `entityStatement` method.
  - Add the `created` method.
  - Add the `acceptedJson` method.
  - Add the `acceptedJwt` method.
  - Add the `tooLarge` method.

- `TokenRequestBaseHandler` class
  - Add the `headers` argument to the `tokenIssue` method.
  - Add the `headers` argument to the `tokenFail` method.

- `TokenRequestHandler` class
  - Support MTLS (RFC 8705).
  - Support DPoP (RFC 9449).
  - Support Token Exchange (RFC 8693).
  - Support JWT Authorization Grant (RFC 7523).

- `TokenRequestHandlerSpi` class
  - Add the `tokenExchange` method.
  - Add the `jwtBearer` method.

- `TokenRequestHandlerSpiAdapter` class
  - Add the `tokenExchange` method.
  - Add the `jwtBearer` method.

- `UserInfoRequestHandler` class
  - Support MTLS (RFC 8705).
  - Support DPoP (RFC 9449).

- New types
  - `CredentialIssuerJwksRequestHandler` class
  - `CredentialIssuerMetadataRequestHandler` class
  - `CredentialJwtIssuerMetadataRequestHandler` class
  - `FederationConfigurationRequestHandler` class
  - `FederationRegistrationRequestHandler` class
  - `ParRequestHandler` class

1.0.1 (2019-09-19)
------------------

- Fixed some bugs in handlers.

1.0.0 (2019-08-09)
------------------

- First release
