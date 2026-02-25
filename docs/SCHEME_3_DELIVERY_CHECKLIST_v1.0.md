# Scheme-3 Delivery Checklist v1.0

## A) Repo structure must exist
- docs/SCHEME_3_TURNKEY_PILOT_KIT.md
- docs/README.md
- docs/pilot-kit.md
- docs/success-metrics.md
- docs/BD_CUSTOMER_TALK_TRACK.md
- docs/SCHEME_3_DELIVERY_CHECKLIST_v1.0.md
- docs/SCHEME_1_MATERIALS_ONLY.md
- docs/SCHEME_2_RUNTIME_ONLY.md
- reference-impl/python/sidecar_service.py
- runtime/gateway_proxy.py
- runtime/upstream_stub.py
- runtime/Dockerfile
- docker-compose.yml
- examples/curl_test.sh
- audit/schema_v1.json
- audit/canonicalization.md
- audit/replay.py
- adapters/envoy-ext-authz.md
- adapters/nginx.md
- scripts/verify_scheme3.sh
- scripts/verify_scheme3.ps1
- .gitignore

## B) Shortest customer acceptance (3 steps)
1) `docker compose up -d --build`
2) `sh examples/curl_test.sh`
3) `python audit/replay.py data/audit.jsonl` → must be ✅ All PASS

## C) Evidence package to share
- terminal screenshots (Case1 allow, Case2/3 fail-closed)
- replay PASS screenshot
- first 20 lines of audit.jsonl (redacted if needed)
- optional screen recording (2–3 minutes)

## D) Production contract appendix suggestions
- boundary statement (pilot vs production)
- deliverables: SEALED GateKernel v1.0 + Evidence Injector + proof chain + SLA
- vulnerability response timeline
- continuous evolution patch cadence
- audit retention & compliance storage
