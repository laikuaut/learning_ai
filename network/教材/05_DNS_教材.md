# 第5章：DNS（Domain Name System）

## この章のゴール

- DNSの役割と名前解決の仕組みを理解すること
- DNSの階層構造と権威DNSサーバ・キャッシュDNSサーバの違いを説明できること
- 主要なDNSレコード種別（A, AAAA, CNAME, MX, NS, TXT, SOA, PTR）を把握すること
- ゾーンとゾーン転送の仕組みを理解すること
- nslookup / dig コマンドを使ってDNSの問い合わせができること

---

## 5.1 DNSとは

### 5.1.1 名前解決の必要性

インターネット上の通信はIPアドレスで行われますが、人間が「93.184.216.34」のような数字の羅列を覚えるのは困難です。DNS（Domain Name System）は、人間が覚えやすい **ドメイン名**（例：`www.example.com`）を **IPアドレス** に変換する仕組みです。

```
【DNSの基本的な役割】

  ユーザ  →  「www.example.com にアクセスしたい」
     │
     ▼
  DNSサーバ  →  「www.example.com は 93.184.216.34 です」
     │
     ▼
  ブラウザ  →  93.184.216.34 に接続

  ドメイン名 → IPアドレス：正引き（Forward Lookup）
  IPアドレス → ドメイン名：逆引き（Reverse Lookup）
```

### 5.1.2 DNSが登場する前

DNS登場以前は **hosts ファイル** でホスト名とIPアドレスの対応を管理していました。

```
# hosts ファイルの例（今でもOSに存在する）
# Windows: C:\Windows\System32\drivers\etc\hosts
# Linux:   /etc/hosts

127.0.0.1       localhost
192.168.1.10    server1.local
192.168.1.20    server2.local
```

hosts ファイルの問題点：
- 全端末に同じ情報を配布する必要がある
- インターネット規模の数では管理不可能
- 変更の反映にタイムラグが生じる

これらの問題を解決するために、1983年にDNSが考案されました。

---

## 5.2 DNSの階層構造

### 5.2.1 ドメイン名の構造

ドメイン名は「.」（ドット）で区切られた階層構造を持ちます。右から左に向かって上位から下位となります。

```
【ドメイン名の階層構造】

  www.example.co.jp.
  │    │      │  │ │
  │    │      │  │ └─ ルートドメイン（"."  通常省略される）
  │    │      │  └─── TLD（トップレベルドメイン）: jp
  │    │      └────── SLD（セカンドレベルドメイン）: co
  │    └───────────── サードレベルドメイン: example
  └────────────────── ホスト名: www

  完全修飾ドメイン名（FQDN）: www.example.co.jp.
  ※ 末尾の「.」はルートを示す
```

### 5.2.2 ドメインの階層ツリー

```
                        . (ルート)
                       /  |  \
                     /    |    \
                   /      |      \
                 jp      com      org     ← TLD（トップレベルドメイン）
                / \      / \
              co  ac  example google     ← SLD（セカンドレベルドメイン）
             / \
        example  ...                     ← サードレベルドメイン
           |
          www                            ← ホスト名
```

### 5.2.3 TLD（トップレベルドメイン）の分類

| 分類 | 正式名称 | 例 | 説明 |
|------|---------|-----|------|
| **gTLD** | 汎用トップレベルドメイン | .com, .net, .org, .info | 用途別（地域に依存しない） |
| **ccTLD** | 国別コードトップレベルドメイン | .jp, .us, .uk, .cn | 国・地域別 |
| **新gTLD** | 新しい汎用TLD | .tokyo, .shop, .app | 2012年以降に追加 |
| **sTLD** | スポンサー付きTLD | .edu, .gov, .mil | 特定組織向け |

---

## 5.3 DNSサーバの種類

### 5.3.1 権威DNSサーバ（Authoritative DNS Server）

特定のゾーン（ドメイン）に関する **正式な情報** を保持し、問い合わせに応答するサーバです。

```
【権威DNSサーバの役割】

  「example.com のAレコードは？」
          │
          ▼
  ┌─────────────────────────┐
  │  権威DNSサーバ            │
  │  (example.com のゾーン)   │
  │                          │
  │  example.com → 93.184.216.34  │
  │  mail.example.com → 93.184.216.35  │
  │  （このゾーンの正式な回答）       │
  └─────────────────────────┘
```

### 5.3.2 キャッシュDNSサーバ（フルリゾルバ / Recursive Resolver）

クライアントからの問い合わせを受けて、ルートから順に権威DNSサーバに問い合わせを行い、結果をキャッシュして応答するサーバです。

```
【キャッシュDNSサーバの役割】

  クライアント → キャッシュDNSサーバ → ルートDNS
                                     → TLD DNS (.com)
                                     → 権威DNS (example.com)
                 ← 結果をキャッシュ  ← 最終回答
```

