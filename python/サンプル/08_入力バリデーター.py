# ==============================
# 入力バリデーター
# 第8章：エラー処理の総合サンプル
# ==============================
# 学べる内容:
#   - try / except / else / finally
#   - 複数の例外を個別にキャッチ
#   - raise で例外を発生させる
#   - カスタム例外クラスの定義
#   - 入力検証ループ（エラー時は再入力）
#   - EAFP（許可より許しを請う）パターン
#   - エラー情報のログ記録
# ==============================

import re
from datetime import datetime


# === カスタム例外クラス ===

class ValidationError(Exception):
    """入力検証エラーの基底クラス"""
    def __init__(self, field_name, value, message):
        self.field_name = field_name
        self.value = value
        self.message = message
        super().__init__(f"{field_name}: {message}")


class RequiredFieldError(ValidationError):
    """必須フィールドが空のエラー"""
    def __init__(self, field_name):
        super().__init__(field_name, "", "この項目は必須です")


class FormatError(ValidationError):
    """フォーマットが不正なエラー"""
    def __init__(self, field_name, value, expected_format):
        super().__init__(
            field_name, value,
            f"形式が不正です（期待: {expected_format}、入力: {value}）"
        )


class RangeError(ValidationError):
    """値が範囲外のエラー"""
    def __init__(self, field_name, value, min_val=None, max_val=None):
        if min_val is not None and max_val is not None:
            msg = f"{min_val}〜{max_val}の範囲で入力してください（入力: {value}）"
        elif min_val is not None:
            msg = f"{min_val}以上で入力してください（入力: {value}）"
        else:
            msg = f"{max_val}以下で入力してください（入力: {value}）"
        super().__init__(field_name, value, msg)


# === バリデーション関数群 ===

def validate_required(value, field_name="フィールド"):
    """必須チェック"""
    if not value or not value.strip():
        raise RequiredFieldError(field_name)
    return value.strip()


def validate_integer(value, field_name="数値", min_val=None, max_val=None):
    """整数バリデーション"""
    try:
        num = int(value)
    except ValueError:
        raise FormatError(field_name, value, "整数")

    if min_val is not None and num < min_val:
        raise RangeError(field_name, num, min_val=min_val, max_val=max_val)
    if max_val is not None and num > max_val:
        raise RangeError(field_name, num, min_val=min_val, max_val=max_val)
    return num


def validate_email(value, field_name="メールアドレス"):
    """メールアドレスバリデーション"""
    value = validate_required(value, field_name)
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9.]+$"
    if not re.match(pattern, value):
        raise FormatError(field_name, value, "user@example.com")
    return value


def validate_phone(value, field_name="電話番号"):
    """電話番号バリデーション（日本形式）"""
    value = validate_required(value, field_name)
    # ハイフンなしの場合はハイフンを入れる
    cleaned = value.replace("-", "").replace(" ", "")
    if not cleaned.isdigit():
        raise FormatError(field_name, value, "090-1234-5678")
    if len(cleaned) < 10 or len(cleaned) > 11:
        raise FormatError(field_name, value, "10〜11桁の数字")
    return value


def validate_date(value, field_name="日付", date_format="%Y-%m-%d"):
    """日付バリデーション"""
    value = validate_required(value, field_name)
    try:
        parsed = datetime.strptime(value, date_format)
        return parsed.strftime(date_format)
    except ValueError:
        raise FormatError(field_name, value, "YYYY-MM-DD")


def validate_password(value, field_name="パスワード"):
    """パスワード強度チェック"""
    value = validate_required(value, field_name)

    errors = []
    if len(value) < 8:
        errors.append("8文字以上")
    if not any(c.isupper() for c in value):
        errors.append("英大文字を1文字以上")
    if not any(c.islower() for c in value):
        errors.append("英小文字を1文字以上")
    if not any(c.isdigit() for c in value):
        errors.append("数字を1文字以上")

    if errors:
        raise ValidationError(
            field_name, "***",
            "以下の条件を満たしてください: " + "、".join(errors)
        )
    return value


def validate_choice(value, choices, field_name="選択"):
    """選択肢バリデーション"""
    value = validate_required(value, field_name)
    if value not in choices:
        raise ValidationError(
            field_name, value,
            f"次の中から選択してください: {', '.join(choices)}"
        )
    return value


# === 入力ヘルパー関数 ===

def get_validated_input(prompt, validator, *args, max_attempts=3, **kwargs):
    """バリデーション付きの入力関数（リトライ機能付き）

    よくある間違い:
    - try の範囲が広すぎる → 関係ないエラーまでキャッチしてしまう
    - except Exception で全てキャッチ → デバッグが困難になる
    """
    for attempt in range(1, max_attempts + 1):
        try:
            value = input(prompt)
            result = validator(value, *args, **kwargs)
            return result
        except ValidationError as e:
            remaining = max_attempts - attempt
            if remaining > 0:
                print(f"  [エラー] {e.message}（残り{remaining}回）")
            else:
                print(f"  [エラー] {e.message}")
                print(f"  入力回数の上限に達しました。")
                raise  # 最後の試行で失敗したら例外を再送出


