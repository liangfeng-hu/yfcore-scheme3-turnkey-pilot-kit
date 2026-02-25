```markdown
# Envoy Ext-Authz Adapter (Scheme-3)

**Goal**: Envoy calls Sidecar before forwarding. Sidecar returns 200 → allow; 403 → Fail-Closed.

**Immutable Constitution**
- `failure_mode_allow` must be **false** (strict Fail-Closed)
- GateVectorLen = 91 fixed forever

## Minimal Working Mode (PoC)
PoC uses Header-mode evidence (for fast validation). Sidecar reads headers like:
- X-Risk-Class
- X-S_EX
- X-IIA-OK, X-Seed-OK, X-Thermo-OK, X-Attest-OK, X-ZK-OK, X-Energy-OK
- X-OutLevel

## Envoy Filter Snippet (Skeleton)
```yaml
- name: envoy.filters.http.ext_authz
  typed_config:
    "@type": type.googleapis.com/envoy.extensions.filters.http.ext_authz.v3.ExtAuthz
    failure_mode_allow: false
    http_service:
      server_uri:
        uri: http://sidecar:8787/v1/adjudicate
        cluster: sidecar_cluster
        timeout: 0.1s
Production Note: never let clients write these headers. Use a gateway-side Evidence Injector.