### 5.3.3 スタブリゾルバ

クライアントPC上で動作する、キャッシュDNSサーバに問い合わせを行うソフトウェアです。OSに組み込まれています。

| 種類 | 場所 | 役割 |
|------|------|------|
| **スタブリゾルバ** | クライアントPC | キャッシュDNSサーバに問い合わせを送る |
| **キャッシュDNSサーバ** | ISP / 社内 | 再帰的に名前解決を行い、結果をキャッシュ |
| **権威DNSサーバ** | ドメイン管理者 | ゾーンの正式なレコードを保持・回答 |

---

## 5.4 名前解決の流れ

### 5.4.1 再帰問い合わせと反復問い合わせ

```
【www.example.com の名前解決の流れ】

  ①クライアント（スタブリゾルバ）
     │  「www.example.com のIPアドレスは？」（再帰問い合わせ）
     ▼
  ②キャッシュDNSサーバ
     │  キャッシュに無い場合、反復問い合わせを開始
     │
     │── ③ ルートDNSサーバに問い合わせ ──→  「.com の権威DNSは？」
     │←── 「ns1.com のアドレスは x.x.x.x」 ──┘
     │
     │── ④ .com のDNSサーバに問い合わせ ──→  「example.com の権威DNSは？」
     │←── 「ns1.example.com は y.y.y.y」 ──┘
     │
     │── ⑤ example.com の権威DNSに問い合わせ →  「www.example.com のIPは？」
     │←── 「93.184.216.34」 ────────────────┘
     │
     ▼
  ⑥クライアントに最終回答を返す
     「www.example.com は 93.184.216.34 です」
```

| 問い合わせ方式 | 説明 | 使われる場面 |
|--------------|------|-------------|
| **再帰問い合わせ（Recursive Query）** | 最終的な回答を求める。回答が得られるまでサーバが代行して調べる | クライアント → キャッシュDNS |
| **反復問い合わせ（Iterative Query）** | 知っている範囲の情報（次に問い合わせるべきサーバ）を返す | キャッシュDNS → 各権威DNS |

### 5.4.2 DNSキャッシュとTTL

名前解決の結果は、**TTL（Time To Live）**で指定された時間だけキャッシュされます。

```
【キャッシュの仕組み】

  1回目の問い合わせ: ルートDNS → TLD DNS → 権威DNS と順にたどる（遅い）
  2回目以降:         キャッシュから即座に回答（高速）

  TTL = 3600（秒）の場合:
  ├─ キャッシュ登録時刻:  10:00:00
  ├─ キャッシュ有効期限:  11:00:00（3600秒後）
  └─ 11:00:00 以降に問い合わせがあれば再度権威DNSへ問い合わせ
```

> **現場の知識**: TTLを短くするとDNS変更が素早く反映されますが、DNSサーバへの問い合わせが増えます。一般的に本番環境では3600秒（1時間）～86400秒（1日）、DNS切り替え前には300秒（5分）程度に短縮するのが定石です。

---

## 5.5 DNSレコードの種類

### 5.5.1 主要なレコードタイプ

| レコード | 正式名称 | 用途 | 例 |
|---------|---------|------|-----|
| **A** | Address | ドメイン名 → IPv4アドレス | `example.com. IN A 93.184.216.34` |
| **AAAA** | Quad-A | ドメイン名 → IPv6アドレス | `example.com. IN AAAA 2606:2800:220:1::` |
| **CNAME** | Canonical Name | ドメイン名の別名（エイリアス） | `www.example.com. IN CNAME example.com.` |
| **MX** | Mail Exchange | メールサーバの指定 | `example.com. IN MX 10 mail.example.com.` |
| **NS** | Name Server | 権威DNSサーバの指定 | `example.com. IN NS ns1.example.com.` |
| **TXT** | Text | テキスト情報（SPF、DKIM等） | `example.com. IN TXT "v=spf1 ..."` |
| **SOA** | Start of Authority | ゾーンの管理情報 | シリアル番号、リフレッシュ間隔等 |
| **PTR** | Pointer | IPアドレス → ドメイン名（逆引き） | `34.216.184.93.in-addr.arpa. IN PTR example.com.` |
| **SRV** | Service | サービスのホスト・ポート情報 | `_sip._tcp.example.com. IN SRV ...` |

### 5.5.2 レコードの詳細

**Aレコード**：最も基本的なレコードで、ドメイン名をIPv4アドレスに対応付けます。

```
; Aレコードの例
example.com.       IN  A     93.184.216.34
www.example.com.   IN  A     93.184.216.34
api.example.com.   IN  A     93.184.216.35
```

