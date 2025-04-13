import json
import random
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        from urllib.parse import urlparse, parse_qs

        query = parse_qs(urlparse(self.path).query)
        uid = query.get("uid", [None])[0]

        if not uid:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing UID")
            return

        try:
            with open("token_ind.json", "r") as f:
                data = json.load(f)
                tokens = data.get("tokens", [])

            if not tokens:
                raise ValueError("No tokens found")

            token = random.choice(tokens)

            response = {
                "uid": uid,
                "token": token,
                "status": "Token Fetched Successfully"
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error: {str(e)}".encode())