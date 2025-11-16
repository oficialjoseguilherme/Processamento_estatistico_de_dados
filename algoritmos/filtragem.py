import pandas as pd

# Mapeamento de sigla de UF -> código IBGE usado em SG_UF_NOT
UF_IBGE = {
    "AC": 12, "AL": 27, "AP": 16, "AM": 13, "BA": 29, "CE": 23,
    "DF": 53, "ES": 32, "GO": 52, "MA": 21, "MT": 51, "MS": 50,
    "MG": 31, "PA": 15, "PB": 25, "PR": 41, "PE": 26, "PI": 22,
    "RJ": 33, "RN": 24, "RS": 43, "RO": 11, "RR": 14, "SC": 42,
    "SP": 35, "SE": 28, "TO": 17
}

# Remove casos com classi_fin considerado descartado
def filtrar_classificados(quadro: pd.DataFrame) -> pd.DataFrame:
    """
    Remove casos descartados (CLASSI_FIN == 5).
    """
    if "classi_fin" not in quadro.columns:
        print("Aviso: coluna 'classi_fin' não encontrada. Nenhum filtro aplicado.")
        return quadro

    quadro["classi_fin"] = pd.to_numeric(quadro["classi_fin"], errors="coerce")
    antes = len(quadro)
    quadro_filtrado = quadro[quadro["classi_fin"] != 5].copy()
    depois = len(quadro_filtrado)

    print(f"Filtrar classificados: {antes} -> {depois} linhas (descartados removidos).")
    return quadro_filtrado

# Filtra o dataframe por UF, somente um UF por vez
def filtrar_uf(quadro: pd.DataFrame, uf_sigla: str) -> pd.DataFrame:
    """
    Filtra o DataFrame pela UF de notificação, usando SG_UF_NOT com código IBGE.
    """
    if "sg_uf_not" not in quadro.columns:
        print("Aviso: coluna 'sg_uf_not' não encontrada. Nenhum filtro de UF aplicado.")
        return quadro

    cod_uf = UF_IBGE.get(uf_sigla.upper())
    if cod_uf is None:
        print(f"Aviso: UF '{uf_sigla}' não mapeada. Nenhum filtro de UF aplicado.")
        return quadro

    quadro["sg_uf_not"] = pd.to_numeric(quadro["sg_uf_not"], errors="coerce")

    antes = len(quadro)
    quadro_filtrado = quadro[quadro["sg_uf_not"] == cod_uf].copy()
    depois = len(quadro_filtrado)

    print(f"Filtrar UF {uf_sigla} (cód {cod_uf}): {antes} -> {depois} linhas.")
    return quadro_filtrado
