# 第7章：API設計書・インターフェース設計

## この章のゴール

- API設計書の目的と構成を理解する
- RESTful APIの設計原則を習得する
- エンドポイント一覧の作成方法を学ぶ
- リクエスト・レスポンス仕様の定義方法を把握する
- OpenAPI（Swagger）仕様の基本を理解する

---

## 7.1 API設計書とは

### 目的

API設計書は、**システム間またはフロントエンドとバックエンド間の通信インターフェースを定義するドキュメント**です。

### API設計書の位置づけ

```
画面設計書                    API設計書
「商品検索画面がある」  →  「GET /api/products?keyword=...」
「注文確定ボタンがある」 →  「POST /api/orders」

データベース設計書             API設計書
「usersテーブルがある」  →  「GET /api/users/:id でデータを返す」
```

フロントエンド開発者とバックエンド開発者が並行して作業するために、API設計書を先に合意しておくことが重要です。

### API設計書の構成

```markdown
1. API概要
   1.1 ベースURL
   1.2 認証方式
   1.3 共通仕様（ヘッダー、エラー形式等）
2. エンドポイント一覧
3. 各エンドポイントの詳細仕様
4. データモデル定義
5. エラーコード一覧
```

---

## 7.2 RESTful API設計の原則

### リソース指向の設計

RESTful APIでは、URLでリソース（データ）を表現し、HTTPメソッドで操作を表現します。

| HTTPメソッド | 操作 | 例 | 説明 |
|-------------|------|-----|------|
| **GET** | 取得（Read） | GET /api/products | 商品一覧の取得 |
| **POST** | 作成（Create） | POST /api/products | 新規商品の登録 |
| **PUT** | 全体更新（Update） | PUT /api/products/1 | 商品情報の全体置換 |
| **PATCH** | 部分更新（Update） | PATCH /api/products/1 | 商品情報の部分更新 |
| **DELETE** | 削除（Delete） | DELETE /api/products/1 | 商品の削除 |

### URL設計のルール

**良い設計:**
```
GET    /api/users              ユーザー一覧
GET    /api/users/123          ユーザー詳細
POST   /api/users              ユーザー作成
PATCH  /api/users/123          ユーザー更新
DELETE /api/users/123          ユーザー削除

GET    /api/users/123/orders   ユーザーの注文一覧（ネスト）
```

**悪い設計:**
```
GET    /api/getUsers           ← 動詞を含めない
GET    /api/user               ← 複数形にする
POST   /api/users/create       ← メソッドで操作を表現する
GET    /api/Users              ← 小文字を使う
GET    /api/users/123/orders/456/items/789  ← ネストは2階層まで
```

### ステータスコードの使い分け

| ステータスコード | 意味 | 使用場面 |
|----------------|------|---------|
| **200 OK** | 成功 | GET、PATCH、DELETEの成功 |
| **201 Created** | 作成成功 | POSTで新規リソース作成時 |
| **204 No Content** | 成功（レスポンスボディなし） | DELETEの成功時 |
| **400 Bad Request** | リクエストが不正 | バリデーションエラー |
| **401 Unauthorized** | 未認証 | 認証が必要なAPIに未認証でアクセス |
| **403 Forbidden** | 権限なし | 認証済みだがリソースへのアクセス権がない |
| **404 Not Found** | リソースが存在しない | 指定IDのリソースが見つからない |
| **409 Conflict** | 競合 | 既に存在するリソースを作成しようとした |
| **422 Unprocessable Entity** | 処理不能 | ビジネスルール違反 |
| **500 Internal Server Error** | サーバーエラー | 予期しないエラー |

---

## 7.3 API共通仕様

### ベースURLと共通ヘッダー

```markdown
## API共通仕様

### ベースURL
- 開発環境: https://dev-api.example.com/api/v1
- ステージング: https://stg-api.example.com/api/v1
- 本番環境: https://api.example.com/api/v1

### 共通リクエストヘッダー
| ヘッダー | 必須 | 値 | 説明 |
|---------|------|-----|------|
| Content-Type | ◯ | application/json | リクエストボディの形式 |
| Authorization | △ | Bearer {token} | 認証トークン（認証必要なAPIのみ） |
| Accept-Language | × | ja | 言語（デフォルト: ja） |

### 共通レスポンスヘッダー
| ヘッダー | 値 | 説明 |
|---------|-----|------|
| Content-Type | application/json | レスポンスボディの形式 |
| X-Request-Id | UUID | リクエストの追跡用ID |
```

