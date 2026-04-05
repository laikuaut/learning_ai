# 第2章：HTTPメソッドとステータスコード

## この章のゴール

- HTTPメソッド（GET, POST, PUT, PATCH, DELETE等）の意味と使い分けを理解する
- べき等性（Idempotency）と安全性（Safety）の概念を理解する
- ステータスコードの分類（1xx〜5xx）を体系的に理解する
- 主要なステータスコードの意味と使用場面を把握する
- REST APIにおけるメソッドとステータスコードの使い方を理解する

---

## 2.1 HTTPメソッド

### 主要なHTTPメソッド一覧

```
【HTTPメソッドの全体像】

┌──────────┬──────────────────────────────┬──────┬──────┐
│ メソッド  │ 用途                          │ 安全 │べき等│
├──────────┼──────────────────────────────┼──────┼──────┤
│ GET      │ リソースの取得                 │  ○  │  ○  │
│ POST     │ リソースの作成・処理の実行      │  ✗  │  ✗  │
│ PUT      │ リソースの全体更新（置換）      │  ✗  │  ○  │
│ PATCH    │ リソースの部分更新             │  ✗  │  ✗  │
│ DELETE   │ リソースの削除                 │  ✗  │  ○  │
│ HEAD     │ ヘッダーのみ取得（GETのボディなし）│ ○  │  ○  │
│ OPTIONS  │ 対応メソッドの確認（CORS等）    │  ○  │  ○  │
└──────────┴──────────────────────────────┴──────┴──────┘

安全（Safe）: サーバーの状態を変更しない
べき等（Idempotent）: 同じリクエストを何度送っても結果が同じ
```

### GET — リソースの取得

```bash
# GETリクエストの例
curl https://httpbin.org/get?name=tanaka

# GETの特徴:
# ・パラメータはURLのクエリ文字列に含める
# ・リクエストボディは通常使わない
# ・ブラウザのアドレスバーに入力した時のデフォルト
# ・キャッシュ可能
# ・ブックマーク可能
```

### POST — リソースの作成

```bash
# POSTリクエストの例：ユーザー作成
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name": "田中太郎", "email": "tanaka@example.com"}'

# POSTの特徴:
# ・データはリクエストボディに含める
# ・新しいリソースを作成する
# ・同じリクエストを2回送ると2つのリソースが作成される（べき等でない）
# ・キャッシュされない（通常）
```

### PUT — リソースの全体更新

```bash
# PUTリクエストの例：ユーザー情報を置換
curl -X PUT https://httpbin.org/put \
  -H "Content-Type: application/json" \
  -d '{"name": "田中次郎", "email": "jiro@example.com"}'

# PUTの特徴:
# ・リソース全体を置き換える
# ・指定した内容で完全に上書き（送信しなかったフィールドは消える）
# ・べき等：同じリクエストを何度送っても結果は同じ
```

### PATCH — リソースの部分更新

```bash
# PATCHリクエストの例：名前だけ更新
curl -X PATCH https://httpbin.org/patch \
  -H "Content-Type: application/json" \
  -d '{"name": "田中次郎"}'

# PATCHの特徴:
# ・リソースの一部だけ更新する
# ・送信しなかったフィールドは変更されない
# ・PUTとの違い：PUTは全体置換、PATCHは部分更新
```

### PUT vs PATCH の違い

```
【PUT と PATCH の違い】

現在のデータ:
  {"name": "田中太郎", "email": "tanaka@example.com", "age": 30}

PUT {"name": "田中次郎"} を送信:
  → {"name": "田中次郎"}
  ※ email と age が消えた！（全体置換）

PATCH {"name": "田中次郎"} を送信:
  → {"name": "田中次郎", "email": "tanaka@example.com", "age": 30}
  ※ name だけ変更、他はそのまま（部分更新）
```

### DELETE — リソースの削除

```bash
# DELETEリクエストの例
curl -X DELETE https://httpbin.org/delete

# DELETEの特徴:
# ・指定したリソースを削除する
# ・べき等：同じリソースを2回削除しても結果は同じ
#  （2回目は「既に存在しない」= 変化なし）
```

