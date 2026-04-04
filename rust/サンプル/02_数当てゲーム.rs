/*
 * ============================================================
 *  数当てゲーム
 * ============================================================
 *
 *  【学べる内容】
 *    - ループ（loop, while）と break / continue
 *    - 条件分岐（if / else if / else, match）
 *    - 標準入力の読み取りとパース
 *    - 簡易乱数生成（外部crateなしで時間ベース）
 *    - 列挙型 Ordering の使い方（std::cmp::Ordering）
 *    - 変数のシャドーイング
 *
 *  【実行方法】
 *    rustc 02_数当てゲーム.rs && ./02_数当てゲーム
 *
 * ============================================================
 */

use std::cmp::Ordering;
use std::io;
use std::io::Write;
use std::time::SystemTime;

// ────────────────────────────────────────
//  簡易乱数生成器
//  外部crateを使わず、システム時刻をシードにした
//  線形合同法（LCG）で擬似乱数を生成する
// ────────────────────────────────────────
struct SimpleRng {
    state: u64,
}

impl SimpleRng {
    /// システム時刻からシードを取得して初期化
    fn new() -> Self {
        let seed = SystemTime::now()
            .duration_since(SystemTime::UNIX_EPOCH)
            .unwrap()
            .as_nanos() as u64;
        SimpleRng { state: seed }
    }

    /// 次の乱数を生成（線形合同法）
    fn next(&mut self) -> u64 {
        // パラメータは glibc 準拠
        self.state = self.state
            .wrapping_mul(6364136223846793005)
            .wrapping_add(1442695040888963407);
        self.state
    }

    /// min 以上 max 以下の乱数を返す
    fn range(&mut self, min: u32, max: u32) -> u32 {
        let range = (max - min + 1) as u64;
        (self.next() % range) as u32 + min
    }
}

// ────────────────────────────────────────
//  難易度の設定
// ────────────────────────────────────────
struct Difficulty {
    name: &'static str,   // 難易度名
    max_number: u32,       // 数の上限
    max_attempts: u32,     // 試行回数の上限
}

/// 難易度を選択する関数
fn select_difficulty() -> Difficulty {
    println!("難易度を選んでください：");
    println!("  1. かんたん （1〜20,  試行回数: 8回）");
    println!("  2. ふつう   （1〜50,  試行回数: 8回）");
    println!("  3. むずかしい（1〜100, 試行回数: 7回）");
    println!();

    loop {
        print!("選択 (1/2/3) > ");
        io::stdout().flush().unwrap();

        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();

        // match 式で入力に応じた Difficulty を返す
        match input.trim() {
            "1" => {
                return Difficulty {
                    name: "かんたん",
                    max_number: 20,
                    max_attempts: 8,
                };
            }
            "2" => {
                return Difficulty {
                    name: "ふつう",
                    max_number: 50,
                    max_attempts: 8,
                };
            }
            "3" => {
                return Difficulty {
                    name: "むずかしい",
                    max_number: 100,
                    max_attempts: 7,
                };
            }
            _ => {
                println!("1, 2, 3 のいずれかを入力してください。");
            }
        }
    }
}

// ────────────────────────────────────────
//  ヒントを表示する関数
// ────────────────────────────────────────
fn show_hint(guess: u32, answer: u32, remaining: u32) {
    // std::cmp::Ordering を使った比較
    match guess.cmp(&answer) {
        Ordering::Less => {
            println!("  → もっと大きい数です！");
            // 残り回数が少ないとき追加ヒント
            if remaining <= 2 {
                let diff = answer - guess;
                if diff <= 5 {
                    println!("  💡 ヒント: かなり近いです！");
                } else if diff <= 15 {
                    println!("  💡 ヒント: もう少しです。");
                }
            }
        }
        Ordering::Greater => {
            println!("  → もっと小さい数です！");
            if remaining <= 2 {
                let diff = guess - answer;
                if diff <= 5 {
                    println!("  💡 ヒント: かなり近いです！");
                } else if diff <= 15 {
                    println!("  💡 ヒント: もう少しです。");
                }
            }
        }
        Ordering::Equal => {
            // ここには来ないはずだが、パターンを網羅するために記載
            println!("  → 正解！");
        }
    }
}

// ────────────────────────────────────────
//  ゲームのメインループ
// ────────────────────────────────────────
fn play_game() -> bool {
    let difficulty = select_difficulty();
    let mut rng = SimpleRng::new();
    let answer = rng.range(1, difficulty.max_number);

    println!();
    println!(
        "【{}モード】1〜{} の中から数を当ててください！（最大{}回）",
        difficulty.name, difficulty.max_number, difficulty.max_attempts
    );
    println!();

    let mut attempts: u32 = 0;

    // loop は無限ループ。break で抜ける
    loop {
        let remaining = difficulty.max_attempts - attempts;
        print!("残り{}回 | 予想を入力 > ", remaining);
        io::stdout().flush().unwrap();

        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();

        // シャドーイング: 同じ名前で型を変えて再束縛
        let guess: u32 = match input.trim().parse() {
            Ok(num) => num,
            Err(_) => {
                println!("  ※ 数字を入力してください。");
                continue; // ループの先頭に戻る（回数は消費しない）
            }
        };

        // 範囲チェック
        if guess < 1 || guess > difficulty.max_number {
            println!(
                "  ※ 1〜{} の範囲で入力してください。",
                difficulty.max_number
            );
            continue;
        }

        attempts += 1;

        if guess == answer {
            println!();
            println!("🎉 正解！ {}回目で当たりました！", attempts);
            // スコア評価
            let score = match attempts {
                1 => "【S】天才！一発正解！",
                2..=3 => "【A】素晴らしい！",
                4..=5 => "【B】なかなかの腕前！",
                _ => "【C】よく頑張りました！",
            };
            println!("  評価: {}", score);
            return true; // 正解で終了
        }

        // 不正解のヒントを表示
        show_hint(guess, answer, difficulty.max_attempts - attempts);

        // 試行回数の上限チェック
        if attempts >= difficulty.max_attempts {
            println!();
            println!("😢 残念！回数を使い切りました。");
            println!("  正解は {} でした。", answer);
            return false; // 不正解で終了
        }
    }
}

// ────────────────────────────────────────
//  メイン関数
// ────────────────────────────────────────
fn main() {
    println!("╔══════════════════════════════════════╗");
    println!("║        🎯 数当てゲーム 🎯           ║");
    println!("╚══════════════════════════════════════╝");
    println!();

    let mut wins: u32 = 0;
    let mut losses: u32 = 0;

    // while ループで繰り返しプレイ
    loop {
        let result = play_game();
        if result {
            wins += 1;
        } else {
            losses += 1;
        }

        println!();
        println!("--- 戦績: {}勝 {}敗 ---", wins, losses);
        println!();
        print!("もう一度遊びますか？ (y/n) > ");
        io::stdout().flush().unwrap();

        let mut input = String::new();
        io::stdin().read_line(&mut input).unwrap();

        if !input.trim().starts_with('y') && !input.trim().starts_with('Y') {
            break;
        }
        println!();
    }

    println!();
    println!("遊んでくれてありがとう！最終戦績: {}勝 {}敗", wins, losses);
}
