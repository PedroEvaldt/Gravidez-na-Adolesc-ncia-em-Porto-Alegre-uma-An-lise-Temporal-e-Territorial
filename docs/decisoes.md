# Decisões

Registro das decisões do grupo. Uma decisão só entra como **decidida** depois de confirmada. Propostas e problemas ainda sem resposta ficam em **Em aberto**. As decisões de limpeza e transformação dos dados ficam em `tratamento.md`.

## Em aberto

### Fonte do bairro de residência

- **Aberta em:** 2026-10-17
- **Problema:** os arquivos públicos do SINASC (`DNRS2017` a `DNRS2024`) não têm `CODBAIRES` nem nenhum campo de endereço, e o único dado territorial é `CODMUNRES` (ver `dados.md`). Sem bairro no nascimento, não dá para fazer as análises por bairro nem por região do OP.
- **Decisões afetadas:**
  - "Território" (o bairro como nível de integração);
  - "Nascimentos sem bairro válido";
  - os dois recortes de análise;
  - o índice `nascimento(id_bairro, ano)`.
- **Opções levantadas:**
  - **A. Pedir à SMS os microdados com bairro, pelo GAT05.** O GAT05 é o grupo de Indicadores do PET-Saúde Digital (MS/MEC), atividade de extensão feita junto com este trabalho. Mantém o modelo como está, mas depende do prazo de resposta.
  - **B. Usar dado já agregado por bairro**, de um TabNet municipal ou do ObservaPOA, caso exista. Ainda não foi confirmado que algum dos dois publique nascidos vivos por bairro. Muda o modelo: o bairro deixa de ser atributo de cada nascimento.
  - As duas opções não se excluem: B pode ser o plano de contingência de A.
- **O que se apurou em 2026-10-17:**
  - **Opção A:** num recurso de LAI de 2025 (Decisão CMRI 01/2025, sobre o SIM), a SMS informou que só libera banco de dados para análise mediante projeto de pesquisa tramitado no Comitê de Ética em Pesquisa (CEP) da Prefeitura, por se tratar de dados sensíveis. O pedido de tabulação foi negado com base no art. 13, III, do Decreto 7.724/2012, que dispensa o órgão de atender pedidos que exijam "trabalhos adicionais de consolidação". Se valer o mesmo para o SINASC, o microdado com bairro depende do CEP.
  - **Opção B:**
    - a SMS publica um painel de Nascidos Vivos em Power BI (`indicadores.procempa.com.br/nascidosvivos`). Ainda não se sabe se ele tem recorte por bairro, idade da mãe e ano, nem se permite exportar os dados;
    - a planilha VITAIS da SMS tinha uma variável de bairro (manual de 2015), mas não aparece mais na página de Eventos Vitais;
    - o boletim de nascidos vivos de set/2025 só traz recorte por distrito sanitário.
- **Pedido à SMS:** enviado pelo GAT05. O Pedro informou o envio em 2026-10-17. Aguardando resposta.
- **Próximo passo:**
  - registrar aqui o que foi pedido (microdado ou agregado, quais variáveis) e a data exata do envio;
  - abrir o painel de Nascidos Vivos e verificar se ele tem bairro, idade da mãe e ano, como plano de contingência.

### Limites do período

- **Aberta em:** 2026-10-17
- **Situação:**
  - **fim em 2024:** confirmado. Em 2026-10-17, `DNRS2024` estava na pasta de dados consolidados do DATASUS, e só 2025 e 2026 estavam em `PRELIM`;
  - **início em 2017:** ainda depende da fonte do bairro. A justificativa era ser o primeiro ano com a codificação nova de bairros, o que só vale se a fonte do bairro usar essa codificação.

## Decididas

Estas decisões foram fechadas pelo grupo antes de 2026-10-17 e registradas aqui nessa data. Os motivos são os que constavam no registro original.

| Tema | Decisão | Motivo |
|---|---|---|
| Período | 2017–2024 (limites ainda em validação, ver acima) | Lei dos Bairros de 2016 no início; último ano consolidado do SINASC no fim |
| Recorte do SINASC | Todos os nascimentos de mães residentes em POA (`CODMUNRES = '431490'`), não só os de adolescentes; a faixa etária é filtro de consulta, não corte do ETL | — |
| Faixas etárias da mãe | 10–14, 15–19, 20–34, 35+ | — |
| Indicador principal | Proporção: nascidos vivos de mães de 10–19 ÷ total de nascidos vivos × 100, na série inteira | — |
| Indicador secundário | Taxa de fecundidade: nascidos vivos de mães de 15–19 ÷ mulheres de 15–19 × 1000, só no triênio 2021–2023 | O denominador vem do Censo 2022 |
| Recorte temporal | Série por região do OP (17 regiões) | — |
| Recorte territorial | Bairro (94 oficiais), triênio 2021–2023 somado | Números pequenos por bairro em cada ano |
| Território | `regiao_op` ← `bairro` ← `setor_censitario`; o bairro integra as fontes | Os setores podem sair se os agregados do Censo por bairro baterem com os 94 bairros (etapa 11 do roteiro) |
| Sem bairro válido | Registro "Não informado": entra nos totais da cidade, fica fora das análises territoriais | — |
| Mãe | Não é entidade; os dados dela são atributos do nascimento | O SINASC não identifica a mãe |
| Medianas | Não são agregadas de setor para bairro; usa-se o valor publicado por bairro | Mediana não se soma |
| Fontes | SINASC, Censo 2022, ObservaPOA, CNES. INEP fora | — |
| Escolaridade | Atraso escolar das mães adolescentes (SINASC) e escolaridade da população do bairro (Censo 2022) | — |
| Visualização | Power BI consumindo views SQL; a lógica dos indicadores fica no Postgres, nunca em DAX | — |
