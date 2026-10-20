# Roteiro do apresentador — laboratórios

Guia operacional para conduzir os laboratórios depois da apresentação inicial.
Ele complementa os READMEs individuais dos labs com ordem de execução, falas,
comandos, verificações e pontos de decisão para o instrutor.

## Agenda dos encontros

### Hoje — 2h30 no total

| Horário relativo | Atividade | Duração |
|---|---|---:|
| 00:00–00:30 | Apresentação de história e fundamentos | 30 min |
| 00:30–00:50 | Lab 01 — preparação | 20 min |
| 00:50–01:20 | Lab 02 — primeiro recurso | 30 min |
| 01:20–01:50 | Lab 03 — variáveis e outputs | 30 min |
| 01:50–02:30 | Lab 04 — state e ciclo de vida | 40 min |
| **Laboratório hoje** | **Após a apresentação** | **2h** |

### Amanhã — 2h30 de laboratório

| Horário relativo | Atividade | Duração |
|---|---|---:|
| 00:00–00:25 | Lab 05 — módulos | 25 min |
| 00:25–00:55 | Lab 06 — expressões e recursos dinâmicos | 30 min |
| 00:55–01:25 | Lab 07 — recursos e data sources | 30 min |
| 01:25–01:50 | Lab 08 — qualidade e segurança | 25 min |
| 01:50–02:30 | Lab 09 — desafio final | 40 min |

O cronograma preenche exatamente o tempo disponível. Demonstrações extras,
perguntas longas e a versão completa do lock demo devem substituir um exercício
adicional ou ficar para depois da sessão; não reduza a revisão de plano nem a
limpeza para tentar encaixá-las.

## Preparação do instrutor

Faça esta checagem antes da turma entrar. Os comandos abaixo não aplicam nem
destroem recursos.

1. Abra a pasta `opentofu-workshop` no VS Code e deixe visíveis:
   - `docs/apresentacao.pptx`;
   - este roteiro;
   - `labs/`;
   - `infra/`.
2. Garanta que os participantes tenham o mesmo workspace e Docker host nos dois
   encontros. O state é local à pasta da máquina e o Floci persiste dados em um
   volume Docker local.
3. Verifique Docker Compose, OpenTofu, Git e conectividade do endpoint:

   ```sh
   ./scripts/check-prerequisites.sh
   docker compose up -d
   docker compose ps
   docker compose logs --tail=30 floci
   ```

4. Aguarde `healthy` em `docker compose ps`. Inicialize apenas os providers:

   ```sh
   tofu -chdir=infra init
   tofu -chdir=infra fmt -check -recursive
   tofu -chdir=infra validate
   ```

5. Confirme que `infra/providers.tf` aponta S3 e IAM somente para
   `http://localhost:4566`. O provider usa credenciais literais de teste.
   Nunca coloque credenciais AWS reais no ambiente da turma.
6. Não execute `tofu apply` no preparo. A primeira criação é feita junto com os
   alunos para que possam ler o plano antes da confirmação.
7. Garanta que AWS CLI é opcional. Para qualquer chamada AWS CLI demonstrada,
   inclua sempre `--endpoint-url http://localhost:4566` e use somente as
   credenciais de teste.

### Convenções para a condução

- Comandos `tofu -chdir=infra ...` são executados da raiz do workshop. Isso
  evita divergência de diretório entre os participantes.
- Peça aos alunos para acompanhar em duplas, mas cada pessoa executa os
  comandos no próprio workspace/Floci.
- Em cada `plan` ou `apply`, pause para que todos identifiquem endpoint,
  recurso, nome e ação prevista antes de continuar.
- Se o plano mostrar endpoint público da AWS ou algo que não foi discutido,
  **pare**. Não aprove.
- Nunca use `tofu state rm`, edição manual do state ou `docker compose down -v`
  como atalho para resolver um erro.
- Use tempos de relógio como limite. Ao final de cada bloco, prefira seguir com
  o grupo e deixar o exercício adicional como tarefa.

## Hoje — roteiro dos 2h de laboratórios

### Lab 01 — Preparação (00:30–00:50, 20 min)

**Objetivo do apresentador:** todos veem o Floci pronto e OpenTofu inicializado,
sem recurso provisionado ainda.

#### 00:30–00:33 — Enquadramento e segurança

Diga:

> “Nos próximos exercícios, o AWS Provider será usado somente como cliente de
> APIs compatíveis do Floci. O endereço deve ser localhost:4566. `init` baixa
> plugins e prepara o diretório; não cria buckets.”

