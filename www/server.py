#!/usr/bin/env python3
import os
import http.server
import socketserver

PORT = int(os.environ.get("PORT", 8099))
WEB_DIR = os.environ.get("WEB_DIR", "/app/www")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

if __name__ == "__main__":
    os.chdir(WEB_DIR)
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()