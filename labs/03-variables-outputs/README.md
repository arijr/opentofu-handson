# Laboratório 03 — Variáveis e outputs (30 min)

## Objetivo

Parametrizar nomes e tags sem editar lógica de recursos e expor informações
úteis por outputs.

## Conceitos explicados

`variables.tf` define tipo, default e validação. `locals.tf` deriva nomes e tags
comuns. Outputs apresentam dados calculados pelos módulos. O arquivo
`terraform.tfvars.example` é um exemplo versionável, não é carregado
automaticamente por seu sufixo `.example`.

## Pré-requisitos e arquivos envolvidos

Labs 01 e 02. Leia `infra/variables.tf`, `infra/locals.tf`,
`infra/outputs.tf` e `infra/terraform.tfvars.example`.

## Passo a passo

Na raiz do projeto, crie sua cópia local do exemplo (Linux/macOS):

```sh
cp infra/terraform.tfvars.example infra/terraform.tfvars
```

PowerShell:

```powershell
Copy-Item infra/terraform.tfvars.example infra/terraform.tfvars
```

Edite `project_prefix`, `environment` e as chaves do mapa `buckets` para
valores válidos. O `terraform.tfvars` é ignorado pelo Git. Em seguida:

```sh
tofu fmt
tofu validate
tofu plan
tofu apply
tofu output bucket_names
tofu output bucket_arns
```

Verifique que os nomes contêm prefixo, ambiente e chave; as tags são comuns
e incluem `Purpose` por bucket. Para comparação sem arquivo:
`tofu plan -var='project_prefix=curso-exemplo'`.

## Resultado esperado e verificação

`tofu output` mostra um mapa de nomes e ARNs dos buckets. Variáveis inválidas
falham na validação, antes de qualquer apply.

## Erros comuns

Não edite o arquivo de exemplo esperando que seja carregado. Use
`terraform.tfvars` ou `-var`. Prefixo e chaves precisam obedecer às validações.

## Exercício adicional

Mude `environment` de `dev` para `test` e examine se o nome induz uma
substituição. Não aplique se não pretende criar essa mudança.

## Critério de conclusão

Validou variáveis, aplicou uma configuração parametrizada e leu ambos os
outputs. **Tempo estimado: 30 min.**
