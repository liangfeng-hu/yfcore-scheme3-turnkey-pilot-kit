```markdown
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

---

## 2) Constitutional Invariants (Non-Negotiable)
1) **GateVectorLen = 91** fixed forever  
2) **Fail-Closed** never weakened: any failure ⇒ ΔΩ=0 ∧ CommitUnique=0 ∧ WorldWriteback=0  
3) **CommitUnique** is the only world-write needle  
4) **No new gates**: upgrades may only replace evidence sources / sealed kernels, never change gate count  
5) **No patch-history as causal parent**: ledger contains only closable, verifiable evidence & witnesses

---

## 3) Two Moats
### 3.1 Political / Accountability Barrier inside Enterprises
Production requires signable vendor-backed deliverables (SEALED artifacts + SLA + vulnerability response).  
Forked PoC scripts are rarely acceptable for production compliance.

### 3.2 Continuous Attack Surface Evolution
Attacks evolve continuously; customers cannot sustainably maintain Gate90/91/LSE criteria, re-seal kernels, and re-close receipts at vendor speed.  
Vendor can ship **monthly/weekly constitutional patches** (no new gates, GateVectorLen=91 fixed).

---

## 4) Quick Start (Two Ways)
### A) One-command self-check (recommended)
```bash
python check_pilot_kit_enhanced.py
