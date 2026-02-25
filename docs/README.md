# docs/README.md — Docs Entry & Customer Troubleshooting

Start here:
- Full pilot guide: `docs/SCHEME_3_TURNKEY_PILOT_KIT.md`
- KPI acceptance: `docs/success-metrics.md`
- Short pilot sheet: `docs/pilot-kit.md`

One-command check:
- `python check_pilot_kit_enhanced.py`

If you insist on bash/curl blackbox:
- `sh examples/curl_test.sh`

Common issues:
- Port conflicts (8080/8787/9001)
- Old Docker (no `docker compose`)
- Corporate proxy blocks image pulls

Hard reset:
- `docker compose down -v`
- delete `data/`
- `docker compose up -d --build`
