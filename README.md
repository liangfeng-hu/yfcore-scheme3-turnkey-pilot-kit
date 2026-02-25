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
