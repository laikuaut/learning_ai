# 第3章：バーチャルホストとServer Block - 演習問題

---

## 問題1：基本的なserver ブロックの作成（基本）

`mysite.local` というドメインに対応する server ブロックを作成してください。以下の要件を満たすこと。

- ポート80で待ち受け
- ドキュメントルートは `/var/www/mysite`
- デフォルトファイルは `index.html`
- アクセスがあったときに `try_files` で存在するファイルを返し、なければ404を返す

**期待される設定：**
```
server ブロックが正しく記述され、nginx -t でエラーが出ないこと
```

<details>
<summary>ヒント</summary>

`server` ブロックの中に `listen`, `server_name`, `root`, `index`, `location` を設定します。`try_files $uri $uri/ =404;` を使いましょう。

</details>

<details>
<summary>解答例</summary>

```nginx
server {
    listen 80;
    server_name mysite.local;

    root /var/www/mysite;
    index index.html;

    location / {
        # リクエストされたURIをファイルとして探し、
        # なければディレクトリとして探し、
        # それでもなければ404を返す
        try_files $uri $uri/ =404;
    }
}
```

</details>

---

## 問題2：www ありなしの統一（基本）

`www.mysite.com` でアクセスされた場合に `mysite.com` へ301リダイレクトする設定を作成してください。

**期待される動作：**
```
http://www.mysite.com/about → http://mysite.com/about（301リダイレクト）
```

<details>
<summary>ヒント</summary>

方法は2つあります。(1) `if ($host = www.mysite.com)` を使う方法、(2) 別の server ブロックで `return 301` する方法です。推奨は(2)の方法です。

</details>

<details>
<summary>解答例</summary>

```nginx
# www ありを www なしにリダイレクト（推奨：専用 server ブロック）
server {
    listen 80;
    server_name www.mysite.com;
    return 301 http://mysite.com$request_uri;
}

# メインの server ブロック
server {
    listen 80;
    server_name mysite.com;
    root /var/www/mysite;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**補足**: `if` を使う方法より、別の server ブロックに分ける方法が推奨されます。Nginxの公式ドキュメントでも「If Is Evil」として、server ブロック内での `if` の多用は避けるよう推奨されています。

</details>

---

## 問題3：default_server の設定（基本）

以下の要件を満たす default_server を設定してください。

- どのドメインにもマッチしないリクエストには接続を切断する（ステータスコード444）
- IPv4とIPv6の両方に対応

**期待される動作：**
```
$ curl -H "Host: unknown.com" http://localhost/
→ 接続が切断される（空のレスポンス）
```

<details>
<summary>ヒント</summary>

`listen` に `default_server` を付け、`server_name _` で全てにマッチさせます。IPv6は `listen [::]:80 default_server;` で対応します。

</details>

<details>
<summary>解答例</summary>

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    # "_" は慣例的に「マッチしない名前」として使用
    server_name _;

    # 444 はNginx独自のステータスコードで、レスポンスを返さず接続を切断
    return 444;
}
```

**補足**: ステータスコード444はNginx独自のコードで、レスポンスボディを返さずにTCP接続を閉じます。不正アクセスやスキャンからサーバーを保護するのに有効です。

</details>

---

## 問題4：複数サイトの設定（応用）

以下の3つのサイトを1台のNginxで運用するための設定を作成してください。

| サイト | ドメイン | ドキュメントルート |
|---|---|---|
| メインサイト | `shop.example.com` | `/var/www/shop` |
| 管理画面 | `admin.example.com` | `/var/www/admin` |
| ドキュメント | `docs.example.com` | `/var/www/docs` |

各サイトのアクセスログとエラーログは個別に出力してください。

**期待される構成：**
```
/etc/nginx/sites-available/
├── shop.example.com
├── admin.example.com
└── docs.example.com
```

<details>
<summary>ヒント</summary>

それぞれの server ブロックで `server_name`, `root`, `access_log`, `error_log` を個別に設定します。ログは `/var/log/nginx/` 配下にサイト名を含めたファイル名にしましょう。

