#!/usr/bin/env python3
"""Build instructor/student lab slides as PowerPoint."""

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "docs" / "laboratorios.pptx"

NAVY = RGBColor(11, 18, 32)
PANEL = RGBColor(19, 31, 50)
PANEL_ALT = RGBColor(23, 40, 62)
WHITE = RGBColor(244, 248, 252)
MUTED = RGBColor(168, 184, 202)
TEAL = RGBColor(58, 220, 194)
BLUE = RGBColor(95, 163, 255)
GOLD = RGBColor(255, 197, 91)
FONT = "Aptos"
CODE_FONT = "Cascadia Mono"

LABS = [
    {
        "number": "01",
        "title": "Preparação",
        "day": "HOJE",
        "time": "20 min",
        "slot": "00:30–00:50",
        "goal": "Deixar o emulador local pronto e inicializar OpenTofu sem criar recursos.",
        "ideas": [
            ("Docker Compose", "Inicia o Floci local na porta 4566."),
            ("tofu init", "Baixa o AWS Provider; não aplica infraestrutura."),
            ("Segurança", "Todo endpoint AWS usado pelo provider é localhost:4566."),
        ],
        "prompt": "Antes de avançar, confira: o container está healthy e o init terminou?",
        "commands": (
            "./scripts/check-prerequisites.sh\n"
            "docker compose up -d\n"
            "docker compose ps\n"
            "docker compose logs --tail=30 floci\n"
            "tofu -chdir=infra init\n"
            "tofu -chdir=infra fmt\n"
            "tofu -chdir=infra validate"
        ),
        "expected": "Floci em execução; provider instalado; nenhum bucket criado.",
        "transition": "Agora descrevemos um bucket e lemos o plano antes de aplicar.",
        "notes": (
            "Comandos mostrados para Bash/macOS/Linux. Em PowerShell, use "
            ".\\scripts\\check-prerequisites.ps1. AWS CLI é opcional. Não trate "
            "resposta HTTP da raiz como health check oficial; use docker compose "
            "ps e aguarde healthy. Se houver problema, projete os logs e deixe "
            "participantes acompanharem em duplas."
        ),
    },
    {
        "number": "02",
        "title": "Primeiro recurso",
        "day": "HOJE",
        "time": "30 min",
        "slot": "00:50–01:20",
        "goal": "Criar e destruir um bucket de teste no Floci, entendendo o ciclo plan/apply.",
        "ideas": [
            ("Provider", "Envia operações S3 ao endpoint local."),
            ("Resource", "Declara o bucket desejado em HCL."),
            ("Plano", "É uma proposta para revisar; não cria o recurso."),
        ],
        "prompt": "No plan, localize ação, endereço do recurso, nome do bucket e endpoint.",
        "commands": (
            "tofu -chdir=infra fmt\n"
            "tofu -chdir=infra validate\n"
            "tofu -chdir=infra plan \\\n"
            "  -var='buckets={primeiro={purpose=\"primeiro recurso\"}}'\n"
            "tofu -chdir=infra apply \\\n"
            "  -var='buckets={primeiro={purpose=\"primeiro recurso\"}}'\n"
            "tofu -chdir=infra output\n"
            "tofu -chdir=infra state list\n"
            "tofu -chdir=infra destroy \\\n"
            "  -var='buckets={primeiro={purpose=\"primeiro recurso\"}}'"
        ),
        "expected": "Um bucket criado, output apresentado e o mesmo bucket destruído após novo plano.",
        "transition": "Agora vamos parametrizar nomes e tags para recursos reutilizáveis.",
        "notes": (
            "Peça confirmação visual do plano antes de apply e destroy. Cada "
            "operação deve listar somente o bucket temporário do exercício. "
            "Responda yes apenas depois de os alunos identificarem que o "
            "endpoint é local."
        ),
    },
    {
        "number": "03",
        "title": "Variáveis e outputs",
        "day": "HOJE",
        "time": "30 min",
        "slot": "01:20–01:50",
        "goal": "Trocar parâmetros de linha de comando por variáveis, tags comuns e outputs informativos.",
        "ideas": [
            ("Variables", "Tipo, default e validação definem entradas."),
            ("Locals", "Derivam nomes e tags padronizados."),
            ("Outputs", "Exibem nomes e ARNs dos buckets."),
        ],
        "prompt": "Preveja os nomes antes do plan: prefixo + ambiente + chave do mapa.",
        "commands": (
            "cp infra/terraform.tfvars.example infra/terraform.tfvars\n"
            "# Revise project_prefix, environment e as chaves artifacts/logs\n"
            "tofu -chdir=infra fmt\n"
            "tofu -chdir=infra validate\n"
            "tofu -chdir=infra plan\n"
            "tofu -chdir=infra apply\n"
            "tofu -chdir=infra output bucket_names\n"
            "tofu -chdir=infra output bucket_arns\n"
            "tofu -chdir=infra state list"
        ),
        "expected": "Dois buckets, tags comuns e outputs com as chaves artifacts e logs.",
        "transition": "Mantenha os buckets e o state: amanhã consultaremos um bucket existente.",
        "notes": (
            "PowerShell para copiar: Copy-Item "
            "infra/terraform.tfvars.example infra/terraform.tfvars. Se o "
            "participante personalizar prefixo, anote-o. Não execute destroy "
            "no fim deste lab: o Lab 07 amanhã precisa do bucket artifacts. "
            "O tfvars local está ignorado pelo Git."
        ),
    },
    {
        "number": "04",
        "title": "State e ciclo de vida",
        "day": "HOJE",
        "time": "40 min",
        "slot": "01:50–02:30",
        "goal": "Inspecionar state, comparar mudanças planejadas e explicar drift e locking.",
        "ideas": [
            ("Configuração", "Expressa a intenção declarativa."),
            ("State", "Relaciona endereços de recursos e atributos observados."),
            ("Drift", "Diferença observável entre configuração/state e infraestrutura."),
        ],
        "prompt": "Compare o plan normal com o plan que altera environment apenas para essa execução.",
        "commands": (
            "tofu -chdir=infra state list\n"
            "tofu -chdir=infra state show \\\n"
            "  'module.s3_bucket[\"artifacts\"].aws_s3_bucket.this'\n"
            "tofu -chdir=infra show\n"
            "tofu -chdir=infra plan\n"
            "tofu -chdir=infra plan -refresh-only\n"
            "tofu -chdir=infra plan -var='environment=qa'\n"
            "tofu -chdir=infra plan"
        ),
        "expected": "State inspecionado; plan com qa não aplicado; plan normal sem mudanças.",
        "transition": "Guarde a mesma pasta, state e volume Floci para a sessão de amanhã.",
        "notes": (
            "Não aplicar o plan com environment=qa: os nomes induzem substituição. "
            "O último plan deve voltar ao estado desejado dev e ser no-op. "
            "O state local é por pasta e não é um mecanismo de colaboração. "
            "Se houver tempo, apresente o lock demo opcional no projetor; a "
            "versão completa está em labs/04-state-lifecycle/lock-demo/README.md. "
            "Não é obrigatório inicializar o backend remoto durante esta aula."
        ),
    },
    {
        "number": "05",
        "title": "Módulos",
        "day": "AMANHÃ",
        "time": "25 min",
        "slot": "00:00–00:25",
        "goal": "Entender a interface do módulo S3 e rastrear dados do root até o resource.",
        "ideas": [
            ("source", "Aponta para o módulo local reutilizável."),
            ("Inputs", "bucket_name, purpose e tags."),
            ("Outputs", "Nome e ARN retornam ao módulo raiz."),
        ],
        "prompt": "Rastreie artifacts: variável → local → input do módulo → resource → output.",
        "commands": (
            "docker compose up -d\n"
            "tofu -chdir=infra init\n"
            "tofu -chdir=infra state list\n"
            "tofu -chdir=infra output bucket_names\n"
            "tofu -chdir=infra validate\n"
            "tofu -chdir=infra plan"
        ),
        "expected": "Buckets de ontem preservados; configuração do módulo válida; plan sem mudanças.",
        "transition": "Com a interface entendida, vamos observar instâncias por chave.",
        "notes": (
            "Início do Dia 2: confirmar que é a mesma pasta e Floci volume. "
            "Se a infra não aparece no state, não aplicar às cegas; verificar "
            "diretório/state primeiro. Abra main.tf, modules/s3-bucket/"
            "variables.tf, main.tf, outputs.tf e root outputs.tf. O plan "
            "deve ser no-op."
        ),
    },
    {
        "number": "06",
        "title": "Expressões e recursos dinâmicos",
        "day": "AMANHÃ",
        "time": "30 min",
        "slot": "00:25–00:55",
        "goal": "Adicionar uma instância via mapa e explicar identidade estável com for_each.",
        "ideas": [
            ("for_each", "Cada chave identifica uma instância no state."),
            ("for expression", "Deriva nomes a partir do mapa de entrada."),
            ("Validação", "Rejeita chaves e quantidade fora dos limites definidos."),
        ],
        "prompt": "Leia o plan: adicionar reports deve criar um único bucket; chaves renomeadas mudam identidade.",
        "commands": (
            "# Em infra/terraform.tfvars, acrescente dentro de buckets:\n"
            "reports = { purpose = \"relatorios do laboratorio\" }\n"
            "tofu -chdir=infra fmt\n"
            "tofu -chdir=infra validate\n"
            "tofu -chdir=infra plan\n"
            "tofu -chdir=infra apply\n"
            "tofu -chdir=infra state list\n"
            "tofu -chdir=infra output bucket_names\n"
            "# Validação negativa: deve falhar; não aplicar\n"
            "tofu -chdir=infra plan \\\n"
            "  -var='buckets={INVALIDA={purpose=\"teste\"}}'"
        ),
        "expected": "reports é a única criação; chave INVALIDA falha em validação antes do apply.",
        "transition": "Agora vamos ler um bucket existente sem criar outro.",
        "notes": (
            "O mapa suporta no máximo quatro chaves. Garanta que a linha "
            "reports fica dentro do bloco buckets, com vírgula/sintaxe HCL "
            "válida. Após a validação negativa, retorne ao tfvars válido e "
            "não deixe a entrada inválida persistida. A validação negativa "
            "não cria recursos."
        ),
    },
    {
        "number": "07",
        "title": "Resources e data sources",
        "day": "AMANHÃ",
        "time": "30 min",
        "slot": "00:55–01:25",
        "goal": "Consultar um bucket existente via data source e distinguir leitura de criação.",
        "ideas": [
            ("Resource", "Declara objeto que OpenTofu cria/gerencia."),
            ("Data source", "Consulta dados de objeto já existente."),
            ("Dependência", "Referências criam dependências implícitas; depends_on é exceção."),
        ],
        "prompt": "Observe que o data source lê artifacts e não adiciona um bucket ao plano.",
        "commands": (
            "# Crie infra/data_source.tf temporariamente:\n"
            "data \"aws_s3_bucket\" \"existing\" {\n"
            "  bucket = \"${var.project_prefix}-${var.environment}-artifacts\"\n"
            "}\n"
            "output \"existing_bucket_from_data_source\" {\n"
            "  value = data.aws_s3_bucket.existing.id\n"
            "}\n"
            "tofu -chdir=infra fmt\n"
            "tofu -chdir=infra validate\n"
            "tofu -chdir=infra plan\n"
            "# Remova infra/data_source.tf ao concluir"
        ),
        "expected": "Consulta S3 local bem-sucedida; nenhum resource novo; arquivo temporário removido.",
        "transition": "Com a leitura testada, revisaremos segurança e qualidade da configuração.",
        "notes": (
            "O data source precisa que o bucket artifacts exista em Floci. "
            "Como o módulo já cria esse bucket, não coloque o data source no "
            "mesmo root durante apply, pois pode gerar dependência circular. "
            "O exercício é plan/read-only. Retirar data_source.tf ao terminar. "
            "IAM permanece opcional; o módulo iam-policy apenas produz JSON."
        ),
    },
    {
        "number": "08",
        "title": "Qualidade e segurança",
        "day": "AMANHÃ",
        "time": "25 min",
        "slot": "01:25–01:50",
        "goal": "Revisar formato, validação, plano, lock file, state e controles do endpoint.",
        "ideas": [
            ("Reproduzibilidade", "Versionar .terraform.lock.hcl com hashes do provider."),
            ("State", "Pode conter dados sensíveis; não deve ser commitado."),
            ("Sensitive", "Mascara certas saídas; não criptografa state."),
        ],
        "prompt": "Faça uma revisão em pares: provider, endpoint, ações e arquivos ignorados no Git.",
        "commands": (
            "tofu -chdir=infra fmt -check -recursive\n"
            "tofu -chdir=infra validate\n"
            "tofu -chdir=infra plan\n"
            "git status --short\n"
            "# Inspecione .gitignore, providers.tf e o lock file"
        ),
        "expected": "Formato e validação passam; plan aponta apenas ao Floci; state/tfvars não entram no Git.",
        "transition": "No desafio, cada dupla vai aplicar e depois limpar o próprio state.",
        "notes": (
            "Antes do plan, confirmar que o arquivo temporário do data source "
            "foi removido. É possível que git status falhe quando não há Git "
            "instalado/inicializado; explicar o comando em vez de bloqueiar "
            "a aula. Reforce que sensitive não criptografa. Para backend "
            "remoto/locking, a extensão prática já está separada no lab04 e "
            "usa o Floci, nunca AWS."
        ),
    },
    {
        "number": "09",
        "title": "Desafio final",
        "day": "AMANHÃ",
        "time": "40 min",
        "slot": "01:50–02:30",
        "goal": "Construir, validar, aplicar, verificar e destruir dois ou mais buckets.",
        "ideas": [
            ("Requisitos", "for_each, mapa de entrada, tags comuns e módulo S3."),
            ("Evidência", "Plan aprovado, outputs de nomes/ARNs e endereços no state."),
            ("Limpeza", "Destroy revisado e confirmação de state vazio."),
        ],
        "prompt": "Avalie pelo resultado e segurança, não pela igualdade textual com a solução do instrutor.",
        "commands": (
            "# Limpe os buckets usados nos labs anteriores\n"
            "tofu -chdir=infra destroy\n"
            "# Configure duas ou mais chaves em infra/terraform.tfvars\n"
            "tofu -chdir=infra fmt -check -recursive\n"
            "tofu -chdir=infra validate\n"
            "tofu -chdir=infra plan\n"
            "tofu -chdir=infra apply\n"
            "tofu -chdir=infra output bucket_names\n"
            "tofu -chdir=infra output bucket_arns\n"
            "tofu -chdir=infra state list\n"
            "tofu -chdir=infra destroy\n"
            "tofu -chdir=infra state list"
        ),
        "expected": "Dois ou mais buckets verificados; após destroy, state sem endereços.",
        "transition": "Fechamento: revisão do aprendizado e confirmação de que não restaram recursos do desafio.",
        "notes": (
            "Reserve ao menos 6 minutos finais para destroy e verificação. "
            "Revise o destroy inicial com os alunos: ele remove buckets "
            "criados em labs anteriores no state desta oficina. Antes do apply "
            "do desafio, leia o plan. AWS CLI é opcional e qualquer chamada "
            "deve incluir --endpoint-url http://localhost:4566 com credenciais "
            "test apenas. Solução de referência em labs/09-challenge/"
            "SOLUCAO-INSTRUTOR.md."
        ),
    },
]


