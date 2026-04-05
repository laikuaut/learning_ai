# 第5章：HTTPS・SSL/TLS

## この章のゴール
- HTTPの3つの問題点（盗聴・改ざん・なりすまし）を理解する
- HTTPS = HTTP + TLS の仕組みを説明できる
- 共通鍵暗号と公開鍵暗号の違いを理解する
- TLSハンドシェイクの流れを図で説明できる
- SSL証明書の種類（DV, OV, EV）と認証局の役割を理解する
- Let's Encryptによる無料証明書の仕組みを知る
- HTTP→HTTPSの移行に必要な対応を理解する

---

## 5.1 HTTPの問題点

HTTPは通信内容を**暗号化しません**。そのため、以下の3つのセキュリティ上の問題があります。

### 3つのリスク

```
クライアント ----[HTTP（平文）]----> サーバー
                    ↑
                  攻撃者
                （盗み見可能）
```

| リスク | 説明 | 具体例 |
|--------|------|--------|
| **盗聴**（Eavesdropping） | 通信内容を第三者が読み取れる | パスワード・クレジットカード番号の漏洩 |
| **改ざん**（Tampering） | 通信内容を途中で書き換えられる | 振込先口座の変更、不正なスクリプト挿入 |
| **なりすまし**（Spoofing） | 偽のサーバーが本物のふりをする | フィッシングサイト |

### 公衆Wi-Fiでの危険

```
あなたのPC                    カフェの無料Wi-Fi                     サーバー
    |                              |                                  |
    | POST /login                  |                                  |
    | username=taro                |                                  |
    | password=secret123           |                                  |
    |----------------------------->|  ← 攻撃者がWi-Fiを盗聴          |
    |                              |  「taro / secret123 を入手!」     |
    |                              |--------------------------------->|
```

> **実務でのポイント**: 2024年現在、主要ブラウザはHTTPサイトに対して「保護されていない通信」と警告を表示します。ユーザーの信頼を得るためにも**HTTPSは必須**です。

---

## 5.2 HTTPS = HTTP + TLS

HTTPS（HTTP Secure / HTTP over TLS）は、HTTPの通信を**TLS**（Transport Layer Security / トランスポート層セキュリティ）で暗号化したプロトコルです。

```
+------------------------------------------------------+
|                  HTTPS の構造                          |
|                                                      |
|  +------------------+                                |
|  |    HTTP          |  ← アプリケーション層            |
|  +------------------+                                |
|  |    TLS           |  ← 暗号化・認証を担当            |
|  +------------------+                                |
|  |    TCP           |  ← トランスポート層              |
|  +------------------+                                |
|  |    IP            |  ← ネットワーク層                |
|  +------------------+                                |
+------------------------------------------------------+
```

| 項目 | HTTP | HTTPS |
|------|------|-------|
| ポート番号 | 80 | 443 |
| 暗号化 | なし | TLSで暗号化 |
| URLスキーム | `http://` | `https://` |
| 証明書 | 不要 | 必要 |
| 速度 | やや速い | TLSハンドシェイク分のオーバーヘッド |

### SSLとTLSの関係

SSL（Secure Sockets Layer）はTLSの前身です。現在「SSL」と呼ばれることがありますが、**実際に使われているのはTLS**です。

```
SSL 1.0 → 公開されず
SSL 2.0 → 1995年（脆弱性あり、非推奨）
SSL 3.0 → 1996年（脆弱性あり、非推奨）
TLS 1.0 → 1999年（非推奨）
TLS 1.1 → 2006年（非推奨）
TLS 1.2 → 2008年（現在広く使用）
TLS 1.3 → 2018年（最新、推奨）
```

> **よくある間違い**: 「SSL証明書」という呼び方が広く使われていますが、技術的には「TLS証明書」が正確です。慣習的に「SSL証明書」「SSL/TLS証明書」と呼ばれています。

---

## 5.3 共通鍵暗号と公開鍵暗号

TLSは**2種類の暗号方式**を組み合わせて使います。

### 共通鍵暗号（Symmetric Key Encryption）

送信者と受信者が**同じ鍵**を使って暗号化・復号を行います。

```
送信者                                  受信者
  |                                       |
  |  共通鍵: 🔑 (同じ鍵)                  |
  |                                       |
  |  平文「Hello」                         |
  |  🔑 → 暗号化 → 「X#9kL」             |
  |                                       |
  |  暗号文「X#9kL」を送信                 |
  |-------------------------------------->|
  |                                       |
  |              🔑 → 復号 → 「Hello」    |
```

