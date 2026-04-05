"""
HTTP/HTTPSサンプル04：簡易HTTPサーバー
======================================

学べる内容:
  - Python標準ライブラリでHTTPサーバーを構築
  - リクエストの受信とレスポンスの返却
  - JSON APIの実装
  - ルーティングの基本
  - ステータスコードとヘッダーの設定

実行方法:
  python 04_簡易HTTPサーバー.py

アクセス方法:
  ブラウザで http://localhost:8080 を開く
  または curl http://localhost:8080/api/users
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from urllib.parse import urlparse, parse_qs
from datetime import datetime

# --- 疑似データベース ---
USERS = [
    {"id": 1, "name": "田中太郎", "email": "tanaka@example.com", "role": "admin"},
    {"id": 2, "name": "鈴木花子", "email": "suzuki@example.com", "role": "user"},
    {"id": 3, "name": "佐藤次郎", "email": "sato@example.com", "role": "user"},
]

next_id = 4


class APIHandler(BaseHTTPRequestHandler):
    """シンプルなREST APIハンドラー"""

    def _send_json(self, status_code, data):
        """JSONレスポンスを送信"""
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))

    def _send_html(self, status_code, html):
        """HTMLレスポンスを送信"""
        self.send_response(status_code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def _read_body(self):
        """リクエストボディをJSONとして読み取り"""
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        return json.loads(body.decode("utf-8"))

    def do_GET(self):
        """GETリクエストの処理"""
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        # トップページ
        if path == "/":
            html = """<!DOCTYPE html>
<html><head><title>HTTP学習サーバー</title></head>
<body>
<h1>HTTP学習サーバー</h1>
<h2>利用可能なエンドポイント:</h2>
<ul>
  <li><a href="/api/users">GET /api/users</a> — ユーザー一覧</li>
  <li>GET /api/users/{id} — ユーザー詳細</li>
  <li>POST /api/users — ユーザー作成</li>
  <li>DELETE /api/users/{id} — ユーザー削除</li>
  <li><a href="/api/info">GET /api/info</a> — サーバー情報</li>
  <li><a href="/api/echo?msg=hello">GET /api/echo?msg=hello</a> — エコー</li>
</ul>
<h2>curlでの実行例:</h2>
<pre>
curl http://localhost:8080/api/users
curl http://localhost:8080/api/users/1
curl -X POST http://localhost:8080/api/users -H "Content-Type: application/json" -d '{"name":"新規","email":"new@example.com"}'
curl -X DELETE http://localhost:8080/api/users/1
</pre>
</body></html>"""
            self._send_html(200, html)

        # ユーザー一覧
        elif path == "/api/users":
            self._send_json(200, {"data": USERS, "count": len(USERS)})

        # ユーザー詳細
        elif path.startswith("/api/users/"):
            user_id = path.split("/")[-1]
            if user_id.isdigit():
                user = next((u for u in USERS if u["id"] == int(user_id)), None)
                if user:
                    self._send_json(200, {"data": user})
                else:
                    self._send_json(404, {"error": {"code": "NOT_FOUND", "message": "ユーザーが見つかりません"}})
            else:
                self._send_json(400, {"error": {"code": "INVALID_ID", "message": "IDは数値で指定してください"}})

        # サーバー情報
        elif path == "/api/info":
            self._send_json(200, {
                "server": "HTTP学習サーバー",
                "version": "1.0",
                "timestamp": datetime.now().isoformat(),
                "endpoints": ["/api/users", "/api/info", "/api/echo"],
            })

        # エコー
        elif path == "/api/echo":
            msg = params.get("msg", [""])[0]
            self._send_json(200, {
                "echo": msg,
                "method": "GET",
                "headers": dict(self.headers),
            })

        else:
            self._send_json(404, {"error": {"code": "NOT_FOUND", "message": f"パス '{path}' は存在しません"}})

    def do_POST(self):
        """POSTリクエストの処理"""
        global next_id

        if self.path == "/api/users":
            try:
                body = self._read_body()
                name = body.get("name", "").strip()
                email = body.get("email", "").strip()

                if not name or not email:
                    self._send_json(422, {"error": {"code": "VALIDATION_ERROR", "message": "name と email は必須です"}})
                    return

                new_user = {"id": next_id, "name": name, "email": email, "role": "user"}
                USERS.append(new_user)
                next_id += 1
                self._send_json(201, {"data": new_user})

            except json.JSONDecodeError:
                self._send_json(400, {"error": {"code": "INVALID_JSON", "message": "JSONの形式が不正です"}})
        else:
            self._send_json(404, {"error": {"code": "NOT_FOUND", "message": "エンドポイントが見つかりません"}})

    def do_DELETE(self):
        """DELETEリクエストの処理"""
        if self.path.startswith("/api/users/"):
            user_id = self.path.split("/")[-1]
            if user_id.isdigit():
                user = next((u for u in USERS if u["id"] == int(user_id)), None)
                if user:
                    USERS.remove(user)
                    self.send_response(204)
                    self.end_headers()
                else:
                    self._send_json(404, {"error": {"code": "NOT_FOUND", "message": "ユーザーが見つかりません"}})
            else:
                self._send_json(400, {"error": {"code": "INVALID_ID", "message": "IDは数値で指定してください"}})
        else:
            self._send_json(404, {"error": {"code": "NOT_FOUND", "message": "エンドポイントが見つかりません"}})

    def do_OPTIONS(self):
        """OPTIONSリクエスト（CORS対応）"""
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """ログ出力のカスタマイズ"""
        print(f"  [{datetime.now().strftime('%H:%M:%S')}] {args[0]}")


def main():
    host = "localhost"
    port = 8080

    print("=" * 50)
    print("HTTP学習用 簡易サーバー")
    print("=" * 50)
    print(f"\nサーバー起動: http://{host}:{port}")
    print(f"停止するには Ctrl+C を押してください\n")

    server = HTTPServer((host, port), APIHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nサーバーを停止しました。")
        server.server_close()


if __name__ == "__main__":
    main()
