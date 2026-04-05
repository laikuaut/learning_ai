# 第1章 演習：HTTP概論

---

## 問題1：HTTPの基本概念（基本）

以下の説明が正しければ「○」、間違っていれば「×」を答え、間違いの場合は正しい内容を述べてください。

1. HTTPではサーバーからクライアントに対してリクエストを送る
2. HTTPはステートレスなプロトコルである
3. HTTP/1.1では1つの接続で1つのリクエストしか送れない
4. URLのフラグメント（`#section`）はサーバーに送信される
5. HTTPSはHTTPにSSL/TLSによる暗号化を加えたものである

<details>
<summary>解答例</summary>

```
1. × — HTTPではクライアント（ブラウザ等）からサーバーに
   リクエストを送り、サーバーがレスポンスを返します。

2. ○ — HTTPはステートレスです。各リクエストは独立しており、
   サーバーは前回のリクエストの状態を保持しません。

3. × — HTTP/1.0では1リクエストごとに接続を切断していましたが、
   HTTP/1.1ではKeep-Aliveにより接続を再利用できます。
   ただし、1接続上でリクエストは順番に処理されます
   （HTTP/2で多重化が実現）。

4. × — フラグメント（# 以降）はブラウザ側で処理され、
   サーバーには送信されません。

5. ○ — HTTPS = HTTP + TLS（Transport Layer Security）で、
   通信内容を暗号化して盗聴・改ざんを防ぎます。
```

</details>

---

## 問題2：URLの解析（基本）

以下のURLの各部分を分解して説明してください。

```
https://api.example.com:8443/v2/users?page=3&sort=name#top
```

<details>
<summary>解答例</summary>

```
スキーム:       https
ホスト名:       api.example.com
ポート番号:     8443
パス:           /v2/users
クエリ文字列:   page=3&sort=name
  ├─ page = 3
  └─ sort = name
フラグメント:   top

補足:
- ポート8443はHTTPSの非標準ポート（標準は443）
- パスの /v2/ はAPIバージョニングを表している
- フラグメント #top はサーバーに送信されない
```

</details>

---

## 問題3：PythonでURLを解析（基本）

Pythonの `urllib.parse` を使って、以下のURLを解析し、各要素を出力するコードを書いてください。

```
https://shop.example.com/products/search?category=books&price_max=3000&lang=ja
```

**期待される出力：**
```
スキーム: https
ホスト: shop.example.com
パス: /products/search
パラメータ:
  category: books
  price_max: 3000
  lang: ja
```

<details>
<summary>解答例</summary>

```python
from urllib.parse import urlparse, parse_qs

url = "https://shop.example.com/products/search?category=books&price_max=3000&lang=ja"
parsed = urlparse(url)

print(f"スキーム: {parsed.scheme}")
print(f"ホスト: {parsed.hostname}")
print(f"パス: {parsed.path}")

params = parse_qs(parsed.query)
print("パラメータ:")
for key, values in params.items():
    print(f"  {key}: {values[0]}")
```

</details>

---

## 問題4：HTTPの歴史（基本）

以下の各機能が導入されたHTTPバージョンを答えてください。

1. Keep-Alive（接続の再利用）
2. 多重化（1接続で複数リクエストを並行処理）
3. ヘッダーの導入（Content-Type等）
4. QUIC（UDPベース）プロトコル
5. Hostヘッダーの必須化

<details>
<summary>解答例</summary>

```
1. Keep-Alive           → HTTP/1.1（1997年）
2. 多重化（Multiplexing）→ HTTP/2（2015年）
3. ヘッダーの導入        → HTTP/1.0（1996年）
4. QUIC（UDPベース）     → HTTP/3（2022年）
5. Hostヘッダー必須化    → HTTP/1.1（1997年）
   ※ 1つのIPアドレスで複数のドメインをホスティングするために必須
```

</details>

---

## 問題5：curlコマンドの使い方（応用）

以下の各操作を行うcurlコマンドを書いてください。

1. `https://httpbin.org/get` にGETリクエストを送り、レスポンスヘッダーも表示する
2. `https://httpbin.org/post` にJSON形式でデータ `{"name": "test"}` をPOSTする
3. `https://httpbin.org/get` のレスポンスヘッダーのみを取得する
4. `https://httpbin.org/get` にカスタムヘッダー `X-Custom-Header: hello` を付けてリクエストする

<details>
<summary>解答例</summary>

