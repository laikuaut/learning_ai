# 第6章 演習：API設計書

---

## 基本問題

### 問題1：RESTful URL設計

以下のAPI操作に対して、RESTfulなHTTPメソッドとURLを設計してください。

1. すべてのユーザーを取得する
2. ID=5のユーザーの情報を取得する
3. 新しいユーザーを作成する
4. ID=5のユーザー情報を更新する
5. ID=5のユーザーを削除する
6. ID=5のユーザーの注文一覧を取得する
7. ID=5のユーザーのID=10の注文の詳細を取得する
8. 商品をキーワードで検索する

**期待される出力例：**

```
1. GET /users
2. GET /users/5
```

<details>
<summary>ヒント</summary>

- リソース名は複数形の名詞を使用する
- HTTPメソッドで操作を表現する（GET=取得、POST=作成、PUT=更新、DELETE=削除）
- ネストで親子関係を表現する

</details>

<details>
<summary>解答例</summary>

```
1. GET    /users                    ユーザー一覧取得
2. GET    /users/5                  ユーザー詳細取得
3. POST   /users                    ユーザー作成
4. PUT    /users/5                  ユーザー更新
5. DELETE /users/5                  ユーザー削除
6. GET    /users/5/orders           ユーザーの注文一覧取得
7. GET    /users/5/orders/10        ユーザーの注文詳細取得
   または GET /orders/10            （注文IDで直接取得）
8. GET    /products?keyword=Tシャツ  商品キーワード検索

【よくある間違い】
✗ GET    /getUsers         → 動詞を使わない
✗ POST   /users/create     → POSTメソッドで表現する
✗ GET    /user/5           → 複数形にする
✗ POST   /users/5/delete   → DELETEメソッドを使う
✗ GET    /searchProducts   → クエリパラメータで検索する

【補足：7の2パターンの使い分け】
・GET /users/5/orders/10
  → ユーザー5の注文10であることを明示（権限チェックが容易）
・GET /orders/10
  → 注文IDで直接アクセス（URLがシンプル）
  → 多くのAPIではこちらが一般的
```

</details>

---

### 問題2：HTTPステータスコードの選択

以下の各シナリオで、どのHTTPステータスコードを返すべきか答えてください。

1. 商品一覧の取得に成功した
2. 新しい注文の作成に成功した
3. ユーザーの削除に成功した（レスポンスボディなし）
4. リクエストのJSONフォーマットが不正だった
5. 認証トークンが期限切れだった
6. 認証済みだが管理者権限がなく操作が拒否された
7. 存在しないユーザーIDを指定した
8. 在庫不足で注文を受け付けられなかった
9. APIの呼び出し回数が上限を超えた
10. サーバー内部で予期しないエラーが発生した

**期待される出力例：**

```
1. 200 OK
2. 201 Created
```

<details>
<summary>ヒント</summary>

2xx=成功、4xx=クライアントエラー、5xx=サーバーエラーの使い分けに注意してください。特に401と403、400と422の違いを考えましょう。

</details>

<details>
<summary>解答例</summary>

```
1.  200 OK
    → GET成功。レスポンスボディにデータを含む。

2.  201 Created
    → POST成功。新しいリソースが作成された。

3.  204 No Content
    → DELETE成功。レスポンスボディなし。

4.  400 Bad Request
    → リクエストの形式が不正（JSON構文エラー等）。

5.  401 Unauthorized
    → 認証が必要、または認証情報が無効。
    → トークン期限切れもこれに含まれる。

6.  403 Forbidden
    → 認証は済んでいるが、権限が不足している。
    → 401との違い：401は「誰かわからない」、
      403は「誰かはわかるが許可されていない」。

7.  404 Not Found
    → 指定されたリソースが存在しない。

8.  409 Conflict
    → ビジネスロジック上の競合・矛盾。
    → 在庫不足はサーバーの状態との競合。
    → 422 Unprocessable Entity も選択肢。

9.  429 Too Many Requests
    → レートリミット超過。
    → Retry-Afterヘッダーで待機時間を通知する。

10. 500 Internal Server Error
    → サーバー内部の予期しないエラー。
    → ユーザーには詳細を見せず、ログに記録する。
```

