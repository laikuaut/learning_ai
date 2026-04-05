# 第1章：HTTP概論

## この章のゴール

- HTTP（HyperText Transfer Protocol）とは何かを理解する
- Webの仕組み（クライアント・サーバーモデル）を理解する
- URLの構造を正確に把握する
- HTTPの歴史（HTTP/0.9 〜 HTTP/3）の流れを知る
- curlコマンドで実際にHTTP通信を体験する

---

## 1.1 HTTPとは

### HTTPの定義

HTTP（HyperText Transfer Protocol）は、**WebブラウザとWebサーバーの間でデータをやり取りするための通信規約（プロトコル）**です。私たちが毎日Webサイトを見たり、APIを利用したりするとき、裏側ではHTTPが使われています。

```
【HTTPの基本的な流れ】

  クライアント                           サーバー
 （ブラウザ）                         （Webサーバー）
     │                                    │
     │  ① HTTPリクエスト                   │
     │  「/index.html をください」         │
     ├───────────────────────────────────→│
     │                                    │
     │  ② HTTPレスポンス                   │
     │  「200 OK、HTMLをどうぞ」           │
     │←───────────────────────────────────┤
     │                                    │
     ▼                                    ▼
  画面表示                             処理完了
```

### HTTPの特徴

```
【HTTPの4つの特徴】

┌──────────────────────────────────────────────────┐
│ 1. クライアント・サーバーモデル                     │
│    → クライアントがリクエストし、サーバーが応答する  │
├──────────────────────────────────────────────────┤
│ 2. ステートレス（Stateless）                       │
│    → 各リクエストは独立しており、前回の状態を保持しない│
│    → Cookie やセッションで状態管理を実現（第4章）   │
├──────────────────────────────────────────────────┤
│ 3. テキストベース（HTTP/1.x）                      │
│    → リクエスト/レスポンスが人間が読めるテキスト形式 │
│    → HTTP/2以降はバイナリ形式（第6章）              │
├──────────────────────────────────────────────────┤
│ 4. 拡張可能                                       │
│    → ヘッダーで様々なメタ情報を付加できる           │
│    → 新しい機能を後方互換性を保ちながら追加できる   │
└──────────────────────────────────────────────────┘
```

> **実務でのポイント**: 「ステートレス」はHTTPの最も重要な特徴です。サーバーはリクエストごとに「誰からのリクエストか」を覚えていません。ログイン状態の維持にはCookieやトークン（第4章で解説）が必要です。

---

## 1.2 URLの構造

### URLの各部分

URL（Uniform Resource Locator）は、Web上のリソースの位置を示す住所です。

```
【URLの構造】

https://www.example.com:443/path/to/page?key=value&lang=ja#section1
└─┬──┘ └──────┬───────┘└┬┘└─────┬──────┘└───────┬────────┘└───┬───┘
スキーム    ホスト名   ポート  パス        クエリ文字列     フラグメント
(scheme)   (host)   (port) (path)    (query string)   (fragment)
```

| 部分 | 説明 | 例 |
|---|---|---|
| **スキーム** | プロトコルの種類 | `http`, `https`, `ftp` |
| **ホスト名** | サーバーの名前またはIPアドレス | `www.example.com`, `192.168.1.1` |
| **ポート番号** | 接続先のポート（省略可） | `:443`（HTTPSデフォルト）, `:80`（HTTPデフォルト） |
| **パス** | サーバー上のリソースの位置 | `/api/users`, `/index.html` |
| **クエリ文字列** | パラメータ（`?` で開始、`&` で区切り） | `?page=1&sort=name` |
| **フラグメント** | ページ内の位置（`#` で開始） | `#section1`（サーバーには送信されない） |

```python
# PythonでURLを解析する
from urllib.parse import urlparse, parse_qs

url = "https://www.example.com:443/search?q=python&page=2#results"
parsed = urlparse(url)

print(f"スキーム:    {parsed.scheme}")     # https
print(f"ホスト名:    {parsed.hostname}")    # www.example.com
print(f"ポート:      {parsed.port}")        # 443
print(f"パス:        {parsed.path}")        # /search
print(f"クエリ:      {parsed.query}")       # q=python&page=2
print(f"フラグメント: {parsed.fragment}")    # results

# クエリパラメータを辞書に
params = parse_qs(parsed.query)
print(f"パラメータ:  {params}")  # {'q': ['python'], 'page': ['2']}
```

---

## 1.3 HTTPの歴史

