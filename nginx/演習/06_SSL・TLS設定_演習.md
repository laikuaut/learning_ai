# 第6章：SSL/TLS設定 - 演習問題

---

## 問題1：基本的なSSL設定（基本）

Let's Encrypt で取得した証明書を使って、`example.com` にHTTPSでアクセスできるNginx設定を作成してください。

**要件：**
- ポート443でSSLを有効にする
- 証明書パスは `/etc/letsencrypt/live/example.com/` 配下
- ドキュメントルートは `/var/www/example.com`

<details>
<summary>ヒント</summary>

`listen 443 ssl;` でSSLを有効にし、`ssl_certificate` に `fullchain.pem`、`ssl_certificate_key` に `privkey.pem` を指定します。

</details>

<details>
<summary>解答例</summary>

```nginx
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name example.com;

    # SSL 証明書（フルチェーン：サーバー証明書 + 中間証明書）
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

**補足**: `ssl_certificate` には `fullchain.pem` を使います。`cert.pem`（サーバー証明書のみ）を使うと、中間証明書が欠けて一部のクライアントで証明書エラーが発生します。

</details>

---

## 問題2：HTTP→HTTPS リダイレクト（基本）

HTTPでアクセスされた場合にHTTPSに301リダイレクトする設定を追加してください。

**要件：**
- `http://example.com/任意のパス` → `https://example.com/任意のパス`
- `http://www.example.com/任意のパス` → `https://example.com/任意のパス`
- パスとクエリパラメータを維持する

**期待される動作：**
```
http://example.com/about?id=1 → https://example.com/about?id=1 (301)
http://www.example.com/contact → https://example.com/contact (301)
```

<details>
<summary>ヒント</summary>

HTTPのserver ブロック（ポート80）で `return 301 https://example.com$request_uri;` を使います。`$request_uri` にはパスとクエリパラメータが含まれます。

</details>

<details>
<summary>解答例</summary>

```nginx
# HTTP → HTTPS リダイレクト
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    # すべてのリクエストをHTTPSの example.com にリダイレクト
    # $request_uri にはパスとクエリパラメータが含まれる
    return 301 https://example.com$request_uri;
}

# HTTPS メインサーバー
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**補足**: `$host` ではなく `example.com` をハードコードすることで、`www.example.com` でのアクセスも `example.com` にリダイレクトされます（wwwなしに統一）。

</details>

---

## 問題3：TLSバージョンと暗号スイートの設定（基本）

以下のセキュリティ要件を満たすSSL設定を作成してください。

**要件：**
- TLS 1.2 と TLS 1.3 のみを許可
- 安全な暗号スイートのみを使用
- DHパラメータファイルは `/etc/nginx/dhparam.pem`

<details>
<summary>ヒント</summary>

`ssl_protocols` でTLSバージョンを指定し、`ssl_ciphers` で暗号スイートを指定します。`ssl_dhparam` でDHパラメータファイルを指定します。

</details>

<details>
<summary>解答例</summary>

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # TLS 1.2 と 1.3 のみ許可（1.0, 1.1 は脆弱性があるため無効化）
    ssl_protocols TLSv1.2 TLSv1.3;

    # 安全な暗号スイート（Mozilla Intermediate 準拠）
    ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;

    # TLS 1.3 ではクライアントの暗号スイート優先順位を使うのが推奨
    ssl_prefer_server_ciphers off;

    # DH パラメータ
    ssl_dhparam /etc/nginx/dhparam.pem;

    root /var/www/example.com;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**DHパラメータの生成コマンド:**
```bash
sudo openssl dhparam -out /etc/nginx/dhparam.pem 2048
```

</details>

---

## 問題4：HSTS の設定（応用）

HSTS を設定してください。ただし、段階的に導入する方針で設定してください。

**ステップ1（テスト）:** max-age を5分（300秒）に設定
**ステップ2（確認後）:** max-age を1年（31536000秒）に設定し、サブドメインにも適用

それぞれの設定を記述し、なぜ段階的に導入するのか理由も説明してください。

<details>
<summary>ヒント</summary>

`add_header Strict-Transport-Security` で設定します。`max-age` の値を段階的に大きくし、`includeSubDomains` はステップ2で追加します。段階的に導入する理由は、HSTSの設定ミスの影響を最小限にするためです。

</details>

<details>
<summary>解答例</summary>

**ステップ1（テスト期間）:**
```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # HSTS テスト（max-age: 5分）
    add_header Strict-Transport-Security "max-age=300" always;

    root /var/www/example.com;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

