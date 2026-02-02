import http.server
import socketserver
import os
from pathlib import Path

# 設定端口（避免與 OpenClaw 的默認端口 18789 衝突）
PORT = 8081

# 設定服務器根目錄為 todo-app
WEB_DIR = Path("/workspaces/OpenClaw/todo-app")

class TodoHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

def run_server():
    print(f"Starting Todo List app server at port {PORT}")
    print(f"Serving files from: {WEB_DIR}")
    
    with socketserver.TCPServer(("", PORT), TodoHandler) as httpd:
        print(f"Server running at: http://localhost:{PORT}")
        httpd.serve_forever()

if __name__ == "__main__":
    run_server()