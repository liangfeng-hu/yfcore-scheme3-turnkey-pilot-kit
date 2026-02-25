<image-card alt="GitHub repo size" src="https://img.shields.io/github/repo-size/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit" ></image-card>

# Scheme-3 Turnkey Pilot Kit (Reference Implementation)
**Origin Compiler-Executor (13 Mother Laws) × GateVector_91 (Gate90/Gate91) × LSE (Meta-Gate)**  
Goal: let enterprise customers prove **Fail-Closed needle gating + auditable write path + replayable determinism** in **~10 minutes**.

![Scheme-3 CI](https://github.com/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit/actions/workflows/scheme3-ci.yml/badge.svg)
![Repo Size](https://img.shields.io/github/repo-size/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit)
![Last Commit](https://img.shields.io/github/last-commit/liangfeng-hu/yfcore-scheme3-turnkey-pilot-kit)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)

---

## IMPORTANT POSITIONING (MUST READ)
**Scheme-3 = Turnkey Pilot Kit (Reference Implementation)**
- For **2–4 weeks validation and value proof only**
- Evidence sources are **PoC simulated** (Header/boolean placeholders); **Gates 1–89 are SEALED placeholders**
- **NOT a production license**. Do **NOT** deploy directly to production.

**Enterprise/Production** must include:
- Trusted Evidence Injector (client-unforgeable)
- SEALED GateKernel v1.0 (Gates 1–89 full hashes & criteria)
- Hardware proof chain (TEE / ZK / energy-thermo ledger)
- Ops / Compliance / SLA + continuous evolution service

Customers may freely run this Pilot Kit for evaluation, but production deployment must be delivered through official vendor delivery.

---

## One-Command PoC Verification (Recommended)
### Mac / Linux
```bash
sh scripts/verify_scheme3.sh
