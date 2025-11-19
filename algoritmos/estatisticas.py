import pandas as pd
import numpy as np
from scipy.stats import iqr

# -------------------------------------------------------------------
# EVOLUÇÃO TEMPORAL – ESTADO DE SÃO PAULO (OU OUTRO UF)
# -------------------------------------------------------------------

def contagem_semanal_uf(quadro: pd.DataFrame, uf_cod: int = 35) -> pd.DataFrame:
    """
    Retorna um DataFrame com o número de casos por ano e semana epidemiológica
    para uma UF específica (padrão: 35 = São Paulo).

    Saída: colunas ['nu_ano', 'semana_ep', 'casos']
    """
    df = quadro.copy()

    # Filtrar UF
    df = df[df["sg_uf_not"] == uf_cod]

    # Garantir que sem_not é numérico e não nulo
    df = df[df["sem_not"].notna()]
    df["sem_not"] = pd.to_numeric(df["sem_not"], errors="coerce")
    df = df[df["sem_not"].notna()]

    # Extrair semana epidemiológica (últimos 2 dígitos, ex: 202415 -> 15)
    df["semana_ep"] = (df["sem_not"] % 100).astype(int)

    semana = (
        df.groupby(["nu_ano", "semana_ep"], as_index=False)
          .size()
          .rename(columns={"size": "casos"})
    )

    return semana


def contagem_anual_uf(quadro: pd.DataFrame, uf_cod: int = 35) -> pd.DataFrame:
    """
    Retorna um DataFrame com o número total de casos por ano para uma UF específica.
    Saída: colunas ['nu_ano', 'casos']
    """
    df = quadro.copy()
    df = df[df["sg_uf_not"] == uf_cod]

    ano = (
        df.groupby("nu_ano", as_index=False)
          .size()
          .rename(columns={"size": "casos"})
    )

    return ano


