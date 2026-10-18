# Roteiro

**Projeto:** Gravidez na Adolescência em Porto Alegre: uma Análise Temporal e Territorial
**Execução:** Pedro Evaldt, com revisão do Claude Code

Marque `[x]` ao concluir cada etapa. As decisões do projeto estão em `docs/decisoes.md`, e o que se sabe de cada arquivo está em `docs/dados.md`.

## Como trabalhamos

Uma etapa por vez, sempre neste ciclo:

1. **Pedro** escreve o código da etapa.
2. **Claude** revisa e roda: corretude, convenções do projeto, idempotência e funcionamento em qualquer sistema. Aponta os problemas com perguntas, em vez de reescrever o código.
3. **Claude** monta os testes, quando a etapa pede.
4. **Claude** registra em `docs/` o que a etapa descobriu ou decidiu.
5. A caixa é marcada e as mudanças são commitadas.

Regras para todo script:
- ler de `data/raw` e nunca alterar o dado bruto;
- rodar de novo do zero com o mesmo resultado;
- montar os caminhos com `pathlib`.

## Situação atual

Os arquivos públicos do SINASC não têm bairro. O pedido à SMS foi enviado pelo GAT05 em 2026-10-17. Até a resposta chegar, os nascimentos entram como "Não informado", e o resto do trabalho segue normalmente. As etapas que dependem da resposta estão na Fase 8.

---

## Fase 0 — Exploração inicial do SINASC

- [x] 0. Baixar o RS de 2017 a 2024, filtrar Porto Alegre, conferir volume e completude, confirmar que 2024 é definitivo e examinar o `CODBAIRES`. Resultado: a coluna não existe nos arquivos públicos. Detalhes em `dados.md`.

## Fase 1 — Arrumação e ambiente

- [ ] 1. **Dependências e `.gitignore`**
  - declarar no `pyproject.toml` o que os scripts usam (`pandas`, `dbfread`, `pyreaddbc`), e o `pytest` como dependência de desenvolvimento;
  - apagar o `main.py` gerado pelo `uv init`;
  - acrescentar `.venv/` ao `.gitignore` e conferir se `claude/` devia ser `.claude/`;
  - commitar a mudança dos PDFs para `docs/apresentacao/`.
  - **Pronto quando:** `uv sync` instala tudo, e o `git status` está limpo.
- [ ] 2. **Corrigir o `baixar_sinasc.py`**
  - criar a pasta de destino certa: hoje o script cria `data/raw`, e não `data/raw/sinasc`;
  - não deixar arquivo pela metade quando o download cair;
  - só baixar dentro de `if __name__ == "__main__":`.
  - **Pronto quando:** baixar para uma pasta vazia gera os 8 arquivos com os mesmos hashes de `FONTES.md`.
- [ ] 3. **Docker Compose**
  - `docker-compose.yml` com a imagem `postgis/postgis` em versão fixa, um volume nomeado, `sql/ddl` montado em `/docker-entrypoint-initdb.d` e a senha lida do `.env`;
  - `.env.example` versionado e `.env` local.
  - **Pronto quando:** `docker compose up -d` sobe o banco, e `SELECT postgis_full_version();` responde.
- [ ] 4. **Conexão do Python com o banco**
  - escolher o driver. Sugestão: `psycopg` 3 com SQLAlchemy e GeoAlchemy2, que o geopandas usa para gravar geometria;
  - criar um módulo em `etl/` com uma função que lê o `.env` e devolve a conexão.
  - **Pronto quando:** um teste marcado `banco` conecta e roda `SELECT 1`.

## Fase 2 — Território

Os mapas ficam na página do ObservaPOA (`prefeitura.poa.br/smpae/observapoa/mapas`), com os shapefiles hospedados no Google Drive. O download é manual, e cada arquivo vai para `FONTES.md`.

- [ ] 5. **Bairros oficiais:** baixar o shapefile para `data/raw/observapoa/bairros_oficiais/` e explorar com geopandas: número de polígonos (o esperado é 94), colunas, sistema de coordenadas e nomes.
- [ ] 6. **Regiões do OP:** baixar para `data/raw/observapoa/regioes_op/` e explorar (o esperado é 17).
- [ ] 7. **Bairro → região:** descobrir a região de cada bairro, por uma tabela se existir ou por junção espacial. Conferir se algum bairro cai em mais de uma região.
- [ ] 8. **Normalização de nomes:** escrever uma função que normaliza nomes de bairro (acentos, maiúsculas, espaços), num módulo reaproveitável de `etl/`. Vai ser a primeira função com testes.

## Fase 3 — Censo 2022 e ObservaPOA

O Censo fica em `ftp.ibge.gov.br/Censos/Censo_Demografico_2022/Agregados_por_Setores_Censitarios/`.

- [ ] 9. **Baixar por script** o dicionário (o `.xlsx` na raiz da pasta) e os CSVs de `Agregados_por_Bairro_csv/`, para `data/raw/ibge_censo2022/`.
- [ ] 10. **Explorar os agregados por bairro de Porto Alegre:** quais variáveis existem (mulheres de 15–19, alfabetização e escolaridade, renda, favelas) e como vêm os valores suprimidos por sigilo.
- [ ] 11. **Comparar os bairros do Censo com os 94 oficiais**, usando a função da etapa 8. Se baterem, a tabela `setor_censitario` sai do modelo.
- [ ] 12. **Só se a etapa 11 não fechar:** baixar os setores de 2022 (shapefile do ObservaPOA e `Agregados_por_Setor_csv/`) e planejar a agregação por bairro.
- [ ] 13. **ObservaPOA:** baixar a população por bairro do Censo 2022 e procurar a renda por bairro, verificando de que ano ela é. Casar os nomes com os bairros oficiais.

## Fase 4 — Fechamento da validação

- [ ] 14. **Dicionário do SINASC:**
  - obter o dicionário oficial;
  - confirmar os códigos de `ESCMAE2010`, `CONSULTAS`, `RACACORMAE` e `PARTO`, e o que o 9 significa em cada um;
  - medir a completude de `PARTO`, `SERIESCMAE` e `DTNASCMAE`;
  - olhar os valores extremos de `PESO` e `CONSPRENAT`.
- [ ] 15. **`validacao.md` e período:** o Claude redige o `validacao.md` e o Pedro revisa. O período fica fixado em `decisoes.md`.

## Fase 5 — Modelagem

- [ ] 16. Listar entidades e atributos: o Pedro propõe e o Claude questiona.
- [ ] 17. Montar o DER conceitual, como figura para o artigo.
- [ ] 18. Montar o modelo lógico em 3FN, com chaves, FKs e índices.
- [ ] 19. Escrever `sql/ddl/01_territorio.sql` e ver o esquema subir limpo no container.
- [ ] 20. Escrever `sql/ddl/02_dominios.sql`.
- [ ] 21. Escrever `sql/ddl/03_nascimento.sql`, com a FK para `bairro` e o registro "Não informado".
- [ ] 22. Escrever `sql/ddl/04_indicadores.sql`, para o Censo e o ObservaPOA.

## Fase 6 — ETL

- [ ] 23. Carregar o território: regiões, bairros com geometria e o registro "Não informado".
- [ ] 24. Carregar os domínios.
- [ ] 25. SINASC: escrever as funções de transformação (código 9 → ausente, faixa etária, atraso escolar).
- [ ] 26. SINASC: carregar 2017–2024, com todos os nascimentos em "Não informado" até a resposta da SMS.
- [ ] 27. Censo: carregar por bairro, com os valores suprimidos ("X") virando `NULL`.
- [ ] 28. ObservaPOA: carregar os indicadores por bairro.
- [ ] 29. Criar um comando único, em Python, que reconstrói o banco do zero.
- [ ] 30. **Checagens de qualidade:**
  - total por ano contra a referência (14.149 em 2021);
  - nenhuma FK órfã;
  - população do Censo próxima da do ObservaPOA em cada bairro.

## Fase 7 — Views que já funcionam sem o bairro

- [ ] 31. View da proporção de nascidos vivos de mães de 10–19 anos, por ano, na cidade (2017–2024).
- [ ] 32. View da taxa de fecundidade de 15–19 anos na cidade, no triênio 2021–2023.

## Fase 8 — Quando chegar o dado da SMS

Entra assim que a resposta chegar, mesmo que interrompa a ordem das fases.

- [ ] 33. Explorar o arquivo recebido: formato, códigos de bairro e completude.
- [ ] 34. Montar a tabela que traduz o código da SMS para o bairro oficial.
- [ ] 35. Ligar os nascimentos aos bairros e refazer as checagens.
- [ ] 36. Criar as views por região do OP (série temporal) e por bairro (triênio 2021–2023).

## Fase 9 — Fechamento

- [ ] 37. **CNES, se der tempo:** baixar os estabelecimentos de Porto Alegre e associar cada um a um bairro. Há duas fontes possíveis: a base completa do site do CNES, que costuma trazer bairro, CEP e coordenadas, e os arquivos mensais `STRS{aamm}` do PySUS.
- [ ] 38. Revisar o `tratamento.md`, que vira a seção de tratamento de dados do artigo.
