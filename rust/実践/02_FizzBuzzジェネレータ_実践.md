# 実践課題02：FizzBuzzジェネレータ ★1

> **難易度**: ★☆☆☆☆（入門）
> **前提知識**: 第2章（条件分岐）、第3章（ループとイテレータ）
> **課題の種類**: ミニプロジェクト
> **学習目標**: 条件分岐とループを組み合わせて、定番の論理問題を正しく実装する力を養う

---

## 完成イメージ

```
===== FizzBuzz ジェネレータ =====
開始数を入力してください: 1
終了数を入力してください: 20

--- 結果 ---
1
2
Fizz
4
Buzz
Fizz
7
8
Fizz
Buzz
11
Fizz
13
14
FizzBuzz
16
17
Fizz
19
Buzz

--- 統計 ---
数値の個数: 8
Fizz の個数: 4
Buzz の個数: 2
FizzBuzz の個数: 1
```

---

## 課題の要件

1. ユーザーから開始数と終了数を入力で受け取る
2. 各数値について以下のルールで出力する：
   - 3と5の両方で割り切れる → `FizzBuzz`
   - 3で割り切れる → `Fizz`
   - 5で割り切れる → `Buzz`
   - それ以外 → その数値
3. 処理後に統計情報（各カテゴリの個数）を表示する
4. 開始数が終了数より大きい場合はエラーメッセージを表示する

---

## ステップガイド

<details>
<summary>ステップ1：入力を受け取る</summary>

前の課題と同様に `std::io::stdin()` で入力を受け取り、`i32` に変換します。

```rust
use std::io;
use std::io::Write;

fn main() {
    print!("開始数を入力してください: ");
    io::stdout().flush().unwrap();

    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("入力エラー");
    let start: i32 = input.trim().parse().expect("整数を入力してください");
}
```

</details>

<details>
<summary>ステップ2：FizzBuzzの条件分岐を書く</summary>

**重要**: 「3と5の両方で割り切れる」判定を**最初に**書く必要があります。順序を間違えると `15` が `Fizz` になってしまいます。

```rust
for n in start..=end {
    if n % 15 == 0 {
        println!("FizzBuzz");
    } else if n % 3 == 0 {
        println!("Fizz");
    } else if n % 5 == 0 {
        println!("Buzz");
    } else {
        println!("{}", n);
    }
}
```

</details>

<details>
<summary>ステップ3：統計情報を集計する</summary>

ループの中でカウンタ変数をインクリメントします。`mut` キーワードで可変にすることを忘れずに。

```rust
let mut fizz_count = 0;
let mut buzz_count = 0;
let mut fizzbuzz_count = 0;
let mut number_count = 0;

for n in start..=end {
    if n % 15 == 0 {
        fizzbuzz_count += 1;
        // ...
    }
}
```

</details>

---

## 解答例

<details>
<summary>解答例（初心者向け）</summary>

```rust
// FizzBuzzジェネレータ
// 学べる内容：条件分岐、ループ、剰余演算、カウンタ変数
// 実行方法：rustc main.rs && ./main

use std::io;
use std::io::Write;

fn main() {
    println!("===== FizzBuzz ジェネレータ =====");

    // --- 入力 ---
    print!("開始数を入力してください: ");
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("入力エラー");
    let start: i32 = input.trim().parse().expect("整数を入力してください");

    print!("終了数を入力してください: ");
    io::stdout().flush().unwrap();
    let mut input2 = String::new();
    io::stdin().read_line(&mut input2).expect("入力エラー");
    let end: i32 = input2.trim().parse().expect("整数を入力してください");

    // --- バリデーション ---
    if start > end {
        println!("エラー: 開始数は終了数以下にしてください。");
        return;
    }

    // --- FizzBuzz処理 ---
    println!("\n--- 結果 ---");

    let mut fizz_count = 0;
    let mut buzz_count = 0;
    let mut fizzbuzz_count = 0;
    let mut number_count = 0;

    for n in start..=end {
        if n % 15 == 0 {
            println!("FizzBuzz");
            fizzbuzz_count += 1;
        } else if n % 3 == 0 {
            println!("Fizz");
            fizz_count += 1;
        } else if n % 5 == 0 {
            println!("Buzz");
            buzz_count += 1;
        } else {
            println!("{}", n);
            number_count += 1;
        }
    }

    // --- 統計表示 ---
    println!("\n--- 統計 ---");
    println!("数値の個数: {}", number_count);
    println!("Fizz の個数: {}", fizz_count);
    println!("Buzz の個数: {}", buzz_count);
    println!("FizzBuzz の個数: {}", fizzbuzz_count);
}
```

