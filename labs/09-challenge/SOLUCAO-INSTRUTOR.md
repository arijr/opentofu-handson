# Solução de referência — material do instrutor

Este arquivo é material de referência para avaliação, não uma etapa obrigatória
do aluno. A solução executável é a configuração final em `../../infra/`.

## Configuração esperada

1. `variables.tf` define `buckets` como mapa de objetos com propósito, com
   validação das chaves.
2. `locals.tf` deriva nomes usando prefixo, ambiente e chave e define tags
   comuns.
3. `main.tf` passa cada entrada para o módulo local:

```hcl
module "s3_bucket" {
  source   = "./modules/s3-bucket"
  for_each = local.bucket_names

  bucket_name = each.value
  purpose     = var.buckets[each.key].purpose
  tags        = local.common_tags
}
```

4. `modules/s3-bucket` declara `aws_s3_bucket` e retorna nome e ARN.
5. `outputs.tf` agrega outputs do módulo por chave.
6. `terraform.tfvars.example` contém duas entradas:

```hcl
buckets = {
  artifacts = {
    purpose = "artefatos de laboratorio"
  }
  logs = {
    purpose = "logs simulados do laboratorio"
  }
}
```

## Execução para conferência

Na raiz, copie o exemplo e inicialize. A configuração do provider só aponta
para o endpoint local do Floci:

```sh
cp infra/terraform.tfvars.example infra/terraform.tfvars
docker compose up -d
tofu -chdir=infra init
tofu -chdir=infra fmt -check -recursive
tofu -chdir=infra validate
tofu -chdir=infra plan
tofu -chdir=infra apply
tofu -chdir=infra output bucket_names
tofu -chdir=infra output bucket_arns
tofu -chdir=infra destroy
```

Os outputs devem ter as chaves `artifacts` e `logs`, com nomes compostos por
prefixo, ambiente e chave. O plano deve criar dois recursos via módulo. Após
destroy, confirme que os recursos gerenciados foram removidos. Para descartar
também os dados persistidos do Floci, use `docker compose down -v` na raiz
depois de verificar que os recursos foram destruídos.

## Avaliação

Aceite soluções equivalentes que cumpram a rubrica, usem mapa de chaves válidas,
preservem identidade via `for_each`, mantenham a endpoint local, mostrem
outputs úteis e destruam os recursos. Não avalie por igualdade textual com os
arquivos de referência.
