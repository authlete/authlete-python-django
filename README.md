Authlete Library for Django (Python)
====================================

Overview
--------

This library provides utility classes to make it easy for developers to
implement an authorization server which supports [OAuth 2.0][RFC6749] and
[OpenID Connect][OIDC] and a resource server.

This library is written using Django API and authlete-python library.
[Django][Django] is a web framework written in Python. On the other hand,
[authlete-python][AuthletePython] is another Authlete's open source library
which provides classes to communicate with [Authlete Web APIs][AuthleteAPI].

[Authlete][Authlete] is a cloud service that provides an implementation of
OAuth 2.0 & OpenID Connect ([overview][AuthleteOverview]). You can build a
_DB-less_ authorization server by using Authlete because authorization data
(e.g. access tokens), settings of authorization servers and settings of client
applications are stored in the Authlete server on cloud.

[django-oauth-server][DjangoOAuthServer] is an authorization server
implementation which uses this library. It implements not only an authorization
endpoint and a token endpoint but also a JWK Set endpoint, a discovery endpoint,
an introspection endpoint and a revocation endpoint.
[django-resource-server][DjangoResourceServer] is a resource server
implementation which also uses this library. It supports a
[userinfo endpoint][UserInfoEndpoint] defined in
[OpenID Connect Core 1.0][OIDCCore] and includes an example of a protected
resource endpoint, too. Use these sample implementations as a starting point
of your own implementations of an authorization server and a resource server.

License
-------

  Apache License, Version 2.0

Source Code
-----------

  <code>https://github.com/authlete/authlete-python-django</code>

PyPI (Python Package Index)
---------------------------

  <code>https://pypi.org/project/authlete-django/</code>

Install
-------

    pip install authlete-django

Samples
-------

- [django-oauth-server][DjangoOAuthServer] - Authorization server
- [django-resource-server][DjangoResourceServer] - Resource server

Contact
-------

Contact Form : https://www.authlete.com/contact/

| Purpose   | Email Address        |
|:----------|:---------------------|
| General   | info@authlete.com    |
| Sales     | sales@authlete.com   |
| PR        | pr@authlete.com      |
| Technical | support@authlete.com |

[Authlete]:             https://www.authlete.com/
[AuthleteAPI]:          https://docs.authlete.com/
[AuthleteOverview]:     https://www.authlete.com/developers/overview/
[AuthletePython]:       https://github.com/authlete/authlete-python/
[Django]:               https://www.djangoproject.com/
[DjangoOAuthServer]:    https://github.com/authlete/django-oauth-server/
[DjangoResourceServer]: https://github.com/authlete/django-resource-server/
[OIDC]:                 https://openid.net/connect/
[OIDCCore]:             https://openid.net/specs/openid-connect-core-1_0.html
[RFC6749]:              https://tools.ietf.org/html/rfc6749
[UserInfoEndpoint]:     https://openid.net/specs/openid-connect-core-1_0.html#UserInfo
