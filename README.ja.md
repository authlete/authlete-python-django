Django (Python) 用 Authlete ライブラリ
======================================

概要
----

このライブラリは、[OAuth 2.0][RFC6749] および [OpenID Connect][OIDC]
をサポートする認可サーバーと、
リソースサーバーを実装するためのユーティリティークラス群を提供します。

このライブラリは、Django API と authlete-python ライブラリを用いて書かれています。
[Django][Django] は Python で書かれた Web フレームワークの一つです。
一方、[authlete-python][AuthletePython] は Authlete
が提供するもう一つのオープンソースライブラリで、[Authlete Web API][AuthleteAPI]
とやりとりするためのクラス群を含んでいます。

[Authlete][Authlete] は OAuth 2.0 と OpenID Connect の実装を提供するクラウドサービスです
([overview][AuthleteOverview])。 認可データ (アクセストークン等)
や認可サーバー自体の設定、クライアントアプリケーション群の設定はクラウド上の Authlete
サーバーに保存されるため、Authlete を使うことで「DB レス」の認可サーバーを構築することができます。

[django-oauth-server][DjangoOAuthServer] はこのライブラリを使用している認可サーバーの実装で、
認可エンドポイントやトークンエンドポイントに加え、JWK Set エンドポイント、
ディスカバリーエンドポイント、取り消しエンドポイントの実装を含んでいます。
また、[django-resource-server][DjangoResourceServer]
はこのライブラリを使用しているリソースサーバーの実装です。 [OpenID Connect Core 1.0][OIDCCore]
で定義されている[ユーザー情報エンドポイント][UserInfoEndpoint]
をサポートし、また、保護リソースエンドポイントの例を含んでいます。
あなたの認可サーバーおよびリソースサーバーの実装の開始点として、
これらのサンプル実装を活用してください。

ライセンス
----------

  Apache License, Version 2.0

ソースコード
------------

  <code>https://github.com/authlete/authlete-python-django</code>

PyPI (Python Package Index)
---------------------------

  <code>https://pypi.org/project/authlete-django/</code>

インストール
------------

    pip install authlete-django

サンプル
--------

- [django-oauth-server][DjangoOAuthServer] - 認可サーバー
- [django-resource-server][DjangoResourceServer] - リソースサーバー

コンタクト
----------

コンタクトフォーム : https://www.authlete.com/contact/

| 目的 | メールアドレス       |
|:-----|:---------------------|
| 一般 | info@authlete.com    |
| 営業 | sales@authlete.com   |
| 広報 | pr@authlete.com      |
| 技術 | support@authlete.com |

[Authlete]:             https://www.authlete.com/ja/
[AuthleteAPI]:          https://docs.authlete.com/
[AuthleteOverview]:     https://www.authlete.com/ja/developers/overview/
[AuthletePython]:       https://github.com/authlete/authlete-python/
[Django]:               https://www.djangoproject.com/
[DjangoOAuthServer]:    https://github.com/authlete/django-oauth-server/
[DjangoResourceServer]: https://github.com/authlete/django-resource-server/
[OIDC]:                 https://openid.net/connect/
[OIDCCore]:             https://openid.net/specs/openid-connect-core-1_0.html
[RFC6749]:              https://tools.ietf.org/html/rfc6749
[UserInfoEndpoint]:     https://openid.net/specs/openid-connect-core-1_0.html#UserInfo