def set_text(shape, text, size, color, bold=False, font=FONT, align=None):
    frame = shape.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Pt(0)
    frame.margin_right = Pt(0)
    frame.margin_top = Pt(0)
    frame.margin_bottom = Pt(0)
    for index, line in enumerate(text.splitlines() or [""]):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.text = line
        paragraph.font.name = font
        paragraph.font.size = Pt(size)
        paragraph.font.bold = bold
        paragraph.font.color.rgb = color
        paragraph.space_after = Pt(0)
        paragraph.space_before = Pt(0)
        if align is not None:
            paragraph.alignment = align


def textbox(slide, text, x, y, w, h, size, color, bold=False, font=FONT, align=None):
    shape = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    set_text(shape, text, size, color, bold, font, align)
    return shape


def panel(slide, x, y, w, h, fill=PANEL):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.fill.background()
    return shape


def base(slide, index, label):
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = NAVY
    accent = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(0.13), Inches(7.5)
    )
    accent.fill.solid()
    accent.fill.fore_color.rgb = TEAL
    accent.line.fill.background()
    textbox(
        slide,
        f"MINICURSO OPENTOFU • LABORATÓRIOS                                    {label.upper()} • {index:02d}/20",
        0.56,
        7.12,
        12,
        0.2,
        9,
        MUTED,
        True,
    )


