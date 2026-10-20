# Pré-requisitos e preparação

## Ferramentas

- OpenTofu CLI 1.8.x ou superior, abaixo da versão 2.0.
- Docker Engine ou Docker Desktop com Docker Compose v2.
- Git para versionar os exercícios.
- `curl` para a checagem HTTP básica.
- AWS CLI v2 é opcional e serve apenas para consultar o endpoint local.

O provider AWS é baixado pelo `tofu init`; a versão está limitada a `~> 5.100`.
Não é necessário instalar Terraform. Confira instruções atuais de instalação
na [documentação OpenTofu](https://opentofu.org/docs/intro/install/).

Se esta pasta ainda não for um clone Git, inicialize o versionamento após
conferir o `.gitignore`:

```sh
git init
git status --short
```

Versione os arquivos `.tf`, documentação e `infra/.terraform.lock.hcl`; não
adicione state, tfvars locais ou planos.

## Segurança do ambiente

O provider define `http://localhost:4566` explicitamente para S3 e IAM e usa as
credenciais literais de teste `test`. Não adicione `profile` ou credenciais
pessoais à configuração. Não altere os endpoints para AWS. AWS CLI é opcional;
em todo comando deste material, informe `--endpoint-url http://localhost:4566`.

As credenciais de teste não são credenciais AWS válidas e devem ser usadas
somente contra o Floci. Mantenha terminais e scripts livres de perfis AWS reais
durante o minicurso.

## Linux/macOS

Na raiz do projeto:

```sh
./scripts/check-prerequisites.sh
docker compose up -d
docker compose ps
curl -sS -o /dev/null -w 'HTTP %{http_code}\n' http://localhost:4566/
cd infra
tofu init
```

O código HTTP da raiz serve somente para constatar conectividade; não é um
health check oficial do Floci. A primeira inicialização pode levar alguns
instantes enquanto a imagem é baixada. O Compose monta o volume nomeado
`floci-data` com `FLOCI_STORAGE_MODE=persistent` e
`FLOCI_STORAGE_PERSISTENT_PATH=/app/data`, conforme a documentação do Floci.
`docker compose down` preserva o volume; após destruir os recursos do state,
`docker compose down -v` descarta os dados deste projeto.

## Windows PowerShell

Execute a partir da pasta do projeto:

```powershell
.\scripts\check-prerequisites.ps1
docker compose up -d
docker compose ps
Invoke-WebRequest -Uri http://localhost:4566/ -UseBasicParsing -TimeoutSec 5
Set-Location infra
tofu init
```

Se a raiz devolver um status HTTP de erro, isso ainda pode demonstrar que a
porta respondeu; não é confirmação de que uma operação AWS foi aceita. Consulte
os logs do container ou faça a chamada S3 local opcional abaixo.

## Verificação opcional com AWS CLI

Linux/macOS:

```sh
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 \
  aws s3api list-buckets --endpoint-url http://localhost:4566
```

PowerShell:

```powershell
$env:AWS_ACCESS_KEY_ID = "test"
$env:AWS_SECRET_ACCESS_KEY = "test"
$env:AWS_DEFAULT_REGION = "us-east-1"
aws s3api list-buckets --endpoint-url http://localhost:4566
Remove-Item Env:AWS_ACCESS_KEY_ID, Env:AWS_SECRET_ACCESS_KEY, Env:AWS_DEFAULT_REGION
```

O `--endpoint-url` explícito impede que essa chamada use o endpoint público da
AWS. Se os comandos falharem, consulte [troubleshooting](troubleshooting.md).

## Inicializar e conferir

`tofu init` baixa o provider e cria/atualiza `.terraform.lock.hcl`; versione
esse lock file junto com os arquivos `.tf`. Apesar do nome, este é também o
lock file usado pelo OpenTofu. A configuração não usa backend remoto:
state e planos são locais e estão excluídos do Git.

```sh
tofu fmt -recursive
tofu validate
tofu plan
```

Antes de aceitar qualquer plano, procure o endpoint local. Não prossiga caso
apareça uma URL AWS real.
