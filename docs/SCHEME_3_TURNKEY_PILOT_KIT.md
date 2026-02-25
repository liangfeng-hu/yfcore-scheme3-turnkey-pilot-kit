# 本源编译执行器通用宪法（13母律）× GateVector_91 × LSE｜方案三：交钥匙试点包
## Scheme-3: Turnkey Pilot Kit (Reference / Pilot-Ready)

Module: **Origin Compiler-Executor (13 Mother Laws) × GateVector_91 (Gate90/Gate91) × LSE (Meta-Gate)**  
Status: Pilot-Ready (no production keys, no real hardware proof chain)

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

## Links to Scheme-1 / Scheme-2 (Subsets of Scheme-3)
- **Scheme-1 (Materials Only):** [SCHEME_1_MATERIALS_ONLY.md](SCHEME_1_MATERIALS_ONLY.md)
- **Scheme-2 (Runtime Only):** [SCHEME_2_RUNTIME_ONLY.md](SCHEME_2_RUNTIME_ONLY.md)

---

## 1) Architecture Overview (10-minute Proof)
Client  
→ **Gateway Proxy :8080** (judge first, forward only if allowed)  
→ **Sidecar :8787** (Gate90 + Gate91 + LSE → persist AuditCard)  
→ **Upstream Stub :9001** (simulated model backend; reached ONLY on allow)

- Sidecar = the adjudicator (Fail-Closed + CommitUnique needle semantics + audit closure)
- Gateway Proxy = PoC gateway (maps requests to evidence; PoC uses placeholder evidence)
- Upstream Stub = backend simulator (proves “only forward on allow”)

---

## 2) Constitutional Invariants (Non-Negotiable)
1) **GateVectorLen = 91** fixed forever  
2) **Fail-Closed** never weakened: any failure ⇒ ΔΩ=0 ∧ CommitUnique=0 ∧ WorldWriteback=0  
3) **CommitUnique** is the only world-write needle  
4) **No new gates**: upgrades may only replace evidence sources / sealed kernels, never change gate count  
5) **No patch-history as causal parent**: ledger contains only closable, verifiable evidence & witnesses

---

## 3) Two Moats (Why PoC ≠ “Customer can finish the product alone”)
### 3.1 Political / Accountability Barrier inside Enterprises
Large enterprises require security/compliance/legal/architecture sign-off.  
They usually will not put a “forked PoC Python script” into production architecture diagrams or audit reports.  
Production needs vendor-backed **SEALED deliverables + SLA + vulnerability response**.  
Scheme-3 gives customers a safe “prove it works” step, while production responsibility remains with official vendor delivery.

### 3.2 Continuous Attack Surface Evolution (Subscription Reality)
Attacks evolve continuously (today distillation, tomorrow new side-channels, next multi-agent bypass).  
Forking PoC code does not grant customers the ability to rapidly update Gate90/91/LSE criteria, re-seal GateKernelHash, and re-close audit receipts.  
Vendor can ship **monthly/weekly constitutional patches** (no new gates, GateVectorLen=91 fixed). This is the real long-term service value.

---

## 4) PoC Red Lines
1) Header-mode evidence exists for **fast PoC only**.  
2) Production must use a **trusted Evidence Injector**; clients must never control decision headers.  
3) Any Fail-Closed result must persist an AuditCard and remain replayable.  
4) Scheme-3 does not ship production keys, real hardware proof chain, or Gates 1–89 criteria (Enterprise delivery scope).

---

## 5) Quick Start (Two Ways)
### A) Pure Python (no Docker)
From repo root, open 3 terminals:
1) `python reference-impl/python/sidecar_service.py`
2) `python runtime/upstream_stub.py`
3) `python runtime/gateway_proxy.py`

Then run:
- `sh examples/curl_test.sh`
- `python audit/replay.py data/audit.jsonl`

### B) Docker Compose (recommended)
1) `docker compose up -d --build`
2) `sh examples/curl_test.sh`
3) `python audit/replay.py data/audit.jsonl`
4) Exit: `docker compose down` (zero-residue rollback)

---

## 6) Acceptance: Only 3 Things
1) Normal request **ALLOW**  
- HTTP 200  

2) High-risk extraction/distillation **FAIL-CLOSED**  
- HTTP 403  
- clear ReasonCode

3) Audit closure is replayable  
- `data/audit.jsonl` grows  
- replay prints **✅ All PASS (100%)**

---

## 7) Path to Production (No New Gates)
Only allowed direction:
1) Replace PoC evidence with **trusted Evidence Injector**
2) Deliver **SEALED GateKernel v1.0** (Gates 1–89 full criteria)
3) Integrate hardware proof chain (TEE / ZK / energy ledger)
4) Provide SLA + vulnerability response + continuous evolution patches
All without adding gates or changing GateVectorLen=91.
