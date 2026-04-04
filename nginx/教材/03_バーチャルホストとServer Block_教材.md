# 第3章：バーチャルホストとServer Block

> **この章のゴール**: 1台のNginxサーバーで複数のWebサイトを運用できるようになる。
> server ブロックの書き方、ドメインごとの振り分け、ログの分離まで理解すれば、実務レベルのマルチサイト運用が可能になります。

---

## なぜバーチャルホストを学ぶのか？

実際のWebサーバーでは、1台のサーバーで複数のサイトを同時に運用するのが一般的です。

```
                    ┌─────────────────────┐
 example.com ──────▶│                     │──▶ /var/www/example.com/
                    │   Nginx (1台)       │
 blog.example.com ─▶│   ポート 80         │──▶ /var/www/blog/
                    │                     │
 api.example.com ──▶│                     │──▶ /var/www/api/
                    └─────────────────────┘
```

この仕組みを **バーチャルホスト（Virtual Host）** と呼びます。Nginxでは **server ブロック（Server Block）** を使って実現します。

---

## 3.1 バーチャルホストの概念

### バーチャルホストとは？

**バーチャルホスト（Virtual Host）** とは、1台の物理サーバー（または1つのIPアドレス）で複数のWebサイトをホスティングする技術です。

Apacheでは「VirtualHost」、Nginxでは「Server Block」と呼ばれますが、概念は同じです。

### 振り分けの仕組み

ブラウザがWebサーバーにアクセスする際、HTTPリクエストの `Host` ヘッダーにドメイン名が含まれます。

```
GET / HTTP/1.1
Host: example.com        ← ここでどのサイトか判別
Accept: text/html
```

Nginxはこの `Host` ヘッダーを見て、どの server ブロックで処理するかを決定します。

```
クライアント                      Nginx
┌──────────┐  Host: example.com  ┌──────────────────────┐
│ブラウザ   │ ─────────────────▶ │ server {              │
│          │                     │   server_name example │
│          │                     │   ...                 │
└──────────┘                     │ }                     │
                                 │                      │
                                 │ server {              │
                                 │   server_name blog    │
                                 │   ...                 │
                                 │ }                     │
                                 └──────────────────────┘
```

---

## 3.2 server ブロックの構成と主要ディレクティブ

### 基本構成

server ブロックは `http` ブロックの中に記述します。

```nginx
http {
    server {
        listen       80;                    # 待ち受けポート
        server_name  example.com;           # ドメイン名
        root         /var/www/example.com;  # ドキュメントルート
        index        index.html;            # デフォルトファイル

        location / {
            try_files $uri $uri/ =404;
        }
    }
}
```

### 主要ディレクティブ一覧

| ディレクティブ | 説明 | 例 |
|---|---|---|
| `listen` | 待ち受けるポート・IPアドレス | `listen 80;` |
| `server_name` | 対応するドメイン名 | `server_name example.com;` |
| `root` | ドキュメントルート | `root /var/www/html;` |
| `index` | デフォルトで返すファイル | `index index.html index.htm;` |
| `access_log` | アクセスログの出力先 | `access_log /var/log/nginx/access.log;` |
| `error_log` | エラーログの出力先 | `error_log /var/log/nginx/error.log;` |
| `location` | URLパスごとの処理 | `location /images/ { ... }` |

---

## 3.3 server_name によるドメインベースの振り分け

### 基本的な使い方

`server_name` ディレクティブで、そのserver ブロックが応答するドメイン名を指定します。

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/example.com;
}
```

### 複数ドメインの指定

スペース区切りで複数のドメインを指定できます。

```nginx
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
}
```

### ワイルドカードの使用

先頭または末尾に `*` を使えます。

```nginx
# サブドメインすべてにマッチ
server {
    listen 80;
    server_name *.example.com;
    root /var/www/example.com;
}

# TLDが異なるドメインにマッチ
server {
    listen 80;
    server_name example.*;
    root /var/www/example.com;
}
```

### 正規表現の使用

`~` プレフィックスを付けると正規表現が使えます。

```nginx
server {
    listen 80;
    server_name ~^(?<subdomain>.+)\.example\.com$;
    root /var/www/$subdomain;
}
```

この設定では `blog.example.com` なら `/var/www/blog` が、`shop.example.com` なら `/var/www/shop` がドキュメントルートになります。

### server_name のマッチング優先順位

Nginxは以下の順序でマッチングを行います。

```
優先度高
  │  1. 完全一致         例: server_name example.com;
  │  2. 先頭ワイルドカード 例: server_name *.example.com;
  │  3. 末尾ワイルドカード 例: server_name example.*;
  │  4. 正規表現          例: server_name ~^(.+)\.example\.com$;
  ▼  5. default_server    （どれにもマッチしない場合）
