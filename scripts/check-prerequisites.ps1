$ErrorActionPreference = "Stop"
$missing = @()

foreach ($commandName in @("tofu", "docker", "git")) {
    if (-not (Get-Command $commandName -ErrorAction SilentlyContinue)) {
        Write-Host "ERRO: ferramenta ausente: $commandName" -ForegroundColor Red
        $missing += $commandName
    }
}

if (Get-Command docker -ErrorAction SilentlyContinue) {
    docker compose version *> $null
    if ($LASTEXITCODE -ne 0) {
        Write-Host "ERRO: Docker Compose v2 não está disponível." -ForegroundColor Red
        $missing += "docker compose"
    }
}

if ($missing.Count -gt 0) {
    Write-Host "Instale as ferramentas ausentes conforme docs/pre-requisitos.md." -ForegroundColor Red
    exit 1
}

tofu version
git --version
docker compose version
