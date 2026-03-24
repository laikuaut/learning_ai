# ==============================
# アクセスコントロールシミュレータ
# 情報セキュリティ基礎：RBAC/ACLの仕組みを体験するサンプル
# ==============================
# 学べる内容:
#   - アクセス制御の基本概念（認証と認可の違い）
#   - RBAC（Role-Based Access Control）ロールベースアクセス制御
#   - ACL（Access Control List）アクセス制御リスト
#   - 最小権限の原則（Principle of Least Privilege）
#   - 権限の継承と職務分離
#
# 実行方法:
#   python 05_アクセスコントロール.py
#
# ※ 本プログラムは教育目的で作成されています
# ==============================


def explain_access_control():
    """アクセス制御の基本をアスキーアートで解説します"""
    print("""
  ┌──────────────────────────────────────────────────┐
  │            アクセス制御（Access Control）とは？    │
  └──────────────────────────────────────────────────┘

  「誰が」「何に」「どのような操作を」できるかを管理する仕組みです。

  【認証と認可の違い】
  ┌──────────┬──────────────────────────────────────┐
  │ 認証      │ あなたは誰ですか？（Authentication）  │
  │ (AuthN)  │ → ログイン、ID/パスワード確認         │
  ├──────────┼──────────────────────────────────────┤
  │ 認可      │ あなたは何ができますか？（Authorization）│
  │ (AuthZ)  │ → 権限チェック、アクセス許可/拒否      │
  └──────────┴──────────────────────────────────────┘

  【主なアクセス制御モデル】

  ◆ ACL（Access Control List）
    リソースごとに「誰がどの操作を許可されているか」を記述
    ┌────────────────────────────────┐
    │ ファイル: report.xlsx           │
    │  ├ 田中: 読み取り, 書き込み    │
    │  ├ 佐藤: 読み取りのみ          │
    │  └ 鈴木: アクセス不可          │
    └────────────────────────────────┘

  ◆ RBAC（Role-Based Access Control）
    ユーザーに「役割（ロール）」を割り当て、
    ロールに権限を付与する方式
    ┌───────────┐     ┌───────────┐     ┌───────────┐
    │ ユーザー   │────→│ ロール    │────→│ 権限       │
    │ (田中)    │     │ (管理者)  │     │ (全操作)   │
    │ (佐藤)    │────→│ (編集者)  │────→│ (読+書)    │
    │ (鈴木)    │────→│ (閲覧者)  │────→│ (読のみ)   │
    └───────────┘     └───────────┘     └───────────┘

  【最小権限の原則】
  ユーザーには業務に必要な最小限の権限のみを付与する。
  → セキュリティインシデントの被害を最小化できます。
    """)


# ============================================================
# RBAC（ロールベースアクセス制御）システム
# ============================================================

