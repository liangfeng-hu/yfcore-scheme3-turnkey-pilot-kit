# Scheme-2: Runtime Only (Runnable PoC)
Purpose: let engineers run it fast and see the effect.  
Includes Sidecar + Proxy + Stub + Compose + blackbox tests + replay.

## Positioning
PoC only, not a production license. Evidence is simulated; Gates 1–89 are placeholders.

## One-Command (Docker)
1) `docker compose up -d --build`
2) `sh examples/curl_test.sh`
3) `python audit/replay.py data/audit.jsonl`
4) `docker compose down`

Pass: Case1=200, Case2/3=403, Replay=✅ All PASS

## Ports
gateway 8080, sidecar 8787, upstream 9001

## PoC Red Line
Header-mode evidence is PoC-only. Production requires trusted evidence injection.
