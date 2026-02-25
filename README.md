# Scheme-3 Turnkey Pilot Kit (Reference Implementation)
**Origin Compiler-Executor (13 Mother Laws) × GateVector_91 (Gate90/Gate91) × LSE (Meta-Gate)**  
Goal: let enterprise customers prove **Fail-Closed needle gating + auditable write path + replayable determinism** in **~10 minutes**.

---

## IMPORTANT POSITIONING (MUST READ)
**Scheme-3 = Turnkey Pilot Kit (Reference Implementation)**
- For **2–4 weeks technical validation and value proof only**
- Evidence sources are **PoC simulated** (Header/boolean placeholders) and **Gates 1–89 are SEALED placeholders**
- **NOT a production license**. Do **NOT** deploy directly to production.

**Enterprise/Production** must include:
- A **trusted Evidence Injector** (client-unforgeable)
- **SEALED GateKernel v1.0** (full hashes & criteria for Gates 1–89)
- **Hardware proof chain** (TEE attestation / ZK verification / energy-thermo ledger)
- Formal **Ops / Compliance / SLA** + ongoing evolution service

Customers may freely run this Pilot Kit for evaluation, but production deployment must be delivered through official vendor delivery.

---

## One-Command PoC Verification (Recommended)
### Mac / Linux
```bash
sh scripts/verify_scheme3.sh

Windows PowerShell
powershell -ExecutionPolicy Bypass -File scripts\verify_scheme3.ps1

Pass criteria

Case 1: HTTP 200 (ALLOW)

Case 2/3: HTTP 403 (FAIL-CLOSED, clear ReasonCode)

Replay: ✅ All PASS (100%)

Troubleshooting (Customer Self-Check)

Please read first:

docs/README.md

Architecture (PoC shape)

Client
→ Gateway Proxy :8080 (judge first, forward only if allowed)
→ Sidecar :8787 (Gate90 + Gate91 + LSE → AuditCard persisted)
→ Upstream Stub :9001 (simulated model backend; reached ONLY on allow)

Relationship of the 3 Schemes

Externally, recommend sending only Scheme-3.
Scheme-1/2 are subsets of Scheme-3.

Scheme-3 (recommended single external entry): docs/SCHEME_3_TURNKEY_PILOT_KIT.md

Scheme-1 (materials only): docs/SCHEME_1_MATERIALS_ONLY.md

Scheme-2 (runtime only): docs/SCHEME_2_RUNTIME_ONLY.md

PoC Red Lines (Production MUST change)

Header-mode evidence is for fast PoC only.

Production evidence must be injected by a trusted gateway-side Evidence Injector; clients must never control decision headers.

Any failure must remain Fail-Closed: WorldWriteback=0, CommitUnique=0, and AuditCard must be persisted & replayable.

Key Paths

docs/SCHEME_3_TURNKEY_PILOT_KIT.md — full enterprise pilot guide

docs/README.md — customer self-troubleshooting

docs/pilot-kit.md — short 2-week pilot sheet

docs/success-metrics.md — KPI and acceptance

reference-impl/python/sidecar_service.py — Sidecar core (Gate90/Gate91/LSE)

runtime/gateway_proxy.py — judge-then-forward proxy

runtime/upstream_stub.py — simulated backend

examples/curl_test.sh — 3 blackbox cases

audit/replay.py — determinism replay check

adapters/envoy-ext-authz.md / adapters/nginx.md — gateway integration notes

