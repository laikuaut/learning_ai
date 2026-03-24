# ==============================
# 暗号アルゴリズム体験
# 応用情報技術者：情報セキュリティ
# ==============================
# 学べる内容:
#   - 共通鍵暗号（シーザー暗号、XOR暗号）
#   - 公開鍵暗号（RSA暗号）の仕組み
#   - RSAの鍵生成・暗号化・復号を小さな素数で体験
#   - 素因数分解の困難性が安全性の根拠であること
#   - ハッシュ関数の基本
#   - デジタル署名の仕組み
#   - 応用情報技術者試験の情報セキュリティ問題への対応力
#
# 実行方法:
#   python 05_暗号アルゴリズム体験.py
# ==============================

import random
import hashlib


# ============================================================
# 1. 共通鍵暗号（対称鍵暗号）
# ============================================================

def caesar_encrypt(plaintext, shift):
    """シーザー暗号で暗号化します（アルファベットのみ対象）"""
    result = ""
    for char in plaintext:
        if char.isalpha():
            base = ord("A") if char.isupper() else ord("a")
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result


def caesar_decrypt(ciphertext, shift):
    """シーザー暗号を復号します"""
    return caesar_encrypt(ciphertext, -shift)


def xor_encrypt(plaintext, key):
    """XOR暗号で暗号化/復号します（XORは暗号化と復号が同じ操作です）"""
    result = []
    for i, char in enumerate(plaintext):
        key_char = key[i % len(key)]
        xored = ord(char) ^ ord(key_char)
        result.append(xored)
    return result


def xor_decrypt(cipher_values, key):
    """XOR暗号を復号します"""
    result = ""
    for i, val in enumerate(cipher_values):
        key_char = key[i % len(key)]
        result += chr(val ^ ord(key_char))
    return result


# ============================================================
# 2. RSA暗号
# ============================================================

def is_prime(n):
    """素数判定を行います"""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def gcd(a, b):
    """最大公約数（GCD）をユークリッドの互除法で求めます"""
    while b:
        a, b = b, a % b
    return a