**CNAMEレコード**：別名（エイリアス）を定義します。CNAMEで指定された名前は、さらにAレコードで解決されます。

```
; CNAMEレコードの例
www.example.com.    IN  CNAME  example.com.
; www.example.com → example.com → 93.184.216.34 と2段階で解決

; よくある間違い: CNAMEとAレコードを同じ名前に共存させてはいけない
; NG: example.com. IN CNAME other.example.com.
;     example.com. IN A     1.2.3.4
```

**MXレコード**：メールの配送先を指定します。優先度（数値が小さいほど優先）を持ちます。

```
; MXレコードの例
example.com.  IN  MX  10  mail1.example.com.   ; 優先（プライマリ）
example.com.  IN  MX  20  mail2.example.com.   ; 次善（セカンダリ）
```

**SOAレコード**：ゾーンの管理情報を定義する、ゾーンファイルの先頭に必ず存在するレコードです。

```
; SOAレコードの例
example.com.  IN  SOA  ns1.example.com. admin.example.com. (
    2024010101  ; シリアル番号（ゾーンの更新を示す）
    3600        ; リフレッシュ間隔（セカンダリが更新確認する間隔）
    900         ; リトライ間隔（リフレッシュ失敗時の再試行間隔）
    604800      ; 有効期限（セカンダリのデータ有効期限）
    86400       ; ネガティブキャッシュTTL（存在しないレコードのキャッシュ時間）
)
```

---

## 5.6 ゾーンとゾーン転送

### 5.6.1 ゾーンとは

**ゾーン（Zone）**とは、権威DNSサーバが管理する範囲のことです。ドメインとゾーンは似ていますが、サブドメインの管理を委任した場合は別のゾーンになります。

```
【ドメインとゾーンの違い】

  example.com ドメイン
  ├── www.example.com      ─┐
  ├── mail.example.com      ├─ example.com ゾーン
  ├── api.example.com      ─┘
  └── sub.example.com      ─── sub.example.com ゾーン（委任）
       ├── www.sub.example.com     別の権威DNSサーバが管理
       └── app.sub.example.com
```

### 5.6.2 ゾーン転送（Zone Transfer）

可用性を確保するため、権威DNSサーバはプライマリ（マスター）とセカンダリ（スレーブ）の構成をとります。ゾーン転送は、プライマリからセカンダリにゾーンデータをコピーする仕組みです。

```
【ゾーン転送の流れ】

  ┌────────────────┐          ┌────────────────┐
  │ プライマリDNS    │          │ セカンダリDNS    │
  │ (マスター)       │          │ (スレーブ)       │
  │                 │          │                 │
  │ ゾーンファイル   │  AXFR/   │ ゾーンファイル   │
  │ (正本)          │──IXFR──→│ (複製)          │
  └────────────────┘          └────────────────┘

  AXFR: フルゾーン転送（全レコードを転送）
  IXFR: 差分ゾーン転送（変更分のみ転送）
```

| 項目 | AXFR | IXFR |
|------|------|------|
| 転送方式 | 全レコード | 差分のみ |
| 転送量 | 大 | 小 |
| 使用場面 | 初回同期、大幅変更時 | 通常の更新時 |
| プロトコル | TCP（ポート53） | TCP（ポート53） |

> **セキュリティ上の注意**: ゾーン転送を許可するサーバを制限しないと、外部からゾーンの全レコードを取得される危険があります。ACL（アクセス制御リスト）で転送先を限定してください。

---

## 5.7 DNSに関連するセキュリティ

### 5.7.1 DNSキャッシュポイズニング

キャッシュDNSサーバに偽のレコードを注入し、ユーザを偽サイトに誘導する攻撃です。

```
【DNSキャッシュポイズニングの攻撃フロー】

  ① ユーザが www.bank.example.com を問い合わせ
  ② キャッシュDNSサーバが権威DNSに問い合わせ
  ③ 攻撃者が権威DNSより先に偽の応答を送信
     「www.bank.example.com は 攻撃者IP です」
  ④ キャッシュDNSが偽情報をキャッシュ
  ⑤ 以降、全ユーザが偽サイトに誘導される

  対策: DNSSEC（DNS Security Extensions）
        ソースポートランダム化
        応答の検証
```

### 5.7.2 DNSSEC（DNS Security Extensions）

DNSの応答にデジタル署名を付与し、応答の正当性を検証できるようにする仕組みです。

### 5.7.3 DNS over HTTPS (DoH) / DNS over TLS (DoT)

| 方式 | ポート | 説明 |
|------|--------|------|
| **従来のDNS** | 53 (UDP/TCP) | 平文で通信（盗聴可能） |
| **DoT** | 853 (TCP) | TLSで暗号化 |
| **DoH** | 443 (TCP) | HTTPS上でDNS問い合わせ |