class RBACSystem:
    """RBACシステムのシミュレーションです"""

    def __init__(self):
        # ロール定義（ロール名: 権限リスト）
        self.roles = {
            "管理者": {
                "description": "システム全体を管理する最高権限",
                "permissions": [
                    "user:create", "user:read", "user:update", "user:delete",
                    "file:create", "file:read", "file:update", "file:delete",
                    "system:config", "system:logs", "system:backup",
                    "report:create", "report:read", "report:export",
                ],
            },
            "マネージャー": {
                "description": "部門を管理し、レポートを作成する権限",
                "permissions": [
                    "user:read",
                    "file:create", "file:read", "file:update",
                    "report:create", "report:read", "report:export",
                    "system:logs",
                ],
            },
            "編集者": {
                "description": "ファイルの作成・編集ができる権限",
                "permissions": [
                    "file:create", "file:read", "file:update",
                    "report:read",
                ],
            },
            "閲覧者": {
                "description": "読み取りのみ可能な権限",
                "permissions": [
                    "file:read",
                    "report:read",
                ],
            },
            "監査人": {
                "description": "ログの確認とレポート閲覧ができる権限",
                "permissions": [
                    "system:logs",
                    "report:read", "report:export",
                ],
            },
        }

        # ユーザー定義（ユーザー名: ロールリスト）
        self.users = {
            "田中太郎": {
                "roles": ["管理者"],
                "department": "情報システム部",
            },
            "佐藤花子": {
                "roles": ["マネージャー"],
                "department": "営業部",
            },
            "鈴木一郎": {
                "roles": ["編集者"],
                "department": "企画部",
            },
            "高橋美咲": {
                "roles": ["閲覧者"],
                "department": "総務部",
            },
            "伊藤健二": {
                "roles": ["編集者", "監査人"],
                "department": "経理部",
            },
        }

        # 操作ログ
        self.access_log = []

    def get_user_permissions(self, username):
        """ユーザーの全権限を取得します（ロール経由）"""
        if username not in self.users:
            return set()

        permissions = set()
        for role_name in self.users[username]["roles"]:
            if role_name in self.roles:
                permissions.update(self.roles[role_name]["permissions"])
        return permissions

    def check_access(self, username, permission):
        """アクセス権限をチェックします"""
        user_permissions = self.get_user_permissions(username)
        allowed = permission in user_permissions

        # ログに記録
        result = "許可" if allowed else "拒否"
        self.access_log.append({
            "user": username,
            "permission": permission,
            "result": result,
        })

        return allowed

    def display_user_info(self, username):
        """ユーザーの情報と権限を表示します"""
        if username not in self.users:
            print(f"  ※ ユーザー '{username}' が見つかりません。")
            return

        user = self.users[username]
        permissions = self.get_user_permissions(username)

        print(f"\n  ┌──────────────────────────────────────────┐")
        print(f"  │  ユーザー情報: {username}")
        print(f"  ├──────────────────────────────────────────┤")
        print(f"  │  部署:   {user['department']}")
        print(f"  │  ロール: {', '.join(user['roles'])}")
        print(f"  ├──────────────────────────────────────────┤")
        print(f"  │  権限一覧 ({len(permissions)}個):")

        # カテゴリ別に表示
        categories = {}
        for perm in sorted(permissions):
            cat, action = perm.split(":")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(action)

        for cat, actions in sorted(categories.items()):
            print(f"  │    {cat}: {', '.join(actions)}")

        print(f"  └──────────────────────────────────────────┘")

    def display_all_users(self):
        """全ユーザーのロールと権限数を一覧表示します"""
        print(f"\n  {'ユーザー名':<12} {'部署':<14} {'ロール':<20} {'権限数':>4}")
        print(f"  {'─' * 12} {'─' * 14} {'─' * 20} {'─' * 4}")

        for username, user in self.users.items():
            perms = self.get_user_permissions(username)
            roles = ", ".join(user["roles"])
            print(f"  {username:<12} {user['department']:<14} {roles:<20} {len(perms):>4}")

    def display_all_roles(self):
        """全ロールの詳細を表示します"""
        print(f"\n  ロール定義一覧:")
        print(f"  {'─' * 55}")

        for role_name, role_info in self.roles.items():
            perms = role_info["permissions"]
            print(f"\n  【{role_name}】 ({len(perms)}権限)")
            print(f"  説明: {role_info['description']}")
            print(f"  権限: ", end="")

            # 権限を改行して表示
            for i, perm in enumerate(perms):
                if i > 0 and i % 4 == 0:
                    print(f"\n        ", end="")
                print(f"{perm}  ", end="")
            print()

    def display_access_log(self):
        """アクセスログを表示します"""
        if not self.access_log:
            print("\n  ※ アクセスログはまだありません。")
            return

        print(f"\n  アクセスログ（直近{min(20, len(self.access_log))}件）:")
        print(f"  {'No':>4} {'ユーザー':<12} {'要求した権限':<20} {'結果'}")
        print(f"  {'─' * 4} {'─' * 12} {'─' * 20} {'─' * 6}")

        recent = self.access_log[-20:]
        for i, log in enumerate(recent, 1):
            mark = "[OK]" if log["result"] == "許可" else "[NG]"
            print(f"  {i:>4} {log['user']:<12} {log['permission']:<20} {mark} {log['result']}")


# ============================================================
# ACL（アクセス制御リスト）システム
# ============================================================

