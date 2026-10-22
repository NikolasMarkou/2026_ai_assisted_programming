"""Notes service: in-memory notes over HTTP and JSON. Standard library only.

Usage: python3 service.py [--port 8000]
POST /notes, GET /notes, GET /notes/<id>, DELETE /notes/<id>. See spec.md.
"""
import argparse
import itertools
import json
from http.server import BaseHTTPRequestHandler, HTTPServer

NOTES = {}  # id -> text, in creation order
IDS = itertools.count(1)  # an id is never reused after a delete


class Handler(BaseHTTPRequestHandler):
    def send_json(self, status, payload=None):
        body = b"" if payload is None else json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def note_id(self):
        """The id in /notes/<id>, or None when the path is not that shape."""
        parts = self.path.strip("/").split("/")
        if len(parts) == 2 and parts[0] == "notes" and parts[1].isdigit():
            return int(parts[1])
        return None

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        try:
            text = json.loads(self.rfile.read(length) or b"null")["text"]
        except (ValueError, KeyError, TypeError):
            return self.send_json(400, {"error": "body must be {\"text\": string}"})
        if self.path != "/notes" or not isinstance(text, str):
            return self.send_json(400, {"error": "text must be a string"})
        note_id = next(IDS)
        NOTES[note_id] = text
        self.send_json(201, {"id": note_id, "text": text})

    def do_GET(self):
        if self.path == "/notes":
            return self.send_json(200, [{"id": i, "text": t} for i, t in NOTES.items()])
        note_id = self.note_id()
        if note_id in NOTES:
            return self.send_json(200, {"id": note_id, "text": NOTES[note_id]})
        self.send_json(404, {"error": "not found"})

    def do_DELETE(self):
        note_id = self.note_id()
        if note_id in NOTES:
            del NOTES[note_id]
            return self.send_json(204)
        self.send_json(404, {"error": "not found"})

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8000)
    HTTPServer(("127.0.0.1", parser.parse_args().port), Handler).serve_forever()
