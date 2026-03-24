# 第1章 演習：Linuxの基本

---

## 基本問題

### 問題1: Linuxの特徴
Linuxの特徴として正しいものをすべて選んでください。

a) オープンソースである
b) マルチユーザーに対応している
c) サーバー用途では使われない
d) 無料のディストリビューションが多い

<details>
<summary>解答</summary>

**a, b, d** が正しいです。

```
a) ○ - Linuxはオープンソースで、ソースコードが公開されています
b) ○ - 複数のユーザーが同時にシステムを利用できます
c) × - Webサーバーの約70%以上がLinuxで動作しています
d) ○ - Ubuntu、Debianなど多くのディストリビューションが無料です
```

</details>

---

### 問題2: ディストリビューションの分類
以下のディストリビューションを「Debian系」と「RHEL系」に分類してください。

- Ubuntu
- Rocky Linux
- Debian
- AlmaLinux
- Linux Mint
- Fedora

<details>
<summary>解答</summary>

```
【Debian系】
- Ubuntu（Debianベース）
- Debian（Debian系の大元）
- Linux Mint（Ubuntuベース）

【RHEL系】
- Rocky Linux（RHEL互換）
- AlmaLinux（RHEL互換）
- Fedora（RHELの開発版的位置づけ）
```

</details>

---

### 問題3: カーネルバージョンの確認
現在のLinuxカーネルバージョンを表示するコマンドを2つ書いてください。

期待される出力例：
```
5.15.0-91-generic
```

<details>
<summary>ヒント</summary>

`uname` コマンドのオプションを使います。

</details>

<details>
<summary>解答</summary>

```bash
# カーネルバージョンのみ表示
$ uname -r
5.15.0-91-generic

# 全情報を表示（カーネルバージョンを含む）
$ uname -a
Linux myserver 5.15.0-91-generic #101-Ubuntu SMP ...
```

</details>

---

### 問題4: シェルの確認
以下の各コマンドが何を表示するか答えてください。

1. `echo $SHELL`
2. `echo $0`
3. `cat /etc/shells`

<details>
<summary>解答</summary>

```bash
# 1. デフォルトのログインシェルのパスを表示
$ echo $SHELL
/bin/bash

# 2. 現在実行中のシェルのプログラム名を表示
$ echo $0
-bash

# 3. システムで利用可能なシェルの一覧を表示
$ cat /etc/shells
/bin/sh
/bin/bash
/usr/bin/bash
/bin/zsh
/usr/bin/zsh
```

</details>

---

### 問題5: ショートカットキー
以下のショートカットキーの機能を答えてください。

1. `Ctrl + C`
2. `Ctrl + L`
3. `Ctrl + R`
4. `Ctrl + D`
5. `Tab`

<details>
<summary>解答</summary>

```
1. Ctrl + C → 実行中のコマンドを中断（キャンセル）
2. Ctrl + L → 画面をクリア（clearコマンドと同等）
3. Ctrl + R → コマンド履歴の検索（インクリメンタルサーチ）
4. Ctrl + D → ログアウト / 入力終了（EOF送信）
5. Tab     → コマンド名やファイル名の自動補完
```

</details>

---

### 問題6: プロンプトの読み方
以下のプロンプトから、ユーザー名、ホスト名、カレントディレクトリ、ユーザー種別（一般/root）を読み取ってください。

```
admin@production:/var/log$
```

<details>
<summary>解答</summary>

```
ユーザー名: admin
ホスト名: production
カレントディレクトリ: /var/log
ユーザー種別: 一般ユーザー（$ はプロンプト記号が $ なので一般ユーザー）
             ※ root の場合は # になる
```

</details>

---

## 応用問題

### 問題7: manコマンドの操作
`man ls` を実行した後、以下の操作をどのキーで行うか答えてください。

1. 次のページに進む
2. 前のページに戻る
3. マニュアルを終了する
4. 文字列 "sort" を検索する
5. 次の検索結果に移動する

<details>
<summary>解答</summary>

```
1. Space キー（または f キー）
2. b キー
3. q キー
4. /sort と入力して Enter
5. n キー
```

</details>

---

### 問題8: コマンドの構文
以下のコマンドについて、「コマンド名」「オプション」「引数」をそれぞれ特定してください。

```bash
ls -la /home
head -n 5 /etc/passwd
grep -rn "error" /var/log/
```

<details>
<summary>解答</summary>

```bash
# ls -la /home
# コマンド名: ls
# オプション: -la（-l と -a の組み合わせ）
# 引数: /home

# head -n 5 /etc/passwd
# コマンド名: head
# オプション: -n 5（5行を指定）
# 引数: /etc/passwd

# grep -rn "error" /var/log/
# コマンド名: grep
# オプション: -rn（-r 再帰検索 と -n 行番号表示 の組み合わせ）
# 引数: "error"（検索パターン）と /var/log/（検索対象ディレクトリ）
```

</details>

---

### 問題9: コマンドの種類
`type` コマンドを使って、以下のコマンドが「エイリアス」「シェル組み込み」「外部コマンド」のどれかを確認してください。

1. `cd`
2. `ls`
3. `python3`

期待される出力例：
```
cd is a shell builtin
ls is aliased to `ls --color=auto'
python3 is /usr/bin/python3
```

<details>
<summary>解答</summary>

```bash
$ type cd
cd is a shell builtin           # シェル組み込みコマンド

$ type ls
ls is aliased to `ls --color=auto'  # エイリアス（別名が設定されている）

$ type python3
python3 is /usr/bin/python3     # 外部コマンド（ファイルとして存在）
```

- **シェル組み込み（builtin）**: シェル自体に組み込まれたコマンド（cd, echo, export等）
- **エイリアス**: 別名が設定されたコマンド
- **外部コマンド**: ファイルとして存在するプログラム

</details>

---

## チャレンジ問題

### 問題10: 総合問題
以下の操作を順番に行い、各コマンドの出力を確認してください。

1. 現在のユーザー名を表示する
2. ホスト名を表示する
3. 現在の日時を表示する
4. カーネルバージョンを表示する
5. 使用中のシェルを表示する
6. 利用可能なシェルの一覧を表示する

<details>
<summary>解答</summary>

```bash
# 1. 現在のユーザー名を表示
$ whoami
tanaka

# 2. ホスト名を表示
$ hostname
myserver

# 3. 現在の日時を表示
$ date
Wed Mar 20 15:30:00 JST 2024

# 4. カーネルバージョンを表示
$ uname -r
5.15.0-91-generic

# 5. 使用中のシェルを表示
$ echo $SHELL
/bin/bash

# 6. 利用可能なシェルの一覧を表示
$ cat /etc/shells
/bin/sh
/bin/bash
/usr/bin/bash
/bin/zsh
/usr/bin/zsh
```

</details>

---

### 問題11: ディストリビューションの確認
自分が使っているLinuxディストリビューションの名前とバージョンを確認するコマンドを書いてください。

<details>
<summary>ヒント</summary>

`/etc/os-release` ファイルの中身を確認してみましょう。

</details>

<details>
<summary>解答</summary>

```bash
# os-release ファイルを確認（最も確実な方法）
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
ID=ubuntu
...

# 短い情報を表示
$ lsb_release -a
Distributor ID: Ubuntu
Description:    Ubuntu 22.04.3 LTS
Release:        22.04
Codename:       jammy

# ホスト名情報を含む確認
$ hostnamectl
   Static hostname: myserver
         Icon name: computer-vm
           Chassis: vm
  Operating System: Ubuntu 22.04.3 LTS
            Kernel: Linux 5.15.0-91-generic
      Architecture: x86-64
```

</details>