> **実務でのポイント**: REST APIの設計では、HTTPメソッドをCRUD操作に対応させるのが一般的です。POST=Create、GET=Read、PUT/PATCH=Update、DELETE=Delete。この対応を崩すと（例：GETで削除する）、予期しないキャッシュや再送で事故が起きます。

---

## 2.2 べき等性と安全性

### べき等性（Idempotency）

**同じリクエストを何回送っても、サーバーの状態が1回送った場合と同じになる**性質です。

```
【べき等性のイメージ】

GET /users/1        → ユーザー情報を返す → 何度呼んでも同じ（べき等 ○）

POST /users         → ユーザーを作成     → 2回呼ぶと2人作成される（べき等 ✗）

PUT /users/1        → ユーザーを上書き   → 何度呼んでも同じ結果（べき等 ○）

DELETE /users/1     → ユーザーを削除     → 2回目は「もうない」（べき等 ○）
```

> **実務でのポイント**: ネットワークエラーでリクエストが重複送信された場合、べき等なメソッド（GET, PUT, DELETE）なら問題ありませんが、POST は重複で意図しないリソースが作成される可能性があります。決済APIなどでは「冪等キー（Idempotency Key）」をヘッダーに含める設計が一般的です。

---

## 2.3 ステータスコード

### ステータスコードの分類

```
【ステータスコードの5分類】

1xx（情報）      : リクエスト処理中。続行してください
2xx（成功）      : リクエスト成功。正常に処理されました
3xx（リダイレクト）: 別の場所を参照してください
4xx（クライアントエラー）: リクエストに問題があります
5xx（サーバーエラー）: サーバー側で問題が発生しました
```

### 主要なステータスコード

```
【2xx: 成功】

200 OK              一般的な成功（GET/PUT/PATCH/DELETE）
201 Created          リソースの作成に成功（POST）
204 No Content       成功したがレスポンスボディなし（DELETE）

【3xx: リダイレクト】

301 Moved Permanently    恒久的な移転（URLが永久に変わった）
302 Found                一時的なリダイレクト
304 Not Modified         キャッシュをそのまま使ってよい

【4xx: クライアントエラー】

400 Bad Request          リクエストの形式が不正
401 Unauthorized         認証が必要（未認証）
403 Forbidden            認証済みだが権限がない（認可エラー）
404 Not Found            リソースが存在しない
405 Method Not Allowed   そのHTTPメソッドは許可されていない
409 Conflict             リソースの状態と矛盾する操作
422 Unprocessable Entity バリデーションエラー
429 Too Many Requests    レートリミット超過

【5xx: サーバーエラー】

500 Internal Server Error  サーバー内部エラー（汎用）
502 Bad Gateway            プロキシ先のサーバーから不正な応答
503 Service Unavailable    サーバーが一時的に利用不可
504 Gateway Timeout        プロキシ先のサーバーがタイムアウト
```

### 401 vs 403 の違い

```
【401 Unauthorized と 403 Forbidden の違い】

401 Unauthorized:
  → 「あなたは誰ですか？」（認証されていない）
  → 正しい認証情報を送れば成功する可能性がある
  例: ログインしていない状態でマイページにアクセス

403 Forbidden:
  → 「あなたが誰かはわかるが、許可されていない」（認可エラー）
  → 認証情報を送っても成功しない
  例: 一般ユーザーが管理者ページにアクセス
```

### 301 vs 302 の違い

```
【301 と 302 の違い】

301 Moved Permanently（恒久的リダイレクト）:
  → URLが永久に変わった
  → ブラウザはリダイレクト先をキャッシュする
  → SEO: 評価が新しいURLに引き継がれる
  例: http → https への移行、ドメイン変更

302 Found（一時的リダイレクト）:
  → URLが一時的に変わっている
  → ブラウザは元のURLを記憶し続ける
  → SEO: 評価は元のURLに残る
  例: メンテナンス中のリダイレクト、ログイン後のリダイレクト
```

