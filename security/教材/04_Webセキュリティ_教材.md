# 第4章：Webセキュリティ

## この章のゴール

- XSS、CSRF、SQLインジェクション等の主要なWeb攻撃の仕組みを理解する
- 各攻撃に対する具体的な防御手法をコードレベルで実装できる
- CORS（Cross-Origin Resource Sharing）の仕組みと適切な設定を理解する
- CSP（Content Security Policy）によるXSS緩和策を設定できる
- OWASP Top 10 の主要な脆弱性カテゴリを把握し、対策を講じられる

---

## 4.1 Webアプリケーションの脅威全体像

### 4.1.1 攻撃の分類

Webアプリケーションに対する攻撃は、大きく以下のように分類されます。

```
┌──────────────────────────────────────────────────────┐
│          Webアプリケーションへの攻撃分類               │
│                                                      │
│  入力値に起因する攻撃                                 │
│  ├── SQLインジェクション                              │
│  ├── XSS（クロスサイトスクリプティング）               │
│  ├── コマンドインジェクション                         │
│  ├── パストラバーサル                                 │
│  └── XXE（XML外部エンティティ）                       │
│                                                      │
│  セッション/認証に対する攻撃                           │
│  ├── CSRF（クロスサイトリクエストフォージェリ）         │
│  ├── セッションハイジャック                            │
│  └── セッションフィクセーション                        │
│                                                      │
│  設定/構成の不備を狙う攻撃                             │
│  ├── ディレクトリリスティング                          │
│  ├── 不要なHTTPメソッドの悪用                         │
│  └── デフォルト設定の悪用                              │
│                                                      │
│  クライアント側の攻撃                                  │
│  ├── クリックジャッキング                              │
│  ├── オープンリダイレクト                              │
│  └── SSRF（サーバーサイドリクエストフォージェリ）       │
└──────────────────────────────────────────────────────┘
```

---

## 4.2 XSS（クロスサイトスクリプティング）

### 4.2.1 XSSとは

XSS（Cross-Site Scripting）は、攻撃者が悪意のあるスクリプトをWebページに埋め込み、そのページを閲覧した他のユーザーのブラウザ上でスクリプトを実行させる攻撃です。Webアプリケーションで最も頻繁に発見される脆弱性の一つです。

### 4.2.2 XSSの種類

| 種類 | 説明 | 永続性 |
|------|------|--------|
| **反射型XSS（Reflected XSS）** | リクエストパラメータに含まれたスクリプトがそのままレスポンスに反映される | 一時的 |
| **格納型XSS（Stored XSS）** | 悪意のあるスクリプトがDB等に保存され、ページ表示時に実行される | 永続的 |
| **DOM Based XSS** | サーバーを経由せず、クライアント側のJavaScriptの処理で発生する | 一時的 |

### 4.2.3 反射型XSSの攻撃フロー

```
┌──────────────────────────────────────────────────────────┐
│             反射型XSS の攻撃フロー                        │
│                                                          │
│  ① 攻撃者が悪意のあるURLを作成                            │
│     https://example.com/search?q=<script>悪意のコード     │
│                                                          │
│  ② 被害者がリンクをクリック                                │
│     （メール、SNS等で誘導）                                │
│                                                          │
│  ③ サーバーが検索クエリをエスケープせずにHTMLに埋め込む     │
│     <p>検索結果: <script>悪意のコード</script></p>        │
│                                                          │
│  ④ 被害者のブラウザでスクリプトが実行される                │
│     → Cookie窃取、フィッシング、キーロガー等              │
│                                                          │
│  攻撃者 → [悪意のURL] → 被害者 → [リクエスト] → サーバー │
│                          被害者 ← [スクリプト含むHTML] ←   │
│                          被害者 → [Cookie等を攻撃者に送信] │
└──────────────────────────────────────────────────────────┘
```

### 4.2.4 XSSの対策

**脆弱なコード（エスケープなし）**:

```javascript
// NG: ユーザー入力をそのままHTMLに挿入
app.get('/search', (req, res) => {
  const query = req.query.q;
  res.send(`<h1>検索結果: ${query}</h1>`);  // XSS脆弱性！
});
```

**修正後コード（出力エスケープ）**:

```javascript
// OK: HTMLエスケープを行う
const escapeHtml = (str) => {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#x27;');
};

app.get('/search', (req, res) => {
  const query = escapeHtml(req.query.q);
  res.send(`<h1>検索結果: ${query}</h1>`);
});
```

**DOM Based XSSの脆弱なコード**:

```javascript
// NG: innerHTML にユーザー入力を直接挿入
const query = new URLSearchParams(location.search).get('q');
document.getElementById('result').innerHTML = query;  // DOM Based XSS！
```

**修正後コード**:

```javascript
// OK: textContent を使用（HTMLとして解釈されない）
const query = new URLSearchParams(location.search).get('q');
document.getElementById('result').textContent = query;
```

### 4.2.5 XSS対策のまとめ

| 対策 | 説明 | 優先度 |
|------|------|--------|
| **出力エスケープ** | HTMLコンテキストに応じた適切なエスケープ処理 | 必須 |
| **CSP（Content Security Policy）** | インラインスクリプトの実行を制限（後述） | 強く推奨 |
| **HttpOnly クッキー** | JavaScriptからのCookieアクセスを防止 | 必須 |
| **テンプレートエンジンの自動エスケープ** | React、Vue.js等のフレームワークが自動で行う | 推奨 |
| **入力検証** | 許可される文字種・形式をホワイトリストで制限 | 推奨 |
| **DOMPurify等のサニタイザー** | HTMLを許可する場合に安全なタグのみ残す | 状況に応じて |

> **よくある間違い**: 「入力をサニタイズすれば安全」と考えがちですが、入力検証だけでは不十分です。**出力時のエスケープ**が最も重要な対策です。データが使われる文脈（HTML、JavaScript、URL、CSS）に応じた適切なエスケープが必要です。

---

## 4.3 SQLインジェクション

### 4.3.1 SQLインジェクションとは

SQLインジェクションは、ユーザーの入力値がSQL文の一部として解釈されることで、攻撃者が意図しないSQL文を実行させる攻撃です。データベースの情報漏洩、改ざん、削除など、深刻な被害を引き起こします。

### 4.3.2 攻撃の仕組み

```
┌──────────────────────────────────────────────────────────┐
│           SQLインジェクションの例                          │
│                                                          │
│  想定される入力: "taro"                                   │
│  生成されるSQL: SELECT * FROM users WHERE name = 'taro'   │
│                                                          │
│  攻撃者の入力: "' OR '1'='1"                              │
│  生成されるSQL: SELECT * FROM users WHERE name = ''       │
│                OR '1'='1'                                 │
│  → 条件が常にTRUEとなり、全ユーザーの情報が返される       │
│                                                          │
│  さらに危険な入力: "'; DROP TABLE users; --"              │
│  生成されるSQL: SELECT * FROM users WHERE name = '';      │
│                DROP TABLE users; --'                      │
│  → usersテーブルが削除される                              │
└──────────────────────────────────────────────────────────┘
```

### 4.3.3 SQLインジェクションの対策

**脆弱なコード（文字列結合によるSQL構築）**:

```python
# NG: ユーザー入力をSQL文に直接結合
def get_user(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)  # SQLインジェクション脆弱性！
    return cursor.fetchone()
```

**修正後コード（プレースホルダ/パラメータ化クエリ）**:

```python
# OK: パラメータ化クエリを使用
def get_user(username):
    query = "SELECT * FROM users WHERE username = ?"
    cursor.execute(query, (username,))  # パラメータとして安全に渡す
    return cursor.fetchone()
```

**ORMを使用した安全な実装**:

```python
# OK: ORM（SQLAlchemy等）を使用
def get_user(username):
    return User.query.filter_by(username=username).first()
    # ORMが内部でパラメータ化クエリを使用
```

### 4.3.4 SQLインジェクション対策のまとめ

| 対策 | 説明 | 優先度 |
|------|------|--------|
| **プレースホルダ（パラメータ化クエリ）** | SQL文とパラメータを分離して渡す | 必須 |
| **ORM の使用** | SQLを直接書かずにORMのAPIを使用 | 推奨 |
| **入力検証** | 想定される形式をホワイトリストで検証 | 推奨 |
| **最小権限のDBアカウント** | アプリケーションのDBユーザーに最小限の権限のみ付与 | 必須 |
| **エラーメッセージの抑制** | SQLエラーの詳細をユーザーに表示しない | 必須 |
| **WAF（Web Application Firewall）** | 追加の防御層として導入 | 推奨 |

