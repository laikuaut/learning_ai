# 第1章：nginx概論

## この章のゴール

- nginx（エンジンエックス）とは何か、その特徴を理解する
- Webサーバーの役割と nginx の位置づけを理解する
- nginx のアーキテクチャ（イベント駆動モデル）を理解する
- nginx のインストール方法を知る
- nginx の起動・停止・再読込などの基本操作を身につける

---

## 1.1 nginxとは

### nginxの概要

nginx（"engine x" と発音）は、**高性能・軽量なWebサーバー/リバースプロキシサーバー**です。2004年にIgor Sysoev氏がロシアで開発し、現在は世界で最も利用されているWebサーバーの一つです。

```
【nginxの主な用途】

┌─────────────────────────────────────────────────┐
│                    nginx                         │
├────────────┬────────────┬────────────┬───────────┤
│ Webサーバー │リバースプロキシ│ロードバランサ│メールプロキシ│
│            │            │            │           │
│ 静的ファイル│ アプリへの   │ 複数サーバー │ SMTP/POP3 │
│ の配信     │ リクエスト転送│ への振り分け │ の中継     │
└────────────┴────────────┴────────────┴───────────┘
```

### Apache vs nginx

```
【Apache と nginx の比較】

                Apache                    nginx
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
アーキテクチャ  プロセス/スレッド駆動     イベント駆動
メモリ使用量    接続数に比例して増加       少量で一定
同時接続処理    数千〜数万                 数万〜数十万
設定変更       .htaccessで動的変更可能    設定ファイルで一括管理
モジュール     動的にロード可能            コンパイル時に組み込み
得意分野       動的コンテンツ             静的コンテンツ・プロキシ
```

> **実務でのポイント**: 現代のWebサービスでは、nginxをリバースプロキシ兼ロードバランサとして前段に配置し、背後にアプリケーションサーバー（Node.js, Python, Go等）を置く構成が一般的です。

---

## 1.2 nginxのアーキテクチャ

### イベント駆動モデル

nginxは**イベント駆動（Event-Driven）のノンブロッキングI/O**アーキテクチャを採用しています。これにより、少ないメモリで大量の同時接続を処理できます。

```
【Apacheのプロセス駆動モデル】

クライアント1 ──→ [プロセス1] ── 処理中（待機） ──→ レスポンス
クライアント2 ──→ [プロセス2] ── 処理中（待機） ──→ レスポンス
クライアント3 ──→ [プロセス3] ── 処理中（待機） ──→ レスポンス
  ...            ...
クライアントN ──→ [プロセスN] ── 処理中（待機） ──→ レスポンス

→ 接続ごとにプロセスが必要 → メモリ消費大


【nginxのイベント駆動モデル】

クライアント1 ──┐
クライアント2 ──┤
クライアント3 ──┼──→ [ワーカープロセス] ──→ レスポンス群
  ...          │     （イベントループ）
クライアントN ──┘

→ 1つのワーカーが数千の接続を処理 → メモリ消費小
```

### マスタープロセスとワーカープロセス

```
【nginxのプロセス構成】

┌──────────────────────────────┐
│      マスタープロセス          │
│    （Master Process）         │
│                              │
│  ・設定ファイルの読み込み      │
│  ・ワーカーの管理（起動・停止）│
│  ・ポートのバインド            │
│  ・ログファイルのオープン      │
└──────┬───────────────────────┘
       │ fork
  ┌────┼────┬────┐
  ▼    ▼    ▼    ▼
┌────┐┌────┐┌────┐┌────┐
│ W1 ││ W2 ││ W3 ││ W4 │  ワーカープロセス
│    ││    ││    ││    │  （Worker Process）
│    ││    ││    ││    │
│接続 ││接続 ││接続 ││接続 │  ・リクエストの処理
│処理 ││処理 ││処理 ││処理 │  ・レスポンスの生成
└────┘└────┘└────┘└────┘  ・各ワーカーが独立に動作
```

---

## 1.3 インストール

### 主要なLinuxディストリビューションでのインストール

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install nginx

# CentOS / RHEL / Amazon Linux 2
sudo yum install nginx
# または
sudo dnf install nginx

# macOS（Homebrew）
brew install nginx
```

### インストールの確認

```bash
# バージョン確認
nginx -v
# 出力例: nginx version: nginx/1.24.0

# 詳細なビルド情報
nginx -V
```

---

## 1.4 ディレクトリ構成

### 主要ファイルとディレクトリ

```
【nginxの主要ディレクトリ構成（Ubuntu/Debian）】