</details>

<details>
<summary>解答例（改良版 ─ イテレータとmatchを活用）</summary>

第3章のイテレータと `match` 式を活用したバージョンです。

```rust
// FizzBuzzジェネレータ（改良版）
// イテレータとmatch式を活用したバージョン
// 実行方法：rustc main.rs && ./main

use std::io;
use std::io::Write;

/// FizzBuzz判定結果を表す列挙型
enum FizzBuzzResult {
    FizzBuzz,
    Fizz,
    Buzz,
    Number(i32),
}

/// 数値をFizzBuzz判定します
fn classify(n: i32) -> FizzBuzzResult {
    match (n % 3, n % 5) {
        (0, 0) => FizzBuzzResult::FizzBuzz,
        (0, _) => FizzBuzzResult::Fizz,
        (_, 0) => FizzBuzzResult::Buzz,
        _      => FizzBuzzResult::Number(n),
    }
}

/// プロンプトを表示して整数を読み取ります
fn read_i32(prompt_msg: &str) -> i32 {
    print!("{}", prompt_msg);
    io::stdout().flush().unwrap();
    let mut input = String::new();
    io::stdin().read_line(&mut input).expect("入力エラー");
    input.trim().parse().expect("整数を入力してください")
}

fn main() {
    println!("===== FizzBuzz ジェネレータ =====");

    let start = read_i32("開始数を入力してください: ");
    let end = read_i32("終了数を入力してください: ");

    if start > end {
        println!("エラー: 開始数は終了数以下にしてください。");
        return;
    }

    // 全結果を収集
    let results: Vec<FizzBuzzResult> = (start..=end).map(classify).collect();

    // 結果表示
    println!("\n--- 結果 ---");
    for result in &results {
        match result {
            FizzBuzzResult::FizzBuzz   => println!("FizzBuzz"),
            FizzBuzzResult::Fizz       => println!("Fizz"),
            FizzBuzzResult::Buzz       => println!("Buzz"),
            FizzBuzzResult::Number(n)  => println!("{}", n),
        }
    }

    // 統計をイテレータで集計
    let number_count = results.iter().filter(|r| matches!(r, FizzBuzzResult::Number(_))).count();
    let fizz_count = results.iter().filter(|r| matches!(r, FizzBuzzResult::Fizz)).count();
    let buzz_count = results.iter().filter(|r| matches!(r, FizzBuzzResult::Buzz)).count();
    let fizzbuzz_count = results.iter().filter(|r| matches!(r, FizzBuzzResult::FizzBuzz)).count();

    println!("\n--- 統計 ---");
    println!("数値の個数: {}", number_count);
    println!("Fizz の個数: {}", fizz_count);
    println!("Buzz の個数: {}", buzz_count);
    println!("FizzBuzz の個数: {}", fizzbuzz_count);
}
```

**初心者向けとの違い:**
- `FizzBuzzResult` 列挙型（enum）で判定結果を型安全に表現
- `match (n % 3, n % 5)` のタプルパターンで条件を簡潔に記述
- `classify()` 関数に判定ロジックを分離 → テスト可能
- `(start..=end).map(classify).collect()` でイテレータチェーンを活用
- `matches!` マクロで統計集計をシンプルに記述

</details>
