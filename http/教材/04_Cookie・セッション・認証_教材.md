# 第4章：Cookie・セッション・認証

## この章のゴール
- Cookieの仕組みとSet-Cookie / Cookieヘッダーの役割を理解する
- Cookieの各属性（Domain, Path, Secure, HttpOnly, SameSiteなど）を正しく設定できる
- セッション管理の仕組みを理解する
- Basic認証、Bearer Token認証、APIキー認証、OAuth 2.0の違いを説明できる
- セッションハイジャック・CSRF攻撃の仕組みと対策を理解する
- ログインフローの全体像を把握する

---

## 4.1 HTTPはステートレス

HTTP（HyperText Transfer Protocol）は**ステートレス**（Stateless / 状態を持たない）なプロトコルです。つまり、サーバーは各リクエストを**独立したもの**として扱い、前回のリクエストの情報を覚えていません。

```
クライアント                  サーバー
    |                            |
    |  1回目: ログインページ表示  |
    |--------------------------->|
    |<---------------------------|
    |                            |  ← この時点でサーバーは
    |  2回目: ログイン処理       |    クライアントを忘れている
    |--------------------------->|
    |<---------------------------|
    |                            |  ← またクライアントを忘れる
    |  3回目: マイページ表示     |
    |--------------------------->|  ← 「あなたは誰？」
```

この問題を解決するのが**Cookie**と**セッション**の仕組みです。

---

## 4.2 Cookieの仕組み

Cookie（クッキー）は、サーバーがクライアント（ブラウザ）に保存させる**小さなデータ**です。

### Cookie のやり取りの流れ

```
クライアント                    サーバー
    |                              |
    |  1. リクエスト（初回）        |
    |----------------------------->|
    |                              |
    |  2. レスポンス               |
    |  Set-Cookie: session=abc123  |  ← Cookieを設定
    |<-----------------------------|
    |                              |
    |  3. 次のリクエスト           |
    |  Cookie: session=abc123      |  ← 自動で送信
    |----------------------------->|
    |                              |  ← サーバーは識別できる
    |  4. レスポンス               |
    |<-----------------------------|
```

### Set-Cookie ヘッダー（サーバー → クライアント）

```
Set-Cookie: session_id=abc123; Path=/; Expires=Thu, 01 Jan 2027 00:00:00 GMT; Secure; HttpOnly; SameSite=Lax
```

### Cookie ヘッダー（クライアント → サーバー）

```
Cookie: session_id=abc123; theme=dark; lang=ja
```

> **ポイント**: Set-Cookieはヘッダーごとに1つのCookieを設定しますが、Cookieヘッダーは複数のCookieをセミコロン区切りで1行にまとめて送信します。

### curlでのCookie操作

```bash
# サーバーからCookieを受け取って表示
curl -v https://httpbin.org/cookies/set/username/taro

# Cookieを送信する
curl -b "session_id=abc123; lang=ja" https://httpbin.org/cookies

# Cookieをファイルに保存して再利用
curl -c cookies.txt https://httpbin.org/cookies/set/test/value
curl -b cookies.txt https://httpbin.org/cookies
```

---

## 4.3 Cookieの属性

### 属性一覧

| 属性 | 説明 | 例 |
|------|------|-----|
| **Domain** | Cookieを送信するドメイン | `Domain=example.com` |
| **Path** | Cookieを送信するパス | `Path=/api` |
| **Expires** | 有効期限（日時指定） | `Expires=Thu, 01 Jan 2027 00:00:00 GMT` |
| **Max-Age** | 有効期限（秒数指定） | `Max-Age=86400`（1日） |
| **Secure** | HTTPS通信時のみ送信 | `Secure` |
| **HttpOnly** | JavaScriptからアクセス不可 | `HttpOnly` |
| **SameSite** | クロスサイトリクエストでの送信制御 | `SameSite=Lax` |

### Domain属性

```
Set-Cookie: token=xyz; Domain=example.com
```

- `Domain=example.com` を設定すると、`sub.example.com` にも送信されます
- Domainを省略すると、**設定元のホストにのみ**送信されます（サブドメインには送信されない）