**ステップ2（本番導入後）:**
```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # HSTS 本番設定（max-age: 1年、サブドメインも対象）
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    root /var/www/example.com;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

**段階的に導入する理由:**
1. HSTSを設定すると、max-age で指定した期間中はブラウザがHTTPアクセスを拒否します
2. SSL設定に不備がある場合、サイトにアクセスできなくなります
3. 短い max-age でテストすれば、問題があっても5分後に元に戻せます
4. `includeSubDomains` を先に付けると、SSLが設定されていないサブドメインにもアクセスできなくなります
5. `preload` でプリロードリストに登録すると、取り消しに数か月かかります

</details>

---

## 問題5：OCSP Stapling の設定（応用）

OCSP Stapling を有効にする設定を作成し、正しく動作しているか確認するコマンドも記載してください。

<details>
<summary>ヒント</summary>

`ssl_stapling on;` と `ssl_stapling_verify on;` で有効化し、`ssl_trusted_certificate` で信頼チェーンを指定します。確認には `openssl s_client` コマンドを使います。

</details>

<details>
<summary>解答例</summary>

```nginx
server {
    listen 443 ssl;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;

    # OCSP レスポンスの検証用チェーン（中間証明書）
    ssl_trusted_certificate /etc/letsencrypt/live/example.com/chain.pem;

    # DNS リゾルバ（OCSP レスポンダへの問い合わせに使用）
    resolver 8.8.8.8 8.8.4.4 valid=300s;
    resolver_timeout 5s;

    root /var/www/example.com;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

**確認コマンド:**
```bash
# OCSP Stapling の動作確認
# "OCSP Response Status: successful" と表示されれば正常
echo | openssl s_client -connect example.com:443 -servername example.com -status 2>/dev/null | grep -A 3 "OCSP Response"

# 期待される出力:
# OCSP Response Status: successful (0x0)
# OCSP Response Data:
#     OCSP Response Status: successful (0x0)
#     Response Type: Basic OCSP Response
```

**補足**: Nginx起動直後はOCSPレスポンスがまだキャッシュされていないため、確認に失敗する場合があります。最初のHTTPSリクエスト後に再度確認してください。

</details>

---

## 問題6：セキュリティヘッダーの設定（応用）

以下のセキュリティヘッダーをすべて設定してください。各ヘッダーが何を防ぐのかコメントで説明を付けてください。

- HSTS
- X-Frame-Options
- X-Content-Type-Options
- X-XSS-Protection
- Referrer-Policy

<details>
<summary>ヒント</summary>

各ヘッダーは `add_header` ディレクティブで設定します。`always` パラメータを付けると、エラーレスポンスにもヘッダーが付与されます。

</details>

<details>
<summary>解答例</summary>

```nginx
server {
    listen 443 ssl http2;
    server_name example.com;

    ssl_certificate     /etc/letsencrypt/live/example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/example.com/privkey.pem;

    # --- セキュリティヘッダー ---

    # HSTS: ブラウザにHTTPS接続を強制する
    # max-age=63072000（2年間）、サブドメインにも適用
    add_header Strict-Transport-Security "max-age=63072000; includeSubDomains; preload" always;

    # X-Frame-Options: クリックジャッキング攻撃を防止
    # DENY = iframe での埋め込みを完全に禁止
    # SAMEORIGIN にすると同一オリジンからのiframeのみ許可
    add_header X-Frame-Options DENY always;

    # X-Content-Type-Options: MIMEタイプスニッフィングを防止
    # ブラウザがContent-Typeを勝手に推測するのを防ぐ
    add_header X-Content-Type-Options nosniff always;

    # X-XSS-Protection: ブラウザ組み込みのXSSフィルターを有効化
    # mode=block: XSSが検出されたらページの表示をブロック
    # ※ 最新ブラウザではCSPで代替されるが、レガシー対策として設定
    add_header X-XSS-Protection "1; mode=block" always;

    # Referrer-Policy: リファラー情報の送信を制御
    # strict-origin-when-cross-origin:
    #   同一オリジン → フルURL、クロスオリジン → オリジンのみ、
    #   HTTPS→HTTP → 送信しない
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    root /var/www/example.com;
    location / {
        try_files $uri $uri/ =404;
    }
}
```

**確認コマンド:**
```bash
# レスポンスヘッダーの確認
curl -I https://example.com

# 期待される出力（抜粋）:
# Strict-Transport-Security: max-age=63072000; includeSubDomains; preload
# X-Frame-Options: DENY
# X-Content-Type-Options: nosniff
# X-XSS-Protection: 1; mode=block
# Referrer-Policy: strict-origin-when-cross-origin
```

</details>

---

## 問題7：Let's Encrypt 証明書の取得と自動更新（チャレンジ）

新しいサーバーに Let's Encrypt の証明書を導入する手順を、コマンドと設定の両方を含めて記述してください。

**要件：**
- ドメイン: `myapp.example.com`
- Certbot の Nginx プラグインを使用
- 自動更新を設定し、更新後にNginxをリロードする
- 自動更新のテストを実行する

<details>
<summary>ヒント</summary>

Certbot のインストール → 証明書取得 → 自動更新の確認、という流れです。更新後のNginxリロードは `--deploy-hook` オプションで設定します。

</details>

<details>
<summary>解答例</summary>

```bash
# ===== 1. Certbot のインストール =====
sudo apt update
sudo apt install certbot python3-certbot-nginx

# ===== 2. 事前にNginxの基本設定を作成 =====
# /etc/nginx/sites-available/myapp.example.com
```

```nginx
# 初期設定（HTTP のみ・Certbot が書き換える前）
server {
    listen 80;
    listen [::]:80;
    server_name myapp.example.com;
    root /var/www/myapp;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

```bash
# 有効化
sudo ln -s /etc/nginx/sites-available/myapp.example.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# ===== 3. 証明書の取得 =====
# --nginx: Nginx設定を自動で書き換え
# -d: 対象ドメイン
# --agree-tos: 利用規約に同意
# --email: 通知用メールアドレス
sudo certbot --nginx \
    -d myapp.example.com \
    --agree-tos \
    --email admin@example.com

# ===== 4. 自動更新の設定確認 =====
# Certbot はインストール時にsystemdタイマーが自動設定される
sudo systemctl status certbot.timer

# ===== 5. 更新後にNginxをリロードする設定 =====
# /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh を作成
sudo tee /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh > /dev/null << 'EOF'
#!/bin/bash
# 証明書更新後にNginxをリロード
systemctl reload nginx
EOF
sudo chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-nginx.sh

# ===== 6. 自動更新のテスト（実際には更新しない） =====
sudo certbot renew --dry-run

# 期待される出力:
# Congratulations, all simulated renewals succeeded:
#   /etc/letsencrypt/live/myapp.example.com/fullchain.pem (success)

# ===== 7. 証明書の有効期限確認 =====
sudo certbot certificates
```

**Certbot が自動生成するNginx設定（参考）:**
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name myapp.example.com;

    # Certbot が追加するリダイレクト設定
    if ($host = myapp.example.com) {
        return 301 https://$host$request_uri;
    }
    return 404;
}

server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name myapp.example.com;

    root /var/www/myapp;
    index index.html;

    # Certbot が追加するSSL設定
    ssl_certificate /etc/letsencrypt/live/myapp.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/myapp.example.com/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**補足**: Certbot の `--nginx` プラグインは設定を自動で書き換えてくれますが、手動で細かくカスタマイズしたい場合は `certonly` モードで証明書だけ取得し、自分でNginx設定を書く方法もあります。

</details>

---

## 問題8：本番環境の完全SSL設定（チャレンジ）

以下の要件をすべて満たす、本番環境で使える完全なSSL設定を作成してください。

**要件：**
- ドメイン: `secure.example.com`
- HTTP → HTTPS リダイレクト（301）
- TLS 1.2 / 1.3 のみ
- 安全な暗号スイート（Mozilla Intermediate 準拠）
- HSTS（1年間、サブドメイン含む）
- OCSP Stapling
- セッションキャッシュ（10MB、有効期間1日）
- セキュリティヘッダー（X-Frame-Options, X-Content-Type-Options, Referrer-Policy）
- HTTP/2 有効
- SSL共通設定は別ファイルに分離

**評価基準：SSL Labs で A+ を取得できる設定であること**

<details>
<summary>ヒント</summary>

SSL共通設定を `/etc/nginx/snippets/ssl-params.conf` 等に分離し、各server ブロックで `include` します。HTTP/2は `listen 443 ssl http2;` で有効化します。A+ を取得するにはHSTSが必須です。

</details>

<details>
<summary>解答例</summary>

**SSL共通設定: `/etc/nginx/snippets/ssl-params.conf`**
```nginx
# --- TLS バージョンと暗号スイート ---
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-ECDSA-CHACHA20-POLY1305:ECDHE-RSA-CHACHA20-POLY1305:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384;
ssl_prefer_server_ciphers off;

# --- DH パラメータ ---
ssl_dhparam /etc/nginx/dhparam.pem;

# --- セッションキャッシュ ---
ssl_session_cache shared:SSL:10m;
ssl_session_timeout 1d;
ssl_session_tickets off;

# --- OCSP Stapling ---
ssl_stapling on;
ssl_stapling_verify on;
resolver 8.8.8.8 8.8.4.4 valid=300s;
resolver_timeout 5s;

# --- セキュリティヘッダー ---
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
add_header X-Frame-Options DENY always;
add_header X-Content-Type-Options nosniff always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
```

**サイト設定: `/etc/nginx/sites-available/secure.example.com`**
```nginx
# HTTP → HTTPS リダイレクト
server {
    listen 80;
    listen [::]:80;
    server_name secure.example.com;
    return 301 https://secure.example.com$request_uri;
}

# HTTPS メインサーバー
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name secure.example.com;

    # SSL 証明書
    ssl_certificate     /etc/letsencrypt/live/secure.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/secure.example.com/privkey.pem;
    ssl_trusted_certificate /etc/letsencrypt/live/secure.example.com/chain.pem;

    # SSL 共通設定を読み込み
    include snippets/ssl-params.conf;

    # ドキュメントルート
    root /var/www/secure.example.com/public;
    index index.html;

    access_log /var/log/nginx/secure.example.com.access.log;
    error_log  /var/log/nginx/secure.example.com.error.log;

    # 静的ファイルのキャッシュ
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg|woff2?)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # メインコンテンツ
    location / {
        try_files $uri $uri/ =404;
    }

    # 隠しファイルへのアクセスを拒否
    location ~ /\. {
        deny all;
    }
}
```

**セットアップ手順:**
```bash
# 1. DH パラメータの生成
sudo openssl dhparam -out /etc/nginx/dhparam.pem 2048

# 2. SSL共通設定ファイルの配置
sudo mkdir -p /etc/nginx/snippets
sudo nano /etc/nginx/snippets/ssl-params.conf

# 3. サイト設定ファイルの作成と有効化
sudo nano /etc/nginx/sites-available/secure.example.com
sudo ln -s /etc/nginx/sites-available/secure.example.com /etc/nginx/sites-enabled/

# 4. Let's Encrypt 証明書の取得
sudo certbot certonly --nginx -d secure.example.com

# 5. 設定テストとリロード
sudo nginx -t && sudo systemctl reload nginx

# 6. SSL Labs でテスト
# https://www.ssllabs.com/ssltest/analyze.html?d=secure.example.com

# 7. セキュリティヘッダーの確認
curl -I https://secure.example.com
```

**SSL Labs で A+ を取得するためのチェックポイント:**
- TLS 1.0, 1.1 が無効であること → A 以上
- HSTS が設定されていること → A+ の必須条件
- 安全な暗号スイートのみを使用していること
- Forward Secrecy（前方秘匿性）に対応した暗号を使用していること

</details>
