/**
 * ============================================================
 * 数当てゲーム（Number Guessing Game）
 * ============================================================
 *
 * 【学べる内容】
 *   - 乱数生成（<random> ヘッダ、メルセンヌ・ツイスタ）
 *   - while / do-while ループ
 *   - 条件分岐（if-else, 三項演算子）
 *   - 関数の定義と呼び出し
 *   - 参照渡し
 *   - ベクトルによるスコア履歴管理
 *   - chrono による時間計測
 *
 * 【実行方法】
 *   g++ -std=c++17 02_数当てゲーム.cpp -o guess_game && ./guess_game
 *
 * 【テーマ】
 *   コンピュータが選んだ1〜100の秘密の数を当てるゲームです。
 *   ヒント（もっと大きい/小さい）を頼りに最短回数を目指しましょう。
 * ============================================================
 */

#include <iostream>
#include <random>
#include <vector>
#include <string>
#include <algorithm>
#include <numeric>
#include <chrono>
#include <iomanip>

using namespace std;

// 難易度の設定を保持する構造体
struct Difficulty {
    string name;       // 難易度名
    int maxNumber;     // 数の上限
    int maxAttempts;   // 最大試行回数（0 = 無制限）
};

// 利用可能な難易度一覧
const vector<Difficulty> DIFFICULTIES = {
    {"Easy   (1-50,  unlimited)", 50, 0},
    {"Normal (1-100, 10 tries)",  100, 10},
    {"Hard   (1-200, 8 tries)",   200, 8},
    {"Expert (1-500, 9 tries)",   500, 9}
};

// ゲーム結果を記録する構造体
struct GameResult {
    int difficulty;      // 難易度番号
    int secretNumber;    // 正解の数
    int attempts;        // かかった試行回数
    bool won;            // 勝ったかどうか
    double elapsedSec;   // かかった時間（秒）
};

// 乱数生成器（プログラム全体で1つ）
mt19937 rng(random_device{}());

// 指定範囲のランダムな整数を返す関数
int getRandomNumber(int minVal, int maxVal) {
    uniform_int_distribution<int> dist(minVal, maxVal);
    return dist(rng);
}

// 難易度選択メニューを表示し、選択を返す関数
int selectDifficulty() {
    cout << endl;
    cout << "--- Select Difficulty ---" << endl;
    for (size_t i = 0; i < DIFFICULTIES.size(); i++) {
        cout << "  " << (i + 1) << ". " << DIFFICULTIES[i].name << endl;
    }
    cout << "-------------------------" << endl;

    int choice;
    do {
        cout << "Choice (1-" << DIFFICULTIES.size() << "): ";
        cin >> choice;
    } while (choice < 1 || choice > static_cast<int>(DIFFICULTIES.size()));

    return choice - 1;  // 0-based インデックスで返す
}

// ヒントのバー表示を生成する関数
string createHintBar(int guess, int secret, int maxNum) {
    const int barWidth = 30;
    int guessPos = guess * barWidth / maxNum;
    int secretPos = secret * barWidth / maxNum;

    string bar(barWidth, '-');
    // 範囲のインジケータを表示
    if (guessPos >= 0 && guessPos < barWidth) {
        bar[guessPos] = 'G';  // Guess位置
    }
    return "[" + bar + "]";
}

