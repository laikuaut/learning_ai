# 第5章：DNS 演習問題

## 基本問題

### 問題5-1：DNSの基本概念
以下の用語を説明してください。

1. 正引き
2. 逆引き
3. FQDN
4. TTL
5. ゾーン

<details>
<summary>解答</summary>

1. **正引き（Forward Lookup）**：ドメイン名からIPアドレスを求めること。例：www.example.com → 93.184.216.34

2. **逆引き（Reverse Lookup）**：IPアドレスからドメイン名を求めること。例：93.184.216.34 → www.example.com。PTRレコードを使用

3. **FQDN（Fully Qualified Domain Name / 完全修飾ドメイン名）**：ルートドメインまで含む完全なドメイン名。例：`www.example.com.`（末尾のドットがルートを示す）

4. **TTL（Time To Live）**：DNSキャッシュの有効期限（秒単位）。この時間が経過するとキャッシュが破棄され、再度権威DNSサーバに問い合わせが行われる

5. **ゾーン（Zone）**：権威DNSサーバが管理する範囲。ドメインの一部または全体を管理単位としてまとめたもの

</details>

### 問題5-2：DNSレコードの種類
以下のDNSレコードタイプの用途を答えてください。

1. Aレコード
2. AAAAレコード
3. CNAMEレコード
4. MXレコード
5. NSレコード
6. PTRレコード
7. SOAレコード
8. TXTレコード

<details>
<summary>解答</summary>

1. **Aレコード**：ドメイン名をIPv4アドレスに対応付ける
2. **AAAAレコード**：ドメイン名をIPv6アドレスに対応付ける
3. **CNAMEレコード**：ドメイン名の別名（エイリアス）を定義する
4. **MXレコード**：メールの配送先サーバを指定する（優先度付き）
5. **NSレコード**：ゾーンの権威DNSサーバを指定する
6. **PTRレコード**：IPアドレスからドメイン名への逆引きに使用
7. **SOAレコード**：ゾーンの管理情報（シリアル番号、リフレッシュ間隔等）を定義
8. **TXTレコード**：テキスト情報を格納（SPFレコード、DKIM、ドメイン所有権の証明等に使用）

</details>

### 問題5-3：DNSサーバの種類
権威DNSサーバとキャッシュDNSサーバ（フルリゾルバ）の違いを説明してください。

<details>
<summary>解答</summary>

| 項目 | 権威DNSサーバ | キャッシュDNSサーバ |
|------|-------------|-------------------|
| 役割 | 特定のゾーンの正式なレコードを保持・回答 | クライアントの代理で名前解決を行い結果をキャッシュ |
| データの出所 | 自身が管理するゾーンファイル（正式情報） | 権威DNSサーバから取得した情報のキャッシュ |
| 問い合わせ方式 | 反復問い合わせを受けて回答 | 再帰問い合わせを受けて代理で解決 |
| 運用者 | ドメインの管理者 | ISP、企業のネットワーク管理者 |
| 例 | ns1.example.com | ISPのDNSサーバ、8.8.8.8（Google Public DNS） |

</details>

### 問題5-4：名前解決の流れ
「www.example.co.jp」の名前解決の流れを、キャッシュDNSサーバの動作を中心に順番に説明してください。（キャッシュに情報がない場合）

<details>
<summary>解答</summary>

1. クライアント（スタブリゾルバ）がキャッシュDNSサーバに **再帰問い合わせ** を送信：「www.example.co.jp のIPアドレスは？」

2. キャッシュDNSサーバが **ルートDNSサーバ** に反復問い合わせ：「www.example.co.jp は？」
   → ルートDNS：「jp の権威DNSサーバは ns1.jp です」

3. キャッシュDNSサーバが **jp のDNSサーバ** に反復問い合わせ：「www.example.co.jp は？」
   → jp DNS：「co.jp の権威DNSサーバは ns1.co.jp です」

4. キャッシュDNSサーバが **co.jp のDNSサーバ** に反復問い合わせ：「www.example.co.jp は？」
   → co.jp DNS：「example.co.jp の権威DNSサーバは ns1.example.co.jp です」

5. キャッシュDNSサーバが **example.co.jp の権威DNSサーバ** に反復問い合わせ：「www.example.co.jp は？」
   → 権威DNS：「www.example.co.jp は 198.51.100.10 です」

6. キャッシュDNSサーバが結果を **キャッシュに保存**（TTLの期間）し、クライアントに回答

</details>

---

## 応用問題

### 問題5-5：DNSレコードの設定
以下の要件を満たすDNSゾーンファイルの設定を記述してください。

- ドメイン：mysite.example.com
- WebサーバのIP：198.51.100.10
- メールサーバのIP：198.51.100.20
- www.mysite.example.com は mysite.example.com の別名
- メールサーバの優先度は10

<details>
<summary>解答</summary>

```
; mysite.example.com のゾーンファイル

; SOAレコード
mysite.example.com.  IN  SOA  ns1.mysite.example.com. admin.mysite.example.com. (
    2024010101  ; シリアル番号
    3600        ; リフレッシュ
    900         ; リトライ
    604800      ; 有効期限
    86400       ; ネガティブキャッシュTTL
)

; NSレコード（権威DNSサーバ）
mysite.example.com.  IN  NS  ns1.mysite.example.com.

; Aレコード（ドメイン → IPアドレス）
mysite.example.com.       IN  A   198.51.100.10
ns1.mysite.example.com.   IN  A   198.51.100.30
mail.mysite.example.com.  IN  A   198.51.100.20

; CNAMEレコード（別名）
www.mysite.example.com.   IN  CNAME  mysite.example.com.

; MXレコード（メールサーバ）
mysite.example.com.       IN  MX  10  mail.mysite.example.com.
```