</details>

---

### 問題3：エラーレスポンスの設計

以下のエラーケースに対して、統一的なエラーレスポンスのJSON形式を設計してください。

1. ユーザー登録時にメールアドレスが既に使われている
2. ログイン時にパスワードが間違っている
3. 商品のカート追加時に在庫が不足している

**期待される出力例：**

```json
{
  "error": {
    "code": "...",
    "message": "...",
    ...
  }
}
```

<details>
<summary>ヒント</summary>

エラーレスポンスには以下の情報を含めましょう。
- エラーコード（機械判読用）：大文字のスネークケース
- メッセージ（ユーザー向け）：日本語の説明文
- 詳細（オプション）：フィールド別のエラー情報

</details>

<details>
<summary>解答例</summary>

```
【1. メールアドレス重複（409 Conflict）】

{
  "error": {
    "code": "EMAIL_ALREADY_EXISTS",
    "message": "このメールアドレスは既に登録されています",
    "details": [
      {
        "field": "email",
        "message": "このメールアドレスは既に使用されています。
                   別のメールアドレスを入力してください。"
      }
    ]
  }
}


【2. パスワード誤り（401 Unauthorized）】

{
  "error": {
    "code": "INVALID_CREDENTIALS",
    "message": "メールアドレスまたはパスワードが正しくありません"
  }
}

※ セキュリティ上、「メールアドレスが間違い」なのか
  「パスワードが間違い」なのかを区別しない。
  これにより、攻撃者がメールアドレスの存在を
  推測することを防ぐ。


【3. 在庫不足（409 Conflict）】

{
  "error": {
    "code": "OUT_OF_STOCK",
    "message": "在庫が不足しています",
    "details": [
      {
        "field": "quantity",
        "message": "「コットンTシャツ ホワイト」の在庫は
                   残り3個です。数量を3以下にしてください。",
        "meta": {
          "product_id": 1,
          "product_name": "コットンTシャツ ホワイト",
          "requested_quantity": 5,
          "available_stock": 3
        }
      }
    ]
  }
}

※ meta にプログラムで利用可能な構造化データを含めると、
  フロントエンドで在庫数をフォームに反映するなど
  ユーザー体験を向上させられる。
```

</details>

---

## 応用問題

### 問題4：API詳細仕様の作成

タスク管理ツールの「タスク作成API」の詳細仕様書を作成してください。

**要件：**
- 認証必須
- タスクにはタイトル（必須）、説明、担当者、優先度、期限がある
- プロジェクトに所属するタスクを作成する
- 優先度はlow/medium/high/urgentの4段階
- 作成成功時はタスクの詳細情報を返す

以下のテンプレートに従って記述してください。

```
API-ID  :
API名   :
メソッド :
URL     :
認証    :

【リクエスト】
■ ヘッダー
■ パスパラメータ
■ リクエストボディ
■ リクエスト例

【レスポンス】
■ 成功時
■ エラー時
```

<details>
<summary>ヒント</summary>

- URLにプロジェクトIDを含める（/projects/:projectId/tasks）
- リクエストボディにタスクの各項目を定義する
- 成功時は201 Createdを返す
- エラーケースを複数考える

</details>

<details>
<summary>解答例</summary>

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
API-ID  : API-TASK-001
API名   : タスク作成
メソッド : POST
URL     : /projects/:projectId/tasks
認証    : 必要（Bearer Token）
概要    : 指定プロジェクト内に新しいタスクを作成する
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【リクエスト】

■ ヘッダー

| ヘッダー名      | 値                     |
|---------------|------------------------|
| Authorization | Bearer {access_token}  |
| Content-Type  | application/json       |

■ パスパラメータ

| パラメータ   | 型     | 必須 | 説明           |
|------------|--------|-----|---------------|
| projectId  | number | ○   | プロジェクトID  |

■ リクエストボディ

| パラメータ    | 型     | 必須 | デフォルト | 説明                          |
|-------------|--------|-----|----------|------------------------------|
| title       | string | ○   |          | タスク名（1〜200文字）          |
| description | string | -   | null     | タスクの説明（最大5000文字）     |
| assignee_id | number | -   | null     | 担当者のユーザーID              |
| priority    | string | -   | medium   | 優先度(low/medium/high/urgent) |
| due_date    | string | -   | null     | 期限（YYYY-MM-DD形式）         |

