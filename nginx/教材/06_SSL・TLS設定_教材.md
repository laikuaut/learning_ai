# 第6章：SSL/TLS設定

> **この章のゴール**: NginxでHTTPS通信を設定し、安全なWebサイトを構築できるようになる。
> SSL/TLSの仕組みから、Let's Encryptによる無料証明書の取得、セキュリティ強化設定まで理解し、本番環境で使えるSSL設定を作成できるようになります。

---

## なぜSSL/TLS設定を学ぶのか？

現在のWebでは、HTTPS（暗号化通信）は**必須**です。

- Google Chromeは、HTTPサイトに「保護されていない通信」と警告を表示します
- Google検索のランキング要因にHTTPSが含まれています
- HTTP/2はHTTPSでしか使えません（事実上）
- Cookie、パスワード、個人情報などの通信内容を暗号化で保護します

```
HTTP（暗号化なし）:
  クライアント ──── パスワード: abc123 ──── サーバー
                   ↑ 盗聴可能！

HTTPS（暗号化あり）:
  クライアント ──── x8Kj2$mP... ──── サーバー
                   ↑ 暗号化されているので盗聴されても解読不能
```

---

## 6.1 HTTPS の仕組み（SSL/TLS ハンドシェイク）

### SSL と TLS の関係

**SSL（Secure Sockets Layer）** は古いプロトコルで、現在は使用が非推奨です。**TLS（Transport Layer Security）** がSSLの後継プロトコルです。日常では「SSL」と呼ばれることが多いですが、実際に使われているのはTLSです。

| バージョン | 状態 |
|---|---|
| SSL 2.0, 3.0 | 非推奨（脆弱性あり） |
| TLS 1.0, 1.1 | 非推奨（2020年以降、主要ブラウザで無効化） |
| TLS 1.2 | 現在も広く使用 |
| TLS 1.3 | 最新・推奨（より高速・安全） |

### TLS ハンドシェイクの流れ

```
クライアント                          サーバー
    │                                  │
    │── 1. Client Hello ──────────────▶│  対応するTLSバージョン・暗号スイートを送信
    │                                  │
    │◀─ 2. Server Hello ──────────────│  使用するTLSバージョン・暗号スイートを返信
    │◀─ 3. 証明書 ────────────────────│  SSL証明書を送信
    │◀─ 4. Server Hello Done ─────────│
    │                                  │
    │── 5. 鍵交換 ────────────────────▶│  共通鍵の素材を交換
    │── 6. Change Cipher Spec ────────▶│  暗号化開始を宣言
    │── 7. Finished ──────────────────▶│
    │                                  │
    │◀─ 8. Change Cipher Spec ────────│
    │◀─ 9. Finished ──────────────────│
    │                                  │
    │◀═══ 暗号化された通信 ══════════▶│  以降、すべてのデータが暗号化される
```

> **📖 ポイント**: TLS 1.3ではハンドシェイクが簡略化され、1-RTT（1回の往復）で接続が確立します。TLS 1.2の2-RTTより高速です。

---

## 6.2 SSL証明書の種類と取得方法

### SSL証明書の種類

| 種類 | 正式名称 | 検証内容 | 費用 | 用途 |
|---|---|---|---|---|
| **DV** | Domain Validation | ドメインの所有権のみ | 無料〜低額 | 個人サイト、ブログ |
| **OV** | Organization Validation | ドメイン + 組織の実在確認 | 中程度 | 企業サイト |
| **EV** | Extended Validation | ドメイン + 組織の厳格な審査 | 高額 | 金融機関、EC大手 |

### ワイルドカード証明書

`*.example.com` のように、サブドメイン全てに対応する証明書です。

```
通常の証明書:
  example.com        ✓
  www.example.com    ✗（別途証明書が必要）
  blog.example.com   ✗

ワイルドカード証明書（*.example.com）:
  example.com        ✗（別途必要な場合あり）
  www.example.com    ✓
  blog.example.com   ✓
  api.example.com    ✓
```

---

## 6.3 Let's Encrypt と Certbot による無料証明書

### Let's Encrypt とは

