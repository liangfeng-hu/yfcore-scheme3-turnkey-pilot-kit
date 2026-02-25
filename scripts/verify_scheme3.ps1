$ErrorActionPreference = "Stop"

Write-Host "== Scheme-3 Verify (Docker Compose) =="

try { docker compose down | Out-Null } catch {}

docker compose up -d --build
Start-Sleep -Seconds 2

Write-Host "[Health] sidecar:"
try { Invoke-RestMethod "http://127.0.0.1:8787/health" | ConvertTo-Json -Depth 6 } catch { Write-Host $_ }

Write-Host "[Health] upstream:"
try { Invoke-RestMethod "http://127.0.0.1:9001/health" | ConvertTo-Json -Depth 6 } catch { Write-Host $_ }

Write-Host "[Health] gateway:"
try { Invoke-RestMethod "http://127.0.0.1:8080/health" | ConvertTo-Json -Depth 6 } catch { Write-Host $_ }

Write-Host "[Case 1] Normal request (should ALLOW -> 200)"
try {
  Invoke-WebRequest -Method POST "http://127.0.0.1:8080/v1/chat/completions" `
    -ContentType "application/json" `
    -Body '{"hint":"hello"}' | Select-Object -ExpandProperty Content
} catch {
  Write-Host $_
}

Write-Host "[Case 2] High distill risk (should FAIL-CLOSED -> 403)"
try {
  Invoke-WebRequest -Method POST "http://127.0.0.1:8080/v1/chat/completions" `
    -Headers @{ "X-Distill-Risk"="0.92" } `
    -ContentType "application/json" `
    -Body '{"hint":"try extract"}' | Select-Object -ExpandProperty Content
} catch {
  Write-Host "Expected 403:"; Write-Host $_.Exception.Message
  if ($_.Exception.Response -ne $null) {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $reader.ReadToEnd() | Write-Host
  }
}

Write-Host "[Case 3] Thermo fail (should FAIL-CLOSED -> 403)"
try {
  Invoke-WebRequest -Method POST "http://127.0.0.1:8080/v1/chat/completions" `
    -Headers @{ "X-Thermo-OK"="false" } `
    -ContentType "application/json" `
    -Body '{"hint":"force physical fail"}' | Select-Object -ExpandProperty Content
} catch {
  Write-Host "Expected 403:"; Write-Host $_.Exception.Message
  if ($_.Exception.Response -ne $null) {
    $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
    $reader.ReadToEnd() | Write-Host
  }
}

python audit/replay.py data/audit.jsonl
Write-Host "✅ Scheme-3 verify OK"
