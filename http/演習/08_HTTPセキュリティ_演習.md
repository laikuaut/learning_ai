# 第8章 演習：HTTPセキュリティ

---

## 問題1：脆弱性の識別（基本）

以下の各コード/設定には脆弱性があります。脆弱性の種類と対策を答えてください。

**コードA（Python）:**
```python
username = request.form["username"]
query = f"SELECT * FROM users WHERE username = '{username}'"
cursor.execute(query)
```

**コードB（HTML）:**
```html
<p>検索結果: {{ user_input }}</p>
<!-- user_input がエスケープされていない -->
```

**コードC（Cookie）:**
```
Set-Cookie: session=abc123
```

<details>
<summary>解答例</summary>

```
コードA: SQLインジェクション
  問題: ユーザー入力を文字列連結でSQL文に埋め込んでいる。
  攻撃例: username に "' OR '1'='1" と入力すると認証をバイパス。
  対策:
    cursor.execute(
        "SELECT * FROM users WHERE username = %s",
        (username,)
    )

コードB: XSS（クロスサイトスクリプティング）
  問題: ユーザー入力をHTMLエスケープせずに出力している。
  攻撃例: user_input に "<script>alert('XSS')</script>" を注入。
  対策:
    - テンプレートエンジンの自動エスケープを有効にする
    - Jinja2: {{ user_input | e }}
    - Content-Security-Policy ヘッダーを設定する

コードC: Cookieのセキュリティ属性不足
  問題: Secure, HttpOnly, SameSite属性がない。
  リスク:
    - Secure なし → HTTP通信でCookieが盗聴される
    - HttpOnly なし → XSSでJavaScriptからCookieを窃取される
    - SameSite なし → CSRFに脆弱
  対策:
    Set-Cookie: session=abc123; Secure; HttpOnly; SameSite=Lax; Path=/
```

</details>

---

## 問題2：XSSの種類と対策（基本）

XSSの3つの種類（反射型、格納型、DOM型）について、それぞれの仕組みと対策を説明してください。

<details>
<summary>解答例</summary>

```
1. 反射型XSS（Reflected XSS）
   仕組み: 攻撃者が仕込んだスクリプトがURLのパラメータに含まれ、
          サーバーがそのままHTMLに反映して返す。
   例: https://example.com/search?q=<script>alert(1)</script>
   対策: サーバー側で出力時にエスケープする

2. 格納型XSS（Stored XSS）
   仕組み: 攻撃者がスクリプトをDB等に保存させ、
          他のユーザーがそのページを閲覧した時に実行される。
   例: 掲示板の投稿にスクリプトを埋め込む
   対策: 入力時のサニタイズ＋出力時のエスケープ
         最も危険（被害が広範囲に及ぶ）

3. DOM型XSS（DOM-Based XSS）
   仕組み: サーバーを経由せず、クライアント側のJavaScriptが
          URLフラグメント等の値を安全でない方法でDOMに挿入する。
   例: document.innerHTML = location.hash.substring(1)
   対策: innerHTMLの代わりにtextContentを使用する
         DOMPurify等のサニタイズライブラリを使用する
```

</details>

---

## 問題3：CSRFの攻撃シナリオ（基本）

以下のシナリオで、CSRF攻撃がどのように成立するか説明し、3つの対策を述べてください。

**シナリオ:** オンラインバンキングの送金API
```
POST /transfer
Cookie: session=xyz789
Content-Type: application/x-www-form-urlencoded

to=12345&amount=100000
```

<details>
<summary>解答例</summary>

