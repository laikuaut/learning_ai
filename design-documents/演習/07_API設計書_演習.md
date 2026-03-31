# 第7章 演習：API設計書・インターフェース設計

---

## 基本問題

### 問題1：RESTful URLの設計

以下の操作に対して、適切なHTTPメソッドとURLを設計してください。

1. ユーザーの一覧を取得する
2. 特定のユーザーの情報を取得する
3. 新しいユーザーを作成する
4. ユーザーの名前を更新する
5. ユーザーを削除する
6. 特定のユーザーの注文一覧を取得する
7. 特定のユーザーの特定の注文を取得する
8. 商品を検索する（キーワード指定）

**期待される出力例：**

```
1. GET /api/v1/users
```

<details>
<summary>ヒント</summary>

RESTful設計のルール：名詞を使う、複数形、HTTPメソッドで操作を表現、ネストは2階層まで。

</details>

<details>
<summary>解答例</summary>

```
1. GET    /api/v1/users              - ユーザー一覧取得
2. GET    /api/v1/users/:id          - 特定ユーザー取得
3. POST   /api/v1/users              - ユーザー作成
4. PATCH  /api/v1/users/:id          - ユーザー部分更新（名前のみ）
5. DELETE /api/v1/users/:id          - ユーザー削除
6. GET    /api/v1/users/:id/orders   - ユーザーの注文一覧
7. GET    /api/v1/orders/:id         - 特定の注文取得
   （※ネスト3階層を避けるため /users/:id/orders/:id ではなく
     注文単体で取得する設計にする）
8. GET    /api/v1/products?keyword=検索語  - 商品検索（クエリパラメータ）
```

</details>

---

### 問題2：HTTPステータスコードの選択

以下のシナリオに適切なHTTPステータスコードを選んでください。

1. 商品一覧を正常に取得した
2. 新しい注文を作成した
3. ユーザーを削除した（レスポンスボディなし）
4. リクエストのJSON形式が不正
5. 認証トークンが未送信
6. 認証済みだが管理者権限が必要なAPIにアクセスした
7. 指定IDの商品が存在しない
8. 同じメールアドレスでユーザー登録しようとした
9. サーバー内部でエラーが発生した
10. 在庫数が0の商品を注文しようとした

<details>
<summary>解答例</summary>

```
1.  200 OK                    - 取得成功
2.  201 Created               - リソース作成成功
3.  204 No Content            - 削除成功（レスポンスボディなし）
4.  400 Bad Request           - リクエスト形式が不正
5.  401 Unauthorized          - 未認証（トークンなし）
6.  403 Forbidden             - 認証済みだが権限不足
7.  404 Not Found             - リソースが存在しない
8.  409 Conflict              - リソースの競合（重複）
9.  500 Internal Server Error - サーバー内部エラー
10. 422 Unprocessable Entity  - ビジネスルール違反（在庫不足）
    （※409 Conflictも許容される。プロジェクトで統一すればOK）
```

</details>

---

### 問題3：API仕様の読み取り

以下のAPI仕様を読み取り、質問に答えてください。

```
## GET /api/v1/products

### クエリパラメータ
| パラメータ | 型 | 必須 | デフォルト | 説明 |
|-----------|-----|------|-----------|------|
| keyword | string | × | - | 検索キーワード |
| category_id | integer | × | - | カテゴリID |
| sort | string | × | newest | newest, price_asc, price_desc |
| page | integer | × | 1 | ページ番号 |
| per_page | integer | × | 20 | 1ページの件数（最大50） |

### レスポンス（200 OK）
{
  "data": [
    {
      "id": 1,
      "name": "商品A",
      "price": 1500,
      "category": { "id": 3, "name": "家電" },
      "is_in_stock": true
    }
  ],
  "pagination": {
    "current_page": 1,
    "per_page": 20,
    "total_count": 150,
    "total_pages": 8
  }
}
```

**質問：**
1. カテゴリID=5の商品を価格の安い順で取得するURLは？
2. 1ページに50件ずつ、2ページ目を取得するURLは？
3. 全150件を取得するには最低何回リクエストが必要ですか（per_page=50の場合）？
4. レスポンスのcategoryはどのような形式ですか？

