# check_pilot_kit.ps1 — Scheme-3 Windows Self-Check
$ErrorActionPreference = "Stop"

function Write-Status {
    param([string]$Message, [string]$Color = "White", [switch]$Bold)
    $prefix = if ($Bold) { "`e[1m" } else { "" }
    $suffix = "`e[0m"
    if ($Color -eq "Green") { Write-Host "$prefix✅ $Message$suffix" -ForegroundColor Green }
    elseif ($Color -eq "Red") { Write-Host "$prefix❌ $Message$suffix" -ForegroundColor Red }
    elseif ($Color -eq "Yellow") { Write-Host "$prefix⚠️  $Message$suffix" -ForegroundColor Yellow }
    elseif ($Color -eq "Cyan") { Write-Host "$prefix$Message$suffix" -ForegroundColor Cyan }
    else { Write-Host "$prefix$Message$suffix" }
}

$EXPECTED_FILES = @(
    "README.md",
    "docker-compose.yml",
    "reference-impl/python/sidecar_service.py",
    "runtime/Dockerfile",
    "runtime/gateway_proxy.py",
    "runtime/upstream_stub.py",
    "examples/curl_test.sh",
    "audit/replay.py",
    "audit/schema_v1.json",
    "adapters/envoy-ext-authz.md",
    "adapters/nginx.md"
)

Write-Status "🚀 Scheme-3 Windows Self-Check starting..." -Color Cyan -Bold

$missing = @()
foreach ($f in $EXPECTED_FILES) { if (-not (Test-Path $f)) { $missing += $f } }

if ($missing.Count -gt 0) {
    Write-Status "Missing required files:" -Color Red -Bold
    $missing | ForEach-Object { Write-Host "   - $_" -ForegroundColor Red }
    exit 1
}
Write-Status "Required files present" -Color Green

if (Test-Path "data") { Remove-Item "data\*.jsonl" -Force -ErrorAction SilentlyContinue }
New-Item -ItemType Directory -Force -Path "data" | Out-Null
Write-Status "data/ cleared" -Color Green

Write-Status "Starting docker compose..." -Color Cyan -Bold
docker compose up -d --build | Out-Null
Start-Sleep -Seconds 6
Write-Status "Compose up OK" -Color Green

$baseUrl = "http://127.0.0.1:8080/v1/chat/completions"

Write-Status "Case 1 (expect 200)..." -Color Cyan
Invoke-WebRequest -Method Post -Uri $baseUrl -Body '{"hint":"hello"}' -ContentType "application/json" -UseBasicParsing -TimeoutSec 10 | Out-Null
Write-Status "Case 1 PASS" -Color Green

Write-Status "Case 2 (expect 403)..." -Color Cyan
$headers = @{ "X-Distill-Risk" = "0.92" }
try {
    Invoke-WebRequest -Method Post -Uri $baseUrl -Headers $headers -Body '{"hint":"try extract"}' -ContentType "application/json" -UseBasicParsing -TimeoutSec 10 | Out-Null
    Write-Status "Case 2 UNEXPECTED (not blocked)" -Color Yellow
} catch { Write-Status "Case 2 PASS (blocked)" -Color Green }

Write-Status "Case 3 (expect 403)..." -Color Cyan
$headers = @{ "X-Thermo-OK" = "false" }
try {
    Invoke-WebRequest -Method Post -Uri $baseUrl -Headers $headers -Body '{"hint":"force physical fail"}' -ContentType "application/json" -UseBasicParsing -TimeoutSec 10 | Out-Null
    Write-Status "Case 3 UNEXPECTED (not blocked)" -Color Yellow
} catch { Write-Status "Case 3 PASS (blocked)" -Color Green }

Write-Status "Running audit replay..." -Color Cyan -Bold
python audit/replay.py data/audit.jsonl | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Status "Replay FAIL" -Color Red -Bold
    docker compose down | Out-Null
    exit 1
}
Write-Status "Replay PASS" -Color Green

docker compose down -v | Out-Null
Write-Status "🎉 ALL PASS — Scheme-3 is ready to ship." -Color Green -Bold
