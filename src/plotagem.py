import matplotlib.pyplot as plot
import seaborn as sns
import pandas as pan

def graficoBox(quadro: pan.DataFrame):

    semana = (quadro.groupby(["numero_ano", "semana_primaria"],
                            as_index=False)
              .size()
              .rename(columns={"size": "casos"}))
    (plot
     .figure(figsize=(10, 6)))

    (sns
     .boxplot(data=semana,
              x="semana_primaria",
              y="casos"))

    (plot
     .title("Distribuição de Casos Semanais"))

    (plot
     .xlabel("Semana Epidemiológica"))

    (plot.
     ylabel("Número de Casos"))

    (plot
     .show())

def graficoTemporal(quadro: pan.DataFrame):

    semana = (quadro.groupby(["numero_ano", "semana_primaria"],
                            as_index=False)
              .size()
              .rename(columns={"size": "casos"}))
    (plot
     .figure(figsize=(10, 6)))

    (sns
     .lineplot(data=semana,
                 x="semana_primaria",
                 y="casos",
                 hue="numero_ano"))

    (plot
     .title("Evolução de Casos Semanais"))

    (plot
     .xlabel("Semana Epidemiológica"))

    (plot.
     ylabel("Número de Casos"))

    (plot
     .show())