---

## 4.4 CSRF（クロスサイトリクエストフォージェリ）

### 4.4.1 CSRFとは

CSRF（Cross-Site Request Forgery）は、ログイン済みのユーザーに対して、意図しないリクエストを送信させる攻撃です。ユーザーの認証情報（セッションクッキー）が自動的に送信されることを悪用します。

### 4.4.2 CSRFの攻撃フロー

```
┌──────────────────────────────────────────────────────────┐
│              CSRF の攻撃フロー                             │
│                                                          │
│  ① 被害者が正規サイト（bank.example.com）にログイン中     │
│     → セッションクッキーがブラウザに保存されている         │
│                                                          │
│  ② 被害者が攻撃者の罠サイトにアクセス                     │
│                                                          │
│  ③ 罠サイトに埋め込まれたフォームが自動送信               │
│     <form action="https://bank.example.com/transfer"     │
│           method="POST">                                 │
│       <input name="to" value="attacker">                 │
│       <input name="amount" value="1000000">              │
│     </form>                                              │
│     <script>document.forms[0].submit();</script>         │
│                                                          │
│  ④ ブラウザが bank.example.com のクッキーを自動付与       │
│     → サーバーは正規ユーザーからのリクエストと判断         │
│     → 不正な送金が実行される                              │
│                                                          │
│  罠サイト → [POSTリクエスト + 自動付与されたクッキー]      │
│           → bank.example.com → 不正送金実行              │
└──────────────────────────────────────────────────────────┘
```

### 4.4.3 CSRF対策

**対策1: CSRFトークン（Synchronizer Token Pattern）**:

```python
# サーバー側: CSRFトークンの生成と検証
import secrets

@app.before_request
def csrf_protect():
    if request.method == 'POST':
        token = session.get('csrf_token')
        if not token or token != request.form.get('csrf_token'):
            abort(403, 'CSRF検証に失敗しました')

@app.route('/transfer', methods=['GET'])
def transfer_form():
    token = secrets.token_hex(32)
    session['csrf_token'] = token
    return render_template('transfer.html', csrf_token=token)
```

```html
<!-- テンプレート: フォームにCSRFトークンを埋め込む -->
<form method="POST" action="/transfer">
  <input type="hidden" name="csrf_token" value="{{ csrf_token }}">
  <input type="text" name="to" placeholder="振込先">
  <input type="number" name="amount" placeholder="金額">
  <button type="submit">送金</button>
</form>
```

**対策2: SameSite Cookie属性**:

```python
# SameSiteクッキー属性の設定
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # または 'Strict'
app.config['SESSION_COOKIE_SECURE'] = True
```

| SameSite値 | 動作 | CSRF防御 |
|-----------|------|---------|
| `Strict` | クロスサイトリクエストではクッキーを一切送信しない | 強い |
| `Lax` | GETリクエスト（トップレベルナビゲーション）のみクッキーを送信 | 中程度（推奨） |
| `None` | 常にクッキーを送信（Secure属性が必須） | なし |

---

## 4.5 その他の重要なWeb攻撃

### 4.5.1 コマンドインジェクション

**脆弱なコード**:

```python
# NG: ユーザー入力をOSコマンドに直接渡す
import os
def ping_host(host):
    os.system(f"ping -c 4 {host}")  # host に "; rm -rf /" と入力されたら？
```

**修正後コード**:

```python
# OK: subprocess を使い、シェル展開を無効化
import subprocess
def ping_host(host):
    # 入力検証
    if not re.match(r'^[a-zA-Z0-9.\-]+$', host):
        raise ValueError("無効なホスト名です")
    # shell=False でシェルインジェクションを防止
    result = subprocess.run(
        ['ping', '-c', '4', host],
        capture_output=True, text=True, shell=False
    )
    return result.stdout
```

### 4.5.2 パストラバーサル

**脆弱なコード**:

```python
# NG: ユーザー入力をファイルパスにそのまま使用
@app.route('/download')
def download():
    filename = request.args.get('file')
    return send_file(f'/var/www/uploads/{filename}')
    # file=../../etc/passwd で機密ファイルが漏洩！
```

