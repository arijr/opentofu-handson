# Laboratório 06 — Expressões e recursos dinâmicos (30 min)

## Objetivo

Entender como map, `for_each`, for expression, locais e validações criam uma
quantidade variável de recursos com identidade previsível.

## Conceitos explicados

`for_each` usa chaves nomeadas, que mantêm identidade associada à chave no
state. Com `count`, endereços dependem do índice e reordenação pode associar
índices a itens diferentes. A for expression em `locals.tf` transforma mapa
em nomes. `merge` combina tags, e condicionais podem selecionar valores.

## Pré-requisitos e arquivos envolvidos

Labs 01 e 05. Arquivos: `infra/variables.tf`, `locals.tf`, `main.tf` e
`modules/s3-bucket/main.tf`.

## Passo a passo

No `terraform.tfvars`, use entradas distintas:

```hcl
buckets = {
  artifacts = { purpose = "artefatos" }
  logs      = { purpose = "logs" }
  reports   = { purpose = "relatorios" }
}
```

Execute:

```sh
cd infra
tofu fmt
tofu validate
tofu plan
```

A transformação `for` usada pelo root module é:

```hcl
bucket_names = {
  for key, bucket in var.buckets :
  key => "${var.project_prefix}-${var.environment}-${key}"
}
```

Uma expressão condicional simples pode selecionar um rótulo:

```hcl
environment_label = var.environment == "dev" ? "desenvolvimento" : "outro ambiente"
```

Para comparar com `count` (exemplo conceitual; não adicione ao root junto do
módulo, pois criaria outro bucket):

```hcl
resource "aws_s3_bucket" "count_example" {
  count  = 1
  bucket = "${var.project_prefix}-${var.environment}-count"
}
```

Relacione cada chave aos endereços `module.s3_bucket["chave"]`. Use
`tofu plan -var='buckets={data={purpose="dados"}}'` para testar uma composição
alternativa sem gravá-la no arquivo. Não mantenha chaves duplicadas; um mapa
HCL não pode ter chaves repetidas.

## Resultado esperado e verificação

O plano deve propor uma instância por chave e os nomes derivados dos locals.
Validações rejeitam mapas muito grandes ou chaves fora do padrão.

## Erros comuns

Trocar uma chave não é apenas renomear texto: muda a identidade no state e
pode substituir bucket. `count` não é a melhor escolha para uma coleção cujos
itens têm nomes próprios e devem manter identidade estável.

## Exercício adicional

Escreva uma for expression que produza apenas as chaves das entradas cujo
propósito inclui `logs` e explique o valor resultante.

## Critério de conclusão

Apresentou os endereços baseados em chave e explicou diferença de identidade
entre `for_each` e `count`. **Tempo estimado: 30 min.**
