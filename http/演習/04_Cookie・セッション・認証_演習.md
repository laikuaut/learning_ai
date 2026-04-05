# 第4章：Cookie・セッション・認証 演習問題

## 基本問題

### 問題4-1：Cookieの基本

以下の文章の空欄を埋めてください。

1. サーバーがクライアントにCookieを設定するには (___) ヘッダーを使用します。
2. クライアントがサーバーにCookieを送信するには (___) ヘッダーを使用します。
3. ExpiresもMax-Ageも設定しないCookieを (___) Cookieと呼び、ブラウザを閉じると消えます。
4. HTTPはリクエストごとに状態を保持しない (___) なプロトコルです。

<details>
<summary>解答</summary>

1. **Set-Cookie** ヘッダー
2. **Cookie** ヘッダー
3. **セッション**Cookie
4. **ステートレス**（Stateless）なプロトコル

</details>

### 問題4-2：Cookie属性の理解

以下のSet-Cookieヘッダーについて、各属性の意味を説明してください。

```
Set-Cookie: session_id=abc123; Domain=example.com; Path=/app; Max-Age=3600; Secure; HttpOnly; SameSite=Lax
```

<details>
<summary>解答</summary>

| 属性 | 値 | 意味 |
|------|-----|------|
| `session_id=abc123` | - | Cookieの名前と値 |
| `Domain=example.com` | example.com | example.comとそのサブドメインにCookieを送信する |
| `Path=/app` | /app | /app以下のパスにのみCookieを送信する |
| `Max-Age=3600` | 3600 | 設定から3600秒（1時間）後にCookieが失効する |
| `Secure` | - | HTTPS通信のときだけCookieを送信する |
| `HttpOnly` | - | JavaScriptのdocument.cookieからアクセスできない |
| `SameSite=Lax` | Lax | トップレベルナビゲーション（リンククリック）では送信するが、サブリクエスト（画像、iframe等）やPOSTでは送信しない |

</details>

### 問題4-3：認証方式の分類

以下のAuthorizationヘッダーの値がどの認証方式か答えてください。

1. `Authorization: Basic dXNlcjpwYXNzd29yZA==`
2. `Authorization: Bearer eyJhbGciOiJIUzI1NiIs...`
3. `X-API-Key: sk-abc123def456`

<details>
<summary>解答</summary>

1. **Basic認証** - ユーザー名とパスワードをBase64エンコードした値。`dXNlcjpwYXNzd29yZA==` をデコードすると `user:password` になります。

2. **Bearer Token認証（JWT）** - JWTトークンをBearerスキームで送信。ヘッダー・ペイロード・署名の3パートをドットで区切った形式です。

3. **APIキー認証** - 独自のカスタムヘッダー（X-API-Key）でAPIキーを送信する方式。Authorizationヘッダーではなくカスタムヘッダーを使用しています。

</details>

### 問題4-4：セッション管理の流れ

サーバーサイドセッションにおけるログイン処理の流れを、以下の選択肢から正しい順番に並べてください。

A. サーバーがセッションIDをSet-Cookieで返す
B. ブラウザが次回リクエストでCookieヘッダーにセッションIDを含める
C. サーバーがセッションIDに紐づくユーザー情報を検索する
D. ユーザーがユーザー名とパスワードを送信する
E. サーバーがセッションIDを生成し、ユーザー情報と紐付けて保存する
F. サーバーがユーザー名とパスワードを検証する

<details>
<summary>解答</summary>

正しい順番: **D → F → E → A → B → C**

1. **D**: ユーザーがユーザー名とパスワードを送信する
2. **F**: サーバーがユーザー名とパスワードを検証する
3. **E**: サーバーがセッションIDを生成し、ユーザー情報と紐付けて保存する
4. **A**: サーバーがセッションIDをSet-Cookieで返す
5. **B**: ブラウザが次回リクエストでCookieヘッダーにセッションIDを含める
6. **C**: サーバーがセッションIDに紐づくユーザー情報を検索する

</details>

## 応用問題

### 問題4-5：セキュリティ上の問題の指摘

以下のSet-Cookieヘッダーにはセキュリティ上の問題があります。問題点をすべて挙げ、改善案を示してください。

