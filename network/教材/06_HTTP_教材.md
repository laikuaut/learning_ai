# 第6章：HTTP（HyperText Transfer Protocol）

## この章のゴール

- HTTPの基本的な仕組み（リクエスト/レスポンス構造）を理解すること
- 主要なHTTPメソッド（GET, POST, PUT, DELETE等）の使い分けを説明できること
- ステータスコードの分類と代表的なコードの意味を把握すること
- HTTPヘッダの役割と主要なヘッダフィールドを理解すること
- HTTPSの仕組み（SSL/TLS）を説明できること
- HTTP/1.1, HTTP/2, HTTP/3 の違いを概説できること

---

## 6.1 HTTPとは

### 6.1.1 HTTPの概要

HTTP（HyperText Transfer Protocol）は、WebブラウザとWebサーバ間でデータをやり取りするためのプロトコルです。OSI参照モデルのアプリケーション層（第7層）で動作し、TCPのポート80番を使用します。

```
【HTTPの基本的な通信モデル】

  クライアント                        サーバ
  (ブラウザ)                        (Webサーバ)
      │                                │
      │── HTTPリクエスト ──────────→│
      │   「GET /index.html を送って」   │
      │                                │
      │←── HTTPレスポンス ─────────│
      │   「200 OK + HTMLデータ」        │
      │                                │

  ・リクエスト/レスポンス型（クライアントが要求、サーバが応答）
  ・ステートレス（各リクエストは独立、前の状態を覚えない）
  ・テキストベース（HTTP/1.x）/ バイナリ（HTTP/2以降）
```

### 6.1.2 URLの構造

HTTP通信で指定するリソースの場所をURL（Uniform Resource Locator）で表します。

```
https://www.example.com:443/path/to/page?key=value&lang=ja#section1
│       │               │  │             │                  │
スキーム  ホスト名       ポート  パス       クエリ文字列       フラグメント

スキーム:       http:// または https://
ホスト名:       サーバのドメイン名またはIPアドレス
ポート番号:     省略時は http=80, https=443
パス:           サーバ上のリソースの場所
クエリ文字列:   パラメータ（?で始まり、&で区切る）
フラグメント:   ページ内の位置（#で始まる、サーバには送信されない）
```

---

## 6.2 HTTPリクエスト

### 6.2.1 リクエストの構造

HTTPリクエストは「リクエスト行」「ヘッダ」「空行」「ボディ」で構成されます。

```
【HTTPリクエストの構造】

  GET /index.html HTTP/1.1           ← リクエスト行（メソッド URI バージョン）
  Host: www.example.com              ← ヘッダ（必須）
  User-Agent: Mozilla/5.0 ...        ← ヘッダ
  Accept: text/html                  ← ヘッダ
  Accept-Language: ja,en              ← ヘッダ
  Connection: keep-alive             ← ヘッダ
                                     ← 空行（ヘッダの終わりを示す）
  （GETの場合、ボディは通常なし）      ← メッセージボディ
```

### 6.2.2 HTTPメソッド

| メソッド | 用途 | ボディ | 冪等性 | 安全性 |
|---------|------|--------|--------|--------|
| **GET** | リソースの取得 | なし | あり | あり |
| **POST** | リソースの作成・データ送信 | あり | なし | なし |
| **PUT** | リソースの更新（全体置換） | あり | あり | なし |
| **PATCH** | リソースの部分更新 | あり | なし | なし |
| **DELETE** | リソースの削除 | なし | あり | なし |
| **HEAD** | レスポンスヘッダのみ取得（GETと同じだがボディなし） | なし | あり | あり |
| **OPTIONS** | 利用可能なメソッドの確認（CORS プリフライト） | なし | あり | あり |

**冪等性（Idempotent）**：同じリクエストを何度実行しても結果が同じになる性質です。
**安全性（Safe）**：リソースの状態を変更しない性質です。