■ リクエスト例

POST /projects/1/tasks
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "title": "ログイン画面のデザイン修正",
  "description": "フォームのバリデーションメッセージの色を赤に変更する",
  "assignee_id": 5,
  "priority": "high",
  "due_date": "2026-04-15"
}


【レスポンス】

■ 成功時（201 Created）

{
  "data": {
    "id": 42,
    "title": "ログイン画面のデザイン修正",
    "description": "フォームのバリデーションメッセージの色を赤に変更する",
    "status": "todo",
    "priority": "high",
    "due_date": "2026-04-15",
    "assignee": {
      "id": 5,
      "name": "田中太郎"
    },
    "created_by": {
      "id": 3,
      "name": "鈴木花子"
    },
    "project": {
      "id": 1,
      "name": "ECサイトリニューアル"
    },
    "created_at": "2026-03-20T10:30:00+09:00",
    "updated_at": "2026-03-20T10:30:00+09:00"
  }
}

■ エラー時

| ステータス | エラーコード          | 説明                         |
|----------|---------------------|------------------------------|
| 400      | VALIDATION_ERROR    | バリデーションエラー             |
|          |                     | ・titleが空                    |
|          |                     | ・titleが200文字超過            |
|          |                     | ・priorityが不正な値            |
|          |                     | ・due_dateが過去の日付          |
| 401      | UNAUTHORIZED        | 認証トークンが無効              |
| 403      | NOT_PROJECT_MEMBER  | プロジェクトのメンバーでない      |
| 404      | PROJECT_NOT_FOUND   | プロジェクトが存在しない         |
| 404      | USER_NOT_FOUND      | 指定した担当者が存在しない       |
| 500      | INTERNAL_ERROR      | サーバー内部エラー              |

■ エラーレスポンス例（400 バリデーションエラー）

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力内容に誤りがあります",
    "details": [
      {
        "field": "title",
        "message": "タスク名は必須です"
      },
      {
        "field": "due_date",
        "message": "期限は今日以降の日付を指定してください"
      }
    ]
  }
}
```

</details>

---

## チャレンジ問題

### 問題5：API設計書の作成（総合演習）

ブログシステムの記事に関するAPIを設計してください。以下の7つのAPIについて、API一覧と主要API（2つ以上）の詳細仕様を作成してください。

**API：**
1. 記事一覧取得（公開記事、ページネーション、カテゴリ・タグによるフィルタ）
2. 記事詳細取得（スラグ指定）
3. 記事作成（認証必須、下書き/公開）
4. 記事更新（認証必須、自分の記事のみ）
5. 記事削除（認証必須、自分の記事のみ）
6. 記事へのコメント投稿（認証必須）
7. 記事のコメント一覧取得

<details>
<summary>ヒント</summary>

- 記事の取得はスラグ（URLフレンドリーな文字列）で行う
- 一覧取得にはページネーション、フィルタ、ソートを含める
- 記事作成時に下書き(draft)か公開(published)を選べる
- 認可チェック：自分の記事のみ編集・削除可能

</details>

<details>
<summary>解答例</summary>

```
【API一覧】

| No | メソッド | エンドポイント                  | 概要             | 認証 |
|----|---------|-------------------------------|-----------------|------|
| 1  | GET     | /articles                     | 記事一覧取得      | 不要 |
| 2  | GET     | /articles/:slug               | 記事詳細取得      | 不要 |
| 3  | POST    | /articles                     | 記事作成          | 必要 |
| 4  | PUT     | /articles/:slug               | 記事更新          | 必要 |
| 5  | DELETE  | /articles/:slug               | 記事削除          | 必要 |
| 6  | POST    | /articles/:slug/comments      | コメント投稿      | 必要 |
| 7  | GET     | /articles/:slug/comments      | コメント一覧取得   | 不要 |


【API-001 記事一覧取得 詳細仕様】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
メソッド : GET
URL     : /articles
認証    : 不要
概要    : 公開済み記事の一覧を取得する

