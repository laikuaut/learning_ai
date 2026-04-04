"""
正規表現サンプル03：テキスト変換ツール
======================================

学べる内容:
  - re.sub() による高度な置換
  - コールバック関数を使った動的置換
  - CamelCase/snake_case変換
  - 個人情報のマスキング

実行方法:
  python 03_テキスト変換ツール.py
"""

import re


def mask_email(text):
    """メールアドレスをマスキング（先頭2文字+ドメインを残す）"""
    def replacer(match):
        email = match.group()
        local, domain = email.split("@")
        if len(local) <= 2:
            masked_local = "*" * len(local)
        else:
            masked_local = local[:2] + "*" * (len(local) - 2)
        return f"{masked_local}@{domain}"
    return re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", replacer, text)


def mask_phone(text):
    """電話番号をマスキング（末尾4桁を残す）"""
    def replacer(match):
        phone = match.group()
        return re.sub(r"\d(?=[\d-]{4,}$)", "*", phone)
    return re.sub(r"0\d{1,3}-\d{2,4}-\d{3,4}", replacer, text)


def camel_to_snake(name):
    """CamelCase を snake_case に変換"""
    s = re.sub(r"(?<=[a-z0-9])([A-Z])", r"_\1", name)
    s = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", s)
    return s.lower()


def snake_to_camel(name, upper_first=False):
    """snake_case を camelCase に変換"""
    result = re.sub(r"_([a-z])", lambda m: m.group(1).upper(), name)
    if upper_first:
        result = result[0].upper() + result[1:]
    return result


def normalize_whitespace(text):
    """連続する空白を1つのスペースに正規化"""
    return re.sub(r"\s+", " ", text).strip()


def replace_with_dict(text, replacements):
    """辞書を使った一括置換"""
    pattern = re.compile("|".join(re.escape(k) for k in replacements))
    return pattern.sub(lambda m: replacements[m.group()], text)


def add_tax(text, tax_rate=0.10):
    """テキスト内の価格に税率を加算"""
    def calc_tax(match):
        price = int(match.group(1).replace(",", ""))
        tax_included = int(price * (1 + tax_rate))
        formatted = f"{tax_included:,}"
        return f"{formatted}円"
    return re.sub(r"([\d,]+)円", calc_tax, text)


def main():
    print("=" * 50)
    print("正規表現 テキスト変換ツール")
    print("=" * 50)

    while True:
        print("\n変換メニュー:")
        print("  1. 個人情報マスキング")
        print("  2. CamelCase ↔ snake_case 変換")
        print("  3. 空白の正規化")
        print("  4. 価格の税込変換")
        print("  5. デモ（全機能実行）")
        print("  q. 終了")

        choice = input("\n選択> ").strip()

        if choice == "q":
            break

        elif choice == "1":
            print("\n--- 個人情報マスキング ---")
            text = input("テキストを入力（またはEnterでサンプル使用）> ")
            if not text:
                text = "田中太郎 tanaka@example.com 090-1234-5678"
            result = mask_email(text)
            result = mask_phone(result)
            print(f"  元: {text}")
            print(f"  後: {result}")

        elif choice == "2":
            print("\n--- 命名規則変換 ---")
            name = input("変換する名前（またはEnterでサンプル使用）> ")
            if not name:
                samples = ["getUserName", "HTMLParser", "get_user_name", "html_parser"]
                for s in samples:
                    if "_" in s:
                        print(f"  {s} → {snake_to_camel(s)} (camelCase)")
                    else:
                        print(f"  {s} → {camel_to_snake(s)} (snake_case)")
            elif "_" in name:
                print(f"  {name} → {snake_to_camel(name)} (camelCase)")
            else:
                print(f"  {name} → {camel_to_snake(name)} (snake_case)")

        elif choice == "3":
            print("\n--- 空白の正規化 ---")
            text = input("テキストを入力（またはEnterでサンプル使用）> ")
            if not text:
                text = "  Hello   World  \t Python \n  Regex  "
            print(f"  元: '{text}'")
            print(f"  後: '{normalize_whitespace(text)}'")

        elif choice == "4":
            print("\n--- 税込変換 ---")
            text = input("テキストを入力（またはEnterでサンプル使用）> ")
            if not text:
                text = "りんご 100円、バナナ 200円、メロン 3,000円"
            print(f"  元: {text}")
            print(f"  後: {add_tax(text)}")

        elif choice == "5":
            print("\n" + "=" * 50)
            print("全機能デモ")
            print("=" * 50)

            # マスキング
            print("\n[1. 個人情報マスキング]")
            sample = "山田花子 yamada.hanako@mail.co.jp 080-9876-5432"
            print(f"  元: {sample}")
            result = mask_email(sample)
            result = mask_phone(result)
            print(f"  後: {result}")

            # 命名規則変換
            print("\n[2. 命名規則変換]")
            names = ["getUserName", "setMaxRetryCount", "HTMLParser"]
            for n in names:
                print(f"  {n} → {camel_to_snake(n)}")

            # 空白正規化
            print("\n[3. 空白の正規化]")
            messy = "  Hello   World  !  "
            print(f"  '{messy}' → '{normalize_whitespace(messy)}'")

            # 税込変換
            print("\n[4. 税込変換]")
            prices = "コーヒー 350円、ケーキ 500円、ランチ 1,200円"
            print(f"  {prices}")
            print(f"  → {add_tax(prices)}")

            # 辞書置換
            print("\n[5. 辞書を使った一括置換]")
            text = "color is red, sky is blue"
            mapping = {"red": "赤", "blue": "青"}
            print(f"  '{text}' → '{replace_with_dict(text, mapping)}'")

    print("\nお疲れさまでした！")


if __name__ == "__main__":
    main()