```
【攻撃の流れ】

1. 被害者が bank.example.com にログイン済み
   → ブラウザにセッションCookie（session=xyz789）が保存

2. 攻撃者が罠サイト evil.example.com に以下のHTMLを設置:
   <form action="https://bank.example.com/transfer" method="POST">
     <input type="hidden" name="to" value="attacker_account">
     <input type="hidden" name="amount" value="100000">
   </form>
   <script>document.forms[0].submit();</script>

3. 被害者が罠サイトにアクセスすると、
   ブラウザが自動的にフォームを送信する
   → セッションCookieが自動で付与される
   → bank.example.com は正規のリクエストと区別できない
   → 送金が実行されてしまう

【3つの対策】

1. CSRFトークン
   サーバーがフォームに一意のトークンを埋め込み、
   リクエスト時に検証する。攻撃者はトークンの値を
   予測できないため、リクエストを偽造できない。

2. SameSite Cookie属性
   Set-Cookie: session=xyz789; SameSite=Lax
   異なるサイトからのPOSTリクエストにCookieを送らない。

3. Origin / Referer ヘッダーの検証
   リクエストの Origin や Referer が自サイトのドメインか
   サーバー側で検証する。
```

</details>

---

## 問題4：セキュリティヘッダーの設定（応用）

以下の攻撃を防ぐために設定すべきHTTPレスポンスヘッダーを答えてください。

1. ブラウザにMIMEタイプを推測させない
2. 他サイトのiframeに埋め込まれることを防ぐ
3. HTTPからHTTPSへの自動アップグレードを強制する
4. 自サイト以外からのスクリプト読み込みを禁止する
5. リファラー情報の漏洩を最小限にする

<details>
<summary>解答例</summary>

```
1. X-Content-Type-Options: nosniff
   ブラウザがContent-Typeを無視してファイル内容から
   MIMEタイプを推測することを禁止。

2. X-Frame-Options: DENY
   または X-Frame-Options: SAMEORIGIN
   他サイトのiframe内でのページ表示を禁止。
   クリックジャッキング対策。

3. Strict-Transport-Security: max-age=63072000; includeSubDomains
   ブラウザに「常にHTTPSでアクセスせよ」と指示。
   max-age は有効期間（秒）。

4. Content-Security-Policy: script-src 'self'
   スクリプトの読み込みを自サイトのオリジンのみに制限。
   インラインスクリプトやeval()も禁止される。

5. Referrer-Policy: strict-origin-when-cross-origin
   同一オリジン: フルURLを送信
   クロスオリジン: オリジンのみ送信（パスを含めない）
   HTTPS→HTTP: リファラーを送信しない
```

</details>

---

## 問題5：安全なパスワード管理（応用）

以下のパスワード保存方法を危険度順に並べ、それぞれの問題点を説明してください。その上で、正しい保存方法を述べてください。

1. `password` カラムに平文で保存
2. `MD5(password)` でハッシュ化して保存
3. `SHA256(password)` でハッシュ化して保存
4. `SHA256(password + "固定salt")` でハッシュ化して保存
5. `bcrypt(password)` でハッシュ化して保存

<details>
<summary>解答例</summary>

```
【危険度順（高→低）】

1. 平文で保存 → 最も危険
   問題: DBが漏洩したら全パスワードが即座に判明する。

2. MD5(password) → 非常に危険
   問題: MD5は高速すぎるため、ブルートフォースやレインボー
   テーブル攻撃で容易に元のパスワードを特定できる。
   また、MD5自体に脆弱性（衝突耐性の欠如）がある。

3. SHA256(password) → 危険
   問題: SHA256も高速なため、GPUによる大量のハッシュ計算が可能。
   また、ソルトがないためレインボーテーブル攻撃に脆弱。
   同じパスワードのユーザーが同じハッシュ値になる。

4. SHA256(password + "固定salt") → やや危険
   問題: 固定ソルトでは、攻撃者がソルトを入手した場合に
   全ユーザー分のレインボーテーブルを1回作れば済む。
   ユーザーごとに異なるソルトが必要。

5. bcrypt(password) → 推奨 ✅
   利点:
   - ユーザーごとにランダムなソルトを自動生成
   - 意図的に計算を遅くする（ストレッチング）
   - cost パラメータで計算回数を調整可能
   - GPU並列化に対する耐性がある

【正しい保存方法】
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
# $2b$12$LJ3m7... のような文字列が生成される
# ソルトはハッシュ値に含まれるため別途保存不要
```

