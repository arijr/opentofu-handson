# Laboratório 09 — Desafio final (40 min)

## Objetivo

Aplicar variáveis, tags, `for_each`, módulo reutilizável, outputs, revisão de
plano e limpeza completa.

## Conceitos explicados

O módulo S3 é chamado uma vez por chave do mapa; nome e propósito variam por
instância. As tags comuns vêm dos locals. Outputs agregam nomes e ARNs.

## Pré-requisitos e arquivos envolvidos

Labs 01–08, Floci ativo e OpenTofu inicializado. Arquivos: `infra/*.tf`,
`infra/modules/s3-bucket/` e `infra/terraform.tfvars.example`.

## Passo a passo

Copie `terraform.tfvars.example` para `infra/terraform.tfvars` e configure
pelo menos duas chaves de bucket. Use prefixo válido e propósito para cada
uma. Depois:

```sh
cd infra
tofu fmt -check -recursive
tofu validate
tofu plan
```

Revise nomes/endpoints e aplique:

```sh
tofu apply
tofu output bucket_names
tofu output bucket_arns
tofu state list
aws s3api list-buckets --endpoint-url http://localhost:4566
```

AWS CLI é opcional; configure apenas as credenciais de teste conforme
`docs/pre-requisitos.md`. Para limpar:

```sh
tofu destroy
tofu state list
```

Confirme o plano do destroy e verifique a lista local. `tofu state list` sem
endereços e listagem sem os buckets do exercício confirmam a limpeza.

## Critérios de avaliação

- Dois ou mais buckets gerados do mapa via `for_each`.
- Reuso do módulo S3, sem duplicação do resource.
- Variáveis validadas e tags comuns.
- Outputs informativos, formato/validação/plano executados.
- Plano revisado antes do apply.
- Recursos destruídos e ausência confirmada no Floci.

## Solução de referência — instrutor

A solução detalhada está separada em
[SOLUCAO-INSTRUTOR.md](SOLUCAO-INSTRUTOR.md), identificada como material do
instrutor. A configuração final em `infra/` é executável e
`infra/terraform.tfvars.example` declara dois buckets. Para a turma, avalie a
solução do aluno a partir dos critérios acima, não por igualdade textual.

## Erros comuns

Nome de bucket inválido, chave renomeada que causa substituição, provider não
inicializado ou Floci parado. Reveja o plano e os guias antes de confirmar.

## Exercício adicional

Adicione um terceiro bucket e escreva um output que informe quantos buckets
estão configurados.

## Critério de conclusão

Todos os itens da rubrica passaram, o output comprovou as instâncias e o
destroy removeu recursos do state e do Floci. **Tempo estimado: 40 min.**