def header(slide, kicker, title, subtitle):
    textbox(slide, kicker, 0.72, 0.35, 11.8, 0.24, 10.5, TEAL, True)
    textbox(slide, title, 0.72, 0.72, 11.8, 0.55, 26, WHITE, True)
    if subtitle:
        textbox(slide, subtitle, 0.74, 1.34, 11.5, 0.34, 13, MUTED)


def create_cover(pres, slide, index):
    base(slide, index, "GUIA DE EXECUÇÃO")
    textbox(slide, "GUIA DO INSTRUTOR E DOS ALUNOS", 0.86, 0.95, 11.6, 0.3, 13, TEAL, True)
    textbox(slide, "Laboratórios OpenTofu + Floci", 0.86, 1.55, 11.6, 0.78, 35, WHITE, True)
    textbox(slide, "Passo a passo visual • 9 labs • 4h de prática em dois encontros", 0.88, 2.52, 11, 0.42, 17, MUTED)
    for i, (label, body) in enumerate(
        [
            ("HOJE • 2h", "Labs 01–04\nPreparar, criar, parametrizar e inspecionar state."),
            ("AMANHÃ • 2h30", "Labs 05–09\nReutilizar, expressar, consultar, revisar e desafiar."),
            ("AMBIENTE LOCAL", "OpenTofu + AWS Provider\nFloci em localhost:4566."),
        ]
    ):
        x = 0.88 + i * 4.08
        panel(slide, x, 3.55, 3.62, 1.48, PANEL if i != 1 else PANEL_ALT)
        textbox(slide, label, x + 0.22, 3.83, 3.2, 0.32, 15, TEAL, True)
        textbox(slide, body, x + 0.22, 4.27, 3.2, 0.64, 13, WHITE)
    slide.notes_slide.notes_text_frame.text = (
        "Deck de condução dos exercícios. Os labs 01–04 acontecem depois dos "
        "30 minutos de apresentação, totalizando 2 horas hoje. Labs 05–09 "
        "ocupam as 2h30 de amanhã. State e buckets do primeiro dia devem ser "
        "preservados para o data source do Lab 07."
    )