Peça para abrir um terminal na raiz do workshop. Faça todos confirmarem que
estão na pasta correta antes dos comandos.

#### 00:33–00:38 — Verificação das ferramentas

Linux/macOS:

```sh
./scripts/check-prerequisites.sh
```

Windows PowerShell:

```powershell
.\scripts\check-prerequisites.ps1
```

Resultado esperado: versões de OpenTofu, Docker Compose e Git são exibidas.
AWS CLI não é necessária para seguir o laboratório.

Se faltar uma ferramenta, deixe o participante acompanhar a projeção em dupla
enquanto resolve o pré-requisito. Não use o tempo da turma para instalar
ferramentas em várias máquinas.

#### 00:38–00:45 — Inicializar e verificar Floci

```sh
docker compose up -d
docker compose ps
docker compose logs --tail=30 floci
```

Fale que `up -d` inicia o emulador em background e não cria recursos de
infraestrutura. Aguarde o status `healthy`. Se ainda estiver iniciando,
repita `docker compose ps` e consulte os logs.

Opcional, apenas para confirmar que uma operação S3 responde. Bash:

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

Resultado esperado: lista vazia ou buckets que o instrutor já identificou
como parte desta oficina. Se AWS CLI não estiver instalada, pule essa chamada.

#### 00:45–00:50 — Inicializar OpenTofu

```sh
tofu -chdir=infra init
tofu -chdir=infra fmt
tofu -chdir=infra validate
```

Explique:

- `init`: instala o AWS Provider fixado e inicializa o módulo;
- `fmt`: padroniza HCL;
- `validate`: verifica a configuração, mas não aplica recursos.

**Transição:** “Agora temos o cliente pronto. Vamos descrever um único bucket
e inspecionar o plano antes de pedir qualquer mudança ao Floci.”

### Lab 02 — Primeiro recurso (00:50–01:20, 30 min)

**Objetivo do apresentador:** cada aluno observa um plano de criação, cria
um bucket no Floci, inspeciona um output e destrói esse recurso temporário.

#### 00:50–00:55 — Leitura guiada do HCL

Abra `infra/providers.tf`, `infra/main.tf` e
`infra/modules/s3-bucket/main.tf`. Mostre:

1. Provider `aws` direcionado aos endpoints locais.
2. Módulo raiz que chama o módulo de S3.
3. Resource `aws_s3_bucket.this` que descreve o bucket.

Diga que os arquivos da oficina já contêm a configuração final. O foco do
exercício é seguir os valores e observar o comportamento, sem criar um segundo
resource manual e duplicar a infraestrutura.

#### 00:55–01:03 — Formatar, validar e planejar

```sh
tofu -chdir=infra fmt
tofu -chdir=infra validate
tofu -chdir=infra plan \
  -var='buckets={primeiro={purpose="primeiro recurso"}}'
```

Peça que localizem no plano:

- a ação `create`;
- o endereço `module.s3_bucket["primeiro"].aws_s3_bucket.this`;
- o nome `tofu-workshop-dev-primeiro`;
- o output `local_endpoint` com `http://localhost:4566`.

O nome pode variar se o aluno tiver alterado o prefixo/ambiente. Reforce:
`plan` mostra uma proposta e ainda não cria o bucket.

#### 01:03–01:10 — Aplicar e inspecionar

```sh
tofu -chdir=infra apply \
  -var='buckets={primeiro={purpose="primeiro recurso"}}'
tofu -chdir=infra output
tofu -chdir=infra state list
```

Peça que confirmem a lista de ações novamente e digitem `yes` somente após
identificar o plano correto. Mostre que agora há um endereço no state e um
output com o nome do bucket.

#### 01:10–01:17 — Destruir o recurso temporário

```sh
tofu -chdir=infra destroy \
  -var='buckets={primeiro={purpose="primeiro recurso"}}'
```

Revise o plano de destroy antes do `yes`. Explique que `destroy` é uma operação
com efeito real no ambiente-alvo — neste exercício, somente o Floci local.
Confirme que o bucket temporário foi removido.

#### 01:17–01:20 — Fechamento

Pergunte: “Qual etapa apenas descreve a mudança e qual efetivamente a executa?”
Resposta esperada: `plan` propõe; `apply` executa após aprovação.

**Transição:** “O próximo passo é parar de passar valores na linha de comando e
dar nomes e metadados aos recursos por variáveis.”

### Lab 03 — Variáveis e outputs (01:20–01:50, 30 min)