### 共通エラーレスポンス形式

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力内容に誤りがあります",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "正しいメールアドレスの形式で入力してください"
      }
    ]
  }
}
```

### ページネーション

```markdown
### ページネーション仕様

一覧取得APIはページネーションに対応する。

#### リクエストパラメータ
| パラメータ | 型 | デフォルト | 説明 |
|-----------|-----|---------|------|
| page | integer | 1 | ページ番号 |
| per_page | integer | 20 | 1ページあたりの件数（最大100） |

#### レスポンス
```

```json
{
  "data": [...],
  "pagination": {
    "current_page": 1,
    "per_page": 20,
    "total_count": 150,
    "total_pages": 8
  }
}
```

---

## 7.4 エンドポイント一覧

### ECサイトのAPI一覧

| No | メソッド | エンドポイント | 認証 | 説明 |
|----|---------|--------------|------|------|
| 1 | POST | /api/v1/auth/register | 不要 | ユーザー登録 |
| 2 | POST | /api/v1/auth/login | 不要 | ログイン |
| 3 | POST | /api/v1/auth/refresh | 必要 | トークンリフレッシュ |
| 4 | GET | /api/v1/users/me | 必要 | ログインユーザー情報取得 |
| 5 | PATCH | /api/v1/users/me | 必要 | ログインユーザー情報更新 |
| 10 | GET | /api/v1/products | 不要 | 商品一覧取得 |
| 11 | GET | /api/v1/products/:id | 不要 | 商品詳細取得 |
| 12 | GET | /api/v1/categories | 不要 | カテゴリ一覧取得 |
| 20 | GET | /api/v1/cart | 必要 | カート内容取得 |
| 21 | POST | /api/v1/cart/items | 必要 | カートに商品追加 |
| 22 | PATCH | /api/v1/cart/items/:id | 必要 | カート内商品の数量変更 |
| 23 | DELETE | /api/v1/cart/items/:id | 必要 | カートから商品削除 |
| 30 | POST | /api/v1/orders | 必要 | 注文作成 |
| 31 | GET | /api/v1/orders | 必要 | 注文一覧取得 |
| 32 | GET | /api/v1/orders/:id | 必要 | 注文詳細取得 |

---

## 7.5 エンドポイント詳細仕様

### API詳細仕様の書き方

各エンドポイントについて、以下を定義します。

```markdown
## POST /api/v1/orders

### 概要
カート内の商品で注文を作成する。

### 認証
必要（Bearer Token）

### リクエスト

#### ヘッダー
| ヘッダー | 値 |
|---------|-----|
| Authorization | Bearer {token} |
| Content-Type | application/json |

#### リクエストボディ
```

```json
{
  "address_id": 1,
  "payment_method": "credit_card",
  "payment_token": "tok_xxxxxxxxxxxx",
  "note": "置き配希望"
}
```

```markdown
#### パラメータ説明
| フィールド | 型 | 必須 | 説明 |
|-----------|-----|------|------|
| address_id | integer | ◯ | 配送先住所ID |
| payment_method | string | ◯ | 支払方法（credit_card / bank_transfer） |
| payment_token | string | △ | 決済トークン（credit_cardの場合必須） |
| note | string | × | 配送メモ（最大200文字） |

### レスポンス

#### 成功（201 Created）
```

```json
{
  "data": {
    "id": 12345,
    "status": "confirmed",
    "items": [
      {
        "product_id": 1,
        "product_name": "ワイヤレスイヤホン",
        "quantity": 1,
        "unit_price": 12800
      }
    ],
    "total_amount": 12800,
    "shipping_fee": 500,
    "grand_total": 13300,
    "ordered_at": "2026-04-01T10:30:00Z"
  }
}
```

```markdown
#### エラー

| ステータス | コード | 説明 |
|-----------|--------|------|
| 400 | INVALID_REQUEST | リクエスト形式が不正 |
| 401 | UNAUTHORIZED | 認証トークンが無効 |
| 409 | INSUFFICIENT_STOCK | 在庫不足 |
| 422 | EMPTY_CART | カートが空 |
| 422 | INVALID_ADDRESS | 配送先住所が無効 |
| 502 | PAYMENT_FAILED | 決済処理が失敗 |
```

---

## 7.6 OpenAPI（Swagger）仕様

### OpenAPIとは

OpenAPI（旧Swagger）は、**REST APIの仕様を標準的なフォーマット（YAML/JSON）で記述する仕様**です。ドキュメント生成、コード生成、テスト自動化に活用できます。

### OpenAPI仕様の例

```yaml
openapi: 3.0.3
info:
  title: ECサイト API
  version: 1.0.0
  description: ECサイトのバックエンドAPI

