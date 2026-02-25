#!/bin/sh
set -e

echo "======================================================"
echo "SCHEME-3 Blackbox Test (Gateway -> Sidecar -> Upstream)"
echo "======================================================"
echo ""

echo "[Case 1] Normal request (should ALLOW -> upstream returns 200)"
curl -i -s -X POST "http://127.0.0.1:8080/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{"hint":"hello"}'
echo ""
echo ""

echo "[Case 2] High extraction/distill risk (should FAIL-CLOSED -> 403)"
curl -i -s -X POST "http://127.0.0.1:8080/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-Distill-Risk: 0.92" \
  -d '{"hint":"try extract"}'
echo ""
echo ""

echo "[Case 3] Thermo proof fails (should FAIL-CLOSED -> 403)"
curl -i -s -X POST "http://127.0.0.1:8080/v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "X-Thermo-OK: false" \
  -d '{"hint":"force physical fail"}'
echo ""
echo ""