```
Domain=example.com の場合:
  ✅ example.com          → 送信される
  ✅ sub.example.com      → 送信される
  ✅ api.sub.example.com  → 送信される
  ❌ other-site.com       → 送信されない

Domain省略の場合（example.comが設定元）:
  ✅ example.com          → 送信される
  ❌ sub.example.com      → 送信されない
```

### Path属性

```
Set-Cookie: token=xyz; Path=/api
```

- 指定したパスとその配下にのみCookieが送信されます

```
Path=/api の場合:
  ✅ /api           → 送信される
  ✅ /api/users     → 送信される
  ✅ /api/v2/data   → 送信される
  ❌ /login         → 送信されない
  ❌ /              → 送信されない
```

### ExpiresとMax-Age

```
# 日時で指定（GMT）
Set-Cookie: token=xyz; Expires=Thu, 01 Jan 2027 00:00:00 GMT

# 秒数で指定（設定時点からの経過秒数）
Set-Cookie: token=xyz; Max-Age=86400

# Cookieを削除する場合（過去の日付を指定）
Set-Cookie: token=; Max-Age=0
```

| 種類 | 動作 |
|------|------|
| ExpiresもMax-Ageも省略 | **セッションCookie**（ブラウザを閉じると消える） |
| Expires指定 | 指定日時まで保持 |
| Max-Age指定 | 指定秒数だけ保持 |
| 両方指定 | Max-Ageが優先 |

### Secure属性

```
Set-Cookie: session_id=abc123; Secure
```

- **HTTPS通信のときだけ**Cookieを送信します
- HTTP通信では送信されないため、盗聴のリスクを軽減します

> **実務でのポイント**: 認証情報を含むCookieには**必ずSecure属性を付けましょう**。

### HttpOnly属性

```
Set-Cookie: session_id=abc123; HttpOnly
```

- JavaScriptの `document.cookie` からアクセスできなくなります
- XSS（クロスサイトスクリプティング）攻撃でCookieを盗まれるリスクを軽減します

```javascript
// HttpOnlyが設定されたCookieは
// JavaScriptからアクセスできない
console.log(document.cookie);  // session_id は表示されない
```

### SameSite属性

クロスサイトリクエスト（別サイトからのリクエスト）でCookieを送信するかを制御します。

| 値 | 動作 | 用途 |
|----|------|------|
| **Strict** | 同一サイトからのリクエストのみCookieを送信 | 最も安全、銀行サイトなど |
| **Lax** | トップレベルナビゲーション（リンククリック）は送信、POSTは送信しない | デフォルト推奨 |
| **None** | 常に送信（Secure属性が必須） | サードパーティCookie |

```
# 厳格モード
Set-Cookie: session=abc; SameSite=Strict

# 緩和モード（多くのブラウザのデフォルト）
Set-Cookie: session=abc; SameSite=Lax

# 制限なし（Secureが必須）
Set-Cookie: tracking=xyz; SameSite=None; Secure
```

> **よくある間違い**: `SameSite=None` を設定する際に `Secure` 属性を忘れるケース。最新のブラウザでは `SameSite=None` は `Secure` 属性がないと無視されます。

---

## 4.4 セッション管理の仕組み

セッション（Session）とは、一連のリクエスト・レスポンスのやり取りを**ひとまとまり**として管理する仕組みです。

### サーバーサイドセッションの流れ

```
クライアント                        サーバー
    |                                  |
    |  1. ログイン要求                 |
    |  POST /login                     |
    |  username=taro&password=secret    |
    |--------------------------------->|
    |                                  |  認証OK!
    |                                  |  セッション作成:
    |                                  |  sessions["abc123"] = {
    |                                  |    user: "taro",
    |                                  |    login_at: "2026-04-05"
    |  2. Set-Cookie: session=abc123   |  }
    |<---------------------------------|
    |                                  |
    |  3. マイページ要求               |
    |  GET /mypage                     |
    |  Cookie: session=abc123          |
    |--------------------------------->|
    |                                  |  sessions["abc123"]を検索
    |                                  |  → user: "taro" を特定!
    |  4. 太郎のマイページ             |
    |<---------------------------------|
```