/etc/nginx/
├── nginx.conf              # メイン設定ファイル
├── conf.d/                 # 追加の設定ファイル（*.conf）
├── sites-available/        # 利用可能なサイト設定
├── sites-enabled/          # 有効化されたサイト設定（シンボリックリンク）
├── snippets/               # 設定の断片（再利用可能なパーツ）
├── mime.types              # MIMEタイプの定義
├── fastcgi_params          # FastCGIパラメータ
├── proxy_params            # プロキシパラメータ
└── modules-enabled/        # 有効化されたモジュール

/var/log/nginx/
├── access.log              # アクセスログ
└── error.log               # エラーログ

/var/www/html/              # デフォルトのドキュメントルート
/usr/share/nginx/html/      # デフォルトのHTMLファイル（ディストリビューションによる）
/run/nginx.pid              # PIDファイル
```

```
【CentOS / RHEL の場合の違い】

/etc/nginx/
├── nginx.conf              # メイン設定ファイル
├── conf.d/                 # 追加の設定ファイル
└── default.d/              # デフォルトサーバー用の設定

※ sites-available / sites-enabled パターンは
  デフォルトでは存在しない（手動で作成可能）
```

---

## 1.5 基本操作コマンド

### nginxの制御

```bash
# 起動
sudo systemctl start nginx

# 停止
sudo systemctl stop nginx

# 再起動（プロセスを停止してから起動）
sudo systemctl restart nginx

# 設定の再読込（ダウンタイムなし）
sudo systemctl reload nginx

# 自動起動の有効化
sudo systemctl enable nginx

# 自動起動の無効化
sudo systemctl disable nginx

# ステータス確認
sudo systemctl status nginx
```

### nginx コマンド直接実行

```bash
# 設定ファイルの文法チェック（非常に重要！）
sudo nginx -t
# 出力例:
# nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
# nginx: configuration file /etc/nginx/nginx.conf test is successful

# 設定の再読込（nginx シグナル）
sudo nginx -s reload

# 緩やかな停止（処理中のリクエストを完了してから停止）
sudo nginx -s quit

# 即座に停止
sudo nginx -s stop

# 設定ファイルを指定して起動
sudo nginx -c /path/to/custom/nginx.conf
```

> **実務でのポイント**: 設定を変更したら、必ず `nginx -t` で文法チェックしてから `reload` しましょう。文法エラーがある状態で `restart` すると、nginxが起動できずサービスが停止してしまいます。`reload` はエラーがあっても既存のプロセスを維持するため、より安全です。

---

## 1.6 動作確認

### デフォルトページへのアクセス

```bash
# ローカルからアクセス
curl http://localhost

# レスポンスヘッダーの確認
curl -I http://localhost
# 出力例:
# HTTP/1.1 200 OK
# Server: nginx/1.24.0
# Content-Type: text/html
# ...
```

### プロセスの確認

```bash
# nginxプロセスの確認
ps aux | grep nginx
# 出力例:
# root     1234  ...  nginx: master process /usr/sbin/nginx
# www-data 1235  ...  nginx: worker process
# www-data 1236  ...  nginx: worker process

# ポートの確認
sudo ss -tlnp | grep nginx
# 出力例:
# LISTEN  0  511  0.0.0.0:80  0.0.0.0:*  users:(("nginx",pid=1234,fd=6))
```

---

## ポイントまとめ

```
┌─────────────────────────────────────────────────────────────┐
│                     第1章のポイント                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  1. nginxはイベント駆動の高性能Webサーバー/リバースプロキシ    │
│     → 少ないメモリで大量の同時接続を処理できる               │
│                                                             │
│  2. マスタープロセス + ワーカープロセスの2層構造              │
│     → マスターが管理、ワーカーがリクエスト処理               │
│                                                             │
│  3. 設定変更後は必ず nginx -t で文法チェック                  │
│     → reload で無停止反映、restart は停止を伴う              │
│                                                             │
│  4. 主な設定ファイルは /etc/nginx/ 以下に配置                │
│     → nginx.conf がメイン、conf.d/ で個別設定               │
│                                                             │
│  5. Webサーバー・リバースプロキシ・ロードバランサの            │
│     3つの役割を1つのソフトウェアで実現できる                  │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

**次の章では**: nginx の設定ファイルの構造（ディレクティブ、ブロック、コンテキスト）を詳しく学びます。nginx.conf の読み書きができるようになります。
