from ftplib import FTP
from pathlib import Path


ANOS = list(range(2017, 2025))
BASE = Path(__file__).resolve().parents[2]
DESTINO = BASE / "data" / "raw" / "sinasc"


def salvar(anos: list[int], destino: Path = DESTINO) -> None:
    destino.parent.mkdir(parents=True, exist_ok=True)
    with FTP("ftp.datasus.gov.br") as ftp:
        ftp.login()  # acesso anônimo
        ftp.cwd("/dissemin/publicos/SINASC/1996_/Dados/DNRES/")
        for ano in anos:
            nome = f"DNRS{ano}.dbc"
            arquivo = destino / nome
            if arquivo.exists():  # não baixa de novo o que já existe
                continue
            with open(arquivo, "wb") as f:
                ftp.retrbinary(f"RETR {nome}", f.write)
            print("baixado:", nome)


salvar(ANOS, DESTINO)