**Objetivo do apresentador:** substituir o bucket descartável por dois buckets
com nome e tag derivados de variáveis comuns; manter esses recursos até amanhã.

#### 01:20–01:25 — Criar valores locais

Na raiz:

Linux/macOS:

```sh
cp infra/terraform.tfvars.example infra/terraform.tfvars
```

PowerShell:

```powershell
Copy-Item infra/terraform.tfvars.example infra/terraform.tfvars
```

Abra `infra/terraform.tfvars` no editor. Mostre `project_prefix`,
`environment`, `aws_region`, `aws_endpoint` e as chaves `artifacts` e `logs`.
O arquivo local está no `.gitignore`; o exemplo segue versionado.

#### 01:25–01:32 — Relacionar variáveis, locals, tags e outputs

Mostre, nesta ordem:

1. `infra/variables.tf`: tipos, valores padrão e validações;
2. `infra/locals.tf`: nomes compostos e tags comuns;
3. `infra/modules/s3-bucket/main.tf`: tag `Purpose` combinada às tags comuns;
4. `infra/outputs.tf`: mapas de nomes e ARNs.

Peça aos alunos para prever o nome antes de abrir o plan:
`tofu-workshop-dev-artifacts` e `tofu-workshop-dev-logs`.

#### 01:32–01:38 — Validar valores e revisar o plano

```sh
tofu -chdir=infra fmt
tofu -chdir=infra validate
tofu -chdir=infra plan
```

Resultado esperado: dois buckets a criar. Faça os alunos verificarem nome,
tags e endpoint. Não prossiga se o plano incluir algo inesperado.

Para demonstrar a validação sem aplicar, opcionalmente rode:

```sh
tofu -chdir=infra plan -var='aws_region=us-west-2'
```

O comando deve falhar pela validação que fixa `us-east-1`. Retorne ao plano
normal antes do apply.

#### 01:38–01:46 — Aplicar e ler outputs

```sh
tofu -chdir=infra apply
tofu -chdir=infra output bucket_names
tofu -chdir=infra output bucket_arns
tofu -chdir=infra state list
```

Leia o plano proposto pelo apply e confirme. Resultado: dois endereços sob
`module.s3_bucket`, nomes e ARNs com as chaves `artifacts` e `logs`.

#### 01:46–01:50 — Fechar sem destruir

Diga explicitamente:

> “Vamos manter esses dois buckets no Floci e o state local nesta pasta. Amanhã
> usaremos um data source para consultar um bucket existente. Não rode `destroy`
> hoje e não remova o volume Docker.”

Se a turma alterou `terraform.tfvars`, anote quais chaves e prefixo foram
usados; os mesmos valores devem continuar amanhã. Não precisa versionar esse
arquivo local.

**Transição:** “Temos configuração e recursos. Agora vamos observar como o
OpenTofu registra a relação entre eles e como uma proposta de mudança aparece.”

### Lab 04 — State e ciclo de vida (01:50–02:30, 40 min)

**Objetivo do apresentador:** alunos inspecionam state, comparam alteração
planejada e configuração vigente e entendem drift sem editar state.

#### 01:50–02:00 — Inspecionar state e configuração

```sh
tofu -chdir=infra state list
tofu -chdir=infra state show \
  'module.s3_bucket["artifacts"].aws_s3_bucket.this'
tofu -chdir=infra show
```

Se a chave for diferente, copiem um endereço retornado por `state list`.
Explique:

- endereço é a identidade do recurso na configuração;
- state mapeia endereço para atributos observados pelo provider;
- state local pode conter valores sensíveis e não deve ir para Git;
- state não é backup nem substituto dos arquivos HCL.

#### 02:00–02:10 — Plano sem mudança e refresh

```sh
tofu -chdir=infra plan
tofu -chdir=infra plan -refresh-only
```

Resultado esperado: não há mudanças, desde que ninguém tenha alterado os
recursos/configuração. Explique que o provider consulta a API e atualiza sua
visão; drift só existe quando há diferença observável entre a infraestrutura e
o que a configuração/state esperam.

#### 02:10–02:20 — Simular uma mudança de configuração sem aplicar

Para evitar editar arquivos que serão usados amanhã, passe uma variável somente
neste comando:

```sh
tofu -chdir=infra plan -var='environment=qa'
tofu -chdir=infra plan
```

O primeiro plan deve propor nomes novos e substituição dos buckets; não
aplique. O segundo volta à configuração `dev` e deve apresentar no-op. Explique
que uma variável muda a configuração desejada, não renomeia recursos por
magia. O plano é o lugar para perceber impacto antes de aplicar.

