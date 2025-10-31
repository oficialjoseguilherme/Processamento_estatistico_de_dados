import pandas as pan

def filtrar(quadro: pan.DataFrame):

    if "classificados" in quadro.columns:

        ignorar_descl = quadro["classificados"].str.contains("descartado", case=False, na=False)
        quadro = quadro[~ignorar_descl].copy()

    return quadro