# 第7章：REST API設計

## この章のゴール

- REST（Representational State Transfer）の設計原則を理解する
- リソース指向のURL設計ができるようになる
- リクエスト・レスポンスの設計パターンを学ぶ
- エラーレスポンスの統一設計を理解する
- API バージョニングとページネーションの方法を学ぶ
- CORS（Cross-Origin Resource Sharing）の仕組みを理解する

---

## 7.1 RESTとは

### RESTの設計原則

REST（Representational State Transfer）は、HTTPプロトコルの特性を活かしたAPI設計スタイルです。

```
【RESTの6つの原則】

┌──────────────────────────────────────────────────┐
│ 1. クライアント・サーバー分離                       │
│    → フロントとバックを独立して開発できる           │
├──────────────────────────────────────────────────┤
│ 2. ステートレス                                    │
│    → 各リクエストに必要な情報をすべて含める          │
├──────────────────────────────────────────────────┤
│ 3. キャッシュ可能                                  │
│    → レスポンスにキャッシュ可否を明示する            │
├──────────────────────────────────────────────────┤
│ 4. 統一インタフェース                               │
│    → URLはリソース名詞、操作はHTTPメソッドで表現     │
├──────────────────────────────────────────────────┤
│ 5. 階層化システム                                  │
│    → プロキシやロードバランサを挟める                │
├──────────────────────────────────────────────────┤
│ 6. コードオンデマンド（オプション）                  │
│    → 必要に応じてクライアントにコードを送る          │
└──────────────────────────────────────────────────┘
```

---

## 7.2 URL設計

### リソース指向のURL

```
【URL設計のルール】

✅ 良い設計（リソースは名詞・複数形）:
  GET    /users              ユーザー一覧
  GET    /users/123          ユーザー詳細
  POST   /users              ユーザー作成
  PUT    /users/123          ユーザー更新
  DELETE /users/123          ユーザー削除
  GET    /users/123/orders   ユーザーの注文一覧

❌ 悪い設計（動詞を含む、一貫性がない）:
  GET    /getUsers
  POST   /createUser
  GET    /user/list
  POST   /users/123/delete
```

### ネスト（親子関係）

```
【ネストの設計指針】

✅ 自然な親子関係（2階層まで）:
  GET /users/123/orders          ← ユーザー123の注文一覧
  GET /users/123/orders/456      ← 注文456の詳細

❌ 深すぎるネスト（3階層以上は避ける）:
  GET /users/123/orders/456/items/789/reviews
  → GET /order-items/789/reviews に分割する
```

---

## 7.3 リクエスト・レスポンス設計

### 一覧取得のレスポンス

```json
{
  "data": [
    {"id": 1, "name": "田中太郎", "email": "tanaka@example.com"},
    {"id": 2, "name": "鈴木花子", "email": "suzuki@example.com"}
  ],
  "pagination": {
    "current_page": 1,
    "per_page": 20,
    "total_count": 45,
    "total_pages": 3,
    "has_next": true,
    "has_prev": false
  }
}
```

### エラーレスポンスの統一形式

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "入力内容に誤りがあります",
    "details": [
      {"field": "email", "message": "メールアドレスの形式が不正です"},
      {"field": "age", "message": "0以上の整数を入力してください"}
    ]
  }
}
```

```
【ステータスコードとエラーコードの対応】

400 Bad Request       → INVALID_JSON, INVALID_PARAMETER
401 Unauthorized      → UNAUTHORIZED, TOKEN_EXPIRED
403 Forbidden         → FORBIDDEN, INSUFFICIENT_PERMISSIONS
404 Not Found         → RESOURCE_NOT_FOUND
409 Conflict          → DUPLICATE_EMAIL, OUT_OF_STOCK
422 Unprocessable     → VALIDATION_ERROR
429 Too Many Requests → RATE_LIMIT_EXCEEDED
500 Internal Error    → INTERNAL_ERROR
```

---

## 7.4 ページネーション

```
【ページネーションの2方式】

■ オフセットベース（一般的）
  GET /users?page=2&per_page=20
  → 利点: ページ番号でジャンプ可能
  → 欠点: 大量データでOFFSETが遅い

■ カーソルベース（大量データ向け）
  GET /users?cursor=eyJpZCI6MTAwfQ&limit=20
  → 利点: 大量データでも高速
  → 欠点: ページ番号ジャンプ不可
```

---

## 7.5 CORS（Cross-Origin Resource Sharing）

### CORSの仕組み

異なるオリジン（ドメイン）間でのHTTPリクエストを制御する仕組みです。

```
【CORSが必要な場面】

フロントエンド: https://app.example.com
API サーバー:  https://api.example.com
→ オリジンが異なるため、ブラウザがリクエストをブロック
→ APIサーバーがCORSヘッダーを返すことで許可する

【CORSのフロー（プリフライトリクエスト）】

ブラウザ                           APIサーバー
  │                                   │
  │ ① OPTIONS /api/users              │  プリフライト
  │    Origin: https://app.example.com │  リクエスト
  ├──────────────────────────────────→│
  │                                   │
  │ ② 200 OK                          │  許可ヘッダー
  │    Access-Control-Allow-Origin: *  │
  │    Access-Control-Allow-Methods:   │
  │      GET, POST                     │
  │←──────────────────────────────────┤
  │                                   │
  │ ③ GET /api/users                  │  実際の
  │    Origin: https://app.example.com │  リクエスト
  ├──────────────────────────────────→│
  │                                   │
  │ ④ 200 OK + データ                 │
  │←──────────────────────────────────┤
```

### 主要なCORSヘッダー

```
Access-Control-Allow-Origin: https://app.example.com
  → 許可するオリジン（* は全オリジン許可）

Access-Control-Allow-Methods: GET, POST, PUT, DELETE
  → 許可するHTTPメソッド

Access-Control-Allow-Headers: Content-Type, Authorization
  → 許可するリクエストヘッダー

Access-Control-Max-Age: 86400
  → プリフライトのキャッシュ期間（秒）
```

> **実務でのポイント**: `Access-Control-Allow-Origin: *` は開発時には便利ですが、本番環境では具体的なオリジンを指定しましょう。`*` と `Authorization` ヘッダーの組み合わせはセキュリティリスクになります。

---

## 7.6 APIバージョニング

```
【バージョニングの3方式】

1. URLパス方式（推奨）
   GET /v1/users
   GET /v2/users

2. ヘッダー方式
   Accept: application/vnd.myapi.v2+json

3. クエリパラメータ方式
   GET /users?version=2
```

---

## ポイントまとめ

```
┌─────────────────────────────────────────────────────────────┐
│                     第7章のポイント                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. REST APIはリソース指向: URLは名詞、操作はHTTPメソッド     │
│                                                             │
│  2. エラーレスポンスはcode + message + detailsの統一形式      │
│                                                             │
│  3. ページネーション: オフセットベース or カーソルベース       │
│                                                             │
│  4. CORS: 異なるオリジン間のリクエスト制御                    │
│     → プリフライトリクエスト（OPTIONS）で許可を確認           │
│                                                             │
│  5. バージョニングはURLパス方式（/v1/）が最も一般的           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**次の章では**: HTTPのセキュリティを総合的に学びます。OWASP Top 10を中心に、Webアプリケーションの代表的な脆弱性と対策を解説します。
