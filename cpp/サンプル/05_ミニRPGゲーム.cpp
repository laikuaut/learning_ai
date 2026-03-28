/**
 * ============================================================
 * ミニRPGバトルゲーム（Mini RPG Battle Game）
 * ============================================================
 *
 * 【学べる内容】
 *   - 継承（inheritance）と仮想関数（virtual functions）
 *   - ポリモーフィズム（多態性）の活用
 *   - スマートポインタ（std::unique_ptr）
 *   - 抽象クラスと純粋仮想関数
 *   - STLコンテナ（vector, map）の組み合わせ
 *   - 乱数生成とゲームロジックの設計
 *   - enum class による型安全な列挙型
 *
 * 【実行方法】
 *   g++ -std=c++17 05_ミニRPGゲーム.cpp -o mini_rpg && ./mini_rpg
 *
 * 【テーマ】
 *   プレイヤーが戦士・魔法使い・ヒーラーから職業を選び、
 *   ダンジョンに出現するモンスターと戦うRPGゲームです。
 *   オブジェクト指向プログラミングの実践的な活用例です。
 * ============================================================
 */

#include <iostream>
#include <string>
#include <vector>
#include <memory>
#include <random>
#include <algorithm>
#include <iomanip>
#include <map>

using namespace std;

// === 乱数生成のユーティリティ ===
mt19937 rng(random_device{}());

int randomInt(int minVal, int maxVal) {
    return uniform_int_distribution<int>(minVal, maxVal)(rng);
}

// === キャラクターの基底クラス（抽象クラス） ===
class Character {
protected:
    string name_;      // 名前
    int maxHp_;        // 最大HP
    int hp_;           // 現在HP
    int attack_;       // 攻撃力
    int defense_;      // 防御力
    int level_;        // レベル
    int exp_;          // 経験値

public:
    Character(const string& name, int hp, int attack, int defense)
        : name_(name), maxHp_(hp), hp_(hp),
          attack_(attack), defense_(defense),
          level_(1), exp_(0) {}

    // 仮想デストラクタ（継承で必須）
    virtual ~Character() = default;

    // ゲッター
    const string& getName() const { return name_; }
    int getHp()      const { return hp_; }
    int getMaxHp()   const { return maxHp_; }
    int getAttack()  const { return attack_; }
    int getDefense() const { return defense_; }
    int getLevel()   const { return level_; }
    bool isAlive()   const { return hp_ > 0; }

    // ダメージを受ける
    void takeDamage(int damage) {
        int actual = max(1, damage - defense_ / 2);
        hp_ = max(0, hp_ - actual);
        cout << "  " << name_ << " takes " << actual << " damage!"
             << " (HP: " << hp_ << "/" << maxHp_ << ")" << endl;
    }

    // HPを回復する
    void heal(int amount) {
        int before = hp_;
        hp_ = min(maxHp_, hp_ + amount);
        cout << "  " << name_ << " recovers " << (hp_ - before) << " HP!"
             << " (HP: " << hp_ << "/" << maxHp_ << ")" << endl;
    }

    // HPバーを表示
    void showHpBar() const {
        int barLen = 20;
        int filled = (hp_ * barLen) / maxHp_;
        cout << "  " << setw(12) << left << name_ << " ";
        cout << "[";
        for (int i = 0; i < barLen; i++) {
            cout << (i < filled ? '#' : '-');
        }
        cout << "] " << hp_ << "/" << maxHp_ << " HP"
             << "  ATK:" << attack_ << " DEF:" << defense_ << endl;
    }

    // 純粋仮想関数 = サブクラスで必ず実装する必要がある
    virtual string getClassName() const = 0;

    // 通常攻撃（仮想関数 = サブクラスでオーバーライド可能）
    virtual int normalAttack() {
        int damage = attack_ + randomInt(-2, 3);
        cout << "  " << name_ << " attacks!" << endl;
        return max(1, damage);
    }

    // スキル攻撃（純粋仮想関数）
    virtual int useSkill() = 0;

    // スキル名（純粋仮想関数）
    virtual string getSkillName() const = 0;
};

// === 戦士クラス（Warrior） ===
class Warrior : public Character {
public:
    Warrior(const string& name)
        : Character(name, 120, 18, 12) {}  // 高HP・高防御

    string getClassName() const override { return "Warrior"; }
    string getSkillName() const override { return "Power Slash"; }

    int useSkill() override {
        // パワースラッシュ：1.5倍〜2倍のダメージ
        int damage = static_cast<int>(attack_ * (1.5 + randomInt(0, 5) / 10.0));
        cout << "  " << name_ << " uses Power Slash!!" << endl;
        return damage;
    }

    // 戦士固有：ガード（防御力一時上昇）
    void guard() {
        defense_ += 5;
        cout << "  " << name_ << " raises guard! (DEF +" << 5 << ")" << endl;
    }
};

// === 魔法使いクラス（Mage） ===
class Mage : public Character {
private:
    int mp_;     // MP
    int maxMp_;

public:
    Mage(const string& name)
        : Character(name, 80, 25, 5), mp_(50), maxMp_(50) {}  // 高攻撃・低防御

