# BD / Sales Talk Track — Scheme-3

## 30-second pitch (Exec)
We add a sidecar needle gate in front of one high-value route. Pass → allow. Fail → fail-closed + replayable audit. No model retraining, zero residue rollback.

## Key line for Security/Compliance/Legal
Pilot kit is for evaluation only. Production needs vendor-backed SEALED deliverables + SLA + vulnerability response + continuous evolution.

## Key line for Architecture
Two integration modes:
1) fastest: gateway proxy (judge-then-forward)
2) native: Envoy ext_authz / Nginx auth_request
Acceptance is simple: ALLOW vs FAIL-CLOSED + AuditCard persistence + replay PASS.

## FAQ: “Can we just fork your PoC and run in prod?”
Answer:
You may freely run the pilot kit for evaluation, but it is not a production license. PoC evidence is simulated and Gates 1–89 are placeholders. Production requires signable SEALED artifacts, trusted evidence injection, hardware proof chain, SLA, and ongoing security updates—otherwise accountability and patch velocity become a serious risk.

## Procurement summary
PoC: self-run in 10 minutes, measurable KPIs, zero residue rollback  
Production: vendor SEALED kernel + SLA + vulnerability response + continuous evolution subscription