<details>
<summary>解答例</summary>

```
1. GET /api/v1/products?category_id=5&sort=price_asc

2. GET /api/v1/products?per_page=50&page=2

3. 3回
   → total_count=150、per_page=50の場合、
     150 ÷ 50 = 3ページ（total_pages=3）
     page=1, page=2, page=3 の3回リクエスト

4. ネストされたオブジェクト
   → { "id": 3, "name": "家電" } のようにidとnameを持つ
     オブジェクトとしてレスポンスに含まれている。
     カテゴリIDだけでなく名前も一緒に返すことで、
     フロントエンドが追加のAPIリクエストをせずに表示できる。
```

</details>

---

## 応用問題

### 問題4：API詳細仕様の作成

以下の機能のAPI詳細仕様を作成してください。

**機能：** ユーザーのプロフィール更新

**要件：**
- ログイン済みユーザーが自分のプロフィールを更新する
- 更新可能な項目：氏名、表示名、自己紹介文
- メールアドレスの変更は別のAPIで行う
- 氏名は必須、表示名と自己紹介文は任意

API詳細仕様（エンドポイント、リクエスト、レスポンス、エラーケース）を作成してください。

<details>
<summary>ヒント</summary>

プロフィールの「部分更新」なので、PATCHメソッドが適切です。全フィールドを送る必要がなく、変更したいフィールドだけ送れる設計にしましょう。

</details>

<details>
<summary>解答例</summary>

```markdown
## PATCH /api/v1/users/me

### 概要
ログイン済みユーザーが自分のプロフィール情報を部分更新する。

### 認証
必要（Bearer Token）

### リクエスト

#### ヘッダー
| ヘッダー | 値 |
|---------|-----|
| Authorization | Bearer {token} |
| Content-Type | application/json |

#### リクエストボディ
送信するフィールドのみを含める（部分更新）。

| フィールド | 型 | 必須 | 制約 | 説明 |
|-----------|-----|------|------|------|
| name | string | △ | 1〜100文字 | 氏名（送信時は空文字不可） |
| display_name | string | × | 0〜50文字 | 表示名（空文字で削除可） |
| bio | string | × | 0〜500文字 | 自己紹介文 |

#### リクエスト例
```json
{
  "name": "山田 太郎",
  "display_name": "yamada",
  "bio": "Webエンジニア3年目です。"
}
```

### レスポンス

#### 成功時（200 OK）
```json
{
  "data": {
    "id": 123,
    "name": "山田 太郎",
    "display_name": "yamada",
    "email": "yamada@example.com",
    "bio": "Webエンジニア3年目です。",
    "avatar_url": "/images/avatars/123.jpg",
    "created_at": "2025-10-01T00:00:00Z",
    "updated_at": "2026-04-01T10:30:00Z"
  }
}
```

### エラーケース

| ステータス | エラーコード | 条件 | メッセージ |
|-----------|------------|------|-----------|
| 400 | VALIDATION_ERROR | nameが空文字 | 氏名を入力してください |
| 400 | VALIDATION_ERROR | nameが100文字超 | 氏名は100文字以内で入力してください |
| 400 | VALIDATION_ERROR | display_nameが50文字超 | 表示名は50文字以内で入力してください |
| 400 | VALIDATION_ERROR | bioが500文字超 | 自己紹介は500文字以内で入力してください |
| 401 | UNAUTHORIZED | 認証トークンが無効 | 認証が必要です |
| 400 | EMPTY_REQUEST | リクエストボディが空 | 更新するフィールドを指定してください |
```

</details>

---

## チャレンジ問題

### 問題5：API設計の総合問題

以下のシステムのAPI一覧と主要API2つの詳細仕様を設計してください。

**システム：** ブックマーク管理サービス

**機能：**
- ユーザー認証（登録・ログイン）
- ブックマークの追加（URL、タイトル、メモ）
- ブックマークの一覧表示（タグ・キーワードでフィルタリング）
- ブックマークの編集・削除
- タグの管理（作成・一覧・削除）
- ブックマークにタグを付与