### セッションIDの保存場所

| 保存場所 | メリット | デメリット |
|---------|---------|-----------|
| **Cookie** | 自動送信、実装が簡単 | Cookie無効時に使えない |
| **URLパラメータ** | Cookieなしで動作 | URLにIDが露出（セキュリティリスク） |
| **Hidden フォームフィールド** | Cookie不要 | ページ遷移ごとにフォーム送信が必要 |

> **実務でのポイント**: 現代のWebアプリケーションでは、**CookieにセッションIDを保存する方式**が標準です。URLパラメータにセッションIDを含める方式は、セキュリティリスクが高いため推奨されません。

### Pythonでのセッション管理の概念

```python
import http.client
import json

# --- 1. ログインしてセッションCookieを取得 ---
conn = http.client.HTTPSConnection("httpbin.org")

# httpbin.orgではCookieを設定するエンドポイントを利用
conn.request("GET", "/cookies/set/session_id/abc123")
response = conn.getresponse()

# Set-Cookieヘッダーを確認
for name, value in response.getheaders():
    if name.lower() == "set-cookie":
        print(f"受信Cookie: {value}")

response.read()
conn.close()

# --- 2. 取得したCookieを次のリクエストで送信 ---
conn = http.client.HTTPSConnection("httpbin.org")
headers = {"Cookie": "session_id=abc123"}
conn.request("GET", "/cookies", headers=headers)
response = conn.getresponse()

print(f"\nサーバーが受け取ったCookie:")
print(response.read().decode())
conn.close()
```

---

## 4.5 認証方式の種類と比較

### Basic認証

Basic認証（基本認証）は、ユーザー名とパスワードを**Base64エンコード**してヘッダーに含める方式です。

```
Authorization: Basic dXNlcjpwYXNzd29yZA==
```

```
エンコード前: user:password
Base64変換:  dXNlcjpwYXNzd29yZA==
```

**curlでの使用例:**

```bash
# 方法1: -u オプション
curl -u user:password https://api.example.com/data

# 方法2: ヘッダーを直接指定
curl -H "Authorization: Basic dXNlcjpwYXNzd29yZA==" https://api.example.com/data
```

**Pythonでの実装例:**

```python
import http.client
import base64

# ユーザー名とパスワードをBase64エンコード
credentials = base64.b64encode(b"user:password").decode("ascii")
print(f"エンコード結果: {credentials}")

conn = http.client.HTTPSConnection("httpbin.org")
headers = {"Authorization": f"Basic {credentials}"}
conn.request("GET", "/basic-auth/user/password", headers=headers)
response = conn.getresponse()

print(f"Status: {response.status}")
print(response.read().decode())
conn.close()
```

> **よくある間違い**: Base64は**暗号化ではなく、単なるエンコード**です。誰でも簡単にデコードできます。Basic認証は**必ずHTTPS**と組み合わせて使用してください。

### Bearer Token認証（JWT）

Bearer Token認証は、サーバーが発行した**トークン**をヘッダーに含める方式です。代表的なトークン形式がJWT（JSON Web Token / ジョット）です。

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IuWkqumDjiIsImlhdCI6MTUxNjIzOTAyMn0.xxxxx
```

**JWTの構造:**

```
ヘッダー.ペイロード.署名

eyJhbGciOi...  ←  ヘッダー（アルゴリズム情報）
.
eyJzdWIiOi...  ←  ペイロード（ユーザー情報など）
.
xxxxx          ←  署名（改ざん検知用）
```

```
+------------------+     +------------------+     +------------------+
|    ヘッダー       |  .  |   ペイロード      |  .  |     署名          |
| {                |     | {                |     |                  |
|   "alg": "HS256",|     |   "sub": "123",  |     |  HMACSHA256(     |
|   "typ": "JWT"   |     |   "name": "太郎", |     |    header + "."  |
| }                |     |   "iat": 15162.. |     |    + payload,    |
|                  |     | }                |     |    secret        |
+------------------+     +------------------+     |  )               |
                                                  +------------------+
        ↓ Base64URL           ↓ Base64URL              ↓ Base64URL
