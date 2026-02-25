# Nginx auth_request Adapter (Scheme-3)

**Goal**: Nginx calls Sidecar before proxying. Sidecar returns 200 → allow; 403 → Fail-Closed.

**Key Points**:
- `auth_request` is a sub-request (usually GET). Sidecar supports GET /v1/adjudicate (Header-mode).
- For production, never allow client spoofing of evidence headers (PoC is OK for demo only).

## Minimal Configuration (Skeleton)
```nginx
location /_vbus_check {
    internal;
    proxy_pass http://sidecar:8787/v1/adjudicate;
    proxy_pass_request_body off;
    proxy_set_header Content-Length "";
    proxy_set_header X-Original-URI $request_uri;
    # Forward required evidence headers
}

server {
    location /v1/chat/completions {
        auth_request /_vbus_check;
        error_page 403 = @fail_closed;
        proxy_pass http://upstream;
    }

    location @fail_closed {
        return 403;
    }
}