```
【HTTPのバージョン変遷】

HTTP/0.9 (1991)  HTML文書の取得のみ。GETメソッドのみ。ヘッダーなし
    │
HTTP/1.0 (1996)  ヘッダー追加。GET以外のメソッド。ステータスコード導入
    │              ※ 1リクエストごとに接続を切断（非効率）
    │
HTTP/1.1 (1997)  Keep-Alive（接続の再利用）。Hostヘッダー必須
    │              パイプライン化。チャンク転送。現在も広く使用中
    │
HTTP/2  (2015)   バイナリプロトコル。多重化（1接続で複数リクエスト）
    │              ヘッダー圧縮（HPACK）。サーバープッシュ
    │
HTTP/3  (2022)   QUIC（UDP）ベース。接続確立の高速化
                   パケットロス時の性能向上
```

```
【HTTP/1.1 vs HTTP/2 の通信イメージ】

HTTP/1.1（順次処理）:
  接続1: GET /index.html → レスポンス → GET /style.css → レスポンス
  接続2: GET /script.js  → レスポンス → GET /image.png → レスポンス

HTTP/2（多重化）:
  接続1: GET /index.html ──→
         GET /style.css  ──→  すべてのリクエスト/レスポンスが
         GET /script.js  ──→  1つの接続上で並行して流れる
         GET /image.png  ──→
```

---

## 1.4 curlコマンドでHTTP通信を体験する

### 基本的なGETリクエスト

```bash
# GETリクエスト（レスポンスボディのみ表示）
curl https://httpbin.org/get

# レスポンスヘッダーも表示（-i オプション）
curl -i https://httpbin.org/get

# リクエスト/レスポンスの詳細を表示（-v オプション）
curl -v https://httpbin.org/get

# レスポンスヘッダーのみ表示（-I オプション = HEADリクエスト）
curl -I https://httpbin.org/get
```

### curlの -v オプション出力の読み方

```
$ curl -v https://httpbin.org/get

*   Trying 3.230.24.45:443...
* Connected to httpbin.org (3.230.24.45) port 443
* SSL connection using TLSv1.3
> GET /get HTTP/1.1              ← リクエスト行（> は送信データ）
> Host: httpbin.org              ← リクエストヘッダー
> User-Agent: curl/8.4.0
> Accept: */*
>
< HTTP/1.1 200 OK               ← ステータス行（< は受信データ）
< Content-Type: application/json ← レスポンスヘッダー
< Content-Length: 256
<
{                                ← レスポンスボディ
  "args": {},
  "headers": { ... },
  "origin": "203.0.113.1",
  "url": "https://httpbin.org/get"
}
```

### POSTリクエスト

```bash
# JSONデータをPOST
curl -X POST https://httpbin.org/post \
  -H "Content-Type: application/json" \
  -d '{"name": "田中太郎", "email": "tanaka@example.com"}'

# フォームデータをPOST
curl -X POST https://httpbin.org/post \
  -d "name=田中太郎&email=tanaka@example.com"
```

> **実務でのポイント**: `curl` はAPI開発・デバッグで最もよく使われるツールです。`-v`（verbose）オプションで通信の詳細が見えるため、問題の調査に欠かせません。

---

## 1.5 Pythonで最初のHTTPリクエスト

```python
# 標準ライブラリのみで GET リクエスト
from urllib.request import urlopen, Request
import json

# GET リクエスト
url = "https://httpbin.org/get"
with urlopen(url) as response:
    print(f"ステータス: {response.status}")                # 200
    print(f"Content-Type: {response.getheader('Content-Type')}")
    body = json.loads(response.read())
    print(f"IP: {body['origin']}")

# POST リクエスト
url = "https://httpbin.org/post"
data = json.dumps({"name": "田中太郎"}).encode("utf-8")
req = Request(url, data=data, method="POST")
req.add_header("Content-Type", "application/json")

with urlopen(req) as response:
    print(f"ステータス: {response.status}")
    body = json.loads(response.read())
    print(f"送信データ: {body['json']}")
```

---

## ポイントまとめ

```
┌─────────────────────────────────────────────────────────────┐
│                     第1章のポイント                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. HTTPはWebの通信プロトコル                                │
│     → クライアントがリクエスト、サーバーがレスポンス          │
│                                                             │
│  2. HTTPはステートレス                                       │
│     → 各リクエストは独立、状態はCookie等で管理               │
│                                                             │
│  3. URLは「スキーム://ホスト:ポート/パス?クエリ#フラグメント」│
│     → 各部分の役割を正確に理解する                           │
│                                                             │
│  4. HTTP/1.1 → HTTP/2 → HTTP/3 と進化                      │
│     → 多重化、ヘッダー圧縮、QUIC等で高速化                  │
│                                                             │
│  5. curlの -v オプションで通信の詳細を確認できる              │
│     → > は送信、< は受信を表す                              │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**次の章では**: HTTPメソッドとステータスコードを詳しく学びます。GET、POST、PUT、DELETEの使い分けと、200、301、404、500などのステータスコードの意味を解説します。