```
Set-Cookie: session_id=abc123; Path=/; Domain=example.com
```

<details>
<summary>ヒント</summary>

セキュリティに関わるCookie属性として、Secure、HttpOnly、SameSiteがあります。これらが設定されていない場合にどのようなリスクがあるか考えてみましょう。

</details>

<details>
<summary>解答</summary>

**問題点:**

1. **Secure属性がない** → HTTP通信でもCookieが送信されるため、ネットワーク上で盗聴される可能性がある
2. **HttpOnly属性がない** → JavaScriptからdocument.cookieでセッションIDにアクセスでき、XSS攻撃でCookieを窃取される可能性がある
3. **SameSite属性がない** → ブラウザのデフォルト動作に依存する。明示的に設定しないとCSRF攻撃のリスクがある
4. **Max-AgeまたはExpiresがない** → セッションCookieとなりブラウザを閉じると消えるが、明示的なタイムアウトがない

**改善案:**

```
Set-Cookie: session_id=abc123; Path=/; Domain=example.com; Secure; HttpOnly; SameSite=Lax; Max-Age=3600
```

</details>

### 問題4-6：CSRF攻撃の理解

以下のシナリオについて、(1) なぜ攻撃が成功するのか、(2) どのような対策が有効かを説明してください。

**シナリオ:**

ユーザーAが `https://shop.example.com` にログインしており、セッションCookieが以下のように設定されています。

```
Set-Cookie: session_id=abc123; Path=/; Secure; HttpOnly
```

攻撃者が作成した罠サイト `https://evil.example.com` に以下のHTMLが仕込まれています。

```html
<img src="https://shop.example.com/api/purchase?item=gift-card&amount=10000&to=attacker" />
```

ユーザーAが罠サイトにアクセスした場合、何が起きますか？

<details>
<summary>解答</summary>

**(1) なぜ攻撃が成功するのか:**

- `<img>` タグのsrc属性はブラウザが自動的にGETリクエストを送信します
- ブラウザは `shop.example.com` へのリクエストにCookieを自動的に付与します
- **SameSite属性が設定されていない**ため、クロスサイトからのリクエストにもCookieが送信されます
- サーバーは正規ユーザーからのリクエストと区別できず、購入処理が実行されてしまいます

**(2) 有効な対策:**

1. **SameSite属性を設定する**: `SameSite=Lax` を設定すれば、imgタグのようなサブリクエストではCookieが送信されません
   ```
   Set-Cookie: session_id=abc123; Path=/; Secure; HttpOnly; SameSite=Lax
   ```

2. **状態変更操作にGETを使わない**: 購入のような操作はPOSTメソッドで実装すべきです。GETは安全なメソッド（データの取得のみ）に限定しましょう

3. **CSRFトークンを導入する**: サーバーが生成した一意のトークンをリクエストに含めることを要求します

4. **Originヘッダーの検証**: リクエストのOriginヘッダーが自サイトかどうかを確認します

</details>

### 問題4-7：curlでのCookie操作

以下の操作を行うcurlコマンドをそれぞれ記述してください。

1. `https://httpbin.org/cookies/set/username/taro` にアクセスしてCookieを受け取り、`cookies.txt` に保存する
2. 保存した `cookies.txt` のCookieを使って `https://httpbin.org/cookies` にアクセスする
3. 手動で `session_id=xyz789` と `lang=ja` の2つのCookieを送信して `https://httpbin.org/cookies` にアクセスする

<details>
<summary>解答</summary>

```bash
# 1. Cookieを受け取ってファイルに保存
curl -c cookies.txt -L https://httpbin.org/cookies/set/username/taro

# 2. 保存したCookieファイルを使ってリクエスト
curl -b cookies.txt https://httpbin.org/cookies

# 3. 手動でCookieを指定してリクエスト
curl -b "session_id=xyz789; lang=ja" https://httpbin.org/cookies
```

**解説:**
- `-c` (--cookie-jar): レスポンスのCookieをファイルに保存
- `-b` (--cookie): Cookieを送信（ファイル名または「名前=値」形式）
- `-L` (--location): リダイレクトを自動追従（cookieの設定エンドポイントは302リダイレクトを返すため）

**実行結果の例（3番）:**

