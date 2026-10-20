# Laboratório 02 — Primeiro recurso (30 min)

## Objetivo

Entender provider, resource, formato declarativo e ciclo plan/apply/destroy
criando um bucket apenas no Floci.

## Conceitos explicados

O provider AWS envia chamadas S3 para o endpoint local. O bloco
`aws_s3_bucket` descreve o resultado desejado. `plan` antecipa operações;
`apply` executa após confirmação. O state registra a relação entre endereço
OpenTofu e bucket do emulador.

## Pré-requisitos e arquivos envolvidos

Conclua o lab 01. Leia `infra/providers.tf`, `infra/main.tf` e
`infra/modules/s3-bucket/main.tf`. A configuração cumulativa final chama esse
módulo para cada entrada de `buckets`.

## Passo a passo

Para a primeira aplicação, use um bucket apenas:

```sh
cd infra
tofu init
tofu fmt
tofu validate
tofu plan -var='buckets={primeiro={purpose="primeiro recurso"}}'
```

Leia o plano: confirme que a única criação é `aws_s3_bucket` no módulo. Depois:

```sh
tofu apply -var='buckets={primeiro={purpose="primeiro recurso"}}'
tofu output
tofu destroy -var='buckets={primeiro={purpose="primeiro recurso"}}'
```

Responda `yes` somente após revisar o plano de cada operação. O parâmetro
`-var` é temporário e não modifica os arquivos.

## Resultado esperado e verificação

O apply cria um bucket no Floci e apresenta output `bucket_names`. Destroy
remove o bucket. Opcional: `aws s3api list-buckets --endpoint-url
http://localhost:4566` lista o estado atual do serviço local.

## Erros comuns

Não execute fora de `infra` sem `-chdir`. Provider inicializado antes do Floci?
Confira `docker compose ps`. Plano mostra muitos recursos? Pare e leia-o antes
de confirmar.

## Exercício adicional

Altere apenas o propósito do bucket e observe o plano. Nem toda mudança de
metadados implica recriação; o plano é a fonte para o que o provider fará.

## Critério de conclusão

Executou fmt, validate, plan, apply e destroy usando somente Floci e viu o
bucket aparecer e desaparecer. **Tempo estimado: 30 min.**
