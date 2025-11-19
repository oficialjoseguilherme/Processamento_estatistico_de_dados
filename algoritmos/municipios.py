# algoritmos/municipios.py
import pandas as pd
from typing import List, Tuple

def carregar_mapa_municipios_sp_de_txt(
    caminho_txt: str = "dados_referencia/municipios_sp_lista.txt"
) -> pd.DataFrame:
    """
    Lê o arquivo de texto com a lista dos municípios de SP (nome + código IBGE)
    e gera um DataFrame com:
        - id_mn_resi_6: código compatível com ID_MN_RESI do SINAN (6 dígitos)
        - municipio_nome: nome do município

    O arquivo deve ter a estrutura como a lista que você colou:
        Nome da cidade
        3550308
        Nome da próxima
        35xxxxx
        ...

    Linhas como 'Municípios de São PauloCódigos', 'A', 'B', etc são ignoradas.
    """

    with open(caminho_txt, "r", encoding="utf-8") as f:
        # remove linhas vazias e tira espaços
        linhas = [linha.strip() for linha in f if linha.strip()]

    pares: List[Tuple[str, str]] = []

    i = 0
    while i < len(linhas) - 1:
        linha = linhas[i]
        prox = linhas[i + 1]

        # ignora cabeçalho e letras soltas (A, B, C...)
        if (
            linha.startswith("Municípios de São Paulo")
            or (len(linha) == 1 and linha.isalpha())
        ):
            i += 1
            continue

        # se a próxima linha é código (só dígitos, 6 ou 7 caracteres),
        # consideramos a atual como nome de município
        if prox.isdigit() and len(prox) in (6, 7):
            nome = linha
            cod_ibge = prox  # ex.: '3550308'
            # usamos apenas os 6 primeiros dígitos para casar com ID_MN_RESI
            cod6 = cod_ibge[:6]
            pares.append((cod6, nome))
            i += 2
        else:
            i += 1

    df = pd.DataFrame(pares, columns=["id_mn_resi_6", "municipio_nome"])
    df = df.drop_duplicates(subset="id_mn_resi_6").reset_index(drop=True)

    return df


def gerar_csv_municipios_sp(
    caminho_txt: str = "dados_referencia/municipios_sp_lista.txt",
    caminho_csv_saida: str = "dados_referencia/municipios_sp.csv",
) -> pd.DataFrame:
    df = carregar_mapa_municipios_sp_de_txt(caminho_txt)
    df.to_csv(caminho_csv_saida, index=False, encoding="utf-8")
    return df
