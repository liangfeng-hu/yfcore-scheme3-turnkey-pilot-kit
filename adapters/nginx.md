# Nginx auth_request Adapter (Scheme-3)

PoC goal: use auth_request to call Sidecar before proxying.
- Sidecar returns **200** → allow
- Sidecar returns **403** → fail-closed

Production note:
- Header-mode evidence is PoC-only.
- Production must use a trusted Evidence Injector (clients must not control decision headers).
