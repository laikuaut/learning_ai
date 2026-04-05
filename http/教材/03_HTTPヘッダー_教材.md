# 第3章：HTTPヘッダー

## この章のゴール
- HTTPヘッダーの役割と4つの分類を理解する
- 主要なリクエストヘッダーとレスポンスヘッダーの用途を説明できる
- Content-TypeとMIMEタイプの仕組みを理解する
- コンテンツネゴシエーションの概念を理解する
- カスタムヘッダーの慣習を知る
- curlコマンドでヘッダーを確認・送信できる

---

## 3.1 HTTPヘッダーとは

HTTPヘッダー（HTTP Header）は、HTTPリクエストやレスポンスに付加される**メタ情報**です。本文（ボディ）とは別に、通信に必要な補足情報をキー: 値の形式で伝えます。

### ヘッダーの基本形式

```
ヘッダー名: 値
```

```
Host: www.example.com
Content-Type: application/json
Accept-Language: ja, en;q=0.8
```

> **ポイント**: ヘッダー名は**大文字・小文字を区別しません**（Case-Insensitive）。`Content-Type` と `content-type` は同じ意味です。

### HTTPメッセージの全体像

```
+---------------------------+
|  リクエストライン /        |  ← メソッド、URL、バージョン
|  ステータスライン          |  ← ステータスコード
+---------------------------+
|  ヘッダー部               |  ← 複数のヘッダー行
|  Host: example.com        |
|  Content-Type: text/html  |
|  ...                      |
+---------------------------+
|  （空行）                  |  ← ヘッダーとボディの区切り
+---------------------------+
|  ボディ部                 |  ← 実際のデータ（HTML, JSONなど）
+---------------------------+
```

---

## 3.2 ヘッダーの4つの分類

HTTPヘッダーは、その役割に応じて4つに分類されます。

| 分類 | 英語名 | 説明 | 例 |
|------|--------|------|-----|
| **一般ヘッダー** | General Header | リクエスト・レスポンス両方で使用 | Cache-Control, Connection |
| **リクエストヘッダー** | Request Header | クライアントからの要求情報 | Host, User-Agent, Accept |
| **レスポンスヘッダー** | Response Header | サーバーからの応答情報 | Server, Set-Cookie, Location |
| **エンティティヘッダー** | Entity Header | ボディの属性情報 | Content-Type, Content-Length |

```
【リクエスト時】
クライアント → サーバー

  一般ヘッダー        ← 両方で使える
  リクエストヘッダー  ← リクエスト固有
  エンティティヘッダー ← ボディがある場合

【レスポンス時】
サーバー → クライアント

  一般ヘッダー        ← 両方で使える
  レスポンスヘッダー  ← レスポンス固有
  エンティティヘッダー ← ボディがある場合
```

> **補足**: HTTP/2以降では、これらの分類よりも「擬似ヘッダーフィールド」（`:method`, `:path` など）という概念が加わっています。ただし、基本的な考え方は同じです。

---

## 3.3 主要なリクエストヘッダー

### Host

アクセス先のホスト名（ドメイン名）とポート番号を指定します。HTTP/1.1では**必須**のヘッダーです。

```
Host: www.example.com
Host: api.example.com:8080
```

> **なぜ必須？**: 1つのIPアドレスで複数のWebサイトをホスティングする**バーチャルホスト**の仕組みに必要だからです。サーバーはHostヘッダーを見て、どのサイトへのリクエストか判別します。

### User-Agent

クライアント（ブラウザなど）の種類やバージョンを伝えます。