| 特徴 | 説明 |
|------|------|
| 処理速度 | **高速** |
| 鍵の管理 | 事前に安全な方法で鍵を共有する必要がある |
| 代表的なアルゴリズム | AES（Advanced Encryption Standard） |

### 公開鍵暗号（Public Key Encryption / 非対称鍵暗号）

**公開鍵**と**秘密鍵**のペアを使います。公開鍵で暗号化し、秘密鍵で復号します。

```
送信者                                   受信者
  |                                        |
  |  受信者の公開鍵: 🔓                     |  秘密鍵: 🔐
  |                                        |
  |  平文「Hello」                          |
  |  🔓 → 暗号化 → 「Y@3mN」              |
  |                                        |
  |  暗号文「Y@3mN」を送信                  |
  |--------------------------------------->|
  |                                        |
  |               🔐 → 復号 → 「Hello」    |
```

| 特徴 | 説明 |
|------|------|
| 処理速度 | **低速**（共通鍵暗号の数百倍〜数千倍遅い） |
| 鍵の管理 | 公開鍵は誰に知られても安全。秘密鍵だけ守ればよい |
| 代表的なアルゴリズム | RSA, ECDSA |

### TLSではどう使い分けるか

```
【TLSのハイブリッド方式】

1. 公開鍵暗号で「共通鍵」を安全に交換
2. 以降の通信は高速な共通鍵暗号で暗号化

   公開鍵暗号 → 鍵の交換（安全だが遅い）
   共通鍵暗号 → データの暗号化（高速）
```

> **ポイント**: 公開鍵暗号の安全性と共通鍵暗号の速さを**いいとこ取り**しているのがTLSの賢いところです。

---

## 5.4 TLSハンドシェイクの流れ

TLSハンドシェイク（TLS Handshake）は、暗号化通信を開始する前に行われる**鍵の交換と認証**の手続きです。

### TLS 1.2 のハンドシェイク

```
クライアント                                サーバー
    |                                          |
    |  ① ClientHello                           |
    |  対応するTLSバージョン、暗号スイート一覧   |
    |  クライアントランダム値                     |
    |----------------------------------------->|
    |                                          |
    |  ② ServerHello                           |
    |  選択したTLSバージョン、暗号スイート       |
    |  サーバーランダム値                        |
    |  ③ Certificate（サーバー証明書）           |
    |  ④ ServerKeyExchange                     |
    |  ⑤ ServerHelloDone                       |
    |<-----------------------------------------|
    |                                          |
    |  ⑥ ClientKeyExchange                     |
    |  （プリマスターシークレットを送信）         |
    |  ⑦ ChangeCipherSpec                      |
    |  ⑧ Finished（暗号化で送信）               |
    |----------------------------------------->|
    |                                          |
    |  ⑨ ChangeCipherSpec                      |
    |  ⑩ Finished（暗号化で送信）               |
    |<-----------------------------------------|
    |                                          |
    |  === 以降、暗号化通信開始 ===              |
    |                                          |
```

### 各ステップの解説

| ステップ | 内容 |
|---------|------|
| ① ClientHello | クライアントが対応するTLSバージョンと暗号スイートを提示 |
| ② ServerHello | サーバーが使用するバージョンと暗号スイートを選択 |
| ③ Certificate | サーバーがSSL証明書を提示（身分証明） |
| ④ ServerKeyExchange | 鍵交換に必要なパラメータを送信 |
| ⑤ ServerHelloDone | サーバー側のHelloフェーズ完了 |
| ⑥ ClientKeyExchange | クライアントがプリマスターシークレットを送信 |
| ⑦⑨ ChangeCipherSpec | 暗号化方式の切り替えを通知 |
| ⑧⑩ Finished | ハンドシェイクの完了確認 |

### TLS 1.3 の改良

TLS 1.3ではハンドシェイクが**1往復（1-RTT）**に短縮されました。

```
クライアント                          サーバー
    |                                    |
    |  ClientHello + KeyShare            |
    |  （鍵交換を同時に開始）             |
    |----------------------------------->|
    |                                    |
    |  ServerHello + KeyShare            |
    |  Certificate + Finished            |
    |<-----------------------------------|
    |                                    |
    |  Finished                          |
    |----------------------------------->|
    |                                    |
    |  === 暗号化通信開始 ===             |
```

