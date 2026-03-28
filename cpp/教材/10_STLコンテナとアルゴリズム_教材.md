# 第10章：STLコンテナとアルゴリズム
> **この章のゴール**: C++のSTL（Standard Template Library）を使いこなし、効率的なデータ管理とアルゴリズム適用ができるようになる。

---

## 1. STLの概要

STL（Standard Template Library）は、C++標準ライブラリの中核をなすテンプレートベースの汎用ライブラリです。データ構造とアルゴリズムを型に依存しない形で提供します。

### STLの3つの構成要素

```
┌─────────────────────────────────────────────────┐
│                    STL                           │
│                                                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────────┐  │
│  │コンテナ   │←→│イテレータ │←→│アルゴリズム   │  │
│  │Container │  │Iterator  │  │Algorithm     │  │
│  │          │  │          │  │              │  │
│  │データを   │  │コンテナと │  │データを      │  │
│  │格納する   │  │アルゴリズム│  │操作する      │  │
│  │          │  │を繋ぐ    │  │              │  │
│  └──────────┘  └──────────┘  └──────────────┘  │
└─────────────────────────────────────────────────┘
```

- **コンテナ（Container）**: データを格納するデータ構造（`vector`, `map` など）
- **イテレータ（Iterator）**: コンテナの要素を順にたどるためのオブジェクト
- **アルゴリズム（Algorithm）**: ソート・検索などの汎用的な操作（`sort`, `find` など）

イテレータがコンテナとアルゴリズムの橋渡しをすることで、任意のコンテナに任意のアルゴリズムを適用できる設計になっています。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    // コンテナにデータを格納
    std::vector<int> nums = {5, 2, 8, 1, 9};

    // アルゴリズムをイテレータ経由で適用
    std::sort(nums.begin(), nums.end());

    for (int n : nums) {
        std::cout << n << " ";  // 1 2 5 8 9
    }
    std::cout << std::endl;
    return 0;
}
```

### ポイントまとめ
- STLは「コンテナ」「イテレータ」「アルゴリズム」の3要素で構成される
- イテレータがコンテナとアルゴリズムを分離し、組み合わせの自由度を高めている
- `#include` で必要なヘッダをインクルードして使用する

---

## 2. イテレータ（Iterator）

イテレータは、コンテナの要素を指し示す「汎用ポインタ」のような存在です。

### begin() と end()

```
  begin()                              end()
    ↓                                    ↓
  [ 10 | 20 | 30 | 40 | 50 ]          (番兵：要素の1つ先)
    ^                          ^
    最初の要素                  最後の要素の次
```

`end()` は最後の要素の**次**を指すことに注意してください。これは半開区間 `[begin, end)` という設計です。

### 基本的な使い方

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};

    // 従来のイテレータ
    for (std::vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;

    // auto を使った簡潔な書き方（C++11以降、推奨）
    for (auto it = v.begin(); it != v.end(); ++it) {
        std::cout << *it << " ";
    }
    std::cout << std::endl;

    // 範囲ベースfor文（最も簡潔）
    for (const auto& elem : v) {
        std::cout << elem << " ";
    }
    std::cout << std::endl;

    return 0;
}
```

### イテレータのカテゴリ

```
入力イテレータ ──→ 前方イテレータ ──→ 双方向イテレータ ──→ ランダムアクセスイテレータ
(InputIterator)   (ForwardIterator)  (BidirectionalIterator) (RandomAccessIterator)
  読み取り専用       前方に進める        前後に進める           任意の位置にジャンプ
  1回のみ走査       複数回走査可         --it が可能           it + n, it[n] が可能

コンテナとの対応:
  forward_list → 前方イテレータ
  list, map, set → 双方向イテレータ
  vector, deque, array → ランダムアクセスイテレータ
```

### ポイントまとめ
- `begin()` は先頭、`end()` は末尾の次を指す（半開区間）
- `auto` を使うとイテレータの型を省略できる
- コンテナごとにサポートするイテレータのカテゴリが異なる

---

## 3. シーケンスコンテナ（Sequence Container）

要素を順序付きで格納するコンテナです。

### std::vector - 動的配列

最も使用頻度の高いコンテナです。末尾への追加・削除が高速で、ランダムアクセスも O(1) です。

```cpp
#include <iostream>
#include <vector>

