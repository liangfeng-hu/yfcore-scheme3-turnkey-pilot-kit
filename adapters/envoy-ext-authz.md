# Envoy ext_authz Adapter (Scheme-3)
PoC goal: call Sidecar before forwarding. Sidecar returns:
- 200 → allow
- 403 → fail-closed

Production note:
- Header-mode evidence is PoC-only. Production must use trusted evidence injection.