> **よくある間違い**: GETリクエストのURLにパスワードや個人情報を含めてはいけません。URLはブラウザ履歴、サーバログ、プロキシログに記録されるため、機密情報はPOSTのボディで送信してください。

### 6.2.3 GETとPOSTの使い分け

```
【GET: データを取得するとき】
GET /search?q=DNS&lang=ja HTTP/1.1
Host: www.example.com

・パラメータはURLのクエリ文字列に含まれる
・ブックマーク可能
・キャッシュされる
・URLの長さに制限あり（ブラウザ依存、約2,000文字程度）

【POST: データを送信するとき】
POST /login HTTP/1.1
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 29

username=admin&password=secret

・パラメータはメッセージボディに含まれる
・ブックマーク不可
・キャッシュされない
・データサイズの制限が緩い
```

---

## 6.3 HTTPレスポンス

### 6.3.1 レスポンスの構造

```
【HTTPレスポンスの構造】

  HTTP/1.1 200 OK                     ← ステータス行（バージョン ステータスコード 理由句）
  Date: Mon, 01 Jan 2024 10:00:00 GMT ← ヘッダ
  Content-Type: text/html; charset=UTF-8  ← ヘッダ
  Content-Length: 1234                 ← ヘッダ
  Server: nginx/1.24.0                ← ヘッダ
                                      ← 空行
  <!DOCTYPE html>                     ← メッセージボディ（レスポンスデータ）
  <html>
  ...
  </html>
```

### 6.3.2 ステータスコード

ステータスコードは3桁の数値で、リクエストの処理結果を示します。

| 分類 | 範囲 | 意味 | 代表例 |
|------|------|------|--------|
| **1xx** | 100-199 | 情報（処理継続中） | 100 Continue |
| **2xx** | 200-299 | 成功 | 200 OK, 201 Created |
| **3xx** | 300-399 | リダイレクト | 301, 302, 304 |
| **4xx** | 400-499 | クライアントエラー | 400, 401, 403, 404 |
| **5xx** | 500-599 | サーバエラー | 500, 502, 503 |

### 6.3.3 主要なステータスコード詳細

**2xx 系（成功）**

| コード | 意味 | 説明 |
|--------|------|------|
| **200** | OK | リクエスト成功 |
| **201** | Created | リソースが作成された（POST成功時） |
| **204** | No Content | 成功したがレスポンスボディなし（DELETE成功時等） |

**3xx 系（リダイレクト）**

| コード | 意味 | 説明 |
|--------|------|------|
| **301** | Moved Permanently | 恒久的なURL移転（SEO的にも重要） |
| **302** | Found | 一時的なリダイレクト |
| **304** | Not Modified | キャッシュが有効（ボディなし） |

**4xx 系（クライアントエラー）**

| コード | 意味 | 説明 |
|--------|------|------|
| **400** | Bad Request | リクエストが不正 |
| **401** | Unauthorized | 認証が必要（未認証） |
| **403** | Forbidden | アクセス拒否（認証済みだが権限なし） |
| **404** | Not Found | リソースが見つからない |
| **405** | Method Not Allowed | 許可されていないHTTPメソッド |
| **429** | Too Many Requests | レート制限超過 |

**5xx 系（サーバエラー）**

| コード | 意味 | 説明 |
|--------|------|------|
| **500** | Internal Server Error | サーバ内部エラー |
| **502** | Bad Gateway | ゲートウェイ/プロキシが不正な応答を受信 |
| **503** | Service Unavailable | サービス一時停止（メンテナンス等） |
| **504** | Gateway Timeout | ゲートウェイ/プロキシがタイムアウト |

> **現場の知識**: 401（Unauthorized）と403（Forbidden）はよく混同されます。401は「あなたが誰かわからない（認証されていない）」、403は「あなたが誰かはわかっているが、アクセス権限がない（認可されていない）」という違いがあります。

---

## 6.4 HTTPヘッダ

