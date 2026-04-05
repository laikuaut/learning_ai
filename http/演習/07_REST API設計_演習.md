# 第7章 演習：REST API設計

---

## 問題1：URL設計の改善（基本）

以下のAPI URLを、RESTful な設計に修正してください。

1. `GET /getUsers`
2. `POST /createProduct`
3. `GET /user/123/getOrders`
4. `POST /deleteUser?id=123`
5. `GET /searchProducts?keyword=python`

<details>
<summary>解答例</summary>

```
1. GET /getUsers         → GET /users
2. POST /createProduct   → POST /products
3. GET /user/123/getOrders → GET /users/123/orders
4. POST /deleteUser?id=123 → DELETE /users/123
5. GET /searchProducts?keyword=python → GET /products?keyword=python

修正ポイント:
- 動詞を使わない（操作はHTTPメソッドで表現）
- リソース名は複数形の名詞
- IDはパスパラメータに含める
- 検索はGET + クエリパラメータ
```

</details>

---

## 問題2：CRUD APIの設計（基本）

オンライン書店の「書籍（Book）」リソースに対して、以下の操作のAPIを設計してください。メソッド、パス、成功時のステータスコードを記述してください。

1. 書籍一覧の取得（カテゴリでフィルタ可能、ページネーション付き）
2. 書籍の詳細取得
3. 書籍の新規登録
4. 書籍情報の更新（タイトルと価格のみ）
5. 書籍の削除
6. 書籍へのレビュー投稿
7. 書籍のレビュー一覧取得

<details>
<summary>解答例</summary>

```
| No | メソッド | パス                               | 成功コード      |
|----|---------|-----------------------------------|----------------|
| 1  | GET     | /books?category=tech&page=1&per_page=20 | 200 OK    |
| 2  | GET     | /books/:id                         | 200 OK         |
| 3  | POST    | /books                             | 201 Created    |
| 4  | PATCH   | /books/:id                         | 200 OK         |
| 5  | DELETE  | /books/:id                         | 204 No Content |
| 6  | POST    | /books/:id/reviews                 | 201 Created    |
| 7  | GET     | /books/:id/reviews?page=1          | 200 OK         |

補足:
- 4はPATCH（部分更新）を使用。PUTだと全項目の指定が必要
- 5のDELETEは204（ボディなし）が一般的
- 6のレビューは書籍の子リソースとしてネスト
```

</details>

---

## 問題3：エラーレスポンスの設計（基本）

以下のエラーケースに対して、ステータスコードとJSON形式のエラーレスポンスを設計してください。

1. 必須パラメータ `name` が未指定
2. メールアドレスが既に登録済み
3. 認証トークンの有効期限切れ
4. 存在しない書籍IDを指定
5. サーバー内部エラー

<details>
<summary>解答例</summary>

```json
// 1. 422 Unprocessable Entity
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力内容に誤りがあります",
    "details": [
      {"field": "name", "message": "名前は必須です"}
    ]
  }
}

// 2. 409 Conflict
{
  "error": {
    "code": "DUPLICATE_EMAIL",
    "message": "このメールアドレスは既に登録されています"
  }
}

// 3. 401 Unauthorized
{
  "error": {
    "code": "TOKEN_EXPIRED",
    "message": "認証トークンの有効期限が切れています。再ログインしてください"
  }
}

// 4. 404 Not Found
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "指定された書籍が見つかりません"
  }
}

// 5. 500 Internal Server Error
{
  "error": {
    "code": "INTERNAL_ERROR",
    "message": "サーバーエラーが発生しました。しばらく後に再度お試しください"
  }
}
```

</details>

---

## 問題4：CORSの理解（応用）

フロントエンド `https://app.example.com` から API `https://api.example.com/users` に POST リクエストを送る場合について答えてください。

1. なぜブラウザがリクエストをブロックするのですか？
2. プリフライトリクエストとは何ですか？
3. APIサーバーはどのようなヘッダーを返す必要がありますか？

<details>
<summary>解答例</summary>

```
1. 同一オリジンポリシー（Same-Origin Policy）により、
   ブラウザは異なるオリジンへのリクエストをデフォルトでブロックします。
   app.example.com と api.example.com はサブドメインが異なるため
   「異なるオリジン」として扱われます。

2. プリフライトリクエストは、実際のリクエストの前にブラウザが
   自動的に送信する OPTIONS リクエストです。
   「このオリジンからのPOSTリクエストを許可しますか？」と
   APIサーバーに事前確認します。

   OPTIONS /users HTTP/1.1
   Origin: https://app.example.com
   Access-Control-Request-Method: POST
   Access-Control-Request-Headers: Content-Type, Authorization

3. APIサーバーが返すべきCORSヘッダー:

   Access-Control-Allow-Origin: https://app.example.com
   Access-Control-Allow-Methods: GET, POST, PUT, DELETE
   Access-Control-Allow-Headers: Content-Type, Authorization
   Access-Control-Max-Age: 86400
   Access-Control-Allow-Credentials: true

   ※ Allow-Origin に * を使うと Authorization ヘッダーとの
     組み合わせが制限されるため、具体的なオリジンを指定する。
```

</details>

---

## 問題5：ページネーションの設計（応用）

商品一覧API `GET /products` にオフセットベースのページネーションを実装する場合のレスポンス形式を設計してください。

**条件：**
- 全商品数: 150件
- 1ページあたり: 20件
- 現在のページ: 3

<details>
<summary>解答例</summary>