**修正後コード**:

```python
# OK: パスの正規化と検証
import os
@app.route('/download')
def download():
    filename = request.args.get('file')
    # パスを正規化し、ベースディレクトリ内に収まるか検証
    base_dir = os.path.realpath('/var/www/uploads')
    file_path = os.path.realpath(os.path.join(base_dir, filename))

    if not file_path.startswith(base_dir):
        abort(403, 'アクセスが拒否されました')

    if not os.path.isfile(file_path):
        abort(404, 'ファイルが見つかりません')

    return send_file(file_path)
```

### 4.5.3 SSRF（サーバーサイドリクエストフォージェリ）

SSRF は、サーバーに対して内部ネットワークへのリクエストを強制させる攻撃です。

```
┌────────────────────────────────────────────────────────┐
│              SSRF の攻撃フロー                           │
│                                                        │
│  攻撃者 → Webサーバー → 内部サーバー（本来アクセス不可） │
│                                                        │
│  例: URL取得機能を悪用                                  │
│  正常: fetch_url("https://example.com/api")             │
│  攻撃: fetch_url("http://169.254.169.254/metadata")     │
│        → クラウドのメタデータサービスにアクセス           │
│        → IAMクレデンシャルの窃取                        │
│                                                        │
│  攻撃: fetch_url("http://localhost:6379/")              │
│        → 内部のRedisサーバーにアクセス                   │
└────────────────────────────────────────────────────────┘
```

### 4.5.4 クリックジャッキング

クリックジャッキングは、透明なiframeを重ねることで、ユーザーに意図しないクリックをさせる攻撃です。

**対策（HTTPレスポンスヘッダー）**:

```
# X-Frame-Options（レガシー）
X-Frame-Options: DENY

# CSP の frame-ancestors（推奨）
Content-Security-Policy: frame-ancestors 'none';
```

---

## 4.6 CORS（Cross-Origin Resource Sharing）

### 4.6.1 同一オリジンポリシー（SOP）

ブラウザは、セキュリティのために**同一オリジンポリシー（Same-Origin Policy）**を適用します。異なるオリジン間でのリソースアクセスを制限することで、悪意のあるサイトからのデータ窃取を防ぎます。

```
オリジン = スキーム + ホスト + ポート

https://example.com:443/page
 ↑         ↑          ↑
スキーム    ホスト     ポート

同一オリジン: https://example.com/page1 と https://example.com/page2
異なるオリジン:
  - http://example.com  （スキームが異なる）
  - https://api.example.com  （ホストが異なる）
  - https://example.com:8080  （ポートが異なる）
```

### 4.6.2 CORSの仕組み

CORS は、同一オリジンポリシーの制限を安全に緩和するための仕組みです。サーバー側のHTTPレスポンスヘッダーで、アクセスを許可するオリジンを指定します。

```
┌──────────────────────────────────────────────────────────┐
│           CORS プリフライトリクエスト                      │
│                                                          │
│  ブラウザ（https://app.example.com）                      │
│       │                                                  │
│  ① プリフライトリクエスト（OPTIONS）                      │
│       │── OPTIONS /api/data ──────────────→│             │
│       │   Origin: https://app.example.com   │             │
│       │   Access-Control-Request-Method: POST│   APIサーバー│
│       │   Access-Control-Request-Headers:    │   (api.     │
│       │     Content-Type                     │   example.  │
│       │                                      │   com)      │
│  ② プリフライト応答                                      │
│       │←── 200 OK ───────────────────────│             │
│       │   Access-Control-Allow-Origin:       │             │
│       │     https://app.example.com          │             │
│       │   Access-Control-Allow-Methods: POST │             │
│       │   Access-Control-Allow-Headers:      │             │
│       │     Content-Type                     │             │
│       │   Access-Control-Max-Age: 86400      │             │
│       │                                      │             │
│  ③ 本リクエスト（許可された場合のみ）                     │
│       │── POST /api/data ─────────────────→│             │
│       │←── 200 OK + データ ────────────────│             │
└──────────────────────────────────────────────────────────┘
```

### 4.6.3 CORSの設定例

**脆弱な設定（全オリジン許可）**:

```python
# NG: すべてのオリジンを許可（クレデンシャル付きでは動作しない）
@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'  # 危険！
    response.headers['Access-Control-Allow-Credentials'] = 'true'  # *と併用不可
    return response
```