### 6.4.1 主要なリクエストヘッダ

| ヘッダ | 説明 | 例 |
|--------|------|-----|
| **Host** | 接続先のホスト名（HTTP/1.1で必須） | `Host: www.example.com` |
| **User-Agent** | クライアントソフトの情報 | `User-Agent: Mozilla/5.0 ...` |
| **Accept** | 受け入れ可能なMIMEタイプ | `Accept: text/html, application/json` |
| **Accept-Language** | 受け入れ可能な言語 | `Accept-Language: ja, en;q=0.8` |
| **Accept-Encoding** | 受け入れ可能なエンコーディング | `Accept-Encoding: gzip, deflate, br` |
| **Authorization** | 認証情報 | `Authorization: Bearer xxx` |
| **Cookie** | クッキー情報 | `Cookie: session_id=abc123` |
| **Content-Type** | リクエストボディのMIMEタイプ | `Content-Type: application/json` |
| **Referer** | 遷移元のURL | `Referer: https://example.com/page1` |
| **Cache-Control** | キャッシュの制御 | `Cache-Control: no-cache` |

### 6.4.2 主要なレスポンスヘッダ

| ヘッダ | 説明 | 例 |
|--------|------|-----|
| **Content-Type** | レスポンスボディのMIMEタイプ | `Content-Type: text/html; charset=UTF-8` |
| **Content-Length** | レスポンスボディのバイト数 | `Content-Length: 1234` |
| **Set-Cookie** | クッキーの設定 | `Set-Cookie: session_id=abc; HttpOnly; Secure` |
| **Cache-Control** | キャッシュの制御 | `Cache-Control: max-age=3600` |
| **Location** | リダイレクト先URL | `Location: https://example.com/new` |
| **Server** | サーバソフトの情報 | `Server: nginx/1.24.0` |
| **Access-Control-Allow-Origin** | CORS許可オリジン | `Access-Control-Allow-Origin: https://app.example.com` |

### 6.4.3 Content-Typeの種類（MIMEタイプ）

| MIMEタイプ | 説明 |
|-----------|------|
| `text/html` | HTMLドキュメント |
| `text/plain` | プレーンテキスト |
| `text/css` | CSSスタイルシート |
| `application/json` | JSONデータ |
| `application/xml` | XMLデータ |
| `application/javascript` | JavaScript |
| `application/x-www-form-urlencoded` | フォームデータ（URLエンコード） |
| `multipart/form-data` | ファイルアップロードを含むフォームデータ |
| `image/png` | PNG画像 |
| `image/jpeg` | JPEG画像 |

---

## 6.5 HTTPの状態管理

### 6.5.1 ステートレスとCookie

HTTPはステートレス（状態を持たない）なプロトコルです。しかし、ログイン状態の維持やショッピングカートなど、状態の管理が必要な場面があります。この問題を解決するのが **Cookie** と **セッション** です。

```
【Cookieによる状態管理】

  ① 初回アクセス
  クライアント ──→ サーバ
                    │ セッションID発行
  クライアント ←── サーバ
  Set-Cookie: session_id=abc123

  ② 2回目以降のアクセス
  クライアント ──→ サーバ
  Cookie: session_id=abc123
                    │ セッションIDで状態を特定
  クライアント ←── サーバ
  「ログイン済みユーザ向けのページ」
```

### 6.5.2 Cookieの属性

| 属性 | 説明 | セキュリティ上の推奨 |
|------|------|---------------------|
| **Secure** | HTTPS通信時のみCookieを送信 | 必ず設定 |
| **HttpOnly** | JavaScriptからのアクセスを禁止 | セッションCookieには必須 |
| **SameSite** | クロスサイトリクエストでのCookie送信を制御 | Lax または Strict |
| **Domain** | Cookieが有効なドメイン | 必要最小限に |
| **Path** | Cookieが有効なパス | 必要最小限に |
| **Max-Age / Expires** | Cookieの有効期限 | セッション管理に応じて設定 |

