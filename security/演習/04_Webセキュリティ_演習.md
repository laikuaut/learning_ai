# 第4章：Webセキュリティ 演習問題

## 基本問題

### 問題4-1：XSSの種類
XSS（クロスサイトスクリプティング）の3つの種類を挙げ、それぞれの特徴を説明してください。

<details>
<summary>解答</summary>

| 種類 | 特徴 | 永続性 |
|------|------|--------|
| **反射型XSS（Reflected）** | リクエストパラメータに含まれたスクリプトが、サーバのレスポンスにそのまま反映されて実行される | 一時的 |
| **格納型XSS（Stored）** | 悪意のあるスクリプトがデータベース等に保存され、ページ表示時に他のユーザのブラウザで実行される | 永続的（最も危険） |
| **DOM Based XSS** | サーバを経由せず、クライアント側のJavaScriptの処理において、ユーザ入力がDOMに安全でない方法で挿入されて実行される | 一時的 |

</details>

### 問題4-2：XSS対策
XSSの主要な対策を4つ挙げ、それぞれの役割を説明してください。

<details>
<summary>解答</summary>

1. **出力エスケープ**：HTMLに出力する際に特殊文字（<, >, ", ', &）をHTMLエンティティに変換する。最も重要な対策

2. **Content Security Policy（CSP）**：HTTPレスポンスヘッダでスクリプトの実行元を制限する。インラインスクリプトの実行を防止

3. **HttpOnly Cookie**：CookieにHttpOnly属性を設定し、JavaScriptからのCookieアクセスを禁止。XSSによるCookie窃取を防止

4. **入力検証**：ユーザ入力を許可された形式（ホワイトリスト）で検証する。ただし、これだけでは不十分で、出力エスケープと併用が必須

</details>

### 問題4-3：SQLインジェクション
以下のPythonコードの脆弱性を指摘し、修正してください。

```python
def search_user(username):
    query = f"SELECT * FROM users WHERE name = '{username}'"
    cursor.execute(query)
    return cursor.fetchall()
```

<details>
<summary>解答</summary>

**脆弱性：** ユーザ入力（username）をSQL文に直接結合しているため、SQLインジェクションの脆弱性があります。例えば `username = "' OR '1'='1"` と入力すると、全ユーザの情報が漏洩します。

**修正後のコード：**
```python
def search_user(username):
    # パラメータ化クエリを使用（プレースホルダ）
    query = "SELECT * FROM users WHERE name = ?"
    cursor.execute(query, (username,))
    return cursor.fetchall()
```

パラメータ化クエリを使用することで、ユーザ入力はSQLの構文としてではなくデータ値として扱われるため、SQLインジェクションを防止できます。

</details>

### 問題4-4：CSRFの仕組み
CSRF（クロスサイトリクエストフォージェリ）攻撃の仕組みを説明し、対策を2つ挙げてください。

<details>
<summary>解答</summary>

**CSRFの仕組み：**
1. 被害者が正規サイト（例：銀行サイト）にログイン中
2. 攻撃者の罠サイトにアクセスすると、罠サイトに埋め込まれたフォームが正規サイトに自動送信される
3. ブラウザが正規サイトのCookieを自動的に付与するため、サーバは正規ユーザからのリクエストと判断してしまう
4. 被害者の意図しない操作（送金、パスワード変更等）が実行される

**対策：**

1. **CSRFトークン**：フォームにサーバが生成したランダムなトークンを埋め込み、送信時にサーバ側で検証する。攻撃者はトークンを知ることができないため、偽のリクエストは拒否される

2. **SameSite Cookie属性**：CookieのSameSite属性をLaxまたはStrictに設定し、クロスサイトリクエストでのCookie送信を制限する

</details>

---

## 応用問題

### 問題4-5：CORS
以下の問いに答えてください。

(1) 同一オリジンポリシー（SOP）とは何ですか。
(2) CORSは何のための仕組みですか。
(3) `Access-Control-Allow-Origin: *` の設定が危険な理由を述べてください。

<details>
<summary>解答</summary>

**(1)** 同一オリジンポリシー（Same-Origin Policy）は、ブラウザのセキュリティ機能で、異なるオリジン（スキーム + ホスト + ポートの組み合わせ）間でのリソースアクセスを制限する仕組みです。悪意のあるサイトが他のサイトのデータを読み取ることを防ぎます。

**(2)** CORS（Cross-Origin Resource Sharing）は、同一オリジンポリシーの制限を安全に緩和するための仕組みです。サーバ側のHTTPレスポンスヘッダで、どのオリジンからのアクセスを許可するかを指定します。

