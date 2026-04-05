# 第3章：HTTPヘッダー 演習問題

## 基本問題

### 問題3-1：ヘッダーの分類

以下のHTTPヘッダーを「リクエストヘッダー」「レスポンスヘッダー」「一般ヘッダー」「エンティティヘッダー」のいずれかに分類してください。

1. Host
2. Cache-Control
3. Content-Type
4. Set-Cookie
5. User-Agent
6. Server
7. Accept

<details>
<summary>解答</summary>

1. Host → **リクエストヘッダー**（アクセス先のホスト名を指定）
2. Cache-Control → **一般ヘッダー**（リクエスト・レスポンス両方で使用）
3. Content-Type → **エンティティヘッダー**（ボディのデータ形式を指定）
4. Set-Cookie → **レスポンスヘッダー**（サーバーがクライアントにCookieを設定）
5. User-Agent → **リクエストヘッダー**（クライアントの種類を伝える）
6. Server → **レスポンスヘッダー**（サーバーソフトウェアの情報）
7. Accept → **リクエストヘッダー**（クライアントが受け入れ可能なメディアタイプ）

</details>

### 問題3-2：MIMEタイプの選択

以下のデータを送受信する場合に適切なMIMEタイプ（Content-Type）を答えてください。

1. HTMLで記述されたWebページ
2. REST APIからのJSON形式のレスポンス
3. ユーザーがプロフィール画像（PNG）をアップロードするフォーム
4. HTMLフォームからの通常のテキストデータ送信
5. CSSスタイルシート

<details>
<summary>解答</summary>

1. `text/html; charset=utf-8` （HTMLドキュメント）
2. `application/json` （JSONデータ）
3. `multipart/form-data` （ファイルアップロードを含むフォーム）
4. `application/x-www-form-urlencoded` （HTMLフォームのデフォルト）
5. `text/css` （CSSスタイルシート）

**補足**: ファイルアップロードで `application/x-www-form-urlencoded` を使うのはよくある間違いです。バイナリデータを含む場合は必ず `multipart/form-data` を使います。

</details>

### 問題3-3：品質値の優先順位

以下のAcceptヘッダーについて、サーバーはどの形式を優先して返すべきか、優先度の高い順に並べてください。

```
Accept: text/plain;q=0.5, application/json;q=0.9, text/html, application/xml;q=0.1
```

<details>
<summary>解答</summary>

優先度の高い順:

1. `text/html` （q=1.0 ※品質値を省略した場合のデフォルト）
2. `application/json` （q=0.9）
3. `text/plain` （q=0.5）
4. `application/xml` （q=0.1）

**ポイント**: 品質値（q値）を省略した場合は**q=1.0（最高優先度）**として扱われます。

</details>

## 応用問題

### 問題3-4：curlコマンドの作成

以下の条件を満たすcurlコマンドを記述してください。

- 送信先: `https://api.example.com/users`
- HTTPメソッド: POST
- 送信データ: `{"name": "太郎", "age": 25}`
- Content-Type: JSON形式
- 認証: Bearer Token `mytoken123`
- レスポンスヘッダーとボディの両方を表示する

<details>
<summary>ヒント</summary>

- `-X POST` でPOSTメソッドを指定します
- `-H` でヘッダーを追加します
- `-d` でボディデータを指定します
- `-D -` でレスポンスヘッダーを標準出力に表示します

</details>

<details>
<summary>解答</summary>

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mytoken123" \
  -d '{"name": "太郎", "age": 25}' \
  -D - \
  https://api.example.com/users
```

**補足**: `-v` オプションを使えばリクエストヘッダーも含めた詳細な通信内容を確認できます。

```bash
curl -v -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer mytoken123" \
  -d '{"name": "太郎", "age": 25}' \
  https://api.example.com/users
```

</details>

### 問題3-5：レスポンスヘッダーの読み取り

以下のレスポンスヘッダーを見て、各問いに答えてください。

```
HTTP/1.1 301 Moved Permanently
Server: nginx/1.24.0
Content-Type: text/html; charset=utf-8
Content-Length: 162
Location: https://www.example.com/new-page
Cache-Control: max-age=3600
Set-Cookie: tracking=abc123; Path=/; Secure; HttpOnly
X-Request-ID: 7f3d2a1b-4c5e-6f7g-8h9i-0j1k2l3m4n5o
Access-Control-Allow-Origin: https://frontend.example.com
```

1. このレスポンスを受け取ったブラウザは何をしますか？
2. Content-Typeから、レスポンスボディはどのような形式ですか？
3. セキュリティ上の懸念点はありますか？
4. X-Request-IDヘッダーの役割は何ですか？
5. CORSの設定はどうなっていますか？

<details>
<summary>解答</summary>

1. **301リダイレクト**のため、ブラウザは `https://www.example.com/new-page` に自動的にリダイレクトします。301は恒久的な移転を意味します。

2. `text/html; charset=utf-8` なので、**UTF-8エンコーディングのHTML文書**です。

3. **Serverヘッダーにバージョン情報（nginx/1.24.0）が含まれている**点がセキュリティ上の懸念です。攻撃者にバージョンを知られると、既知の脆弱性を狙われる可能性があります。バージョン情報は隠すのが望ましいです。