---

## 6.6 HTTPS（HTTP over SSL/TLS）

### 6.6.1 HTTPSの仕組み

HTTPS は、HTTPの通信をSSL/TLSで暗号化したものです。ポート443番を使用します。

```
【HTTPとHTTPSの違い】

  HTTP:   クライアント ←──平文──→ サーバ    （盗聴・改ざん可能）
  HTTPS:  クライアント ←─暗号化─→ サーバ    （盗聴・改ざん防止）

  HTTP:   http://www.example.com   (ポート80)
  HTTPS:  https://www.example.com  (ポート443)
```

### 6.6.2 SSL/TLSハンドシェイク

```
【TLSハンドシェイク（TLS 1.2 の場合）】

  クライアント                                サーバ
      │                                        │
      │── ① ClientHello ──────────────→│
      │   ・対応するTLSバージョン               │
      │   ・対応する暗号スイート一覧             │
      │   ・クライアントランダム値               │
      │                                        │
      │←── ② ServerHello ─────────────│
      │   ・選択したTLSバージョン               │
      │   ・選択した暗号スイート                 │
      │   ・サーバランダム値                     │
      │                                        │
      │←── ③ Certificate ─────────────│
      │   ・サーバ証明書（公開鍵を含む）         │
      │                                        │
      │←── ④ ServerHelloDone ─────────│
      │                                        │
      │── ⑤ ClientKeyExchange ────────→│
      │   ・プリマスターシークレット             │
      │   （サーバの公開鍵で暗号化）             │
      │                                        │
      │── ⑥ ChangeCipherSpec ─────────→│
      │   ・以降は暗号通信に切り替え             │
      │                                        │
      │── ⑦ Finished ─────────────────→│
      │←── ⑧ ChangeCipherSpec + Finished ──│
      │                                        │
      │←═══ 暗号化された通信 ═══════════→│
```

### 6.6.3 サーバ証明書とCA

```
【証明書の信頼チェーン】

  ルート認証局（Root CA）
       │ 署名
  中間認証局（Intermediate CA）
       │ 署名
  サーバ証明書（www.example.com）

  ブラウザは「信頼されたルートCA」の一覧を持っており、
  証明書チェーンをたどって信頼性を検証する
```

| 証明書の種類 | 略称 | 検証レベル | 表示 |
|-------------|------|-----------|------|
| **ドメイン認証** | DV | ドメインの所有権のみ | 鍵マーク |
| **企業認証** | OV | 組織の実在性を確認 | 鍵マーク |
| **EV認証** | EV | 厳格な組織審査 | 鍵マーク（詳細に組織名） |

> **現場の知識**: Let's Encryptの登場により、DV証明書は無料で取得できるようになりました。ただし、フィッシングサイトでもDV証明書を取得できるため、「鍵マーク=安全」とは限りません。証明書の種類（DV/OV/EV）と発行元を確認することが重要です。

---

## 6.7 HTTPのバージョン

### 6.7.1 HTTP/1.0, HTTP/1.1, HTTP/2, HTTP/3 の比較

| 特徴 | HTTP/1.0 | HTTP/1.1 | HTTP/2 | HTTP/3 |
|------|----------|----------|--------|--------|
| 接続 | 毎回切断 | Keep-Alive（持続的接続） | 多重化 | 多重化 |
| 圧縮 | なし | コンテンツ圧縮 | ヘッダ圧縮（HPACK） | ヘッダ圧縮（QPACK） |
| 形式 | テキスト | テキスト | バイナリ | バイナリ |
| 並列処理 | 不可 | パイプライン（HoL問題） | ストリーム多重化 | ストリーム多重化 |
| トランスポート | TCP | TCP | TCP | **QUIC（UDP）** |
| 暗号化 | 任意 | 任意 | 事実上必須 | 必須 |

### 6.7.2 HTTP/2 の特徴