```

**curlでの使用例:**

```bash
curl -H "Authorization: Bearer eyJhbGciOi..." https://api.example.com/users
```

### APIキー認証

APIキー（API Key）は、サービスが発行する**固定の文字列**を使って認証する方式です。

```bash
# ヘッダーで送信
curl -H "X-API-Key: sk-abc123def456" https://api.example.com/data

# クエリパラメータで送信
curl "https://api.example.com/data?api_key=sk-abc123def456"
```

> **実務でのポイント**: APIキーはクエリパラメータよりも**ヘッダーで送信する方が安全**です。URLはサーバーログやブラウザ履歴に残るためです。

### OAuth 2.0（概要）

OAuth 2.0は、**第三者のサービスに権限を委譲**する仕組みです。「Googleでログイン」「GitHubでログイン」などで使われています。

```
ユーザー        クライアント        認可サーバー        リソースサーバー
  (ブラウザ)      (Webアプリ)        (Google等)          (API等)
    |                 |                  |                    |
    | 1.ログインボタン  |                  |                    |
    |---------------->|                  |                    |
    |                 |  2.認可リクエスト  |                    |
    |                 |----------------->|                    |
    |  3.ログイン画面  |                  |                    |
    |<----------------------------------|                    |
    |  4.許可          |                  |                    |
    |---------------------------------->|                    |
    |                 |  5.認可コード     |                    |
    |                 |<-----------------|                    |
    |                 |  6.トークン要求   |                    |
    |                 |----------------->|                    |
    |                 |  7.アクセストークン|                    |
    |                 |<-----------------|                    |
    |                 |  8.APIリクエスト  |                    |
    |                 |  (Bearer Token)  |                    |
    |                 |---------------------------------->   |
    |                 |  9.データ         |                    |
    |                 |<------------------------------------|
```

### 認証方式の比較

| 方式 | セキュリティ | 複雑さ | 用途 |
|------|:---:|:---:|------|
| **Basic認証** | 低 | 低 | 内部ツール、テスト環境 |
| **Bearer Token (JWT)** | 高 | 中 | Web/モバイルアプリのAPI |
| **APIキー** | 中 | 低 | 外部サービス連携 |
| **OAuth 2.0** | 高 | 高 | ソーシャルログイン、API連携 |

---

## 4.6 セッションハイジャック・CSRF対策

### セッションハイジャック

セッションハイジャック（Session Hijacking）とは、他人のセッションIDを盗んで**なりすます**攻撃です。

```
攻撃の流れ:

1. 正規ユーザーがログイン → session_id=abc123 を取得
2. 攻撃者がsession_id=abc123 を何らかの手段で入手
3. 攻撃者がCookie: session_id=abc123 を使ってリクエスト
4. サーバーは攻撃者を正規ユーザーと認識してしまう
```

**対策:**

| 対策 | 説明 |
|------|------|
| **HTTPS必須** | 通信の盗聴を防止（Secure属性） |
| **HttpOnly属性** | XSSによるCookie窃取を防止 |
| **セッションIDの定期更新** | ログイン後に新しいIDを発行 |
| **IPアドレス・User-Agentのチェック** | セッション固定化攻撃の検出 |
| **セッションのタイムアウト** | 一定時間で自動失効 |

### CSRF（Cross-Site Request Forgery）

CSRF（クロスサイトリクエストフォージェリ / サイト横断リクエスト偽造）は、ユーザーが意図しないリクエストを**別サイトから送信**させる攻撃です。

```
攻撃の流れ:

1. ユーザーが銀行サイト（bank.example.com）にログイン中
2. 攻撃者の罠サイト（evil.example.com）にアクセス
3. 罠サイトに仕込まれたHTMLが銀行サイトに自動的にPOSTリクエストを送信

   <form action="https://bank.example.com/transfer" method="POST">
     <input type="hidden" name="to" value="attacker">
     <input type="hidden" name="amount" value="1000000">
   </form>
   <script>document.forms[0].submit();</script>

