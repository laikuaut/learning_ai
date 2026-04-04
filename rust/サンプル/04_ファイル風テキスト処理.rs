/*
 * ============================================================
 *  ファイル風テキスト処理ツール
 * ============================================================
 *
 *  【学べる内容】
 *    - 文字列操作（split, contains, replace, trim, chars）
 *    - エラーハンドリング（Result型, Option型）
 *    - ? 演算子によるエラーの伝播
 *    - HashMap の活用（単語の出現頻度カウント）
 *    - ライフタイムの基本的な考え方
 *    - トレイト Display の実装
 *
 *  【実行方法】
 *    rustc 04_ファイル風テキスト処理.rs && ./04_ファイル風テキスト処理
 *
 * ============================================================
 */

use std::collections::HashMap;
use std::fmt;
use std::io;
use std::io::Write;

// ────────────────────────────────────────
//  テキスト解析結果を表す構造体
// ────────────────────────────────────────
struct TextStats {
    line_count: usize,      // 行数
    word_count: usize,      // 単語数（スペース区切り）
    char_count: usize,      // 文字数（空白含む）
    char_count_no_ws: usize, // 文字数（空白除く）
    longest_line: String,    // 最長行
    shortest_line: String,   // 最短行（空行除く）
}

// Display トレイトを実装してフォーマット表示を可能にする
impl fmt::Display for TextStats {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        writeln!(f, "┌─────────────────────────────────────┐")?;
        writeln!(f, "│       📊 テキスト統計情報           │")?;
        writeln!(f, "├─────────────────────────────────────┤")?;
        writeln!(f, "│  行数           : {:>6}            │", self.line_count)?;
        writeln!(f, "│  単語数         : {:>6}            │", self.word_count)?;
        writeln!(f, "│  文字数(空白込) : {:>6}            │", self.char_count)?;
        writeln!(f, "│  文字数(空白除) : {:>6}            │", self.char_count_no_ws)?;
        writeln!(f, "├─────────────────────────────────────┤")?;
        writeln!(f, "│  最長行: {}",
            if self.longest_line.len() > 30 {
                format!("{}...", &self.longest_line[..30])
            } else {
                self.longest_line.clone()
            }
        )?;
        writeln!(f, "│  最短行: {}",
            if self.shortest_line.len() > 30 {
                format!("{}...", &self.shortest_line[..30])
            } else {
                self.shortest_line.clone()
            }
        )?;
        write!(f, "└─────────────────────────────────────┘")
    }
}

// ────────────────────────────────────────
//  エラー型の定義
// ────────────────────────────────────────
#[derive(Debug)]
enum TextError {
    EmptyInput,
    InvalidCommand(String),
}

// Display トレイトでエラーメッセージをカスタマイズ
impl fmt::Display for TextError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            TextError::EmptyInput => write!(f, "テキストが空です"),
            TextError::InvalidCommand(cmd) => {
                write!(f, "不明なコマンド: '{}'", cmd)
            }
        }
    }
}

// ────────────────────────────────────────
//  テキスト解析関数
//  Result型を返してエラーハンドリングを行う
// ────────────────────────────────────────
fn analyze_text(text: &str) -> Result<TextStats, TextError> {
    if text.trim().is_empty() {
        return Err(TextError::EmptyInput);
    }

    let lines: Vec<&str> = text.lines().collect();
    let line_count = lines.len();

    // 単語数: 各行を空白で分割してカウント
    let word_count: usize = lines
        .iter()
        .map(|line| line.split_whitespace().count())
        .sum();

    let char_count = text.chars().count();
    let char_count_no_ws = text.chars().filter(|c| !c.is_whitespace()).count();

    // 最長行を探す（max_by_key を使用）
    let longest_line = lines
        .iter()
        .max_by_key(|line| line.len())
        .unwrap_or(&"")
        .to_string();

    // 最短行を探す（空行を除外）
    let shortest_line = lines
        .iter()
        .filter(|line| !line.trim().is_empty())
        .min_by_key(|line| line.len())
        .unwrap_or(&"")
        .to_string();

    Ok(TextStats {
        line_count,
        word_count,
        char_count,
        char_count_no_ws,
        longest_line,
        shortest_line,
    })
}

// ────────────────────────────────────────
//  単語の出現頻度を集計（HashMap を活用）
// ────────────────────────────────────────
fn word_frequency(text: &str) -> HashMap<String, usize> {
    let mut freq: HashMap<String, usize> = HashMap::new();

    for word in text.split_whitespace() {
        // 句読点を除去して小文字化
        let cleaned: String = word
            .chars()
            .filter(|c| c.is_alphanumeric() || *c > '\u{3000}') // 日本語文字を保持
            .collect();

        if !cleaned.is_empty() {
            // entry API: キーが存在しなければ 0 を挿入し、参照を返す
            let count = freq.entry(cleaned).or_insert(0);
            *count += 1;
        }
    }

    freq
}

// ────────────────────────────────────────
//  テキスト変換関数群
// ────────────────────────────────────────