int main() {
    std::vector<int> v;

    // 要素の追加
    v.push_back(10);
    v.push_back(20);
    v.push_back(30);

    // インデックスでアクセス
    std::cout << "先頭: " << v[0] << std::endl;       // 10
    std::cout << "安全なアクセス: " << v.at(1) << std::endl; // 20（範囲外で例外）

    // サイズと容量
    std::cout << "要素数: " << v.size() << std::endl;      // 3
    std::cout << "容量: " << v.capacity() << std::endl;

    // 初期化リスト
    std::vector<std::string> fruits = {"apple", "banana", "cherry"};

    // 末尾の削除
    fruits.pop_back();
    std::cout << "要素数: " << fruits.size() << std::endl;  // 2

    return 0;
}
```

### std::array - 固定長配列（C++11）

コンパイル時にサイズが確定する配列です。Cスタイル配列の安全な代替として使います。

```cpp
#include <iostream>
#include <array>

int main() {
    std::array<int, 5> arr = {1, 2, 3, 4, 5};

    std::cout << "サイズ: " << arr.size() << std::endl;  // 5
    std::cout << "先頭: " << arr.front() << std::endl;   // 1
    std::cout << "末尾: " << arr.back() << std::endl;    // 5

    // 範囲外アクセスの検出
    // arr.at(10);  // std::out_of_range 例外が発生

    return 0;
}
```

### std::list - 双方向連結リスト

任意の位置への挿入・削除が O(1) ですが、ランダムアクセスはできません。

```cpp
#include <iostream>
#include <list>

int main() {
    std::list<int> lst = {10, 20, 30};

    lst.push_front(5);   // 先頭に追加
    lst.push_back(40);   // 末尾に追加

    // イテレータを使った中間挿入
    auto it = lst.begin();
    std::advance(it, 2);   // 2つ進める
    lst.insert(it, 15);    // その位置に挿入

    for (const auto& val : lst) {
        std::cout << val << " ";  // 5 10 15 20 30 40
    }
    std::cout << std::endl;

    return 0;
}
```

### std::deque - 両端キュー

先頭・末尾の両方に高速な追加・削除ができます。

```cpp
#include <iostream>
#include <deque>

int main() {
    std::deque<int> dq = {10, 20, 30};

    dq.push_front(5);    // 先頭に追加
    dq.push_back(40);    // 末尾に追加

    std::cout << dq.front() << std::endl;  // 5
    std::cout << dq.back() << std::endl;   // 40
    std::cout << dq[2] << std::endl;       // 20（ランダムアクセス可能）

    return 0;
}
```

### シーケンスコンテナの使い分け

```
用途                        → 推奨コンテナ
─────────────────────────────────────────
汎用・迷ったらこれ            → vector
サイズ固定                   → array
先頭・末尾の両方で追加/削除    → deque
中間の挿入/削除が頻繁         → list
```

### ポイントまとめ
- 迷ったら `vector` を使う（最も高速でキャッシュ効率が良い）
- `array` はサイズ固定の場面でCスタイル配列の代わりに使う
- `list` は中間挿入が多い場面で有効だが、ランダムアクセスは不可

---

## 4. 連想コンテナ（Associative Container）

キーを使って要素を高速に検索できるコンテナです。

### std::map - 順序付きキーバリューストア

キーが自動的にソートされます。内部実装は赤黒木で、検索は O(log n) です。

```cpp
#include <iostream>
#include <map>
#include <string>

int main() {
    std::map<std::string, int> scores;

    // 要素の追加
    scores["Alice"] = 90;
    scores["Bob"] = 85;
    scores["Charlie"] = 92;
    scores.insert({"Diana", 88});

    // 検索
    if (scores.find("Bob") != scores.end()) {
        std::cout << "Bob: " << scores["Bob"] << std::endl;  // 85
    }

    // count で存在確認
    if (scores.count("Eve") == 0) {
        std::cout << "Eve は見つかりません" << std::endl;
    }

    // 全要素の列挙（キー順にソート済み）
    for (const auto& [name, score] : scores) {  // C++17 構造化束縛
        std::cout << name << ": " << score << std::endl;
    }

    return 0;
}
```

### std::set - 順序付き集合

重複しない要素の集合を管理します。

```cpp
#include <iostream>
#include <set>

