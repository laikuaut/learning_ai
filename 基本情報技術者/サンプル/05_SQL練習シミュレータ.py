# ==============================
# SQL練習シミュレータ
# 基本情報技術者：データベース
# ==============================
# 学べる内容:
#   - SELECT文（射影・選択）
#   - WHERE句（条件指定）
#   - ORDER BY句（並べ替え）
#   - GROUP BY句 / HAVING句（集約）
#   - 集約関数（COUNT, SUM, AVG, MAX, MIN）
#   - JOIN（内部結合・左外部結合）
#   - INSERT / UPDATE / DELETE
#   - 基本情報技術者試験のSQL問題への対応力
#
# 実行方法:
#   python 05_SQL練習シミュレータ.py
# ==============================

import re


# ============================================================
# テーブルデータ（メモリ上のデータベース）
# ============================================================

class Table:
    """メモリ上のテーブルを表現するクラスです"""

    def __init__(self, name, columns, rows=None):
        self.name = name
        self.columns = columns  # カラム名のリスト
        self.rows = rows if rows else []  # 辞書のリスト

    def copy(self):
        """テーブルのコピーを作成します"""
        return Table(self.name, self.columns.copy(),
                     [row.copy() for row in self.rows])

    def display(self, title=None, max_rows=50):
        """テーブルを整形して表示します"""
        if title:
            print(f"\n  {title}")

        if not self.rows:
            print("    (0件)")
            return

        # 各カラムの最大幅を計算します
        widths = {}
        for col in self.columns:
            widths[col] = max(
                len(str(col)),
                max((len(str(row.get(col, ""))) for row in self.rows), default=0)
            )
            widths[col] = min(widths[col], 20)  # 最大20文字

        # ヘッダー
        header = " | ".join(f"{col:<{widths[col]}}" for col in self.columns)
        separator = "-+-".join("-" * widths[col] for col in self.columns)
        print(f"    {header}")
        print(f"    {separator}")

        # データ行
        display_rows = self.rows[:max_rows]
        for row in display_rows:
            line = " | ".join(
                f"{str(row.get(col, 'NULL')):<{widths[col]}}"
                for col in self.columns
            )
            print(f"    {line}")

        if len(self.rows) > max_rows:
            print(f"    ... 他 {len(self.rows) - max_rows} 件")

        print(f"    ({len(self.rows)}件)")


class Database:
    """メモリ上のデータベースです"""

    def __init__(self):
        self.tables = {}

    def create_table(self, name, columns, rows=None):
        """テーブルを作成します"""
        table = Table(name, columns, rows)
        self.tables[name] = table
        return table

    def get_table(self, name):
        """テーブルを取得します"""
        name_upper = name.upper()
        for tname, table in self.tables.items():
            if tname.upper() == name_upper:
                return table
        return None

    def show_tables(self):
        """全テーブル一覧を表示します"""
        print("\n  ■ テーブル一覧")
        for name, table in self.tables.items():
            print(f"    {name} ({len(table.columns)}列, {len(table.rows)}行)")
            cols = ", ".join(table.columns)
            print(f"      カラム: {cols}")


# ============================================================
# SQLパーサーとエグゼキュータ
# ============================================================

