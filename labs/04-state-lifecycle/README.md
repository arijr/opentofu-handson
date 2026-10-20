# Laboratório 04 — State e ciclo de vida (40 min)

## Objetivo

Inspecionar state e configuração, acompanhar um plano de mudança e destruir
recursos de forma controlada.

## Conceitos explicados

O state local mapeia endereços aos objetos gerenciados e pode conter dados
sensíveis. A configuração descreve intenção; state não é configuração nem
backup. O provider observa a API para identificar diferenças. Drift significa
diferença entre configuração/state gerenciado e infraestrutura observada.

## Pré-requisitos e arquivos envolvidos

Conclua labs 01–03 e tenha recursos de teste criados. Arquivos: `.tf` e os
arquivos locais `terraform.tfstate`/`terraform.tfstate.backup` (não versionar).

## Passo a passo

Na pasta `infra`:

```sh
tofu state list
tofu state show 'module.s3_bucket["artifacts"].aws_s3_bucket.this'
tofu show
tofu plan
```

O endereço depende das chaves presentes em `buckets`. Se estiver usando chave
diferente, copie o endereço retornado por `tofu state list`.

Faça uma pequena alteração em `purpose` no exemplo local, execute `tofu plan`
e descreva a diferença sem aplicar. Reponha o valor anterior, rode o plano e
confirme que não restaram mudanças:

```sh
tofu plan
```

Para testar uma mudança real no nome, ajuste o prefixo e revise o plano antes
de aplicar. Ao terminar, volte às entradas desejadas e use `tofu destroy`.
Não edite state manualmente.

## Resultado esperado e verificação

State list apresenta endereços; state show e show exibem atributos registrados.
Um plano sem diferença informa que não há mudanças. Destroy remove recursos
gerenciados pelo state; valide via output/Floci.

## Erros comuns

State não existe se nenhum apply completou. State não é global ao Floci:
apagar o diretório de state perde o mapeamento, mas não necessariamente recursos.
Drift real exige alteração observável na infraestrutura via API do provider.

## Exercício adicional

Se desejar, altere tags do bucket pela AWS CLI explicitamente apontada ao
Floci e então faça um plan. Confirme suporte/operação e reverta pelo provider.
Esta ação é opcional; não altere state.

Para demonstrar concorrência e state locking com o backend S3 nativo do Floci,
use o exercício opcional
[Lock nativo S3](lock-demo/README.md). Ele mantém o state padrão local; a
demonstração separada segura o lock por 45 segundos para que outra execução
observe a espera.

## Critério de conclusão

Explicou diferença entre configuração, state e drift; inspecionou state e
revisou uma mudança antes de destruí-la. **Tempo estimado: 40 min.**