■ クエリパラメータ

| パラメータ  | 型     | 必須 | デフォルト | 説明                     |
|-----------|--------|-----|----------|--------------------------|
| category  | string | -   |          | カテゴリスラグでフィルタ    |
| tag       | string | -   |          | タグ名でフィルタ           |
| keyword   | string | -   |          | タイトル・本文のキーワード検索|
| sort      | string | -   | newest   | newest/oldest/popular     |
| page      | number | -   | 1        | ページ番号                |
| per_page  | number | -   | 10       | 1ページ件数（最大50）      |

■ リクエスト例
GET /articles?category=tech&sort=newest&page=1&per_page=10

■ 成功レスポンス（200 OK）

{
  "data": [
    {
      "id": 42,
      "title": "Next.js 15の新機能まとめ",
      "slug": "nextjs-15-new-features",
      "excerpt": "Next.js 15がリリースされました。主な新機能を...",
      "author": {
        "id": 3,
        "name": "田中太郎",
        "avatar_url": "/avatars/3.jpg"
      },
      "category": {
        "id": 1,
        "name": "技術",
        "slug": "tech"
      },
      "tags": ["Next.js", "React", "フロントエンド"],
      "published_at": "2026-03-20T10:00:00+09:00",
      "reading_time_min": 8,
      "comment_count": 5
    }
  ],
  "pagination": {
    "current_page": 1,
    "per_page": 10,
    "total_count": 42,
    "total_pages": 5,
    "has_next": true,
    "has_prev": false
  }
}

■ エラー時
| ステータス | コード            | 説明              |
|----------|------------------|-------------------|
| 400      | INVALID_PARAMETER| パラメータ不正      |


【API-003 記事作成 詳細仕様】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
メソッド : POST
URL     : /articles
認証    : 必要（Bearer Token）
概要    : 新しい記事を作成する（下書きまたは公開）

■ リクエストボディ

| パラメータ    | 型       | 必須 | 説明                         |
|-------------|---------|-----|------------------------------|
| title       | string  | ○   | タイトル（1〜200文字）         |
| slug        | string  | ○   | URLスラグ（英数字・ハイフン）   |
| body        | string  | ○   | 本文（Markdown形式）           |
| excerpt     | string  | -   | 要約（最大500文字）            |
| category_id | number  | ○   | カテゴリID                    |
| tag_names   | array   | -   | タグ名の配列                  |
| status      | string  | -   | draft（デフォルト）/ published|
| published_at| string  | -   | 公開日時（予約投稿、ISO 8601） |

■ リクエスト例

POST /articles
Authorization: Bearer eyJhbGci...
Content-Type: application/json

{
  "title": "Next.js 15の新機能まとめ",
  "slug": "nextjs-15-new-features",
  "body": "# はじめに\n\nNext.js 15がリリースされました...",
  "excerpt": "Next.js 15の主な新機能を解説します",
  "category_id": 1,
  "tag_names": ["Next.js", "React", "フロントエンド"],
  "status": "published"
}

■ 成功レスポンス（201 Created）

{
  "data": {
    "id": 43,
    "title": "Next.js 15の新機能まとめ",
    "slug": "nextjs-15-new-features",
    "body": "# はじめに\n\nNext.js 15がリリースされました...",
    "excerpt": "Next.js 15の主な新機能を解説します",
    "author": {
      "id": 3,
      "name": "田中太郎"
    },
    "category": {
      "id": 1,
      "name": "技術"
    },
    "tags": ["Next.js", "React", "フロントエンド"],
    "status": "published",
    "published_at": "2026-03-20T10:00:00+09:00",
    "created_at": "2026-03-20T10:00:00+09:00",
    "updated_at": "2026-03-20T10:00:00+09:00"
  }
}

■ エラー時
| ステータス | コード              | 説明                   |
|----------|--------------------|-----------------------|
| 400      | VALIDATION_ERROR   | バリデーションエラー     |
| 401      | UNAUTHORIZED       | 認証エラー              |
| 409      | SLUG_ALREADY_EXISTS| スラグが既に使われている |
| 404      | CATEGORY_NOT_FOUND | カテゴリが存在しない    |
```

</details>