class ACLSystem:
    """ACLシステムのシミュレーションです"""

    def __init__(self):
        # リソースごとのACL
        self.resources = {
            "売上レポート.xlsx": {
                "type": "ファイル",
                "owner": "佐藤花子",
                "acl": {
                    "田中太郎": ["read", "write", "delete"],
                    "佐藤花子": ["read", "write", "delete"],
                    "鈴木一郎": ["read", "write"],
                    "高橋美咲": ["read"],
                },
            },
            "顧客データベース": {
                "type": "データベース",
                "owner": "田中太郎",
                "acl": {
                    "田中太郎": ["read", "write", "delete", "admin"],
                    "佐藤花子": ["read", "write"],
                    "鈴木一郎": ["read"],
                },
            },
            "社内ポータル": {
                "type": "Webアプリ",
                "owner": "田中太郎",
                "acl": {
                    "田中太郎": ["read", "write", "admin"],
                    "佐藤花子": ["read", "write"],
                    "鈴木一郎": ["read", "write"],
                    "高橋美咲": ["read"],
                    "伊藤健二": ["read"],
                },
            },
            "経理システム": {
                "type": "業務システム",
                "owner": "伊藤健二",
                "acl": {
                    "田中太郎": ["read", "write", "delete", "admin"],
                    "伊藤健二": ["read", "write", "delete"],
                    "佐藤花子": ["read"],
                },
            },
        }

    def check_access(self, username, resource_name, action):
        """ACLに基づいてアクセスをチェックします"""
        if resource_name not in self.resources:
            return False, "リソースが見つかりません"

        resource = self.resources[resource_name]
        acl = resource["acl"]

        if username not in acl:
            return False, "ACLに登録されていません"

        if action in acl[username]:
            return True, "アクセス許可"
        else:
            return False, f"'{action}' 権限がありません"

    def display_resource_acl(self, resource_name):
        """リソースのACLを表示します"""
        if resource_name not in self.resources:
            print(f"  ※ リソース '{resource_name}' が見つかりません。")
            return

        resource = self.resources[resource_name]
        print(f"\n  ┌──────────────────────────────────────────┐")
        print(f"  │  リソース: {resource_name}")
        print(f"  │  種類:     {resource['type']}")
        print(f"  │  所有者:   {resource['owner']}")
        print(f"  ├──────────────────────────────────────────┤")
        print(f"  │  アクセス制御リスト（ACL）:")
        print(f"  │  {'ユーザー':<12} {'権限'}")
        print(f"  │  {'─' * 12} {'─' * 25}")

        for user, perms in resource["acl"].items():
            perm_str = ", ".join(perms)
            print(f"  │  {user:<12} {perm_str}")
        print(f"  └──────────────────────────────────────────┘")

    def display_all_resources(self):
        """全リソースのACLを表示します"""
        for resource_name in self.resources:
            self.display_resource_acl(resource_name)

    def display_user_access_matrix(self):
        """ユーザー×リソースのアクセスマトリックスを表示します"""
        # 全ユーザーを収集
        all_users = set()
        for resource in self.resources.values():
            all_users.update(resource["acl"].keys())
        all_users = sorted(all_users)

        print(f"\n  アクセスマトリックス（R=読/W=書/D=削/A=管理）:")
        print(f"\n  {'ユーザー':<12}", end="")
        resource_names = list(self.resources.keys())
        for name in resource_names:
            short_name = name[:8]
            print(f" {short_name:>10}", end="")
        print()

        print(f"  {'─' * 12}", end="")
        for _ in resource_names:
            print(f" {'─' * 10}", end="")
        print()

        for user in all_users:
            print(f"  {user:<12}", end="")
            for resource_name in resource_names:
                acl = self.resources[resource_name]["acl"]
                if user in acl:
                    perms = acl[user]
                    flags = ""
                    if "read" in perms:
                        flags += "R"
                    if "write" in perms:
                        flags += "W"
                    if "delete" in perms:
                        flags += "D"
                    if "admin" in perms:
                        flags += "A"
                    print(f" {flags:>10}", end="")
                else:
                    print(f" {'---':>10}", end="")
            print()


def demo_mode():
    """デモモード: RBAC/ACLの動作を実演します"""
    print("\n" + "=" * 55)
    print("  【デモモード】アクセス制御の実演")
    print("=" * 55)

    # === RBAC デモ ===
    rbac = RBACSystem()

    print("\n  ◆ RBAC（ロールベースアクセス制御）")
    print("  " + "─" * 50)

    # 全ユーザー一覧
    print("\n  【ユーザー一覧】")
    rbac.display_all_users()

    # 全ロール一覧
    print("\n  【ロール定義】")
    rbac.display_all_roles()

    # アクセスチェックのデモ
    print("\n\n  【アクセスチェックのデモ】")
    test_cases = [
        ("田中太郎", "system:config", "管理者がシステム設定を変更"),
        ("佐藤花子", "file:create", "マネージャーがファイルを作成"),
        ("鈴木一郎", "system:config", "編集者がシステム設定を変更（権限なし）"),
        ("高橋美咲", "file:read", "閲覧者がファイルを読む"),
        ("高橋美咲", "file:delete", "閲覧者がファイルを削除（権限なし）"),
        ("伊藤健二", "system:logs", "監査人がログを確認"),
        ("伊藤健二", "file:update", "編集者兼監査人がファイルを更新"),
    ]

    print(f"\n  {'操作':.<40} {'結果'}")
    print(f"  {'─' * 40} {'─' * 10}")

    for username, permission, description in test_cases:
        allowed = rbac.check_access(username, permission)
        mark = "[OK] 許可" if allowed else "[NG] 拒否"
        print(f"  {description:<40} {mark}")

    # アクセスログ
    print("\n  【アクセスログ】")
    rbac.display_access_log()

    # === ACL デモ ===
    acl = ACLSystem()

    print("\n\n  ◆ ACL（アクセス制御リスト）")
    print("  " + "─" * 50)

    # アクセスマトリックス
    print("\n  【アクセスマトリックス】")
    acl.display_user_access_matrix()

    # ACL チェックのデモ
    print("\n  【ACLによるアクセスチェック】")
    acl_tests = [
        ("佐藤花子", "売上レポート.xlsx", "write", "所有者がファイルに書き込み"),
        ("高橋美咲", "売上レポート.xlsx", "write", "閲覧者がファイルに書き込み"),
        ("鈴木一郎", "経理システム", "read", "経理以外がシステムにアクセス"),
        ("伊藤健二", "経理システム", "delete", "経理担当がデータを削除"),
    ]

    print(f"\n  {'操作':.<40} {'結果'}")
    print(f"  {'─' * 40} {'─' * 15}")

    for username, resource, action, desc in acl_tests:
        allowed, reason = acl.check_access(username, resource, action)
        mark = f"[OK] {reason}" if allowed else f"[NG] {reason}"
        print(f"  {desc:<40} {mark}")