def extended_gcd(a, b):
    """拡張ユークリッド互除法: ax + by = gcd(a,b) を満たす x, y を求めます"""
    if a == 0:
        return b, 0, 1
    g, x, y = extended_gcd(b % a, a)
    return g, y - (b // a) * x, x


def mod_inverse(e, phi):
    """モジュラ逆元を求めます: e * d ≡ 1 (mod phi)"""
    g, x, _ = extended_gcd(e % phi, phi)
    if g != 1:
        return None  # 逆元が存在しません
    return x % phi


def generate_rsa_keys(p, q, verbose=True):
    """RSA鍵ペアを生成します（小さな素数で体験用）

    手順:
    1. 2つの素数 p, q を選びます
    2. n = p × q を計算します
    3. φ(n) = (p-1)(q-1) を計算します（オイラーのトーシェント関数）
    4. gcd(e, φ(n)) = 1 となる e を選びます（公開指数）
    5. e × d ≡ 1 (mod φ(n)) となる d を求めます（秘密指数）
    """
    if verbose:
        print(f"\n  ━━━ RSA鍵生成の手順 ━━━")

    # ステップ1: 素数の確認
    if not is_prime(p) or not is_prime(q):
        print(f"  ※ p={p}, q={q} は両方とも素数である必要があります。")
        return None

    if verbose:
        print(f"  ステップ1: 2つの素数を選びます")
        print(f"    p = {p}")
        print(f"    q = {q}")

    # ステップ2: n = p × q
    n = p * q
    if verbose:
        print(f"\n  ステップ2: n = p × q を計算します")
        print(f"    n = {p} × {q} = {n}")

    # ステップ3: φ(n) = (p-1)(q-1)
    phi = (p - 1) * (q - 1)
    if verbose:
        print(f"\n  ステップ3: φ(n) = (p-1)(q-1) を計算します")
        print(f"    φ({n}) = ({p}-1)({q}-1) = {p-1} × {q-1} = {phi}")

    # ステップ4: 公開指数 e を選びます
    e = 0
    for candidate in [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 65537]:
        if candidate < phi and gcd(candidate, phi) == 1:
            e = candidate
            break

    if e == 0:
        print("  ※ 適切な公開指数が見つかりませんでした。")
        return None

    if verbose:
        print(f"\n  ステップ4: gcd(e, φ(n)) = 1 となる e を選びます")
        print(f"    e = {e}")
        print(f"    gcd({e}, {phi}) = {gcd(e, phi)} ✓")

    # ステップ5: 秘密指数 d を求めます
    d = mod_inverse(e, phi)
    if d is None:
        print("  ※ モジュラ逆元が見つかりませんでした。")
        return None

    if verbose:
        print(f"\n  ステップ5: e × d ≡ 1 (mod φ(n)) となる d を求めます")
        print(f"    d = {d}")
        print(f"    検算: {e} × {d} = {e * d} = {phi} × {e * d // phi} + {e * d % phi}")
        print(f"    {e} × {d} mod {phi} = {(e * d) % phi} ✓")

    if verbose:
        print(f"\n  ━━━ 生成された鍵ペア ━━━")
        print(f"    公開鍵: (e={e}, n={n})")
        print(f"    秘密鍵: (d={d}, n={n})")
        print(f"\n  ■ セキュリティの根拠")
        print(f"    n={n} を知っていても、p={p} と q={q} への")
        print(f"    素因数分解が困難であれば、d は求められません。")
        print(f"    （この例では n が小さいので簡単ですが、")
        print(f"     実際のRSAでは n は2048ビット以上の巨大な数です）")

    return {"p": p, "q": q, "n": n, "phi": phi, "e": e, "d": d}


def rsa_encrypt(message, e, n, verbose=True):
    """RSA暗号化: C = M^e mod n"""
    if message >= n:
        print(f"  ※ メッセージ({message})は n({n})未満である必要があります。")
        return None

    cipher = pow(message, e, n)

    if verbose:
        print(f"\n  ■ RSA暗号化")
        print(f"    平文 M = {message}")
        print(f"    公開鍵 (e={e}, n={n})")
        print(f"    暗号文 C = M^e mod n = {message}^{e} mod {n}")

        # 計算過程（小さな数の場合のみ）
        if message < 100 and e < 100:
            raw = message ** e
            print(f"    {message}^{e} = {raw}")
            print(f"    {raw} mod {n} = {cipher}")

        print(f"    → 暗号文 C = {cipher}")

    return cipher


def rsa_decrypt(cipher, d, n, verbose=True):
    """RSA復号: M = C^d mod n"""
    message = pow(cipher, d, n)

    if verbose:
        print(f"\n  ■ RSA復号")
        print(f"    暗号文 C = {cipher}")
        print(f"    秘密鍵 (d={d}, n={n})")
        print(f"    平文 M = C^d mod n = {cipher}^{d} mod {n}")
        print(f"    → 平文 M = {message}")

    return message


def rsa_sign(message, d, n, verbose=True):
    """RSAデジタル署名: S = M^d mod n（秘密鍵で署名します）"""
    signature = pow(message, d, n)

    if verbose:
        print(f"\n  ■ デジタル署名の作成")
        print(f"    メッセージ M = {message}")
        print(f"    秘密鍵で署名: S = M^d mod n = {message}^{d} mod {n}")
        print(f"    → 署名 S = {signature}")

    return signature


def rsa_verify(message, signature, e, n, verbose=True):
    """RSA署名検証: M' = S^e mod n、M' == M なら検証成功です"""
    recovered = pow(signature, e, n)

    if verbose:
        print(f"\n  ■ デジタル署名の検証")
        print(f"    署名 S = {signature}")
        print(f"    公開鍵で検証: M' = S^e mod n = {signature}^{e} mod {n}")
        print(f"    → 復元値 M' = {recovered}")
        print(f"    元のメッセージ M = {message}")
        if recovered == message:
            print(f"    → M' == M → 署名は有効です ✓")
        else:
            print(f"    → M' != M → 署名は無効です ✗")

    return recovered == message


# ============================================================
# 3. ハッシュ関数
# ============================================================

def simple_hash(data, mod=256):
    """簡易ハッシュ関数（教育用）です"""
    h = 0
    for char in data:
        h = (h * 31 + ord(char)) % mod
    return h


def demonstrate_hash():
    """ハッシュ関数の特性をデモンストレーションします"""
    print("\n  ━━━ ハッシュ関数の特性 ━━━")
    print("  ハッシュ関数は任意の長さのデータを固定長の値に変換します")

    test_data = [
        "Hello",
        "Hello!",
        "hello",
        "Hello World",
        "A" * 100,
        "B" * 100,
    ]

    print(f"\n  ■ 同じデータ → 同じハッシュ（一貫性）")
    print(f"  ■ 少しでも違うデータ → 全く異なるハッシュ（雪崩効果）")
    print(f"\n    {'入力':<16} {'簡易ハッシュ':>12} {'SHA-256 (先頭16文字)'}")
    print("    " + "-" * 52)

    for data in test_data:
        simple_h = simple_hash(data)
        sha256_h = hashlib.sha256(data.encode()).hexdigest()[:16]
        display_data = data if len(data) <= 14 else data[:11] + "..."
        print(f"    {display_data:<16} {simple_h:>12} {sha256_h}")

    print(f"\n  ■ ハッシュ関数の用途")
    print(f"    - パスワードの保存（元のパスワードを保存しない）")
    print(f"    - データの改ざん検知（ハッシュ値の比較）")
    print(f"    - デジタル署名（メッセージのハッシュに署名する）")


# ============================================================
# 対話モード
# ============================================================

def interactive_mode():
    """対話型の暗号アルゴリズム体験です"""
    print("\n" + "=" * 55)
    print("  暗号アルゴリズム体験 - 対話モード")
    print("=" * 55)
    print("  操作を選んでください:")
    print("    1. シーザー暗号")
    print("    2. XOR暗号")
    print("    3. RSA鍵生成")
    print("    4. RSA暗号化・復号")
    print("    5. RSAデジタル署名")
    print("    6. ハッシュ値の計算")
    print("    0. 終了")
    print("-" * 55)

    rsa_keys = None

    while True:
        choice = input("\n  選択 (0-6): ").strip()

        if choice == "0":
            print("  暗号アルゴリズム体験を終了します。")
            break

        elif choice == "1":
            text = input("  テキスト: ").strip()
            try:
                shift = int(input("  シフト数 (1-25): "))
                encrypted = caesar_encrypt(text, shift)
                decrypted = caesar_decrypt(encrypted, shift)
                print(f"  暗号化: {text} → {encrypted}")
                print(f"  復号:   {encrypted} → {decrypted}")
            except ValueError:
                print("  ※ 正しい数値を入力してください。")

        elif choice == "2":
            text = input("  テキスト: ").strip()
            key = input("  鍵（文字列）: ").strip()
            if key:
                encrypted = xor_encrypt(text, key)
                encrypted_hex = " ".join(f"{v:02X}" for v in encrypted)
                decrypted = xor_decrypt(encrypted, key)
                print(f"  暗号化: {encrypted_hex}")
                print(f"  復号:   {decrypted}")
            else:
                print("  ※ 鍵を入力してください。")

        elif choice == "3":
            try:
                p = int(input("  素数 p (例: 61): "))
                q = int(input("  素数 q (例: 53): "))
                rsa_keys = generate_rsa_keys(p, q)
            except ValueError:
                print("  ※ 正しい整数を入力してください。")

        elif choice == "4":
            if rsa_keys is None:
                print("  ※ 先にRSA鍵を生成してください（選択肢3）。")
                continue
            try:
                msg = int(input(f"  メッセージ（0〜{rsa_keys['n']-1}の整数）: "))
                cipher = rsa_encrypt(msg, rsa_keys["e"], rsa_keys["n"])
                if cipher is not None:
                    plain = rsa_decrypt(cipher, rsa_keys["d"], rsa_keys["n"])
                    if plain == msg:
                        print(f"  → 復号成功！ {msg} → {cipher} → {plain}")
            except ValueError:
                print("  ※ 正しい整数を入力してください。")

        elif choice == "5":
            if rsa_keys is None:
                print("  ※ 先にRSA鍵を生成してください（選択肢3）。")
                continue
            try:
                msg = int(input(f"  メッセージ（0〜{rsa_keys['n']-1}の整数）: "))
                sig = rsa_sign(msg, rsa_keys["d"], rsa_keys["n"])
                rsa_verify(msg, sig, rsa_keys["e"], rsa_keys["n"])
            except ValueError:
                print("  ※ 正しい整数を入力してください。")

        elif choice == "6":
            text = input("  テキスト: ").strip()
            if text:
                md5_hash = hashlib.md5(text.encode()).hexdigest()
                sha1_hash = hashlib.sha1(text.encode()).hexdigest()
                sha256_hash = hashlib.sha256(text.encode()).hexdigest()
                print(f"  MD5:    {md5_hash}")
                print(f"  SHA-1:  {sha1_hash}")
                print(f"  SHA-256: {sha256_hash}")

        else:
            print("  ※ 0-6の番号を入力してください。")


# === デモンストレーション ===
print("=" * 55)
print("  暗号アルゴリズム体験")
print("  ～ 暗号の仕組みを実際に動かして理解しよう ～")
print("=" * 55)

# --- デモ1: シーザー暗号 ---
print("\n━━━ デモ1: シーザー暗号（共通鍵暗号の原型） ━━━")
print("  アルファベットを一定文字数ずらして暗号化します")
print("  ジュリアス・シーザーが使ったとされる暗号です")

plaintext = "HELLO WORLD"
shift = 3
encrypted = caesar_encrypt(plaintext, shift)
decrypted = caesar_decrypt(encrypted, shift)

print(f"\n  平文:    {plaintext}")
print(f"  鍵:      シフト数 = {shift}")
print(f"  暗号文:  {encrypted}")
print(f"  復号:    {decrypted}")

print(f"\n  ■ 全シフトパターン（暗号解読のイメージ）")
for s in range(1, 6):
    print(f"    シフト{s}: {caesar_encrypt(plaintext, s)}")

# --- デモ2: XOR暗号 ---
print("\n\n━━━ デモ2: XOR暗号 ━━━")
print("  XOR演算の特性: A XOR K XOR K = A（2回同じ鍵でXORすると元に戻ります）")

text = "SECRET"
key = "KEY"
encrypted_vals = xor_encrypt(text, key)
encrypted_hex = " ".join(f"0x{v:02X}" for v in encrypted_vals)
decrypted = xor_decrypt(encrypted_vals, key)

print(f"\n  平文:    {text}")
print(f"  鍵:      {key}")
print(f"  暗号文:  [{encrypted_hex}]")
print(f"  復号:    {decrypted}")

print(f"\n  ■ XOR演算の計算過程")
for i, char in enumerate(text):
    key_char = key[i % len(key)]
    xored = ord(char) ^ ord(key_char)
    print(f"    '{char}' (0x{ord(char):02X}) XOR '{key_char}' (0x{ord(key_char):02X}) "
          f"= 0x{xored:02X} ({xored:08b})")

# --- デモ3: RSA暗号（小さな素数で体験） ---
print("\n\n━━━ デモ3: RSA暗号 ━━━")
print("  公開鍵暗号方式の代表格です")
print("  小さな素数を使って、暗号化・復号の仕組みを体験します")

# 鍵生成
keys = generate_rsa_keys(61, 53)

if keys:
    # 暗号化と復号
    print(f"\n\n  ■ 暗号化と復号の実行")
    test_messages = [42, 100, 7]
    for msg in test_messages:
        if msg < keys["n"]:
            cipher = rsa_encrypt(msg, keys["e"], keys["n"])
            plain = rsa_decrypt(cipher, keys["d"], keys["n"])
            status = "成功 ✓" if plain == msg else "失敗 ✗"
            print(f"    {msg} → 暗号化 → {cipher} → 復号 → {plain} ({status})")

    # デジタル署名
    print(f"\n\n  ━━━ デジタル署名の仕組み ━━━")
    print("  RSAを「逆方向」に使います:")
    print("    暗号化: 公開鍵で暗号化 → 秘密鍵で復号")
    print("    署名:   秘密鍵で署名   → 公開鍵で検証")

    msg = 42
    sig = rsa_sign(msg, keys["d"], keys["n"])
    rsa_verify(msg, sig, keys["e"], keys["n"])

    # 改ざんされた場合
    print(f"\n  ■ メッセージが改ざんされた場合")
    rsa_verify(43, sig, keys["e"], keys["n"])  # 異なるメッセージで検証

# --- デモ4: ハッシュ関数 ---
demonstrate_hash()

# --- 暗号方式の比較 ---
print("""

━━━ 暗号方式の比較（試験頻出！） ━━━

  ■ 共通鍵暗号（対称鍵暗号）
    特徴: 暗号化と復号に同じ鍵を使います
    例:   AES, DES, 3DES
    長所: 処理が高速です
    短所: 鍵の配送問題（安全に鍵を渡す方法が必要）
    鍵数: n人で通信 → n(n-1)/2 個の鍵が必要です

  ■ 公開鍵暗号（非対称鍵暗号）
    特徴: 暗号化と復号に異なる鍵を使います
    例:   RSA, 楕円曲線暗号(ECC)
    長所: 鍵の配送が容易です（公開鍵は公開できます）
    短所: 処理が低速です（共通鍵暗号の100〜1000倍遅い）
    鍵数: n人で通信 → 2n 個の鍵が必要です

  ■ ハイブリッド暗号
    特徴: 公開鍵暗号で共通鍵を交換し、以降は共通鍵暗号で通信します
    例:   SSL/TLS, S/MIME
    両方の長所を活用する実用的な方式です

  ■ ハッシュ関数
    特徴: 一方向性（元のデータを復元できない）
    例:   SHA-256, SHA-3, MD5（非推奨）
    用途: パスワード保存、改ざん検知、デジタル署名

  ■ デジタル署名の仕組み
    1. 送信者がメッセージのハッシュ値を計算します
    2. ハッシュ値を送信者の秘密鍵で暗号化します → 署名
    3. メッセージと署名を送付します
    4. 受信者が署名を送信者の公開鍵で復号します
    5. 受信者がメッセージのハッシュ値を計算し、比較します
    → 一致すれば「なりすまし」も「改ざん」もないことが確認できます
""")

# --- 対話モード ---
interactive_mode()