#### 02:20–02:27 — Reforçar segurança e apresentar lock

Recapitule que execuções simultâneas sobre o mesmo state precisam de
coordenação. O state local padrão é apropriado para a oficina individual, não
para compartilhamento por cópia entre pessoas.

Se o instrutor preparou as pastas do
[lock demo](../labs/04-state-lifecycle/lock-demo/README.md), demonstre no
projetor (opcional): enquanto o `apply` segura o lock por 45 segundos, rode um
`plan` no segundo terminal. O backend S3 desse exercício aponta ao Floci. Não
é necessário que todos inicializem e limpem o backend durante a sessão de hoje.
Deixe a limpeza do bucket/state remoto da demonstração para depois da aula e
siga a ordem descrita no README do lock demo.

Se o demo não estiver pré-inicializado, explique o ciclo de lock sem executar
setup: o comando concorrente espera; `-lock-timeout` limita essa espera.
Reserve a demonstração completa para depois da aula.

#### 02:27–02:30 — Preparar a continuação

Confirme:

```sh
tofu -chdir=infra state list
docker compose ps
```

Oriente os alunos a:

- manter a mesma pasta/workspace e máquina;
- não remover `infra/terraform.tfstate`;
- não executar `docker compose down -v`;
- se parar Floci, usar `docker compose down` sem `-v`, que preserva o volume.

### Estado esperado ao encerrar hoje

- Floci está rodando (ou foi parado sem apagar o volume).
- `infra/terraform.tfvars` contém as chaves dos buckets de cada participante.
- State local registra pelo menos `artifacts` e `logs`.
- O volume `floci-data` mantém os mesmos recursos para amanhã.
- Não há operação pendente de `apply` ou `destroy`.

Se state ou recursos foram removidos por engano, amanhã recrie o ambiente com:

```sh
docker compose up -d
tofu -chdir=infra init
tofu -chdir=infra apply
```

Revise o plano antes de confirmar.

## Amanhã — roteiro dos 2h30 de laboratórios

### Abertura e retomada (integrada aos 5 primeiros minutos do Lab 05)

Pergunte o que foi preservado do encontro anterior. Na raiz, cada aluno roda:

```sh
docker compose up -d
docker compose ps
tofu -chdir=infra init
tofu -chdir=infra state list
tofu -chdir=infra output bucket_names
```

Se os recursos não aparecerem no state, mas Floci continua com os buckets,
não aplique às cegas. Primeiro verifique se é a mesma pasta. Para uma turma que
precise recuperar rapidamente, aplique a configuração atual e confirme o
plano; isso recria somente o que estiver faltando.

### Lab 05 — Módulos (00:00–00:25, 25 min)

**Objetivo do apresentador:** explicar os módulos existentes, sua interface e
mostrar que um mesmo módulo pode atender diferentes chaves.

#### 00:00–00:05 — Retomar o ambiente

Use a checagem de abertura acima. Se algum participante perdeu a pasta, pare
antes de prosseguir e recupere os buckets no Floci conforme o state disponível.

#### 00:05–00:13 — Ler a interface do módulo

Abra:

- `infra/main.tf`: `source`, `for_each` e argumentos;
- `infra/modules/s3-bucket/variables.tf`: inputs;
- `infra/modules/s3-bucket/main.tf`: resource;
- `infra/modules/s3-bucket/outputs.tf`: valores retornados;
- `infra/outputs.tf`: agregação no módulo raiz.

Diga que `infra/` é o módulo raiz e `modules/s3-bucket/` é filho. O valor
passado em `bucket_name` e o mapa passado em `tags` compõem a interface.

#### 00:13–00:20 — Rastrear um valor

Escolha a chave `artifacts` e trace no quadro:

`var.buckets` → `local.bucket_names` → `module.s3_bucket[each.key]` →
`var.bucket_name` → `aws_s3_bucket.this` → output `bucket_name`.

Pergunte ao grupo quais inputs e outputs são necessários para manter o módulo
reutilizável. Reforce que não se deve duplicar o resource no root module.

#### 00:20–00:25 — Verificar e transicionar

```sh
tofu -chdir=infra validate
tofu -chdir=infra plan
```

Resultado esperado: configuração válida e sem mudança. Diga que o próximo
exercício usa novas chaves para revelar o efeito de `for_each`.

### Lab 06 — Expressões e recursos dinâmicos (00:25–00:55, 30 min)

