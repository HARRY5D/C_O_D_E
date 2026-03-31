"""
serve.py — Serve the VoiceAPI frontend on http://localhost:5500
Run: python serve.py  (from the frontend/ directory)
"""
import http.server
import socketserver
import os

PORT = 5500
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class Handler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, fmt, *args):
        # Only log non-200 so the terminal stays clean
        if args[1] not in ('200', '304'):
            super().log_message(fmt, *args)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Frontend: http://localhost:{PORT}/index.html")
    print("Press Ctrl+C to stop.\n")
    httpd.serve_forever()
