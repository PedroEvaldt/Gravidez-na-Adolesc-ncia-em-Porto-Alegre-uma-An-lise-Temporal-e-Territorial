# -*- coding: utf-8 -*-
"""Gera o documento de referência com as fontes de dados do trabalho."""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                TableStyle, HRFlowable, KeepTogether)

AZUL = colors.HexColor("#1b3a52")
AZUL_LINK = colors.HexColor("#1f6fb2")
CINZA = colors.HexColor("#4a5560")
LINHA = colors.HexColor("#dfe5ea")
CAB = colors.HexColor("#eef2f6")

NOME_ARQUIVO = "fontes_de_dados.pdf"

# --------------------------------------------------------------------------
# Estilos
# --------------------------------------------------------------------------
titulo = ParagraphStyle("titulo", fontName="Helvetica-Bold", fontSize=15,
                        leading=18, alignment=TA_CENTER, textColor=AZUL)
sub = ParagraphStyle("sub", fontName="Helvetica", fontSize=9, leading=11,
                     alignment=TA_CENTER, textColor=CINZA)
h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=11.5, leading=14,
                    textColor=AZUL, spaceBefore=12, spaceAfter=4)
h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=9.5, leading=12,
                    textColor=AZUL, spaceBefore=8, spaceAfter=3)
corpo = ParagraphStyle("corpo", fontName="Helvetica", fontSize=9, leading=11.6,
                       alignment=TA_JUSTIFY, spaceAfter=4)
item = ParagraphStyle("item", parent=corpo, leftIndent=10, bulletIndent=2,
                      spaceAfter=2)
nota = ParagraphStyle("nota", fontName="Helvetica-Oblique", fontSize=8.2,
                      leading=10.4, alignment=TA_JUSTIFY, textColor=CINZA,
                      leftIndent=8, spaceBefore=2, spaceAfter=4)
cel = ParagraphStyle("cel", fontName="Helvetica", fontSize=7.6, leading=9.2)
celb = ParagraphStyle("celb", parent=cel, fontName="Helvetica-Bold")


def link(texto, url):
    """Devolve o texto como hyperlink clicável."""
    return ('<link href="%s"><font color="#1f6fb2"><u>%s</u></font></link>'
            % (url, texto))


def tabela(linhas):
    """Monta a tabela padrão de fontes (5 colunas)."""
    dados = [[Paragraph(c, celb) for c in
              ("Indicador", "Fonte", "Onde pegar", "Menor recorte", "Formato")]]
    for l in linhas:
        dados.append([Paragraph(c, cel) for c in l])
    t = Table(dados, colWidths=[4.9 * cm, 3.3 * cm, 4.6 * cm, 2.5 * cm, 2.1 * cm],
              repeatRows=1)
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 4),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ("BACKGROUND", (0, 0), (-1, 0), CAB),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINHA),
        ("BOX", (0, 0), (-1, -1), 0.5, LINHA),
    ]))
    return t


# --------------------------------------------------------------------------
# URLs
# --------------------------------------------------------------------------
U = {
    "poa_analise": "https://portoalegreemanalise.procempa.com.br/",
    "observapoa": "http://www.observapoa.com.br/",
    "observapoa_shapes": "http://observapoa.com.br/default.php?p_secao=46&reg=259",
    "dados_poa": "https://dadosabertos.poa.br/",
    "rop": "https://dadosabertos.poa.br/dataset/regioes-do-orcamento-participativo-rop",
    "mapas_poa": "https://prefeitura.poa.br/smamus/planejamento-urbano/mapas-digitais",
    "censo_down": "https://censo2022.ibge.gov.br/panorama/downloads.html",
    "censo_divulg": "https://censo2022.ibge.gov.br/pt/etapas/divulgacao-dos-resultados.html",
    "censo_ibge": "https://www.ibge.gov.br/estatisticas/sociais/saude/22827-censo-demografico-2022.html",
    "inep_abertos": "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos",
    "inep_censo": "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar",
    "inep_distorcao": "https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/indicadores-educacionais/taxas-de-distorcao-idade-serie",
    "cnes": "https://cnes.datasus.gov.br/pages/downloads/arquivosBaseDados.jsp",
    "cnes_estab": "https://estabelecimentos.datasus.gov.br/pages/downloads/arquivosBaseDados.jsp",
    "tabnet": "http://tabnet.datasus.gov.br",
    "bd_sinasc": "https://basedosdados.org/dataset/48ccef51-8207-40ee-af5b-134c8ac3fb8c",
    "bd_cnes": "https://basedosdados.org/dataset/354d6d98-bc09-4e22-a58a-e4eac3a5283c",
    "pcdas": "https://pcdas.icict.fiocruz.br/conjunto-de-dados/sistema-de-informacao-sobre-nascidos-vivos/dicionario-de-variaveis/",
}

