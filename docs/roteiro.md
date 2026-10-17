# Roteiro — Blocos 0 a 3

**Projeto:** Gravidez na Adolescência em Porto Alegre: uma Análise Temporal e Territorial
**Grupo:** Pedro Evaldt (líder) · Alexandre Raczinoski · Bruno Delgiovo

Marque `[x]` em cada tarefa concluída. As decisões do projeto estão em `docs/decisoes.md`, e o que se sabe de cada arquivo está em `docs/dados.md`.

## Dependências

```
0 (validação) ──→ 2 (modelagem) ──→ 3.1–3.2 (território, domínios) ──→ 3.3–3.6 (fontes) ──→ 3.7 (checagens)
1 (ambiente) ──────────────────────↗
```

Os blocos 0 e 1 rodam em paralelo. No Bloco 3, os passos 3.3 a 3.6 são independentes entre si, e é ali que a divisão por pessoa rende mais.

---

## Bloco 0 — Validação dos dados

Objetivo: descobrir o que cada fonte realmente entrega antes de desenhar o modelo. Os scripts de exploração ficam em `etl/validacao/`, e cada arquivo baixado ganha uma linha em `docs/FONTES.md` (fonte, URL, arquivo, data do download, observações).

### SINASC → `data/raw/sinasc/`

**Onde buscar:** FTP do DATASUS, em `ftp.datasus.gov.br/dissemin/publicos/SINASC/1996_/Dados/DNRES/`. Os arquivos seguem o padrão `DNRS{ano}.dbc`. O download direto é feito por `etl/validacao/baixar_sinasc.py`, com `ftplib`.

O PySUS 2.x não serve para isso: a API antiga (`SINASC().load()`) não existe mais, e o catálogo dele só tem o RS até 2022.

**Como ler:** `.dbc` é um DBF compactado. O `pyreaddbc.dbc2dbf` descompacta para `.dbf` em `data/processed/`, e o `dbfread` lê o `.dbf`.

- [x] 0.1 Baixar o RS de 2017 e de 2024 (no ETL, o período inteiro)
- [x] 0.2 Filtrar mães residentes em Porto Alegre (`CODMUNRES == '431490'`)
- [x] 0.3 Conferir o volume: cerca de 13–14 mil nascimentos por ano
- [x] 0.4 Examinar o `CODBAIRES`: % preenchido por ano, nº de códigos distintos e formato
  - **2026-10-17:** a coluna **não existe** nos arquivos públicos de 2017 a 2024, que não têm nenhum campo de endereço. Ver "Fonte do bairro de residência" em `decisoes.md`.
- [ ] 0.5 Obter a **tabela que traduz código → nome de bairro**, que tende a ser municipal (depende da fonte do bairro)
- [x] 0.6 Medir a completude de `IDADEMAE`, `ESCMAE2010`, `CONSULTAS`, `CONSPRENAT`, `PESO`, `SEMAGESTAC` e `RACACORMAE`
- [x] 0.7 Confirmar se 2024 é definitivo. Se no FTP ele só aparecer na pasta de preliminares (`PRELIM`), ainda é preliminar.

### Censo 2022 → `data/raw/ibge_censo2022/`

**Onde buscar:** FTP do IBGE, em `ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/`.

- [ ] 0.8 Baixar o dicionário de dados (`.xlsx` na raiz da pasta)
- [ ] 0.9 Baixar os CSVs de `Agregados_por_Bairro_csv/` e de `Agregados_por_Setor_csv/` e filtrar Porto Alegre
- [ ] 0.10 Ver quais variáveis existem: população por idade e sexo (mulheres de 15–19), alfabetização e escolaridade, renda, favelas
- [ ] 0.11 **Comparar os bairros do `Agregados_por_Bairro` com os 94 bairros oficiais.** Se baterem, os indicadores do Censo entram direto por bairro, a mediana de renda vem pronta e a tabela `setor_censitario` pode sair do modelo.

### ObservaPOA e mapas → `data/raw/observapoa/`

**Onde buscar:** página de mapas do ObservaPOA (`prefeitura.poa.br/smpae/observapoa/mapas`). Os shapefiles estão hospedados no Google Drive.

- [ ] 0.12 Baixar o shapefile dos **bairros oficiais** → `bairros_oficiais/`
- [ ] 0.13 Baixar o shapefile das **regiões do OP** → `regioes_op/`
- [ ] 0.14 Baixar o shapefile dos **setores censitários 2022** (versão final) → `setores_2022/`
- [ ] 0.15 Baixar a **população por bairro do Censo 2022** (CSV)
- [ ] 0.16 Procurar no site a **renda por bairro** e de que ano ela é
- [ ] 0.17 Descobrir **em qual região do OP fica cada bairro**: pela tabela, se existir, ou cruzando os dois shapefiles no PostGIS

### CNES → `data/raw/cnes/`

**Onde buscar:** a base completa da área de downloads do site do CNES costuma trazer bairro, CEP e coordenadas. Como alternativa, o PySUS no grupo `ST` (arquivos mensais, por exemplo `STRS2412`), que traz CEP mas, até onde se sabe, não coordenadas.