def interactive_mode():
    """対話モード: ユーザーがアクセス制御を体験します"""
    rbac = RBACSystem()
    acl = ACLSystem()

    print("\n" + "=" * 55)
    print("  【対話モード】アクセス制御シミュレータ")
    print("=" * 55)

    while True:
        print("\n  操作を選んでください:")
        print("  ── RBAC（ロールベース）──")
        print("  1. ユーザー一覧を表示")
        print("  2. ロール定義を表示")
        print("  3. ユーザーの詳細情報を表示")
        print("  4. アクセス権限をチェック")
        print("  ── ACL ──")
        print("  5. リソースのACLを表示")
        print("  6. アクセスマトリックスを表示")
        print("  7. ACLでアクセスチェック")
        print("  ── その他 ──")
        print("  8. アクセスログを表示")
        print("  9. メニューに戻る")

        choice = input("\n  選択 (1-9): ").strip()

        if choice == "1":
            rbac.display_all_users()

        elif choice == "2":
            rbac.display_all_roles()

        elif choice == "3":
            print("\n  ユーザー名一覧:", ", ".join(rbac.users.keys()))
            name = input("  ユーザー名を入力: ").strip()
            rbac.display_user_info(name)

        elif choice == "4":
            print("\n  ユーザー名一覧:", ", ".join(rbac.users.keys()))
            name = input("  ユーザー名を入力: ").strip()

            # 権限のカテゴリを表示
            print("  権限カテゴリ: user, file, system, report")
            print("  操作:        create, read, update, delete, config, logs, backup, export")
            perm = input("  権限を入力 (例: file:read): ").strip()

            if name and perm:
                allowed = rbac.check_access(name, perm)
                if allowed:
                    print(f"\n  [OK] {name} は '{perm}' の権限を持っています。")
                else:
                    print(f"\n  [NG] {name} は '{perm}' の権限を持っていません。")

        elif choice == "5":
            print("\n  リソース一覧:", ", ".join(acl.resources.keys()))
            resource = input("  リソース名を入力: ").strip()
            if resource:
                acl.display_resource_acl(resource)
            else:
                acl.display_all_resources()

        elif choice == "6":
            acl.display_user_access_matrix()

        elif choice == "7":
            print("\n  リソース一覧:", ", ".join(acl.resources.keys()))
            resource = input("  リソース名を入力: ").strip()
            name = input("  ユーザー名を入力: ").strip()
            print("  操作: read, write, delete, admin")
            action = input("  操作を入力: ").strip()

            if resource and name and action:
                allowed, reason = acl.check_access(name, resource, action)
                if allowed:
                    print(f"\n  [OK] {reason}: {name} は {resource} に対して '{action}' できます。")
                else:
                    print(f"\n  [NG] {reason}: {name} は {resource} に対して '{action}' できません。")

        elif choice == "8":
            rbac.display_access_log()

        elif choice == "9":
            break
        else:
            print("  ※ 1〜9 の数字を入力してください。")


# --- メインプログラム ---
if __name__ == "__main__":
    print("+" + "=" * 53 + "+")
    print("|        アクセスコントロールシミュレータ             |")
    print("|        〜 RBAC/ACLの仕組みを体験 〜               |")
    print("+" + "=" * 53 + "+")

    # アクセス制御の解説
    explain_access_control()

    while True:
        print("\n  モードを選択してください:")
        print("  1. デモモード（RBAC/ACLの動作を実演）")
        print("  2. 対話モード（自分で操作）")
        print("  3. 終了")

        mode = input("\n  選択 (1-3): ").strip()

        if mode == "1":
            demo_mode()
        elif mode == "2":
            interactive_mode()
        elif mode == "3":
            print("\n  ご利用ありがとうございました！")
            break
        else:
            print("  ※ 1〜3 の数字を入力してください。")
