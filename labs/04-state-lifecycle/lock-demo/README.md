# Demonstração opcional — Lock nativo do backend S3

Este exercício usa um state remoto **somente no bucket S3 local do Floci**. O
backend padrão do workshop continua local. O objetivo é observar o lockfile
nativo `terraform.tfstate.tflock` e uma segunda execução aguardando a liberação.

> OpenTofu não oferece um parâmetro para adicionar artificialmente uma pausa
> antes de adquirir o lock. `-lock-timeout` define quanto tempo uma execução
> concorrente espera. Para tornar o lock visível, a configuração deste
> exercício mantém o primeiro comando ocupado por 45 segundos **depois** da
> aquisição do lock; outra execução tenta adquiri-lo nesse intervalo.

## Pré-requisitos

- Floci iniciado a partir da raiz do workshop.
- OpenTofu 1.8 ou superior.
- As pastas `bootstrap/` e `hold-lock/` deste exercício.
- Execute todos os comandos OpenTofu indicados aqui. O backend contém endpoint
  local explícito e credenciais de teste; não o redirecione à AWS.

## 1. Criar o bucket de state no Floci

O bucket precisa existir antes de inicializar um backend S3. A configuração
isolada `bootstrap/` usa state local apenas para criar esse bucket:

```sh
tofu -chdir=labs/04-state-lifecycle/lock-demo/bootstrap init
tofu -chdir=labs/04-state-lifecycle/lock-demo/bootstrap fmt
tofu -chdir=labs/04-state-lifecycle/lock-demo/bootstrap validate
tofu -chdir=labs/04-state-lifecycle/lock-demo/bootstrap plan
tofu -chdir=labs/04-state-lifecycle/lock-demo/bootstrap apply
```

Leia e confirme o plano. Ele deve criar somente `tofu-workshop-lock-state` no
Floci. Não execute essa configuração com provider ou endpoint diferentes.

## 2. Inicializar o backend S3 com lockfile

Na raiz do workshop, copie o arquivo de exemplo:

Linux/macOS:

```sh
cp labs/04-state-lifecycle/lock-demo/hold-lock/backend.hcl.example \
   labs/04-state-lifecycle/lock-demo/hold-lock/backend.hcl
```

PowerShell:

```powershell
Copy-Item labs/04-state-lifecycle/lock-demo/hold-lock/backend.hcl.example `
  labs/04-state-lifecycle/lock-demo/hold-lock/backend.hcl
```

O arquivo local é ignorado pelo Git. Confira que `endpoints.s3` é
`http://localhost:4566`, antes de inicializar:

```sh
tofu -chdir=labs/04-state-lifecycle/lock-demo/hold-lock init \
  -backend-config=backend.hcl
```

O backend usa `use_lockfile = true`; não usa DynamoDB. O arquivo `.tflock` é
temporário, criado quando uma operação adquire o lock e removido ao liberá-lo.
Não crie nem edite esse arquivo manualmente. State e lock ficam no endpoint
local informado no backend config.

## 3. Ocupar o lock por 45 segundos

Abra um primeiro terminal na raiz do projeto e force a substituição do recurso
de espera para repetir a demonstração:

```sh
tofu -chdir=labs/04-state-lifecycle/lock-demo/hold-lock apply \
  -replace=time_sleep.lock_holder \
  -lock-timeout=30s
```

Confirme o plano. Durante o `time_sleep`, o comando mantém o lock do backend;
o atraso não faz parte da operação de aquisição em si.

## 4. Observar uma segunda execução concorrente

Enquanto o primeiro terminal ainda espera, execute no segundo:

```sh
tofu -chdir=labs/04-state-lifecycle/lock-demo/hold-lock plan \
  -lock-timeout=60s
```

O segundo processo deve informar que o state está bloqueado e aguardar. Depois
que o primeiro terminar, o lock é liberado e o `plan` pode continuar. Para
demonstrar um timeout curto, opcionalmente repita durante uma nova espera com
`-lock-timeout=5s`; essa execução deverá desistir se o lock continuar ocupado
além do limite.

Enquanto a primeira operação estiver no `time_sleep`, é possível observar os
objetos do bucket:

```sh
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 \
aws s3api list-objects-v2 --bucket tofu-workshop-lock-state \
  --endpoint-url http://localhost:4566 \
  --query 'Contents[].Key'
```

Durante a operação, a resposta inclui `lock-demo/terraform.tfstate.tflock`;
depois que o processo libera o lock, esse objeto desaparece e permanece apenas
o state. No PowerShell, defina primeiro as variáveis de teste e use:

```powershell
$env:AWS_ACCESS_KEY_ID = "test"
$env:AWS_SECRET_ACCESS_KEY = "test"
$env:AWS_DEFAULT_REGION = "us-east-1"
aws s3api list-objects-v2 --bucket tofu-workshop-lock-state `
  --endpoint-url http://localhost:4566 `
  --query 'Contents[].Key'
```

## 5. Inspecionar e limpar

O bucket contém o objeto de state e, durante uma operação, o lockfile. Não
apague o objeto `.tflock` manualmente. Após a operação:

```sh
tofu -chdir=labs/04-state-lifecycle/lock-demo/hold-lock state list
tofu -chdir=labs/04-state-lifecycle/lock-demo/hold-lock destroy
aws s3api delete-object --bucket tofu-workshop-lock-state \
  --key lock-demo/terraform.tfstate \
  --endpoint-url http://localhost:4566
tofu -chdir=labs/04-state-lifecycle/lock-demo/bootstrap destroy
```

PowerShell:

```powershell
aws s3api delete-object --bucket tofu-workshop-lock-state `
  --key lock-demo/terraform.tfstate `
  --endpoint-url http://localhost:4566
tofu -chdir=labs/04-state-lifecycle/lock-demo/bootstrap destroy
```

O state remoto de `hold-lock` guarda apenas o recurso didático `time_sleep`.
Depois do `destroy`, o objeto de state vazio continua no bucket; o comando AWS
CLI acima o remove explicitamente do Floci para permitir destruir o bucket de
backend. Sempre informe `--endpoint-url` como acima. Não destrua o bucket
enquanto o backend remoto ainda estiver sendo utilizado. Para recomeçar, crie
novamente o bucket com `bootstrap/` e rode `init` do backend. Se AWS CLI não
estiver instalado, deixe o bucket no Floci até uma limpeza do volume local.

## Resultado esperado

- O bucket do backend é criado localmente.
- O `apply` segura o lock durante o tempo configurado.
- Um `plan` simultâneo aguarda (ou expira com timeout curto).
- O lock é liberado ao terminar a operação.
- State remoto e bucket são removidos na ordem correta.

## Limitação de compatibilidade

OpenTofu documenta o locking S3 nativo por escrita condicional (`If-None-Match`)
com `use_lockfile = true`. O Floci documenta compatibilidade com backend S3 e
locking DynamoDB. A demonstração foi testada com OpenTofu 1.13.1, AWS Provider
5.100.0, time Provider 0.13.1 e Floci 2.3.0: o objeto `.tflock` apareceu no
bucket durante o apply e um `plan` concorrente aguardou a liberação. Essa
verificação não garante outras combinações de versões. Se `init` ou a aquisição
do lock falhar no Floci, não use o backend em AWS como alternativa: mantenha o
state local do workshop e explique o mecanismo conceitualmente.