def create_agenda(pres, slide, index):
    base(slide, index, "AGENDA")
    header(slide, "MAPA DA SESSÃO", "Do setup à limpeza", "Quatro horas de laboratório, mantendo a prática segura e revisável.")
    rows = [
        ("HOJE • 120 min", "01 Setup 20’   ·   02 Bucket 30’   ·   03 Variables 30’   ·   04 State 40’"),
        ("AMANHÃ • 150 min", "05 Módulos 25’   ·   06 Expressões 30’   ·   07 Data 30’   ·   08 Qualidade 25’   ·   09 Desafio 40’"),
        ("REGRA DE OURO", "Leia todo plan antes de apply/destroy. Use somente localhost:4566."),
    ]
    for i, (label, body) in enumerate(rows):
        y = 2.1 + i * 1.15
        panel(slide, 0.85, y, 11.6, 0.86, PANEL if i != 1 else PANEL_ALT)
        textbox(slide, label, 1.12, y + 0.16, 2.0, 0.27, 14, TEAL, True)
        textbox(slide, body, 3.15, y + 0.15, 9.0, 0.48, 14, WHITE)
    slide.notes_slide.notes_text_frame.text = (
        "Hoje, após os 30 minutos de apresentação, conduza exatamente os labs "
        "01–04 em 2 horas. Amanhã conduza labs 05–09 em 2h30. Exercícios "
        "opcionais devem substituir, não acrescentar tempo."
    )