```
【HTTP/1.1 vs HTTP/2】

  HTTP/1.1:
  ┌─リクエスト1──→ ──レスポンス1──→┐
  │  リクエスト2──→ ──レスポンス2──→│  直列処理（HoL Blocking）
  │  リクエスト3──→ ──レスポンス3──→│
  └────────────── 時間 ──────────→┘

  HTTP/2:
  ┌─リクエスト1──→ ─レスポンス1──→┐
  │  リクエスト2──→ ─レスポンス2──→│  多重化（並列処理）
  │  リクエスト3──→ ─レスポンス3──→│
  └──────────── 時間 ────────→┘  ← 高速

  主な特徴:
  ・ストリーム多重化: 1つのTCP接続で複数リクエストを並列処理
  ・ヘッダ圧縮（HPACK）: 重複するヘッダを効率的に圧縮
  ・サーバプッシュ: サーバが先回りしてリソースを送信
  ・バイナリプロトコル: テキストからバイナリに変更し効率化
```

### 6.7.3 HTTP/3 と QUIC

HTTP/3 はトランスポート層にTCPではなく **QUIC**（UDP上に構築）を使用します。

```
【HTTP/2 vs HTTP/3 のプロトコルスタック】

  HTTP/2            HTTP/3
  ┌──────┐        ┌──────┐
  │ HTTP/2│        │ HTTP/3│
  ├──────┤        ├──────┤
  │  TLS  │        │ QUIC  │  ← TLS 1.3を内蔵
  ├──────┤        ├──────┤
  │  TCP  │        │  UDP  │
  └──────┘        └──────┘

  QUIC の利点:
  ・接続確立が高速（0-RTT / 1-RTT）
  ・TCPのHead-of-Line Blocking を回避
  ・接続のマイグレーション（Wi-Fi→モバイル切替時に接続維持）
```

---

## 6.8 まとめ

### ポイントまとめ

1. **HTTP** はリクエスト/レスポンス型のステートレスなプロトコルで、Webの基盤技術です
2. **HTTPメソッド** はリソースに対する操作を指定します（GET=取得、POST=作成、PUT=更新、DELETE=削除）
3. **ステータスコード** は処理結果を3桁の数値で示します（2xx=成功、3xx=リダイレクト、4xx=クライアントエラー、5xx=サーバエラー）
4. **Cookie** によりステートレスなHTTPに状態管理の仕組みを付加しています
5. **HTTPS** はSSL/TLSによりHTTP通信を暗号化し、盗聴・改ざん・なりすましを防止します
6. **HTTP/2** はストリーム多重化とヘッダ圧縮により高速化、**HTTP/3** はQUIC（UDP）により更なる高速化を実現しています

### 試験対策キーワード

- HTTP、リクエスト、レスポンス、ステートレス
- GET、POST、PUT、DELETE、HEAD、OPTIONS
- ステータスコード（200, 301, 302, 304, 400, 401, 403, 404, 500, 503）
- Cookie、セッション、Set-Cookie、HttpOnly、Secure、SameSite
- HTTPS、SSL/TLS、サーバ証明書、CA、DV/OV/EV
- HTTP/2（多重化、HPACK）、HTTP/3（QUIC）
- URL、MIMEタイプ、Content-Type

---

## 確認問題

1. GETメソッドとPOSTメソッドの違いを、パラメータの送信方法とセキュリティの観点から説明してください。
2. ステータスコード 301 と 302 の違いを説明してください。
3. ステータスコード 401 と 403 の違いを説明してください。
4. HTTPSにおけるSSL/TLSハンドシェイクの流れを概説してください。
5. HTTP/2 が HTTP/1.1 に比べて高速である理由を2つ挙げてください。

---

**前章**: [第5章：DNS](./05_DNS_教材.md)
**次章**: [第7章：ルーティングとNAT](./07_ルーティングとNAT_教材.md)