```json
{
  "data": [
    {"id": 41, "name": "商品41", "price": 1000},
    {"id": 42, "name": "商品42", "price": 1500},
    ...
    {"id": 60, "name": "商品60", "price": 2000}
  ],
  "pagination": {
    "current_page": 3,
    "per_page": 20,
    "total_count": 150,
    "total_pages": 8,
    "has_next": true,
    "has_prev": true
  },
  "links": {
    "first": "/products?page=1&per_page=20",
    "prev": "/products?page=2&per_page=20",
    "next": "/products?page=4&per_page=20",
    "last": "/products?page=8&per_page=20"
  }
}
```

```
補足:
- total_pages = ceil(150 / 20) = 8
- page 3 → items 41~60（OFFSET 40, LIMIT 20）
- linksセクションで前後ページのURLを提供（HATEOAS準拠）
- per_page の上限を設ける（例: max 100）ことでDoS対策
```

</details>

---

## 問題6：APIバージョニング（応用）

あなたのAPIで破壊的な変更（レスポンス形式の変更）が必要になりました。v1とv2を同時に運用する場合の設計を考えてください。

**変更内容:** ユーザーAPIのレスポンスで、`name` フィールドを `first_name` と `last_name` に分割する

<details>
<summary>解答例</summary>

```
【v1のレスポンス（既存）】
GET /v1/users/123

{
  "id": 123,
  "name": "田中 太郎",
  "email": "tanaka@example.com"
}


【v2のレスポンス（新規）】
GET /v2/users/123

{
  "id": 123,
  "first_name": "太郎",
  "last_name": "田中",
  "email": "tanaka@example.com"
}


【移行戦略】
1. v2をリリースし、v1とv2を並行運用する
2. v1のレスポンスに Deprecation ヘッダーを追加
   Deprecation: true
   Sunset: Sat, 01 Oct 2026 00:00:00 GMT
3. APIドキュメントでv2への移行を案内する
4. v1の利用状況をモニタリングし、
   利用がなくなった時点でv1を廃止する

【URLパス方式での実装】
/v1/users/* → v1のコントローラーにルーティング
/v2/users/* → v2のコントローラーにルーティング
```

</details>

---

## 問題7：総合API設計（チャレンジ）

タスク管理アプリのREST APIを設計してください。以下のリソースと操作を含めてください。

**リソース：** プロジェクト（Project）、タスク（Task）、コメント（Comment）

**操作：**
- プロジェクトのCRUD
- プロジェクト内のタスクのCRUD
- タスクのステータス変更（todo → in_progress → done）
- タスクへのコメント投稿・一覧取得
- 自分に割り当てられたタスクの一覧取得

API一覧表、主要なリクエスト/レスポンス例、エラーケースを含めてください。

<details>
<summary>解答例</summary>

```
【API一覧】

| No | メソッド | パス                              | 概要              | 認証 |
|----|---------|----------------------------------|-------------------|------|
| 1  | GET     | /projects                        | PJ一覧取得         | 必要 |
| 2  | POST    | /projects                        | PJ作成            | 必要 |
| 3  | GET     | /projects/:id                    | PJ詳細取得         | 必要 |
| 4  | PATCH   | /projects/:id                    | PJ更新            | 必要 |
| 5  | DELETE  | /projects/:id                    | PJ削除            | 必要 |
| 6  | GET     | /projects/:id/tasks              | タスク一覧取得     | 必要 |
| 7  | POST    | /projects/:id/tasks              | タスク作成         | 必要 |
| 8  | GET     | /tasks/:id                       | タスク詳細取得     | 必要 |
| 9  | PATCH   | /tasks/:id                       | タスク更新         | 必要 |
| 10 | PATCH   | /tasks/:id/status                | ステータス変更     | 必要 |
| 11 | DELETE  | /tasks/:id                       | タスク削除         | 必要 |
| 12 | GET     | /tasks/:id/comments              | コメント一覧       | 必要 |
| 13 | POST    | /tasks/:id/comments              | コメント投稿       | 必要 |
| 14 | GET     | /users/me/tasks                  | 自分のタスク一覧   | 必要 |


【タスク作成リクエスト例】

POST /projects/1/tasks
Authorization: Bearer <token>
Content-Type: application/json

{
  "title": "ログイン画面の実装",
  "description": "React + NextAuth.js でログイン画面を実装する",
  "assignee_id": 5,
  "priority": "high",
  "due_date": "2026-04-20"
}

→ 201 Created
{
  "data": {
    "id": 42,
    "title": "ログイン画面の実装",
    "status": "todo",
    "priority": "high",
    "assignee": {"id": 5, "name": "田中太郎"},
    "due_date": "2026-04-20",
    "created_at": "2026-04-05T10:00:00+09:00"
  }
}


【ステータス変更リクエスト例】

PATCH /tasks/42/status
Authorization: Bearer <token>
Content-Type: application/json

{"status": "in_progress"}

→ 200 OK
{
  "data": {
    "id": 42,
    "status": "in_progress",
    "updated_at": "2026-04-05T11:00:00+09:00"
  }
}


【エラーケース】

| コード | シナリオ                      | レスポンス                     |
|-------|------------------------------|-------------------------------|
| 401   | トークン未指定                 | UNAUTHORIZED                  |
| 403   | 他人のPJにタスク作成           | FORBIDDEN                     |
| 404   | 存在しないPJ IDを指定          | RESOURCE_NOT_FOUND            |
| 422   | titleが空                     | VALIDATION_ERROR              |
| 422   | statusに無効な値               | INVALID_STATUS                |
| 409   | done → todo に戻そうとした     | INVALID_STATUS_TRANSITION     |
```

</details>