def lab_intro(pres, slide, index, lab):
    label = f"DIA {lab['day']} • LAB {lab['number']} • {lab['time']} • {lab['slot']}"
    base(slide, index, lab["day"])
    header(slide, label, lab["title"], lab["goal"])
    for i, (title, body) in enumerate(lab["ideas"]):
        y = 2.2 + i * 1.16
        panel(slide, 0.82, y, 7.28, 0.9, PANEL if i % 2 == 0 else PANEL_ALT)
        textbox(slide, title, 1.08, y + 0.16, 1.72, 0.27, 14, TEAL, True)
        textbox(slide, body, 2.85, y + 0.14, 4.95, 0.52, 13.2, WHITE)
    panel(slide, 8.42, 2.2, 4.05, 3.22, PANEL_ALT)
    textbox(slide, "PERGUNTA-GUIA", 8.72, 2.5, 3.5, 0.25, 11, GOLD, True)
    textbox(slide, lab["prompt"], 8.72, 2.98, 3.47, 1.45, 18, WHITE, True)
    panel(slide, 0.82, 5.96, 11.65, 0.55, PANEL)
    textbox(slide, f"RESULTADO ESPERADO   {lab['expected']}", 1.08, 6.11, 11.1, 0.26, 12, WHITE)
    slide.notes_slide.notes_text_frame.text = lab["notes"]