class SQLEngine:
    """簡易SQLエンジンです（SELECT, INSERT, UPDATE, DELETE対応）"""

    def __init__(self, db):
        self.db = db

    def execute(self, sql):
        """SQLを解析して実行します"""
        sql = sql.strip().rstrip(";")
        sql_upper = sql.upper().strip()

        if sql_upper.startswith("SELECT"):
            return self._execute_select(sql)
        elif sql_upper.startswith("INSERT"):
            return self._execute_insert(sql)
        elif sql_upper.startswith("UPDATE"):
            return self._execute_update(sql)
        elif sql_upper.startswith("DELETE"):
            return self._execute_delete(sql)
        elif sql_upper.startswith("SHOW"):
            self.db.show_tables()
            return None
        else:
            print("    ※ 対応していないSQL文です。")
            return None

    def _execute_select(self, sql):
        """SELECT文を実行します"""
        sql_upper = sql.upper()

        # FROM句からテーブル名を取得します
        from_match = re.search(r'FROM\s+(\w+)', sql_upper)
        if not from_match:
            print("    ※ FROM句が見つかりません。")
            return None

        table_name = from_match.group(1)
        table = self.db.get_table(table_name)
        if not table:
            print(f"    ※ テーブル '{table_name}' が見つかりません。")
            return None

        # 作業用のコピーを作成します
        working_rows = [row.copy() for row in table.rows]
        available_columns = table.columns.copy()

        # JOIN句の処理
        join_match = re.search(
            r'(INNER\s+JOIN|LEFT\s+(?:OUTER\s+)?JOIN|JOIN)\s+(\w+)\s+ON\s+(\w+)\.(\w+)\s*=\s*(\w+)\.(\w+)',
            sql_upper
        )
        if join_match:
            join_type = join_match.group(1).strip()
            join_table_name = join_match.group(2)
            left_table = join_match.group(3)
            left_col = join_match.group(4)
            right_table = join_match.group(5)
            right_col = join_match.group(6)

            join_table = self.db.get_table(join_table_name)
            if not join_table:
                print(f"    ※ テーブル '{join_table_name}' が見つかりません。")
                return None

            # 結合カラムを追加します
            for col in join_table.columns:
                if col not in available_columns:
                    available_columns.append(col)

            # 結合を実行します
            new_rows = []
            is_left_join = "LEFT" in join_type

            # カラム名のマッピング（テーブル名を除去）
            for row in working_rows:
                matched = False
                for jrow in join_table.rows:
                    left_val = row.get(left_col, row.get(f"{left_table}.{left_col}"))
                    right_val = jrow.get(right_col, jrow.get(f"{right_table}.{right_col}"))
                    if left_val is not None and right_val is not None and str(left_val) == str(right_val):
                        merged = {**row, **jrow}
                        new_rows.append(merged)
                        matched = True
                if is_left_join and not matched:
                    null_row = {col: None for col in join_table.columns}
                    merged = {**row, **null_row}
                    new_rows.append(merged)

            working_rows = new_rows

        # WHERE句の処理
        where_match = re.search(r'WHERE\s+(.+?)(?:\s+GROUP\s+BY|\s+ORDER\s+BY|\s+HAVING|\s*$)', sql, re.IGNORECASE)
        if where_match:
            condition = where_match.group(1).strip()
            working_rows = self._filter_rows(working_rows, condition)

        # GROUP BY句の処理
        group_match = re.search(r'GROUP\s+BY\s+([\w\s,]+?)(?:\s+HAVING|\s+ORDER\s+BY|\s*$)', sql_upper)
        if group_match:
            group_cols = [c.strip() for c in group_match.group(1).split(",")]
            working_rows = self._group_rows(working_rows, group_cols, sql)

            # HAVING句の処理
            having_match = re.search(r'HAVING\s+(.+?)(?:\s+ORDER\s+BY|\s*$)', sql, re.IGNORECASE)
            if having_match:
                condition = having_match.group(1).strip()
                working_rows = self._filter_rows(working_rows, condition)

        # ORDER BY句の処理
        order_match = re.search(r'ORDER\s+BY\s+([\w\s,]+?)(?:\s+ASC|\s+DESC)?(?:\s*$)', sql_upper)
        if order_match:
            order_col = order_match.group(1).strip().split(",")[0].strip()
            desc = "DESC" in sql_upper.split("ORDER BY")[1] if "ORDER BY" in sql_upper else False
            working_rows = self._order_rows(working_rows, order_col, desc)

        # SELECT句の処理（カラム選択）
        select_match = re.search(r'SELECT\s+(.+?)\s+FROM', sql, re.IGNORECASE)
        if select_match:
            select_clause = select_match.group(1).strip()
            if select_clause == "*":
                result_columns = available_columns
            else:
                result_columns = []
                for part in select_clause.split(","):
                    part = part.strip()
                    # エイリアス処理
                    alias_match = re.match(r'(.+?)\s+AS\s+(\w+)', part, re.IGNORECASE)
                    if alias_match:
                        expr = alias_match.group(1).strip()
                        alias = alias_match.group(2).strip()
                        result_columns.append(alias)
                        # 集約関数の結果をエイリアスで参照可能にします
                        for row in working_rows:
                            if expr.upper() in row:
                                row[alias] = row[expr.upper()]
                    else:
                        # テーブル名.カラム名の場合、カラム名だけ取得します
                        if "." in part:
                            col = part.split(".")[1].strip()
                        else:
                            col = part
                        result_columns.append(col)
        else:
            result_columns = available_columns

        # DISTINCT の処理
        distinct = "DISTINCT" in sql_upper.split("FROM")[0]
        if distinct:
            seen = []
            unique_rows = []
            for row in working_rows:
                key = tuple(row.get(col) for col in result_columns)
                if key not in seen:
                    seen.append(key)
                    unique_rows.append(row)
            working_rows = unique_rows

        result = Table("結果", result_columns, working_rows)
        return result

    def _filter_rows(self, rows, condition):
        """WHERE/HAVING条件でフィルタリングします"""
        filtered = []
        for row in rows:
            if self._evaluate_condition(row, condition):
                filtered.append(row)
        return filtered

    def _evaluate_condition(self, row, condition):
        """条件式を評価します"""
        # AND/OR対応
        condition_upper = condition.upper()

        if " AND " in condition_upper:
            parts = re.split(r'\s+AND\s+', condition, flags=re.IGNORECASE)
            return all(self._evaluate_condition(row, p.strip()) for p in parts)

        if " OR " in condition_upper:
            parts = re.split(r'\s+OR\s+', condition, flags=re.IGNORECASE)
            return any(self._evaluate_condition(row, p.strip()) for p in parts)

        # BETWEEN
        between_match = re.match(r'(\w+)\s+BETWEEN\s+(\S+)\s+AND\s+(\S+)', condition, re.IGNORECASE)
        if between_match:
            col = between_match.group(1).strip()
            low = self._parse_value(between_match.group(2))
            high = self._parse_value(between_match.group(3))
            val = row.get(col)
            if val is not None:
                return low <= val <= high
            return False

        # LIKE
        like_match = re.match(r"(\w+)\s+LIKE\s+'([^']*)'", condition, re.IGNORECASE)
        if like_match:
            col = like_match.group(1).strip()
            pattern = like_match.group(2)
            val = str(row.get(col, ""))
            # SQL LIKE → 簡易正規表現変換
            regex_pattern = "^" + pattern.replace("%", ".*").replace("_", ".") + "$"
            return bool(re.match(regex_pattern, val, re.IGNORECASE))

        # IN
        in_match = re.match(r"(\w+)\s+IN\s*\(([^)]+)\)", condition, re.IGNORECASE)
        if in_match:
            col = in_match.group(1).strip()
            values = [self._parse_value(v.strip()) for v in in_match.group(2).split(",")]
            return row.get(col) in values

        # IS NULL / IS NOT NULL
        null_match = re.match(r'(\w+)\s+IS\s+(NOT\s+)?NULL', condition, re.IGNORECASE)
        if null_match:
            col = null_match.group(1).strip()
            is_not = null_match.group(2) is not None
            val = row.get(col)
            if is_not:
                return val is not None
            return val is None

        # 比較演算子（>=, <=, !=, <>, =, >, <）
        comp_match = re.match(r"(\w+(?:\(\w+\))?)\s*(>=|<=|!=|<>|=|>|<)\s*(.+)", condition.strip())
        if comp_match:
            left = comp_match.group(1).strip()
            op = comp_match.group(2).strip()
            right_str = comp_match.group(3).strip()

            # 集約関数の場合
            left_upper = left.upper()
            if left_upper in row:
                left_val = row[left_upper]
            else:
                left_val = row.get(left, None)

            right_val = self._parse_value(right_str)

            if left_val is None:
                return False

            try:
                # 数値比較を試みます
                left_num = float(left_val)
                right_num = float(right_val)
                if op == "=":
                    return left_num == right_num
                elif op in ("!=", "<>"):
                    return left_num != right_num
                elif op == ">":
                    return left_num > right_num
                elif op == "<":
                    return left_num < right_num
                elif op == ">=":
                    return left_num >= right_num
                elif op == "<=":
                    return left_num <= right_num
            except (ValueError, TypeError):
                # 文字列比較
                left_str = str(left_val)
                right_str_val = str(right_val)
                if op == "=":
                    return left_str == right_str_val
                elif op in ("!=", "<>"):
                    return left_str != right_str_val

        return True

    def _parse_value(self, value_str):
        """値の文字列をPythonの値に変換します"""
        value_str = value_str.strip()
        # 文字列リテラル
        if (value_str.startswith("'") and value_str.endswith("'")) or \
           (value_str.startswith('"') and value_str.endswith('"')):
            return value_str[1:-1]
        # 数値
        try:
            if "." in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            return value_str

    def _group_rows(self, rows, group_cols, original_sql):
        """GROUP BY を処理します"""
        groups = {}
        for row in rows:
            key = tuple(row.get(col) for col in group_cols)
            if key not in groups:
                groups[key] = []
            groups[key].append(row)

        # 集約関数の検出
        select_match = re.search(r'SELECT\s+(.+?)\s+FROM', original_sql, re.IGNORECASE)
        if not select_match:
            return rows

        select_clause = select_match.group(1)
        agg_funcs = re.findall(r'(COUNT|SUM|AVG|MAX|MIN)\s*\(\s*(\*|\w+)\s*\)', select_clause, re.IGNORECASE)

        result = []
        for key, group in groups.items():
            row = {}
            for i, col in enumerate(group_cols):
                row[col] = key[i]

            for func_name, col_name in agg_funcs:
                func_upper = func_name.upper()
                agg_key = f"{func_upper}({col_name.upper()})"

                if func_upper == "COUNT":
                    if col_name == "*":
                        row[agg_key] = len(group)
                    else:
                        row[agg_key] = sum(1 for r in group if r.get(col_name) is not None)
                elif func_upper == "SUM":
                    vals = [r.get(col_name, 0) for r in group if r.get(col_name) is not None]
                    row[agg_key] = sum(vals)
                elif func_upper == "AVG":
                    vals = [r.get(col_name, 0) for r in group if r.get(col_name) is not None]
                    row[agg_key] = round(sum(vals) / len(vals), 1) if vals else 0
                elif func_upper == "MAX":
                    vals = [r.get(col_name) for r in group if r.get(col_name) is not None]
                    row[agg_key] = max(vals) if vals else None
                elif func_upper == "MIN":
                    vals = [r.get(col_name) for r in group if r.get(col_name) is not None]
                    row[agg_key] = min(vals) if vals else None

            result.append(row)
        return result

    def _order_rows(self, rows, order_col, desc=False):
        """ORDER BY を処理します"""
        def sort_key(row):
            val = row.get(order_col, "")
            if val is None:
                return (1, "")
            try:
                return (0, float(val))
            except (ValueError, TypeError):
                return (0, str(val))

        return sorted(rows, key=sort_key, reverse=desc)

    def _execute_insert(self, sql):
        """INSERT文を実行します"""
        match = re.match(
            r"INSERT\s+INTO\s+(\w+)\s*\(([^)]+)\)\s*VALUES\s*\(([^)]+)\)",
            sql, re.IGNORECASE
        )
        if not match:
            print("    ※ INSERT文の構文エラーです。")
            return None

        table_name = match.group(1)
        columns = [c.strip() for c in match.group(2).split(",")]
        values = [self._parse_value(v.strip()) for v in match.group(3).split(",")]

        table = self.db.get_table(table_name)
        if not table:
            print(f"    ※ テーブル '{table_name}' が見つかりません。")
            return None

        row = dict(zip(columns, values))
        table.rows.append(row)
        print(f"    → 1行挿入しました ({table_name})")
        return table

    def _execute_update(self, sql):
        """UPDATE文を実行します"""
        match = re.match(
            r"UPDATE\s+(\w+)\s+SET\s+(.+?)(?:\s+WHERE\s+(.+))?$",
            sql, re.IGNORECASE
        )
        if not match:
            print("    ※ UPDATE文の構文エラーです。")
            return None

        table_name = match.group(1)
        set_clause = match.group(2)
        where_clause = match.group(3)

        table = self.db.get_table(table_name)
        if not table:
            print(f"    ※ テーブル '{table_name}' が見つかりません。")
            return None

        # SET句の解析
        updates = {}
        for part in set_clause.split(","):
            col, val = part.split("=")
            updates[col.strip()] = self._parse_value(val.strip())

        count = 0
        for row in table.rows:
            if where_clause is None or self._evaluate_condition(row, where_clause):
                for col, val in updates.items():
                    row[col] = val
                count += 1

        print(f"    → {count}行更新しました ({table_name})")
        return table

    def _execute_delete(self, sql):
        """DELETE文を実行します"""
        match = re.match(
            r"DELETE\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+))?$",
            sql, re.IGNORECASE
        )
        if not match:
            print("    ※ DELETE文の構文エラーです。")
            return None

        table_name = match.group(1)
        where_clause = match.group(2)

        table = self.db.get_table(table_name)
        if not table:
            print(f"    ※ テーブル '{table_name}' が見つかりません。")
            return None

        if where_clause:
            original_count = len(table.rows)
            table.rows = [
                row for row in table.rows
                if not self._evaluate_condition(row, where_clause)
            ]
            count = original_count - len(table.rows)
        else:
            count = len(table.rows)
            table.rows = []

        print(f"    → {count}行削除しました ({table_name})")
        return table

    # SQLパーサーで使うユーティリティ
    def _parse_value(self, value_str):
        """値の文字列をPythonの値に変換します"""
        value_str = value_str.strip()
        if (value_str.startswith("'") and value_str.endswith("'")) or \
           (value_str.startswith('"') and value_str.endswith('"')):
            return value_str[1:-1]
        try:
            if "." in value_str:
                return float(value_str)
            return int(value_str)
        except ValueError:
            return value_str