4. **リクエストの追跡（トレーシング）用のID**です。複数のサービスを横断してリクエストを追跡する際に使用されます。ログ調査やデバッグ時に役立ちます。

5. `Access-Control-Allow-Origin: https://frontend.example.com` により、**`https://frontend.example.com` からのクロスオリジンリクエストのみ許可**されています。特定のオリジンに限定しているため、適切な設定です。

</details>

### 問題3-6：Pythonでのヘッダー確認

Pythonの`http.client`を使って、`https://httpbin.org/response-headers?Content-Type=application/json&X-Custom=hello` にGETリクエストを送信し、レスポンスヘッダーをすべて表示するプログラムを作成してください。

<details>
<summary>ヒント</summary>

- `http.client.HTTPSConnection` でHTTPS接続を作成します
- `response.getheaders()` で全ヘッダーを取得できます

</details>

<details>
<summary>解答</summary>

```python
import http.client

# HTTPS接続を作成
conn = http.client.HTTPSConnection("httpbin.org")

# GETリクエストを送信
conn.request("GET", "/response-headers?Content-Type=application/json&X-Custom=hello")

# レスポンスを取得
response = conn.getresponse()

# ステータスコードの表示
print(f"Status: {response.status} {response.reason}")
print()

# 全レスポンスヘッダーを表示
print("--- レスポンスヘッダー ---")
for name, value in response.getheaders():
    print(f"{name}: {value}")

# ボディも読み取り（接続を正しく閉じるため）
body = response.read()
print()
print("--- レスポンスボディ ---")
print(body.decode())

# 接続を閉じる
conn.close()
```

**実行結果の例:**

```
Status: 200 OK

--- レスポンスヘッダー ---
content-type: application/json
x-custom: hello
content-length: 87
...

--- レスポンスボディ ---
{"Content-Type": "application/json", "X-Custom": "hello"}
```

</details>

## チャレンジ問題

### 問題3-7：コンテンツネゴシエーションの実装

以下のシナリオを考えてください。

APIサーバーがエンドポイント `/api/data` を提供しており、以下の3形式でレスポンスを返せます。
- JSON (`application/json`)
- XML (`application/xml`)
- プレーンテキスト (`text/plain`)

クライアントが以下のリクエストを送った場合、サーバーはどの形式で返すべきですか？それぞれ理由とともに答えてください。

1. `Accept: application/xml;q=0.9, application/json`
2. `Accept: text/html`
3. `Accept: */*`
4. `Accept: application/json;q=0.5, text/plain;q=0.5, application/xml;q=0.5`

<details>
<summary>解答</summary>

1. **JSON（application/json）** を返すべきです。
   - `application/json` は品質値を省略しているため q=1.0
   - `application/xml` は q=0.9
   - JSONの方が優先度が高いため

2. **406 Not Acceptable** を返すか、サーバーの判断でいずれかの形式を返します。
   - `text/html` はサーバーが対応していない形式
   - 厳密にはHTTP仕様では406を返すべきですが、実務ではサーバーのデフォルト形式（多くの場合JSON）を返すことも一般的です

3. **サーバーのデフォルト形式**（通常JSON）を返します。
   - `*/*` は「どの形式でも受け入れる」という意味
   - サーバーは自由に最適な形式を選べます

4. **どの形式でも可**ですが、一般的にはサーバーのデフォルト形式を返します。
   - 3つとも同じ優先度（q=0.5）なので、サーバーが任意に選択します
   - 多くのAPIサーバーではJSON形式がデフォルトです

</details>

### 問題3-8：セキュリティヘッダーの設定

あなたはWebアプリケーションのセキュリティ担当です。以下の攻撃を防ぐために設定すべきレスポンスヘッダーをそれぞれ記述してください。

1. XSS（クロスサイトスクリプティング）攻撃を防ぎたい
2. HTTPでのアクセスを強制的にHTTPSにリダイレクトしたい
3. 他のサイトの `<iframe>` で自サイトが埋め込まれること（クリックジャッキング）を防ぎたい
4. ブラウザがContent-Typeを推測して実行することを防ぎたい
5. 他オリジンからのAPIアクセスを `https://app.example.com` にのみ許可したい

<details>
<summary>解答</summary>

```
# 1. XSS対策 - コンテンツセキュリティポリシー
Content-Security-Policy: default-src 'self'; script-src 'self'

# 2. HTTPS強制 - HTTP Strict Transport Security
Strict-Transport-Security: max-age=31536000; includeSubDomains

# 3. クリックジャッキング対策
X-Frame-Options: DENY
# または
Content-Security-Policy: frame-ancestors 'none'

# 4. MIMEスニッフィング対策
X-Content-Type-Options: nosniff

# 5. CORS設定
Access-Control-Allow-Origin: https://app.example.com
```

**解説:**
- CSP（Content-Security-Policy）は最も強力なXSS対策で、読み込み可能なリソースのオリジンを細かく制御できます
- HSTSはmax-ageで指定した秒数（31536000秒 = 1年）の間、ブラウザがHTTPSを強制します
- X-Frame-Optionsは古いブラウザ向け、CSPのframe-ancestorsは新しいブラウザ向けの対策です。両方設定するのが推奨です
- nosniffを指定しないと、ブラウザがファイル内容からContent-Typeを推測し、意図しない実行が起こる可能性があります

</details>