int main() {
    std::set<int> s = {3, 1, 4, 1, 5, 9, 2, 6, 5};

    // 重複は自動的に除去される
    std::cout << "要素数: " << s.size() << std::endl;  // 7

    for (int val : s) {
        std::cout << val << " ";  // 1 2 3 4 5 6 9（ソート済み）
    }
    std::cout << std::endl;

    // 要素の検索
    if (s.count(4)) {
        std::cout << "4 は存在します" << std::endl;
    }

    return 0;
}
```

### std::unordered_map / std::unordered_set

ハッシュテーブルによる実装で、平均 O(1) の検索が可能です。順序は保証されません。

```cpp
#include <iostream>
#include <unordered_map>
#include <string>

int main() {
    std::unordered_map<std::string, int> word_count;

    std::string words[] = {"apple", "banana", "apple", "cherry", "banana", "apple"};
    for (const auto& w : words) {
        word_count[w]++;  // 存在しないキーは自動で0初期化される
    }

    for (const auto& [word, count] : word_count) {
        std::cout << word << ": " << count << std::endl;
    }
    // 順序は不定（例: cherry: 1, banana: 2, apple: 3）

    return 0;
}
```

### 連想コンテナの使い分け

```
用途                         → 推奨コンテナ
──────────────────────────────────────────────
キー順にソートが必要           → map / set
最速の検索（順序不要）         → unordered_map / unordered_set
キーの重複を許容              → multimap / multiset
```

### ポイントまとめ
- `map`/`set` はキー順にソートされ、検索は O(log n)
- `unordered_map`/`unordered_set` はハッシュベースで平均 O(1)
- 順序が不要なら `unordered_` 系の方が高速

---

## 5. コンテナアダプタ（Container Adaptor）

既存のコンテナをラップして、特定のインターフェースだけを公開するものです。

### std::stack - LIFO（後入れ先出し）

```cpp
#include <iostream>
#include <stack>

int main() {
    std::stack<int> st;

    st.push(10);
    st.push(20);
    st.push(30);

    std::cout << "先頭: " << st.top() << std::endl;  // 30

    while (!st.empty()) {
        std::cout << st.top() << " ";  // 30 20 10
        st.pop();
    }
    std::cout << std::endl;

    return 0;
}
```

### std::queue - FIFO（先入れ先出し）

```cpp
#include <iostream>
#include <queue>
#include <string>

int main() {
    std::queue<std::string> q;

    q.push("タスクA");
    q.push("タスクB");
    q.push("タスクC");

    while (!q.empty()) {
        std::cout << "処理中: " << q.front() << std::endl;
        q.pop();
    }
    // 出力: タスクA → タスクB → タスクC の順

    return 0;
}
```

### std::priority_queue - 優先度付きキュー

デフォルトでは最大値が先頭に来ます。

```cpp
#include <iostream>
#include <queue>
#include <vector>

int main() {
    // デフォルト: 最大ヒープ
    std::priority_queue<int> max_pq;
    max_pq.push(30);
    max_pq.push(10);
    max_pq.push(50);
    max_pq.push(20);

    std::cout << "最大値から取り出し: ";
    while (!max_pq.empty()) {
        std::cout << max_pq.top() << " ";  // 50 30 20 10
        max_pq.pop();
    }
    std::cout << std::endl;

    // 最小ヒープ
    std::priority_queue<int, std::vector<int>, std::greater<int>> min_pq;
    min_pq.push(30);
    min_pq.push(10);
    min_pq.push(50);

    std::cout << "最小値: " << min_pq.top() << std::endl;  // 10

    return 0;
}
```

### ポイントまとめ
- `stack` はLIFO、`queue` はFIFO
- `priority_queue` はデフォルトで最大値が優先される
- 最小ヒープにするには `std::greater<>` を第3テンプレート引数に渡す

---

## 6. STLアルゴリズム

`<algorithm>` と `<numeric>` ヘッダに多数の汎用アルゴリズムが用意されています。

### std::sort - ソート

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {5, 2, 8, 1, 9, 3};

    // 昇順ソート
    std::sort(v.begin(), v.end());
    // v: {1, 2, 3, 5, 8, 9}

    // 降順ソート
    std::sort(v.begin(), v.end(), std::greater<int>());
    // v: {9, 8, 5, 3, 2, 1}

    for (int n : v) std::cout << n << " ";
    std::cout << std::endl;

    return 0;
}
```