# ============================================================
# サンプルデータベースの構築
# ============================================================

def create_sample_db():
    """試験でよく出るサンプルデータベースを作成します"""
    db = Database()

    # 社員テーブル
    db.create_table("社員", ["社員番号", "名前", "部署コード", "役職", "給与", "入社年"], [
        {"社員番号": 1001, "名前": "田中太郎", "部署コード": "D01", "役職": "部長", "給与": 600000, "入社年": 2005},
        {"社員番号": 1002, "名前": "佐藤花子", "部署コード": "D01", "役職": "課長", "給与": 450000, "入社年": 2010},
        {"社員番号": 1003, "名前": "鈴木一郎", "部署コード": "D02", "役職": "主任", "給与": 380000, "入社年": 2015},
        {"社員番号": 1004, "名前": "高橋美咲", "部署コード": "D02", "役職": "一般", "給与": 300000, "入社年": 2020},
        {"社員番号": 1005, "名前": "伊藤健太", "部署コード": "D03", "役職": "課長", "給与": 420000, "入社年": 2012},
        {"社員番号": 1006, "名前": "渡辺優子", "部署コード": "D03", "役職": "一般", "給与": 280000, "入社年": 2022},
        {"社員番号": 1007, "名前": "山本大輔", "部署コード": "D01", "役職": "一般", "給与": 320000, "入社年": 2018},
        {"社員番号": 1008, "名前": "中村理恵", "部署コード": "D02", "役職": "課長", "給与": 440000, "入社年": 2011},
    ])

    # 部署テーブル
    db.create_table("部署", ["部署コード", "部署名", "所在地"], [
        {"部署コード": "D01", "部署名": "営業部", "所在地": "東京"},
        {"部署コード": "D02", "部署名": "開発部", "所在地": "横浜"},
        {"部署コード": "D03", "部署名": "人事部", "所在地": "東京"},
        {"部署コード": "D04", "部署名": "経理部", "所在地": "大阪"},
    ])

    # 売上テーブル
    db.create_table("売上", ["売上ID", "社員番号", "商品名", "金額", "売上日"], [
        {"売上ID": 1, "社員番号": 1001, "商品名": "ノートPC", "金額": 150000, "売上日": "2024-01-15"},
        {"売上ID": 2, "社員番号": 1002, "商品名": "タブレット", "金額": 80000, "売上日": "2024-01-20"},
        {"売上ID": 3, "社員番号": 1001, "商品名": "モニター", "金額": 45000, "売上日": "2024-02-10"},
        {"売上ID": 4, "社員番号": 1005, "商品名": "キーボード", "金額": 12000, "売上日": "2024-02-15"},
        {"売上ID": 5, "社員番号": 1007, "商品名": "ノートPC", "金額": 150000, "売上日": "2024-03-01"},
        {"売上ID": 6, "社員番号": 1002, "商品名": "マウス", "金額": 5000, "売上日": "2024-03-10"},
        {"売上ID": 7, "社員番号": 1001, "商品名": "プリンター", "金額": 35000, "売上日": "2024-03-20"},
    ])

    return db


