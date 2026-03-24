# ==============================
# パスワード強度チェッカー
# 情報セキュリティ基礎：パスワードセキュリティを体験するサンプル
# ==============================
# 学べる内容:
#   - パスワードの強度を決める要素
#   - 文字種（大文字、小文字、数字、記号）の重要性
#   - パスワードの長さとエントロピーの関係
#   - よくある危険なパスワードパターン
#   - 辞書攻撃とブルートフォース攻撃の耐性
#   - パスワードポリシーの考え方
#
# 実行方法:
#   python 03_パスワード強度チェッカー.py
#
# ※ 本プログラムは教育目的で作成されています
# ※ 入力したパスワードはどこにも保存・送信されません
# ==============================

import math
import string
import re


def explain_password_security():
    """パスワードセキュリティの基本を解説します"""
    print("""
  ┌──────────────────────────────────────────────────┐
  │          パスワードセキュリティの基本              │
  └──────────────────────────────────────────────────┘

  【パスワードの強度を決める要素】

    1. 長さ ─── 長いほど強い（最低12文字以上推奨）
    2. 文字種 ─ 使う文字の種類が多いほど強い
    3. 予測困難性 ─ 辞書に載っていない組み合わせ

  【文字種と組み合わせ数】
  ┌────────────────┬────────┬────────────────────────┐
  │ 文字種          │ 文字数 │ 8文字のパスワード      │
  ├────────────────┼────────┼────────────────────────┤
  │ 数字のみ        │   10   │ 10^8 = 1億通り         │
  │ 小文字のみ      │   26   │ 26^8 = 約2千億通り     │
  │ 大文字+小文字   │   52   │ 52^8 = 約53兆通り      │
  │ +数字           │   62   │ 62^8 = 約218兆通り     │
  │ +記号           │   94   │ 94^8 = 約6千兆通り     │
  └────────────────┴────────┴────────────────────────┘

  【攻撃手法】
  ┌────────────────┬──────────────────────────────────┐
  │ ブルートフォース │ 全ての組み合わせを試す            │
  │ 辞書攻撃       │ よくあるパスワードのリストを試す    │
  │ レインボーテーブル│ 事前計算したハッシュ値で照合      │
  │ ソーシャル      │ 個人情報から推測                   │
  └────────────────┴──────────────────────────────────┘
    """)


# よくある危険なパスワードリスト（辞書攻撃で真っ先に試される）
COMMON_PASSWORDS = [
    "password", "123456", "12345678", "qwerty", "abc123",
    "monkey", "1234567", "letmein", "trustno1", "dragon",
    "baseball", "iloveyou", "master", "sunshine", "ashley",
    "bailey", "shadow", "123123", "654321", "superman",
    "qazwsx", "michael", "football", "password1", "password123",
    "admin", "welcome", "login", "starwars", "hello",
    "charlie", "donald", "princess", "qwerty123", "!@#$%^&*",
    "aa123456", "abc1234", "p@ssw0rd", "p@ssword", "passw0rd",
]

# よくある危険なパターン
KEYBOARD_PATTERNS = [
    "qwerty", "qwertyuiop", "asdfgh", "asdfghjkl", "zxcvbn",
    "1qaz2wsx", "qazwsxedc",
]


def calculate_entropy(password):
    """パスワードのエントロピー（情報量）を計算します

    エントロピー = log2(文字種の数 ^ パスワード長)
    エントロピーが高いほど推測が困難です。
    """
    charset_size = 0

    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", password))

    if has_lower:
        charset_size += 26
    if has_upper:
        charset_size += 26
    if has_digit:
        charset_size += 10
    if has_symbol:
        charset_size += 32  # 一般的な記号の数

    if charset_size == 0:
        return 0

    entropy = len(password) * math.log2(charset_size)
    return entropy


def estimate_crack_time(entropy):
    """エントロピーからブルートフォース攻撃の所要時間を推定します"""
    # 1秒間に試行可能な回数（一般的なPCを想定）
    attempts_per_second = {
        "一般的なPC": 1_000_000_000,           # 10億回/秒
        "高性能GPU": 100_000_000_000,          # 1000億回/秒
        "スーパーコンピュータ": 1_000_000_000_000_000,  # 1000兆回/秒
    }

    total_combinations = 2 ** entropy
    # 平均して半分の試行で見つかる
    average_attempts = total_combinations / 2

    results = {}
    for name, speed in attempts_per_second.items():
        seconds = average_attempts / speed
        results[name] = format_time(seconds)

    return results


