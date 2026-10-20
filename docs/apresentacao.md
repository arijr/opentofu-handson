# Apresentação — OpenTofu e fundamentos de IaC (30 min)

## Slides

O deck PowerPoint projetável está em
[apresentacao.pptx](apresentacao.pptx), com notas do apresentador em cada slide.
Para regenerá-lo após editar o conteúdo, instale `docs/requirements-slides.txt`
e execute `python3 docs/build_slides.py` na raiz do workshop. Este roteiro
continua como fonte detalhada das notas, perguntas e referências.

## Roteiro de slides

| Slide | Tempo | Conteúdo |
|---|---:|---|
| 1. OpenTofu e fundamentos de IaC | 1 min | Objetivos e laboratório exclusivamente local. |
| 2. Terraform e MPL 2.0 | 3 min | Terraform surgiu em 2014 sob Mozilla Public License 2.0; crescimento do ecossistema. |
| 3. Mudança de licença | 4 min | HashiCorp anunciou em 10 ago. 2023 a mudança de projetos core, incluindo Terraform, de MPL para Business Source License 1.1 (BUSL). |
| 4. Preocupações e resposta comunitária | 3 min | Distinguir a posição do manifesto de fatos históricos e interpretações jurídicas. |
| 5. Do anúncio ao fork público | 3 min | Anúncio do fork OpenTofu em 25 ago. 2023; repositório público em setembro de 2023. |
| 6. Fundação e primeira versão estável | 3 min | Linux Foundation em setembro de 2023; OpenTofu 1.6.0 em janeiro de 2024. |
| 7. Governança e posicionamento | 3 min | Proposta de desenvolvimento comunitário, neutralidade e compatibilidade. |
| 8. IaC declarativa | 3 min | Estado desejado, comparação e revisão de mudanças. |
| 9. As peças da configuração | 2 min | Providers, recursos, variáveis, outputs e módulos. |
| 10. Referências e dependências | 1 min | Dependências implícitas e fluxo de chamadas exclusivamente ao Floci. |
| 11. State e ciclo de execução | 3 min | `init`, `plan`, `apply`, drift, state e `destroy`; state local e locking. |
| 12. Perguntas para levar ao laboratório | 1 min | Discussão e transição para a preparação do Floci. |
| **Total** | **30 min** | |

## Notas do instrutor

### História: fatos versus avaliações

- Terraform foi lançado como software open source sob MPL 2.0 em 2014.
- HashiCorp anunciou em 10 de agosto de 2023 que Terraform e outros produtos
  core passariam a BUSL 1.1. A licença afeta versões sob os termos anunciados;
  não descreva a mudança como uma revogação retroativa de versões anteriores.
- O manifesto OpenTofu critica a BUSL como não open source e registra receios
  comunitários sobre concessão de uso e atividade potencialmente competitiva.
  Apresente isso como posição de seus autores e apoiadores, não como consenso
  universal ou interpretação jurídica definitiva.
- O fork foi anunciado publicamente em 25 de agosto. O artigo de setembro
  anunciou que o repositório OpenTofu estava público; o cronograma original
  ainda descrevia publicação da primeira versão estável como etapa futura.
- A Linux Foundation anunciou a incorporação do projeto em setembro de 2023.
  OpenTofu 1.6.0, primeira versão estável, foi publicada em janeiro de 2024.
- O projeto defende desenvolvimento comunitário, neutralidade e licença open
  source. Evite afirmar que governança garante por si só qualquer resultado
  futuro; aponte para o processo público, manifesto e documentação atual.

### Conceitos fundamentais

Apresente um diagrama verbal: arquivos HCL -> OpenTofu -> AWS Provider ->
endpoint Floci. Recursos que referenciam outputs/atributos de outros recursos
criam dependências implícitas; use `depends_on` somente quando a relação não
puder ser expressa naturalmente.

O ciclo didático é `init` (providers e módulos), `fmt`/`validate`, `plan`
(proposta), `apply` (execução confirmada) e `destroy` (remoção controlada).
Provider observa APIs e compara resultados com o state. Drift requer diferença
observável entre recursos gerenciados e infraestrutura, não apenas alteração
em um arquivo de state.

Explique que state local simplifica o curso, mas não é adequado para colaboração
sem proteção e coordenação. State pode guardar valores sensíveis; marcar um
output como `sensitive` mascara certas saídas, não criptografa os dados.

## Perguntas para discussão

1. O que uma licença open source permite e por que previsibilidade importa
   para quem mantém ferramentas em torno de um provider?
2. Quem deve participar das decisões de um projeto de infraestrutura?
3. Quando um plano deve ser tratado como revisão de mudança, não como mera
   formalidade?
4. O que pode dar errado se state local for compartilhado por cópia?
5. Que diferenças podem existir entre um emulador e o serviço AWS real?

## Fontes primárias e referências

- [OpenTofu Manifesto](https://opentofu.org/manifesto/) — cronologia e
  posicionamento dos autores do manifesto.
- [Anúncio do fork](https://opentofu.org/blog/opentofu-announces-fork-of-terraform/)
  — anúncio de 25 de agosto de 2023.
- [Fork disponível publicamente](https://opentofu.org/blog/the-opentofu-fork-is-now-available/)
  — publicação do repositório em setembro de 2023.
- [FAQ OpenTofu](https://opentofu.org/faq/) — contexto e respostas do projeto.
- [Documentação OpenTofu](https://opentofu.org/docs/) — linguagem e fluxo.
- [OpenTofu na Linux Foundation](https://www.linuxfoundation.org/press/announcing-opentofu)
  — incorporação e governança da fundação.
- [OpenTofu 1.6.0 GA](https://opentofu.org/blog/opentofu-is-going-ga/)
  — anúncio oficial da primeira versão estável.
- [Release OpenTofu 1.6.0](https://github.com/opentofu/opentofu/releases/tag/v1.6.0)
  — primeira versão estável, janeiro de 2024.