| 比較項目 | TLS 1.2 | TLS 1.3 |
|---------|---------|---------|
| ハンドシェイク | 2往復（2-RTT） | 1往復（1-RTT） |
| 0-RTT再接続 | 非対応 | 対応 |
| 暗号スイート | 多数（弱いものも含む） | 安全なもののみ |
| 前方秘匿性 | オプション | 必須 |

### curlでTLS情報を確認

```bash
# TLSハンドシェイクの詳細を表示
curl -v https://www.example.com 2>&1 | grep -E "SSL|TLS|subject|issuer"

# 使用されるTLSバージョンを確認
curl -v https://www.example.com 2>&1 | grep "SSL connection"
```

出力例:

```
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* Server certificate:
*  subject: CN=www.example.org
*  issuer: C=US; O=DigiCert Inc; CN=DigiCert Global G2 TLS RSA SHA256 2020 CA1
```

### Pythonでの確認

```python
import http.client
import ssl

# TLS接続の詳細を確認
conn = http.client.HTTPSConnection("www.example.com")
conn.request("GET", "/")
response = conn.getresponse()

# 使用されている暗号情報
sock = conn.sock
if hasattr(sock, 'version'):
    print(f"TLSバージョン: {sock.version()}")
if hasattr(sock, 'cipher'):
    cipher = sock.cipher()
    print(f"暗号スイート: {cipher[0]}")
    print(f"プロトコル: {cipher[1]}")
    print(f"鍵長: {cipher[2]}ビット")

response.read()
conn.close()
```

---

## 5.5 SSL証明書の仕組みと種類

### SSL証明書とは

SSL証明書（正確にはTLS証明書）は、**Webサイトの身分証明書**です。以下の情報が含まれます。

- ドメイン名（例: www.example.com）
- 発行者（認証局）の情報
- 有効期間
- 公開鍵
- デジタル署名

### 証明書の種類

| 種類 | 正式名称 | 検証レベル | 取得コスト | 用途 |
|------|---------|-----------|-----------|------|
| **DV** | Domain Validation | ドメインの所有権のみ | 無料〜安価 | 個人サイト、ブログ |
| **OV** | Organization Validation | ドメイン＋組織の実在確認 | 中程度 | 企業サイト |
| **EV** | Extended Validation | 厳格な組織審査 | 高額 | 金融機関、ECサイト |

```
【検証レベルの比較】

DV証明書:
  ✅ ドメインの所有者であること → 確認済み
  ❌ 組織の実在性 → 未確認
  ❌ 組織の法的存在 → 未確認

OV証明書:
  ✅ ドメインの所有者であること → 確認済み
  ✅ 組織の実在性 → 確認済み
  ❌ 組織の法的存在 → 簡易確認

EV証明書:
  ✅ ドメインの所有者であること → 確認済み
  ✅ 組織の実在性 → 確認済み
  ✅ 組織の法的存在 → 厳格に確認済み
```

> **よくある間違い**: DV証明書だから安全でない、EV証明書だから安全、というわけではありません。**暗号化の強度はどの種類でも同じ**です。違いは「誰が運営しているか」の検証レベルです。

---

## 5.6 認証局（CA）とルート証明書

### 認証局（CA: Certificate Authority）

認証局とは、SSL証明書を**発行する信頼された組織**です。

```
【証明書の信頼チェーン（Chain of Trust）】

  ルート認証局（Root CA）
  自己署名証明書（最上位の信頼の起点）
        |
        | 署名
        ↓
  中間認証局（Intermediate CA）
  ルートCAに署名された証明書
        |
        | 署名
        ↓
  サーバー証明書
  中間CAに署名された証明書
  （www.example.comの証明書）
```

### ルート証明書

ルート証明書は、OS やブラウザに**あらかじめ組み込まれている**信頼の起点です。

- Windows: 「証明書マネージャー」に格納
- macOS: 「キーチェーンアクセス」に格納
- Linux: `/etc/ssl/certs/` ディレクトリ
- ブラウザ: 独自の証明書ストア（Firefoxなど）

### 証明書の検証の流れ