優先度低
```

> **⚠️ よくある間違い**: `server_name` に `www.example.com` を書き忘れて、`www` 付きでアクセスするとデフォルトサーバーに飛んでしまうケースが多いです。`www` ありなしの両方を指定するか、リダイレクトで統一しましょう。

---

## 3.4 listen ディレクティブ

### 基本形式

```nginx
listen  ポート番号;
listen  IPアドレス:ポート番号;
```

### ポート指定

```nginx
server {
    listen 80;          # ポート80（HTTP）で待ち受け
    listen 443 ssl;     # ポート443（HTTPS）で待ち受け
    listen 8080;        # カスタムポートで待ち受け
}
```

### IPアドレス指定

特定のIPアドレスでのみ待ち受ける場合に使います。

```nginx
server {
    listen 192.168.1.100:80;  # 特定IPのポート80で待ち受け
}
```

### default_server

どの `server_name` にもマッチしないリクエストを受け取るサーバーを指定します。

```nginx
# デフォルトサーバー（マッチしないリクエストを処理）
server {
    listen 80 default_server;
    server_name _;              # 慣例的に "_" を使う
    return 444;                 # 接続を切断（不正アクセス対策）
}

# メインサイト
server {
    listen 80;
    server_name example.com www.example.com;
    root /var/www/example.com;
}
```

> **📖 ポイント**: `default_server` を設定しないと、設定ファイルの最初に記述された server ブロックがデフォルトになります。意図しないサイトが表示されるトラブルの原因になるため、明示的に指定しましょう。

---

## 3.5 複数サイトの運用（sites-available / sites-enabled パターン）

### ディレクトリ構成

本番環境では、サイトごとに設定ファイルを分けるのが一般的です。Debian/Ubuntu系では以下の構成が標準です。

```
/etc/nginx/
├── nginx.conf              # メイン設定（sites-enabled を include）
├── sites-available/        # 利用可能な全サイト設定
│   ├── default
│   ├── example.com
│   └── blog.example.com
├── sites-enabled/          # 有効化されたサイト設定（シンボリックリンク）
│   ├── default -> ../sites-available/default
│   └── example.com -> ../sites-available/example.com
└── conf.d/                 # その他の設定
```

### nginx.conf でのインクルード

```nginx
http {
    # 基本設定は省略

    # sites-enabled 配下の設定を全て読み込む
    include /etc/nginx/sites-enabled/*;
}
```

### サイトの有効化・無効化

```bash
# サイト設定ファイルを作成
sudo nano /etc/nginx/sites-available/example.com

# シンボリックリンクで有効化
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/

# 設定テスト
sudo nginx -t

# Nginx をリロード
sudo systemctl reload nginx

# サイトを無効化（シンボリックリンクを削除するだけ）
sudo rm /etc/nginx/sites-enabled/example.com
sudo systemctl reload nginx
```

> **⚠️ よくある間違い**: `sites-available` にファイルを作っただけでは有効になりません。必ず `sites-enabled` へのシンボリックリンクを作成してください。また、`cp` でコピーすると設定の二重管理になるため、`ln -s` を使いましょう。

### RHEL/CentOS 系の場合

RHEL系（CentOS, Rocky Linux, AlmaLinux）では `sites-available`/`sites-enabled` の代わりに `conf.d/` ディレクトリを使うのが一般的です。

```
/etc/nginx/
├── nginx.conf
└── conf.d/
    ├── example.com.conf
    └── blog.example.com.conf
```

```nginx
# nginx.conf 内
http {
    include /etc/nginx/conf.d/*.conf;
}
```

---

## 3.6 root ディレクティブと index ディレクティブ

### root ディレクティブ

`root` はドキュメントルート（Webサイトのファイルが置かれるディレクトリ）を指定します。

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/example.com/public;

    location / {
        try_files $uri $uri/ =404;
    }

    location /images/ {
        root /var/www/example.com/assets;
        # /images/logo.png → /var/www/example.com/assets/images/logo.png
    }
}
```

> **⚠️ よくある間違い**: `root` は location のパスを**そのまま追加**します。`/images/logo.png` へのリクエストに対して `root /var/www/assets;` と設定すると、`/var/www/assets/images/logo.png` を探しに行きます。パスを置き換えたい場合は `alias` を使います。

### alias ディレクティブとの違い

```nginx
# root: location パスがそのまま追加される
location /images/ {
    root /var/www/assets;
    # /images/logo.png → /var/www/assets/images/logo.png
}

# alias: location パスが置き換わる
location /images/ {
    alias /var/www/assets/img/;
    # /images/logo.png → /var/www/assets/img/logo.png
}
```

```
root の場合:
  リクエスト: /images/logo.png
  実ファイル: /var/www/assets + /images/logo.png
              └── root ──────┘   └── URI ────────┘

alias の場合:
  リクエスト: /images/logo.png
  実ファイル: /var/www/assets/img/ + logo.png
              └── alias ─────────┘   └── URI の残り ┘
```

### index ディレクティブ

ディレクトリへのアクセス時に自動的に返すファイルを指定します。

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/example.com;

    # 左から順に探し、最初に見つかったファイルを返す
    index index.html index.htm index.php;
}
```

---

## 3.7 アクセスログ・エラーログの分離

### サイトごとにログを分ける

複数サイトを運用する場合、ログを分けないとどのサイトへのアクセスか判別が困難です。

```nginx
server {
    listen 80;
    server_name example.com;
    root /var/www/example.com;

    access_log /var/log/nginx/example.com.access.log;
    error_log  /var/log/nginx/example.com.error.log;
}

server {
    listen 80;
    server_name blog.example.com;
    root /var/www/blog;

    access_log /var/log/nginx/blog.access.log;
    error_log  /var/log/nginx/blog.error.log;
}
```

### ログフォーマットのカスタマイズ

```nginx
http {
    # カスタムログフォーマットを定義
    log_format main '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';

    log_format detailed '$remote_addr - $remote_user [$time_local] '
                        '"$request" $status $body_bytes_sent '
                        '"$http_referer" "$http_user_agent" '
                        '$request_time $upstream_response_time';

    server {
        listen 80;
        server_name example.com;

        # フォーマットを指定してログ出力
        access_log /var/log/nginx/example.com.access.log detailed;
        error_log  /var/log/nginx/example.com.error.log warn;
    }
}
```

### エラーログのレベル

| レベル | 説明 |
|---|---|
| `debug` | デバッグ情報（最も詳細） |
| `info` | 一般情報 |
| `notice` | 注意すべき正常イベント |
| `warn` | 警告 |
| `error` | エラー（デフォルト） |
| `crit` | 致命的な状態 |
| `alert` | 即時対応が必要 |
| `emerg` | システムが利用不能 |

```nginx
# warn 以上のエラーのみ記録
error_log /var/log/nginx/error.log warn;
```

---

## 3.8 実用例：複数ドメインの同一サーバー運用

### 完全な設定例

以下は、1台のサーバーで3つのサイトを運用する完全な設定例です。

**デフォルトサーバー: `/etc/nginx/sites-available/default`**

```nginx
# 不正アクセス対策：どのドメインにもマッチしないリクエストを拒否
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name _;
    return 444;
}
```

**メインサイト: `/etc/nginx/sites-available/example.com`**

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name example.com www.example.com;

    root /var/www/example.com/public;
    index index.html index.htm;

    access_log /var/log/nginx/example.com.access.log;
    error_log  /var/log/nginx/example.com.error.log;

    # www ありを www なしにリダイレクト
    if ($host = www.example.com) {
        return 301 http://example.com$request_uri;
    }

    location / {
        try_files $uri $uri/ =404;
    }

    # 静的ファイルのキャッシュ設定
    location ~* \.(css|js|png|jpg|jpeg|gif|ico|svg)$ {
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # .htaccess などの隠しファイルへのアクセスを拒否
    location ~ /\. {
        deny all;
    }
}
```

**ブログサイト: `/etc/nginx/sites-available/blog.example.com`**

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name blog.example.com;

    root /var/www/blog/public;
    index index.html;

    access_log /var/log/nginx/blog.access.log;
    error_log  /var/log/nginx/blog.error.log;

    location / {
        try_files $uri $uri/ =404;
    }

    # カスタム404ページ
    error_page 404 /404.html;
    location = /404.html {
        internal;
    }
}
```

**APIサーバー: `/etc/nginx/sites-available/api.example.com`**

```nginx
server {
    listen 80;
    listen [::]:80;
    server_name api.example.com;

    access_log /var/log/nginx/api.access.log;
    error_log  /var/log/nginx/api.error.log;

    location / {
        proxy_pass http://127.0.0.1:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### サイトの有効化と動作確認

```bash
# シンボリックリンクで各サイトを有効化
sudo ln -s /etc/nginx/sites-available/example.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/blog.example.com /etc/nginx/sites-enabled/
sudo ln -s /etc/nginx/sites-available/api.example.com /etc/nginx/sites-enabled/

# 設定テスト
sudo nginx -t
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# リロード
sudo systemctl reload nginx

# 動作確認（Host ヘッダーを指定してリクエスト）
curl -H "Host: example.com" http://localhost/
curl -H "Host: blog.example.com" http://localhost/
curl -H "Host: api.example.com" http://localhost/
```

---

## ポイントまとめ

| 項目 | 内容 |
|---|---|
| バーチャルホスト | 1台のサーバーで複数サイトを運用する仕組み |
| server ブロック | Nginxでバーチャルホストを定義する単位 |
| server_name | ドメイン名でリクエストを振り分ける |
| listen | 待ち受けるポートとIPアドレスを指定する |
| default_server | どのドメインにもマッチしないリクエストの受け皿 |
| root と alias | ドキュメントルートの指定方法（パスの扱いに注意） |
| sites-available/enabled | サイトごとに設定を分離し、有効化・無効化を管理する |
| ログの分離 | サイトごとに access_log / error_log を分けて管理性を向上させる |

> **次の章では**: リバースプロキシについて学びます。Nginxをバックエンドアプリケーション（Node.js, Python等）の前段に配置する方法を理解します。
