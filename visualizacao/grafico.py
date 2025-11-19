import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os

# -------------------------------------------------------------------
# GRÁFICOS DE EVOLUÇÃO TEMPORAL – SÃO PAULO
# -------------------------------------------------------------------

def grafico_linha_semanal_sp(semana_df: pd.DataFrame):
    """
    Plota a evolução semanal dos casos de dengue em SP,
    com uma linha por ano (NU_ANO), usando semana_ep (1–52/53).
    """
    if semana_df.empty:
        print("DataFrame semanal vazio – nenhum gráfico gerado.")
        return

    # Garantir ordenação por ano e semana
    semana_df = semana_df.sort_values(["NU_ANO", "semana_ep"])

    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=semana_df,
        x="semana_ep",
        y="casos",
        hue="NU_ANO",
        marker="o"
    )

    plt.title("Evolução semanal dos casos de dengue – São Paulo (2020–2025)")
    plt.xlabel("Semana epidemiológica")
    plt.ylabel("Número de casos")
    plt.xticks(range(1, semana_df["semana_ep"].max() + 1, 2))  # de 2 em 2 pra não poluir
    plt.legend(title="Ano")
    plt.tight_layout()
    plt.show()

def grafico_barras_anual_sp(ano_df: pd.DataFrame):
    """
    Plota um gráfico de barras com o total anual de casos em SP.
    """
    if ano_df.empty:
        print("DataFrame anual vazio – nenhum gráfico gerado.")
        return

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=ano_df,
        x="NU_ANO",
        y="casos"
    )

    plt.title("Total anual de casos de dengue – São Paulo (2020–2025)")
    plt.xlabel("Ano")
    plt.ylabel("Número de casos")
    plt.tight_layout()
    plt.show()


def grafico_proporcao_graves_sp(tabela_gravidade: pd.DataFrame):
    """
    Plota a proporção de casos graves por ano em São Paulo.
    """
    if tabela_gravidade.empty:
        print("Tabela de gravidade vazia – nenhum gráfico gerado.")
        return

    plt.figure(figsize=(8, 5))
    sns.barplot(
        data=tabela_gravidade,
        x="NU_ANO",
        y="prop_grave"
    )

    plt.title("Proporção de casos de dengue grave por ano – São Paulo (2020–2025)")
    plt.xlabel("Ano")
    plt.ylabel("Proporção de casos graves")
    plt.tight_layout()
    plt.show()








def grafico_perfil_demografico(perfil_df: pd.DataFrame):
    """
    Gráfico de barras mostrando o perfil demográfico (faixa etária e sexo)
    e a proporção de casos graves.
    """
    if perfil_df.empty:
        print("Perfil demográfico vazio – nenhum gráfico gerado.")
        return

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=perfil_df,
        x="faixa_etaria",
        y="proporcao_graves",
        hue="cs_sexo",
        ci=None
    )

    plt.title("Proporção de casos graves por faixa etária e sexo")
    plt.xlabel("Faixa Etária")
    plt.ylabel("Proporção de Casos Graves")
    plt.tight_layout()
    plt.show()


def grafico_perfil_por_ano(perfil_ano_df: pd.DataFrame):
    """
    Gráfico de barras empilhadas por ano, faixa etária e sexo,
    mostrando a distribuição dos casos graves.
    """
    if perfil_ano_df.empty:
        print("Perfil por ano vazio – nenhum gráfico gerado.")
        return

    plt.figure(figsize=(12, 6))
    sns.barplot(
        data=perfil_ano_df,
        x="nu_ano",
        y="proporcao_graves",
        hue="faixa_etaria",
        errorbar=None
    )

    plt.title("Proporção de casos graves por ano e faixa etária")
    plt.xlabel("Ano")
    plt.ylabel("Proporção de Casos Graves")
    plt.tight_layout()
    plt.show()




def grafico_top_municipios_casos_sp(
    tabela_mun,
    titulo: str = "Top municípios de SP com mais casos de dengue",
    caminho_saida: str | None = None,
):
    df = tabela_mun.copy()

    # usa o nome se existir, senão cai no código
    if "municipio_nome" in df.columns and not df["municipio_nome"].isna().all():
        df["municipio_label"] = df["municipio_nome"].astype(str)
    else:
        df["municipio_label"] = df["id_mn_resi"].astype(str)

    df = df.sort_values("casos", ascending=True)

    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=df,
        x="casos",
        y="municipio_label",
        orient="h",
        errorbar=None,
    )
    plt.xlabel("Número de casos")
    plt.ylabel("Município de residência")
    plt.title(titulo)
    plt.tight_layout()

    if caminho_saida:
        os.makedirs(os.path.dirname(caminho_saida), exist_ok=True)
        plt.savefig(caminho_saida, dpi=300)
        print(f"Gráfico salvo em: {caminho_saida}")

    plt.show()



def grafico_top_municipios_graves_sp(
    tabela_mun_graves,
    titulo: str = "Top municípios de SP com mais casos graves de dengue",
    caminho_saida: str | None = None,
):
    df = tabela_mun_graves.copy()

    if "municipio_nome" in df.columns and not df["municipio_nome"].isna().all():
        df["municipio_label"] = df["municipio_nome"].astype(str)
    else:
        df["municipio_label"] = df["id_mn_resi"].astype(str)

    df_graves = df.sort_values("total_graves", ascending=True)
    df_prop = df.sort_values("proporcao_graves", ascending=True)

    # 1) total de graves
    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=df_graves,
        x="total_graves",
        y="municipio_label",
        orient="h",
        errorbar=None,
    )
    plt.xlabel("Número de casos graves")
    plt.ylabel("Município de residência")
    plt.title(titulo)
    plt.tight_layout()

    if caminho_saida:
        base, ext = os.path.splitext(caminho_saida)
        caminho1 = base + "_graves" + (ext or ".png")
        os.makedirs(os.path.dirname(caminho1), exist_ok=True)
        plt.savefig(caminho1, dpi=300)
        print(f"Gráfico (total de graves) salvo em: {caminho1}")

    plt.show()

    # 2) proporção de graves
    plt.figure(figsize=(10, 8))
    sns.barplot(
        data=df_prop,
        x="proporcao_graves",
        y="municipio_label",
        orient="h",
        errorbar=None,
    )
    plt.xlabel("Proporção de casos graves (graves / total)")
    plt.ylabel("Município de residência")
    plt.title(titulo + " – proporção")
    plt.tight_layout()

    if caminho_saida:
        base, ext = os.path.splitext(caminho_saida)
        caminho2 = base + "_proporcao" + (ext or ".png")
        os.makedirs(os.path.dirname(caminho2), exist_ok=True)
        plt.savefig(caminho2, dpi=300)
        print(f"Gráfico (proporção de graves) salvo em: {caminho2}")

    plt.show()
