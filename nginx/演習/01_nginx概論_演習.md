# 第1章 演習：nginx概論

---

## 問題1：nginxの特徴（基本）

以下の説明が正しければ「○」、間違っていれば「×」を答え、間違いの場合は正しい内容を述べてください。

1. nginxはプロセス駆動（マルチプロセス）モデルで動作する
2. nginxのワーカープロセスは1つで数千の同時接続を処理できる
3. 設定を変更した後は必ず `nginx restart` する必要がある
4. nginxはWebサーバーとしてのみ使用される
5. nginxのメイン設定ファイルは `/etc/nginx/nginx.conf` である

<details>
<summary>解答例</summary>

```
1. × — nginxはイベント駆動（Event-Driven）モデルで動作します。
   プロセス駆動はApacheの特徴です。

2. ○ — nginxのワーカープロセスはイベントループにより、
   1つのプロセスで数千の同時接続を効率的に処理できます。

3. × — restart はプロセスを停止してから再起動するため、
   一瞬のダウンタイムが発生します。設定変更の反映には
   `nginx -t` で文法チェック後、`reload` を使うのが安全です。

4. × — nginxはWebサーバーだけでなく、リバースプロキシ、
   ロードバランサ、メールプロキシとしても使用できます。

5. ○ — Ubuntu/Debian、CentOS/RHELともに
   /etc/nginx/nginx.conf がメイン設定ファイルです。
```

</details>

---

## 問題2：コマンドの使い分け（基本）

以下の各シナリオで、使うべきコマンドを答えてください。

1. nginxの設定ファイルを編集した後、文法エラーがないか確認したい
2. 文法チェックが通った後、ダウンタイムなしで設定を反映したい
3. nginxが正常に動作しているか確認したい
4. サーバー起動時にnginxを自動で起動するようにしたい
5. 処理中のリクエストを完了させてからnginxを停止したい

<details>
<summary>解答例</summary>

```bash
# 1. 設定ファイルの文法チェック
sudo nginx -t

# 2. ダウンタイムなしで設定を反映
sudo systemctl reload nginx
# または
sudo nginx -s reload

# 3. 動作状態の確認
sudo systemctl status nginx

# 4. 自動起動の有効化
sudo systemctl enable nginx

# 5. 緩やかな停止（グレースフルシャットダウン）
sudo nginx -s quit
```

</details>

---

## 問題3：Apache と nginx の比較（基本）

以下の観点で、Apache と nginx のどちらが適しているか答え、理由を述べてください。

1. 大量の同時接続（C10K問題）への対応
2. `.htaccess` によるディレクトリ単位の設定変更
3. 静的ファイル（画像、CSS、JS）の高速配信
4. リバースプロキシとしてアプリケーションサーバーの前段に配置

<details>
<summary>解答例</summary>

```
1. nginx が適している
   理由：イベント駆動モデルにより、少ないメモリで
   数万〜数十万の同時接続を処理できます。
   Apacheのプロセス駆動モデルでは接続ごとに
   プロセス/スレッドが必要なため、メモリを大量に消費します。

2. Apache が適している
   理由：Apacheは .htaccess ファイルによるディレクトリ単位の
   動的な設定変更をサポートしています。nginxはこの機能がなく、
   設定変更には設定ファイルの編集と reload が必要です。
   共有ホスティングなどで各ユーザーが個別に設定を変えたい場合は
   Apacheの方が適しています。

3. nginx が適している
   理由：nginxは静的ファイルの配信に非常に優れており、
   イベント駆動による非同期I/Oで高いスループットを実現します。
   sendfile, tcp_nopush などの最適化も標準で備えています。

4. nginx が適している
   理由：nginxはリバースプロキシとして設計されており、
   proxy_pass、upstream ブロック、ロードバランシングなどの
   機能が充実しています。メモリ効率が良いため、
   前段のプロキシとして少ないリソースで多数の接続を中継できます。
```

</details>

---

## 問題4：ディレクトリ構成の理解（基本）

Ubuntu/Debian環境のnginxにおいて、以下の各ファイル/ディレクトリの役割を説明してください。

1. `/etc/nginx/nginx.conf`
2. `/etc/nginx/sites-available/`
3. `/etc/nginx/sites-enabled/`
4. `/var/log/nginx/access.log`
5. `/var/www/html/`

<details>
<summary>解答例</summary>

```
1. /etc/nginx/nginx.conf
   nginxのメイン設定ファイル。ワーカープロセス数、
   ログの設定、HTTPブロックなどグローバルな設定を記述します。

2. /etc/nginx/sites-available/
   利用可能なサイトの設定ファイルを格納するディレクトリ。
   ここにファイルを置いただけでは有効にはなりません。

3. /etc/nginx/sites-enabled/
   実際に有効化されたサイトの設定ファイル（のシンボリックリンク）を
   格納するディレクトリ。sites-available 内のファイルへの
   シンボリックリンクを作成することで設定を有効化します。

   有効化: ln -s /etc/nginx/sites-available/mysite /etc/nginx/sites-enabled/
   無効化: rm /etc/nginx/sites-enabled/mysite

4. /var/log/nginx/access.log
   nginxのアクセスログ。クライアントからのリクエストの記録
   （IPアドレス、日時、リクエスト内容、ステータスコード等）
   が書き込まれます。

5. /var/www/html/
   デフォルトのドキュメントルート。Webサイトの
   HTMLファイルや静的ファイルを配置する場所です。
   通常は各サイトごとに別のディレクトリを指定します。
```

</details>

---

## 問題5：プロセス構成の理解（応用）