**Objetivo do apresentador:** adicionar um terceiro bucket, comparar
`for_each`/`count` e explicar identidade e validação.

#### 00:25–00:32 — Adicionar uma chave

Edite `infra/terraform.tfvars` e acrescente:

```hcl
  reports = {
    purpose = "relatorios do laboratorio"
  }
```

Ela deve ficar dentro do mapa `buckets`. Não altere `project_prefix`,
`environment` nem `aws_endpoint`.

#### 00:32–00:40 — Format, validate e plan

```sh
tofu -chdir=infra fmt
tofu -chdir=infra validate
tofu -chdir=infra plan
```

Resultado: uma criação adicional com endereço
`module.s3_bucket["reports"]`. Peça para localizar a expressão `for` em
`infra/locals.tf`, que deriva os nomes. Explique que as chaves nomeadas de
`for_each` preservam identidade por item; índices de `count` estão associados
à posição e podem causar churn ao reordenar listas.

#### 00:40–00:48 — Aplicar a nova instância

```sh
tofu -chdir=infra apply
tofu -chdir=infra state list
tofu -chdir=infra output bucket_names
```

Confirme uma criação. Peça para relacionar as três chaves do state com o mapa
em HCL.

#### 00:48–00:55 — Validar uma chave inválida sem aplicar

```sh
tofu -chdir=infra plan \
  -var='buckets={INVALIDA={purpose="teste"}}'
```

Resultado esperado: falha de validação de input. Explique a expressão
condicional e a for expression documentadas no lab, sem adicionar um recurso
`count` à configuração executável. Volte ao plano normal se houver tempo.

### Lab 07 — Recursos e data sources (00:55–01:25, 30 min)

**Objetivo do apresentador:** mostrar consulta real ao S3 local e comparar
data source com resource sem incluir IAM como dependência do curso.

#### 00:55–01:00 — Enquadrar a diferença

Diga:

> “Um resource representa algo que esta configuração cria/gerencia. Um data
> source consulta algo que já existe. O recurso precisa estar no Floci antes da
> consulta.”

Confirme que o mapa contém `artifacts` e que o state registra o bucket.

#### 01:00–01:10 — Criar consulta temporária

Crie `infra/data_source.tf` no editor com:

```hcl
data "aws_s3_bucket" "existing" {
  bucket = "${var.project_prefix}-${var.environment}-artifacts"
}

output "existing_bucket_from_data_source" {
  description = "Bucket consultado pelo data source."
  value       = data.aws_s3_bucket.existing.id
}
```

Explique que a consulta usa variáveis para montar o nome e não declara um
segundo bucket.

#### 01:10–01:18 — Consultar o Floci

```sh
tofu -chdir=infra fmt
tofu -chdir=infra validate
tofu -chdir=infra plan
```

Resultado esperado: o data source lê o bucket existente; nenhum resource novo
é criado. A leitura deve apresentar `existing_bucket_from_data_source` no plan.
Se a consulta falhar, confirme nome, endpoint e existência do bucket antes de
tentar de novo.

#### 01:18–01:22 — Comparar e limpar o arquivo temporário

Compare `data.aws_s3_bucket.existing.id` com
`module.s3_bucket["artifacts"].bucket_name`. Remova `infra/data_source.tf` no
editor e confirme que não faz mais parte do próximo plan. Não deixe output
temporário nos arquivos da oficina.

#### 01:22–01:25 — IAM opcional

Floci documenta operações IAM, porém não faça o restante do laboratório
depender delas. O módulo `infra/modules/iam-policy` gera JSON local; ele não
cria policy AWS. Explique essa diferença e siga sem configurar IAM.

### Lab 08 — Qualidade e segurança (01:25–01:50, 25 min)

**Objetivo do apresentador:** transformar formatação, validação, lock file,
revisão de plano e state em uma checklist repetível.

#### 01:25–01:30 — Rodar verificações

```sh
tofu -chdir=infra fmt -check -recursive
tofu -chdir=infra validate
tofu -chdir=infra plan
```

Não aplique mudanças nesta etapa. Se o data source temporário permaneceu, pare
e peça que o removam antes.

#### 01:30–01:38 — Revisão de segurança com o grupo

Abra `.gitignore`, `infra/.terraform.lock.hcl` e `infra/providers.tf`. Peça que
apontem:

- state, backups, `.terraform/`, tfvars local e planos excluídos do Git;
- lock file de providers versionado;
- endpoint local explicitamente configurado;
- credenciais `test`, sem perfil AWS.