**Let's Encrypt** は、無料でDV証明書を発行する認証局（CA: Certificate Authority）です。自動更新に対応しており、個人から企業まで広く利用されています。

### Certbot のインストールと証明書取得

```bash
# Certbot のインストール（Ubuntu/Debian）
sudo apt update
sudo apt install certbot python3-certbot-nginx

# 証明書の取得（Nginxプラグイン使用）
# Nginx設定を自動で書き換えてくれる
sudo certbot --nginx -d example.com -d www.example.com

# 対話なしで取得する場合
sudo certbot --nginx \
    -d example.com \
    -d www.example.com \
    --non-interactive \
    --agree-tos \
    --email admin@example.com
```

### 証明書ファイルの保存場所

```
/etc/letsencrypt/live/example.com/
├── fullchain.pem    # SSL証明書（中間証明書を含む）
├── privkey.pem      # 秘密鍵
├── cert.pem         # サーバー証明書のみ
└── chain.pem        # 中間証明書のみ
```

### 自動更新の設定

Let's Encrypt の証明書は90日間有効です。Certbot はsystemdタイマーで自動更新を行います。

```bash
# 自動更新のテスト（実際には更新せず、手順を確認）
sudo certbot renew --dry-run

# systemd タイマーの確認
sudo systemctl status certbot.timer

# 手動更新が必要な場合
sudo certbot renew
```

> **📖 ポイント**: Certbot の `--nginx` プラグインを使うと、Nginxの設定ファイルを自動で書き換えてくれます。手動でSSL設定を書く場合は `certonly` コマンドで証明書だけを取得します。

---

## 6.4 ssl_certificate / ssl_certificate_key の設定

### 基本的なSSL設定

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    # SSL証明書（中間証明書を含むフルチェーン）
    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;

    # 秘密鍵
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

### 証明書チェーンの仕組み

```
ルート認証局（Root CA）
  │  ルート証明書（ブラウザにプリインストール済み）
  │
  ├── 中間認証局（Intermediate CA）
  │     │  中間証明書
  │     │
  │     └── あなたのサーバー証明書
  │           example.com
  │
  ↓
  fullchain.pem = サーバー証明書 + 中間証明書
```

> **⚠️ よくある間違い**: `ssl_certificate` にサーバー証明書のみ（`cert.pem`）を指定すると、中間証明書が欠けてしまい、一部のブラウザやデバイスで証明書エラーが発生します。必ず `fullchain.pem` を使いましょう。

---

## 6.5 HTTP→HTTPS リダイレクト（301）

HTTPでアクセスされた場合、HTTPSに自動リダイレクトする設定です。

```nginx
# HTTP → HTTPS リダイレクト
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    # 全リクエストをHTTPSにリダイレクト（301 = 恒久的な移転）
    return 301 https://$host$request_uri;
}

# HTTPS サーバー
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name example.com www.example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

> **📖 ポイント**: `301`（Moved Permanently）を使うと、ブラウザがリダイレクトをキャッシュし、次回以降は直接HTTPSにアクセスします。テスト中は `302`（一時的なリダイレクト）を使い、確認が取れたら `301` に変更するのが安全です。

---

## 6.6 SSL プロトコルと暗号スイートの設定

### TLS バージョンの指定

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # TLS 1.2 と TLS 1.3 のみ許可（1.0, 1.1 は脆弱性があるため無効化）
    ssl_protocols TLSv1.2 TLSv1.3;
}
```

### 暗号スイート（Cipher Suite）の設定

暗号スイートは、暗号化に使うアルゴリズムの組み合わせです。

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    ssl_protocols TLSv1.2 TLSv1.3;

    # 強力な暗号スイートのみを使用
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;

    # サーバー側の暗号スイート優先順位を使用
    ssl_prefer_server_ciphers off;
}
```

> **📖 ポイント**: TLS 1.3では暗号スイートがプロトコル側で固定されるため、`ssl_ciphers` の設定は TLS 1.2の接続にのみ影響します。TLS 1.3のみをサポートするなら `ssl_ciphers` は不要です。

### DH パラメータ

```bash
# DH パラメータの生成（一度だけ実行）
sudo openssl dhparam -out /etc/nginx/dhparam.pem 2048
```

```nginx
# DH パラメータの指定
ssl_dhparam /etc/nginx/dhparam.pem;
```

---

## 6.7 HSTS（HTTP Strict Transport Security）

### HSTS とは

**HSTS（HTTP Strict Transport Security）** は、ブラウザに「このサイトへは必ずHTTPSでアクセスしろ」と指示するセキュリティ機能です。

```
HSTS なし:
  ユーザー → http://example.com → 301 リダイレクト → https://example.com
  ↑ 最初のHTTPリクエストが中間者攻撃（MITM）の対象になりうる

