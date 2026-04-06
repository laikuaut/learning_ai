# 実践課題04：DNS名前解決ツール ★2

> **難易度**: ★★☆☆☆（基礎）
> **前提知識**: 第5章（DNS）
> **課題の種類**: ミニプロジェクト
> **学習目標**: DNSの名前解決（Name Resolution）の仕組みを理解し、Pythonでドメイン名からIPアドレスを取得する正引き・逆引きツールを作る

---

## 完成イメージ

```
===== DNS名前解決ツール =====

1. 正引き（ドメイン名 → IPアドレス）
2. 逆引き（IPアドレス → ドメイン名）
3. 複数ドメインの一括正引き
4. 終了

選択: 1
ドメイン名を入力してください: www.example.com

【正引き結果】
  ドメイン名   : www.example.com
  IPアドレス   : 93.184.216.34
  エイリアス   : なし
  アドレス一覧 : 93.184.216.34

選択: 2
IPアドレスを入力してください: 8.8.8.8

【逆引き結果】
  IPアドレス   : 8.8.8.8
  ホスト名     : dns.google

選択: 3
ドメイン名をカンマ区切りで入力してください:
google.com, github.com, python.org

【一括正引き結果】
  ドメイン名         IPアドレス          応答時間
  ─────────────────────────────────────────────
  google.com         142.250.196.110     12ms
  github.com         20.27.177.113       15ms
  python.org         151.101.0.223       18ms
```

---

## 課題の要件

1. `socket` モジュールを使ってドメイン名からIPアドレスを取得する（正引き）
2. IPアドレスからドメイン名を取得する（逆引き）
3. 複数ドメインの一括解決と応答時間の計測を行う
4. エラー処理を適切に行う（存在しないドメインなど）
5. メニュー形式で繰り返し使えるようにする

---

## ステップガイド

<details>
<summary>ステップ1：正引きの基本</summary>

`socket.gethostbyname()` で最も基本的な正引きが行えます。
詳細情報が必要な場合は `socket.getaddrinfo()` を使います。

```python
import socket

# 基本的な正引き
ip = socket.gethostbyname("www.example.com")
print(f"IPアドレス: {ip}")

# 詳細な正引き
hostname, aliases, addresses = socket.gethostbyname_ex("www.example.com")
print(f"ホスト名: {hostname}")
print(f"エイリアス: {aliases}")
print(f"アドレス一覧: {addresses}")
```

</details>

<details>
<summary>ステップ2：逆引きの基本</summary>

`socket.gethostbyaddr()` でIPアドレスからホスト名を取得します。

```python
hostname, aliases, addresses = socket.gethostbyaddr("8.8.8.8")
print(f"ホスト名: {hostname}")
```

</details>

<details>
<summary>ステップ3：応答時間の計測</summary>

`time.time()` で前後の時刻を取得して差を計算します。

```python
import time

start = time.time()
ip = socket.gethostbyname("example.com")
elapsed_ms = (time.time() - start) * 1000
print(f"{elapsed_ms:.0f}ms")
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```python
# DNS名前解決ツール
# 学べる内容：DNSの正引き・逆引き、socketモジュール
# 実行方法：python dns_resolver.py

import socket
import time


def forward_lookup(domain):
    """正引き：ドメイン名 → IPアドレス"""
    try:
        hostname, aliases, addresses = socket.gethostbyname_ex(domain)
        print()
        print("【正引き結果】")
        print(f"  ドメイン名   : {domain}")
        print(f"  ホスト名     : {hostname}")
        if aliases:
            print(f"  エイリアス   : {', '.join(aliases)}")
        else:
            print(f"  エイリアス   : なし")
        print(f"  アドレス一覧 : {', '.join(addresses)}")
    except socket.gaierror:
        print(f"  エラー: '{domain}' を解決できません。ドメイン名を確認してください。")
    except socket.herror:
        print(f"  エラー: DNSサーバとの通信に失敗しました。")


def reverse_lookup(ip_address):
    """逆引き：IPアドレス → ドメイン名"""
    try:
        hostname, aliases, addresses = socket.gethostbyaddr(ip_address)
        print()
        print("【逆引き結果】")
        print(f"  IPアドレス   : {ip_address}")
        print(f"  ホスト名     : {hostname}")
        if aliases:
            print(f"  エイリアス   : {', '.join(aliases)}")
    except socket.herror:
        print(f"  エラー: '{ip_address}' の逆引きに失敗しました。")
    except socket.gaierror:
        print(f"  エラー: 無効なIPアドレスです。")


def batch_lookup(domains):
    """複数ドメインの一括正引き"""
    print()
    print("【一括正引き結果】")
    print(f"  {'ドメイン名':<22}{'IPアドレス':<22}{'応答時間'}")
    print(f"  {'─' * 55}")

    for domain in domains:
        domain = domain.strip()
        if not domain:
            continue
        try:
            start = time.time()
            ip = socket.gethostbyname(domain)
            elapsed_ms = (time.time() - start) * 1000
            print(f"  {domain:<22}{ip:<22}{elapsed_ms:.0f}ms")
        except socket.gaierror:
            print(f"  {domain:<22}{'解決失敗':<22}---")


# --- メイン処理 ---
print("===== DNS名前解決ツール =====")

