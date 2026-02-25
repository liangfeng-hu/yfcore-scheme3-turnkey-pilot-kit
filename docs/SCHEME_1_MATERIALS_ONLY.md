# Scheme-1: Materials Only (Docs / Acceptance / KPI)
Purpose: a signable package for internal approval (security/compliance/legal/architecture/procurement).  
No runnable code included.

## Positioning
This is not a production license and not a production deliverable.  
Production requires vendor delivery: trusted Evidence Injector + SEALED GateKernel v1.0 + hardware proof chain + SLA + continuous evolution.

## Executive One-Liner
We do not touch model weights or the main chain. We add a sidecar needle gate: pass → allow, fail → fail-closed + replayable audit.

## Scope (2–4 weeks)
- Gate exactly one high-value route first
- Sidecar integration without retraining
- Zero-residue rollback

## Invariants
- GateVectorLen=91 fixed
- Fail-Closed never weakened
- CommitUnique is the only needle
- No new gates (replace evidence sources only)

## KPIs (Summary)
- Distillation/extraction block rate ≥ 95%
- False positive ≤ 0.5%
- AuditCard persisted rate = 100%
- Replay determinism = 100%
- p95 added latency ≤ 80ms (PoC target)

## Exit
Remove hook / proxy; main chain remains clean.

## Why Vendor Delivery Matters
Enterprise production requires signable artifacts: SEALED deliverables + SLA + vulnerability response + continuous evolution.