HSTS あり:
  ユーザー → ブラウザが自動的に → https://example.com
  ↑ HTTP リクエストが発生しない（ブラウザが変換）
```

### HSTS の設定

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # HSTS ヘッダーを追加
    # max-age=31536000  : 1年間（秒）
    # includeSubDomains : サブドメインにも適用
    # preload           : ブラウザのHSTSプリロードリストへの登録用
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
}
```

> **⚠️ よくある間違い**: HSTSを設定すると、`max-age` で指定した期間中はHTTPに戻せなくなります。最初は短い `max-age`（例: 300秒）でテストし、問題なければ徐々に延ばしましょう。`preload` を付けてプリロードリストに登録すると、取り消しに数か月かかる場合があります。

---

## 6.8 OCSP Stapling

### OCSP Stapling とは

**OCSP（Online Certificate Status Protocol）** は、証明書が失効していないかを確認するプロトコルです。通常はクライアントが認証局に問い合わせますが、**OCSP Stapling** ではサーバーが代わりに問い合わせ結果をキャッシュし、クライアントに提供します。

```
OCSP Stapling なし:
  クライアント → 認証局に問い合わせ → 証明書の有効性を確認 → サーバーに接続
  ↑ 余分な通信が発生（レイテンシ増加）

OCSP Stapling あり:
  サーバー → 認証局に定期的に問い合わせ → 結果をキャッシュ
  クライアント → サーバーが証明書と一緒にOCSPレスポンスを返す
  ↑ 余分な通信が不要（高速）
```

### OCSP Stapling の設定

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # OCSP Stapling を有効化
    ssl_stapling on;
    ssl_stapling_verify on;

    # OCSPレスポンスの検証に使う信頼された証明書チェーン
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

    # DNS リゾルバの指定（OCSPレスポンダへの問い合わせに使用）
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;
}
```

---

## 6.9 SSL設定のセキュリティ強化

### Mozilla SSL Configuration Generator 準拠の設定

Mozilla が公開している [SSL Configuration Generator](https://ssl-config.mozilla.org/) は、安全なSSL設定のテンプレートを提供しています。以下は「中間（Intermediate）」レベルの設定です。

```nginx
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # TLS バージョン
    ssl_protocols TLSv1.2 TLSv1.3;

    # 暗号スイート（TLS 1.2 用）
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;

    # DH パラメータ
    ssl_dhparam /etc/nginx/dhparam.pem;

    # SSL セッションキャッシュ
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 1d;
    ssl_session_tickets off;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    # セキュリティヘッダー
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```

### SSL セッションキャッシュ

SSLハンドシェイクはCPU負荷が高いため、セッション情報をキャッシュして再接続を高速化します。

```nginx
# 共有メモリキャッシュ（10MB で約40,000セッションを保存）
ssl_session_cache shared:SSL:10m;

# セッションの有効期間
ssl_session_timeout 1d;

# セッションチケットの無効化（Perfect Forward Secrecy のため）
ssl_session_tickets off;
```

> **📖 ポイント**: `ssl_session_tickets off` は **Perfect Forward Secrecy（PFS: 前方秘匿性）** を確保するための設定です。セッションチケットのキーが漏洩した場合、過去の通信が復号されるリスクがあるため、セキュリティを重視する場合は無効にします。

### セキュリティヘッダー一覧

| ヘッダー | 目的 |
|---|---|
| `Strict-Transport-Security` | HTTPS強制（HSTS） |
| `X-Frame-Options` | クリックジャッキング防止（iframe埋め込みの制御） |
| `X-Content-Type-Options` | MIMEタイプスニッフィング防止 |
| `X-XSS-Protection` | XSSフィルター有効化（レガシーブラウザ向け） |
| `Referrer-Policy` | リファラー情報の送信制御 |
| `Content-Security-Policy` | コンテンツの読み込み元を制御 |

---

## 6.10 実用例：本番環境のSSL設定テンプレート

### 完全な設定例

以下は、本番環境で実際に使える完全なSSL設定テンプレートです。

**SSL共通設定: `/etc/nginx/conf.d/ssl-common.conf`**

```nginx
# TLS バージョン
ssl_protocols TLSv1.2 TLSv1.3;

