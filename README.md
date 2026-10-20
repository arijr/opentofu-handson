# Minicurso OpenTofu com Floci

Laboratório introdutório de Infrastructure as Code com OpenTofu e AWS Provider,
executado exclusivamente contra o emulador local Floci. Nenhum recurso AWS real
é necessário ou deve ser criado.

## Curso em 5 horas

- **Dia 1 (2h30):** 30 min de história e conceitos; 20 min de preparação; 30 min
  no primeiro bucket; 30 min de variáveis e outputs; 40 min de state e ciclo de vida.
- **Dia 2 (2h30):** 25 min de módulos; 30 min de expressões; 30 min de recursos e
  data sources; 25 min de qualidade e segurança; 40 min de desafio.

Comece pelo deck [docs/apresentacao.pptx](docs/apresentacao.pptx); as notas,
referências e o roteiro detalhado ficam em
[docs/apresentacao.md](docs/apresentacao.md). Os passos, objetivos e critérios
de cada atividade estão em [labs/](labs/).

Para conduzir as sessões de laboratório em ordem e dentro do tempo, consulte o
[roteiro do apresentador](docs/roteiro-apresentador-labs.md).

## Início rápido

Pré-requisitos e instalação estão em [docs/pre-requisitos.md](docs/pre-requisitos.md).
Na raiz deste projeto:

```sh
./scripts/check-prerequisites.sh
docker compose up -d
docker compose ps
curl -sS -o /dev/null -w 'HTTP %{http_code}\n' http://localhost:4566/
cd infra
tofu init
tofu fmt
tofu validate
tofu plan
tofu apply
```

O `curl` verifica somente que há um servidor HTTP respondendo na porta. O Floci
não documenta essa rota raiz como health check. Para validar uma operação AWS
simulada, use `aws s3api list-buckets --endpoint-url http://localhost:4566` com
as credenciais de teste indicadas neste material.

`apply` cria recursos simulados no Floci; `destroy` os remove. Sempre revise o
plano e confirme que o endpoint é `http://localhost:4566`. Não exporte perfis
AWS reais durante o curso.

## Comandos convenientes

```sh
make check
make up
make init
make fmt
make validate
make plan
make apply       # requer confirmação do OpenTofu
make destroy     # requer confirmação do OpenTofu
make down
```

O provider, as variáveis locais, as tags comuns e o módulo reutilizável estão
em [infra/](infra/). Sem tfvars, o mapa `buckets` cria um bucket padrão; o
arquivo `infra/terraform.tfvars.example` apresenta dois. As etapas explicam
como os conceitos se relacionam sem exigir edição manual do state.

## Limpeza

Dentro de `infra`, confira os recursos e execute `tofu destroy` para remover
somente aqueles gerenciados por este state. Depois, na raiz, `docker compose down`
para o Floci. O compose usa o modo persistente documentado pelo Floci e grava os
dados no volume nomeado `floci-data`; `down` preserva esse volume e os dados.

`scripts/cleanup.sh` não destrói nada por padrão. O uso de `--destroy` requer uma
confirmação literal antes de executar `tofu destroy`.

O Compose mantém os dados do Floci em um volume nomeado para que persistam
entre reinicializações. Para descartar os dados deste projeto, depois de
destruir os recursos execute `docker compose down -v`; isso remove o volume
`floci-data` pertencente a este projeto. Confirme que está na raiz do workshop
antes de executar esse comando.

## Estrutura

- `docs/`: apresentação, preparação, solução de problemas e glossário.
- `infra/`: configuração OpenTofu final e módulos didáticos.
- `labs/`: nove roteiros para os dois encontros.
- `scripts/`: verificações, validação e limpeza explícita.

O [lab 04 inclui uma demonstração opcional de lock nativo do backend S3](labs/04-state-lifecycle/lock-demo/README.md),
separada da configuração padrão com state local.

## Fontes e compatibilidade

- [OpenTofu Manifesto](https://opentofu.org/manifesto/)
- [Floci: repositório e início rápido](https://github.com/floci-io/floci)
- [Floci 2.3.0: quick start](https://github.com/floci-io/floci/blob/2.3.0/docs/getting-started/quick-start.md)
- [Floci: persistência Docker Compose](https://floci.io/floci/configuration/docker-compose/)
- [Floci: S3](https://floci.io/floci/services/s3/)
- [Floci: guia de Terraform/OpenTofu](https://github.com/floci-io/floci/blob/2.3.0/docs/getting-started/terraform.md)
- [Floci: workflow de compatibilidade OpenTofu](https://github.com/floci-io/floci/blob/2.3.0/.github/workflows/compatibility.yml)
- [OpenTofu: backend S3 e lock nativo](https://opentofu.org/docs/language/settings/backends/s3/)
- [AWS Provider 5.100.0: endpoints customizados](https://registry.terraform.io/providers/hashicorp/aws/5.100.0/docs/guides/custom-service-endpoints)
- [AWS Provider: configuração](https://registry.terraform.io/providers/hashicorp/aws/5.100.0/docs)

O Floci documenta S3 (incluindo `CreateBucket`, `HeadBucket` e
`GetBucketLocation`) e IAM como serviços suportados. O workflow 2.3.0 inclui
suítes de compatibilidade e uma checagem de paridade dos recursos OpenTofu.
Neste projeto também foram executados create/list, consulta por data source,
plan e destroy do bucket com AWS Provider 5.100.0 e Floci 2.3.0. Isso não
certifica todas as operações/recursos desses produtos; mantenha os exercícios
avançados opcionais e revalide-os ao atualizar versões.
