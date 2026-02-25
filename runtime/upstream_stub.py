import json
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse


def _now_ms() -> int:
    return int(time.time() * 1000)


class StubHandler(BaseHTTPRequestHandler):
    server_version = "UpstreamStub/1.0"

    def _json(self, status: int, obj: dict) -> None:
        body = (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if urlparse(self.path).path == "/health":
            return self._json(200, {"ok": True, "service": "upstream_stub", "ts_ms": _now_ms()})
        return self._json(404, {"error": "not found"})

    def do_POST(self):
        path = urlparse(self.path).path
        if path not in ("/v1/chat/completions", "/completion", "/"):
            return self._json(404, {"error": "not found"})

        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length > 0 else b"{}"
        try:
            req = json.loads(raw.decode("utf-8"))
        except Exception:
            req = {}

        hint = req.get("hint")
        if hint is None and isinstance(req.get("messages"), list) and req["messages"]:
            hint = req["messages"][-1].get("content")

        content = "Hello from upstream stub. (Simulated model backend.)"
        if hint:
            content += " | echo_hint=" + str(hint)[:80]

        return self._json(200, {
            "id": f"stub_{_now_ms()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": "upstream_stub",
            "choices": [
                {"index": 0, "message": {"role": "assistant", "content": content}, "finish_reason": "stop"}
            ],
        })


def main():
    httpd = ThreadingHTTPServer(("0.0.0.0", 9001), StubHandler)
    print("Upstream Stub listening on http://127.0.0.1:9001")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


if __name__ == "__main__":
    main()