Explique que `sensitive = true` mascara certas exibições, mas não criptografa
state. State pode conter dados sensíveis e exige proteção.

#### 01:38–01:45 — State remoto e locking

Explique conceitualmente o propósito de backend remoto e locking para
colaboração. A configuração principal da turma mantém backend local. Se desejar
ver a mecânica real, o lock demo fica separado e usa backend S3 **no Floci**:
`labs/04-state-lifecycle/lock-demo/README.md`. Não redirecione para AWS.

#### 01:45–01:50 — Preparar desafio e limpeza

Confirme que o plano atual está compreendido. Explique que o próximo exercício
começa com a configuração limpa, e que todos os buckets do desafio serão
removidos ao final.

### Lab 09 — Desafio final (01:50–02:30, 40 min)

**Objetivo do apresentador:** deixar alunos construir, aplicar, verificar e
destruir pelo menos dois buckets via `for_each` e módulo reutilizável.

#### 01:50–01:56 — Definir o desafio e limpar os recursos anteriores

Leia os seis critérios de avaliação do
[README do desafio](../labs/09-challenge/README.md). A turma começa o desafio
sem recursos anteriores. Revise o plano e confirme:

```sh
tofu -chdir=infra destroy
tofu -chdir=infra state list
```

Só confirme `yes` depois de verificar que todos entendem que isso remove os
recursos do state local no Floci. A configuração HCL e state vazio permanecem.

#### 01:56–02:05 — Planejar a solução

Peça aos participantes para conferirem `infra/terraform.tfvars`. Para uma
solução rápida, mantenham duas chaves válidas — `artifacts` e `logs` — e as
finalidades diferentes. O prefixo e o ambiente devem permanecer válidos.

Perguntas orientadoras:

- Qual bloco cria uma instância por chave?
- Onde as tags comuns são definidas?
- Qual output permite confirmar os nomes?

#### 02:05–02:15 — Revisar, formatar e aplicar

```sh
tofu -chdir=infra fmt -check -recursive
tofu -chdir=infra validate
tofu -chdir=infra plan
tofu -chdir=infra apply
```

Não aceite que pulem o plan. O resultado precisa mostrar pelo menos dois
resources S3 através do módulo. A confirmação do apply é deliberada e local ao
Floci.

#### 02:15–02:22 — Verificar outputs e state

```sh
tofu -chdir=infra output bucket_names
tofu -chdir=infra output bucket_arns
tofu -chdir=infra state list
```

Se AWS CLI estiver instalada, listar buckets é opcional; sempre use endpoint
explícito:

```sh
AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test AWS_DEFAULT_REGION=us-east-1 \
  aws s3api list-buckets --endpoint-url http://localhost:4566
```

#### 02:22–02:28 — Limpar o desafio

```sh
tofu -chdir=infra destroy
tofu -chdir=infra state list
```

Revise o plano de destroy e confirme. A listagem de state deve ficar vazia.
Se foi usado AWS CLI, confirme que os buckets do desafio não aparecem mais.

#### 02:28–02:30 — Fechamento

Peça a cada dupla uma frase sobre o aprendizado: identidade estável,
dependência, plan, state ou segurança. Informe que um output de contagem ou um
terceiro bucket é exercício extra, fora dos 40 minutos.

## Recuperação rápida de problemas

| Sintoma | Ação do apresentador |
|---|---|
| Docker não conecta | Confirmar que o Engine/Desktop iniciou; consultar `docker compose ps` e `docker compose logs --tail=50 floci`. |
| Porta 4566 ocupada | Identificar qual serviço está usando a porta. Não apontar provider a endpoints externos. |
| `tofu init` falha | Verificar rede e proxy; preservar `.terraform.lock.hcl`; tentar novamente após serviço disponível. |
| Bucket não aparece no plan | Confirmar pasta raiz, `terraform.tfvars`, chaves e endereço do Floci. |
| Data source não encontra bucket | Verificar que `artifacts` existe com prefixo/ambiente atuais e que Floci preservou o volume. |
| O plano propõe muitas substituições | Não aplicar. Verificar variáveis, chaves renomeadas e diferenças de ambiente. |
| State local ausente | Não apagar recursos nem usar `state rm`. Confirmar se é a mesma pasta; recuperar com o instrutor antes de seguir. |
| Aluno sem AWS CLI | Prosseguir usando outputs, state e plano; AWS CLI é opcional. |

Mais detalhes e comandos de recuperação estão em
[docs/troubleshooting.md](troubleshooting.md).
