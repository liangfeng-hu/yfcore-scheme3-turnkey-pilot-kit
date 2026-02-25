# Pilot Kit (Scheme-3 Short Sheet)
Goal: insert a minimal Sidecar / Gateway Filter in front of one high-value route to prove **Fail-Closed needle gating + replayable audit**.

## Positioning (Short)
- Pilot-only (2–4 weeks). Not a production license.
- PoC evidence is simulated (headers/boolean placeholders); Gates 1–89 are SEALED placeholders.
- Production requires vendor delivery: trusted Evidence Injector + SEALED GateKernel v1.0 + hardware proof chain + SLA + continuous evolution.

## Non-Negotiables
- GateVectorLen=91 fixed
- Fail-Closed never weakened (WorldWriteback=0 on any failure)
- CommitUnique is the only needle
- No new gates (replace evidence, don’t change gate count)

## Fastest Acceptance
1) `docker compose up -d --build`
2) `sh examples/curl_test.sh`
3) `python audit/replay.py data/audit.jsonl` → must be **✅ All PASS**

## Exit
Remove sidecar hook / proxy: zero residue rollback.
