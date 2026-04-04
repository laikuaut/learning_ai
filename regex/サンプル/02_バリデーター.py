"""
正規表現サンプル02：入力バリデーター
====================================

学べる内容:
  - re.fullmatch() による入力値の検証
  - 実用的な正規表現パターン（メール、電話番号、郵便番号など）
  - バリデーション関数の設計パターン

実行方法:
  python 02_バリデーター.py
"""

import re


# --- バリデーション関数群 ---

def validate_email(email):
    """メールアドレスのバリデーション"""
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.fullmatch(pattern, email) is not None


def validate_phone(phone):
    """日本の電話番号のバリデーション（ハイフンあり・なし両対応）"""
    pattern = re.compile(r"""
        ^(
            0[789]0-?\d{4}-?\d{4}      # 携帯電話: 070/080/090
            |                           # または
            0\d{1,3}-?\d{2,4}-?\d{3,4} # 固定電話
        )$
    """, re.VERBOSE)
    return pattern.fullmatch(phone) is not None


def validate_postal_code(code):
    """郵便番号のバリデーション（ハイフンあり・なし両対応）"""
    pattern = r"^\d{3}-?\d{4}$"
    return re.fullmatch(pattern, code) is not None


def validate_date(date_str):
    """日付形式のバリデーション（YYYY-MM-DD or YYYY/MM/DD）"""
    pattern = r"^\d{4}[-/](0[1-9]|1[0-2])[-/](0[1-9]|[12]\d|3[01])$"
    return re.fullmatch(pattern, date_str) is not None


def validate_password(password):
    """パスワード強度のバリデーション"""
    errors = []
    if len(password) < 8:
        errors.append("8文字以上にしてください")
    if not re.search(r"[A-Z]", password):
        errors.append("大文字を1文字以上含めてください")
    if not re.search(r"[a-z]", password):
        errors.append("小文字を1文字以上含めてください")
    if not re.search(r"\d", password):
        errors.append("数字を1文字以上含めてください")
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>/?]", password):
        errors.append("記号を1文字以上含めてください")
    return errors


def validate_url(url):
    """URLのバリデーション（簡易版）"""
    pattern = r"^https?://[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?(\.[a-zA-Z0-9]([a-zA-Z0-9\-]*[a-zA-Z0-9])?)*(/[^\s]*)?$"
    return re.fullmatch(pattern, url) is not None


# --- メイン処理 ---

def main():
    print("=" * 50)
    print("正規表現 入力バリデーター")
    print("=" * 50)

    validators = {
        "1": ("メールアドレス", validate_email, [
            ("user@example.com", True),
            ("test.user+tag@mail.co.jp", True),
            ("@example.com", False),
            ("user@", False),
            ("plaintext", False),
        ]),
        "2": ("電話番号", validate_phone, [
            ("090-1234-5678", True),
            ("09012345678", True),
            ("03-1234-5678", True),
            ("0312345678", True),
            ("123-4567", False),
            ("abc", False),
        ]),
        "3": ("郵便番号", validate_postal_code, [
            ("123-4567", True),
            ("1234567", True),
            ("12-3456", False),
            ("abc-defg", False),
        ]),
        "4": ("日付", validate_date, [
            ("2026-04-05", True),
            ("2026/04/05", True),
            ("2026-13-01", False),
            ("2026-04-32", False),
            ("26-04-05", False),
        ]),
        "5": ("URL", validate_url, [
            ("https://example.com", True),
            ("http://www.example.co.jp/path", True),
            ("ftp://example.com", False),
            ("not-a-url", False),
        ]),
    }

    while True:
        print("\n検証したい項目を選んでください:")
        for key, (name, _, _) in validators.items():
            print(f"  {key}. {name}")
        print(f"  6. パスワード強度チェック")
        print(f"  7. デモ（全テストケース実行）")
        print(f"  q. 終了")

        choice = input("\n選択> ").strip()

        if choice == "q":
            break
        elif choice == "7":
            # デモモード
            print("\n--- 全テストケース実行 ---")
            for key, (name, func, cases) in validators.items():
                print(f"\n[{name}]")
                for value, expected in cases:
                    result = func(value)
                    mark = "✓" if result == expected else "✗"
                    print(f"  {mark} '{value}' → {'有効' if result else '無効'}")
        elif choice == "6":
            # パスワード強度チェック
            password = input("パスワードを入力> ")
            errors = validate_password(password)
            if errors:
                print("❌ パスワードが弱いです:")
                for err in errors:
                    print(f"   - {err}")
            else:
                print("✅ パスワードは十分強力です！")
        elif choice in validators:
            name, func, _ = validators[choice]
            value = input(f"{name}を入力> ")
            if func(value):
                print(f"✅ '{value}' は有効な{name}です")
            else:
                print(f"❌ '{value}' は無効な{name}です")
        else:
            print("無効な選択です。")

    print("\nお疲れさまでした！")


if __name__ == "__main__":
    main()
