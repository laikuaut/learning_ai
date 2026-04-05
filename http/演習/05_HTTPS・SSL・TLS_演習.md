# 第5章：HTTPS・SSL/TLS 演習問題

## 基本問題

### 問題5-1：HTTPの3つのリスク

HTTPによる通信にはセキュリティ上の3つの主要なリスクがあります。それぞれの名称と内容を答えてください。

<details>
<summary>解答</summary>

| リスク | 英語名 | 内容 |
|--------|--------|------|
| **盗聴** | Eavesdropping | 通信内容を第三者が読み取れる。パスワードやクレジットカード番号が漏洩する |
| **改ざん** | Tampering | 通信内容を途中で書き換えられる。振込先の変更や不正スクリプトの挿入が可能 |
| **なりすまし** | Spoofing | 偽のサーバーが本物のふりをする。フィッシングサイトなど |

HTTPSはTLSによる暗号化で**盗聴**を防ぎ、メッセージ認証コードで**改ざん**を検知し、証明書で**なりすまし**を防止します。

</details>

### 問題5-2：暗号方式の比較

共通鍵暗号と公開鍵暗号について、以下の表の空欄を埋めてください。

| 項目 | 共通鍵暗号 | 公開鍵暗号 |
|------|-----------|-----------|
| 使用する鍵の数 | (a) | (b) |
| 処理速度 | (c) | (d) |
| 鍵の配送問題 | (e) | (f) |
| 代表的なアルゴリズム | (g) | (h) |
| TLSでの用途 | (i) | (j) |

<details>
<summary>解答</summary>

| 項目 | 共通鍵暗号 | 公開鍵暗号 |
|------|-----------|-----------|
| 使用する鍵の数 | (a) **1つ**（送信者・受信者が同じ鍵） | (b) **2つ**（公開鍵と秘密鍵のペア） |
| 処理速度 | (c) **高速** | (d) **低速**（共通鍵の数百〜数千倍遅い） |
| 鍵の配送問題 | (e) **あり**（事前に安全な方法で共有が必要） | (f) **なし**（公開鍵は誰に知られても安全） |
| 代表的なアルゴリズム | (g) **AES** | (h) **RSA, ECDSA** |
| TLSでの用途 | (i) **データの暗号化**（実際の通信） | (j) **鍵の交換**（共通鍵の安全な受け渡し） |

</details>

### 問題5-3：SSL証明書の種類

以下のWebサイトに最も適切なSSL証明書の種類（DV, OV, EV）を選び、理由を説明してください。

1. 個人が運営する技術ブログ
2. 大手銀行のオンラインバンキング
3. 中規模企業のコーポレートサイト
4. 開発中のテスト環境

<details>
<summary>解答</summary>

1. **DV証明書** - 個人サイトではドメインの所有確認で十分です。Let's Encryptなどで無料で取得できます。

2. **EV証明書** - 金融機関は組織の法的存在を厳格に証明する必要があります。顧客の信頼を得るために最高レベルの検証が求められます。

3. **OV証明書** - 企業サイトでは組織の実在性を示すことが望ましいです。EV証明書ほどの厳格さは不要ですが、DVよりは信頼性が高くなります。

4. **DV証明書**（またはLet's Encrypt / 自己署名証明書） - テスト環境では暗号化が主目的であり、組織の検証は不要です。自己署名証明書でも構いません。

**補足**: 暗号化の強度はDV/OV/EVで変わりません。違いは「誰が運営しているか」の検証レベルです。

</details>

### 問題5-4：TLSバージョンの歴史

以下のTLS/SSLバージョンについて、使用を推奨するもの、非推奨のものをそれぞれ分類してください。

SSL 2.0 / SSL 3.0 / TLS 1.0 / TLS 1.1 / TLS 1.2 / TLS 1.3

<details>
<summary>解答</summary>

| 分類 | バージョン | 理由 |
|------|-----------|------|
| **非推奨** | SSL 2.0 | 深刻な脆弱性が多数存在 |
| **非推奨** | SSL 3.0 | POODLE攻撃などの脆弱性 |
| **非推奨** | TLS 1.0 | 2020年に主要ブラウザがサポート終了 |
| **非推奨** | TLS 1.1 | 2020年に主要ブラウザがサポート終了 |
| **推奨** | TLS 1.2 | 現在広く使用されており、安全 |
| **最も推奨** | TLS 1.3 | 最新版。ハンドシェイクが高速化され、弱い暗号スイートが排除されている |

</details>

## 応用問題

### 問題5-5：TLSハンドシェイクの理解

TLS 1.2のハンドシェイクについて、以下の問いに答えてください。

1. ハンドシェイクの主な目的を2つ挙げてください
2. ClientHelloメッセージに含まれる主要な情報を3つ挙げてください
3. なぜ公開鍵暗号ではなく共通鍵暗号でデータを暗号化するのですか？
4. TLS 1.3ではハンドシェイクがどのように改善されましたか？

<details>
<summary>解答</summary>

