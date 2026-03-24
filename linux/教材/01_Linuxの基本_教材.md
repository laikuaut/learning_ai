# 第1章：Linuxの基本

## 1.1 Linuxとは

Linuxは、1991年にフィンランドのリーナス・トーバルズ（Linus Torvalds）が開発を始めたオープンソースのオペレーティングシステム（OS）である。正確には「Linux」はカーネル（OSの中核部分）の名称であり、カーネルとその周辺ソフトウェアを含めた全体を「GNU/Linux」と呼ぶこともある。

### Linuxの特徴

| 特徴 | 説明 |
|------|------|
| オープンソース | ソースコードが公開されており、誰でも自由に利用・改変・再配布できる |
| マルチユーザー | 複数のユーザーが同時にシステムを利用できる |
| マルチタスク | 複数のプログラムを同時に実行できる |
| 安定性 | サーバー用途で数年間再起動なしで動作することも珍しくない |
| セキュリティ | ユーザー権限の分離が厳密で、ウイルスに強い |
| 無料 | 多くのディストリビューションが無料で利用できる |

### Linuxが使われている場所

- **サーバー**: Webサーバーの約70%以上がLinuxで動作している
- **スマートフォン**: AndroidはLinuxカーネルをベースにしている
- **組み込みシステム**: ルーター、IoTデバイス、家電製品
- **スーパーコンピュータ**: TOP500の上位のほぼ全てがLinux
- **クラウド**: AWS、Google Cloud、Azureの仮想マシンの多くがLinux

---

## 1.2 ディストリビューション

Linuxカーネルに、各種ソフトウェアやパッケージ管理システムを組み合わせたものを**ディストリビューション（ディストロ）**と呼ぶ。

### 主要なディストリビューション

#### Ubuntu
```
用途: デスクトップ / サーバー
ベース: Debian系
パッケージ管理: apt / dpkg
リリースサイクル: 6ヶ月ごと（LTSは2年ごと）
特徴: 初心者に優しい、情報が豊富
```

Ubuntu のバージョン確認：
```bash
$ cat /etc/os-release
NAME="Ubuntu"
VERSION="22.04.3 LTS (Jammy Jellyfish)"
ID=ubuntu
ID_LIKE=debian
PRETTY_NAME="Ubuntu 22.04.3 LTS"
VERSION_ID="22.04"
```

#### CentOS / Rocky Linux / AlmaLinux
```
用途: サーバー（企業用途）
ベース: RHEL（Red Hat Enterprise Linux）系
パッケージ管理: yum / dnf / rpm
特徴: 安定性重視、企業向け、長期サポート
```

> **注意**: CentOS 8は2021年末にサポート終了。後継として Rocky Linux や AlmaLinux が登場した。

#### Debian
```
用途: サーバー / デスクトップ
パッケージ管理: apt / dpkg
特徴: 安定性を最重視、膨大なパッケージ数、Ubuntuの親
```

### ディストリビューションの系統図

```
Debian系
├── Debian
│   ├── Ubuntu
│   │   ├── Linux Mint
│   │   └── Pop!_OS
│   └── Kali Linux
│
RHEL系
├── Red Hat Enterprise Linux (RHEL)
│   ├── CentOS Stream
│   ├── Rocky Linux
│   ├── AlmaLinux
│   └── Fedora（開発版的位置づけ）
│
その他
├── Arch Linux
│   └── Manjaro
├── openSUSE
└── Gentoo
```

---

## 1.3 カーネル

**カーネル**はOSの中核であり、ハードウェアとソフトウェアの橋渡しをする。

### カーネルの役割

```
┌─────────────────────────────────┐
│        アプリケーション          │  ← ユーザーが操作する
│  (Firefox, vim, bash, etc.)     │
├─────────────────────────────────┤
│        システムコール            │  ← アプリとカーネルの接点
├─────────────────────────────────┤
│          カーネル                │  ← OSの中核
│  ┌──────┬──────┬──────┬──────┐  │
│  │プロセス│メモリ│ファイル│デバイス│  │
│  │管理  │管理  │システム│ドライバ│  │
│  └──────┴──────┴──────┴──────┘  │
├─────────────────────────────────┤
│        ハードウェア              │  ← CPU, メモリ, ディスク等
└─────────────────────────────────┘
```