# ============================================================
# 対話モード
# ============================================================

def interactive_mode(db, engine):
    """対話型のSQL練習シミュレータです"""
    print("\n" + "=" * 60)
    print("  SQL練習シミュレータ - 対話モード")
    print("=" * 60)
    print("  使えるコマンド:")
    print("    SQL文を入力     ... SQLを実行します")
    print("    SHOW TABLES      ... テーブル一覧を表示します")
    print("    SHOW テーブル名  ... テーブルの中身を表示します")
    print("    HINT             ... 練習問題のヒントを表示します")
    print("    RESET            ... データを初期状態に戻します")
    print("    EXIT             ... 終了します")
    print("-" * 60)

    while True:
        try:
            sql = input("\n  SQL> ").strip()
        except EOFError:
            break

        if not sql:
            continue

        sql_upper = sql.upper()

        if sql_upper in ("EXIT", "QUIT", "Q"):
            print("  SQL練習シミュレータを終了します。")
            break

        elif sql_upper == "RESET":
            db = create_sample_db()
            engine.db = db
            print("  → データを初期状態にリセットしました。")

        elif sql_upper == "HINT":
            print("\n  ■ 練習問題（試してみましょう！）")
            print("    1. SELECT * FROM 社員")
            print("    2. SELECT 名前, 給与 FROM 社員 WHERE 給与 >= 400000")
            print("    3. SELECT 名前, 給与 FROM 社員 ORDER BY 給与 DESC")
            print("    4. SELECT 部署コード, COUNT(*) AS 人数 FROM 社員 GROUP BY 部署コード")
            print("    5. SELECT 名前, 部署名 FROM 社員 JOIN 部署 ON 社員.部署コード = 部署.部署コード")
            print("    6. SELECT 部署コード, AVG(給与) AS 平均給与 FROM 社員 GROUP BY 部署コード HAVING AVG(給与) > 350000")

        elif sql_upper.startswith("SHOW ") and sql_upper != "SHOW TABLES":
            table_name = sql.split(None, 1)[1]
            table = db.get_table(table_name)
            if table:
                table.display(f"テーブル: {table.name}")
            else:
                print(f"    ※ テーブル '{table_name}' が見つかりません。")

        else:
            print(f"  実行: {sql}")
            result = engine.execute(sql)
            if result and isinstance(result, Table):
                result.display("実行結果:")


