/**
 * ============================================================
 * 自己紹介カード生成プログラム
 * ============================================================
 *
 * 【学べる内容】
 *   - 基本的な入出力（cin / cout）
 *   - 文字列型（std::string）の扱い方
 *   - 基本データ型（int, double, string, bool）
 *   - getline() による空白を含む入力の取得
 *   - 文字列の連結とフォーマット出力
 *   - iomanip を使った出力整形
 *   - 条件分岐（if / switch）
 *
 * 【実行方法】
 *   g++ -std=c++17 01_自己紹介カード.cpp -o self_intro && ./self_intro
 *
 * 【テーマ】
 *   対話形式で情報を入力し、装飾されたプロフィールカードを
 *   コンソール上に表示する実用的なプログラムです。
 * ============================================================
 */

#include <iostream>
#include <string>
#include <iomanip>
#include <vector>
#include <algorithm>

using namespace std;

// カードの横幅（文字数）
const int CARD_WIDTH = 50;

// 区切り線を描画する関数
void printBorder(char corner, char horizontal) {
    cout << corner;
    for (int i = 0; i < CARD_WIDTH - 2; i++) {
        cout << horizontal;
    }
    cout << corner << endl;
}

// 中央揃えで文字列を表示する関数
void printCentered(const string& text) {
    // 日本語はマルチバイトなので簡易的な処理
    int padding = (CARD_WIDTH - 2 - static_cast<int>(text.size())) / 2;
    if (padding < 0) padding = 0;
    cout << "|";
    cout << string(padding, ' ');
    cout << text;
    // 右側のパディングを調整
    int rightPad = CARD_WIDTH - 2 - padding - static_cast<int>(text.size());
    if (rightPad < 0) rightPad = 0;
    cout << string(rightPad, ' ');
    cout << "|" << endl;
}

// ラベル付きの行を表示する関数
void printField(const string& label, const string& value) {
    string line = "  " + label + ": " + value;
    int rightPad = CARD_WIDTH - 2 - static_cast<int>(line.size());
    if (rightPad < 0) rightPad = 0;
    cout << "|" << line << string(rightPad, ' ') << "|" << endl;
}

// 空行を表示する関数
void printEmptyLine() {
    cout << "|" << string(CARD_WIDTH - 2, ' ') << "|" << endl;
}

// 血液型の名前を返す関数
string getBloodTypeName(int choice) {
    switch (choice) {
        case 1: return "A";
        case 2: return "B";
        case 3: return "O";
        case 4: return "AB";
        default: return "unknown";
    }
}

// 星座を計算する関数（月と日から）
string getZodiacSign(int month, int day) {
    // 星座の境界日と名称
    vector<pair<pair<int,int>, string>> signs = {
        {{1, 20}, "Capricorn"},   {{2, 19}, "Aquarius"},
        {{3, 20}, "Pisces"},      {{4, 20}, "Aries"},
        {{5, 21}, "Taurus"},      {{6, 21}, "Gemini"},
        {{7, 23}, "Cancer"},      {{8, 23}, "Leo"},
        {{9, 23}, "Virgo"},       {{10, 23}, "Libra"},
        {{11, 22}, "Scorpio"},    {{12, 22}, "Sagittarius"},
        {{12, 31}, "Capricorn"}
    };

    for (auto& [boundary, name] : signs) {
        if (month < boundary.first ||
            (month == boundary.first && day <= boundary.second)) {
            return name;
        }
    }
    return "Capricorn";
}

int main() {
    // === ようこそメッセージ ===
    cout << "========================================" << endl;
    cout << "   Welcome to Self-Introduction Card!" << endl;
    cout << "========================================" << endl;
    cout << endl;

    // === ユーザー情報の入力 ===
    string name;
    cout << "Your name: ";
    getline(cin, name);  // getline で空白を含む名前も取得可能

    int age;
    cout << "Your age: ";
    cin >> age;
    cin.ignore();  // 改行文字をバッファから除去（重要！）

    int birthMonth, birthDay;
    cout << "Birthday (month day, e.g. 3 15): ";
    cin >> birthMonth >> birthDay;
    cin.ignore();

    string hometown;
    cout << "Hometown: ";
    getline(cin, hometown);

    string occupation;
    cout << "Occupation / School: ";
    getline(cin, occupation);

    // 趣味を複数入力
    cout << "How many hobbies do you have? ";
    int hobbyCount;
    cin >> hobbyCount;
    cin.ignore();

    vector<string> hobbies;
    for (int i = 0; i < hobbyCount; i++) {
        string hobby;
        cout << "  Hobby " << (i + 1) << ": ";
        getline(cin, hobby);
        hobbies.push_back(hobby);
    }

    // 血液型の選択
    cout << "Blood type? (1:A  2:B  3:O  4:AB): ";
    int bloodChoice;
    cin >> bloodChoice;
    cin.ignore();

    string motto;
    cout << "Motto / Favorite phrase: ";
    getline(cin, motto);

    // 自己PR
    string selfPR;
    cout << "Brief self-introduction: ";
    getline(cin, selfPR);

    // === 星座を自動計算 ===
    string zodiac = getZodiacSign(birthMonth, birthDay);
    string bloodType = getBloodTypeName(bloodChoice);

    // === カードの描画 ===
    cout << endl;
    cout << endl;

    // 上部の飾り枠
    printBorder('+', '-');
    printEmptyLine();
    printCentered("*** PROFILE CARD ***");
    printEmptyLine();
    printBorder('+', '-');

    // 基本情報セクション
    printEmptyLine();
    printField("Name", name);
    printField("Age", to_string(age));
    printField("Birthday", to_string(birthMonth) + "/" + to_string(birthDay)
               + " (" + zodiac + ")");
    printField("Blood", bloodType);
    printField("From", hometown);
    printField("Work", occupation);
    printEmptyLine();

    // 趣味セクション
    printBorder('|', '-');
    printCentered("[ Hobbies ]");
    printEmptyLine();
    for (size_t i = 0; i < hobbies.size(); i++) {
        string hobbyLine = "  * " + hobbies[i];
        int rightPad = CARD_WIDTH - 2 - static_cast<int>(hobbyLine.size());
        if (rightPad < 0) rightPad = 0;
        cout << "|" << hobbyLine << string(rightPad, ' ') << "|" << endl;
    }
    printEmptyLine();

    // 座右の銘セクション
    printBorder('|', '-');
    printCentered("[ Motto ]");
    printEmptyLine();
    printCentered("\"" + motto + "\"");
    printEmptyLine();

    // 自己PRセクション
    printBorder('|', '-');
    printCentered("[ About Me ]");
    printEmptyLine();
    // 長い文は折り返して表示
    int maxLineLen = CARD_WIDTH - 6;
    for (size_t pos = 0; pos < selfPR.size(); pos += maxLineLen) {
        string segment = selfPR.substr(pos, maxLineLen);
        string line = "  " + segment;
        int rightPad = CARD_WIDTH - 2 - static_cast<int>(line.size());
        if (rightPad < 0) rightPad = 0;
        cout << "|" << line << string(rightPad, ' ') << "|" << endl;
    }
    printEmptyLine();

    // 下部の飾り枠
    printBorder('+', '=');

    // === もう一枚作るか確認 ===
    cout << endl;
    cout << "Your profile card is ready!" << endl;
    cout << "Thank you, " << name << "!" << endl;

    return 0;
}
