# ==============================
# データ構造体験プログラム
# 基本情報技術者：データ構造とアルゴリズム
# ==============================
# 学べる内容:
#   - スタック（stack）: LIFO（Last In, First Out）
#   - キュー（queue）: FIFO（First In, First Out）
#   - 連結リスト（linked list）: ノードの連鎖
#   - 二分探索木（binary search tree）: 探索・挿入・削除
#   - 各データ構造の計算量（オーダー記法）
#   - 基本情報技術者試験のデータ構造問題への対応力
#
# 実行方法:
#   python 03_データ構造体験.py
# ==============================


# ============================================================
# 1. スタック（Stack）
# ============================================================

class Stack:
    """スタック: 後入れ先出し（LIFO）のデータ構造です

    イメージ: 積み上げた本 → 一番上からしか取れません
    """

    def __init__(self, max_size=10):
        self.data = []
        self.max_size = max_size

    def push(self, item):
        """データをスタックの一番上に積みます"""
        if self.is_full():
            print(f"    ※ スタックオーバーフロー! (最大{self.max_size}個)")
            return False
        self.data.append(item)
        return True

    def pop(self):
        """スタックの一番上からデータを取り出します"""
        if self.is_empty():
            print("    ※ スタックアンダーフロー! (空です)")
            return None
        return self.data.pop()

    def peek(self):
        """一番上のデータを覗きます（取り出しません）"""
        if self.is_empty():
            return None
        return self.data[-1]

    def is_empty(self):
        return len(self.data) == 0

    def is_full(self):
        return len(self.data) >= self.max_size

    def size(self):
        return len(self.data)

    def display(self):
        """スタックの中身を視覚的に表示します"""
        if self.is_empty():
            print("    (空)")
            return
        print("    ┌─────────┐")
        for i in range(len(self.data) - 1, -1, -1):
            marker = " ← top" if i == len(self.data) - 1 else ""
            print(f"    │ {str(self.data[i]):>7} │{marker}")
        print("    └─────────┘")


# ============================================================
# 2. キュー（Queue）
# ============================================================

class Queue:
    """キュー: 先入れ先出し（FIFO）のデータ構造です

    イメージ: レジの行列 → 先に並んだ人から順番に処理されます
    """

    def __init__(self, max_size=10):
        self.data = []
        self.max_size = max_size

    def enqueue(self, item):
        """データをキューの末尾に追加します"""
        if self.is_full():
            print(f"    ※ キューが満杯です! (最大{self.max_size}個)")
            return False
        self.data.append(item)
        return True

    def dequeue(self):
        """キューの先頭からデータを取り出します"""
        if self.is_empty():
            print("    ※ キューが空です!")
            return None
        return self.data.pop(0)

    def front(self):
        """先頭のデータを覗きます（取り出しません）"""
        if self.is_empty():
            return None
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

    def is_full(self):
        return len(self.data) >= self.max_size

    def size(self):
        return len(self.data)

    def display(self):
        """キューの中身を視覚的に表示します"""
        if self.is_empty():
            print("    (空)")
            return
        items = " → ".join(str(x) for x in self.data)
        print(f"    先頭 [ {items} ] 末尾")


# ============================================================
# 3. 連結リスト（Linked List）
# ============================================================