</details>

### 問題5-6：nslookup / dig の読み方
以下の dig コマンドの出力を解釈してください。

```
$ dig example.com MX

;; ANSWER SECTION:
example.com.    3600  IN  MX  10  mail1.example.com.
example.com.    3600  IN  MX  20  mail2.example.com.

;; ADDITIONAL SECTION:
mail1.example.com.  3600  IN  A  198.51.100.10
mail2.example.com.  3600  IN  A  198.51.100.20
```

(1) example.com のプライマリメールサーバはどれですか。
(2) TTLは何秒ですか。
(3) mail2.example.com のIPアドレスは何ですか。
(4) mail1.example.com がダウンした場合、メールはどこに配送されますか。

<details>
<summary>解答</summary>

(1) **mail1.example.com** がプライマリメールサーバです。MXレコードの優先度は値が小さいほど優先されるため、10のmail1が20のmail2より優先されます。

(2) TTLは **3600秒（1時間）** です。キャッシュDNSサーバはこの期間、結果をキャッシュします。

(3) mail2.example.com のIPアドレスは **198.51.100.20** です（ADDITIONALセクションに記載）。

(4) mail1.example.com がダウンした場合、次に優先度の高い **mail2.example.com（198.51.100.20）** にメールが配送されます。MXレコードの複数設定はメールの冗長性確保のために使用されます。

</details>

### 問題5-7：DNSセキュリティ
DNSキャッシュポイズニング攻撃の仕組みを説明し、対策を3つ挙げてください。

<details>
<summary>解答</summary>

**DNSキャッシュポイズニングの仕組み：**

1. キャッシュDNSサーバが権威DNSサーバに問い合わせを行う
2. 正規の応答が返ってくる前に、攻撃者が偽の応答を送信する
3. キャッシュDNSサーバが偽の応答をキャッシュに保存してしまう
4. 以降、このキャッシュDNSサーバを利用する全ユーザが偽サイトに誘導される

**対策：**

1. **DNSSEC（DNS Security Extensions）**：DNS応答にデジタル署名を付与し、応答の正当性と完全性を検証できるようにする

2. **ソースポートランダム化**：DNS問い合わせの送信元ポートをランダム化し、攻撃者が正しいポートを推測しにくくする（Kaminsky攻撃への対策）

3. **DNS over HTTPS（DoH）/ DNS over TLS（DoT）**：DNS通信を暗号化し、中間者攻撃や盗聴を防止する

（他にも：問い合わせIDのランダム化、キャッシュDNSサーバへのアクセス制限、応答検証の強化 等）

</details>

---

## チャレンジ問題

### 問題5-8：DNS設計問題
ある企業が以下のサーバ構成を持つ場合、DNS設計について考えてください。

- ドメイン：corp.example.co.jp
- 外部公開Webサーバ：198.51.100.10
- 社内専用Webサーバ：192.168.1.10
- メールサーバ（プライマリ）：198.51.100.20
- メールサーバ（セカンダリ）：198.51.100.21

(1) 外部向けと内部向けでDNSの応答を分ける仕組みの名称を答えてください。
(2) 外部向けDNSと内部向けDNSでwww.corp.example.co.jpの解決結果がどう異なるか説明してください。
(3) ゾーン転送のセキュリティについて注意すべき点を述べてください。

<details>
<summary>解答</summary>

**(1)** **スプリットDNS（Split DNS）** またはスプリットホライズンDNSと呼ばれます。

**(2)**
- **外部向けDNS**：www.corp.example.co.jp → **198.51.100.10**（グローバルIP、外部公開Webサーバ）
- **内部向けDNS**：www.corp.example.co.jp → **192.168.1.10**（プライベートIP、社内Webサーバ）

社内ユーザは内部DNSを参照するため、直接社内サーバにアクセスでき、ファイアウォールやNATを経由する必要がなくなります。外部ユーザは外部DNSを参照し、公開用サーバにアクセスします。

**(3)** ゾーン転送のセキュリティに関する注意点：
- ゾーン転送（AXFR/IXFR）はセカンダリDNSサーバのみに許可し、それ以外からの転送要求は拒否する（ACLで制限）
- 制限しないと、攻撃者がゾーンの全レコードを取得でき、サーバ構成が漏洩する
- ゾーン転送にはTSIG（Transaction Signature）による認証を使用することが推奨される

</details>

### 問題5-9：トラブルシューティング
「Webサイトにアクセスできない」という問い合わせに対し、DNS関連の原因を調査するための手順を、使用するコマンドとともに説明してください。

<details>
<summary>解答</summary>

**調査手順：**

1. **DNS名前解決の確認**
   ```
   nslookup www.example.com
   ```
   - 正常に応答があるか確認。応答がない場合はDNSに問題がある

2. **別のDNSサーバで確認**
   ```
   nslookup www.example.com 8.8.8.8
   ```
   - 社内DNSの問題か、ドメイン自体の問題かを切り分け

3. **DNSサーバへの到達性確認**
   ```
   ping 設定されているDNSサーバのIP
   ```
   - DNSサーバに到達できない場合はネットワークの問題

4. **IPアドレスでの直接アクセス確認**
   - IPアドレスが判明している場合、ブラウザでIPアドレスを直接指定してアクセス
   - アクセスできればDNSの問題、できなければDNS以外の問題

5. **詳細な調査（dig コマンド）**
   ```
   dig +trace www.example.com
   ```
   - どの段階で名前解決が失敗しているかを特定

6. **hosts ファイルの確認**
   - hostsファイルに不正なエントリがないか確認（マルウェアが書き換える場合がある）

</details>
