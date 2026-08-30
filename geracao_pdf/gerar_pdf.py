from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image,
                                Table, TableStyle, HRFlowable)

AZUL = colors.HexColor("#1b3a52")
CINZA = colors.HexColor("#4a5560")
LINHA = colors.HexColor("#dfe5ea")

doc = SimpleDocTemplate(
    "proposta_gravidez_adolescencia_poa.pdf",
    pagesize=A4,
    leftMargin=1.8 * cm, rightMargin=1.8 * cm,
    topMargin=1.2 * cm, bottomMargin=1.0 * cm,
    title="Gravidez na Adolescência em Porto Alegre: uma Análise Temporal e Territorial",
    author="Pedro Evaldt, Alexandre Raczinoski, Bruno Delgiovo",
)

titulo = ParagraphStyle("titulo", fontName="Helvetica-Bold", fontSize=13.5,
                        leading=16, alignment=TA_CENTER, textColor=AZUL)
sub = ParagraphStyle("sub", fontName="Helvetica", fontSize=8.5, leading=10,
                     alignment=TA_CENTER, textColor=CINZA)
h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=9, leading=10.5,
                   textColor=AZUL, spaceBefore=5, spaceAfter=2)
corpo = ParagraphStyle("corpo", fontName="Helvetica", fontSize=8.3, leading=10.2,
                       alignment=TA_JUSTIFY, textColor=colors.black)
item = ParagraphStyle("item", parent=corpo, leftIndent=9, bulletIndent=1,
                      spaceAfter=0.5)
celula = ParagraphStyle("celula", fontName="Helvetica", fontSize=7.8,
                        leading=9.4, textColor=colors.black)
celulab = ParagraphStyle("celulab", parent=celula, fontName="Helvetica-Bold")
legenda = ParagraphStyle("legenda", fontName="Helvetica-Oblique", fontSize=6.8,
                         leading=8.2, alignment=TA_CENTER, textColor=CINZA)

s = []

s.append(Paragraph("Gravidez na Adolescência em Porto Alegre:<br/>uma Análise Temporal e Territorial", titulo))
s.append(Spacer(1, 2))
s.append(Paragraph("Trabalho da disciplina de Banco de Dados", sub))
s.append(Spacer(1, 4))
s.append(HRFlowable(width="100%", thickness=1, color=AZUL, spaceAfter=5))

# ---- Identificação ----
dados = [
    [Paragraph("<b>Integrantes</b>", corpo),
     Paragraph("Pedro Evaldt · Alexandre Raczinoski · Bruno Delgiovo", corpo)],
    [Paragraph("<b>Líder</b>", corpo),
     Paragraph("Pedro Evaldt", corpo)],
    [Paragraph("<b>Cooperação</b>", corpo),
     Paragraph("Trabalho da disciplina", corpo)],
    [Paragraph("<b>Base de dados</b>", corpo),
     Paragraph("SINASC – Sistema de Informações sobre Nascidos Vivos (DATASUS/Ministério da Saúde), "
               "com recorte para o município de Porto Alegre. Complementada pelos indicadores "
               "territoriais do ObservaPOA / Porto Alegre em Análise (Procempa), pelos Agregados por "
               "Setores Censitários do Censo 2022 (IBGE), pelos indicadores educacionais do INEP e pelo "
               "CNES (DATASUS).", corpo)],
    [Paragraph("<b>Tecnologias</b>", corpo),
     Paragraph("PostgreSQL (SGBD relacional), Python com pandas para extração, limpeza e carga dos "
               "dados, pgAdmin/DBeaver para modelagem e consultas SQL, e Power BI para a visualização "
               "dos indicadores.", corpo)],
]
t = Table(dados, colWidths=[2.6 * cm, 14.8 * cm])
t.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (0, -1), 6),
    ("TOPPADDING", (0, 0), (-1, -1), 2),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINHA),
]))
s.append(t)

# ---- Resumo ----
s.append(Paragraph("Resumo", h))
s.append(Paragraph(
    "<b>Objetivo geral:</b> projetar e implementar um banco de dados relacional que integre os microdados "
    "do SINASC a indicadores sociais por território, permitindo analisar a evolução da gravidez na "
    "adolescência em Porto Alegre ao longo do tempo e sua correlação com as condições sociais de cada "
    "bairro e região da cidade.", corpo))
