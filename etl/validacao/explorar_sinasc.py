from pathlib import Path

import pandas as pd
from dbfread import DBF
from pyreaddbc import dbc2dbf

ANOS = list(range(2017, 2025))
BASE = Path(__file__).resolve().parents[2]
RAW = BASE / "data" / "raw" / "sinasc"
PROCESSED = BASE / "data" / "processed" / "sinasc"

COD_POA = "431490"  # texto, não número
TOTAL_SMS_2021 = 14_149  # nascidos vivos de mães residentes em POA, segundo a SMS

# Variáveis com códigos fixos: a tabela mostra cada código por ano
CATEGORICAS = ["ESCMAE2010", "CONSULTAS", "RACACORMAE"]
# Variáveis com valor livre (idade, semanas, gramas): a tabela mostra mínimo e máximo
NUMERICAS = ["IDADEMAE", "CONSPRENAT", "SEMAGESTAC", "PESO"]


def ler_ano(ano: int) -> pd.DataFrame:
    """Lê o DNRS de um ano, com todas as colunas como texto."""
    dbc = RAW / f"DNRS{ano}.dbc"
    dbf = PROCESSED / f"DNRS{ano}.dbf"
    if not dbf.exists():  # descompacta só na primeira vez
        PROCESSED.mkdir(parents=True, exist_ok=True)
        dbc2dbf(str(dbc), str(dbf))
    df = pd.DataFrame(iter(DBF(dbf, encoding="latin-1")))
    df.columns = df.columns.str.upper()  # 2017 traz "contador" em minúsculas
    return df.apply(lambda col: col.str.strip())  # a largura dos campos muda entre anos


def resumo_volume(ano: int, df: pd.DataFrame, poa: pd.DataFrame) -> dict:
    """0.2 e 0.3: quantos nascimentos são de mães residentes em POA."""
    ano_dtnasc = poa["DTNASC"].str[-4:]  # DTNASC vem como DDMMAAAA
    return {
        "ano": ano,
        "linhas_rs": len(df),
        "nascimentos_poa": len(poa),
        "pct_dtnasc_no_ano": round(100 * (ano_dtnasc == str(ano)).mean(), 2),
    }


def resumo_completude(ano: int, poa: pd.DataFrame) -> list[dict]:
    """0.6: % de valores vazios e % de valores formados só por noves."""
    linhas = []
    for var in CATEGORICAS + NUMERICAS:
        valores = poa[var]
        linhas.append(
            {
                "ano": ano,
                "variavel": var,
                "pct_vazio": round(100 * (valores == "").mean(), 2),
                # 9, 99, 9999... costumam ser "ignorado", mas o dicionário decide
                "pct_so_noves": round(100 * valores.str.fullmatch(r"9+").mean(), 2),
            }
        )
    return linhas


def main() -> None:
    pd.set_option("display.width", 200)
    pd.set_option("display.max_rows", 200)

    volume, completude, poa_por_ano = [], [], {}
    for ano in ANOS:
        df = ler_ano(ano)
        poa = df[df["CODMUNRES"] == COD_POA]
        volume.append(resumo_volume(ano, df, poa))
        completude.extend(resumo_completude(ano, poa))
        poa_por_ano[ano] = poa
        print(f"lido: {ano}")

    print("\n=== 0.2 e 0.3: volume por ano ===")
    tabela_volume = pd.DataFrame(volume).set_index("ano")
    print(tabela_volume)
    total_2021 = tabela_volume.loc[2021, "nascimentos_poa"]
    print(
        f"\n2021: {total_2021} no arquivo x {TOTAL_SMS_2021} da SMS "
        f"(diferença: {total_2021 - TOTAL_SMS_2021})"
    )

    print("\n=== 0.6: completude (% sobre os nascimentos de POA) ===")
    tabela = pd.DataFrame(completude)
    for medida in ["pct_vazio", "pct_so_noves"]:
        print(f"\n{medida}:")
        print(tabela.pivot(index="variavel", columns="ano", values=medida))

    print("\n=== 0.6: códigos encontrados (contagem por ano) ===")
    for var in CATEGORICAS:
        contagens = (
            pd.DataFrame(
                {
                    ano: poa[var].replace("", "(vazio)").value_counts()
                    for ano, poa in poa_por_ano.items()
                }
            )
            .fillna(0)
            .astype(int)
            .sort_index()
        )
        print(f"\n{var}:")
        print(contagens)

    print("\n=== 0.6: faixa de valores (sem vazios e sem 'só noves') ===")
    for var in NUMERICAS:
        faixa = {}
        for ano, poa in poa_por_ano.items():
            valores = poa[var]
            validos = pd.to_numeric(
                valores[~valores.str.fullmatch(r"9+") & (valores != "")],
                errors="coerce",
            )
            faixa[ano] = {
                "min": validos.min(),
                "max": validos.max(),
                "nao_numerico": int(validos.isna().sum()),
            }
        print(f"\n{var}:")
        print(pd.DataFrame(faixa))


if __name__ == "__main__":
    main()
