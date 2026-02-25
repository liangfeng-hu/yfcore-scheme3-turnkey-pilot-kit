# Origin Compiler-Executor General Constitution (13 Mother Laws) × GateVector_91 × LSE  
## Scheme-3: Turnkey Pilot Kit (Reference Implementation)

**Origin Compiler-Executor (13 Mother Laws) × GateVector_91 (Gates 90/91) × LSE (0th Meta-Gate)**  
**Goal**: Enable enterprise customers to verify **Fail-Closed Needle-Eye + Replayable Audit + CommitUnique as the only World Writeback** in **under 10 minutes**.

---

## 🚨 IMPORTANT POSITIONING STATEMENT (Please Read First)

**This repository = Turnkey Pilot Kit (Reference Implementation)**  
- For **2–4 week technical validation and value proof only**  
- Evidence sources are **PoC simulation** (Header/boolean placeholders). Gates 1–89 are **SEALED placeholders**  
- **NOT a production license**. **Strictly prohibited for production use**

**Enterprise/Production version MUST include**:
- Trusted Evidence Injector (client cannot spoof)
- SEALED GateKernel v1.0 (full hash + judgment for Gates 1–89)
- Real hardware proof chain (TEE attestation / ZKP / thermodynamic ledger)
- Official operations, compliance, SLA and continuous evolution service

Customers may freely run this pilot kit for acceptance, but production deployment must go through official delivery.

---

![GitHub last commit](https://img.shields.io/github/last-commit/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit)
![GitHub repo size](https://img.shields.io/github/repo-size/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

---

## 🔥 One-Click Self-Check + PoC Validation (Recommended)

### Mac / Linux / Windows (Recommended Enhanced Version)
```bash
python check_pilot_kit_enhanced.py     # Colorful output + full one-click verification

Windows PowerShell (Alternative)
.\check_pilot_kit.ps1

Architecture (PoC Form)
Client
 → Gateway Proxy (8080) → Judge first → Forward only if allowed
          ↓
     Sidecar (8787) → Gate90 + Gate91 + LSE → AuditCard persisted
          ↓
   Upstream Stub (9001) (only reached on ALLOW)
Core Deliverables








































DirectoryFilePurposereference-impl/python/sidecar_service.pyCore Judgment Engine (Gate90/91 + LSE full implementation)runtime/gateway_proxy.py / upstream_stub.py / DockerfileJudge-then-forward + simulated modelexamples/curl_test.sh / docker-compose.ymlBlack-box test script + one-click trioaudit/replay.py / schema_v1.jsonReplay verification tool + fixed schemaadapters/envoy-ext-authz.md / nginx.mdProduction gateway integration guidesdocs/SCHEME_3_TURNKEY_PILOT_KIT.md etc.Enterprise pilot guide + KPI

Quick Start (Docker Recommended)
docker compose up -d --build
bash examples/curl_test.sh
python audit/replay.py data/audit.jsonl   # Must be 100% PASS
Zero-residue rollback: docker compose down — no changes to your model main path.
Contact us for the production SEALED GateKernel + real evidence chain injector.
Repository: https://github.com/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit
