# docs/README.md — Docs Entry & Customer Self-Troubleshooting

This folder enables customers to self-run Scheme-3 without vendor hands-on operations:
- One-command verification
- 3 blackbox cases
- AuditCard persistence
- Replay determinism PASS
- Common failure triage and recovery

---

## IMPORTANT POSITIONING (MUST READ)
**Scheme-3 = Turnkey Pilot Kit (Reference Implementation)**
- For **2–4 weeks validation only**
- Evidence sources are **PoC simulated** (Header/boolean placeholders); **Gates 1–89 are SEALED placeholders**
- **NOT a production license**. Do **NOT** deploy directly to production.

Enterprise/Production requires:
- Trusted Evidence Injector (client-unforgeable)
- SEALED GateKernel v1.0 (Gates 1–89 full hashes & criteria)
- Hardware proof chain (TEE / ZK / energy-thermo ledger)
- Ops/Compliance/SLA + continuous evolution service

---

## Where to Start
- Full pilot guide: `docs/SCHEME_3_TURNKEY_PILOT_KIT.md`
- Short 2-week sheet: `docs/pilot-kit.md`
- KPI acceptance: `docs/success-metrics.md`
- BD talk track: `docs/BD_CUSTOMER_TALK_TRACK.md`
- Delivery checklist: `docs/SCHEME_3_DELIVERY_CHECKLIST_v1.0.md`

---

## One-Command Verification (Recommended)
### Mac / Linux
From repo root:
```bash
sh scripts/verify_scheme3.sh

Windows PowerShell

From repo root:
powershell -ExecutionPolicy Bypass -File scripts\verify_scheme3.ps1

Pass criteria

sidecar / upstream / gateway health returns ok

Case 1: HTTP 200 (ALLOW)

Case 2/3: HTTP 403 (FAIL-CLOSED, clear ReasonCode)

Replay prints: ✅ All PASS (100%)

Optional: Run Compose from examples/ (Same stack, alternate entry)

Root-level compose is recommended:

docker compose up -d --build

If a customer wants to run via the example compose file:

docker compose -f examples/docker-compose.yml up -d --build

To stop:

docker compose -f examples/docker-compose.yml down -v

Note: The example compose uses ../data for persistence (same audit/ledger folder).

Self-Triage (Most Common Issues → Shortest Fix)
A. Docker / Compose

A1: docker not found

Install and start Docker Desktop, then retry.

A2: docker compose not found

Your Docker is too old (only docker-compose exists).

Fix:

Preferred: upgrade Docker Desktop

Alternative: replace docker compose with docker-compose in scripts.

A3: pull/build times out

Corporate proxy or blocked registry.

Fix: configure Docker proxy/mirror, or ask network team to allow registry access.

B. Port Conflicts (Most Common)

Default ports:

gateway: 8080

sidecar: 8787

upstream: 9001

B1: “port already allocated / address already in use”

Another service is using that port.

Fix: free ports OR change host port mapping in docker-compose.yml.

Check port usage

Mac/Linux: lsof -i :8080 (also 8787 / 9001)

Windows: netstat -ano | findstr :8080 (also 8787 / 9001)

Change ports

In docker-compose.yml, change "8080:8080" to "18080:8080" (host:container)

Then use http://127.0.0.1:18080/health

C. Windows Script Execution / Line Endings

C1: PowerShell blocks script

Use the provided command:

powershell -ExecutionPolicy Bypass -File scripts\verify_scheme3.ps1

C2: /bin/sh^M

CRLF line endings. Fix by converting scripts to LF or run via WSL.

D. “It runs but outputs look wrong”

D1: Case 1 returns 403

Confirm services:

docker compose ps

Check gateway → sidecar connectivity:

curl http://127.0.0.1:8080/health

Logs:

docker compose logs --tail=200 gateway

docker compose logs --tail=200 sidecar

D2: data/audit.jsonl is empty

Request didn’t reach sidecar or data volume not writable.

Check:

ls -la data/

curl http://127.0.0.1:8787/health

D3: replay FAIL

If the audit file was edited, reset PoC state and rerun.

Hard Reset (Fastest Recovery)

docker compose down

delete data/

docker compose up -d --build

rerun verify script

If You Need Vendor Support

Please share:

docker --version

docker compose version (or docker-compose --version)

docker compose ps

docker compose logs --tail=200 sidecar

docker compose logs --tail=200 gateway

first 20 lines of data/audit.jsonl (redact if needed)

::contentReference[oaicite:0]{index=0}