doc = SimpleDocTemplate(
    NOME_ARQUIVO, pagesize=A4,
    leftMargin=1.8 * cm, rightMargin=1.8 * cm,
    topMargin=1.5 * cm, bottomMargin=1.4 * cm,
    title="Fontes de dados – Gravidez na Adolescência em Porto Alegre",
    author="Pedro Evaldt, Alexandre Raczinoski, Bruno Delgiovo",
)

s = []

# --------------------------------------------------------------------------
# Capa / cabeçalho
# --------------------------------------------------------------------------
s.append(Paragraph("Fontes de Dados", titulo))
s.append(Spacer(1, 3))
s.append(Paragraph("Gravidez na Adolescência em Porto Alegre: uma Análise Temporal e Territorial<br/>"
                   "Trabalho da disciplina de Banco de Dados — Pedro Evaldt, Alexandre Raczinoski e Bruno Delgiovo", sub))
s.append(Spacer(1, 6))
s.append(HRFlowable(width="100%", thickness=1, color=AZUL, spaceAfter=8))

s.append(Paragraph(
    "Este documento reúne as bases de dados utilizadas no projeto, os indicadores extraídos de cada uma, "
    "o menor recorte territorial disponível, o formato dos arquivos e os endereços de download. Todos os "
    "links são clicáveis.", corpo))

# --------------------------------------------------------------------------
# 1. Bases principais
# --------------------------------------------------------------------------
s.append(Paragraph("1. Bases principais", h1))

s.append(Paragraph("1.1 SINASC / DATASUS — base central do trabalho", h2))
s.append(Paragraph(
    "Sistema de Informações sobre Nascidos Vivos, do Ministério da Saúde. As secretarias de saúde coletam "
    "as Declarações de Nascido Vivo (DN) nos hospitais e cartórios, lançam os dados no SINASC, e o "
    "Ministério consolida a base nacional redistribuindo os registros pelo local de residência da mãe. "
    "Cada linha corresponde a um nascimento, com cerca de 30 variáveis, e a série pública começa em 1996. "
    "O recorte do trabalho é feito pelo código do município de residência de Porto Alegre (431490).", corpo))
s.append(Paragraph(
    "<b>Variáveis de interesse:</b> IDADEMAE, ESCMAE / ESCMAE2010, RACACORMAE, ESTCIVMAE, CONSULTAS / "
    "CONSPRENAT, CODOCUPMAE, QTDFILVIVO, PARTO, PESO, GESTACAO, DTNASC, CODMUNRES.", corpo))
s.append(Paragraph("Onde pegar: " + link("Base dos Dados — SINASC tratado", U["bd_sinasc"]) +
                   " · " + link("Dicionário de variáveis (PCDaS/Fiocruz)", U["pcdas"]) +
                   " · " + link("TabNet/DATASUS (dados já agregados)", U["tabnet"]), corpo))
s.append(Paragraph(
    "Limitação importante: o menor nível geográfico dos microdados públicos é o município. Não há bairro. "
    "Toda a análise territorial dentro de Porto Alegre depende das fontes das seções seguintes.", nota))

s.append(Paragraph("1.2 ObservaPOA / Porto Alegre em Análise (Procempa)", h2))
s.append(Paragraph(
    "Observatório da Prefeitura de Porto Alegre. Disponibiliza indicadores sociais georreferenciados, "
    "organizados por bairro e por Região do Orçamento Participativo, com séries históricas e comparações "
    "intraurbanas. É a fonte que viabiliza o recorte territorial do trabalho. Os dados vêm agregados "
    "(percentuais por território), não como microdados.", corpo))