</details>

<details>
<summary>解答例</summary>

**shop.example.com:**
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name shop.example.com;

    root /var/www/shop;
    index index.html;

    access_log /var/log/nginx/shop.access.log;
    error_log  /var/log/nginx/shop.error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**admin.example.com:**
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name admin.example.com;

    root /var/www/admin;
    index index.html;

    access_log /var/log/nginx/admin.access.log;
    error_log  /var/log/nginx/admin.error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**docs.example.com:**
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name docs.example.com;

    root /var/www/docs;
    index index.html;

    access_log /var/log/nginx/docs.access.log;
    error_log  /var/log/nginx/docs.error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**有効化コマンド:**
```bash
sudo ln -s /etc/nginx/sites-available/shop.example.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/admin.example.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/docs.example.com /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx
```

</details>

---

## 問題5：root と alias の使い分け（応用）

以下の要件を満たす location ブロックを作成してください。

1. `/images/` へのリクエストは `/var/www/shared/images/` から返す（root を使用）
2. `/downloads/` へのリクエストは `/opt/files/` から返す（alias を使用）
3. `/old-docs/` へのリクエストは `/var/www/archive/documents/` から返す（alias を使用）

それぞれ、リクエスト `/images/photo.jpg`, `/downloads/report.pdf`, `/old-docs/guide.html` に対して、実際にどのファイルパスが参照されるかもコメントで記載してください。

<details>
<summary>ヒント</summary>

- `root` はURLパス全体をルートディレクトリに追加します
- `alias` はlocation で指定したパスを置き換えます
- `alias` を使う場合、末尾の `/` の有無に注意が必要です

</details>

<details>
<summary>解答例</summary>

```nginx
server {
    listen 80;
    server_name example.com;

    # 1. root を使用
    # /images/photo.jpg → /var/www/shared/images/photo.jpg
    location /images/ {
        root /var/www/shared;
        # root ではURLパス（/images/photo.jpg）がそのまま追加される
    }

    # 2. alias を使用
    # /downloads/report.pdf → /opt/files/report.pdf
    location /downloads/ {
        alias /opt/files/;
        # alias ではlocationパス（/downloads/）が置き換わる
        # alias の末尾に / を忘れないこと！
    }

    # 3. alias を使用
    # /old-docs/guide.html → /var/www/archive/documents/guide.html
    location /old-docs/ {
        alias /var/www/archive/documents/;
    }
}
```

**注意点**: `alias` を使う場合、末尾のスラッシュを忘れると意図しないパスになります。`alias /opt/files;` だと `/downloads/report.pdf` が `/opt/filesreport.pdf` と解釈されてしまいます。

</details>

---

## 問題6：カスタムログフォーマット（応用）

以下の情報を含むカスタムログフォーマット `custom` を定義し、特定のサイトに適用してください。

- クライアントIPアドレス
- アクセス日時
- リクエストメソッドとURI
- ステータスコード
- レスポンスサイズ
- リクエスト処理時間

**期待されるログ出力例：**
```
192.168.1.10 [05/Apr/2026:10:15:30 +0900] "GET /index.html" 200 1234 0.002
```

<details>
<summary>ヒント</summary>

`log_format` ディレクティブは `http` ブロック内で定義します。使用できる主な変数：`$remote_addr`, `$time_local`, `$request_method`, `$request_uri`, `$status`, `$body_bytes_sent`, `$request_time`

</details>

<details>
<summary>解答例</summary>

```nginx
http {
    # カスタムログフォーマットの定義
    log_format custom '$remote_addr [$time_local] '
                      '"$request_method $request_uri" '
                      '$status $body_bytes_sent '
                      '$request_time';

    server {
        listen 80;
        server_name example.com;
        root /var/www/example.com;

        # カスタムフォーマットを指定してログ出力
        access_log /var/log/nginx/example.com.access.log custom;
        error_log  /var/log/nginx/example.com.error.log warn;

        location / {
            try_files $uri $uri/ =404;
        }
    }
}
```

</details>

---