def resumo_temporal_por_ano(semana_df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Recebe o DataFrame de contagem semanal (nu_ano, semana_ep, casos)
    e calcula estatísticas descritivas da série de 'casos' POR ANO.

    Retorna:
    - resumo: DataFrame com uma linha por ano e colunas de estatísticas
    - outliers: DataFrame com semanas consideradas outliers por ano
    """
    if semana_df.empty:
        return pd.DataFrame(), pd.DataFrame()

    def _estatisticas(g: pd.DataFrame) -> pd.Series:
        serie = g["casos"]
        media = serie.mean()
        mediana = serie.median()
        moda = serie.mode().tolist()
        desvio = serie.std()
        iqr_val = iqr(serie, nan_policy="omit")
        return pd.Series({
            "media": media,
            "mediana": mediana,
            "moda": moda[0] if len(moda) > 0 else None,
            "desvio_padrao": desvio,
            "iqr": iqr_val,
        })

    resumo = (
        semana_df
        .groupby("nu_ano")
        .apply(_estatisticas)
        .reset_index()
    )

    # Calcular outliers por ano
    lista_outliers = []
    for ano, g in semana_df.groupby("nu_ano"):
        serie = g["casos"]
        q1, q3 = serie.quantile([0.25, 0.75])
        lim_inf = q1 - 1.5 * (q3 - q1)
        lim_sup = q3 + 1.5 * (q3 - q1)
        out = g[(g["casos"] < lim_inf) | (g["casos"] > lim_sup)].copy()
        out["nu_ano"] = ano
        lista_outliers.append(out)

    outliers = (
        pd.concat(lista_outliers, ignore_index=True)
        if lista_outliers else pd.DataFrame()
    )

    return resumo, outliers

# -------------------------------------------------------------------
# GRAVIDADE POR ANO – ESTADO DE SÃO PAULO
# -------------------------------------------------------------------

def tabela_gravidade_por_ano_uf(quadro: pd.DataFrame, uf_cod: int = 35) -> pd.DataFrame:
    """
    Retorna uma tabela com contagem de casos por ano e por CLASSI_FIN
    para uma UF específica (padrão: 35 = São Paulo).

    CLASSI_FIN (segundo dicionário online):
        10 = Dengue
        11 = Dengue com sinais de alarme
        12 = Dengue grave
        8  = Outros / Síndrome febril inespecífica (dependendo do dicionário)

    Saída: DataFrame com colunas:
        ['nu_ano', 'total', 'dengue', 'sinal_alarme', 'grave', 'outros',
         'prop_grave']
    """
    df = quadro.copy()

    # Filtrar UF
    df = df[df["sg_uf_not"] == uf_cod]

    # Garantir numérico
    df["classi_fin"] = pd.to_numeric(df["classi_fin"], errors="coerce")

    # Contagem por ano e classificação
    contagem = (
        df.groupby(["nu_ano", "classi_fin"], as_index=False)
          .size()
          .rename(columns={"size": "casos"})
    )

    # Pivotar para colunas por tipo
    tabela = contagem.pivot(index="nu_ano", columns="classi_fin", values="casos").fillna(0)

    tabela.reset_index(inplace=True)

    # Renomear colunas conforme o código
    tabela_final = pd.DataFrame({
        "nu_ano": tabela["nu_ano"],
        "dengue": tabela.get(10.0, 0),
        "sinal_alarme": tabela.get(11.0, 0),
        "grave": tabela.get(12.0, 0),
        "outros": tabela.get(8.0, 0),
    })

    tabela_final["total"] = (
        tabela_final["dengue"]
        + tabela_final["sinal_alarme"]
        + tabela_final["grave"]
        + tabela_final["outros"]
    )

    # Proporção de casos graves
    tabela_final["prop_grave"] = np.where(
        tabela_final["total"] > 0,
        tabela_final["grave"] / tabela_final["total"],
        0.0
    )

    # Ordenar por ano
    tabela_final = tabela_final.sort_values("nu_ano").reset_index(drop=True)

    return tabela_final


def idade_para_anos(idade_codificada: float) -> float:
    """
    Converte a idade codificada para anos, considerando o padrão do campo 'NU_IDADE_N'.
    """
    if pd.isna(idade_codificada):
        return None

    # O valor de 'idade_codificada' já é o número da idade, mas precisamos determinar
    # se está em ano, mês, etc.
    idade_valor = int(idade_codificada)

    # Vamos supor que o número indica anos, pois o dicionário nos sugere que os dados
    # estão codificados por unidades de tempo (ano, mês, etc.), e a maior parte dos valores
    # é grande o suficiente para ser idade em anos.

    return idade_valor  # Consideramos que todos os valores estão em anos (conforme esperado)

def faixa_etaria(idade: float) -> str:
    """
    Converte a idade para uma faixa etária.
    """
    idade_em_anos = idade_para_anos(idade)

    if pd.isna(idade_em_anos) or idade_em_anos <= 0:
        return "Desconhecida"
    
    elif idade_em_anos <= 14:
        return "0-14"
    elif idade_em_anos <= 29:
        return "15-29"
    elif idade_em_anos <= 59:
        return "30-59"
    else:
        return "60+"
    

def perfil_demografico(quadro: pd.DataFrame) -> pd.DataFrame:
    """
    Analisa o perfil demográfico (idade e sexo) dos casos de dengue,
    segmentando por faixa etária e sexo, além de calcular a proporção de casos graves.
    """
    df = quadro[quadro['sg_uf_not'] == 35].copy()

    # Criação da coluna 'faixa_etaria' a partir de 'NU_IDADE_N'
    df['faixa_etaria'] = df['nu_idade_n'].apply(faixa_etaria)

    # Filtrando apenas os casos graves
    casos_graves = df[df['classi_fin'] == 12]

    # Contagem por faixa etária e sexo
    perfil_geral = df.groupby(['faixa_etaria', 'cs_sexo']).size().reset_index(name='total')
    perfil_graves = casos_graves.groupby(['faixa_etaria', 'cs_sexo']).size().reset_index(name='total_graves')

    # Merge para ter o perfil geral e o de casos graves na mesma tabela
    perfil = pd.merge(perfil_geral, perfil_graves, on=['faixa_etaria', 'cs_sexo'], how='left')
    perfil['proporcao_graves'] = perfil['total_graves'] / perfil['total']

    return perfil


def perfil_por_ano(quadro: pd.DataFrame) -> pd.DataFrame:
    """
    Analisa a evolução do perfil demográfico ao longo do tempo.
    """
    df = quadro[quadro['sg_uf_not'] == 35].copy()

    # Criação da coluna 'faixa_etaria' a partir de 'NU_IDADE_N'
    df['faixa_etaria'] = df['nu_idade_n'].apply(faixa_etaria)

    # Filtrando apenas os casos graves
    casos_graves = df[df['classi_fin'] == 12]

    # Contagem por ano, faixa etária e sexo
    perfil_geral_ano = df.groupby(['nu_ano', 'faixa_etaria', 'cs_sexo']).size().reset_index(name='total')
    perfil_graves_ano = casos_graves.groupby(['nu_ano', 'faixa_etaria', 'cs_sexo']).size().reset_index(name='total_graves')

    # Merge para ter o perfil geral e o de casos graves na mesma tabela
    perfil_ano = pd.merge(perfil_geral_ano, perfil_graves_ano, on=['nu_ano', 'faixa_etaria', 'cs_sexo'], how='left')
    perfil_ano['proporcao_graves'] = perfil_ano['total_graves'] / perfil_ano['total']

    return perfil_ano








def casos_por_municipio_sp(
    quadro: pd.DataFrame,
    mapa_mun_sp: pd.DataFrame,
    uf_cod: int = 35,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    TOP N municípios de SP em número de casos notificados.
    Usa ID_MN_RESI (código do município de residência) + mapa para nome.
    """
    df = quadro.copy()

    # filtra SP
    df_sp = df[df["sg_uf_not"] == uf_cod].copy()

    # padroniza ID_MN_RESI como string de 6 dígitos
    df_sp["id_mn_resi_6"] = (
        df_sp["id_mn_resi"]
        .astype("Int64")
        .astype(str)
        .str.zfill(6)
    )

    contagem = (
        df_sp.groupby("id_mn_resi_6")
        .size()
        .reset_index(name="casos")
    )

    # junta com o mapa de municípios
    tabela = contagem.merge(mapa_mun_sp, on="id_mn_resi_6", how="left")

    # se algum código não casar, usa o código como fallback
    tabela["municipio_nome"] = tabela["municipio_nome"].fillna(tabela["id_mn_resi_6"])

    tabela = (
        tabela.sort_values("casos", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    # ordena colunas de forma amigável
    tabela = tabela[["id_mn_resi_6", "municipio_nome", "casos"]]

    return tabela


def casos_graves_por_municipio_sp(
    quadro: pd.DataFrame,
    mapa_mun_sp: pd.DataFrame,
    uf_cod: int = 35,
    top_n: int = 20,
) -> pd.DataFrame:
    """
    TOP N municípios de SP em número de casos graves, com:
      - total_casos
      - total_graves
      - proporcao_graves
    """
    df = quadro.copy()

    df_sp = df[df["sg_uf_not"] == uf_cod].copy()

    df_sp["id_mn_resi_6"] = (
        df_sp["id_mn_resi"]
        .astype("Int64")
        .astype(str)
        .str.zfill(6)
    )

    total = (
        df_sp.groupby("id_mn_resi_6")
        .size()
        .reset_index(name="total_casos")
    )

    graves = df_sp[df_sp["classi_fin"] == 12]
    total_graves = (
        graves.groupby("id_mn_resi_6")
        .size()
        .reset_index(name="total_graves")
    )

    tabela = total.merge(total_graves, on="id_mn_resi_6", how="left")
    tabela["total_graves"] = tabela["total_graves"].fillna(0).astype(int)
    tabela["proporcao_graves"] = tabela["total_graves"] / tabela["total_casos"]

    tabela = tabela.merge(mapa_mun_sp, on="id_mn_resi_6", how="left")
    tabela["municipio_nome"] = tabela["municipio_nome"].fillna(tabela["id_mn_resi_6"])

    tabela = (
        tabela.sort_values("total_graves", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    tabela = tabela[
        ["id_mn_resi_6", "municipio_nome", "total_casos", "total_graves", "proporcao_graves"]
    ]

    return tabela