s.append(Paragraph("Onde pegar: " + link("Porto Alegre em Análise", U["poa_analise"]) +
                   " · " + link("ObservaPOA", U["observapoa"]) +
                   " · " + link("Geoprocessamento, arquivos e shapes", U["observapoa_shapes"]), corpo))
s.append(Paragraph(
    "Duas ressalvas a registrar no trabalho: o total de nascidos vivos da cidade é maior que a soma dos "
    "valores por bairro e região, porque alguns registros não têm endereço que permita localizá-los; e os "
    "dados vêm do próprio DATASUS, podendo sofrer alterações por atualizações na base de origem.", nota))

s.append(Paragraph("1.3 IBGE — Censo Demográfico 2022", h2))
s.append(Paragraph(
    "Fornece os denominadores populacionais (necessários para calcular taxas em vez de proporções) e os "
    "indicadores socioeconômicos por território. Os resultados foram divulgados para Brasil, regiões, "
    "estados, municípios, distritos, subdistritos, bairros e setores censitários.", corpo))
s.append(Paragraph("Onde pegar: " + link("Downloads do Censo 2022", U["censo_down"]) +
                   " · " + link("Divulgação dos resultados", U["censo_divulg"]) +
                   " · " + link("Página do Censo no portal do IBGE", U["censo_ibge"]), corpo))

# --------------------------------------------------------------------------
# 2. Eixos sociais
# --------------------------------------------------------------------------
s.append(Paragraph("2. Indicadores sociais por território", h1))

# --- Renda ---
s.append(Paragraph("2.1 Renda e desigualdade", h2))
s.append(tabela([
    ("Rendimento mediano; razão de rendimento entre homens e mulheres",
     "ObservaPOA / Procempa",
     link("Porto Alegre em Análise", U["poa_analise"]) + " &#8594; Regiões e seus Indicadores",
     "Bairro e Região do OP", "Consulta / tabela"),
    ("Rendimento por domicílio e por pessoa",
     "IBGE — Censo 2022, Agregados por Setores Censitários",
     link("Downloads do Censo 2022", U["censo_down"]) + " (divulgação de 14/11/2024)",
     "Setor censitário", "CSV"),
    ("Rendimento por município",
     "IBGE — SIDRA / Panorama",
     link("Downloads do Censo 2022", U["censo_down"]),
     "Município", "CSV / XLSX"),
]))
s.append(Paragraph(
    "Atenção: a primeira divulgação dos Agregados por Setores Censitários saiu com um conjunto reduzido de "
    "variáveis, para preservar o sigilo em caso de mudança nas geometrias dos setores; o IBGE informou que "
    "a divulgação seguinte, sobre a malha definitiva, incluiria as demais variáveis e cruzamentos. "
    "Confirmar se a variável de rendimento já consta no arquivo antes de modelar em cima dela. "
    "Se não constar, o ObservaPOA supre a necessidade.", nota))

# --- Escolaridade ---
s.append(Paragraph("2.2 Escolaridade e evasão escolar", h2))
s.append(tabela([
    ("Taxas de abandono, aprovação e reprovação",
     "INEP — Indicadores Educacionais",
     link("Dados abertos do INEP", U["inep_abertos"]),
     "Escola", "XLSX"),
    ("Taxa de distorção idade-série",
     "INEP",
     link("Taxas de distorção idade-série", U["inep_distorcao"]),
     "Escola", "XLSX"),
    ("Matrículas, endereço da escola, dependência administrativa",
     "INEP — Censo Escolar",
     link("Microdados do Censo Escolar", U["inep_censo"]),
     "Escola", "CSV (arquivos grandes)"),
    ("Alfabetização e anos de estudo da população",
     "IBGE — Censo 2022",
     link("Downloads do Censo 2022", U["censo_down"]),
     "Setor censitário", "CSV"),
    ("Escolaridade da mãe",
     "SINASC",
     link("Base dos Dados — SINASC", U["bd_sinasc"]),
     "Registro individual", "DBC / CSV"),
]))
s.append(Paragraph(
    "Este é o eixo mais caro do projeto: os dados do INEP são por escola, não por bairro. Para agregar por "
    "território é preciso geocodificar o endereço das escolas (disponível nos microdados do Censo Escolar) "
    "e cruzar com a malha de bairros. A alternativa de baixo custo é usar apenas a escolaridade da mãe, "
    "que já vem no SINASC.", nota))

