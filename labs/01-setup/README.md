# Laboratório 01 — Preparação (20 min)

## Objetivo

Conferir ferramentas, iniciar o Floci local e inicializar os providers do
projeto sem criar recursos.

## Conceitos explicados

Docker executa o emulador; OpenTofu inicializa plugins em `init`. Inicializar
não equivale a aplicar uma infraestrutura. A porta `4566` é o endpoint local
documentado pelo Floci.

## Pré-requisitos e arquivos envolvidos

Docker Compose v2, OpenTofu, Git e curl. AWS CLI é opcional. Arquivos:
`docker-compose.yml`, `infra/versions.tf`, `infra/providers.tf` e
`infra/.terraform.lock.hcl` (criado/atualizado por `tofu init`).

## Passo a passo

Linux/macOS, na raiz:

```sh
./scripts/check-prerequisites.sh
docker compose up -d
docker compose ps
docker compose logs --tail=50 floci
curl -sS -o /dev/null -w 'HTTP %{http_code}\n' http://localhost:4566/
tofu -chdir=infra init
```

PowerShell:

```powershell
.\scripts\check-prerequisites.ps1
docker compose up -d
docker compose ps
docker compose logs --tail=50 floci
Invoke-WebRequest http://localhost:4566/ -UseBasicParsing -TimeoutSec 5
tofu -chdir=infra init
```

O status HTTP da rota raiz apenas demonstra conectividade; não é health check
documentado. `docker compose down` para o container e preserva o volume
persistente `floci-data`. Use `docker compose down -v` para descartá-lo depois
de remover os recursos via OpenTofu.

## Resultado esperado e verificação

`tofu init` informa que inicializou o módulo e instalou `hashicorp/aws`. Confira
que o endpoint em `infra/providers.tf` é local. O comando não executa `apply`.

## Erros comuns

Porta ocupada: confira `docker compose ps` e os logs. Docker indisponível:
inicie Docker Desktop/Engine. Rede indisponível: o primeiro `init` precisa
baixar o provider.

## Exercício adicional

Use `aws s3api list-buckets --endpoint-url http://localhost:4566` com as
credenciais `test` documentadas em [pré-requisitos](../../docs/pre-requisitos.md).

## Critério de conclusão

Pré-requisitos passam, container aparece em execução e `tofu init` termina sem
erro. **Tempo estimado: 20 min.**