    string getClassName() const override { return "Mage"; }
    string getSkillName() const override { return "Fireball (10 MP)"; }

    int getMp() const { return mp_; }

    void showHpBar() const {
        Character::showHpBar();
        cout << "             MP: " << mp_ << "/" << maxMp_ << endl;
    }

    int useSkill() override {
        if (mp_ < 10) {
            cout << "  Not enough MP! Normal attack instead." << endl;
            return normalAttack();
        }
        mp_ -= 10;
        // ファイアボール：高ダメージ
        int damage = attack_ * 2 + randomInt(5, 15);
        cout << "  " << name_ << " casts Fireball!! (MP: "
             << mp_ << "/" << maxMp_ << ")" << endl;
        return damage;
    }
};

// === ヒーラークラス（Healer） ===
class Healer : public Character {
private:
    int mp_;
    int maxMp_;

public:
    Healer(const string& name)
        : Character(name, 100, 12, 8), mp_(60), maxMp_(60) {}  // バランス型

    string getClassName() const override { return "Healer"; }
    string getSkillName() const override { return "Holy Light (8 MP)"; }

    int getMp() const { return mp_; }

    void showHpBar() const {
        Character::showHpBar();
        cout << "             MP: " << mp_ << "/" << maxMp_ << endl;
    }

    int useSkill() override {
        if (mp_ < 8) {
            cout << "  Not enough MP! Normal attack instead." << endl;
            return normalAttack();
        }
        mp_ -= 8;
        // ホーリーライト：ダメージ + 自己回復
        int damage = attack_ + randomInt(5, 10);
        int healAmt = randomInt(15, 30);
        cout << "  " << name_ << " uses Holy Light!! (MP: "
             << mp_ << "/" << maxMp_ << ")" << endl;
        heal(healAmt);
        return damage;
    }
};

// === モンスタークラス ===
class Monster : public Character {
private:
    int expReward_;  // 倒した時にもらえる経験値

public:
    Monster(const string& name, int hp, int attack, int defense, int expReward)
        : Character(name, hp, attack, defense), expReward_(expReward) {}

    string getClassName() const override { return "Monster"; }
    string getSkillName() const override { return "Special Attack"; }

    int getExpReward() const { return expReward_; }

    int useSkill() override {
        int damage = static_cast<int>(attack_ * 1.3) + randomInt(0, 5);
        cout << "  " << name_ << " uses a special attack!!" << endl;
        return damage;
    }
};

// === モンスターを生成するファクトリ関数 ===
unique_ptr<Monster> createMonster(int floor) {
    // フロアに応じて強さを調整
    int scaleFactor = floor;

    // モンスターのバリエーション
    struct MonsterTemplate {
        string name;
        int baseHp, baseAtk, baseDef, baseExp;
    };

    vector<MonsterTemplate> templates = {
        {"Slime",        30, 8,  2, 10},
        {"Goblin",       45, 12, 5, 15},
        {"Wolf",         40, 15, 3, 18},
        {"Skeleton",     55, 14, 8, 22},
        {"Orc",          70, 18, 10, 30},
        {"Dark Mage",    50, 22, 4, 28},
        {"Golem",        90, 16, 15, 35},
        {"Dragon Whelp", 80, 24, 12, 45}
    };

    // フロアに応じたモンスターを選択
    int idx = min(static_cast<int>(templates.size()) - 1,
                  (floor - 1) / 2 + randomInt(0, 1));
    auto& t = templates[idx];

    return make_unique<Monster>(
        t.name,
        t.baseHp + scaleFactor * 5,
        t.baseAtk + scaleFactor * 2,
        t.baseDef + scaleFactor,
        t.baseExp + scaleFactor * 5
    );
}

// === バトル処理 ===
bool battle(Character& player, Monster& monster) {
    cout << endl;
    cout << "========================================" << endl;
    cout << "  A wild " << monster.getName() << " appeared!" << endl;
    cout << "========================================" << endl;

    int turn = 1;

    while (player.isAlive() && monster.isAlive()) {
        cout << endl;
        cout << "--- Turn " << turn << " ---" << endl;
        player.showHpBar();
        monster.showHpBar();

        // プレイヤーの行動選択
        cout << endl;
        cout << "  Actions:" << endl;
        cout << "    1. Attack" << endl;
        cout << "    2. " << player.getSkillName() << endl;
        cout << "    3. Defend" << endl;
        cout << "  Choice: ";

        int action;
        cin >> action;
        cout << endl;

        int playerDamage = 0;
        bool defending = false;

        switch (action) {
            case 1:
                playerDamage = player.normalAttack();
                break;
            case 2:
                playerDamage = player.useSkill();
                break;
            case 3:
                defending = true;
                cout << "  " << player.getName() << " takes a defensive stance!" << endl;
                break;
            default:
                cout << "  Invalid action! Turn wasted." << endl;
                break;
        }

        // プレイヤーの攻撃をモンスターに適用
        if (playerDamage > 0) {
            monster.takeDamage(playerDamage);
        }

        // モンスターが倒れたかチェック
        if (!monster.isAlive()) {
            cout << endl;
            cout << "  >> " << monster.getName() << " was defeated! <<" << endl;
            return true;  // 勝利
        }

        // モンスターのターン
        cout << endl;
        int monsterDamage;
        if (randomInt(1, 100) <= 25) {
            // 25%の確率でスキル攻撃
            monsterDamage = monster.useSkill();
        } else {
            monsterDamage = monster.normalAttack();
        }

        // 防御中はダメージ半減
        if (defending) {
            monsterDamage /= 2;
            cout << "  (Damage halved by defense!)" << endl;
        }

        player.takeDamage(monsterDamage);

        // プレイヤーが倒れたかチェック
        if (!player.isAlive()) {
            cout << endl;
            cout << "  >> " << player.getName() << " was defeated... <<" << endl;
            return false;  // 敗北
        }

        turn++;
    }

    return false;
}

