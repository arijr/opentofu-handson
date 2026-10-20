# Solução de problemas

## Porta 4566 já está em uso

O compose publica `4566:4566`, endpoint esperado pelos exercícios. Identifique
o processo/container que está usando a porta e encerre-o conscientemente ou
pare o outro emulador. Não altere a configuração do provider sem alinhar também
a porta publicada e todos os comandos do curso.

```sh
docker compose ps
docker compose logs --tail=100 floci
```

## Container não iniciou ou ainda não responde

```sh
docker compose ps
docker compose logs -f floci
curl -v --connect-timeout 3 http://localhost:4566/
```

O projeto não define um health check Compose inventado. O `curl` verifica
conectividade HTTP, não uma rota de diagnóstico oficial. Consulte a documentação
Floci para comportamento e configurações atuais.

## `tofu init` não baixa o provider

Confirme acesso à rede e tente novamente. Não remova `.terraform.lock.hcl` para
"resolver" uma inconsistência; verifique a versão do OpenTofu e a origem
`hashicorp/aws` no lock file. Para atualizar uma dependência, faça uma alteração
intencional e revise o novo lock file.

## Credenciais ou metadata

O provider fornece as credenciais de teste e desativa verificações que
dependem de credenciais AWS reais ou do serviço de metadata. O código não deve
usar `profile`. Se aparecer solicitação para entrar em uma conta, pare e
verifique se está executando `tofu` no diretório `infra` e usando os arquivos
deste projeto.

## `BucketAlreadyExists` ou nome indisponível

Nomes de bucket são globais no namespace S3 do emulador e seguem a validação
do S3. Altere `project_prefix` em `terraform.tfvars` (ou passe
`-var='project_prefix=...'`) para um prefixo minúsculo, único e válido. Não
inclua espaços, letras maiúsculas nem underscore. Não altere o state à mão.

## Plano mostra destruição/recriação inesperada

Leia a seção `Plan` completa e compare mudanças de nome, mapa `buckets` e
módulo chamado. O `for_each` associa recursos pela chave; renomear uma chave
muda a identidade e pode resultar em substituir o bucket. Faça backup do
diretório de state antes de práticas deliberadas e consulte o instrutor.

## Provider aponta a um endpoint inesperado

Confirme `infra/providers.tf` e `infra/variables.tf`. Este workshop não aceita
endpoints AWS reais como entrada: `aws_endpoint` tem validação para o host local.
Não contorne essa validação. A AWS CLI precisa de `--endpoint-url` em cada
comando.

## Limpar sessão

Destrua os recursos pelo state do curso (`tofu -chdir=infra destroy`) e pare o
container com `docker compose down`. O volume nomeado `floci-data` preserva os
dados entre sessões. Para descartá-los após a destruição dos recursos:
`docker compose down -v`. Esse comando remove os volumes nomeados declarados
por este compose; confirme estar na raiz do workshop antes de executá-lo.
