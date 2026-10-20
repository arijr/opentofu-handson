# Laboratório 05 — Módulos (25 min)

## Objetivo

Identificar como o módulo S3 separa inputs, resource e outputs e como o módulo
raiz o reutiliza.

## Conceitos explicados

`source` aponta para módulo local. Inputs são parâmetros; outputs expõem
resultados. Módulos organizam e reutilizam configuração, mas não são, por si
só, recursos físicos. O módulo raiz deste exercício cria instâncias com
`for_each`.

## Pré-requisitos e arquivos envolvidos

Leia `infra/main.tf` e `infra/modules/s3-bucket/{variables,main,outputs}.tf`.
As referências a `each.value` alimentam os inputs do módulo.

## Passo a passo

No módulo raiz:

```sh
cd infra
tofu init
tofu validate
tofu plan
```

Compare os nomes de argumentos `bucket_name`, `purpose` e `tags` com as
declarações de variáveis. Compare `bucket_name` e `bucket_arn` na interface
outputs do módulo com `infra/outputs.tf`. O código final já chama o módulo;
não mova nem duplique o resource S3.

Para observar reuso, acrescente uma entrada ao mapa `buckets` no seu
`terraform.tfvars` e compare `tofu plan`; o mesmo módulo atenderá a nova chave.
Após revisar, aplique ou descarte a mudança.

## Resultado esperado e verificação

`tofu validate` passa e o plano lista uma instância por chave. Outputs no
módulo raiz agregam as saídas do módulo por chave.

## Erros comuns

Um argumento não declarado em `variables.tf` ou output inexistente resulta em
erro de validação. Não use caminhos de registry: o source é um diretório local.

## Exercício adicional

Adicione uma variável opcional ao módulo com default e documente como ela se
reflete em `tags`.

## Critério de conclusão

Explicou inputs, outputs, source e reuso sem duplicar o resource. **Tempo
estimado: 25 min.**