**修正後コード（ホワイトリスト方式）**:

```python
# OK: 許可するオリジンをホワイトリストで管理
ALLOWED_ORIGINS = {
    'https://app.example.com',
    'https://admin.example.com',
}

@app.after_request
def add_cors_headers(response):
    origin = request.headers.get('Origin')
    if origin in ALLOWED_ORIGINS:
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Access-Control-Max-Age'] = '86400'
    return response
```

> **よくある間違い**: `Access-Control-Allow-Origin: *` と `Access-Control-Allow-Credentials: true` は同時に使用できません。クレデンシャル（Cookie等）を含むリクエストでは、具体的なオリジンを指定する必要があります。また、Origin ヘッダーの値をそのまま反射する実装は、実質的に全オリジン許可と同じで危険です。

---

## 4.7 CSP（Content Security Policy）

### 4.7.1 CSPとは

CSP（Content Security Policy）は、XSS攻撃を緩和するためのHTTPレスポンスヘッダーです。ブラウザに対して、どのソースからのコンテンツ（スクリプト、スタイルシート、画像等）の実行・読み込みを許可するかを指示します。

### 4.7.2 CSPの主要ディレクティブ

| ディレクティブ | 制御対象 | 例 |
|-------------|---------|-----|
| `default-src` | 未指定のリソース全般のデフォルト | `'self'` |
| `script-src` | JavaScript | `'self' https://cdn.example.com` |
| `style-src` | CSS | `'self' 'unsafe-inline'` |
| `img-src` | 画像 | `'self' data: https:` |
| `connect-src` | AJAX、WebSocket等 | `'self' https://api.example.com` |
| `font-src` | フォント | `'self' https://fonts.googleapis.com` |
| `frame-src` | iframe | `'none'` |
| `frame-ancestors` | このページをiframeに入れられるか | `'none'` |
| `form-action` | フォームの送信先 | `'self'` |

### 4.7.3 CSPの設定例

```
# 基本的なCSP設定
Content-Security-Policy:
  default-src 'self';
  script-src 'self' 'nonce-abc123';
  style-src 'self' 'unsafe-inline';
  img-src 'self' data: https:;
  connect-src 'self' https://api.example.com;
  font-src 'self' https://fonts.googleapis.com;
  frame-ancestors 'none';
  form-action 'self';
  base-uri 'self';
  upgrade-insecure-requests;
```

```html
<!-- nonce ベースのCSPを使ったインラインスクリプトの許可 -->
<!-- サーバーがリクエストごとにランダムな nonce を生成 -->
<script nonce="abc123">
  // この nonce がCSPヘッダーと一致するので実行される
  console.log('許可されたスクリプト');
</script>

<script>
  // nonce がないので実行がブロックされる（攻撃者が挿入したスクリプト）
  document.cookie; // 実行されない
</script>
```

---

## 4.8 セキュリティ関連のHTTPヘッダー

### 4.8.1 重要なセキュリティヘッダー

| ヘッダー | 用途 | 推奨値 |
|---------|------|--------|
| `Strict-Transport-Security` | HTTPS強制（HSTS） | `max-age=31536000; includeSubDomains` |
| `Content-Security-Policy` | コンテンツの読み込み制御 | 上記参照 |
| `X-Content-Type-Options` | MIMEスニッフィング防止 | `nosniff` |
| `X-Frame-Options` | クリックジャッキング防止 | `DENY` |
| `Referrer-Policy` | Referer情報の制御 | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | ブラウザ機能の制御 | `camera=(), microphone=(), geolocation=()` |
| `Cache-Control` | キャッシュ制御 | 機密ページ: `no-store` |

### 4.8.2 セキュリティヘッダーの設定例（Express.js）

```javascript
const helmet = require('helmet');
const app = express();

// helmet を使用してセキュリティヘッダーを一括設定
app.use(helmet({
  contentSecurityPolicy: {
    directives: {
      defaultSrc: ["'self'"],
      scriptSrc: ["'self'"],
      styleSrc: ["'self'", "'unsafe-inline'"],
      imgSrc: ["'self'", "data:", "https:"],
      connectSrc: ["'self'", "https://api.example.com"],
      frameAncestors: ["'none'"],
    },
  },
  hsts: {
    maxAge: 31536000,
    includeSubDomains: true,
    preload: true,
  },
  referrerPolicy: { policy: 'strict-origin-when-cross-origin' },
}));
```

