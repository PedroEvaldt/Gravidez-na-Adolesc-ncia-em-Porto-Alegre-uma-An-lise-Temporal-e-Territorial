# Dados

O que existe em `data/`, em que formato e o que já se sabe de cada arquivo. A origem dos arquivos (URL, data do download) fica em `FONTES.md`.

## Organização das pastas

```
data/raw/sinasc/DNRS{ano}.dbc        # bruto, imutável (2017–2024)
data/processed/sinasc/DNRS{ano}.dbf  # descompactado; gerado por etl/validacao/explorar_sinasc.py
```

Nenhum arquivo do Censo 2022, do ObservaPOA ou do CNES foi baixado até 2026-10-17.

## SINASC — `DNRS{ano}`

Conferido em 2026-10-17 com `etl/validacao/explorar_sinasc.py`.

### Formato e leitura

- `.dbc` é um DBF compactado. O `pyreaddbc.dbc2dbf` gera o `.dbf`, e o `dbfread` lê o resultado com `encoding="latin-1"`.
- Todas as colunas são lidas como **texto**. A largura dos campos muda entre anos, então os valores precisam de `strip()`.
- Em 2017, a coluna `contador` vem em minúsculas, e nos outros anos vem como `CONTADOR`. O leitor converte todos os nomes para maiúsculas.
- `DTNASC` vem como `DDMMAAAA`. Em todos os anos, 100% dos registros têm o ano de `DTNASC` igual ao ano do arquivo.

### Cobertura e volume

Cada arquivo traz o RS inteiro. Porto Alegre sai do filtro `CODMUNRES == '431490'`.

| Ano | Linhas (RS) | Mães residentes em POA |
|---|---|---|
| 2017 | 141.568 | 18.490 |
| 2018 | 140.047 | 17.579 |
| 2019 | 134.596 | 16.520 |
| 2020 | 130.742 | 15.687 |
| 2021 | 124.446 | 14.153 |
| 2022 | 120.942 | 13.679 |
| 2023 | 120.974 | 13.663 |
| 2024 | 111.988 | 12.850 |

**Checagem de referência:** o arquivo de 2021 tem 14.153 nascimentos, contra 14.149 da SMS. A diferença é de 4 registros, ou 0,03%.

### Colunas

São 61 colunas, **as mesmas nos 8 anos**:

`CONTADOR` `ORIGEM` `CODESTAB` `CODMUNNASC` `LOCNASC` `IDADEMAE` `ESTCIVMAE` `ESCMAE` `CODOCUPMAE` `QTDFILVIVO` `QTDFILMORT` `CODMUNRES` `GESTACAO` `GRAVIDEZ` `PARTO` `CONSULTAS` `DTNASC` `HORANASC` `SEXO` `APGAR1` `APGAR5` `RACACOR` `PESO` `IDANOMAL` `DTCADASTRO` `CODANOMAL` `NUMEROLOTE` `VERSAOSIST` `DTRECEBIM` `DIFDATA` `DTRECORIGA` `NATURALMAE` `CODMUNNATU` `CODUFNATU` `ESCMAE2010` `SERIESCMAE` `DTNASCMAE` `RACACORMAE` `QTDGESTANT` `QTDPARTNOR` `QTDPARTCES` `IDADEPAI` `DTULTMENST` `SEMAGESTAC` `TPMETESTIM` `CONSPRENAT` `MESPRENAT` `TPAPRESENT` `STTRABPART` `STCESPARTO` `TPNASCASSI` `TPFUNCRESP` `TPDOCRESP` `DTDECLARAC` `ESCMAEAGR1` `STDNEPIDEM` `STDNNOVA` `CODPAISRES` `TPROBSON` `PARIDADE` `KOTELCHUCK`

**Não existe `CODBAIRES` nem nenhum outro campo de endereço** (bairro, CEP, logradouro). O único dado territorial da residência é `CODMUNRES`. Isso está em aberto em `decisoes.md`.

### Completude das variáveis principais

Calculada sobre os nascimentos de POA. A tabela mostra o maior valor entre os 8 anos.

| Variável | % vazio (máx.) | % só noves (máx.) |
|---|---|---|
| `IDADEMAE` | 0,00 | 0,01 (2018) |
| `ESCMAE2010` | 0,03 | 0,08 (2021) |
| `RACACORMAE` | 0,06 | 0,00 |
| `CONSULTAS` | 0,00 | 0,44 (2024) |
| `CONSPRENAT` | 0,35 | 0,44 (2024) |
| `SEMAGESTAC` | 0,03 | 0,00 |
| `PESO` | 0,01 | 0,00 |

Todas as variáveis principais passam de 99% de preenchimento em todos os anos.

### Códigos e faixas encontrados

O dicionário oficial ainda não foi obtido, então esta seção lista o que aparece no dado, sem afirmar o significado.

- **Variáveis categóricas:**
  - `ESCMAE2010`: códigos 0 a 5, e 9;
  - `CONSULTAS`: códigos 1 a 4, e 9. Não aparece código 0;
  - `RACACORMAE`: códigos 1 a 5. Não aparece código 9.
- **Variáveis numéricas** (sem vazios e sem "só noves"):
  - `IDADEMAE`: 12 a 56 anos;
  - `SEMAGESTAC`: 19 a 45 semanas;
  - `PESO`: 100 a 6.035 g;
  - `CONSPRENAT`: 0 a 41 consultas.

### Em aberto

- **Dicionário:** obter o dicionário oficial do SINASC, para confirmar o significado de cada código e se o 9 é "ignorado" em cada variável.
- **Plausibilidade:** conferir valores extremos, como `PESO` de 100 g (2022) e `CONSPRENAT` de 41.
- **Atraso escolar:** `SERIESCMAE` e `DTNASCMAE` existem e podem servir para derivá-lo. A completude delas ainda não foi medida.