以下のコマンド出力を見て、質問に答えてください。

```
$ ps aux | grep nginx
root     1001  0.0  0.1  nginx: master process /usr/sbin/nginx
www-data 1002  0.0  0.3  nginx: worker process
www-data 1003  0.0  0.3  nginx: worker process
www-data 1004  0.0  0.3  nginx: worker process
www-data 1005  0.0  0.3  nginx: worker process
```

1. マスタープロセスはどれですか？なぜそう判断できますか？
2. ワーカープロセスは何個ありますか？
3. マスタープロセスとワーカープロセスの実行ユーザーが異なる理由は何ですか？
4. ワーカープロセス数を変更するにはどうしますか？

<details>
<summary>解答例</summary>

```
1. PID 1001 がマスタープロセスです。
   「nginx: master process」と表示されていること、
   実行ユーザーが root であることから判断できます。

2. ワーカープロセスは4個あります（PID 1002〜1005）。
   すべて「nginx: worker process」と表示されています。

3. マスタープロセスは root 権限で動作する必要があります。
   理由：
   ・特権ポート（80, 443）をバインドするため
   ・ログファイルを開くため
   ・ワーカープロセスを管理（fork/kill）するため

   ワーカープロセスは www-data（非特権ユーザー）で動作します。
   理由：
   ・セキュリティ上、リクエスト処理を低権限で行う
   ・万が一脆弱性を突かれても被害を最小化できる

4. nginx.conf の worker_processes ディレクティブを変更します。

   worker_processes 4;    # 固定値
   worker_processes auto;  # CPUコア数に自動設定（推奨）

   変更後、nginx -t で文法チェックし、reload で反映します。
```

</details>

---

## 問題6：トラブルシューティング（応用）

以下の各状況で、原因の調査に使うコマンドと、想定される原因を答えてください。

1. `http://localhost` にアクセスしても応答がない
2. 設定を変更して `reload` したが、変更が反映されていない
3. `systemctl start nginx` がエラーで失敗する

<details>
<summary>解答例</summary>

```
1. http://localhost に応答がない

   調査コマンド:
   $ sudo systemctl status nginx      # サービスの状態確認
   $ sudo ss -tlnp | grep :80         # 80番ポートのリスン確認
   $ sudo journalctl -u nginx --no-pager -n 20  # ログ確認
   $ curl -v http://localhost          # 詳細な接続情報

   想定される原因:
   ・nginxが起動していない
   ・ファイアウォール（ufw, iptables）でポート80がブロック
   ・他のプロセス（Apache等）がポート80を使用中
   ・listen ディレクティブが 80 以外のポートを指定


2. reload したが変更が反映されない

   調査コマンド:
   $ sudo nginx -t                    # 文法チェック
   $ sudo nginx -T                    # 実際に読み込まれている設定を表示
   $ ls -la /etc/nginx/sites-enabled/ # シンボリックリンク確認

   想定される原因:
   ・設定ファイルに文法エラーがあり、reload が失敗している
     （reload はエラー時に旧設定を維持するため気づきにくい）
   ・編集したファイルが sites-enabled にリンクされていない
   ・編集したファイルが nginx.conf から include されていない
   ・ブラウザのキャッシュが残っている


3. systemctl start nginx が失敗する

   調査コマンド:
   $ sudo nginx -t                    # 文法チェック
   $ sudo journalctl -xe -u nginx     # 詳細なエラーログ
   $ sudo ss -tlnp | grep :80         # ポート競合の確認
   $ cat /var/log/nginx/error.log     # エラーログ確認

   想定される原因:
   ・設定ファイルに文法エラーがある
   ・ポート80/443が他のプロセスに占有されている
   ・SSL証明書ファイルが見つからない
   ・ドキュメントルートのディレクトリが存在しない
   ・権限の問題（ログファイルやPIDファイルの書き込み権限）
```

</details>

---

## 問題7：実践シナリオ（チャレンジ）

あなたは新しいUbuntuサーバーにnginxをセットアップする担当者です。以下の手順を、コマンドとともに記述してください。

1. nginxをインストールする
2. nginxが正常にインストールされたことをバージョンで確認する
3. nginxを起動する
4. サーバー起動時の自動起動を有効にする
5. ブラウザ（またはcurl）でデフォルトページが表示されることを確認する
6. デフォルトの `index.html` を編集して「Hello, nginx!」と表示する
7. ファイアウォール（ufw）でHTTP（80）とHTTPS（443）を許可する

<details>
<summary>解答例</summary>

```bash
# 1. nginxのインストール
sudo apt update
sudo apt install -y nginx

# 2. バージョン確認
nginx -v
# 出力例: nginx version: nginx/1.24.0

# 3. nginx起動
sudo systemctl start nginx

# 4. 自動起動の有効化
sudo systemctl enable nginx

# 5. デフォルトページの確認
curl http://localhost
# または
curl -I http://localhost
# HTTP/1.1 200 OK が返ればOK

# 6. index.html の編集
sudo tee /var/www/html/index.html > /dev/null <<'EOF'
<!DOCTYPE html>
<html>
<head>
    <title>Hello</title>
</head>
<body>
    <h1>Hello, nginx!</h1>
</body>
</html>
EOF

# 確認
curl http://localhost
# <h1>Hello, nginx!</h1> が含まれていればOK

# 7. ファイアウォールの設定
sudo ufw allow 'Nginx Full'
# または個別に
# sudo ufw allow 80/tcp
# sudo ufw allow 443/tcp

# ファイアウォール状態の確認
sudo ufw status
```

</details>
