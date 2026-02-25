# Success Metrics — Scheme-3 Turnkey Pilot Kit

## IMPORTANT POSITIONING (MUST READ)
Scheme-3 is a **Pilot / Reference Implementation**:
- For 2–4 weeks validation only
- PoC evidence is simulated (headers/boolean placeholders); Gates 1–89 are SEALED placeholders
- Not a production license

Production requires: trusted Evidence Injector + SEALED GateKernel v1.0 + hardware proof chain + SLA + continuous evolution service.

## PoC vs Production Measurement
- PoC: use simulated/adversarial/replay traffic to prove constitutional correctness and replay determinism.
- Production: use red-team samples and trusted evidence to prove “non-bypassable + signable + continuously updatable”.

---

## 1) Security Effectiveness
- Distillation/extraction block rate ≥ 95% (PoC adversarial samples; production red-team samples)
- High-fidelity output leakage rate = 0% on any FAIL-CLOSED (WorldWriteback=0, CommitUnique=0)
- LSE violation detection = 100% (any layer fracture → RC_LSE_VIOLATION → FAIL-CLOSED)
- ReasonCode coverage = 100% (every failure must emit a clear reason code)

## 2) Usability / False Positives
- Normal request pass rate ≥ 99.5%
- False positive (normal blocked) ≤ 0.5%
- Rollback time ≤ 1 minute (remove hook / take down proxy)

## 3) Performance
- p95 added latency ≤ 80ms (PoC target; production measured)
- p99 added latency ≤ 150ms (PoC target; production measured)

## 4) Auditability (Hard Compliance)
- AuditCard persisted rate = 100%
- Replay determinism = 100% (`audit/replay.py` all pass)
- Canonicalization determinism = 100% (same evidence → same hash → same verdict)

## 5) Success / Fail Threshold
- Success: all core KPIs met + replayable audit report generated
- Pause/Fail: any core KPI not met or integration risk deemed unacceptable; exit with zero residue rollback