## 問題7：ワイルドカードサブドメインの振り分け（チャレンジ）

ワイルドカードサブドメインを使って、`<ユーザー名>.myapp.com` というURLでアクセスすると、そのユーザー名に対応するディレクトリのコンテンツが表示される設定を作成してください。

例：
- `alice.myapp.com` → `/var/www/users/alice/public/`
- `bob.myapp.com` → `/var/www/users/bob/public/`

**期待される動作：**
```
$ curl -H "Host: alice.myapp.com" http://localhost/
→ /var/www/users/alice/public/index.html の内容が返される
```

<details>
<summary>ヒント</summary>

正規表現を使った `server_name` で名前付きキャプチャ `(?<name>...)` を使い、キャプチャした値を `root` で利用します。`server_name ~^(?<username>.+)\.myapp\.com$;` のような書き方です。

</details>

<details>
<summary>解答例</summary>

```nginx
server {
    listen 80;

    # 正規表現で server_name をキャプチャ
    # ~  : 正規表現であることを示すプレフィックス
    # (?<username>.+) : サブドメイン部分を $username にキャプチャ
    server_name ~^(?<username>.+)\.myapp\.com$;

    # キャプチャした値をルートディレクトリに使用
    root /var/www/users/$username/public;
    index index.html;

    access_log /var/log/nginx/myapp.access.log;
    error_log  /var/log/nginx/myapp.error.log;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**補足**: この方法はユーザーごとにサブドメインを割り当てるSaaSアプリケーションでよく使われるパターンです。ただし、ディレクトリトラバーサルを防ぐため、ユーザー名のバリデーションを別途行うことをお勧めします。正規表現を `(?<username>[a-z0-9]+)` のように制限するとより安全です。

</details>

---

## 問題8：ポートベースのバーチャルホスト（チャレンジ）

以下の要件を満たす設定を作成してください。ドメイン名ではなく、ポート番号でサイトを振り分けます。

| ポート | 用途 | ドキュメントルート |
|---|---|---|
| 80 | 本番サイト | `/var/www/production` |
| 8080 | ステージング環境 | `/var/www/staging` |
| 8888 | 開発環境 | `/var/www/development` |

さらに、ステージング環境（8080）と開発環境（8888）にはBASIC認証を設定してください。

<details>
<summary>ヒント</summary>

- 各ポートごとに `listen` を変えた server ブロックを作成します
- BASIC認証には `auth_basic` と `auth_basic_user_file` ディレクティブを使います
- パスワードファイルは `htpasswd` コマンドで作成できます

</details>

<details>
<summary>解答例</summary>

```nginx
# 本番サイト（ポート80・認証なし）
server {
    listen 80;
    server_name _;

    root /var/www/production;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}

# ステージング環境（ポート8080・BASIC認証あり）
server {
    listen 8080;
    server_name _;

    root /var/www/staging;
    index index.html;

    # BASIC認証の設定
    auth_basic "Staging Environment";
    auth_basic_user_file /etc/nginx/.htpasswd_staging;

    location / {
        try_files $uri $uri/ =404;
    }
}

# 開発環境（ポート8888・BASIC認証あり）
server {
    listen 8888;
    server_name _;

    root /var/www/development;
    index index.html;

    auth_basic "Development Environment";
    auth_basic_user_file /etc/nginx/.htpasswd_dev;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

**パスワードファイルの作成:**
```bash
# htpasswd コマンドでパスワードファイルを作成
# -c: ファイルを新規作成  -B: bcrypt暗号化を使用
sudo htpasswd -cB /etc/nginx/.htpasswd_staging admin
sudo htpasswd -cB /etc/nginx/.htpasswd_dev developer

# 権限を設定（Nginxのみ読み取れるようにする）
sudo chmod 640 /etc/nginx/.htpasswd_staging
sudo chmod 640 /etc/nginx/.htpasswd_dev
sudo chown root:www-data /etc/nginx/.htpasswd_staging
sudo chown root:www-data /etc/nginx/.htpasswd_dev
```

</details>