# --- Favelas ---
s.append(Paragraph("2.3 Favelas e comunidades urbanas", h2))
s.append(tabela([
    ("População e domicílios em favelas e comunidades urbanas",
     "IBGE — Censo 2022",
     link("Downloads do Censo 2022", U["censo_down"]) + " (divulgação de 08/11/2024)",
     "Favela / comunidade e setor", "CSV"),
    ("Características urbanísticas do entorno dos domicílios",
     "IBGE — Censo 2022",
     link("Downloads do Censo 2022", U["censo_down"]) + " (divulgação de 24/10/2025)",
     "Setor censitário", "CSV"),
    ("Malha georreferenciada dos setores de favela",
     "IBGE",
     link("Divulgação dos resultados", U["censo_divulg"]),
     "Setor censitário", "Shapefile / GeoPackage"),
    ("AEIS — Áreas Especiais de Interesse Social",
     "Prefeitura de POA / SMAMUS",
     link("Mapas digitais", U["mapas_poa"]),
     "Polígono", "Shapefile / PDF"),
]))
s.append(Paragraph(
    "Detalhe metodológico que convém citar: o IBGE identificou 2.298 favelas e comunidades urbanas cujo "
    "total estimado de domicílios ficou entre 21 e 50, e para essas áreas não foram divulgadas informações "
    "específicas, porque não puderam ser definidas em setores censitários próprios. A cobertura, portanto, "
    "não é total.", nota))

# --- Saúde ---
s.append(Paragraph("2.4 Acesso à saúde", h2))
s.append(tabela([
    ("% de nascidos vivos cujas mães fizeram menos de 7 consultas de pré-natal",
     "ObservaPOA (calculado sobre o DATASUS)",
     link("Porto Alegre em Análise", U["poa_analise"]),
     "Bairro e Região do OP", "Consulta / tabela"),
    ("Número de consultas de pré-natal por nascimento",
     "SINASC",
     link("Base dos Dados — SINASC", U["bd_sinasc"]),
     "Registro individual", "DBC / CSV"),
    ("Estabelecimentos de saúde com endereço e tipo",
     "CNES / DATASUS",
     link("Downloads da base do CNES", U["cnes"]),
     "Estabelecimento", "Arquivos mensais"),
    ("Consultas agregadas prontas",
     "DATASUS — TabNet",
     link("tabnet.datasus.gov.br", U["tabnet"]),
     "Município", "Tabela / CSV"),
    ("CNES já tratado e consultável em SQL",
     "Base dos Dados",
     link("Dataset do CNES", U["bd_cnes"]),
     "Estabelecimento", "BigQuery / CSV"),
]))

# --------------------------------------------------------------------------
# 3. Chaves territoriais
# --------------------------------------------------------------------------
s.append(Paragraph("3. Chaves de integração territorial", h1))
s.append(Paragraph(
    "As fontes usam recortes diferentes: o SINASC agrega por município, o ObservaPOA por bairro e Região "
    "do OP, o IBGE por setor censitário e o INEP por escola. Para integrá-las, o banco precisa de uma "
    "dimensão territorial hierárquica — <b>setor censitário &#8594; bairro &#8594; Região do OP</b> — com "
    "todas as tabelas de indicadores apontando para ela por chave estrangeira. Esta é a decisão de "
    "modelagem mais importante do projeto.", corpo))
