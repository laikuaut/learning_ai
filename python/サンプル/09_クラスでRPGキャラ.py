# ==============================
# クラスでRPGキャラ
# 第9章：クラスとオブジェクト指向の実践
# ==============================
# 学べる内容:
#   - クラスの定義（class）と __init__ メソッド
#   - インスタンス変数とメソッド
#   - 継承（Inheritance）の活用
#   - メソッドのオーバーライド
#   - 特殊メソッド（__str__, __repr__）
#   - クラスメソッドとスタティックメソッド
#   - プロパティ（@property）
#   - ポリモーフィズムの実践
# 実行方法:
#   python 09_クラスでRPGキャラ.py
# ==============================

import random


# === 基底クラス ===

class Character:
    """RPGキャラクターの基底クラス"""

    # クラス変数：全キャラクター共通のカウンター
    total_characters = 0

    def __init__(self, name, hp, attack, defense):
        """コンストラクタ：キャラクター生成時に呼ばれる"""
        self.name = name
        self._max_hp = hp       # プライベートっぽく使う慣例（先頭_）
        self._hp = hp
        self.attack = attack
        self.defense = defense
        self.level = 1
        self.exp = 0
        self.is_alive = True

        # クラス変数のカウントアップ
        Character.total_characters += 1

    # --- プロパティ ---
    @property
    def hp(self):
        """HPの取得（読み取り専用のようにアクセスできる）"""
        return self._hp

    @hp.setter
    def hp(self, value):
        """HPの設定（0〜最大HP の範囲に制限）"""
        self._hp = max(0, min(value, self._max_hp))
        if self._hp == 0:
            self.is_alive = False

    @property
    def max_hp(self):
        return self._max_hp

    # --- 特殊メソッド ---
    def __str__(self):
        """print() で表示されるときの文字列"""
        return (f"{self.name}（Lv.{self.level}）"
                f" HP:{self.hp}/{self.max_hp}"
                f" 攻撃:{self.attack} 防御:{self.defense}")

    def __repr__(self):
        """デバッグ用の文字列表現"""
        return (f"Character(name='{self.name}', hp={self.hp}, "
                f"attack={self.attack}, defense={self.defense})")

    # --- 通常メソッド ---
    def take_damage(self, damage):
        """ダメージを受ける"""
        # 防御力でダメージ軽減（最低1ダメージ）
        actual_damage = max(1, damage - self.defense)
        self.hp -= actual_damage
        print(f"  {self.name} は {actual_damage} のダメージを受けた！"
              f"（HP: {self.hp}/{self.max_hp}）")
        if not self.is_alive:
            print(f"  {self.name} は倒れた...")
        return actual_damage

    def heal(self, amount):
        """回復する"""
        old_hp = self.hp
        self.hp += amount
        healed = self.hp - old_hp
        print(f"  {self.name} は {healed} 回復した！"
              f"（HP: {self.hp}/{self.max_hp}）")

    def gain_exp(self, amount):
        """経験値を獲得する"""
        self.exp += amount
        print(f"  {self.name} は {amount} の経験値を獲得！（合計: {self.exp}）")
        # 100経験値ごとにレベルアップ
        while self.exp >= self.level * 100:
            self.exp -= self.level * 100
            self.level_up()

    def level_up(self):
        """レベルアップ処理"""
        self.level += 1
        # ステータス上昇
        self._max_hp += 10
        self._hp = self._max_hp  # 全回復
        self.attack += 3
        self.defense += 2
        print(f"  ★ {self.name} はレベル {self.level} になった！")
        print(f"    HP:{self.max_hp} 攻撃:{self.attack} 防御:{self.defense}")

    def show_status(self):
        """ステータスを表示する"""
        print(f"  {self}")

    # --- クラスメソッド ---
    @classmethod
    def get_total_characters(cls):
        """作成されたキャラクターの総数を返す"""
        return cls.total_characters

    # --- スタティックメソッド ---
    @staticmethod
    def calculate_damage(attack, defense):
        """ダメージ計算（インスタンスに依存しない純粋な計算）"""
        return max(1, attack - defense)


# === 戦士クラス（継承）===

class Warrior(Character):
    """戦士クラス：高いHP と防御力"""

    def __init__(self, name):
        # 親クラスの __init__ を呼ぶ
        super().__init__(name, hp=120, attack=15, defense=10)
        self.skill_name = "パワースラッシュ"

    def skill_attack(self, target):
        """スキル攻撃：通常の1.5倍ダメージ"""
        print(f"\n  {self.name} の『{self.skill_name}』！")
        damage = int(self.attack * 1.5)
        target.take_damage(damage)

    # レベルアップのオーバーライド（戦士はHP多めに上昇）
    def level_up(self):
        self.level += 1
        self._max_hp += 20  # 戦士はHP上昇が大きい
        self._hp = self._max_hp
        self.attack += 4
        self.defense += 3
        print(f"  ★ {self.name}（戦士）はレベル {self.level} になった！")
        print(f"    HP:{self.max_hp} 攻撃:{self.attack} 防御:{self.defense}")