def format_time(seconds):
    """秒数を人間が読みやすい形式に変換します"""
    if seconds < 0.001:
        return "一瞬"
    elif seconds < 1:
        return f"{seconds * 1000:.1f} ミリ秒"
    elif seconds < 60:
        return f"{seconds:.1f} 秒"
    elif seconds < 3600:
        return f"{seconds / 60:.1f} 分"
    elif seconds < 86400:
        return f"{seconds / 3600:.1f} 時間"
    elif seconds < 86400 * 365:
        return f"{seconds / 86400:.1f} 日"
    elif seconds < 86400 * 365 * 1000:
        return f"{seconds / (86400 * 365):.1f} 年"
    elif seconds < 86400 * 365 * 1_000_000:
        return f"{seconds / (86400 * 365 * 1000):.1f} 千年"
    elif seconds < 86400 * 365 * 1_000_000_000:
        return f"{seconds / (86400 * 365 * 1_000_000):.1f} 百万年"
    else:
        return f"{seconds / (86400 * 365 * 1_000_000_000):.1f} 十億年以上"


def check_password_strength(password):
    """パスワードの強度を総合的に評価します"""
    score = 0
    max_score = 100
    feedback = []
    warnings = []

    # --- 長さの評価（最大30点）---
    length = len(password)
    if length >= 16:
        score += 30
        feedback.append(("長さ", f"{length}文字 - 非常に良い", 30))
    elif length >= 12:
        score += 25
        feedback.append(("長さ", f"{length}文字 - 良い", 25))
    elif length >= 8:
        score += 15
        feedback.append(("長さ", f"{length}文字 - 最低限", 15))
    elif length >= 6:
        score += 5
        feedback.append(("長さ", f"{length}文字 - 短すぎる", 5))
        warnings.append("8文字以上にしてください（12文字以上を推奨）")
    else:
        feedback.append(("長さ", f"{length}文字 - 非常に短い", 0))
        warnings.append("最低でも8文字以上にしてください")

    # --- 文字種の評価（最大40点）---
    has_lower = bool(re.search(r"[a-z]", password))
    has_upper = bool(re.search(r"[A-Z]", password))
    has_digit = bool(re.search(r"[0-9]", password))
    has_symbol = bool(re.search(r"[^a-zA-Z0-9]", password))

    char_types = sum([has_lower, has_upper, has_digit, has_symbol])
    char_score = char_types * 10
    score += char_score

    types_detail = []
    if has_lower:
        types_detail.append("小文字")
    if has_upper:
        types_detail.append("大文字")
    if has_digit:
        types_detail.append("数字")
    if has_symbol:
        types_detail.append("記号")
    feedback.append(("文字種", f"{char_types}種類（{', '.join(types_detail)}）", char_score))

    if not has_upper:
        warnings.append("大文字を含めてください")
    if not has_digit:
        warnings.append("数字を含めてください")
    if not has_symbol:
        warnings.append("記号（!@#$%など）を含めてください")

    # --- パターンチェック（減点方式、最大-30点）---
    pattern_penalty = 0

    # 連続する文字のチェック
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            pattern_penalty += 10
            warnings.append(f"同じ文字の連続（'{password[i]}{password[i+1]}{password[i+2]}'）は避けてください")
            break

    # 連番のチェック
    for i in range(len(password) - 2):
        if (password[i:i + 3].isdigit() and
                int(password[i + 1]) == int(password[i]) + 1 and
                int(password[i + 2]) == int(password[i]) + 2):
            pattern_penalty += 10
            warnings.append("連続する数字（123, 456等）は避けてください")
            break

    # キーボード配列パターン
    lower_pw = password.lower()
    for pattern in KEYBOARD_PATTERNS:
        if pattern in lower_pw:
            pattern_penalty += 10
            warnings.append(f"キーボード配列パターン（'{pattern}'）は避けてください")
            break

    score -= pattern_penalty
    if pattern_penalty > 0:
        feedback.append(("パターン", f"危険なパターンを検出 (-{pattern_penalty}点)", -pattern_penalty))

    # --- 辞書攻撃耐性（最大30点）---
    is_common = password.lower() in COMMON_PASSWORDS
    if is_common:
        score -= 30
        feedback.append(("辞書攻撃耐性", "よく使われるパスワードです！", -30))
        warnings.append("このパスワードは辞書攻撃リストに載っています。絶対に使わないでください")
    else:
        # 部分一致チェック
        partial_match = False
        for common in COMMON_PASSWORDS:
            if common in password.lower() and len(common) >= 4:
                partial_match = True
                break

        if partial_match:
            score += 15
            feedback.append(("辞書攻撃耐性", "一般的な単語を含んでいます", 15))
            warnings.append("よく使われる単語を基にしたパスワードは推測されやすいです")
        else:
            score += 30
            feedback.append(("辞書攻撃耐性", "辞書にない組み合わせ", 30))

    # スコアを0〜100に正規化
    score = max(0, min(max_score, score))

    return score, feedback, warnings