while True:
    print()
    print("1. 正引き（ドメイン名 → IPアドレス）")
    print("2. 逆引き（IPアドレス → ドメイン名）")
    print("3. 複数ドメインの一括正引き")
    print("4. 終了")
    print()

    choice = input("選択: ").strip()

    if choice == "1":
        domain = input("ドメイン名を入力してください: ").strip()
        forward_lookup(domain)

    elif choice == "2":
        ip = input("IPアドレスを入力してください: ").strip()
        reverse_lookup(ip)

    elif choice == "3":
        domains_str = input("ドメイン名をカンマ区切りで入力してください:\n")
        domains = domains_str.split(",")
        batch_lookup(domains)

    elif choice == "4":
        print("終了します。")
        break

    else:
        print("1〜4の番号を入力してください。")
```

</details>

<details>
<summary>解答例（改良版 ─ 詳細情報と統計表示）</summary>

`getaddrinfo()` を使った詳細表示と、統計情報を追加したバージョンです。

```python
# DNS名前解決ツール（改良版）
# 学べる内容：DNS正引き・逆引き、getaddrinfo、応答時間計測
# 実行方法：python dns_resolver_v2.py

import socket
import time


def forward_lookup_detail(domain):
    """詳細な正引きを行う"""
    print(f"\n【正引き結果: {domain}】")

    # 基本的な正引き
    try:
        start = time.time()
        hostname, aliases, addresses = socket.gethostbyname_ex(domain)
        elapsed_ms = (time.time() - start) * 1000

        print(f"  ホスト名     : {hostname}")
        print(f"  エイリアス   : {', '.join(aliases) if aliases else 'なし'}")
        print(f"  IPv4アドレス : {', '.join(addresses)}")
        print(f"  応答時間     : {elapsed_ms:.1f}ms")
    except socket.gaierror as e:
        print(f"  エラー: {e}")
        return

    # getaddrinfoで追加情報を取得
    try:
        addr_infos = socket.getaddrinfo(domain, None)
        ip_set = set()
        for family, socktype, proto, canonname, sockaddr in addr_infos:
            ip = sockaddr[0]
            family_name = "IPv4" if family == socket.AF_INET else "IPv6"
            ip_set.add((family_name, ip))

        if ip_set:
            print()
            print("  【アドレス詳細】")
            for family_name, ip in sorted(ip_set):
                print(f"    {family_name}: {ip}")
    except socket.gaierror:
        pass


def reverse_lookup(ip_address):
    """逆引きを行う"""
    print(f"\n【逆引き結果: {ip_address}】")
    try:
        start = time.time()
        hostname, aliases, addresses = socket.gethostbyaddr(ip_address)
        elapsed_ms = (time.time() - start) * 1000

        print(f"  ホスト名     : {hostname}")
        print(f"  エイリアス   : {', '.join(aliases) if aliases else 'なし'}")
        print(f"  応答時間     : {elapsed_ms:.1f}ms")
    except socket.herror:
        print(f"  逆引きレコードが見つかりません。")
    except socket.gaierror:
        print(f"  無効なIPアドレスです。")


def batch_lookup(domains):
    """複数ドメインの一括正引きと統計"""
    results = []

    print(f"\n{'─' * 60}")
    print(f"  {'ドメイン名':<22}{'IPアドレス':<22}{'応答時間':>8}")
    print(f"{'─' * 60}")

    for domain in domains:
        domain = domain.strip()
        if not domain:
            continue
        try:
            start = time.time()
            ip = socket.gethostbyname(domain)
            elapsed_ms = (time.time() - start) * 1000
            results.append({"domain": domain, "ip": ip, "time_ms": elapsed_ms, "ok": True})
            print(f"  {domain:<22}{ip:<22}{elapsed_ms:>6.0f}ms")
        except socket.gaierror:
            results.append({"domain": domain, "ip": "", "time_ms": 0, "ok": False})
            print(f"  {domain:<22}{'--- 解決失敗 ---':<22}{'---':>8}")

    # 統計表示
    ok_results = [r for r in results if r["ok"]]
    if ok_results:
        times = [r["time_ms"] for r in ok_results]
        print(f"{'─' * 60}")
        print(f"\n【統計情報】")
        print(f"  成功: {len(ok_results)} / {len(results)}")
        print(f"  平均応答時間: {sum(times) / len(times):.1f}ms")
        print(f"  最速: {min(times):.1f}ms ({ok_results[times.index(min(times))]['domain']})")
        print(f"  最遅: {max(times):.1f}ms ({ok_results[times.index(max(times))]['domain']})")


def main():
    print("===== DNS名前解決ツール =====")

    while True:
        print("\n1. 正引き（詳細）  2. 逆引き  3. 一括正引き  4. 終了")
        choice = input("選択: ").strip()

        if choice == "1":
            domain = input("ドメイン名: ").strip()
            forward_lookup_detail(domain)
        elif choice == "2":
            ip = input("IPアドレス: ").strip()
            reverse_lookup(ip)
        elif choice == "3":
            domains_str = input("ドメイン名（カンマ区切り）:\n").strip()
            batch_lookup(domains_str.split(","))
        elif choice == "4":
            print("終了します。")
            break
        else:
            print("1〜4で選択してください。")


if __name__ == "__main__":
    main()
```

**初心者向けとの違い:**
- `getaddrinfo()` でIPv4/IPv6両方のアドレスを取得
- 一括正引きの統計情報（平均・最速・最遅）を表示
- 結果を辞書のリストで管理し、後から集計しやすい構造
- エラーハンドリングがより詳細

</details>
