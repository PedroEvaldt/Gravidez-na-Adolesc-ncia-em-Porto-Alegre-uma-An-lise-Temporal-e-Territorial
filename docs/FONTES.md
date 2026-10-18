# Fontes

Origem de cada arquivo em `data/raw/`. Cada download novo ganha uma linha aqui. O conteúdo dos arquivos (colunas, códigos, problemas) fica em `dados.md`.

## SINASC (DATASUS)

| Arquivo | URL | Download | Observações |
|---|---|---|---|
| `sinasc/DNRS2017.dbc` … `sinasc/DNRS2024.dbc` (8 arquivos, um por ano) | `ftp://ftp.datasus.gov.br/dissemin/publicos/SINASC/1996_/Dados/DNRES/` | 2026-10-16 | Nascidos vivos por residência da mãe, RS inteiro. Baixados por `etl/validacao/baixar_sinasc.py` (`ftplib`, acesso anônimo). |

- **2024 é definitivo.** Em 2026-10-17, `DNRS2024` estava na pasta `DNRES` (consolidados), e a pasta `PRELIM/DNRES/` só trazia 2025 e 2026.
- **Por que não o PySUS:** a API antiga (`SINASC().load()`) não existe no PySUS 2.x, e o catálogo dele só tem o RS até 2022.

Hashes SHA-256, para saber se o DATASUS republicou algum arquivo:

```
4feb0730a75b2e0a0696bfe4a8f1f12d545221eb85dd0e399dd35accd8aada4f  DNRS2017.dbc
163fd8dbd77d1b43c3f1f4dde4b5e438e23914060f1189c8e54a6b769e3a3c3d  DNRS2018.dbc
10bcb14df033be6e8af0b7993a964ae5b151ef06a16de6a7d13ba6cb5c0c7dc7  DNRS2019.dbc
fa3198cedbbad419c0e7dff4acab43d944587305722720d7787de04edefa4985  DNRS2020.dbc
6eff8462df09ad9ece5e4dad13607538d6d708e7c6119326e63cf66072c08bce  DNRS2021.dbc
21d160971419a6c69fc44e155f5c69f404fdb1656e39d7020ea9c9e7b212384c  DNRS2022.dbc
cd90645b1fc4e2fb55c5aea91dc18d65edff1d1ed937af8ba27530982b410b9d  DNRS2023.dbc
72efcc8f2e4ed17c4932479658b2a09a4dbb1d9bf19a49227610c5b24315a4c8  DNRS2024.dbc
```

## Censo 2022 (IBGE)

Ainda não baixado (etapas 9–12 do roteiro).

## ObservaPOA

Ainda não baixado (etapas 5, 6, 12 e 13 do roteiro).

## CNES

Ainda não baixado (etapa 37 do roteiro).
