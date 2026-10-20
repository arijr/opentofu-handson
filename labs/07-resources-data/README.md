# Laboratório 07 — Recursos e data sources (30 min)

## Objetivo

Ver referências implícitas e consultar um bucket já gerenciado usando uma
operação documentada no Floci.

## Conceitos explicados

Referenciar um output de módulo estabelece dependência implícita. `depends_on`
é reservado a dependências que não podem ser expressas por referência direta.
Um data source lê um recurso; não o cria nem o gerencia.

## Pré-requisitos e arquivos envolvidos

Tenha um bucket criado no Floci. O provider usa endpoint local para S3 e IAM.
A documentação S3 do Floci lista `HeadBucket` e `GetBucketLocation`, operações
usadas para consultar bucket. O repositório Floci declara testes de
compatibilidade OpenTofu e checagem de paridade dos alvos de compatibilidade.

## Passo a passo

No root module, crie temporariamente em `infra/main.tf` um data source para um
bucket existente, substituindo o nome pela saída real:

```hcl
data "aws_s3_bucket" "existing" {
  bucket = "${var.project_prefix}-${var.environment}-artifacts"
}
```

Ajuste a chave se necessário. O bucket precisa ter sido criado antes; esta
consulta é destinada a ler um objeto existente e não introduz dependência
circular com o módulo que o cria. Valide e leia o plano:

```sh
cd infra
tofu fmt
tofu validate
tofu plan
```

O data source lê bucket local já criado. Remova o bloco depois do exercício se
o bucket não existir ou se o provider não aceitar a consulta. Não crie
dependência artificial via `depends_on`.

## IAM opcional

Floci documenta IAM e ações de policy (CreatePolicy/GetPolicy/DeletePolicy).
O módulo `modules/iam-policy` deste projeto gera somente JSON local; não cria
policy AWS. O uso de `aws_iam_policy` é opcional para o instrutor e requer teste
end-to-end do provider selecionado antes da aula. Se executado, provider aponta
IAM ao endpoint local; não use uma conta AWS.

## Resultado esperado e verificação

Data source lê o bucket e `tofu validate` passa. Não há recurso novo criado
pelo data source.

## Erros comuns

Data source falha se o bucket não existe no emulador ou foi apagado fora do
state. O suporte de uma API pelo Floci não garante cobertura de todo atributo
ou comportamento específico do AWS Provider.

## Exercício adicional

Use um output do data source em um output temporário e compare-o ao módulo.

## Critério de conclusão

Distinguiu leitura e criação, identificou dependência implícita e evitou
`depends_on` desnecessário. **Tempo estimado: 30 min.**
