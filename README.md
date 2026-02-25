# Scheme-3: Turnkey Pilot Kit (Reference Implementation)
**Origin Compiler-Executor (13 Mother Laws) × GateVector_91 (Gates 90/91) × LSE (0th Meta-Gate)**  
Goal: Enable enterprise customers to verify **Fail-Closed Needle-Eye + Replayable Audit + CommitUnique as the only World Writeback** in **under 10 minutes**.

![Scheme-3 CI](https://github.com/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit/actions/workflows/scheme3-ci.yml/badge.svg)
![GitHub last commit](https://img.shields.io/github/last-commit/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit)
![GitHub repo size](https://img.shields.io/github/repo-size/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![Status](https://img.shields.io/badge/Status-Pilot%20Only-orange)

---

## 🚨 IMPORTANT POSITIONING STATEMENT (Please Read First)

**This repository = Turnkey Pilot Kit (Reference Implementation)**  
- For **2–4 week** technical validation and value proof only  
- Evidence sources are **PoC simulation** (header/boolean placeholders). Gates 1–89 are **SEALED placeholders**  
- **NOT a production license**. **Strictly prohibited for production use**

**Enterprise/Production version MUST include:**
- Trusted Evidence Injector (client cannot spoof)
- SEALED GateKernel v1.0 (full hash + judgment for Gates 1–89)
- Real hardware proof chain (TEE attestation / ZKP / thermodynamic ledger)
- Official operations, compliance, SLA and continuous evolution service

Customers may freely run this pilot kit for acceptance, but production deployment must go through official delivery.

---

## 🔥 One-Click Self-Check + PoC Validation (Recommended)

### Mac / Linux / Windows (Enhanced Version)
```bash
python check_pilot_kit_enhanced.py

Windows PowerShell (Alternative)
.\check_pilot_kit.ps1

Pass criteria

Case 1: ALLOW (HTTP 200)

Case 2/3: FAIL-CLOSED (HTTP 403)

Replay: audit/replay.py prints ✅ All PASS (100%)

Architecture (PoC Form)
Client
 → Gateway Proxy (8080) → Judge first → Forward only if allowed
          ↓
     Sidecar (8787) → Gate90 + Gate91 + LSE → AuditCard persisted
          ↓
   Upstream Stub (9001) (only reached on ALLOW)
Core Deliverables
| Directory                | File(s)                                                               | Purpose                                                        |
| ------------------------ | --------------------------------------------------------------------- | -------------------------------------------------------------- |
| `reference-impl/python/` | `sidecar_service.py`                                                  | **Core Judgment Engine** (Gate90/91 + LSE full implementation) |
| `runtime/`               | `gateway_proxy.py`, `upstream_stub.py`, `Dockerfile`                  | Judge-then-forward gateway + simulated model backend           |
| `examples/`              | `curl_test.sh`, `docker-compose.yml`                                  | Black-box test script + example compose entry                  |
| `audit/`                 | `replay.py`, `schema_v1.json`, `canonicalization.md`                  | Replay verification + fixed schema + canonical rules           |
| `adapters/`              | `envoy-ext-authz.md`, `nginx.md`                                      | Gateway integration guides (Envoy/Nginx)                       |
| `docs/`                  | `SCHEME_3_TURNKEY_PILOT_KIT.md`, `pilot-kit.md`, `success-metrics.md` | Enterprise pilot guide + KPI + acceptance criteria             |

Quick Start (Docker Recommended)
docker compose up -d --build
bash examples/curl_test.sh
python audit/replay.py data/audit.jsonl   # Must be 100% PASS

Zero-residue rollback:
docker compose down -v

Scheme Relationship (Optional Subsets)

Scheme-3 (this repo is the recommended external entry)

Scheme-1: Materials Only (docs-only subset) → docs/SCHEME_1_MATERIALS_ONLY.md

Scheme-2: Runtime Only (engineering-only subset) → docs/SCHEME_2_RUNTIME_ONLY.md

Contact

Contact us for the production SEALED GateKernel + real evidence-chain injector + SLA & continuous evolution.

Repository: [yfcore-scheme3-turnkey-pilot-kit](https://github.com/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit)