### カーネルバージョンの確認

```bash
$ uname -r
5.15.0-91-generic

$ uname -a
Linux myserver 5.15.0-91-generic #101-Ubuntu SMP Tue Nov 14 13:30:08 UTC 2023 x86_64 x86_64 x86_64 GNU/Linux
```

各フィールドの意味：
- `Linux` - OS名
- `myserver` - ホスト名
- `5.15.0-91-generic` - カーネルバージョン
- `x86_64` - アーキテクチャ（64ビット）

---

## 1.4 シェル（bash / zsh）

**シェル**は、ユーザーがコマンドを入力してカーネルとやり取りするためのインターフェースである。

### 主なシェルの種類

| シェル | 特徴 |
|--------|------|
| **bash** | 最も広く使われているシェル。多くのLinuxでデフォルト |
| **zsh** | bashの上位互換的シェル。macOSのデフォルト。補完機能が強力 |
| **sh** | 最も基本的なシェル（Bourne Shell） |
| **fish** | ユーザーフレンドリー。構文がやや独特 |
| **dash** | 軽量シェル。Debianでは /bin/sh のリンク先 |

### 使用中のシェルを確認する

```bash
# 現在のシェルを確認
$ echo $SHELL
/bin/bash

# プロセスとして確認
$ echo $0
-bash

# 利用可能なシェル一覧
$ cat /etc/shells
/bin/sh
/bin/bash
/usr/bin/bash
/bin/zsh
/usr/bin/zsh
```

### シェルの切り替え

```bash
# 一時的にzshを起動
$ zsh

# デフォルトシェルをzshに変更
$ chsh -s /bin/zsh
```

### bashの設定ファイル

```
~/.bashrc      ← 対話的シェル起動時に読み込まれる（最も重要）
~/.bash_profile ← ログインシェル起動時に読み込まれる
~/.bash_logout  ← ログアウト時に実行される
~/.bash_history ← コマンド履歴が保存される
```

### 基本的なショートカットキー

| ショートカット | 機能 |
|----------------|------|
| `Ctrl + C` | 実行中のコマンドを中断 |
| `Ctrl + D` | ログアウト / 入力終了 |
| `Ctrl + L` | 画面クリア（clearコマンドと同等） |
| `Ctrl + A` | カーソルを行頭に移動 |
| `Ctrl + E` | カーソルを行末に移動 |
| `Ctrl + R` | コマンド履歴の検索 |
| `Ctrl + Z` | 実行中のプロセスを一時停止 |
| `Tab` | コマンド名やファイル名の自動補完 |
| `↑ / ↓` | コマンド履歴の前後を移動 |

### Tab補完の実演

```bash
$ ls /etc/net  [Tabキーを押す]
$ ls /etc/network/    # 自動補完される

$ sys  [Tabキーを2回押す]
systemctl   systemd-analyze  systemd-cat  ...  # 候補が表示される
```

---

## 1.5 ターミナルの使い方

### ターミナルとは

**ターミナル（端末エミュレータ）**は、シェルにアクセスするためのGUIアプリケーションである。

| ターミナル | 環境 |
|------------|------|
| GNOME Terminal | Ubuntu (GNOME) |
| Konsole | KDE |
| xterm | 古典的なターミナル |
| Alacritty | GPU加速、高速 |
| Windows Terminal | WSL利用時 |

### ターミナルの起動方法

- **Ubuntu**: `Ctrl + Alt + T`
- **GUI**: アプリケーション一覧から「ターミナル」を検索
- **SSH**: リモートからアクセス（`ssh user@hostname`）

### プロンプトの読み方