# === デモンストレーション ===
print("=" * 60)
print("  SQL練習シミュレータ")
print("  ～ SQLの基本操作を体験しよう ～")
print("=" * 60)

db = create_sample_db()
engine = SQLEngine(db)

# テーブル一覧の表示
db.show_tables()

# 各テーブルの中身を表示
for name, table in db.tables.items():
    table.display(f"テーブル: {name}")

# --- デモ1: 基本的なSELECT ---
print("\n\n━━━ デモ1: 基本的なSELECT ━━━")

demo_queries = [
    ("全件取得", "SELECT * FROM 社員"),
    ("カラム指定", "SELECT 名前, 給与 FROM 社員"),
    ("条件指定（WHERE）", "SELECT 名前, 給与 FROM 社員 WHERE 給与 >= 400000"),
    ("複数条件（AND）", "SELECT 名前, 役職, 給与 FROM 社員 WHERE 部署コード = 'D01' AND 給与 > 300000"),
    ("LIKE検索", "SELECT 名前, 役職 FROM 社員 WHERE 名前 LIKE '%子'"),
    ("BETWEEN", "SELECT 名前, 入社年 FROM 社員 WHERE 入社年 BETWEEN 2010 AND 2018"),
]

for title, sql in demo_queries:
    print(f"\n  ■ {title}")
    print(f"    SQL: {sql}")
    result = engine.execute(sql)
    if result:
        result.display()

