# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Read port from .env or use default
$port = 8001
if (Test-Path .env) {
    $envContent = Get-Content .env
    foreach ($line in $envContent) {
        if ($line -match '^PORT=(\d+)') {
            $port = $matches[1]
        }
    }
}

Write-Host "Starting backend on port $port..."
uvicorn app.main:app --reload --host 127.0.0.1 --port $port