### std::find - 検索

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {10, 20, 30, 40, 50};

    auto it = std::find(v.begin(), v.end(), 30);
    if (it != v.end()) {
        std::cout << "見つかりました: " << *it << std::endl;
        std::cout << "インデックス: " << std::distance(v.begin(), it) << std::endl;
    }

    return 0;
}
```

### std::transform - 要素の変換

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> src = {1, 2, 3, 4, 5};
    std::vector<int> dst(src.size());

    // 各要素を2倍にして dst に格納
    std::transform(src.begin(), src.end(), dst.begin(),
                   [](int x) { return x * 2; });

    for (int n : dst) std::cout << n << " ";  // 2 4 6 8 10
    std::cout << std::endl;

    return 0;
}
```

### std::accumulate - 集計

```cpp
#include <iostream>
#include <vector>
#include <numeric>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};

    int sum = std::accumulate(v.begin(), v.end(), 0);
    std::cout << "合計: " << sum << std::endl;  // 15

    // カスタム演算（積の計算）
    int product = std::accumulate(v.begin(), v.end(), 1,
                                  [](int a, int b) { return a * b; });
    std::cout << "積: " << product << std::endl;  // 120

    return 0;
}
```

### std::for_each - 各要素に処理を適用

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5};

    std::for_each(v.begin(), v.end(), [](int& x) {
        x *= 10;  // 各要素を10倍に変更
    });

    for (int n : v) std::cout << n << " ";  // 10 20 30 40 50
    std::cout << std::endl;

    return 0;
}
```

### std::count_if - 条件を満たす要素数

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    int even_count = std::count_if(v.begin(), v.end(),
                                    [](int x) { return x % 2 == 0; });
    std::cout << "偶数の数: " << even_count << std::endl;  // 5

    return 0;
}
```

### erase-remove イディオム

`std::remove_if` は要素を実際には削除せず、残す要素を前に詰めるだけです。実際の削除には `erase` と組み合わせます。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>

int main() {
    std::vector<int> v = {1, 2, 3, 4, 5, 6, 7, 8, 9, 10};

    // 奇数を削除（erase-remove イディオム）
    v.erase(
        std::remove_if(v.begin(), v.end(), [](int x) { return x % 2 != 0; }),
        v.end()
    );

    for (int n : v) std::cout << n << " ";  // 2 4 6 8 10
    std::cout << std::endl;

    // C++20 以降は std::erase_if が使える
    // std::erase_if(v, [](int x) { return x > 6; });

    return 0;
}
```

### ポイントまとめ
- `sort` は平均 O(n log n) の高速ソート
- `find` は線形探索、ソート済みなら `lower_bound` を使うと O(log n)
- `accumulate` は `<numeric>` ヘッダに定義されている（`<algorithm>` ではない）
- erase-remove イディオムは `vector` から条件付き削除する定番パターン

---

## 7. ラムダ式とアルゴリズムの組み合わせ

ラムダ式（Lambda Expression）を使うと、アルゴリズムに渡す処理をその場で簡潔に記述できます。

### ラムダ式の構文

```
[キャプチャ](引数) -> 戻り値型 { 本体 }

例: [](int x) -> bool { return x > 0; }
    [&total](int x) { total += x; }       // total を参照キャプチャ
    [=](int x) { return x + offset; }     // 全変数を値キャプチャ
```

### 実践例：学生データの処理

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
#include <numeric>
#include <string>

struct Student {
    std::string name;
    int score;
};

int main() {
    std::vector<Student> students = {
        {"Alice", 85}, {"Bob", 92}, {"Charlie", 78},
        {"Diana", 95}, {"Eve", 88}
    };

    // 1. スコア順にソート（降順）
    std::sort(students.begin(), students.end(),
              [](const Student& a, const Student& b) {
                  return a.score > b.score;
              });

    std::cout << "=== 成績ランキング ===" << std::endl;
    for (const auto& s : students) {
        std::cout << s.name << ": " << s.score << std::endl;
    }

    // 2. 90点以上の人数
    int high_scorers = std::count_if(students.begin(), students.end(),
                                      [](const Student& s) { return s.score >= 90; });
    std::cout << "90点以上: " << high_scorers << "人" << std::endl;

    // 3. 平均点の計算
    int total = std::accumulate(students.begin(), students.end(), 0,
                                 [](int sum, const Student& s) { return sum + s.score; });
    double avg = static_cast<double>(total) / students.size();
    std::cout << "平均点: " << avg << std::endl;

    // 4. 名前の一覧を抽出
    std::vector<std::string> names(students.size());
    std::transform(students.begin(), students.end(), names.begin(),
                   [](const Student& s) { return s.name; });

    std::cout << "名前一覧: ";
    for (const auto& name : names) {
        std::cout << name << " ";
    }
    std::cout << std::endl;

    // 5. 条件に合う最初の要素を検索
    auto it = std::find_if(students.begin(), students.end(),
                            [](const Student& s) { return s.name == "Bob"; });
    if (it != students.end()) {
        std::cout << "Bob のスコア: " << it->score << std::endl;
    }

    return 0;
}
```