```
ブラウザ                                     サーバー
    |                                           |
    |  1. HTTPS接続開始                          |
    |------------------------------------------>|
    |                                           |
    |  2. サーバー証明書 + 中間証明書を返す       |
    |<------------------------------------------|
    |                                           |
    |  3. 証明書の検証                           |
    |  ① サーバー証明書の署名を中間CAの          |
    |     公開鍵で検証                           |
    |  ② 中間CA証明書の署名をルートCAの          |
    |     公開鍵で検証                           |
    |  ③ ルートCA証明書がOS/ブラウザの           |
    |     信頼リストに存在するか確認              |
    |  ④ 証明書の有効期限を確認                  |
    |  ⑤ ドメイン名の一致を確認                  |
    |                                           |
    |  すべてOK → 安全な接続を確立               |
```

---

## 5.7 Let's Encrypt による無料証明書

Let's Encrypt（レッツ・エンクリプト）は、**無料でDV証明書を発行する認証局**です。2016年のサービス開始以来、HTTPSの普及に大きく貢献しました。

### 特徴

| 項目 | 内容 |
|------|------|
| 費用 | **無料** |
| 証明書の種類 | DV証明書のみ |
| 有効期間 | 90日（自動更新を推奨） |
| 発行方法 | ACME（Automatic Certificate Management Environment）プロトコル |
| ツール | certbot（公式推奨クライアント） |

### certbotでの証明書取得（例）

```bash
# certbotのインストール（Ubuntu/Debian）
sudo apt install certbot

# Nginx用の証明書取得と自動設定
sudo certbot --nginx -d example.com -d www.example.com

# 証明書の自動更新テスト
sudo certbot renew --dry-run
```

### ACME チャレンジの仕組み

Let's Encryptはドメインの所有権を自動的に確認します。

```
certbot                     Let's Encrypt              あなたのサーバー
   |                              |                         |
   |  1. 証明書発行リクエスト      |                         |
   |----------------------------->|                         |
   |                              |                         |
   |  2. チャレンジトークン発行    |                         |
   |<-----------------------------|                         |
   |                              |                         |
   |  3. トークンをサーバーに配置                             |
   |------------------------------------------------>       |
   |                              |                         |
   |                              |  4. トークンを確認       |
   |                              |------------------------>|
   |                              |  5. 確認OK              |
   |                              |<------------------------|
   |                              |                         |
   |  6. 証明書発行               |                         |
   |<-----------------------------|                         |
```

---

## 5.8 HTTP→HTTPSの移行

### 301リダイレクト

HTTPでアクセスされた場合に、HTTPSに恒久的にリダイレクトします。

```
クライアント                              サーバー
    |                                        |
    |  GET http://example.com/               |
    |--------------------------------------->|
    |                                        |
    |  301 Moved Permanently                 |
    |  Location: https://example.com/        |
    |<---------------------------------------|
    |                                        |
    |  GET https://example.com/              |
    |--------------------------------------->|
    |                                        |
    |  200 OK (暗号化通信)                    |
    |<---------------------------------------|
```

**Nginxでの設定例:**

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    return 301 https://$server_name$request_uri;
}
```

### HSTS（HTTP Strict Transport Security）

HSTS は、ブラウザに「**このサイトには今後HTTPSでのみアクセスせよ**」と指示する仕組みです。

```
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
```

| ディレクティブ | 説明 |
|---------------|------|
| `max-age=31536000` | 1年間（秒数）HTTPSを強制 |
| `includeSubDomains` | サブドメインにも適用 |
| `preload` | ブラウザのプリロードリストに登録を希望 |

```
【HSTSの効果】

最初のアクセス（HSTS未設定時）:
  http://example.com → 301 → https://example.com
  ↑ この最初のHTTP通信が攻撃対象になり得る

HSTSが設定された後:
  ブラウザが自動的に https://example.com に変換
  → HTTP通信が発生しないため安全
```

> **実務でのポイント**: HSTSの `preload` ディレクティブを設定し、[hstspreload.org](https://hstspreload.org/) に登録すると、ブラウザに最初からHTTPS強制のリストが組み込まれます。これにより、初回アクセスからHTTPSが強制されます。

### curlでの確認

```bash
# HTTPでアクセスしてリダイレクトを確認
curl -v http://www.google.com 2>&1 | grep -E "Location|301"

