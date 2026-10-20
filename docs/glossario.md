# Glossário

- **Backend:** mecanismo onde o OpenTofu guarda o state. O curso usa o backend
  local padrão; um backend remoto pode permitir colaboração e locking.
- **Data source:** consulta uma informação existente por meio de um provider,
  sem declarar que o OpenTofu é dono daquele recurso.
- **Drift:** diferença entre a configuração/state gerenciado e o recurso
  observado pelo provider. Não é sinônimo de qualquer alteração no state.
- **HCL:** HashiCorp Configuration Language, linguagem declarativa usada nos
  arquivos `.tf`.
- **IaC:** Infrastructure as Code; recursos de infraestrutura descritos,
  versionados e revisados como código.
- **Módulo:** conjunto de arquivos de configuração reutilizável. A pasta raiz
  do projeto também é um módulo.
- **Plan:** proposta das ações que o OpenTofu executaria para aproximar recursos
  observados da configuração desejada.
- **Provider:** plugin que traduz a configuração declarativa para operações
  numa API, como o AWS Provider.
- **Resource:** bloco que declara um objeto que o OpenTofu cria e gerencia.
- **State:** mapeamento local entre endereços de recursos da configuração e
  objetos identificados no provider. Pode conter valores sensíveis.
- **Variable:** entrada parametrizável de um módulo.
- **Output:** valor exposto por um módulo após avaliar a configuração.
- **`for_each`:** cria instâncias identificadas por chaves estáveis de um mapa
  ou conjunto.
- **`count`:** cria instâncias indexadas por posição numérica; alterações na
  ordem podem afetar a identidade.
- **Lock file:** `.terraform.lock.hcl`, nome usado pelo OpenTofu para registrar
  versões e hashes dos providers selecionados para inicialização reproduzível.
- **Floci:** emulador local de serviços AWS usado neste curso em
  `http://localhost:4566`; não é a AWS e pode ter diferenças de comportamento.