def display_strength_result(password):
    """パスワード強度チェックの結果を表示します"""
    # マスク表示
    masked = password[0] + "*" * (len(password) - 2) + password[-1] if len(password) > 2 else "*" * len(password)

    print(f"\n  パスワード: {masked} （{len(password)}文字）")

    # 強度チェック
    score, feedback, warnings = check_password_strength(password)

    # エントロピー計算
    entropy = calculate_entropy(password)

    # 強度レベルの判定
    if score >= 80:
        level = "非常に強い"
        bar_char = "█"
        color_label = "緑"
    elif score >= 60:
        level = "強い"
        bar_char = "█"
        color_label = "黄緑"
    elif score >= 40:
        level = "普通"
        bar_char = "▓"
        color_label = "黄"
    elif score >= 20:
        level = "弱い"
        bar_char = "▒"
        color_label = "橙"
    else:
        level = "非常に弱い"
        bar_char = "░"
        color_label = "赤"

    # スコアバー
    bar_length = score // 5
    bar = bar_char * bar_length + "░" * (20 - bar_length)

    print(f"\n  ┌──────────────────────────────────────────────┐")
    print(f"  │  強度スコア: {score}/100 ({level})")
    print(f"  │  [{bar}] {score}%")
    print(f"  │  エントロピー: {entropy:.1f} ビット")
    print(f"  └──────────────────────────────────────────────┘")

    # 評価詳細
    print(f"\n  【評価詳細】")
    print(f"  {'項目':<16} {'評価':<30} {'スコア'}")
    print(f"  {'─' * 16} {'─' * 30} {'─' * 8}")
    for item, detail, pts in feedback:
        sign = "+" if pts >= 0 else ""
        print(f"  {item:<16} {detail:<30} {sign}{pts}点")

    # ブルートフォース耐性
    crack_times = estimate_crack_time(entropy)
    print(f"\n  【ブルートフォース攻撃の推定所要時間】")
    for device, time_str in crack_times.items():
        print(f"  {device + ':':>24} {time_str}")

    # 警告
    if warnings:
        print(f"\n  【改善ポイント】")
        for i, warning in enumerate(warnings, 1):
            print(f"  {i}. {warning}")
    else:
        print(f"\n  ※ 改善ポイントはありません。強力なパスワードです！")