for txt in [
    "<b>Bairro &#8594; Região do OP:</b> lista de bairros por região em PDF e XLS em " +
    link("Geoprocessamento, arquivos e shapes (ObservaPOA)", U["observapoa_shapes"]) +
    ". A espacialização vigente foi aprovada pelo Conselho do OP em 09/04/2019, alinhando as regiões aos "
    "bairros oficiais da Lei Complementar 12.112/2016 — delimitações anteriores ainda circulam e não devem "
    "ser usadas.",
    "<b>Setor censitário &#8594; bairro:</b> cada setor do Censo 2022 já vem vinculado a município, "
    "distrito, subdistrito e bairro, de modo que o próprio arquivo do IBGE traz a chave.",
    "<b>Malhas geográficas:</b> shapefiles de bairros e das Regiões do OP em " +
    link("Mapas digitais da SMAMUS", U["mapas_poa"]) + " e em " +
    link("Dados Abertos POA — ROP", U["rop"]) + ".",
]:
    s.append(Paragraph(txt, item, bulletText="•"))

# --------------------------------------------------------------------------
# 4. Observações metodológicas
# --------------------------------------------------------------------------
s.append(Paragraph("4. Observações metodológicas", h1))
s.append(Paragraph(
    "<b>Falácia ecológica.</b> Correlacionar o percentual de gravidez adolescente de um bairro com a renda "
    "média desse bairro produz uma conclusão sobre o território, não sobre as pessoas. A redação correta é "
    "\"bairros de menor renda apresentam maiores proporções\", e não \"adolescentes de menor renda "
    "engravidam mais\". A diferença é substantiva e deve constar na análise.", corpo))
s.append(Paragraph(
    "<b>Compatibilidade temporal.</b> As fontes têm periodicidades distintas: o SINASC é anual e "
    "atualizado com defasagem; o Censo é decenal; os indicadores do ObservaPOA nem sempre acompanham o "
    "ano mais recente. O ano de referência deve ser um atributo explícito em cada tabela de indicadores, "
    "e não um pressuposto.", corpo))
s.append(Paragraph(
    "<b>Formato .dbc.</b> Os microdados originais do DATASUS usam um formato compactado próprio, que não "
    "abre diretamente no pandas. As versões já tratadas da Base dos Dados e da PCDaS/Fiocruz evitam esse "
    "problema.", corpo))

# --------------------------------------------------------------------------
# 5. Índice de links
# --------------------------------------------------------------------------
s.append(Paragraph("5. Índice de links", h1))
indice = [
    ("Porto Alegre em Análise (ObservaPOA/Procempa)", U["poa_analise"]),
    ("ObservaPOA", U["observapoa"]),
    ("ObservaPOA — Geoprocessamento, arquivos e shapes", U["observapoa_shapes"]),
    ("Dados Abertos Porto Alegre", U["dados_poa"]),
    ("Dados Abertos POA — Regiões do Orçamento Participativo", U["rop"]),
    ("Prefeitura de POA / SMAMUS — Mapas digitais", U["mapas_poa"]),
    ("IBGE — Censo 2022, downloads", U["censo_down"]),
    ("IBGE — Censo 2022, divulgação dos resultados", U["censo_divulg"]),
    ("IBGE — Censo Demográfico 2022", U["censo_ibge"]),
    ("INEP — Dados abertos", U["inep_abertos"]),
    ("INEP — Microdados do Censo Escolar", U["inep_censo"]),
    ("INEP — Taxas de distorção idade-série", U["inep_distorcao"]),
    ("CNES/DATASUS — Downloads da base de dados", U["cnes"]),
    ("CNES/DATASUS — Estabelecimentos, downloads", U["cnes_estab"]),
    ("DATASUS — TabNet", U["tabnet"]),
    ("Base dos Dados — SINASC", U["bd_sinasc"]),
    ("Base dos Dados — CNES", U["bd_cnes"]),
    ("PCDaS/Fiocruz — Dicionário de variáveis do SINASC", U["pcdas"]),
]
linhas_idx = [[Paragraph("<b>Fonte</b>", celb), Paragraph("<b>Endereço</b>", celb)]]
for nome, url in indice:
    linhas_idx.append([Paragraph(nome, cel), Paragraph(link(url, url), cel)])
ti = Table(linhas_idx, colWidths=[7.0 * cm, 10.4 * cm], repeatRows=1)
ti.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ("BACKGROUND", (0, 0), (-1, 0), CAB),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINHA),
    ("BOX", (0, 0), (-1, -1), 0.5, LINHA),
]))
s.append(ti)

doc.build(s)
print("PDF 2 gerado")