4. ブラウザはbank.example.comへのリクエストにCookieを自動付与
5. 銀行サーバーは正規のリクエストと区別できない
```

**対策:**

| 対策 | 説明 |
|------|------|
| **CSRFトークン** | フォームに予測不可能なトークンを埋め込む |
| **SameSite Cookie** | `SameSite=Strict` または `SameSite=Lax` |
| **Originヘッダーの検証** | リクエスト元のオリジンを確認 |
| **カスタムヘッダーの要求** | `X-Requested-With` 等（ブラウザのCORSプリフライトで保護） |

> **実務でのポイント**: 現代のフレームワーク（Django, Rails, Laravelなど）は**CSRFトークンを自動的に生成・検証する機能**を持っています。これを無効化せずに利用しましょう。

---

## 4.7 実用例：ログインフローの全体像

実際のWebアプリケーションでのログインフローを追いかけてみましょう。

### フロー全体

```
クライアント                              サーバー
    |                                        |
    |  1. GET /login                         |
    |--------------------------------------->|
    |  200 OK (ログインフォーム HTML)          |
    |  Set-Cookie: csrf_token=xyz789         |
    |<---------------------------------------|
    |                                        |
    |  2. POST /login                        |
    |  Content-Type: application/x-www...    |
    |  Cookie: csrf_token=xyz789             |
    |  Body: username=taro&password=...      |
    |        &csrf_token=xyz789              |
    |--------------------------------------->|
    |                                        |  ① CSRFトークン検証 ✅
    |                                        |  ② ユーザー名・パスワード検証 ✅
    |                                        |  ③ セッション作成
    |                                        |
    |  3. 302 Found                          |
    |  Location: /dashboard                  |
    |  Set-Cookie: session_id=newid123;      |
    |    Path=/; Secure; HttpOnly;           |
    |    SameSite=Lax; Max-Age=3600          |
    |<---------------------------------------|
    |                                        |
    |  4. GET /dashboard                     |
    |  Cookie: session_id=newid123           |
    |--------------------------------------->|
    |                                        |  ④ セッション確認 → taro
    |  200 OK (太郎のダッシュボード)           |
    |<---------------------------------------|
    |                                        |
    |  ... 作業 ...                           |
    |                                        |
    |  5. POST /logout                       |
    |  Cookie: session_id=newid123           |
    |--------------------------------------->|
    |                                        |  ⑤ セッション破棄
    |  6. 302 Found                          |
    |  Location: /login                      |
    |  Set-Cookie: session_id=; Max-Age=0    |  ← Cookie削除
    |<---------------------------------------|
```

### 各ステップの解説

1. **ログインページ表示**: CSRFトークンをCookieとフォームに埋め込む
2. **ログイン送信**: CSRFトークンの一致を確認してから認証処理
3. **ログイン成功**: 新しいセッションIDを発行（セッション固定化攻撃の防止）
4. **認証済みページ**: セッションIDでユーザーを特定
5. **ログアウト**: サーバー側のセッションを破棄
6. **Cookie削除**: Max-Age=0でCookieを即座に失効させる

---

## ポイントまとめ

1. HTTPは**ステートレス**なため、状態管理にはCookieとセッションが必要
2. **Set-Cookie**（レスポンス）でCookieを設定し、**Cookie**（リクエスト）で送信する
3. Cookieの属性（**Secure, HttpOnly, SameSite**）はセキュリティに直結する
4. **セッション**はサーバー側で状態を管理し、セッションIDで紐付ける
5. **Basic認証**はBase64エンコード（暗号化ではない）のため、HTTPS必須
6. **JWT**はペイロードに情報を含む自己完結型トークン
7. **APIキー**はヘッダーで送信するのが安全
8. **OAuth 2.0**は第三者サービスに権限を委譲する仕組み
9. **セッションハイジャック**対策にはSecure・HttpOnly・セッションID更新が重要
10. **CSRF対策**にはCSRFトークンとSameSite Cookieが有効