</details>

---

## 問題6：セキュリティ監査（応用）

以下のHTTPレスポンスヘッダーを監査し、セキュリティ上の問題点をすべて指摘してください。

```
HTTP/1.1 200 OK
Server: Apache/2.4.41 (Ubuntu)
X-Powered-By: PHP/8.1.2
Content-Type: text/html
Set-Cookie: session=abc123
Access-Control-Allow-Origin: *
```

<details>
<summary>解答例</summary>

```
問題点:

1. Server: Apache/2.4.41 (Ubuntu)
   → バージョン情報が露出。攻撃者に既知の脆弱性を
     特定する手がかりを与える。
   対策: ServerTokens Prod（バージョン非表示）

2. X-Powered-By: PHP/8.1.2
   → 使用言語とバージョンが露出。
   対策: php.ini で expose_php = Off に設定

3. Set-Cookie: session=abc123
   → Secure, HttpOnly, SameSite属性がない。
   対策: Set-Cookie: session=abc123; Secure; HttpOnly; SameSite=Lax

4. Access-Control-Allow-Origin: *
   → 全オリジンからのアクセスを許可。
     認証付きAPIでは特に危険。
   対策: 具体的なオリジンを指定する

5. セキュリティヘッダーが不足:
   - Strict-Transport-Security がない
   - X-Content-Type-Options がない
   - X-Frame-Options がない
   - Content-Security-Policy がない
   - Referrer-Policy がない
```

</details>

---

## 問題7：総合セキュリティ設計（チャレンジ）

ECサイトのログイン機能を設計する際に、以下のセキュリティ要件を満たす設計を行ってください。

1. ログインAPIの設計（メソッド、パス、リクエスト/レスポンス）
2. パスワードの安全な保存方法
3. セッション管理の方法（Cookie設定）
4. ブルートフォース攻撃への対策
5. レスポンスに含めるセキュリティヘッダー

<details>
<summary>解答例</summary>

```
【1. ログインAPI】

POST /api/auth/login
Content-Type: application/json

リクエスト:
{
  "email": "user@example.com",
  "password": "MyPass123!"
}

成功レスポンス (200 OK):
Set-Cookie: session=<token>; Secure; HttpOnly; SameSite=Lax; Path=/; Max-Age=86400
{
  "data": {
    "user": {"id": 1, "name": "田中太郎", "email": "user@example.com"},
    "expires_at": "2026-04-06T10:00:00Z"
  }
}

失敗レスポンス (401 Unauthorized):
{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "メールアドレスまたはパスワードが正しくありません"
  }
}
※ メールが存在しない/パスワードが違うを区別しない（情報漏洩防止）


【2. パスワードの保存】

import bcrypt

# 保存時
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12))
# DB に hashed を保存

# 検証時
if bcrypt.checkpw(input_password.encode(), stored_hash):
    # 認証成功
else:
    # 認証失敗


【3. セッション管理】

Set-Cookie:
  session=<ランダムトークン>;
  Secure;        → HTTPSのみ送信
  HttpOnly;      → JavaScriptからアクセス不可
  SameSite=Lax;  → CSRF対策
  Path=/;        → 全パスで有効
  Max-Age=86400; → 24時間で期限切れ

セッションデータはサーバー側（Redis等）に保存。
Cookieにはセッション ID のみ含める。


【4. ブルートフォース対策】

- レートリミット: 1IPあたり 1分間に5回まで
  429 Too Many Requests + Retry-After ヘッダー
- アカウントロック: 10回連続失敗で30分間ロック
- CAPTCHA: 3回失敗後にCAPTCHAを表示
- ログイン試行のログ記録と監視


【5. セキュリティヘッダー】

Strict-Transport-Security: max-age=63072000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Content-Security-Policy: default-src 'self'
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: camera=(), microphone=()
```

</details>
