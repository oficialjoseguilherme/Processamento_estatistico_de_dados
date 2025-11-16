import pandas as pd
from scipy.stats import iqr


def resumo_estatistico_semanais(quadro: pd.DataFrame) -> dict:
    """
    Agrupa por NU_ANO (nu_ano - ano da notificação) e SEM_NOT (sem_not - semana da notificação) e calcula estatísticas
    sobre o número de casos por semana.
    """
    if "nu_ano" not in quadro.columns or "sem_not" not in quadro.columns:
        print("Colunas 'nu_ano' ou 'sem_not' ausentes. Não é possível gerar resumo semanal.")
        return {
            "media": None,
            "mediana": None,
            "moda": [],
            "desvio_padrao": None,
            "IQR": None,
            "outliers": pd.DataFrame()
        }

    # Agrupamento
    semana = (
        quadro
        .groupby(["nu_ano", "sem_not"], as_index=False)
        .size()
        .rename(columns={"size": "casos"})
    )

    if semana.empty:
        print("Resumo estatístico: agrupamento vazio (sem dados após filtros).")
        return {
            "media": None,
            "mediana": None,
            "moda": [],
            "desvio_padrao": None,
            "IQR": None,
            "outliers": semana
        }

    media = semana["casos"].mean()
    mediana = semana["casos"].median()
    moda = semana["casos"].mode().tolist()
    desvio_padrao = semana["casos"].std()

    try:
        iqr_valor = iqr(semana["casos"], nan_policy="omit")
    except Exception as e:
        print(f"Erro ao calcular IQR: {e}")
        iqr_valor = None

    # Outliers
    q1, q3 = semana["casos"].quantile([0.25, 0.75])
    lim_inferior = q1 - 1.5 * (q3 - q1)
    lim_superior = q3 + 1.5 * (q3 - q1)

    outliers = semana[(semana["casos"] < lim_inferior) | (semana["casos"] > lim_superior)]

    return {
        "media": media,
        "mediana": mediana,
        "moda": moda,
        "desvio_padrao": desvio_padrao,
        "IQR": iqr_valor,
        "outliers": outliers
    }


def calcular_proporcao_graves(quadro: pd.DataFrame) -> float:
    """
    Calcula a proporção de casos graves (CLASSI_FIN == 12) em relação ao total.
    """
    if "classi_fin" not in quadro.columns:
        print("Coluna 'classi_fin' ausente. Não é possível calcular proporção de graves.")
        return 0.0

    quadro["classi_fin"] = pd.to_numeric(quadro["classi_fin"], errors="coerce")

    total = len(quadro)
    if total == 0:
        print("Nenhuma linha no quadro após filtros. Proporção de graves = 0.")
        return 0.0

    graves = quadro[quadro["classi_fin"] == 12]
    proporcao = len(graves) / total

    print(f"Total de linhas: {total}, casos graves: {len(graves)}, proporção: {proporcao:.6f}")
    return proporcao