# HSTSヘッダーを確認
curl -I https://www.google.com 2>&1 | grep -i strict
```

---

## 5.9 Mixed Content問題

Mixed Content（混在コンテンツ）とは、HTTPSのページ内でHTTPのリソースを読み込んでいる状態です。

```
https://example.com/page.html  ← HTTPS（安全）
  ├── <script src="https://cdn.example.com/app.js">  ← HTTPS ✅
  ├── <img src="http://images.example.com/photo.jpg"> ← HTTP ❌ Mixed Content!
  └── <link href="http://cdn.example.com/style.css">  ← HTTP ❌ Mixed Content!
```

### Mixed Contentの種類

| 種類 | 影響 | 例 |
|------|------|-----|
| **Active Mixed Content** | ブロック（読み込まれない） | `<script>`, `<iframe>`, CSS |
| **Passive Mixed Content** | 警告のみ（読み込まれる場合もある） | `<img>`, `<audio>`, `<video>` |

> **よくある間違い**: HTTPS化したのに、HTML内のリソースURLが `http://` のままになっているケース。すべてのリソースURLを `https://` または相対パス（`//cdn.example.com/...`）に変更する必要があります。

### 対策

```html
<!-- ❌ HTTPのまま -->
<img src="http://cdn.example.com/image.png">

<!-- ✅ HTTPSに変更 -->
<img src="https://cdn.example.com/image.png">

<!-- ✅ プロトコル相対URL（ページと同じプロトコルを使用） -->
<img src="//cdn.example.com/image.png">
```

**Content-Security-PolicyでMixed Contentをブロック:**

```
Content-Security-Policy: upgrade-insecure-requests
```

このヘッダーを設定すると、ブラウザが自動的にHTTPリクエストをHTTPSにアップグレードします。

---

## 5.10 実用例：ブラウザでの証明書の確認方法

### Chrome / Edgeでの確認

1. アドレスバーの**鍵アイコン**（🔒）をクリック
2. 「この接続は保護されています」をクリック
3. 「証明書は有効です」をクリック

### 確認できる情報

```
+------------------------------------------+
|  証明書ビューア                            |
|                                          |
|  発行先: www.example.com                  |
|  発行者: DigiCert SHA2 Extended           |
|          Validation Server CA             |
|  有効期間:                                |
|    開始: 2025/01/01                       |
|    終了: 2026/01/01                       |
|                                          |
|  フィンガープリント:                       |
|    SHA-256: AB:CD:EF:12:34:...           |
|                                          |
|  証明書チェーン:                           |
|    DigiCert Global Root G2  (ルートCA)    |
|    └─ DigiCert SHA2 ... CA  (中間CA)     |
|        └─ www.example.com   (サーバー)    |
+------------------------------------------+
```

### opensslコマンドでの確認

```bash
# 証明書の詳細を表示
openssl s_client -connect www.example.com:443 -showcerts < /dev/null 2>/dev/null | openssl x509 -text -noout

# 証明書チェーンを表示
openssl s_client -connect www.example.com:443 < /dev/null 2>/dev/null | grep -E "subject|issuer|verify"
```

### Pythonでの証明書情報取得

```python
import ssl
import socket
import pprint

# SSL証明書情報を取得
hostname = "www.example.com"
context = ssl.create_default_context()

with socket.create_connection((hostname, 443)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        cert = ssock.getpeercert()
        print(f"TLSバージョン: {ssock.version()}")
        print(f"\n--- 証明書情報 ---")
        pprint.pprint(cert)
```

---

## ポイントまとめ

1. HTTPには**盗聴・改ざん・なりすまし**の3つのリスクがある
2. **HTTPS = HTTP + TLS** で通信を暗号化する
3. TLSは**公開鍵暗号**（鍵交換）と**共通鍵暗号**（データ暗号化）を組み合わせている
4. **TLSハンドシェイク**で安全に鍵を交換し、暗号化通信を確立する
5. TLS 1.3はハンドシェイクが**1往復に短縮**され、より高速かつ安全
6. SSL証明書は**DV（ドメイン検証）、OV（組織検証）、EV（拡張検証）**の3種類
7. **認証局（CA）**が証明書を発行し、ルート証明書を起点とした**信頼チェーン**で検証する
8. **Let's Encrypt**で無料のDV証明書を取得・自動更新できる
9. HTTP→HTTPSの移行には**301リダイレクト**と**HSTS**を設定する
10. **Mixed Content**に注意し、すべてのリソースをHTTPSで読み込む