servers:
  - url: https://api.example.com/api/v1
    description: 本番環境
  - url: https://dev-api.example.com/api/v1
    description: 開発環境

paths:
  /products:
    get:
      summary: 商品一覧取得
      tags:
        - Products
      parameters:
        - name: keyword
          in: query
          schema:
            type: string
          description: 検索キーワード
        - name: category_id
          in: query
          schema:
            type: integer
          description: カテゴリID
        - name: page
          in: query
          schema:
            type: integer
            default: 1
          description: ページ番号
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/Product'
                  pagination:
                    $ref: '#/components/schemas/Pagination'

  /orders:
    post:
      summary: 注文作成
      tags:
        - Orders
      security:
        - BearerAuth: []
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateOrderRequest'
      responses:
        '201':
          description: 注文作成成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    $ref: '#/components/schemas/Order'
        '409':
          description: 在庫不足
        '422':
          description: バリデーションエラー

components:
  securitySchemes:
    BearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT

  schemas:
    Product:
      type: object
      properties:
        id:
          type: integer
        name:
          type: string
        price:
          type: integer
        description:
          type: string
        image_url:
          type: string

    Pagination:
      type: object
      properties:
        current_page:
          type: integer
        per_page:
          type: integer
        total_count:
          type: integer
        total_pages:
          type: integer

    CreateOrderRequest:
      type: object
      required:
        - address_id
        - payment_method
      properties:
        address_id:
          type: integer
        payment_method:
          type: string
          enum: [credit_card, bank_transfer]
        payment_token:
          type: string
        note:
          type: string
          maxLength: 200
```

### OpenAPIの活用方法

| 活用 | ツール | 説明 |
|------|--------|------|
| **ドキュメント生成** | Swagger UI, Redoc | APIドキュメントを自動生成 |
| **モック生成** | Prism, Mockoon | APIのモックサーバーを自動生成 |
| **コード生成** | OpenAPI Generator | クライアント/サーバーのコードを自動生成 |
| **テスト** | Postman, Dredd | API仕様との整合性を自動テスト |

> **実務でのポイント**: OpenAPI仕様を「設計書」として使い、Swagger UIで表示すればそのままAPIドキュメントになります。設計書とドキュメントを二重管理する必要がなくなります。

---

## 7.7 API設計のベストプラクティス

### バージョニング

```
# URLにバージョンを含める（推奨）
GET /api/v1/products
GET /api/v2/products

# ヘッダーでバージョン指定
Accept: application/vnd.example.v1+json
```

### フィルタリング・ソート・検索

```
# フィルタリング
GET /api/v1/products?category_id=1&min_price=1000

# ソート
GET /api/v1/products?sort=price&order=asc

# 検索
GET /api/v1/products?keyword=イヤホン

# 組み合わせ
GET /api/v1/products?category_id=1&sort=price&order=asc&page=2
```

### レート制限

```markdown
## レート制限

| エンドポイント | 制限 | 説明 |
|--------------|------|------|
| 認証系 | 10回/分 | ブルートフォース防止 |
| 一般API | 100回/分 | 一般的な利用制限 |
| 検索API | 30回/分 | 負荷の高い処理 |

レート制限を超えた場合、429 Too Many Requests を返す。
レスポンスヘッダーで残回数を通知する。

| ヘッダー | 説明 |
|---------|------|
| X-RateLimit-Limit | 制限回数 |
| X-RateLimit-Remaining | 残回数 |
| X-RateLimit-Reset | リセット時刻（Unix Timestamp） |
```

---

## まとめ

| 概念 | ポイント |
|------|---------|
| API設計書 | フロント・バックエンド間のインターフェースを定義する |
| REST設計 | リソース指向のURL + HTTPメソッドで操作を表現する |
| 共通仕様 | ベースURL、認証、エラー形式、ページネーションを統一する |
| エンドポイント詳細 | リクエスト・レスポンスの形式と全ステータスコードを定義する |
| OpenAPI | 標準フォーマットで記述し、ドキュメント・コード自動生成に活用する |
| ベストプラクティス | バージョニング、フィルタリング、レート制限を適切に設計する |

---

## 次章の予告

次章では、設計品質を担保するための「設計レビューと品質管理」について学びます。レビューの進め方、チェックリスト、設計品質メトリクスを実践的に解説します。