---

## 5.8 nslookup / dig コマンド

### 5.8.1 nslookup コマンド

Windows / Linux / macOS で使用可能な名前解決ツールです。

```
# 基本的な正引き
> nslookup www.example.com
Server:    192.168.1.1          ← 使用しているDNSサーバ
Address:   192.168.1.1#53

Non-authoritative answer:       ← キャッシュからの応答
Name:    www.example.com
Address: 93.184.216.34

# 特定のDNSサーバを指定して問い合わせ
> nslookup www.example.com 8.8.8.8

# レコードタイプを指定
> nslookup -type=MX example.com
example.com     mail exchanger = 10 mail.example.com.

# 逆引き
> nslookup 93.184.216.34
```

### 5.8.2 dig コマンド

Linux / macOS で使用できる、より詳細なDNS問い合わせツールです（Windowsでは別途インストールが必要）。

```
# 基本的な正引き
$ dig www.example.com

;; QUESTION SECTION:
;www.example.com.       IN      A

;; ANSWER SECTION:
www.example.com.  3600  IN      A       93.184.216.34

;; Query time: 25 msec
;; SERVER: 192.168.1.1#53(192.168.1.1)

# MXレコードの問い合わせ
$ dig example.com MX

# 権威DNSサーバを直接指定
$ dig @ns1.example.com www.example.com

# 短縮出力
$ dig +short www.example.com
93.184.216.34

# 名前解決の過程を追跡（トレース）
$ dig +trace www.example.com
; 「.」→「com.」→「example.com.」の順にたどる様子が表示される

# 逆引き
$ dig -x 93.184.216.34

# ゾーン転送の試行（セキュリティテスト）
$ dig @ns1.example.com example.com AXFR
```

### 5.8.3 出力の読み方（dig）

```
$ dig www.example.com

; <<>> DiG 9.18.18 <<>> www.example.com
;; global options: +cmd

;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 12345
;; flags: qr rd ra; QUERY: 1, ANSWER: 1, AUTHORITY: 0, ADDITIONAL: 1

;; QUESTION SECTION:          ← 問い合わせ内容
;www.example.com.       IN      A

;; ANSWER SECTION:            ← 回答
www.example.com.  3600  IN      A       93.184.216.34
│                 │     │       │       └─ IPアドレス
│                 │     │       └── レコードタイプ
│                 │     └── クラス（IN = Internet）
│                 └── TTL（秒）
└── ドメイン名

;; Query time: 25 msec       ← 応答時間
;; SERVER: 192.168.1.1#53    ← 使用したDNSサーバ
;; WHEN: Mon Jan 01 10:00:00 JST 2024
;; MSG SIZE  rcvd: 62        ← 応答メッセージサイズ
```

---

## 5.9 まとめ

### ポイントまとめ

1. **DNS** はドメイン名をIPアドレスに変換する仕組みで、インターネットの根幹技術です
2. **階層構造**：ルート → TLD → SLD → ... と階層的に管理されています
3. **権威DNSサーバ** はゾーンの正式な情報を保持し、**キャッシュDNSサーバ** はクライアントに代わって名前解決を行います
4. **再帰問い合わせ**（クライアント→キャッシュDNS）と **反復問い合わせ**（キャッシュDNS→権威DNS）の違いを理解しましょう
5. **主要なレコード**：A（IPv4）、AAAA（IPv6）、CNAME（別名）、MX（メール）、NS（ネームサーバ）、SOA（ゾーン管理）、PTR（逆引き）
6. **TTL** によってキャッシュの有効期限が管理されます
7. **DNSSEC** でDNS応答の正当性を検証し、キャッシュポイズニングを防止できます

### 試験対策キーワード

- DNS、名前解決、正引き、逆引き
- FQDN、ドメイン、ゾーン
- 権威DNSサーバ、キャッシュDNSサーバ、スタブリゾルバ
- 再帰問い合わせ、反復問い合わせ
- A、AAAA、CNAME、MX、NS、SOA、PTR、TXT
- ゾーン転送（AXFR / IXFR）
- DNSキャッシュポイズニング、DNSSEC
- nslookup、dig

---

## 確認問題

1. DNSにおける「正引き」と「逆引き」の違いを説明してください。
2. 権威DNSサーバとキャッシュDNSサーバの役割の違いを述べてください。
3. 再帰問い合わせと反復問い合わせの違いを、それぞれどの場面で使われるかを含めて説明してください。
4. MXレコードの優先度（プリファレンス値）はどのように解釈されますか。
5. DNSキャッシュポイズニング攻撃の仕組みと対策を説明してください。

---

**前章**: [第4章：TCP と UDP](./04_TCP_UDP_教材.md)
**次章**: [第6章：HTTP](./06_HTTP_教材.md)