/// 各行に行番号を付与する
fn add_line_numbers(text: &str) -> String {
    text.lines()
        .enumerate()
        .map(|(i, line)| format!("{:>4} | {}", i + 1, line))
        .collect::<Vec<String>>()
        .join("\n")
}

/// 指定キーワードを含む行だけ抽出（grep風）
fn search_lines(text: &str, keyword: &str) -> Vec<String> {
    text.lines()
        .enumerate()
        .filter(|(_, line)| line.contains(keyword))
        .map(|(i, line)| format!("{:>4}: {}", i + 1, line))
        .collect()
}

/// テキストの文字列置換
fn replace_text(text: &str, from: &str, to: &str) -> String {
    text.replace(from, to)
}

/// テキストを逆順にする（行単位）
fn reverse_lines(text: &str) -> String {
    let mut lines: Vec<&str> = text.lines().collect();
    lines.reverse();
    lines.join("\n")
}

// ────────────────────────────────────────
//  コマンド処理（Result と ? 演算子の実践）
// ────────────────────────────────────────
fn process_command(text: &str, command: &str) -> Result<String, TextError> {
    let parts: Vec<&str> = command.splitn(2, ' ').collect();
    let cmd = parts[0];
    let arg = if parts.len() > 1 { parts[1] } else { "" };

    match cmd {
        "stats" => {
            // ? 演算子: Err ならそのまま返す、Ok なら中身を取り出す
            let stats = analyze_text(text)?;
            Ok(format!("{}", stats))
        }
        "lines" => {
            Ok(add_line_numbers(text))
        }
        "search" => {
            if arg.is_empty() {
                return Ok("使い方: search <キーワード>".to_string());
            }
            let results = search_lines(text, arg);
            if results.is_empty() {
                Ok(format!("'{}' に一致する行はありません。", arg))
            } else {
                Ok(format!(
                    "検索結果 ('{}': {}件):\n{}",
                    arg,
                    results.len(),
                    results.join("\n")
                ))
            }
        }
        "replace" => {
            let replace_parts: Vec<&str> = arg.splitn(2, ' ').collect();
            if replace_parts.len() < 2 {
                return Ok("使い方: replace <置換前> <置換後>".to_string());
            }
            let result = replace_text(text, replace_parts[0], replace_parts[1]);
            Ok(format!("置換結果:\n{}", result))
        }
        "reverse" => {
            Ok(format!("逆順:\n{}", reverse_lines(text)))
        }
        "freq" => {
            let freq = word_frequency(text);
            let mut sorted: Vec<_> = freq.iter().collect();
            sorted.sort_by(|a, b| b.1.cmp(a.1)); // 出現回数で降順ソート

            let mut output = String::from("単語出現頻度（上位10件）:\n");
            for (word, count) in sorted.iter().take(10) {
                output.push_str(&format!("  {:>4}回 : {}\n", count, word));
            }
            Ok(output)
        }
        _ => Err(TextError::InvalidCommand(cmd.to_string())),
    }
}

// ────────────────────────────────────────
//  入力補助
// ────────────────────────────────────────
fn read_input(prompt: &str) -> String {
    print!("{}", prompt);
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).unwrap();
    input.trim().to_string()
}

// ────────────────────────────────────────
//  メイン関数
// ────────────────────────────────────────
fn main() {
    println!("╔══════════════════════════════════════╗");
    println!("║  📝 ファイル風テキスト処理ツール     ║");
    println!("╚══════════════════════════════════════╝");
    println!();

    // サンプルテキスト
    let sample_text = "\
Rustは安全性、速度、並行性に焦点を当てたシステムプログラミング言語です。
メモリ安全性をガベージコレクタなしで実現する点が大きな特徴です。
所有権システムにより、コンパイル時にメモリの問題を検出できます。

Rustの主な特徴：
  - ゼロコスト抽象化
  - ムーブセマンティクス
  - 保証されたメモリ安全性
  - スレッド安全性
  - トレイトベースのジェネリクス
  - パターンマッチング
  - 型推論
  - 効率的なC言語バインディング

Rustは2015年に バージョン1.0がリリースされました。
Stack Overflowの調査で「最も愛されている言語」に選ばれ続けています。
Rustはシステムプログラミングの世界に新しい風を吹き込んでいます。";

    println!("--- サンプルテキストを読み込みました ---\n");
    println!("{}\n", add_line_numbers(sample_text));

    println!("コマンド一覧:");
    println!("  stats           - テキストの統計情報を表示");
    println!("  lines           - 行番号付きで表示");
    println!("  search <語句>   - キーワード検索");
    println!("  replace <前> <後> - 文字列置換");
    println!("  reverse         - 行を逆順に表示");
    println!("  freq            - 単語出現頻度");
    println!("  quit            - 終了");
    println!();

    loop {
        let command = read_input("command > ");

        if command == "quit" || command == "q" {
            break;
        }

        // Result型のハンドリング
        match process_command(sample_text, &command) {
            Ok(result) => println!("\n{}\n", result),
            Err(e) => println!("\n⚠️  エラー: {}\n", e),
        }
    }

    println!("\nプログラムを終了します。お疲れさまでした！");
}