# 暗号スイート
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;

# DH パラメータ
ssl_dhparam /etc/nginx/dhparam.pem;

# セッションキャッシュ
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# OCSP Stapling
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;
```

**セキュリティヘッダー共通設定: `/etc/nginx/conf.d/security-headers.conf`**

```nginx
add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;
add_header X-Frame-Options DENY always;
add_header X-Content-Type-Options nosniff always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

**サイト設定: `/etc/nginx/sites-available/example.com`**

```nginx
# HTTP → HTTPS リダイレクト
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;
    return 301 https://example.com$request_uri;
}

# www → non-www リダイレクト（HTTPS）
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name www.example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

    return 301 https://example.com$request_uri;
}

# メインサイト
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name example.com;

    # SSL 証明書
    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

    # SSL 共通設定とセキュリティヘッダーを読み込み
    include conf.d/ssl-common.conf;
    include conf.d/security-headers.conf;

    # ドキュメントルート
    root /var/www/example.com/public;
    index index.html;

    access_log /var/log/nginx/example.com.access.log;
    error_log  /var/log/nginx/example.com.error.log;

    # 静的ファイル
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    location / {
        try_files $uri $uri/ =404;
    }

    # 隠しファイルへのアクセスを拒否
    location ~ /\. {
        deny all;
    }
}
```

### SSL設定の動作確認

```bash
# Nginx 設定のテスト
sudo nginx -t

# Nginx のリロード
sudo systemctl reload nginx

# SSL証明書の確認
echo | openssl s_client -connect example.com:443 -servername example.com 2>/dev/null | openssl x509 -noout -dates

# SSL 設定のテスト（SSL Labs のコマンドライン版）
# ブラウザで https://www.ssllabs.com/ssltest/ にアクセスしてテストも可能
curl -I https://example.com
```

### SSL設定のチェックリスト

```
□ TLS 1.0, 1.1 を無効化しているか
□ 強力な暗号スイートのみを許可しているか
□ HTTP → HTTPS リダイレクトが設定されているか
□ HSTS ヘッダーが設定されているか
□ OCSP Stapling が有効か
□ ssl_certificate に fullchain.pem を使っているか
□ 証明書の自動更新が設定されているか
□ セキュリティヘッダーが適切に設定されているか
□ SSL Labs で A 以上の評価を取得しているか
```

---

## ポイントまとめ

| 項目 | 内容 |
|---|---|
| SSL/TLS | 通信を暗号化するプロトコル。TLS 1.2 以上を使用する |
| 証明書の種類 | DV（ドメイン検証）、OV（組織検証）、EV（拡張検証） |
| Let's Encrypt | 無料のDV証明書を発行する認証局。Certbot で自動取得・更新 |
| ssl_certificate | 証明書ファイル。fullchain.pem（中間証明書含む）を使う |
| HTTP→HTTPS | 301リダイレクトで全通信をHTTPSに誘導する |
| HSTS | ブラウザに「必ずHTTPSでアクセスせよ」と指示するヘッダー |
| OCSP Stapling | サーバーが証明書の有効性を代理確認し、パフォーマンスを向上させる |
| セッションキャッシュ | TLSハンドシェイクの結果をキャッシュし、再接続を高速化する |
| セキュリティヘッダー | HSTS, X-Frame-Options, X-Content-Type-Options などで追加防御 |

> **次の章では**: Nginxのキャッシュ設定について学びます。プロキシキャッシュやブラウザキャッシュを活用して、Webサイトのパフォーマンスを向上させる方法を理解します。