```
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

```
User-Agent: curl/8.4.0
```

> **実務でのポイント**: User-Agentを見て、モバイル向け・PC向けのレスポンスを切り替えるサーバーもあります。APIのスクレイピングブロックにも使われるため、適切なUser-Agentを設定することが重要です。

### Accept

クライアントが受け取りたい**メディアタイプ**（MIMEタイプ）を伝えます。

```
Accept: text/html, application/xhtml+xml, application/xml;q=0.9, */*;q=0.8
```

`q=0.9` は**品質値**（Quality Value）で、優先度を0〜1で表します（デフォルトは1.0）。

### Accept-Language

希望する言語を伝えます。

```
Accept-Language: ja, en-US;q=0.9, en;q=0.8
```

この例では「日本語を最優先、次に米国英語、その次に英語」という意味です。

### Accept-Encoding

クライアントが対応している圧縮方式を伝えます。

```
Accept-Encoding: gzip, deflate, br
```

| 値 | 圧縮方式 |
|----|---------|
| gzip | GNU zip形式（最も普及） |
| deflate | zlib形式 |
| br | Brotli（Googleが開発、高圧縮率） |

### Authorization

認証情報を送信します。認証方式によって値の形式が異なります。

```
Authorization: Basic dXNlcjpwYXNzd29yZA==
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

> **注意**: 認証の詳細は第4章で解説します。

### Cookie

サーバーから以前受け取ったクッキーを送り返します。

```
Cookie: session_id=abc123; theme=dark; lang=ja
```

### Referer

現在のリクエストの**参照元ページのURL**を伝えます。

```
Referer: https://www.example.com/page1.html
```

> **よくある間違い**: 正しい英語スペルは "Referrer" ですが、HTTP仕様策定時のタイプミスにより "Referer" となっています。この綴りは変更されずに残っています。

### Content-Type（リクエスト時）

POSTやPUTリクエストでボディに含まれるデータの形式を伝えます。

```
Content-Type: application/json
Content-Type: application/x-www-form-urlencoded
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary
```

### Content-Length（リクエスト時）

ボディのバイト数を伝えます。

```
Content-Length: 256
```

---

## 3.4 主要なレスポンスヘッダー

### Content-Type

レスポンスボディのメディアタイプと文字エンコーディングを指定します。

```
Content-Type: text/html; charset=utf-8
Content-Type: application/json
Content-Type: image/png
```

### Content-Length

レスポンスボディのサイズ（バイト数）を伝えます。

```
Content-Length: 12345
```

### Cache-Control

キャッシュの動作を指示します（詳細は第6章で解説）。

```
Cache-Control: max-age=3600
Cache-Control: no-cache
Cache-Control: no-store
```

### Set-Cookie

クライアントにクッキーを保存させます（詳細は第4章で解説）。

```
Set-Cookie: session_id=abc123; Path=/; HttpOnly; Secure; SameSite=Strict
```

### Location

リダイレクト先のURLを指定します。3xx系のステータスコードと一緒に使います。

```
HTTP/1.1 301 Moved Permanently
Location: https://www.example.com/new-page
```

### Server

Webサーバーのソフトウェア情報を伝えます。

```
Server: nginx/1.24.0
Server: Apache/2.4.57
```

> **実務でのポイント**: セキュリティの観点から、サーバーのバージョン情報は隠すのが一般的です。攻撃者にバージョンを知られると、既知の脆弱性を狙われる可能性があります。

### Access-Control-Allow-Origin

CORS（Cross-Origin Resource Sharing / オリジン間リソース共有）で、アクセスを許可するオリジン（Origin）を指定します。

```
Access-Control-Allow-Origin: https://www.example.com
Access-Control-Allow-Origin: *
```

> **用語解説**: オリジンとは「スキーム + ホスト + ポート番号」の組み合わせです。`https://example.com:443` と `http://example.com:80` は異なるオリジンです。

---

## 3.5 Content-TypeとMIMEタイプ

### MIMEタイプとは

MIME（Multipurpose Internet Mail Extensions）タイプは、データの種類を表す標準的な書式です。もともとメールの添付ファイルのために作られた仕組みですが、HTTPでも広く使われています。

### MIMEタイプの書式

```
タイプ/サブタイプ
```

### 主要なMIMEタイプ一覧

| MIMEタイプ | 説明 | 用途 |
|-----------|------|------|
| `text/html` | HTML文書 | Webページ |
| `text/plain` | プレーンテキスト | テキストファイル |
| `text/css` | CSSスタイルシート | スタイル定義 |
| `text/javascript` | JavaScript | スクリプト |
| `application/json` | JSONデータ | API通信 |
| `application/xml` | XMLデータ | データ交換 |
| `application/pdf` | PDFファイル | ドキュメント |
| `application/octet-stream` | バイナリデータ（汎用） | ファイルダウンロード |
| `application/x-www-form-urlencoded` | URLエンコードされたフォーム | HTMLフォーム送信 |
| `multipart/form-data` | マルチパートデータ | ファイルアップロード |
| `image/png` | PNG画像 | 画像表示 |
| `image/jpeg` | JPEG画像 | 画像表示 |
| `image/svg+xml` | SVG画像 | ベクター画像 |

### フォーム送信時のContent-Type

HTMLフォームを送信するとき、Content-Typeは`enctype`属性で決まります。

**application/x-www-form-urlencoded（デフォルト）**

```
POST /login HTTP/1.1
Content-Type: application/x-www-form-urlencoded

username=taro&password=secret123
```

キーと値が `=` で結ばれ、`&` で区切られます。日本語などはURLエンコードされます。

**multipart/form-data（ファイルアップロード時）**

```
POST /upload HTTP/1.1
Content-Type: multipart/form-data; boundary=----Boundary123

------Boundary123
Content-Disposition: form-data; name="file"; filename="photo.jpg"
Content-Type: image/jpeg

（バイナリデータ）
------Boundary123
Content-Disposition: form-data; name="description"

旅行の写真
------Boundary123--
```

> **よくある間違い**: ファイルをアップロードするのに `application/x-www-form-urlencoded` を使ってしまうケース。ファイルアップロードには必ず `multipart/form-data` を使います。

**application/json（API通信）**

```
POST /api/users HTTP/1.1
Content-Type: application/json

{"name": "太郎", "email": "taro@example.com"}
```

---

## 3.6 コンテンツネゴシエーション

コンテンツネゴシエーション（Content Negotiation）とは、同じURLに対して**クライアントの希望に応じて最適な表現を返す**仕組みです。

### ネゴシエーションの流れ

```
クライアント                              サーバー
    |                                        |
    |  Accept: application/json              |
    |  Accept-Language: ja                   |
    |  Accept-Encoding: gzip, br             |
    |--------------------------------------->|
    |                                        |
    |  Content-Type: application/json        |
    |  Content-Language: ja                  |
    |  Content-Encoding: gzip               |
    |<---------------------------------------|
    |                                        |
```

### ネゴシエーションで使われるヘッダー

| リクエストヘッダー | レスポンスヘッダー | 対象 |
|-------------------|-------------------|------|
| Accept | Content-Type | メディアタイプ |
| Accept-Language | Content-Language | 言語 |
| Accept-Encoding | Content-Encoding | 圧縮方式 |
| Accept-Charset | Content-Type (charset) | 文字コード |

### 品質値（Quality Value）による優先度指定

```
Accept: text/html;q=1.0, application/json;q=0.9, text/plain;q=0.5
```

| 品質値 | 意味 |
|--------|------|
| q=1.0 | 最も希望する（省略時のデフォルト） |
| q=0.9 | かなり希望する |
| q=0.5 | まあまあ |
| q=0.0 | 受け入れ不可 |

### Pythonでの確認例

```python
import http.client

conn = http.client.HTTPSConnection("httpbin.org")

# 日本語JSONを希望するリクエスト
headers = {
    "Accept": "application/json",
    "Accept-Language": "ja;q=1.0, en;q=0.5"
}

conn.request("GET", "/headers", headers=headers)
response = conn.getresponse()
print(response.read().decode())
conn.close()
```

---

## 3.7 カスタムヘッダー

### X-接頭辞の歴史

かつては、標準仕様にないカスタムヘッダーには `X-` 接頭辞を付ける慣習がありました。

```
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000
X-Forwarded-For: 192.168.1.1
X-RateLimit-Limit: 100
```

しかし、RFC 6648（2012年）で `X-` 接頭辞は**非推奨**とされました。理由は、カスタムヘッダーが後に標準化された際に名前を変更するのが困難だからです。

### 現在の慣習

現在は `X-` を付けても付けなくてもよいとされていますが、以下のような傾向があります。

| パターン | 例 | 説明 |
|---------|-----|------|
| 歴史的に`X-`が定着したもの | `X-Forwarded-For` | 変更すると互換性が壊れるためそのまま使用 |
| 新しい標準ヘッダー | `Forwarded` | X-Forwarded-Forの後継として標準化 |
| アプリケーション固有 | `X-Request-ID` | 未だにX-を付けることが多い |

> **実務でのポイント**: API設計では、独自ヘッダーを使ってリクエストID、レート制限情報、ページネーション情報などを伝えることが一般的です。

### よく使われるカスタムヘッダー

```
# リクエストの追跡用ID
X-Request-ID: 550e8400-e29b-41d4-a716-446655440000

# プロキシ経由のクライアントIPアドレス
X-Forwarded-For: 203.0.113.50, 70.41.3.18

# API利用制限
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1609459200
```

---

## 3.8 curlコマンドでのヘッダー確認

### レスポンスヘッダーの確認

```bash
# -I : HEADリクエストでヘッダーだけ取得
curl -I https://www.example.com

# -v : 詳細表示（リクエストヘッダーとレスポンスヘッダーの両方）
curl -v https://www.example.com

# -D - : レスポンスヘッダーを標準出力に表示
curl -D - https://www.example.com
```

### -v オプションの出力の読み方

```
* Connected to www.example.com (93.184.216.34) port 443
> GET / HTTP/1.1          ← 「>」はリクエスト（送信データ）
> Host: www.example.com
> User-Agent: curl/8.4.0
> Accept: */*
>
< HTTP/1.1 200 OK         ← 「<」はレスポンス（受信データ）
< Content-Type: text/html; charset=UTF-8
< Content-Length: 1256
< Cache-Control: max-age=604800
< Server: ECAcc (sab/576E)
<
```

### カスタムヘッダーの送信

```bash
# -H でヘッダーを追加
curl -H "Accept: application/json" https://httpbin.org/headers