```json
{
  "cookies": {
    "lang": "ja",
    "session_id": "xyz789"
  }
}
```

</details>

## チャレンジ問題

### 問題4-8：Basic認証のPython実装

Pythonの `http.client` と `base64` モジュールを使って、以下の処理を行うプログラムを作成してください。

1. ユーザー名 `testuser`、パスワード `testpass` をBase64エンコードする
2. `https://httpbin.org/basic-auth/testuser/testpass` にBasic認証付きでリクエストを送信する
3. ステータスコードとレスポンスボディを表示する

<details>
<summary>ヒント</summary>

- `base64.b64encode()` でBase64エンコードできます
- エンコードする文字列は `ユーザー名:パスワード` の形式です
- `b64encode()` はバイト列を返すので `.decode("ascii")` で文字列に変換します

</details>

<details>
<summary>解答</summary>

```python
import http.client
import base64

# 1. Base64エンコード
username = "testuser"
password = "testpass"
credentials = f"{username}:{password}"
encoded = base64.b64encode(credentials.encode()).decode("ascii")
print(f"Base64エンコード結果: {encoded}")

# 2. Basic認証付きリクエスト
conn = http.client.HTTPSConnection("httpbin.org")
headers = {
    "Authorization": f"Basic {encoded}"
}
conn.request("GET", "/basic-auth/testuser/testpass", headers=headers)

# 3. レスポンスの表示
response = conn.getresponse()
print(f"\nステータスコード: {response.status} {response.reason}")
print(f"レスポンスボディ: {response.read().decode()}")

conn.close()
```

**実行結果:**

```
Base64エンコード結果: dGVzdHVzZXI6dGVzdHBhc3M=

ステータスコード: 200 OK
レスポンスボディ: {
  "authenticated": true,
  "user": "testuser"
}
```

</details>

### 問題4-9：安全なCookie設定の設計

あなたはECサイトのバックエンド開発者です。以下の3種類のCookieを設計してください。それぞれのSet-Cookieヘッダーを記述し、各属性を選んだ理由を説明してください。

1. **セッションCookie**（ユーザーのログイン状態を管理）
2. **言語設定Cookie**（ユーザーが選択した表示言語を記憶、30日間保持）
3. **外部分析サービス用Cookie**（サードパーティの分析サービスが使用）

<details>
<summary>解答</summary>

**1. セッションCookie:**

```
Set-Cookie: session_id=<ランダムな長い文字列>; Path=/; Secure; HttpOnly; SameSite=Lax; Max-Age=1800
```

| 属性 | 理由 |
|------|------|
| `Secure` | 認証情報を含むためHTTPS必須 |
| `HttpOnly` | XSSによるセッションID窃取を防止 |
| `SameSite=Lax` | CSRF対策。Strictだとリンクからのアクセスでもログアウト状態になるため、Laxが実用的 |
| `Max-Age=1800` | 30分のタイムアウトで、長時間放置時のリスクを軽減 |

**2. 言語設定Cookie:**

```
Set-Cookie: lang=ja; Path=/; Max-Age=2592000; SameSite=Lax
```

| 属性 | 理由 |
|------|------|
| `Max-Age=2592000` | 30日間（30×24×60×60秒）保持 |
| `SameSite=Lax` | 基本的な保護 |
| Secureなし | 言語設定は機密情報ではないため、HTTP環境でも使えるように（ただしHTTPS環境ならSecureを付けるのが望ましい） |
| HttpOnlyなし | JavaScriptから読み取って表示を切り替える可能性があるため |

**3. 外部分析サービス用Cookie:**

```
Set-Cookie: _analytics=<tracking_id>; Path=/; Secure; SameSite=None; Max-Age=31536000
```

| 属性 | 理由 |
|------|------|
| `SameSite=None` | サードパーティCookieとして他サイトからも送信する必要がある |
| `Secure` | SameSite=Noneの場合は必須 |
| `Max-Age=31536000` | 1年間保持（分析データの継続性のため） |

**補足:** 近年のブラウザではサードパーティCookieの廃止が進んでおり、この方式は将来使えなくなる可能性があります。プライバシーサンドボックス等の代替技術への移行を検討する必要があります。

</details>