- [ ] 0.18 Baixar os estabelecimentos de Porto Alegre e ver se trazem bairro, CEP ou latitude/longitude

### Decisão

- [ ] 0.19 Escrever `docs/validacao.md`: o que cada fonte entrega, completude e problemas encontrados
- [ ] 0.20 Fixar o período (primeiro ano com códigos novos de bairro e último ano consolidado)
- [ ] 0.21 Decidir sobre o bairro. **Se o SINASC público não servir, enviar o pedido à SMS via GAT05 imediatamente.**

**Pronto quando:** o `validacao.md` existe, e o período e a decisão do bairro estão fechados.

---

## Bloco 1 — Ambiente

Roda em paralelo ao Bloco 0.

- [ ] 1.1 Criar o repositório no GitHub com README e `.gitignore`. Ficam de fora `data/`, `.env` e `.venv/`.
- [ ] 1.2 Criar a estrutura de pastas: `data/raw`, `data/processed`, `etl/validacao`, `sql/ddl`, `sql/views`, `docs/`
- [ ] 1.3 Escrever o `docker-compose.yml`:
  - imagem `postgis/postgis`;
  - volume de dados;
  - `sql/ddl` montado em `/docker-entrypoint-initdb.d`;
  - senha lida do `.env`.
- [ ] 1.4 Criar o `.env.example` versionado
- [ ] 1.5 Criar o projeto com uv: pandas, geopandas, pysus e um driver de Postgres
- [ ] 1.6 Criar os comandos: subir o banco, rodar o ETL e resetar tudo. Precisam rodar em Python; o Makefile é opcional.
- [ ] 1.7 Testar nas três máquinas, inclusive no Windows com Docker Desktop
- [ ] 1.8 Preencher a seção "Comandos" do `CLAUDE.md`

**Pronto quando:** qualquer integrante clona o repositório e, com dois comandos, tem o banco no ar.

---

## Bloco 2 — Modelagem

Depende do `validacao.md`.

- [ ] 2.1 Listar entidades e atributos a partir da validação. Núcleo previsto:
  - **Território:** `regiao_op` ← `bairro` (← `setor_censitario`, se a tarefa 0.11 não o eliminar), com geometria
  - **Fato:** `nascimento`, com FK para `bairro`. A mãe não é entidade.
  - **Domínios:** `escolaridade`, `raca_cor`, `tipo_parto`, `faixa_consultas` etc., que traduzem os códigos do SINASC
  - **Indicadores:** uma tabela por fonte, no nível natural de cada uma
- [ ] 2.2 Montar o DER conceitual
- [ ] 2.3 Montar o modelo lógico em 3FN, com chaves, FKs e índices. O índice principal é `nascimento(id_bairro, ano)`.
- [ ] 2.4 Escrever o DDL em `sql/ddl`, em arquivos numerados
- [ ] 2.5 Revisar em grupo antes de iniciar o ETL

**Pronto quando:** o DER e o modelo lógico estão prontos como figuras para o artigo, e o DDL sobe limpo no container.

---

## Bloco 3 — ETL

Depende do DDL. Regras para todo script:

- ler de `data/raw`;
- nunca alterar o dado bruto;
- poder rodar de novo do zero com o mesmo resultado;
- registrar cada decisão em `docs/tratamento.md`.

- [ ] 3.1 **Território:** regiões; bairros com contorno e região; setores, se ficarem no modelo; registro "Não informado"
- [ ] 3.2 **Tabelas de domínio:** códigos do dicionário do SINASC
- [ ] 3.3 **SINASC (período inteiro):**
  - ler cada ano, filtrar Porto Alegre e selecionar as colunas;
  - tratar o código 9 (ignorado) como ausente, conferindo com o dicionário;
  - validar os códigos contra as tabelas de domínio;
  - derivar o ano, a faixa etária (10–14, 15–19, 20–34, 35+) e o atraso escolar;
  - traduzir o código de bairro para `id_bairro`, ou "Não informado";
  - carregar.
- [ ] 3.4 **Censo 2022:** filtrar Porto Alegre e converter os números. Valores suprimidos por sigilo (geralmente "X") viram `NULL`, não zero.
- [ ] 3.5 **ObservaPOA:** casar os nomes dos bairros com a tabela `bairro`, normalizando acentos, maiúsculas e espaços
- [ ] 3.6 **CNES:** associar cada estabelecimento a um bairro, pelo nome ou por junção espacial no PostGIS
- [ ] 3.7 **Checagens de qualidade:**
  - total de nascidos vivos por ano contra o TabNet e o boletim da SMS (referência: 14.149 em 2021);
  - nascimentos sem bairro por ano;
  - nenhuma FK órfã;
  - população do Censo por bairro próxima da população do ObservaPOA.
- [ ] 3.8 Revisar o `docs/tratamento.md`, que vira a seção de tratamento de dados do artigo

**Pronto quando:** um único comando reconstrói o banco inteiro do zero, e as checagens estão documentadas.

**Prioridade se faltar tempo:** o CNES (3.6) é a fonte que pode ficar por último.