# --- デモ2: 並べ替えと集約 ---
print("\n\n━━━ デモ2: 並べ替えと集約 ━━━")

demo_queries2 = [
    ("給与順（降順）", "SELECT 名前, 給与 FROM 社員 ORDER BY 給与 DESC"),
    ("部署別人数", "SELECT 部署コード, COUNT(*) AS 人数 FROM 社員 GROUP BY 部署コード"),
    ("部署別平均給与", "SELECT 部署コード, AVG(給与) AS 平均給与 FROM 社員 GROUP BY 部署コード"),
    ("HAVING条件", "SELECT 部署コード, AVG(給与) AS 平均給与 FROM 社員 GROUP BY 部署コード HAVING AVG(給与) > 350000"),
]

for title, sql in demo_queries2:
    print(f"\n  ■ {title}")
    print(f"    SQL: {sql}")
    result = engine.execute(sql)
    if result:
        result.display()

# --- デモ3: JOIN ---
print("\n\n━━━ デモ3: テーブル結合（JOIN） ━━━")

demo_queries3 = [
    ("内部結合（INNER JOIN）",
     "SELECT 名前, 部署名, 給与 FROM 社員 JOIN 部署 ON 社員.部署コード = 部署.部署コード"),
    ("左外部結合（LEFT JOIN）",
     "SELECT 部署名, 名前 FROM 部署 LEFT JOIN 社員 ON 部署.部署コード = 社員.部署コード"),
]