// 1回のゲームを実行する関数
GameResult playOneGame(int diffIndex) {
    const Difficulty& diff = DIFFICULTIES[diffIndex];

    // 秘密の数を生成
    int secret = getRandomNumber(1, diff.maxNumber);
    int attempts = 0;

    cout << endl;
    cout << "=================================" << endl;
    cout << " I'm thinking of a number" << endl;
    cout << " between 1 and " << diff.maxNumber << "!" << endl;
    if (diff.maxAttempts > 0) {
        cout << " You have " << diff.maxAttempts << " attempts." << endl;
    } else {
        cout << " Unlimited attempts." << endl;
    }
    cout << "=================================" << endl;
    cout << endl;

    // 時間計測の開始
    auto startTime = chrono::steady_clock::now();

    bool won = false;

    while (true) {
        // 残り回数の表示（制限がある場合）
        if (diff.maxAttempts > 0) {
            int remaining = diff.maxAttempts - attempts;
            cout << "[Remaining: " << remaining << "] ";
        }

        // ユーザーの入力を取得
        cout << "Your guess: ";
        int guess;
        cin >> guess;

        // 入力範囲のチェック
        if (guess < 1 || guess > diff.maxNumber) {
            cout << "  -> Please enter a number between 1 and "
                 << diff.maxNumber << "." << endl;
            continue;  // 試行回数にはカウントしない
        }

        attempts++;

        // 正解判定
        if (guess == secret) {
            won = true;
            break;
        }

        // ヒントの表示
        if (guess < secret) {
            int diff_val = secret - guess;
            if (diff_val <= 5) {
                cout << "  -> Very close! Go HIGHER!" << endl;
            } else if (diff_val <= 15) {
                cout << "  -> Close. Go higher." << endl;
            } else {
                cout << "  -> Too low. Go much higher." << endl;
            }
        } else {
            int diff_val = guess - secret;
            if (diff_val <= 5) {
                cout << "  -> Very close! Go LOWER!" << endl;
            } else if (diff_val <= 15) {
                cout << "  -> Close. Go lower." << endl;
            } else {
                cout << "  -> Too high. Go much lower." << endl;
            }
        }

        // 試行回数の上限チェック
        if (diff.maxAttempts > 0 && attempts >= diff.maxAttempts) {
            cout << endl;
            cout << "  Game Over! You've used all attempts." << endl;
            cout << "  The answer was: " << secret << endl;
            break;
        }
    }

    // 時間計測の終了
    auto endTime = chrono::steady_clock::now();
    double elapsed = chrono::duration<double>(endTime - startTime).count();

    // 勝利メッセージの表示
    if (won) {
        cout << endl;
        cout << "***************************" << endl;
        cout << " Correct! The answer was " << secret << "!" << endl;
        cout << " Attempts: " << attempts << endl;
        cout << " Time: " << fixed << setprecision(1) << elapsed << " sec" << endl;

        // 評価コメント
        if (attempts <= 3) {
            cout << " Rating: Amazing!!" << endl;
        } else if (attempts <= 6) {
            cout << " Rating: Great!" << endl;
        } else if (attempts <= 10) {
            cout << " Rating: Good." << endl;
        } else {
            cout << " Rating: Keep trying!" << endl;
        }
        cout << "***************************" << endl;
    }

    // 結果を返す
    return {diffIndex, secret, attempts, won, elapsed};
}

// スコア履歴を表示する関数
void showHistory(const vector<GameResult>& history) {
    if (history.empty()) {
        cout << "No games played yet." << endl;
        return;
    }

    cout << endl;
    cout << "====== Game History ======" << endl;
    cout << " #  | Diff | Answer | Tries | Time   | Result" << endl;
    cout << "----|------|--------|-------|--------|-------" << endl;

    for (size_t i = 0; i < history.size(); i++) {
        const auto& r = history[i];
        cout << " " << setw(2) << (i + 1) << " | "
             << setw(4) << (r.difficulty + 1) << " | "
             << setw(6) << r.secretNumber << " | "
             << setw(5) << r.attempts << " | "
             << fixed << setprecision(1) << setw(5) << r.elapsedSec << "s | "
             << (r.won ? "WIN" : "LOSE") << endl;
    }

    // 統計情報
    int wins = 0;
    int totalAttempts = 0;
    for (const auto& r : history) {
        if (r.won) wins++;
        totalAttempts += r.attempts;
    }

    cout << "==========================" << endl;
    cout << " Total games: " << history.size() << endl;
    cout << " Wins: " << wins << " / Losses: " << (history.size() - wins) << endl;
    cout << " Win rate: " << (wins * 100 / static_cast<int>(history.size())) << "%" << endl;
    cout << " Avg attempts: " << fixed << setprecision(1)
         << (static_cast<double>(totalAttempts) / history.size()) << endl;
    cout << "==========================" << endl;
}


int main() {
    cout << "==============================" << endl;
    cout << "   Number Guessing Game" << endl;
    cout << "==============================" << endl;

    vector<GameResult> history;  // ゲーム履歴を保持

    // メインループ
    while (true) {
        cout << endl;
        cout << "--- Main Menu ---" << endl;
        cout << "  1. Play a new game" << endl;
        cout << "  2. View history" << endl;
        cout << "  3. Quit" << endl;
        cout << "-----------------" << endl;
        cout << "Choice: ";

        int menuChoice;
        cin >> menuChoice;

        switch (menuChoice) {
            case 1: {
                // 難易度を選択してゲーム開始
                int diff = selectDifficulty();
                GameResult result = playOneGame(diff);
                history.push_back(result);
                break;
            }
            case 2:
                showHistory(history);
                break;
            case 3:
                cout << endl;
                cout << "Thanks for playing! Goodbye!" << endl;
                return 0;
            default:
                cout << "Invalid choice." << endl;
        }
    }

    return 0;
}
