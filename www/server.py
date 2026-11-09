#!/usr/bin/env python3
import os
import json
import http.server
import socketserver
import shutil

PORT = int(os.environ.get("PORT", 8099))
WEB_DIR = os.environ.get("WEB_DIR", "/local_apps/build-ledger/www")

# Load Home Assistant add-on options
options = {}
try:
    with open("/data/options.json", "r") as f:
        options = json.load(f)
except Exception:
    pass

SERVER_URL = options.get("server_url", "")
APP_NAME = options.get("app_name", "Build Ledger")
APK_ENABLED = options.get("apk_enabled", False)
APK_PATH = options.get("apk_path", "/local_apps/build-ledger/www/apk/build-ledger.apk")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        # Serve index.html for root
        if self.path == "/":
            self.path = "/index.html"

        # Clean uninstall endpoint
        if self.path == "/api/uninstall":
            data_dir = os.environ.get("DATA_DIR", "/config/build_ledger/data")
            docs_dir = os.environ.get("DOCS_DIR", "/config/build_ledger/docs")
            deleted = []
            if os.path.exists(data_dir):
                shutil.rmtree(data_dir)
                deleted.append("data")
            if os.path.exists(docs_dir):
                shutil.rmtree(docs_dir)
                deleted.append("docs")
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"status": "deleted", "deleted": deleted}).encode())
            return

        return super().do_GET()

if __name__ == "__main__":
    os.chdir(WEB_DIR)
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()