s.append(Spacer(1, 2))
s.append(Paragraph("<b>Objetivos específicos:</b>", corpo))
for txt in [
    "Extrair, limpar e padronizar os microdados do SINASC referentes a nascimentos de mães de 10 a 19 anos residentes em Porto Alegre;",
    "Integrar ao banco os indicadores sociais por bairro e Região do Orçamento Participativo, criando uma dimensão territorial hierárquica (setor censitário &#8594; bairro &#8594; região);",
    "Elaborar o modelo conceitual (DER) e o modelo lógico normalizado até a 3ª forma normal, com chaves, índices e integridade referencial;",
    "Desenvolver consultas SQL que descrevam a série temporal e a distribuição territorial do fenômeno, e que o correlacionem com os quatro eixos sociais definidos;",
    "Apresentar os resultados em visualizações que evidenciem as desigualdades intraurbanas.",
]:
    s.append(Paragraph(txt, item, bulletText="•"))

# ---- Eixos sociais ----
s.append(Paragraph("Aspectos sociais correlacionados", h))
eixos = [
    [Paragraph("<b>Eixo</b>", celulab), Paragraph("<b>Indicadores</b>", celulab),
     Paragraph("<b>Fonte</b>", celulab)],
    [Paragraph("Renda e desigualdade", celula),
     Paragraph("Rendimento mediano e razão de rendimento entre homens e mulheres", celula),
     Paragraph("ObservaPOA; Censo 2022 (IBGE)", celula)],
    [Paragraph("Escolaridade e evasão", celula),
     Paragraph("Alfabetização, anos de estudo, abandono e distorção idade-série", celula),
     Paragraph("Censo 2022 (IBGE); INEP", celula)],
    [Paragraph("Favelas e comunidades urbanas", celula),
     Paragraph("População e domicílios em favelas; características do entorno", celula),
     Paragraph("Censo 2022 (IBGE)", celula)],
    [Paragraph("Acesso à saúde", celula),
     Paragraph("Pré-natal insuficiente (menos de 7 consultas) e rede instalada", celula),
     Paragraph("ObservaPOA; SINASC; CNES", celula)],
]
te = Table(eixos, colWidths=[3.9 * cm, 8.3 * cm, 5.2 * cm])
te.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 4),
    ("RIGHTPADDING", (0, 0), (-1, -1), 4),
    ("TOPPADDING", (0, 0), (-1, -1), 2.5),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
    ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#eef2f6")),
    ("LINEBELOW", (0, 0), (-1, -2), 0.4, LINHA),
    ("BOX", (0, 0), (-1, -1), 0.5, LINHA),
]))
s.append(te)

# ---- Justificativa ----
s.append(Paragraph("Justificativa", h))
s.append(Paragraph(
    "Em 2025 nasceram cerca de 274 mil bebês de mães com até 19 anos no Brasil, 11,3% do total de "
    "nascimentos. Porto Alegre registrou 6,16%, um dos menores percentuais do país, mas esse valor médio "
    "esconde diferenças expressivas entre os bairros da cidade — daí a necessidade de uma análise ao mesmo "
    "tempo temporal e territorial. Os dados do SINASC são públicos, cobrem mais de duas décadas e são "
    "distribuídos em arquivos brutos, sem estrutura de consulta, o que justifica organizá-los em um banco "
    "relacional. Ao integrá-los a indicadores sociais de fontes distintas (IBGE, INEP, CNES e Prefeitura), "
    "o trabalho exige exatamente as etapas centrais da disciplina: modelagem conceitual e lógica, "
    "normalização, definição de chaves e integridade referencial, processo de carga (ETL) e elaboração de "
    "consultas SQL com junções, agregações e filtros sobre um volume real de registros.", corpo))

# ---- Imagem ----
s.append(Spacer(1, 5))
s.append(Image("grafico.png", width=10.2 * cm, height=4.11 * cm))
s.append(Spacer(1, 1))
s.append(Paragraph(
    "Imagem representativa do tema: proporção de nascidos vivos de mães com até 19 anos em 2025. "
    "Fontes: SINASC/Ministério da Saúde e Secretaria Municipal de Saúde de Porto Alegre.", legenda))

doc.build(s)
print("PDF 1 gerado")
