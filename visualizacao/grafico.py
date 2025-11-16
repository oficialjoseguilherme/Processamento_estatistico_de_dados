import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def _agrupar_semana(quadro: pd.DataFrame) -> pd.DataFrame:
    """
    Função interna: agrupa por nu_ano + sem_not e retorna DataFrame com colunas:
    ['nu_ano', 'sem_not', 'casos'].
    """
    semana = (
        quadro
        .groupby(["nu_ano", "sem_not"], as_index=False)
        .size()
        .rename(columns={"size": "casos"})
    )
    return semana


def graficoBox(quadro: pd.DataFrame):
    """
    Boxplot da distribuição de casos por semana (SEM_NOT), para o período filtrado.
    """
    if "nu_ano" not in quadro.columns or "sem_not" not in quadro.columns:
        print("Colunas 'nu_ano' ou 'sem_not' ausentes. Não é possível gerar boxplot.")
        return

    semana = _agrupar_semana(quadro)

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=semana, x="sem_not", y="casos")
    plt.title("Distribuição de Casos Semanais (todas as séries no período filtrado)")
    plt.xlabel("SEM_NOT (Ano+Semana)")
    plt.ylabel("Número de Casos")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()


def graficoTemporal(quadro: pd.DataFrame):
    """
    Série temporal de casos por semana, com uma curva para cada ano (nu_ano).
    """
    if "nu_ano" not in quadro.columns or "sem_not" not in quadro.columns:
        print("Colunas 'nu_ano' ou 'sem_not' ausentes. Não é possível gerar gráfico temporal.")
        return

    semana = _agrupar_semana(quadro)

    plt.figure(figsize=(12, 6))
    sns.lineplot(data=semana, x="sem_not", y="casos", hue="nu_ano", marker="o")
    plt.title("Evolução de Casos Semanais por Ano")
    plt.xlabel("SEM_NOT (Ano+Semana)")
    plt.ylabel("Número de Casos")
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()