---

## 2.4 REST APIでの実践例

### ユーザーAPIの設計例

```
【REST API設計例：ユーザー管理】

メソッド   パス              操作          ステータスコード
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GET       /users            一覧取得       200 OK
GET       /users/123        詳細取得       200 OK / 404 Not Found
POST      /users            新規作成       201 Created
PUT       /users/123        全体更新       200 OK / 404 Not Found
PATCH     /users/123        部分更新       200 OK / 404 Not Found
DELETE    /users/123        削除           204 No Content / 404 Not Found
```

### Pythonでの実行例

```python
from urllib.request import urlopen, Request
import json

BASE_URL = "https://httpbin.org"

# --- GET ---
print("=== GET ===")
with urlopen(f"{BASE_URL}/get") as resp:
    print(f"Status: {resp.status}")  # 200

# --- POST ---
print("\n=== POST ===")
data = json.dumps({"name": "田中太郎"}).encode("utf-8")
req = Request(f"{BASE_URL}/post", data=data, method="POST")
req.add_header("Content-Type", "application/json")
with urlopen(req) as resp:
    print(f"Status: {resp.status}")  # 200
    body = json.loads(resp.read())
    print(f"送信データ: {body['json']}")

# --- PUT ---
print("\n=== PUT ===")
data = json.dumps({"name": "田中次郎", "email": "jiro@example.com"}).encode("utf-8")
req = Request(f"{BASE_URL}/put", data=data, method="PUT")
req.add_header("Content-Type", "application/json")
with urlopen(req) as resp:
    print(f"Status: {resp.status}")  # 200

# --- DELETE ---
print("\n=== DELETE ===")
req = Request(f"{BASE_URL}/delete", method="DELETE")
with urlopen(req) as resp:
    print(f"Status: {resp.status}")  # 200
```

---

## 2.5 レスポンスボディの形式

### 主要なレスポンス形式

```
【レスポンスボディの主な形式】

┌────────────────────┬──────────────────────────┬────────────────┐
│ Content-Type       │ 用途                      │ 例             │
├────────────────────┼──────────────────────────┼────────────────┤
│ text/html          │ Webページ（HTML）          │ ブラウザ表示    │
│ application/json   │ API のデータ交換           │ REST API      │
│ text/plain         │ プレーンテキスト           │ ログ、.txt     │
│ application/xml    │ XMLデータ                  │ SOAP、設定     │
│ image/png          │ PNG画像                    │ 画像ファイル    │
│ application/pdf    │ PDFファイル                │ ドキュメント    │
│ application/octet-stream│ バイナリデータ（汎用）│ ファイルDL      │
└────────────────────┴──────────────────────────┴────────────────┘
```

---

## ポイントまとめ

```
┌─────────────────────────────────────────────────────────────┐
│                     第2章のポイント                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. HTTPメソッドはリソースに対する「操作」を表す              │
│     → GET=取得, POST=作成, PUT=全体更新, PATCH=部分更新,     │
│       DELETE=削除                                           │
│                                                             │
│  2. べき等性: 同じリクエストを何度送っても結果が同じ           │
│     → GET, PUT, DELETE はべき等。POST はべき等でない         │
│                                                             │
│  3. ステータスコードは5分類                                   │
│     → 2xx=成功, 3xx=リダイレクト, 4xx=クライアントエラー,    │
│       5xx=サーバーエラー                                     │
│                                                             │
│  4. 401（未認証）と 403（権限不足）を区別する                │
│     → 401=ログインしていない, 403=ログイン済みだが権限がない │
│                                                             │
│  5. REST APIではメソッド×パス×ステータスコードの                │
│     組み合わせで直感的なAPI設計ができる                       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**次の章では**: HTTPヘッダーを詳しく学びます。Content-Type、Authorization、Cache-Control など、リクエストとレスポンスのメタ情報を制御する方法を解説します。