# 複数のヘッダーを指定
curl -H "Accept: application/json" \
     -H "Authorization: Bearer mytoken123" \
     -H "X-Request-ID: abc-123" \
     https://httpbin.org/headers
```

### Pythonでのヘッダー確認

```python
import http.client

conn = http.client.HTTPSConnection("www.example.com")
conn.request("GET", "/")
response = conn.getresponse()

# ステータスコード
print(f"Status: {response.status} {response.reason}")

# 全レスポンスヘッダーを表示
print("\n--- レスポンスヘッダー ---")
for header, value in response.getheaders():
    print(f"{header}: {value}")

conn.close()
```

実行結果の例:

```
Status: 200 OK

--- レスポンスヘッダー ---
content-type: text/html; charset=UTF-8
content-length: 1256
cache-control: max-age=604800
server: ECAcc (sab/576E)
```

---

## 3.9 実務でのポイント

### セキュリティ関連ヘッダー

実際のWebサービスでは、セキュリティを強化するために以下のヘッダーがよく設定されます。

| ヘッダー | 役割 |
|---------|------|
| `Strict-Transport-Security` (HSTS) | HTTPS接続を強制 |
| `X-Content-Type-Options: nosniff` | MIMEタイプの推測を防止 |
| `X-Frame-Options: DENY` | クリックジャッキング対策 |
| `Content-Security-Policy` (CSP) | XSS対策（読み込み可能なリソースを制限） |
| `X-XSS-Protection` | ブラウザのXSSフィルターを有効化 |

### CORS関連ヘッダー

フロントエンド開発で頻繁に遭遇するのがCORS関連のヘッダーです。

```
# レスポンスヘッダー
Access-Control-Allow-Origin: https://frontend.example.com
Access-Control-Allow-Methods: GET, POST, PUT, DELETE
Access-Control-Allow-Headers: Content-Type, Authorization
Access-Control-Max-Age: 86400
```

> **よくある間違い**: 開発中に `Access-Control-Allow-Origin: *` で全オリジンを許可してしまい、そのまま本番環境に持ち込んでしまうケース。本番では必ず**特定のオリジンのみ許可**しましょう。

---

## ポイントまとめ

1. **HTTPヘッダーは「キー: 値」の形式**で、リクエスト・レスポンスのメタ情報を伝える
2. ヘッダーは**一般・リクエスト・レスポンス・エンティティ**の4つに分類される
3. **Hostヘッダー**はHTTP/1.1で必須（バーチャルホストの判別に必要）
4. **Content-Type**はボディのデータ形式を示す最も重要なヘッダーの一つ
5. **MIMEタイプ**は `タイプ/サブタイプ` の形式でデータの種類を表す
6. **コンテンツネゴシエーション**でクライアントの希望に応じた最適なレスポンスを返せる
7. カスタムヘッダーの**X-接頭辞**は非推奨だが、歴史的に定着したものは今も使われている
8. **curlの-vオプション**で送受信されるヘッダーの詳細を確認できる
9. セキュリティヘッダーの設定は**実務で必須**の知識