---

## 4.9 OWASP Top 10

### 4.9.1 OWASP Top 10（2021年版）

OWASP（Open Web Application Security Project）は、Webアプリケーションセキュリティに関する非営利団体です。定期的に発表される「OWASP Top 10」は、最も深刻なWebセキュリティリスクのランキングです。

| 順位 | カテゴリ | 概要 |
|------|---------|------|
| A01 | **アクセス制御の不備** | 認可チェックの欠如、IDOR、権限昇格 |
| A02 | **暗号化の失敗** | 機密データの平文通信/保存、弱い暗号の使用 |
| A03 | **インジェクション** | SQL、XSS、コマンドインジェクション等 |
| A04 | **安全でない設計** | 設計段階でのセキュリティ考慮の不足 |
| A05 | **セキュリティの設定ミス** | デフォルト設定、不要な機能の有効化 |
| A06 | **脆弱で古いコンポーネント** | 既知の脆弱性を持つライブラリの使用 |
| A07 | **識別と認証の失敗** | 弱いパスワード、セッション管理の不備 |
| A08 | **ソフトウェアとデータの整合性の不備** | CI/CDパイプライン、デシリアライゼーション |
| A09 | **セキュリティログと監視の不備** | ログ不足、異常検知の欠如 |
| A10 | **SSRF（サーバーサイドリクエストフォージェリ）** | サーバーに内部リソースへのリクエストを強制 |

### 4.9.2 A01: アクセス制御の不備（IDOR の例）

IDOR（Insecure Direct Object Reference）は、ユーザーが本来アクセスできないリソースに直接アクセスできてしまう脆弱性です。

**脆弱なコード**:

```python
# NG: ユーザーIDの検証なし
@app.route('/api/users/<int:user_id>/profile')
def get_profile(user_id):
    # 任意のユーザーIDを指定してプロファイルを取得できる
    return User.query.get(user_id).to_dict()
```

**修正後コード**:

```python
# OK: 認可チェックを実施
@app.route('/api/users/<int:user_id>/profile')
@login_required
def get_profile(user_id):
    current_user = get_current_user()
    # 自分自身のプロファイルか、管理者であることを確認
    if current_user.id != user_id and not current_user.is_admin:
        abort(403, '他のユーザーのプロファイルにはアクセスできません')
    return User.query.get(user_id).to_dict()
```

> **現場での注意点**: OWASP Top 10 の2021年版では「アクセス制御の不備」が1位になりました。これは、認証（ログイン）は実装されていても、認可（権限チェック）が不十分なアプリケーションが非常に多いことを示しています。すべてのAPIエンドポイントで、リソースへのアクセス権限を確認する仕組みを設けてください。

---

## 4.10 まとめ

### 重要ポイント

1. **XSS対策の要は出力エスケープ**です。入力値検証だけでは不十分であり、CSPも併用してください
2. **SQLインジェクション対策にはパラメータ化クエリ**を必ず使用してください。文字列結合でSQL文を組み立ててはいけません
3. **CSRF対策にはCSRFトークンとSameSite Cookie**を組み合わせてください
4. **CORSは必要最小限のオリジンのみ許可**し、ワイルドカード（`*`）の使用は避けてください
5. **CSPで防御層を追加**し、万が一のXSSの影響を最小限に抑えてください
6. **OWASP Top 10**を定期的に確認し、自アプリケーションの脆弱性をチェックしてください

### 試験対策キーワード

- XSS（反射型、格納型、DOM Based）、エスケープ処理
- SQLインジェクション、パラメータ化クエリ、プレースホルダ
- CSRF、CSRFトークン、SameSite Cookie
- CORS、同一オリジンポリシー、プリフライトリクエスト
- CSP（Content Security Policy）、nonce、ディレクティブ
- SSRF、IDOR、クリックジャッキング
- OWASP Top 10、セキュリティヘッダー

---

**前章**: [第3章：暗号技術](./03_暗号技術_教材.md)
**次章**: [第5章：ネットワークセキュリティ](./05_ネットワークセキュリティ_教材.md)