以下を作成してください：
1. API一覧表（8エンドポイント以上）
2. 任意のAPI2つの詳細仕様（リクエスト・レスポンス・エラー含む）

<details>
<summary>解答例</summary>

```markdown
## 1. API一覧

| No | メソッド | エンドポイント | 認証 | 説明 |
|----|---------|--------------|------|------|
| 1 | POST | /api/v1/auth/register | 不要 | ユーザー登録 |
| 2 | POST | /api/v1/auth/login | 不要 | ログイン |
| 3 | GET | /api/v1/bookmarks | 必要 | ブックマーク一覧取得 |
| 4 | POST | /api/v1/bookmarks | 必要 | ブックマーク追加 |
| 5 | GET | /api/v1/bookmarks/:id | 必要 | ブックマーク詳細取得 |
| 6 | PATCH | /api/v1/bookmarks/:id | 必要 | ブックマーク編集 |
| 7 | DELETE | /api/v1/bookmarks/:id | 必要 | ブックマーク削除 |
| 8 | GET | /api/v1/tags | 必要 | タグ一覧取得 |
| 9 | POST | /api/v1/tags | 必要 | タグ作成 |
| 10 | DELETE | /api/v1/tags/:id | 必要 | タグ削除 |

## 2-A. POST /api/v1/bookmarks（ブックマーク追加）

### 認証
必要（Bearer Token）

### リクエストボディ
| フィールド | 型 | 必須 | 制約 | 説明 |
|-----------|-----|------|------|------|
| url | string | ◯ | URL形式、2048文字以内 | ブックマークするURL |
| title | string | × | 200文字以内 | タイトル（未指定時はURLから自動取得） |
| memo | string | × | 1000文字以内 | メモ |
| tag_ids | integer[] | × | - | 付与するタグのIDリスト |

### リクエスト例
```json
{
  "url": "https://example.com/article",
  "title": "参考記事",
  "memo": "設計パターンについての良記事",
  "tag_ids": [1, 3]
}
```

### レスポンス（201 Created）
```json
{
  "data": {
    "id": 42,
    "url": "https://example.com/article",
    "title": "参考記事",
    "memo": "設計パターンについての良記事",
    "tags": [
      { "id": 1, "name": "技術" },
      { "id": 3, "name": "設計" }
    ],
    "created_at": "2026-04-01T10:00:00Z"
  }
}
```

### エラーケース
| ステータス | エラーコード | 条件 |
|-----------|------------|------|
| 400 | INVALID_URL | URL形式が不正 |
| 401 | UNAUTHORIZED | 認証トークンが無効 |
| 409 | DUPLICATE_URL | 同じURLが既に登録されている |

## 2-B. GET /api/v1/bookmarks（ブックマーク一覧取得）

### 認証
必要（Bearer Token）

### クエリパラメータ
| パラメータ | 型 | 必須 | デフォルト | 説明 |
|-----------|-----|------|-----------|------|
| keyword | string | × | - | タイトル・メモの部分一致検索 |
| tag_id | integer | × | - | タグIDで絞り込み |
| sort | string | × | newest | newest, oldest, title_asc |
| page | integer | × | 1 | ページ番号 |
| per_page | integer | × | 20 | 1ページの件数（最大50） |

### リクエスト例
GET /api/v1/bookmarks?tag_id=1&sort=newest&page=1

### レスポンス（200 OK）
```json
{
  "data": [
    {
      "id": 42,
      "url": "https://example.com/article",
      "title": "参考記事",
      "memo": "設計パターンについての良記事",
      "tags": [
        { "id": 1, "name": "技術" }
      ],
      "created_at": "2026-04-01T10:00:00Z"
    }
  ],
  "pagination": {
    "current_page": 1,
    "per_page": 20,
    "total_count": 35,
    "total_pages": 2
  }
}
```

### エラーケース
| ステータス | エラーコード | 条件 |
|-----------|------------|------|
| 401 | UNAUTHORIZED | 認証トークンが無効 |
| 400 | INVALID_PARAMETER | sort値が不正 |
```

</details>