```bash
# 1. レスポンスヘッダーも表示
curl -i https://httpbin.org/get

# 2. JSONデータをPOST
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name": "test"}'

# 3. レスポンスヘッダーのみ（HEADリクエスト）
curl -I https://httpbin.org/get

# 4. カスタムヘッダー付き
curl -H "X-Custom-Header: hello" https://httpbin.org/get
```

</details>

---

## 問題6：curl -v の出力読解（応用）

以下の `curl -v` 出力を読んで、質問に答えてください。

```
> POST /api/login HTTP/1.1
> Host: api.example.com
> Content-Type: application/json
> Content-Length: 42
>
< HTTP/1.1 401 Unauthorized
< Content-Type: application/json
< WWW-Authenticate: Bearer
< Content-Length: 38
<
{"error": "Invalid credentials"}
```

1. リクエストのHTTPメソッドとパスは何ですか？
2. リクエストのContent-Typeは何ですか？
3. レスポンスのステータスコードとその意味は？
4. サーバーが推奨する認証方式は何ですか？
5. レスポンスボディの内容から、何が起きたと考えられますか？

<details>
<summary>解答例</summary>

```
1. メソッド: POST、パス: /api/login
   ログインAPIにPOSTリクエストを送信している。

2. Content-Type: application/json
   リクエストボディがJSON形式であることを示している。

3. ステータスコード: 401 Unauthorized
   認証が必要、または認証に失敗したことを意味する。

4. Bearer トークン認証
   WWW-Authenticate: Bearer ヘッダーは、
   Bearer Token（JWTなど）での認証を推奨している。

5. ログイン認証情報（メール/パスワード等）が
   不正であったため認証に失敗した。
   "Invalid credentials" = 「認証情報が無効」
```

</details>

---

## 問題7：HTTP通信の全体像（応用）

ブラウザで `https://www.example.com/index.html` にアクセスしたとき、裏側で何が起こるかを時系列で説明してください。以下のステップを含めてください。

- DNS解決
- TCP接続
- TLSハンドシェイク
- HTTPリクエスト送信
- HTTPレスポンス受信
- HTML解析と追加リソースの取得

<details>
<summary>解答例</summary>

```
1. DNS解決
   ブラウザが www.example.com のIPアドレスを
   DNSサーバーに問い合わせる。
   → 例: 93.184.216.34 が返される

2. TCP接続（3ウェイハンドシェイク）
   ブラウザが 93.184.216.34:443 に対して
   TCP接続を確立する。
   → SYN → SYN-ACK → ACK

3. TLSハンドシェイク
   HTTPS のため、TCP接続の上でTLSハンドシェイクを行い、
   暗号化通信を確立する。
   → サーバー証明書の検証
   → 暗号方式の合意
   → 共通鍵の生成

4. HTTPリクエスト送信
   GET /index.html HTTP/1.1
   Host: www.example.com
   User-Agent: Mozilla/5.0 ...
   Accept: text/html
   → 暗号化されたHTTPリクエストをサーバーに送信

5. HTTPレスポンス受信
   HTTP/1.1 200 OK
   Content-Type: text/html; charset=UTF-8
   Content-Length: 1256
   → HTML文書を受信

6. HTML解析と追加リソースの取得
   ブラウザがHTMLを解析し、追加リソースを発見:
   - <link href="/style.css"> → GET /style.css
   - <script src="/app.js">   → GET /app.js
   - <img src="/logo.png">    → GET /logo.png
   → 各リソースについてHTTPリクエストを送信
     （HTTP/2なら1接続上で多重化）

7. レンダリング
   すべてのリソースが揃ったら、
   ブラウザがページを描画して表示する。
```

</details>

---

## 問題8：総合問題（チャレンジ）

Pythonの標準ライブラリのみを使って、指定したURLにGETリクエストを送り、以下の情報を表示するスクリプトを作成してください。

- ステータスコード
- Content-Type ヘッダー
- レスポンスボディのサイズ（バイト数）
- レスポンスボディの先頭200文字

テスト用URL: `https://httpbin.org/html`

<details>
<summary>解答例</summary>

```python
from urllib.request import urlopen

url = "https://httpbin.org/html"

with urlopen(url) as response:
    status = response.status
    content_type = response.getheader("Content-Type")
    body = response.read()
    size = len(body)
    preview = body.decode("utf-8")[:200]

    print(f"URL: {url}")
    print(f"ステータス: {status}")
    print(f"Content-Type: {content_type}")
    print(f"サイズ: {size} bytes")
    print(f"先頭200文字:\n{preview}...")
```

</details>