# === エラーログ機能 ===

class ErrorLog:
    """エラー情報を記録するクラス"""

    def __init__(self):
        self.errors = []

    def add(self, error):
        """エラーを記録する"""
        self.errors.append({
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "type": type(error).__name__,
            "message": str(error),
        })

    def show(self):
        """記録されたエラーを表示する"""
        if not self.errors:
            print("  エラーはありません。")
            return
        print(f"\n  記録されたエラー: {len(self.errors)}件")
        for i, err in enumerate(self.errors, start=1):
            print(f"  {i}. [{err['timestamp']}] {err['type']}: {err['message']}")

    def clear(self):
        """エラー記録をクリアする"""
        self.errors.clear()


# === デモ: ユーザー登録フォーム ===

def user_registration_demo():
    """ユーザー登録のデモ（バリデーション実演）"""
    print("\n" + "=" * 50)
    print("  ユーザー登録フォーム")
    print("=" * 50)

    error_log = ErrorLog()
    user_data = {}

    # 名前（必須チェック）
    print("\n--- 名前 ---")
    try:
        user_data["name"] = get_validated_input(
            "名前: ", validate_required, "名前"
        )
    except ValidationError as e:
        error_log.add(e)
        user_data["name"] = None

    # 年齢（整数 + 範囲チェック）
    print("\n--- 年齢 ---")
    try:
        user_data["age"] = get_validated_input(
            "年齢: ", validate_integer, "年齢", min_val=0, max_val=150
        )
    except ValidationError as e:
        error_log.add(e)
        user_data["age"] = None

    # メールアドレス（形式チェック）
    print("\n--- メールアドレス ---")
    try:
        user_data["email"] = get_validated_input(
            "メール: ", validate_email, "メール"
        )
    except ValidationError as e:
        error_log.add(e)
        user_data["email"] = None

    # 電話番号（形式チェック）
    print("\n--- 電話番号 ---")
    try:
        user_data["phone"] = get_validated_input(
            "電話: ", validate_phone, "電話"
        )
    except ValidationError as e:
        error_log.add(e)
        user_data["phone"] = None

    # 生年月日（日付形式チェック）
    print("\n--- 生年月日 ---")
    try:
        user_data["birthday"] = get_validated_input(
            "生年月日 (YYYY-MM-DD): ", validate_date, "生年月日"
        )
    except ValidationError as e:
        error_log.add(e)
        user_data["birthday"] = None

    # パスワード（強度チェック）
    print("\n--- パスワード ---")
    try:
        user_data["password"] = get_validated_input(
            "パスワード: ", validate_password, "パスワード"
        )
    except ValidationError as e:
        error_log.add(e)
        user_data["password"] = None

    # 結果表示
    print("\n" + "=" * 50)
    print("  登録結果")
    print("=" * 50)

    valid_count = sum(1 for v in user_data.values() if v is not None)
    total_count = len(user_data)

    for key, value in user_data.items():
        if value is not None:
            # パスワードは伏せ字で表示
            display = "***" if key == "password" else value
            print(f"  [OK] {key}: {display}")
        else:
            print(f"  [NG] {key}: 未入力または不正")

    print(f"\n  有効項目: {valid_count}/{total_count}")

    # エラーログ表示
    error_log.show()


# === バリデーション単体テスト（デモ）===

def validation_test_demo():
    """各バリデーション関数のテスト"""
    print("\n" + "=" * 50)
    print("  バリデーション動作テスト")
    print("=" * 50)

    test_cases = [
        ("必須チェック - 空文字", lambda: validate_required("", "名前")),
        ("必須チェック - 正常", lambda: validate_required("太郎", "名前")),
        ("整数チェック - 文字列", lambda: validate_integer("abc", "年齢")),
        ("整数チェック - 範囲外", lambda: validate_integer("200", "年齢", max_val=150)),
        ("整数チェック - 正常", lambda: validate_integer("25", "年齢", min_val=0, max_val=150)),
        ("メール - 不正形式", lambda: validate_email("invalid")),
        ("メール - 正常", lambda: validate_email("user@example.com")),
        ("パスワード - 弱い", lambda: validate_password("abc")),
        ("パスワード - 正常", lambda: validate_password("Abc12345")),
        ("日付 - 不正形式", lambda: validate_date("2025/13/45")),
        ("日付 - 正常", lambda: validate_date("2025-04-15")),
    ]

    for name, test_func in test_cases:
        try:
            result = test_func()
            print(f"  [PASS] {name} → {result}")
        except ValidationError as e:
            print(f"  [FAIL] {name} → {e.message}")


# === メインプログラム ===

print("+" + "-" * 28 + "+")
print("|    入力バリデーター      |")
print("+" + "-" * 28 + "+")

while True:
    print("\n--- メニュー ---")
    print("1. ユーザー登録デモ")
    print("2. バリデーションテスト")
    print("3. 終了")

    choice = input("選択 (1-3): ").strip()

    if choice == "1":
        user_registration_demo()
    elif choice == "2":
        validation_test_demo()
    elif choice == "3":
        print("終了します。")
        break
    else:
        print("1〜3の数字を入力してください。")