**1. ハンドシェイクの主な目的:**
- **サーバーの認証**: 証明書を検証して、接続先が本物のサーバーであることを確認する
- **共通鍵の安全な交換**: 以降のデータ暗号化に使う共通鍵（セッションキー）を安全に共有する

**2. ClientHelloに含まれる主要情報:**
- 対応するTLSバージョン（例: TLS 1.2）
- 対応する暗号スイートの一覧（例: TLS_AES_256_GCM_SHA384）
- クライアントランダム値（鍵生成に使用するランダムなバイト列）

**3. 共通鍵暗号でデータを暗号化する理由:**
- 公開鍵暗号は**処理速度が遅い**（共通鍵暗号の数百〜数千倍）
- 大量のデータを暗号化するには共通鍵暗号の方が効率的
- 公開鍵暗号は鍵の交換（安全に共通鍵を渡す）にのみ使い、実際のデータ暗号化には高速な共通鍵暗号を使う（ハイブリッド方式）

**4. TLS 1.3の改善:**
- ハンドシェイクが**2往復（2-RTT）から1往復（1-RTT）に短縮**
- ClientHelloと同時に鍵交換パラメータを送信する
- 弱い暗号スイートが排除され、安全なもののみが使用可能
- 0-RTT再接続に対応し、過去に接続したサーバーへの再接続がさらに高速化

</details>

### 問題5-6：HTTPS移行の計画

あなたのWebサイト `http://mysite.example.com` をHTTPS化することになりました。以下の手順を正しい順番に並べ、各手順で設定すべき具体的な内容を記述してください。

A. Mixed Content の修正
B. SSL証明書の取得とインストール
C. HSTSヘッダーの設定
D. HTTPからHTTPSへの301リダイレクト設定
E. HTTPS対応のテスト

<details>
<summary>解答</summary>

正しい順番: **B → A → E → D → C**

**B. SSL証明書の取得とインストール**
- Let's Encryptまたは商用CAからSSL証明書を取得
- Webサーバーに証明書と秘密鍵を設定
- ポート443でHTTPSを有効化

**A. Mixed Contentの修正**
- HTMLやCSS内のリソースURL（画像、スクリプト、スタイルシートなど）を `https://` に変更
- データベースに保存された `http://` URLも修正が必要な場合がある

**E. HTTPS対応のテスト**
- すべてのページがHTTPSで正しく表示されることを確認
- Mixed Contentの警告がないことを確認
- 証明書の有効性をブラウザやSSL Labsで確認

**D. HTTPからHTTPSへの301リダイレクト設定**
```
# テストが完了してからリダイレクトを有効化
HTTP/1.1 301 Moved Permanently
Location: https://mysite.example.com/（元のパス）
```

**C. HSTSヘッダーの設定**
```
# まず短いmax-ageで試して問題がないことを確認
Strict-Transport-Security: max-age=300

# 問題なければ期間を延長
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

**注意**: HSTSは一度設定すると取り消しが困難（ブラウザがmax-ageの間HTTPSを強制し続ける）なので、すべてのテストが完了してから最後に設定します。

</details>

### 問題5-7：証明書の信頼チェーン

以下のcurlコマンドの出力を見て、質問に答えてください。

```
* SSL connection using TLSv1.3 / TLS_AES_256_GCM_SHA384
* Server certificate:
*  subject: CN=www.example.com
*  start date: Jan  1 00:00:00 2025 GMT
*  expire date: Dec 31 23:59:59 2025 GMT
*  subjectAltName: host "www.example.com" matched cert's "www.example.com"
*  issuer: C=US; O=DigiCert Inc; CN=DigiCert Global G2 TLS RSA SHA256 2020 CA1
*  SSL certificate verify ok.
```

1. 使用されているTLSバージョンは何ですか？
2. 暗号スイートは何ですか？
3. 証明書の発行対象（サブジェクト）は何ですか？
4. 証明書の発行者（イシュア）は何ですか？
5. 証明書の有効期間はいつからいつまでですか？
6. 「SSL certificate verify ok」は何を意味しますか？

<details>
<summary>解答</summary>

1. **TLS 1.3** (`TLSv1.3`)

2. **TLS_AES_256_GCM_SHA384** - AES 256ビット鍵のGCMモードで暗号化し、SHA-384でメッセージ認証を行う暗号スイート

3. **www.example.com** (`CN=www.example.com`) - この証明書は `www.example.com` に対して発行されています

4. **DigiCert Global G2 TLS RSA SHA256 2020 CA1**（DigiCert社の中間認証局）

5. **2025年1月1日 00:00:00 GMT から 2025年12月31日 23:59:59 GMT まで**（約1年間）

6. 証明書の**信頼チェーンの検証に成功**したことを意味します。具体的には:
   - サーバー証明書の署名が中間CAで正しく検証された
   - 中間CA証明書がルートCA証明書で正しく検証された
   - ルートCA証明書がシステムの信頼リストに存在した
   - 証明書の有効期限内である
   - ドメイン名が一致している

</details>

## チャレンジ問題

### 問題5-8：Mixed Contentの修正

以下のHTMLにはMixed Contentの問題があります。問題箇所をすべて特定し、修正してください。また、Active Mixed ContentとPassive Mixed Contentを区別してください。

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Secure Site</title>
    <link rel="stylesheet" href="http://cdn.example.com/style.css">
    <script src="http://cdn.example.com/app.js"></script>
</head>
<body>
    <h1>Welcome</h1>
    <img src="http://images.example.com/logo.png" alt="Logo">
    <iframe src="http://widget.example.com/chat"></iframe>
    <a href="http://example.com/page">リンク</a>
    <video src="http://media.example.com/intro.mp4"></video>
</body>
</html>
```