**(3)** `Access-Control-Allow-Origin: *` は全てのオリジンからのアクセスを許可するため、悪意のあるサイトからのリクエストも許可されてしまいます。特に、クレデンシャル（Cookie等）を含むリクエストでは `*` と `Access-Control-Allow-Credentials: true` を同時に使用できません。許可するオリジンをホワイトリストで管理するべきです。

</details>

### 問題4-6：OWASP Top 10
OWASP Top 10（2021年版）のA01「アクセス制御の不備」について、具体的な脆弱性の例を2つ挙げ、それぞれの対策を述べてください。

<details>
<summary>解答</summary>

**例1：IDOR（Insecure Direct Object Reference）**
- 脆弱性：`/api/users/123/profile` のURLのIDを変更するだけで他のユーザの情報にアクセスできる
- 対策：全てのAPIエンドポイントでリソースへのアクセス権限を検証する。リクエストしたユーザが当該リソースにアクセスする権限を持っているかチェックする

**例2：権限昇格**
- 脆弱性：一般ユーザが管理者用APIエンドポイント（`/api/admin/users`）に直接アクセスできてしまう
- 対策：サーバ側で全てのリクエストに対してロールベースの認可チェックを実施する。クライアント側の制御（ボタンの非表示等）だけに頼らない

</details>

### 問題4-7：セキュリティヘッダ
以下のHTTPセキュリティヘッダの用途を説明してください。

1. Strict-Transport-Security
2. X-Content-Type-Options
3. X-Frame-Options
4. Content-Security-Policy
5. Referrer-Policy

<details>
<summary>解答</summary>

1. **Strict-Transport-Security（HSTS）**：ブラウザにHTTPSでの通信を強制する。一度HTTPSでアクセスすると、指定期間中はHTTPへのアクセスも自動的にHTTPSにリダイレクトされる

2. **X-Content-Type-Options**：値を`nosniff`に設定すると、ブラウザのMIMEスニッフィング（Content-Typeを無視してコンテンツの種類を推測する動作）を防止する

3. **X-Frame-Options**：このページをiframe内に表示することを制限する。`DENY`で完全禁止、`SAMEORIGIN`で同一オリジンのみ許可。クリックジャッキング攻撃の対策

4. **Content-Security-Policy（CSP）**：ページが読み込める外部リソース（スクリプト、スタイル、画像等）の出所を制限する。XSS攻撃の緩和に有効

5. **Referrer-Policy**：リクエスト時にRefererヘッダに含める情報を制御する。`strict-origin-when-cross-origin`で、クロスオリジン時にはオリジンのみ送信

</details>

---

## チャレンジ問題

### 問題4-8：脆弱性の発見と修正
以下のNode.js（Express）のコードには複数のセキュリティ上の問題があります。全て指摘し、修正方針を述べてください。

```javascript
app.get('/search', (req, res) => {
  const query = req.query.q;
  const sql = `SELECT * FROM products WHERE name LIKE '%${query}%'`;
  db.query(sql, (err, results) => {
    res.send(`<h1>検索結果: ${query}</h1><p>${results.length}件</p>`);
  });
});
```

<details>
<summary>解答</summary>

**脆弱性1：SQLインジェクション**
- 問題：ユーザ入力（query）をSQL文に直接結合している
- 修正：パラメータ化クエリを使用する
```javascript
const sql = "SELECT * FROM products WHERE name LIKE ?";
db.query(sql, [`%${query}%`], (err, results) => { ... });
```

**脆弱性2：反射型XSS**
- 問題：ユーザ入力（query）をHTMLエスケープせずにレスポンスに埋め込んでいる
- 修正：出力時にHTMLエスケープを行う
```javascript
const escapeHtml = (str) => str
  .replace(/&/g, '&amp;')
  .replace(/</g, '&lt;')
  .replace(/>/g, '&gt;')
  .replace(/"/g, '&quot;')
  .replace(/'/g, '&#x27;');

res.send(`<h1>検索結果: ${escapeHtml(query)}</h1>`);
```

**脆弱性3：エラーハンドリングの不備**
- 問題：データベースエラー（err）をチェックしていない。エラー内容がユーザに漏洩する可能性がある
- 修正：エラー時にはユーザに一般的なメッセージを返し、詳細はログに記録する

**追加の改善点：**
- Content-Security-Policyヘッダでインラインスクリプトを制限する
- 入力値の長さや文字種を検証する

</details>
