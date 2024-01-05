変更点
======

- `ConfigurationRequestHandler` クラス
  - `AuthleteApi.getServiceConfiguration` の引数変更に合わせるために更新。

- `RequestUtility` クラス
  - `extractBasicCredentials` メソッドを追加。
  - `extractClientCert` メソッドを追加。

- `ResponseUtility` クラス
  - `headers=None` 引数を全てのメソッドに追加。
  - `created` メソッドを追加。
  - `tooLarge` メソッドを追加。

- `TokenRequestBaseHandler` クラス
  - 引数 `headers` を `tokenIssue` メソッドに追加。
  - 引数 `headers` を `tokenFail` メソッドに追加。

- `TokenRequestHandler` クラス
  - MTLS (RFC 8705) をサポート。
  - DPoP (RFC 9449) をサポート。
  - Token Exchange (RFC 8693) をサポート。
  - JWT Authorization Grant (RFC 7523) をサポート。

- `TokenRequestHandlerSpi` クラス
  - `tokenExchange` メソッドを追加。
  - `jwtBearer` メソッドを追加。

- `TokenRequestHandlerSpiAdapter` クラス
  - `tokenExchange` メソッドを追加。
  - `jwtBearer` メソッドを追加。

- 新しい型
  - `ParRequestHandler` クラス

1.0.1 (2019 年 09 月 19 日)
---------------------------

- ハンドラーの不具合を幾つか修正。

1.0.0 (2019 年 08 月 09 日)
---------------------------

- 最初のリリース
