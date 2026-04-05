# 第2章 演習：HTTPメソッドとステータスコード

---

## 問題1：HTTPメソッドの選択（基本）

以下の各操作に適切なHTTPメソッドを選んでください。

1. ユーザー一覧を取得する
2. 新しい商品を登録する
3. ユーザーのメールアドレスだけを変更する
4. 注文をキャンセル（削除）する
5. ユーザー情報を全項目指定して上書きする
6. サーバーが対応しているHTTPメソッドを確認する

<details>
<summary>解答例</summary>

```
1. GET     ─ リソースの取得。サーバーの状態を変更しない。
2. POST    ─ 新しいリソースの作成。
3. PATCH   ─ リソースの部分更新。メールアドレスだけ変更。
4. DELETE  ─ リソースの削除。
5. PUT     ─ リソースの全体更新（全項目で置換）。
6. OPTIONS ─ サーバーがサポートするメソッドを確認。
             CORSのプリフライトリクエストでも使用される。
```

</details>

---

## 問題2：べき等性の判定（基本）

以下の各操作はべき等ですか？理由とともに「べき等」「べき等でない」を答えてください。

1. `GET /users/1` でユーザー情報を取得する
2. `POST /orders` で注文を作成する
3. `PUT /users/1` でユーザー情報を上書きする
4. `DELETE /users/1` でユーザーを削除する
5. `PATCH /counter` でカウンターを+1する

<details>
<summary>解答例</summary>

```
1. べき等 ○
   理由：何度取得しても同じ結果が返り、サーバーの状態は変わらない。

2. べき等でない ✗
   理由：2回送信すると2つの注文が作成される。
   同じリクエストで異なる結果（別の注文）が生まれる。

3. べき等 ○
   理由：同じデータで何度上書きしても、結果は同じ状態になる。

4. べき等 ○
   理由：1回目の削除で削除され、2回目以降は「既に存在しない」。
   サーバーの最終状態は同じ（そのユーザーが存在しない）。

5. べき等でない ✗
   理由：1回呼ぶとカウンター+1、2回呼ぶと+2になる。
   呼ぶ回数によって結果が変わる。
   ※ PATCH自体はべき等になりうるが、
     この場合の「+1する」という操作は非べき等。
```

</details>

---

## 問題3：ステータスコードの選択（基本）

以下の各シナリオで返すべきステータスコードを答えてください。

1. ユーザー一覧の取得に成功した
2. 新しい注文の作成に成功した
3. ユーザーの削除に成功した（レスポンスボディなし）
4. リクエストのJSONフォーマットが不正だった
5. ログインしていない状態で会員ページにアクセスした
6. 一般ユーザーが管理者用APIにアクセスした
7. 存在しないIDのユーザーを取得しようとした
8. サイトのURLが `https://new.example.com` に永久に変更された
9. サーバーのデータベースが一時的にダウンしている
10. APIの呼び出し回数が上限を超えた

<details>
<summary>解答例</summary>

```
1.  200 OK                  ── 取得成功
2.  201 Created             ── リソース作成成功
3.  204 No Content          ── 成功だがボディなし
4.  400 Bad Request         ── リクエスト形式不正
5.  401 Unauthorized        ── 認証が必要（未ログイン）
6.  403 Forbidden           ── 認証済みだが権限不足
7.  404 Not Found           ── リソースが存在しない
8.  301 Moved Permanently   ── 恒久的なURL変更
9.  503 Service Unavailable ── サーバー一時利用不可
10. 429 Too Many Requests   ── レートリミット超過
```

</details>

---

## 問題4：PUT vs PATCH の違い（基本）

現在のユーザーデータが以下の場合、PUT と PATCH でそれぞれどうなるか答えてください。

**現在のデータ:**
```json
{
  "id": 1,
  "name": "田中太郎",
  "email": "tanaka@example.com",
  "age": 30,
  "role": "admin"
}
```

**送信するデータ:**
```json
{"name": "田中次郎", "email": "jiro@example.com"}
```

<details>
<summary>解答例</summary>

```
【PUTの場合（全体置換）】
{
  "id": 1,
  "name": "田中次郎",
  "email": "jiro@example.com"
}
→ age と role が消える。送信されなかったフィールドは削除される。
  （サーバー実装によっては age=null, role=null になる場合も）

【PATCHの場合（部分更新）】
{
  "id": 1,
  "name": "田中次郎",
  "email": "jiro@example.com",
  "age": 30,
  "role": "admin"
}
→ name と email だけが更新され、age と role はそのまま残る。
```

</details>

---

## 問題5：REST APIの設計（応用）

ブログシステムの記事（Article）に関するREST APIを設計してください。以下の操作に対して、メソッド、パス、成功時のステータスコードを定義してください。

1. 記事の一覧を取得する（ページネーション付き）
2. 特定の記事を取得する（IDで指定）
3. 新しい記事を作成する
4. 記事のタイトルだけを変更する
5. 記事を削除する
6. 記事にコメントを投稿する
7. 記事のコメント一覧を取得する

<details>
<summary>解答例</summary>