### ポイントまとめ
- ラムダ式はSTLアルゴリズムとの組み合わせで真価を発揮する
- `[&]` で外部変数を参照キャプチャ、`[=]` で値キャプチャ
- 構造体のソートやフィルタリングなど、実務で頻繁に使うパターンを覚えておく

---

## 8. よくある間違い

### 間違い1：無効なイテレータの使用

`vector` に要素を追加・削除すると、既存のイテレータが無効化されることがあります。

```cpp
// NG: push_back でイテレータが無効化される可能性
std::vector<int> v = {1, 2, 3};
auto it = v.begin();
v.push_back(4);     // メモリ再確保が起きるとイテレータ無効化
// *it;             // 未定義動作！

// OK: push_back 後にイテレータを取り直す
v.push_back(5);
it = v.begin();     // 再取得
```

### 間違い2：map の [] 演算子で意図しない要素が作られる

```cpp
std::map<std::string, int> m;
// NG: 存在しないキーに [] でアクセスすると要素が作られる
if (m["key"] == 0) {  // "key" が勝手に挿入されてしまう！
    // ...
}

// OK: find または count で存在確認
if (m.find("key") == m.end()) {
    std::cout << "キーが存在しません" << std::endl;
}
```

### 間違い3：erase-remove イディオムを忘れる

```cpp
std::vector<int> v = {1, 2, 3, 4, 5};

// NG: remove だけでは要素は消えない
std::remove_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
// v.size() は変わらない！

// OK: erase と組み合わせる
v.erase(
    std::remove_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; }),
    v.end()
);
```

### 間違い4：ソートされていないコンテナに二分探索

```cpp
std::vector<int> v = {5, 3, 1, 4, 2};

// NG: ソートされていないのに binary_search を使う
// bool found = std::binary_search(v.begin(), v.end(), 3);  // 結果は不定

// OK: 先にソートする
std::sort(v.begin(), v.end());
bool found = std::binary_search(v.begin(), v.end(), 3);  // true
```

---

## 9. 章末まとめ

この章で学んだ内容を整理します。

### コンテナの分類

```
STLコンテナ
├── シーケンスコンテナ
│   ├── vector     … 動的配列（最も汎用的）
│   ├── array      … 固定長配列
│   ├── deque      … 両端キュー
│   └── list       … 双方向連結リスト
├── 連想コンテナ
│   ├── map / set           … 順序付き（赤黒木）
│   └── unordered_map / set … ハッシュベース
└── コンテナアダプタ
    ├── stack          … LIFO
    ├── queue          … FIFO
    └── priority_queue … 優先度付きキュー
```

### 主要アルゴリズム一覧

| アルゴリズム | ヘッダ | 用途 |
|---|---|---|
| `sort` | `<algorithm>` | ソート |
| `find` / `find_if` | `<algorithm>` | 線形検索 |
| `binary_search` | `<algorithm>` | 二分探索（要ソート済み） |
| `count` / `count_if` | `<algorithm>` | 条件を満たす要素数 |
| `transform` | `<algorithm>` | 要素の変換 |
| `for_each` | `<algorithm>` | 各要素に処理を適用 |
| `remove_if` | `<algorithm>` | 条件付き削除（eraseと併用） |
| `accumulate` | `<numeric>` | 集計 |

### 重要な原則
1. **迷ったら `vector`** を使う。メモリ局所性が良く、ほとんどの用途で最速
2. **キーで検索するなら `unordered_map`**。順序が必要なときだけ `map` を使う
3. **ラムダ式を積極的に使う**。STLアルゴリズムと組み合わせて宣言的なコードを書く
4. **イテレータの無効化に注意**。コンテナを変更した後は既存のイテレータを使わない
5. **erase-remove イディオム**は `vector` の要素削除の定番パターン