# === 魔法使いクラス（継承）===

class Mage(Character):
    """魔法使いクラス：高い攻撃力と魔法"""

    def __init__(self, name):
        super().__init__(name, hp=80, attack=20, defense=5)
        self.mp = 50
        self.max_mp = 50
        self.skill_name = "ファイアボール"

    def __str__(self):
        """魔法使いは MP も表示する（オーバーライド）"""
        return (f"{self.name}（Lv.{self.level}）"
                f" HP:{self.hp}/{self.max_hp}"
                f" MP:{self.mp}/{self.max_mp}"
                f" 攻撃:{self.attack} 防御:{self.defense}")

    def skill_attack(self, target):
        """魔法攻撃：MP消費で大ダメージ"""
        mp_cost = 10
        if self.mp < mp_cost:
            print(f"  {self.name}：MPが足りない！（MP: {self.mp}）")
            return
        self.mp -= mp_cost
        print(f"\n  {self.name} の『{self.skill_name}』！（MP: {self.mp}/{self.max_mp}）")
        # 魔法攻撃は防御無視でダメージ
        damage = int(self.attack * 2)
        actual = max(1, damage - target.defense // 2)
        target.take_damage(actual)

    def level_up(self):
        self.level += 1
        self._max_hp += 8
        self._hp = self._max_hp
        self.max_mp += 10
        self.mp = self.max_mp
        self.attack += 5
        self.defense += 1
        print(f"  ★ {self.name}（魔法使い）はレベル {self.level} になった！")
        print(f"    HP:{self.max_hp} MP:{self.max_mp}"
              f" 攻撃:{self.attack} 防御:{self.defense}")


# === ヒーラークラス（継承）===

class Healer(Character):
    """ヒーラークラス：味方を回復できる"""

    def __init__(self, name):
        super().__init__(name, hp=90, attack=10, defense=8)
        self.mp = 60
        self.max_mp = 60
        self.skill_name = "ヒーリング"

    def __str__(self):
        return (f"{self.name}（Lv.{self.level}）"
                f" HP:{self.hp}/{self.max_hp}"
                f" MP:{self.mp}/{self.max_mp}"
                f" 攻撃:{self.attack} 防御:{self.defense}")

    def skill_heal(self, target):
        """回復魔法：味方を回復する"""
        mp_cost = 15
        if self.mp < mp_cost:
            print(f"  {self.name}：MPが足りない！（MP: {self.mp}）")
            return
        self.mp -= mp_cost
        heal_amount = 30 + self.level * 5
        print(f"\n  {self.name} の『{self.skill_name}』！（MP: {self.mp}/{self.max_mp}）")
        target.heal(heal_amount)

    def level_up(self):
        self.level += 1
        self._max_hp += 10
        self._hp = self._max_hp
        self.max_mp += 15
        self.mp = self.max_mp
        self.attack += 2
        self.defense += 2
        print(f"  ★ {self.name}（ヒーラー）はレベル {self.level} になった！")
        print(f"    HP:{self.max_hp} MP:{self.max_mp}"
              f" 攻撃:{self.attack} 防御:{self.defense}")


# === モンスタークラス ===

class Monster(Character):
    """モンスタークラス"""

    def __init__(self, name, hp, attack, defense, exp_reward):
        super().__init__(name, hp, attack, defense)
        self.exp_reward = exp_reward

    def act(self, targets):
        """モンスターの行動（ランダムに攻撃）"""
        if not self.is_alive:
            return
        # 生きているターゲットからランダムに選択
        alive_targets = [t for t in targets if t.is_alive]
        if not alive_targets:
            return
        target = random.choice(alive_targets)
        print(f"\n  {self.name} の攻撃！")
        target.take_damage(self.attack)


# === バトルシステム ===

def battle(party, monsters):
    """パーティ vs モンスターのバトル"""
    print("\n" + "=" * 50)
    print("  バトル開始！")
    print("=" * 50)

    print("\n【敵】")
    for m in monsters:
        m.show_status()

    print("\n【味方】")
    for p in party:
        p.show_status()

    turn = 1
    while True:
        print(f"\n--- ターン {turn} ---")

        # プレイヤーの行動
        for member in party:
            if not member.is_alive:
                continue

            # 敵が全滅しているか確認
            alive_monsters = [m for m in monsters if m.is_alive]
            if not alive_monsters:
                break

            print(f"\n{member.name} の行動：")
            print("  1. 通常攻撃")
            if isinstance(member, (Warrior, Mage)):
                print(f"  2. スキル（{member.skill_name}）")
            elif isinstance(member, Healer):
                print(f"  2. 回復魔法（{member.skill_name}）")

            choice = input("  選択: ").strip()

            if choice == "2":
                if isinstance(member, Healer):
                    # ヒーラーは一番HPが低い味方を回復
                    alive_party = [p for p in party if p.is_alive]
                    weakest = min(alive_party, key=lambda p: p.hp / p.max_hp)
                    member.skill_heal(weakest)
                elif isinstance(member, (Warrior, Mage)):
                    # 最初の生きている敵を攻撃
                    target = alive_monsters[0]
                    member.skill_attack(target)
            else:
                # 通常攻撃
                target = alive_monsters[0]
                print(f"\n  {member.name} の攻撃！")
                target.take_damage(member.attack)

        # 敵が全滅しているか確認
        alive_monsters = [m for m in monsters if m.is_alive]
        if not alive_monsters:
            print("\n" + "=" * 50)
            print("  勝利！！")
            print("=" * 50)
            # 経験値の配布
            total_exp = sum(m.exp_reward for m in monsters)
            print(f"\n  獲得経験値: {total_exp}")
            for member in party:
                if member.is_alive:
                    member.gain_exp(total_exp)
            return True

        # モンスターの行動
        for monster in monsters:
            if monster.is_alive:
                alive_party = [p for p in party if p.is_alive]
                if alive_party:
                    monster.act(alive_party)

        # 味方が全滅しているか確認
        alive_party = [p for p in party if p.is_alive]
        if not alive_party:
            print("\n" + "=" * 50)
            print("  全滅... ゲームオーバー")
            print("=" * 50)
            return False

        # 状況表示
        print("\n【現在の状況】")
        for p in party:
            marker = " " if p.is_alive else "x"
            print(f"  [{marker}] {p}")
        for m in monsters:
            if m.is_alive:
                print(f"  [敵] {m}")

        turn += 1


# === キャラクター作成 ===

def create_character():
    """対話式でキャラクターを作成する"""
    print("\n--- キャラクター作成 ---")
    name = input("名前を入力: ").strip()
    if not name:
        name = "勇者"

    print("職業を選択:")
    print("  1. 戦士（HP・防御が高い）")
    print("  2. 魔法使い（攻撃魔法が強力）")
    print("  3. ヒーラー（味方を回復できる）")

    choice = input("選択 (1-3): ").strip()

    if choice == "2":
        return Mage(name)
    elif choice == "3":
        return Healer(name)
    else:
        return Warrior(name)


# === モンスター生成 ===

def generate_monsters(difficulty=1):
    """難易度に応じたモンスターを生成する"""
    monster_templates = [
        ("スライム", 30, 8, 2, 30),
        ("ゴブリン", 50, 12, 5, 50),
        ("オーク", 80, 18, 8, 80),
        ("ドラゴン", 150, 25, 15, 200),
    ]

    # 難易度に応じて敵の数と種類を決定
    if difficulty == 1:
        templates = monster_templates[:2]
        count = random.randint(1, 2)
    elif difficulty == 2:
        templates = monster_templates[1:3]
        count = random.randint(2, 3)
    else:
        templates = monster_templates[2:]
        count = random.randint(1, 2)

    monsters = []
    for _ in range(count):
        name, hp, atk, dfn, exp = random.choice(templates)
        # 個体差をつける
        hp_var = random.randint(-5, 5)
        atk_var = random.randint(-2, 2)
        monsters.append(Monster(name, hp + hp_var, atk + atk_var, dfn, exp))

    return monsters


# === メインプログラム ===

print("+" + "-" * 34 + "+")
print("|     RPGキャラクターバトル       |")
print("+" + "-" * 34 + "+")

# パーティ作成
print("\nパーティを編成しましょう！（最大3人）")
party = []
for i in range(3):
    print(f"\n--- {i + 1}人目 ---")
    create_more = input("キャラクターを作成しますか？ (y/n): ").strip().lower()
    if create_more != "y" and i > 0:
        break
    member = create_character()
    party.append(member)
    print(f"  {member} を仲間に加えました！")

print(f"\n作成されたキャラクター数: {Character.get_total_characters()}")

# ゲームループ
difficulty = 1
while True:
    print(f"\n--- 冒険メニュー（難易度: {difficulty}）---")
    print("1. バトルへ出発")
    print("2. パーティ状態確認")
    print("3. 冒険を終える")

    choice = input("選択 (1-3): ").strip()

    if choice == "1":
        monsters = generate_monsters(difficulty)
        result = battle(party, monsters)
        if result:
            difficulty = min(difficulty + 1, 3)
            # 生存者を全回復
            for member in party:
                if member.is_alive:
                    member.hp = member.max_hp
            print("\n  パーティは全回復した！")
        else:
            print("\n  冒険は失敗に終わった...")
            break

    elif choice == "2":
        print("\n--- パーティ状態 ---")
        for member in party:
            marker = "生存" if member.is_alive else "戦闘不能"
            print(f"  [{marker}] {member}")

    elif choice == "3":
        print("\nお疲れさまでした！冒険の記録：")
        for member in party:
            print(f"  {member}")
        break

    else:
        print("1〜3の数字を入力してください。")