```bash
user@hostname:~$
│    │         │ │
│    │         │ └─ $: 一般ユーザー / #: rootユーザー
│    │         └─── カレントディレクトリ（~はホームディレクトリ）
│    └───────────── ホスト名
└────────────────── ユーザー名
```

実例：
```bash
tanaka@webserver01:~$          # 一般ユーザー tanaka がホームにいる
tanaka@webserver01:/var/log$   # /var/log ディレクトリにいる
root@webserver01:/etc#         # root ユーザー（# になっている）
```

### コマンドの基本構文

```
コマンド [オプション] [引数]
```

例：
```bash
$ ls -la /home
  │   │    │
  │   │    └─ 引数（操作対象）
  │   └────── オプション（動作を変更）
  └────────── コマンド名
```

### オプションの書き方

```bash
# ショートオプション（ハイフン1つ + 1文字）
$ ls -l
$ ls -a
$ ls -la        # 複数を組み合わせる

# ロングオプション（ハイフン2つ + 単語）
$ ls --all
$ ls --help

# 値を取るオプション
$ head -n 5 file.txt
$ head --lines=5 file.txt
```

---

## 1.6 manコマンド（マニュアル）

`man`コマンドは、Linuxで最も重要な学習ツールの一つである。コマンドの詳細な使い方を確認できる。

### 基本的な使い方

```bash
# lsコマンドのマニュアルを表示
$ man ls

# セクションを指定して表示
$ man 5 passwd    # /etc/passwdの設定ファイルの説明

# キーワードで検索
$ man -k "copy files"
cp (1)    - copy files and directories
install (1) - copy files and set attributes
```

### manページ内の操作

| キー | 操作 |
|------|------|
| `Space` / `f` | 次のページへ |
| `b` | 前のページへ |
| `q` | 終了 |
| `/検索語` | 前方検索 |
| `?検索語` | 後方検索 |
| `n` | 次の検索結果へ |
| `N` | 前の検索結果へ |
| `g` | 先頭へ |
| `G` | 末尾へ |

### manページのセクション番号

| セクション | 内容 |
|------------|------|
| 1 | ユーザーコマンド |
| 2 | システムコール |
| 3 | ライブラリ関数 |
| 4 | スペシャルファイル（/dev配下） |
| 5 | ファイルフォーマット（設定ファイル等） |
| 6 | ゲーム |
| 7 | その他（規約、プロトコル等） |
| 8 | システム管理コマンド |

### その他のヘルプ取得方法

```bash
# --helpオプション（簡易ヘルプ）
$ ls --help
Usage: ls [OPTION]... [FILE]...
List information about the FILEs (the current directory by default).
...

# infoコマンド（詳細なドキュメント）
$ info coreutils

# whatis（コマンドの一行説明）
$ whatis ls
ls (1)    - list directory contents

# type（コマンドの種類を確認）
$ type ls
ls is aliased to `ls --color=auto'
$ type cd
cd is a shell builtin
$ type python3
python3 is /usr/bin/python3
```

---

## 1.7 まとめ

| 項目 | 覚えるべきこと |
|------|----------------|
| Linuxとは | オープンソースOS、サーバーで広く利用 |
| ディストリビューション | Ubuntu(初心者向け)、CentOS系(企業向け)、Debian(安定性重視) |
| カーネル | OSの中核、`uname -r`で確認 |
| シェル | bash/zshが主流、`echo $SHELL`で確認 |
| ターミナル | シェルにアクセスするGUIアプリ |
| manコマンド | `man コマンド名`で使い方を調べる |

### 次章の準備

次の章では、ファイルとディレクトリの操作を学ぶ。以下のコマンドを試しておこう：

```bash
$ pwd          # 現在のディレクトリを表示
$ ls           # ファイル一覧を表示
$ whoami       # 現在のユーザー名を表示
$ hostname     # ホスト名を表示
$ date         # 現在の日時を表示
$ cal          # カレンダーを表示
```
