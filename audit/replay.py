import sys
import json
import hashlib

AUDIT_VERSION = "AUDITCARD_V1"
EVIDENCE_VERSION = "EVIDENCE_V1"

GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python audit/replay.py <path_to_audit_jsonl>")
        return 2

    path = sys.argv[1]
    total = 0
    ok = 0
    bad = 0

    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1

            try:
                a = json.loads(line)
            except Exception:
                bad += 1
                continue

            evidence_canon = a.get("evidence_canon", "")
            evidence_hash_expected = _sha256(f"{EVIDENCE_VERSION}|{evidence_canon}")

            ssot_hash = a.get("ssot_hash", "")
            ledger_root = a.get("ledger_root", "")
            req_id = a.get("req_id", "")
            reason_code = a.get("reason_code", "")
            out_level = a.get("out_level", "")
            commit_unique = a.get("commit_unique", 0)
            world_writeback = a.get("world_writeback", 0)

            audit_hash_expected = _sha256(
                f"{AUDIT_VERSION}|{ssot_hash}|{ledger_root}|{req_id}|{reason_code}|{out_level}|{commit_unique}|{world_writeback}|{evidence_hash_expected}"
            )

            evidence_hash_ok = (a.get("evidence_hash") == evidence_hash_expected)
            audit_hash_ok = (a.get("audit_receipt_hash") == audit_hash_expected)

            if evidence_hash_ok and audit_hash_ok:
                ok += 1
            else:
                bad += 1
                print(f"{RED}FAIL{RESET} record #{total} req_id={req_id} evidence_ok={evidence_hash_ok} audit_ok={audit_hash_ok}")

    if bad == 0:
        print(f"{GREEN}✅ All PASS (100%){RESET} total={total}")
        return 0

    print(f"{RED}❌ Replay FAIL{RESET} total={total} pass={ok} fail={bad}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
