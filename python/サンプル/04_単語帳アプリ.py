# ==============================
# 単語帳アプリ
# 第4章：リストと辞書の総合サンプル
# ==============================
# 学べる内容:
#   - リストの作成・追加・削除・ソート
#   - インデックスとスライス
#   - 辞書の作成・更新・ループ
#   - 辞書のリスト
#   - リスト内包表記
#   - enumerate(), len(), sum()
# ==============================

import random

# --- 単語データ（辞書のリスト）---
words = [
    {"english": "apple", "japanese": "りんご", "correct": 0, "wrong": 0},
    {"english": "book", "japanese": "本", "correct": 0, "wrong": 0},
    {"english": "cat", "japanese": "猫", "correct": 0, "wrong": 0},
    {"english": "dog", "japanese": "犬", "correct": 0, "wrong": 0},
    {"english": "egg", "japanese": "卵", "correct": 0, "wrong": 0},
    {"english": "fish", "japanese": "魚", "correct": 0, "wrong": 0},
    {"english": "grape", "japanese": "ぶどう", "correct": 0, "wrong": 0},
    {"english": "house", "japanese": "家", "correct": 0, "wrong": 0},
]


def show_word_list(words):
    """単語一覧を表示する（辞書のループ）"""
    print("\n=== 単語一覧 ===")
    print(f"{'No':>3} {'英語':<10} {'日本語':<8} {'正解':>4} {'不正解':>4}")
    print("-" * 38)
    for i, word in enumerate(words, start=1):
        print(f"{i:3d} {word['english']:<10} {word['japanese']:<8} "
              f"{word['correct']:4d} {word['wrong']:4d}")
    print(f"\n合計 {len(words)} 単語")


def add_word(words):
    """単語を追加する（リストのappend、辞書の作成）"""
    eng = input("英語: ").strip()
    jpn = input("日本語: ").strip()

    # 重複チェック（リスト内包表記 + in）
    existing = [w["english"] for w in words]
    if eng in existing:
        print(f"「{eng}」は既に登録されています。")
        return

    words.append({"english": eng, "japanese": jpn, "correct": 0, "wrong": 0})
    print(f"「{eng} = {jpn}」を追加しました！")


def quiz(words, count=5):
    """クイズモード（リストのスライス、辞書の更新）"""
    if len(words) == 0:
        print("単語が登録されていません。")
        return

    # 出題数の調整
    count = min(count, len(words))

    # ランダムに出題（リストのコピー + シャッフル）
    quiz_words = words[:]  # スライスでコピー
    random.shuffle(quiz_words)
    quiz_words = quiz_words[:count]  # スライスで切り出し

    score = 0
    print(f"\n=== クイズ（{count}問）===")

    for i, word in enumerate(quiz_words, start=1):
        answer = input(f"Q{i}. 「{word['japanese']}」を英語で: ").strip().lower()

        if answer == word["english"]:
            print("  -> 正解！")
            word["correct"] += 1  # 辞書の値を更新
            score += 1
        else:
            print(f"  -> 不正解... 正解は「{word['english']}」")
            word["wrong"] += 1

    # 結果表示
    print(f"\n結果: {score}/{count}問正解")

    # 正答率の計算（リスト内包表記）
    rate = score / count * 100
    if rate == 100:
        print("パーフェクト！素晴らしい！")
    elif rate >= 80:
        print("よくできました！")
    elif rate >= 60:
        print("もう少し頑張りましょう！")
    else:
        print("復習が必要です。もう一度挑戦してみましょう！")


def show_stats(words):
    """成績統計を表示する（リスト内包表記、sorted）"""
    total_correct = sum(w["correct"] for w in words)
    total_wrong = sum(w["wrong"] for w in words)
    total = total_correct + total_wrong

    print("\n=== 成績統計 ===")
    print(f"総回答数: {total}")
    print(f"正解: {total_correct}  不正解: {total_wrong}")
    if total > 0:
        print(f"正答率: {total_correct / total * 100:.1f}%")

    # 苦手な単語ランキング（sortedでソート）
    struggled = sorted(words, key=lambda w: w["wrong"], reverse=True)
    struggled = [w for w in struggled if w["wrong"] > 0]  # 内包表記でフィルタ

    if struggled:
        print("\n--- 苦手な単語 TOP3 ---")
        for w in struggled[:3]:  # スライスで上位3つ
            print(f"  {w['english']} ({w['japanese']}) - {w['wrong']}回間違い")


# === メインループ ===
print("+" + "-" * 28 + "+")
print("|      単語帳アプリ         |")
print("+" + "-" * 28 + "+")

while True:
    print("\n--- メニュー ---")
    print("1. 単語一覧")
    print("2. 単語を追加")
    print("3. クイズに挑戦")
    print("4. 成績を見る")
    print("5. 終了")

    choice = input("選択 (1-5): ").strip()

    if choice == "1":
        show_word_list(words)
    elif choice == "2":
        add_word(words)
    elif choice == "3":
        count = input("出題数（Enter で5問）: ").strip()
        count = int(count) if count else 5
        quiz(words, count)
    elif choice == "4":
        show_stats(words)
    elif choice == "5":
        print("お疲れさまでした！")
        break
    else:
        print("1〜5の数字を入力してください。")