for title, sql in demo_queries3:
    print(f"\n  ■ {title}")
    print(f"    SQL: {sql}")
    result = engine.execute(sql)
    if result:
        result.display()

# --- デモ4: INSERT / UPDATE / DELETE ---
print("\n\n━━━ デモ4: データ更新（INSERT / UPDATE / DELETE） ━━━")

print("\n  ■ INSERT（挿入）")
insert_sql = "INSERT INTO 社員 (社員番号, 名前, 部署コード, 役職, 給与, 入社年) VALUES (1009, '木村拓也', 'D02', '一般', 290000, 2024)"
print(f"    SQL: {insert_sql}")
engine.execute(insert_sql)

print("\n  ■ 挿入後の確認")
result = engine.execute("SELECT * FROM 社員 WHERE 社員番号 = 1009")
if result:
    result.display()

print("\n  ■ UPDATE（更新）")
update_sql = "UPDATE 社員 SET 給与 = 310000 WHERE 社員番号 = 1009"
print(f"    SQL: {update_sql}")
engine.execute(update_sql)

result = engine.execute("SELECT 名前, 給与 FROM 社員 WHERE 社員番号 = 1009")
if result:
    result.display()

print("\n  ■ DELETE（削除）")
delete_sql = "DELETE FROM 社員 WHERE 社員番号 = 1009"
print(f"    SQL: {delete_sql}")
engine.execute(delete_sql)

# --- 試験頻出ポイント ---
print("\n\n━━━ 試験頻出ポイント ━━━")
print("  ■ SQL句の実行順序（重要！）")
print("    1. FROM    ... テーブルを指定します")
print("    2. JOIN    ... テーブルを結合します")
print("    3. WHERE   ... 行を絞り込みます")
print("    4. GROUP BY ... グループ化します")
print("    5. HAVING  ... グループを絞り込みます")
print("    6. SELECT  ... 列を選択します")
print("    7. ORDER BY ... 並べ替えます")
print()
print("  ■ 集約関数")
print("    COUNT(*) ... 行数を数えます（NULLも含む）")
print("    COUNT(列) ... 列のNULL以外の数を数えます")
print("    SUM(列)  ... 合計を計算します")
print("    AVG(列)  ... 平均を計算します")
print("    MAX(列)  ... 最大値を返します")
print("    MIN(列)  ... 最小値を返します")

# --- 対話モード ---
print()
interactive_mode(db, engine)