// === メインのゲームループ ===
void gameLoop() {
    cout << "==============================" << endl;
    cout << "    Mini RPG Battle Game" << endl;
    cout << "==============================" << endl;
    cout << endl;

    // プレイヤー名の入力
    cout << "Enter your name: ";
    string playerName;
    cin.ignore();
    getline(cin, playerName);
    if (playerName.empty()) playerName = "Hero";

    // 職業選択
    cout << endl;
    cout << "Choose your class:" << endl;
    cout << "  1. Warrior  - High HP & DEF, Power Slash" << endl;
    cout << "  2. Mage     - High ATK, Fireball (MP)" << endl;
    cout << "  3. Healer   - Balanced, Holy Light heals" << endl;
    cout << "Choice: ";

    int classChoice;
    cin >> classChoice;

    // プレイヤーキャラクターの生成（unique_ptrで管理）
    unique_ptr<Character> player;
    switch (classChoice) {
        case 1:
            player = make_unique<Warrior>(playerName);
            break;
        case 2:
            player = make_unique<Mage>(playerName);
            break;
        case 3:
            player = make_unique<Healer>(playerName);
            break;
        default:
            cout << "Invalid. Defaulting to Warrior." << endl;
            player = make_unique<Warrior>(playerName);
            break;
    }

    cout << endl;
    cout << "You are " << player->getName()
         << " the " << player->getClassName() << "!" << endl;

    // ダンジョン探索ループ
    int floor = 1;
    int totalExp = 0;
    int monstersDefeated = 0;
    map<string, int> defeatedLog;  // 倒したモンスターの記録

    while (player->isAlive()) {
        cout << endl;
        cout << "================================" << endl;
        cout << "  Dungeon Floor " << floor << endl;
        cout << "================================" << endl;

        // モンスターを生成
        auto monster = createMonster(floor);

        // バトル実行
        bool won = battle(*player, *monster);

        if (won) {
            int exp = monster->getExpReward();
            totalExp += exp;
            monstersDefeated++;
            defeatedLog[monster->getName()]++;

            cout << "  Gained " << exp << " EXP! (Total: " << totalExp << ")" << endl;

            // 小回復ボーナス
            int healBonus = randomInt(5, 15);
            player->heal(healBonus);

            // 次のフロアへ進むか確認
            cout << endl;
            cout << "  Continue to next floor? (1: Yes / 0: No): ";
            int cont;
            cin >> cont;

            if (cont != 1) {
                cout << endl;
                cout << "You leave the dungeon safely." << endl;
                break;
            }

            floor++;
        } else {
            // ゲームオーバー
            cout << endl;
            cout << "================================" << endl;
            cout << "        GAME OVER" << endl;
            cout << "  You fell on Floor " << floor << "..." << endl;
            cout << "================================" << endl;
        }
    }

    // === 最終結果の表示 ===
    cout << endl;
    cout << "========================================" << endl;
    cout << "          Adventure Summary" << endl;
    cout << "========================================" << endl;
    cout << "  Player:    " << player->getName()
         << " (" << player->getClassName() << ")" << endl;
    cout << "  Reached:   Floor " << floor << endl;
    cout << "  Defeated:  " << monstersDefeated << " monsters" << endl;
    cout << "  Total EXP: " << totalExp << endl;
    cout << endl;

    if (!defeatedLog.empty()) {
        cout << "  --- Monsters Defeated ---" << endl;
        for (const auto& [name, count] : defeatedLog) {
            cout << "    " << setw(15) << left << name
                 << " x " << count << endl;
        }
    }

    cout << "========================================" << endl;
    cout << "  Thank you for playing!" << endl;
    cout << "========================================" << endl;
}

int main() {
    // ゲームを開始
    gameLoop();

    // リプレイ確認
    cout << endl;
    cout << "Play again? (1: Yes / 0: No): ";
    int replay;
    cin >> replay;

    if (replay == 1) {
        gameLoop();
    }

    cout << "Goodbye!" << endl;
    return 0;
}