<details>
<summary>ヒント</summary>

- Active Mixed Content: `<script>`, `<link rel="stylesheet">`, `<iframe>` など、ページの動作に影響するリソース
- Passive Mixed Content: `<img>`, `<video>`, `<audio>` など、表示に影響するリソース
- `<a href>` のリンクはMixed Contentではありません（クリックして遷移するだけなので）

</details>

<details>
<summary>解答</summary>

**問題箇所と分類:**

| 要素 | 種類 | ブラウザの動作 |
|------|------|-------------|
| `<link href="http://...style.css">` | **Active** Mixed Content | ブロックされる |
| `<script src="http://...app.js">` | **Active** Mixed Content | ブロックされる |
| `<img src="http://...logo.png">` | **Passive** Mixed Content | 警告（読み込まれる場合もある） |
| `<iframe src="http://...chat">` | **Active** Mixed Content | ブロックされる |
| `<a href="http://...">` | **Mixed Contentではない** | 問題なし（通常のリンク） |
| `<video src="http://...mp4">` | **Passive** Mixed Content | 警告（読み込まれる場合もある） |

**修正後:**

```html
<!DOCTYPE html>
<html>
<head>
    <title>My Secure Site</title>
    <link rel="stylesheet" href="https://cdn.example.com/style.css">
    <script src="https://cdn.example.com/app.js"></script>
</head>
<body>
    <h1>Welcome</h1>
    <img src="https://images.example.com/logo.png" alt="Logo">
    <iframe src="https://widget.example.com/chat"></iframe>
    <a href="https://example.com/page">リンク</a>
    <video src="https://media.example.com/intro.mp4"></video>
</body>
</html>
```

**追加対策**: サーバー側でCSPヘッダーを設定し、自動アップグレードを有効にすることもできます。

```
Content-Security-Policy: upgrade-insecure-requests
```

</details>

### 問題5-9：Pythonで証明書情報を取得

Pythonの `ssl` モジュールと `socket` モジュールを使って、`www.google.com` のSSL証明書から以下の情報を取得・表示するプログラムを作成してください。

- TLSバージョン
- 証明書の発行先（subject）
- 証明書の発行者（issuer）
- 証明書の有効期限（notAfter）

<details>
<summary>ヒント</summary>

- `ssl.create_default_context()` でSSLコンテキストを作成します
- `context.wrap_socket()` でSSL接続を確立します
- `ssock.getpeercert()` で証明書情報を辞書形式で取得できます
- `ssock.version()` でTLSバージョンを取得できます

</details>

<details>
<summary>解答</summary>

```python
import ssl
import socket

hostname = "www.google.com"
port = 443

# SSLコンテキストの作成
context = ssl.create_default_context()

# TCP接続を確立し、SSLでラップする
with socket.create_connection((hostname, port)) as sock:
    with context.wrap_socket(sock, server_hostname=hostname) as ssock:
        # TLSバージョン
        print(f"TLSバージョン: {ssock.version()}")

        # 証明書情報の取得
        cert = ssock.getpeercert()

        # 発行先（subject）
        subject = dict(x[0] for x in cert["subject"])
        print(f"発行先 (Subject): {subject.get('commonName', 'N/A')}")

        # 発行者（issuer）
        issuer = dict(x[0] for x in cert["issuer"])
        print(f"発行者 (Issuer): {issuer.get('organizationName', 'N/A')} - {issuer.get('commonName', 'N/A')}")

        # 有効期限
        print(f"有効期限開始 (Not Before): {cert['notBefore']}")
        print(f"有効期限終了 (Not After): {cert['notAfter']}")

        # SAN（Subject Alternative Name）
        san = cert.get("subjectAltName", [])
        print(f"\nSAN (Subject Alternative Name):")
        for type_name, value in san[:5]:  # 最初の5件のみ表示
            print(f"  {type_name}: {value}")
        if len(san) > 5:
            print(f"  ... 他 {len(san) - 5} 件")
```

**実行結果の例:**

```
TLSバージョン: TLSv1.3
発行先 (Subject): www.google.com
発行者 (Issuer): Google Trust Services - WR2
有効期限開始 (Not Before): Mar 10 08:36:10 2026 GMT
有効期限終了 (Not After): Jun  2 08:36:09 2026 GMT

SAN (Subject Alternative Name):
  DNS: www.google.com
```

</details>
