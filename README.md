# Scheme-3: Turnkey Pilot Kit (Reference Implementation)
**Origin Compiler-Executor (13 Mother Laws) × GateVector_91 (Gate90/Gate91) × LSE (Meta-Gate)**  
Goal: let enterprise customers prove **Fail-Closed needle gating + persisted AuditCards + replayable determinism** in ~10 minutes.

![Scheme-3 CI](https://github.com/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit/actions/workflows/scheme3-ci.yml/badge.svg)
![Repo Size](https://img.shields.io/github/repo-size/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit)
![Last Commit](https://img.shields.io/github/last-commit/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Status](https://img.shields.io/badge/Status-Pilot%20Only-orange)

---

## IMPORTANT POSITIONING (MUST READ)
**This repository is a Turnkey Pilot Kit (Reference Implementation).**
- For **2–4 weeks technical validation and value proof only**
- Evidence sources are **PoC simulated** (header/boolean placeholders); **Gates 1–89 are SEALED placeholders**
- **NOT a production license**. Do **NOT** deploy directly to production.

**Enterprise/Production** must include:
- A **trusted Evidence Injector** (client-unforgeable)
- **SEALED GateKernel v1.0** (full hashes & criteria for Gates 1–89)
- **Hardware proof chain** (TEE attestation / ZK verification / energy-thermo ledger)
- Formal **Ops / Compliance / SLA** + continuous evolution service

Customers may freely run this pilot kit for evaluation, but production deployment must be delivered through official vendor delivery.

---

## One-Command Self-Check (Recommended)
### Cross-platform (no bash/curl required)
```bash
python check_pilot_kit_enhanced.py

Windows PowerShell (fallback)
.\check_pilot_kit.ps1

Pass criteria

Required files present ✅

Docker compose stack starts ✅

3 blackbox cases: 1×ALLOW (200) + 2×FAIL-CLOSED (403) ✅

audit/replay.py prints ✅ All PASS (100%) ✅

Architecture (PoC shape)
Client
 → Gateway Proxy (8080)  (judge first, forward only if allowed)
          ↓
     Sidecar (8787)      (Gate90 + Gate91 + LSE → AuditCard persisted)
          ↓
   Upstream Stub (9001)  (reached ONLY on allow)
Quick Start (Manual)
docker compose up -d --build
sh examples/curl_test.sh
python audit/replay.py data/audit.jsonl
docker compose down -v
Optional: run via example compose:
docker compose -f examples/docker-compose.yml up -d --build
docker compose -f examples/docker-compose.yml down -v

Docs

Full pilot guide: docs/SCHEME_3_TURNKEY_PILOT_KIT.md

Customer troubleshooting: docs/README.md

2-week pilot sheet: docs/pilot-kit.md

KPI acceptance: docs/success-metrics.md

Scheme subsets (optional):

Scheme-1 (materials only): docs/SCHEME_1_MATERIALS_ONLY.md

Scheme-2 (runtime only): docs/SCHEME_2_RUNTIME_ONLY.md

PoC Red Lines (Production MUST change)

Header-mode evidence exists for fast PoC only.

Production must use a trusted Evidence Injector; clients must never control decision headers.

Any failure must remain Fail-Closed: WorldWriteback=0, CommitUnique=0, and AuditCards must be persisted & replayable.