def lab_run(pres, slide, index, lab):
    label = f"LAB {lab['number']} • EXECUÇÃO • {lab['slot']}"
    base(slide, index, lab["day"])
    header(slide, label, f"Execute em ordem: {lab['title']}", "Terminal na raiz do workshop, salvo indicação em contrário.")

    panel(slide, 0.82, 1.9, 7.46, 4.66, PANEL)
    textbox(slide, "COMANDOS", 1.08, 2.12, 6.9, 0.25, 11, TEAL, True)
    code = slide.shapes.add_textbox(Inches(1.08), Inches(2.5), Inches(6.93), Inches(3.82))
    set_text(code, lab["commands"], 11.2, WHITE, font=CODE_FONT)

    panel(slide, 8.58, 1.9, 3.89, 2.46, PANEL_ALT)
    textbox(slide, "VERIFIQUE", 8.86, 2.16, 3.2, 0.26, 11, TEAL, True)
    textbox(slide, lab["expected"], 8.86, 2.58, 3.2, 1.34, 14, WHITE, True)
    panel(slide, 8.58, 4.62, 3.89, 1.94, PANEL)
    textbox(slide, "TRANSIÇÃO", 8.86, 4.89, 3.1, 0.24, 11, GOLD, True)
    textbox(slide, lab["transition"], 8.86, 5.29, 3.2, 1.05, 13, WHITE)
    slide.notes_slide.notes_text_frame.text = (
        lab["notes"] + "\n\nComandos para projetar:\n" + lab["commands"]
    )


def build():
    pres = Presentation()
    pres.slide_width = Inches(13.333)
    pres.slide_height = Inches(7.5)
    pres.core_properties.title = "Guia de execução dos laboratórios OpenTofu"
    pres.core_properties.subject = "Passo a passo dos nove laboratórios em dois encontros"
    pres.core_properties.author = "Minicurso OpenTofu com Floci"
    blank = pres.slide_layouts[6]

    slide = pres.slides.add_slide(blank)
    create_cover(pres, slide, 1)
    slide = pres.slides.add_slide(blank)
    create_agenda(pres, slide, 2)

    index = 3
    for lab in LABS:
        slide = pres.slides.add_slide(blank)
        lab_intro(pres, slide, index, lab)
        index += 1
        slide = pres.slides.add_slide(blank)
        lab_run(pres, slide, index, lab)
        index += 1

    pres.save(OUTPUT)
    print(f"Generated {OUTPUT} ({len(pres.slides)} slides)")


if __name__ == "__main__":
    build()