```
| No | メソッド | パス                           | 成功コード  | 説明                |
|----|---------|--------------------------------|-----------|---------------------|
| 1  | GET     | /articles?page=1&per_page=20   | 200 OK    | 一覧取得（ページ指定） |
| 2  | GET     | /articles/:id                  | 200 OK    | 詳細取得             |
| 3  | POST    | /articles                      | 201 Created| 新規作成            |
| 4  | PATCH   | /articles/:id                  | 200 OK    | タイトルのみ更新      |
| 5  | DELETE  | /articles/:id                  | 204 No Content| 削除            |
| 6  | POST    | /articles/:id/comments         | 201 Created| コメント投稿        |
| 7  | GET     | /articles/:id/comments         | 200 OK    | コメント一覧取得     |

エラー時のステータスコード:
・記事が存在しない → 404 Not Found
・認証なしで記事作成 → 401 Unauthorized
・他人の記事を削除 → 403 Forbidden
・バリデーションエラー → 422 Unprocessable Entity
```

</details>

---

## 問題6：ステータスコードの読解（応用）

以下のHTTPレスポンスを読んで、何が起きたかを説明してください。

**レスポンスA:**
```
HTTP/1.1 301 Moved Permanently
Location: https://www.example.com/new-page
```

**レスポンスB:**
```
HTTP/1.1 304 Not Modified
ETag: "abc123"
Cache-Control: max-age=3600
```

**レスポンスC:**
```
HTTP/1.1 429 Too Many Requests
Retry-After: 60
Content-Type: application/json

{"error": "Rate limit exceeded. Try again in 60 seconds."}
```

<details>
<summary>解答例</summary>

```
レスポンスA: 301 Moved Permanently
  リクエストしたページが永久に移動した。
  ブラウザは Location ヘッダーに示された
  https://www.example.com/new-page に自動でリダイレクトする。
  ブックマークや検索エンジンも新しいURLに更新される。

レスポンスB: 304 Not Modified
  クライアントがキャッシュしているリソースが最新であることを示す。
  サーバーはボディを返さず、クライアントはローカルキャッシュを使用する。
  ETag "abc123" はリソースのバージョン識別子。
  Cache-Control: max-age=3600 はキャッシュの有効期限（3600秒=1時間）。
  → 通信量の削減とレスポンス高速化に貢献。

レスポンスC: 429 Too Many Requests
  クライアントがAPIのレートリミット（呼び出し回数上限）を超過した。
  Retry-After: 60 により、60秒後に再試行すべきことが示されている。
  レスポンスボディにもエラーメッセージが含まれている。
```

</details>

---

## 問題7：curlでHTTPメソッドを実行（応用）

以下の各操作をcurlコマンドで実行してください。テスト先は `https://httpbin.org` を使用。

1. GETリクエストでクエリパラメータ `name=test&page=2` を送信
2. POSTリクエストでJSON `{"title": "Hello", "body": "World"}` を送信
3. PUTリクエストでJSON `{"name": "Updated"}` を送信
4. DELETEリクエストを送信
5. HEADリクエストでレスポンスヘッダーだけ取得

<details>
<summary>解答例</summary>

```bash
# 1. GET + クエリパラメータ
curl "https://httpbin.org/get?name=test&page=2"

# 2. POST + JSON
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"title": "Hello", "body": "World"}'

# 3. PUT + JSON
curl -X PUT https://httpbin.org/put \
  -H "Content-Type: application/json" \
  -d '{"name": "Updated"}'

# 4. DELETE
curl -X DELETE https://httpbin.org/delete

# 5. HEAD（ヘッダーのみ）
curl -I https://httpbin.org/get
```

</details>

---

## 問題8：エラーハンドリングの設計（チャレンジ）

ECサイトの「注文作成 API」（`POST /orders`）で発生しうるエラーケースをすべて洗い出し、それぞれに適切なステータスコードとエラーレスポンスを設計してください。

**正常時：**
```
POST /orders
Content-Type: application/json
Authorization: Bearer <token>

{"product_id": 123, "quantity": 2, "address_id": 456}
```

<details>
<summary>ヒント</summary>

認証、バリデーション、在庫、アドレス、サーバーエラーの各観点で考えてみましょう。

</details>

<details>
<summary>解答例</summary>

```
| ステータス | エラーコード           | 発生条件                       |
|----------|----------------------|-------------------------------|
| 400      | INVALID_JSON         | JSONのフォーマットが不正         |
| 401      | UNAUTHORIZED         | 認証トークンがない・無効         |
| 403      | ACCOUNT_SUSPENDED    | アカウントが停止されている        |
| 404      | PRODUCT_NOT_FOUND    | 指定した商品IDが存在しない       |
| 404      | ADDRESS_NOT_FOUND    | 指定した配送先IDが存在しない      |
| 409      | OUT_OF_STOCK         | 在庫が不足している              |
| 422      | VALIDATION_ERROR     | quantity が0以下、必須項目欠落等  |
| 429      | RATE_LIMIT_EXCEEDED  | APIの呼び出し上限を超過          |
| 500      | INTERNAL_ERROR       | サーバー内部エラー              |
| 503      | SERVICE_UNAVAILABLE  | 決済サービスが一時的に利用不可    |

エラーレスポンスの統一形式:
{
  "error": {
    "code": "OUT_OF_STOCK",
    "message": "在庫が不足しています",
    "details": [{
      "field": "quantity",
      "message": "商品ID:123の在庫は残り1個です"
    }]
  }
}

成功レスポンス:
HTTP/1.1 201 Created
{
  "data": {
    "id": 789,
    "order_number": "ORD-20260405-001",
    "status": "confirmed",
    "total": 5960
  }
}
```

</details>
