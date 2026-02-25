# Canonicalization Rules — Scheme-3
Goal: same evidence → same canonical form → same hash → same verdict, replayable.

1) Canonical JSON
- sort keys: true
- separators: (",", ":") (no spaces)
- encoding: UTF-8
- ensure_ascii: false

2) evidence_hash
evidence_hash = SHA256("EVIDENCE_V1|" + evidence_canon)

3) audit_receipt_hash
audit_receipt_hash = SHA256(
  "AUDITCARD_V1|{ssot_hash}|{ledger_root}|{req_id}|{reason_code}|{out_level}|{commit_unique}|{world_writeback}|{evidence_hash}"
)

Notes:
- PoC allows placeholder roots but they must be inside receipt_roots and closed by hash.
- Production replaces placeholders with SEALED kernel hashes and real proof chain.
