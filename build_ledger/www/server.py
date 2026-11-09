#!/usr/bin/env python3
import os
import json
import http.server
import socketserver
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("PORT", 8099))
WEB_DIR = os.environ.get("WEB_DIR", "/app/www")
DATA_DIR = "/config/build_ledger/data"

os.makedirs(DATA_DIR, exist_ok=True)

def safe_user(u):
    cleaned = "".join(c for c in (u or "default") if c.isalnum() or c in ("-", "_", ".", "@"))
    return cleaned or "default"

def vault_path(user):
    return os.path.join(DATA_DIR, f"vault_{safe_user(user)}.json")

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=WEB_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, PUT, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type, X-User, X-Auth")
        super().end_headers()

    def send_json(self, status, payload):
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/ping":
            return self.send_json(200, {"ok": True})

        if path == "/api/kdf":
            qs = parse_qs(parsed.query)
            user = qs.get("user", [""])[0]
            vp = vault_path(user)
            if not os.path.exists(vp):
                return self.send_json(200, {"rev": 0})
            with open(vp, "r", encoding="utf-8") as f:
                data = json.load(f)
            v = data.get("vault", {})
            return self.send_json(200, {
                "rev": data.get("rev", 0),
                "salt": v.get("salt"),
                "iter": v.get("iter")
            })

        if path == "/api/vault":
            user = self.headers.get("X-User", "")
            auth = self.headers.get("X-Auth", "")
            vp = vault_path(user)
            if not os.path.exists(vp):
                return self.send_json(404, {"error": "not found"})
            with open(vp, "r", encoding="utf-8") as f:
                data = json.load(f)
            if data.get("auth") and auth and data["auth"] != auth:
                return self.send_json(403, {"error": "unauthorized"})
            out = dict(data.get("vault", {}))
            out["rev"] = data.get("rev", 0)
            return self.send_json(200, out)

        return super().do_GET()

    def do_PUT(self):
        parsed = urlparse(self.path)
        if parsed.path != "/api/vault":
            return self.send_json(404, {"error": "not found"})

        user = self.headers.get("X-User", "")
        auth = self.headers.get("X-Auth", "")
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8")
        payload = json.loads(raw)

        base_rev = payload.get("baseRev", 0)
        vault = payload.get("vault")
        vp = vault_path(user)

        current_rev = 0
        if os.path.exists(vp):
            with open(vp, "r", encoding="utf-8") as f:
                existing = json.load(f)
            if existing.get("auth") and auth and existing["auth"] != auth:
                return self.send_json(403, {"error": "unauthorized"})
            current_rev = existing.get("rev", 0)
            if base_rev != current_rev:
                return self.send_json(409, {"error": "conflict", "serverRev": current_rev})

        new_rev = current_rev + 1
        with open(vp, "w", encoding="utf-8") as f:
            json.dump({"rev": new_rev, "auth": auth, "vault": vault}, f)

        return self.send_json(200, {"ok": True, "rev": new_rev})

if __name__ == "__main__":
    os.chdir(WEB_DIR)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving Build Ledger on port {PORT}")
        httpd.serve_forever()