def compare_passwords():
    """複数のパスワード例を比較して強度の違いを見せます"""
    print("\n" + "=" * 55)
    print("  パスワード強度の比較")
    print("=" * 55)

    examples = [
        ("123456", "最も使われる危険なパスワード"),
        ("password", "英単語そのもの"),
        ("P@ssw0rd", "よくある置換パターン"),
        ("MyDog2023!", "個人情報ベース"),
        ("Tr0ub4dor&3", "ランダム風だが短め"),
        ("correct-horse-battery-staple", "パスフレーズ方式（推奨）"),
        ("kX$9mP2vL!qR#nW7", "完全ランダム（推奨）"),
    ]

    print(f"\n  {'パスワード':<35} {'スコア':>6} {'エントロピー':>12} {'レベル'}")
    print(f"  {'─' * 35} {'─' * 6} {'─' * 12} {'─' * 12}")

    for pw, desc in examples:
        score, _, _ = check_password_strength(pw)
        entropy = calculate_entropy(pw)

        if score >= 80:
            level = "非常に強い"
        elif score >= 60:
            level = "強い"
        elif score >= 40:
            level = "普通"
        elif score >= 20:
            level = "弱い"
        else:
            level = "非常に弱い"

        # パスワードをマスク表示
        if len(pw) > 20:
            display_pw = pw[:8] + "..." + pw[-4:]
        else:
            display_pw = pw

        print(f"  {display_pw:<35} {score:>4}点 {entropy:>9.1f}bit  {level}")

    print(f"\n  ※ パスフレーズ方式: 複数の単語を組み合わせる方法です。")
    print(f"     覚えやすく、エントロピーも高くなります。")


def demo_mode():
    """デモモード: 様々なパスワードの強度を評価します"""
    print("\n" + "=" * 55)
    print("  【デモモード】パスワード強度チェック")
    print("=" * 55)

    # パスワード比較
    compare_passwords()

    # 詳細評価の例
    print("\n\n  ◆ 詳細評価の例")
    sample_passwords = ["abc123", "P@ssw0rd!", "My$ecureP@ss2026"]
    for pw in sample_passwords:
        display_strength_result(pw)
        print()


def interactive_mode():
    """対話モード: ユーザーが入力したパスワードの強度を評価します"""
    print("\n" + "=" * 55)
    print("  【対話モード】パスワード強度チェッカー")
    print("=" * 55)
    print("  ※ 入力したパスワードはどこにも保存・送信されません。")

    while True:
        print("\n  操作を選んでください:")
        print("  1. パスワードの強度をチェック")
        print("  2. 代表的なパスワードの比較表を表示")
        print("  3. パスワード作成のアドバイスを表示")
        print("  4. メニューに戻る")

        choice = input("\n  選択 (1-4): ").strip()

        if choice == "1":
            password = input("  チェックするパスワードを入力: ")
            if password:
                display_strength_result(password)
            else:
                print("  ※ パスワードを入力してください。")

        elif choice == "2":
            compare_passwords()

        elif choice == "3":
            print("""
  ┌──────────────────────────────────────────────────────┐
  │          強いパスワードの作り方                        │
  └──────────────────────────────────────────────────────┘

  【推奨ルール】
  1. 12文字以上（できれば16文字以上）
  2. 大文字・小文字・数字・記号をすべて含む
  3. 辞書に載っている単語をそのまま使わない
  4. 個人情報（名前、誕生日等）を含めない
  5. サービスごとに異なるパスワードを使う

  【おすすめの方法】
  ◆ パスフレーズ方式
    複数のランダムな単語を組み合わせます。
    例: "correct-horse-battery-staple"
    覚えやすく、十分な長さがあります。

  ◆ パスワードマネージャーの利用
    ランダムな強力パスワードを自動生成し、
    安全に管理してくれるソフトウェアです。
    1Password, Bitwarden, KeePass 等が有名です。

  【やってはいけないこと】
  - 同じパスワードの使い回し
  - メモ帳やファイルに平文で保存
  - 他人と共有
  - 短い・単純なパスワード
            """)

        elif choice == "4":
            break
        else:
            print("  ※ 1〜4 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        パスワード強度チェッカー                    |")
    print("|        〜 安全なパスワードを考えよう 〜            |")
    print("+" + "=" * 53 + "+")

    # パスワードセキュリティの解説
    explain_password_security()

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（代表的なパスワードを評価）")
        print("  2. 対話モード（自分のパスワードをチェック）")
        print("  3. 終了")

        mode = input("\n  選択 (1-3): ").strip()

        if mode == "1":
            demo_mode()
        elif mode == "2":
            interactive_mode()
        elif mode == "3":
            print("\n  ご利用ありがとうございました！")
            break
        else:
            print("  ※ 1〜3 の数字を入力してください。")