class Node:
    """連結リストのノード（節点）です"""

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    """単方向連結リスト: ノードがポインタで繋がったデータ構造です

    イメージ: しりとり → 各単語が次の単語を指しています
    """

    def __init__(self):
        self.head = None
        self.length = 0

    def append(self, data):
        """末尾にノードを追加します"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.length += 1

    def insert(self, index, data):
        """指定位置にノードを挿入します"""
        if index < 0 or index > self.length:
            print(f"    ※ インデックス {index} は範囲外です (0〜{self.length})")
            return False
        new_node = Node(data)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            current = self.head
            for _ in range(index - 1):
                current = current.next
            new_node.next = current.next
            current.next = new_node
        self.length += 1
        return True

    def delete(self, data):
        """指定データのノードを削除します"""
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self.length -= 1
            return True
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                self.length -= 1
                return True
            current = current.next
        return False

    def search(self, data):
        """データを検索します（見つかった位置を返します）"""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def display(self):
        """連結リストを視覚的に表示します"""
        if self.head is None:
            print("    (空)")
            return
        current = self.head
        parts = []
        while current:
            parts.append(f"[{current.data}]")
            current = current.next
        print("    " + " → ".join(parts) + " → None")


# ============================================================
# 4. 二分探索木（Binary Search Tree）
# ============================================================

class BSTNode:
    """二分探索木のノードです"""

    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    """二分探索木: 左 < 親 < 右 の規則で整列されるデータ構造です

    特徴: 探索・挿入・削除が平均 O(log n) で高速です
    """

    def __init__(self):
        self.root = None

    def insert(self, data):
        """データを挿入します"""
        if self.root is None:
            self.root = BSTNode(data)
            return
        self._insert_recursive(self.root, data)

    def _insert_recursive(self, node, data):
        if data < node.data:
            if node.left is None:
                node.left = BSTNode(data)
            else:
                self._insert_recursive(node.left, data)
        elif data > node.data:
            if node.right is None:
                node.right = BSTNode(data)
            else:
                self._insert_recursive(node.right, data)
        # data == node.data の場合は重複として無視します

    def search(self, data):
        """データを探索します（探索過程を表示します）"""
        print(f"    探索: {data}")
        return self._search_recursive(self.root, data, 1)

    def _search_recursive(self, node, data, step):
        if node is None:
            print(f"      ステップ{step}: 見つかりませんでした")
            return False
        if data == node.data:
            print(f"      ステップ{step}: {node.data} → 発見!")
            return True
        elif data < node.data:
            print(f"      ステップ{step}: {node.data} → 左へ ({data} < {node.data})")
            return self._search_recursive(node.left, data, step + 1)
        else:
            print(f"      ステップ{step}: {node.data} → 右へ ({data} > {node.data})")
            return self._search_recursive(node.right, data, step + 1)

    def inorder(self):
        """中間順走査（inorder traversal）: 昇順にデータを取得します"""
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, node, result):
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)

    def preorder(self):
        """前順走査（preorder traversal）"""
        result = []
        self._preorder_recursive(self.root, result)
        return result

    def _preorder_recursive(self, node, result):
        if node:
            result.append(node.data)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder(self):
        """後順走査（postorder traversal）"""
        result = []
        self._postorder_recursive(self.root, result)
        return result

    def _postorder_recursive(self, node, result):
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.data)

    def display(self):
        """二分探索木をアスキーアートで表示します"""
        if self.root is None:
            print("    (空)")
            return
        lines = []
        self._build_display(self.root, "", True, lines)
        for line in lines:
            print("    " + line)

    def _build_display(self, node, prefix, is_last, lines):
        if node is not None:
            connector = "└── " if is_last else "├── "
            lines.append(prefix + connector + str(node.data))
            new_prefix = prefix + ("    " if is_last else "│   ")
            # 右の子を先に表示します（上側に表示されるため）
            children = []
            if node.left:
                children.append(("L:", node.left))
            if node.right:
                children.append(("R:", node.right))
            for i, (label, child) in enumerate(children):
                is_last_child = (i == len(children) - 1)
                self._build_display(child, new_prefix, is_last_child, lines)


# ============================================================
# 計算量の比較表
# ============================================================

def show_complexity_table():
    """各データ構造の計算量を比較表で表示します"""
    print("\n  ■ データ構造の計算量比較（オーダー記法）")
    print(f"    {'構造':　<12} {'探索':>8} {'挿入':>8} {'削除':>8} {'備考'}")
    print("    " + "─" * 56)
    data = [
        ("配列(array)", "O(n)", "O(n)", "O(n)", "インデックスアクセスはO(1)"),
        ("スタック", "O(n)", "O(1)", "O(1)", "push/popのみ"),
        ("キュー", "O(n)", "O(1)", "O(1)", "enqueue/dequeueのみ"),
        ("連結リスト", "O(n)", "O(1)*", "O(1)*", "*位置が分かっている場合"),
        ("二分探索木", "O(log n)", "O(log n)", "O(log n)", "平均の場合"),
        ("ハッシュ表", "O(1)", "O(1)", "O(1)", "平均の場合"),
    ]
    for name, search, insert, delete, note in data:
        print(f"    {name:<12} {search:>8} {insert:>8} {delete:>8} {note}")


# ============================================================
# 対話モード
# ============================================================

def interactive_mode():
    """対話型のデータ構造体験です"""
    print("\n" + "=" * 55)
    print("  データ構造体験 - 対話モード")
    print("=" * 55)
    print("  操作するデータ構造を選んでください:")
    print("    1. スタック (LIFO)")
    print("    2. キュー (FIFO)")
    print("    3. 連結リスト")
    print("    4. 二分探索木")
    print("    0. 終了")
    print("-" * 55)

    while True:
        choice = input("\n  データ構造を選択 (0-4): ").strip()

        if choice == "0":
            print("  データ構造体験を終了します。")
            break

        elif choice == "1":
            print("\n  ■ スタック操作")
            stack = Stack()
            while True:
                print("\n    操作: push / pop / peek / show / back")
                op = input("    > ").strip().lower()
                if op == "back":
                    break
                elif op == "push":
                    val = input("    値を入力: ").strip()
                    if stack.push(val):
                        print(f"    → {val} を push しました")
                    stack.display()
                elif op == "pop":
                    val = stack.pop()
                    if val is not None:
                        print(f"    → {val} を pop しました")
                    stack.display()
                elif op == "peek":
                    val = stack.peek()
                    print(f"    → トップの値: {val}")
                elif op == "show":
                    stack.display()

        elif choice == "2":
            print("\n  ■ キュー操作")
            queue = Queue()
            while True:
                print("\n    操作: enqueue / dequeue / front / show / back")
                op = input("    > ").strip().lower()
                if op == "back":
                    break
                elif op == "enqueue":
                    val = input("    値を入力: ").strip()
                    if queue.enqueue(val):
                        print(f"    → {val} を enqueue しました")
                    queue.display()
                elif op == "dequeue":
                    val = queue.dequeue()
                    if val is not None:
                        print(f"    → {val} を dequeue しました")
                    queue.display()
                elif op == "front":
                    val = queue.front()
                    print(f"    → 先頭の値: {val}")
                elif op == "show":
                    queue.display()

        elif choice == "3":
            print("\n  ■ 連結リスト操作")
            ll = LinkedList()
            while True:
                print("\n    操作: append / insert / delete / search / show / back")
                op = input("    > ").strip().lower()
                if op == "back":
                    break
                elif op == "append":
                    val = input("    値を入力: ").strip()
                    ll.append(val)
                    print(f"    → {val} を末尾に追加しました")
                    ll.display()
                elif op == "insert":
                    try:
                        idx = int(input("    挿入位置 (インデックス): "))
                        val = input("    値を入力: ").strip()
                        if ll.insert(idx, val):
                            print(f"    → 位置{idx}に {val} を挿入しました")
                        ll.display()
                    except ValueError:
                        print("    ※ 正しい数値を入力してください。")
                elif op == "delete":
                    val = input("    削除する値: ").strip()
                    if ll.delete(val):
                        print(f"    → {val} を削除しました")
                    else:
                        print(f"    → {val} は見つかりませんでした")
                    ll.display()
                elif op == "search":
                    val = input("    検索する値: ").strip()
                    idx = ll.search(val)
                    if idx >= 0:
                        print(f"    → {val} は位置 {idx} にあります")
                    else:
                        print(f"    → {val} は見つかりませんでした")
                elif op == "show":
                    ll.display()

        elif choice == "4":
            print("\n  ■ 二分探索木操作")
            bst = BinarySearchTree()
            while True:
                print("\n    操作: insert / search / traverse / show / back")
                op = input("    > ").strip().lower()
                if op == "back":
                    break
                elif op == "insert":
                    try:
                        val = int(input("    挿入する数値: "))
                        bst.insert(val)
                        print(f"    → {val} を挿入しました")
                        bst.display()
                    except ValueError:
                        print("    ※ 整数を入力してください。")
                elif op == "search":
                    try:
                        val = int(input("    検索する数値: "))
                        bst.search(val)
                    except ValueError:
                        print("    ※ 整数を入力してください。")
                elif op == "traverse":
                    print(f"    中間順（inorder）:  {bst.inorder()}")
                    print(f"    前順（preorder）:   {bst.preorder()}")
                    print(f"    後順（postorder）:  {bst.postorder()}")
                elif op == "show":
                    bst.display()

        else:
            print("  ※ 0-4の番号を入力してください。")


# === デモンストレーション ===
print("=" * 55)
print("  データ構造体験プログラム")
print("  ～ スタック・キュー・リスト・木を動かそう ～")
print("=" * 55)

# --- 1. スタックのデモ ---
print("\n━━━ 1. スタック（LIFO: 後入れ先出し） ━━━")
print("  イメージ: 積み上げた本 → 上からしか取れません")
print()
stack = Stack()
for item in ["A", "B", "C", "D"]:
    stack.push(item)
    print(f"  push({item})")
stack.display()

print()
for _ in range(2):
    val = stack.pop()
    print(f"  pop() → {val}")
stack.display()

# スタックの応用例: 括弧の対応チェック
print("\n  ■ スタックの応用: 括弧の対応チェック")
test_exprs = ["((a+b)*(c-d))", "((a+b)", "(a+b))(", "{[()]}"]
for expr in test_exprs:
    bracket_stack = Stack()
    pairs = {"(": ")", "[": "]", "{": "}"}
    valid = True
    for ch in expr:
        if ch in pairs:
            bracket_stack.push(ch)
        elif ch in pairs.values():
            if bracket_stack.is_empty():
                valid = False
                break
            top = bracket_stack.pop()
            if pairs.get(top) != ch:
                valid = False
                break
    if not bracket_stack.is_empty():
        valid = False
    status = "OK" if valid else "NG"
    print(f"    {expr:<16} → {status}")

# --- 2. キューのデモ ---
print("\n\n━━━ 2. キュー（FIFO: 先入れ先出し） ━━━")
print("  イメージ: レジの行列 → 先に並んだ人から処理されます")
print()
queue = Queue()
customers = ["田中さん", "佐藤さん", "鈴木さん", "高橋さん"]
for c in customers:
    queue.enqueue(c)
    print(f"  enqueue({c})")
queue.display()

print()
for _ in range(2):
    val = queue.dequeue()
    print(f"  dequeue() → {val}")
queue.display()

# --- 3. 連結リストのデモ ---
print("\n\n━━━ 3. 連結リスト（Linked List） ━━━")
print("  各ノードが次のノードへのポインタを持ちます")
print()
ll = LinkedList()
for item in [10, 20, 30, 40, 50]:
    ll.append(item)
print("  初期状態:")
ll.display()

print("\n  位置2に 25 を挿入:")
ll.insert(2, 25)
ll.display()

print("\n  30 を削除:")
ll.delete(30)
ll.display()

print(f"\n  25 を検索: 位置 {ll.search(25)}")
print(f"  99 を検索: 位置 {ll.search(99)} (見つからない)")

# --- 4. 二分探索木のデモ ---
print("\n\n━━━ 4. 二分探索木（Binary Search Tree） ━━━")
print("  規則: 左の子 < 親 < 右の子")
print()
bst = BinarySearchTree()
values = [50, 30, 70, 20, 40, 60, 80]
print(f"  挿入順: {values}")
for v in values:
    bst.insert(v)

print("\n  木の構造:")
bst.display()

print("\n  ■ 走査（traversal）結果")
print(f"    中間順（inorder）:  {bst.inorder()}  ← 昇順になります!")
print(f"    前順（preorder）:   {bst.preorder()}")
print(f"    後順（postorder）:  {bst.postorder()}")

print("\n  ■ 探索のデモ")
bst.search(40)
bst.search(55)

# --- 5. 計算量の比較 ---
print("\n")
show_complexity_table()

# --- 対話モード ---
print()
interactive_mode()
