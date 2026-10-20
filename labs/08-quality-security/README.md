# Laboratório 08 — Qualidade e segurança (25 min)

## Objetivo

Verificar formato, configuração, plano e controles básicos para manter o
exercício reproduzível e direcionado ao emulador.

## Conceitos explicados

`.terraform.lock.hcl` registra a versão e os hashes do provider; versioná-lo mantém
inicializações consistentes. State pode conter dados sensíveis, então não deve
ser versionado. `sensitive = true` oculta valores em certas saídas de CLI,
mas não criptografa state nem protege outros armazenamentos.

## Pré-requisitos e arquivos envolvidos

Labs anteriores; confira `.gitignore`, `infra/providers.tf`,
`infra/versions.tf` e `infra/.terraform.lock.hcl`.

## Passo a passo

```sh
tofu -chdir=infra fmt -check -recursive
tofu -chdir=infra validate
tofu -chdir=infra plan
```

Revise ações, nomes e endpoint. Verifique que `.gitignore` exclui state,
backups, `.terraform/`, tfvars locais e planos, mas não ignora o lock file.
Antes de compartilhar mudanças:

```sh
git status --short
```

Não adicione state, arquivos `terraform.tfvars` ou planos ao commit. A
configuração principal do curso mantém state local. Como extensão prática, o
[lab 04 opcional](../04-state-lifecycle/lock-demo/README.md) demonstra backend
S3 e locking nativo contra o Floci; ele não altera o backend principal nem deve
ser apontado à AWS. Em ambientes reais, backend remoto, controle de acesso,
criptografia e locking precisam ser projetados conscientemente.

## Resultado esperado e verificação

fmt e validate terminam sem erro; o plan contém somente operações contra o
endpoint local. O lock file permanece versionável.

## Erros comuns

`sensitive` não equivale a criptografia. `.gitignore` não remove arquivos já
adicionados ao Git. O OpenTofu usa o nome `.terraform.lock.hcl` para o lock
file de providers; gere-o com `tofu init`, não o preencha manualmente.

## Exercício adicional

Faça uma revisão por pares do plano sem aplicá-lo e peça ao colega para
identificar endpoint, recurso e ação prevista.

## Critério de conclusão

Executou as verificações, descreveu os riscos do state e explicou o papel do
lock file sem confundir mascaramento com criptografia. **Tempo estimado: 25 min.**
