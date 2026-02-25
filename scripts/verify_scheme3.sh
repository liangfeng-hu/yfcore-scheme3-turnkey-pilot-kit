#!/bin/sh
set -e

echo "== Scheme-3 Verify (Docker Compose) =="

docker compose down >/dev/null 2>&1 || true
docker compose up -d --build

sleep 2

echo "[Health] sidecar:"
curl -s http://127.0.0.1:8787/health || true
echo ""
echo "[Health] upstream:"
curl -s http://127.0.0.1:9001/health || true
echo ""
echo "[Health] gateway:"
curl -s http://127.0.0.1:8080/health || true
echo ""

sh examples/curl_test.sh
python audit/replay.py data/audit.jsonl

echo "✅ Scheme-3 verify OK"
