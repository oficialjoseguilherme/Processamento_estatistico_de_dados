import pandas as pd

# 1. Mapeamento UF -> código IBGE (SG_UF_NOT)
UF_IBGE = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 29, "CE": 23,
    "DF": 53, "ES": 32, "GO": 52, "MA": 21, "MT": 51, "MS": 50,
    "MG": 31, "PA": 15, "PB": 25, "PR": 41, "PE": 26, "PI": 22,
    "RJ": 33, "RN": 24, "RS": 43, "RO": 11, "RR": 14, "SC": 42,
    "SP": 35, "SE": 28, "TO": 17
}


def processar_dados(caminhos: list, colunas: list, uf_sigla: str):
    # 2. Leitura de todos os arquivos, mantendo nomes originais das colunas
    dados_finais = pd.DataFrame()

    for caminho in caminhos:
        try:
            quadro = pd.read_csv(caminho, usecols=colunas, low_memory=False)
            print(f"\nArquivo lido: {caminho}")
            print("Colunas originais:", list(quadro.columns))

            # Padronizar colunas para minúsculas
            quadro.columns = [c.lower() for c in quadro.columns]
            print("Colunas após lower():", list(quadro.columns))

            dados_finais = pd.concat([dados_finais, quadro], ignore_index=True)
        except Exception as e:
            print(f"Erro ao ler {caminho}: {e}")

    print("\n=== RESUMO GERAL DO DATAFRAME UNIFICADO ===")
    print("Colunas do DataFrame final:", list(dados_finais.columns))
    print("Número total de linhas:", len(dados_finais))

    # 3. Verificar SEM_NOT
    if "sem_not" in dados_finais.columns:
        print("\nValores únicos em sem_not (alguns primeiros):")
        print(dados_finais["sem_not"].value_counts().head(20))
    else:
        print("\nATENÇÃO: coluna 'sem_not' não encontrada no DataFrame!")

    # 4. Agrupamento por ano e semana (usando nu_ano e sem_not)
    if "nu_ano" in dados_finais.columns and "sem_not" in dados_finais.columns:
        semana = (
            dados_finais
            .groupby(["nu_ano", "sem_not"], as_index=False)
            .size()
            .rename(columns={"size": "casos"})
        )
        print("\nPrimeiras linhas do agrupamento por nu_ano + sem_not:")
        print(semana.head(20))
        print("Número de linhas no agrupamento:", len(semana))
    else:
        print("\nNão foi possível agrupar por nu_ano e sem_not (colunas ausentes).")

    # 5. Verificar casos graves (CLASSI_FIN == 12)
    if "classi_fin" in dados_finais.columns:
        # garantir que é numérico
        dados_finais["classi_fin"] = pd.to_numeric(dados_finais["classi_fin"], errors="coerce")
        casos_graves = dados_finais[dados_finais["classi_fin"] == 12]
        print("\nNúmero total de casos graves (classi_fin == 12):", len(casos_graves))
        print("Amostra de casos graves:")
        print(casos_graves.head())
    else:
        print("\nColuna 'classi_fin' não encontrada.")

    # 6. Teste de filtro por UF usando SG_UF_NOT + dicionário IBGE
    if "sg_uf_not" in dados_finais.columns:
        cod_uf = UF_IBGE.get(uf_sigla.upper(), None)
        print(f"\nUF solicitada: {uf_sigla} -> código IBGE esperado em sg_uf_not: {cod_uf}")

        if cod_uf is not None:
            # sg_uf_not pode estar como int ou string, então vamos normalizar:
            # converter pra numérico (errors='coerce' -> NaN onde não der)
            dados_finais["sg_uf_not"] = pd.to_numeric(dados_finais["sg_uf_not"], errors="coerce")

            dados_uf = dados_finais[dados_finais["sg_uf_not"] == cod_uf]
            print("Linhas após filtro de UF:", len(dados_uf))

            if len(dados_uf) > 0:
                print("Amostra de linhas filtradas por UF:")
                print(dados_uf.head())
            else:
                print("Nenhuma linha encontrada para essa UF. Verifique o código IBGE e o tipo da coluna.")
        else:
            print("UF não mapeada no dicionário UF_IBGE.")
    else:
        print("\nColuna 'sg_uf_not' não encontrada.")


if __name__ == "__main__":
    # Colunas como estão nos CSVs (maiúsculas)
    colunas_necessarias = [
        "NU_ANO", "SEM_NOT", "SG_UF_NOT", "CLASSI_FIN",
        "NU_IDADE_N", "CS_SEXO", "DT_SIN_PRI", "DT_NOTIFIC"
    ]

    caminhos = [
        "dados/DENGBR20.csv",
        "dados/DENGBR21.csv",
        "dados/DENGBR22.csv",
        "dados/DENGBR23.csv",
        "dados/DENGBR24.csv",
        "dados/DENGBR25.csv",
    ]

    # teste com UF de escolha
    processar_dados(caminhos, colunas_necessarias, uf_sigla="SP")
