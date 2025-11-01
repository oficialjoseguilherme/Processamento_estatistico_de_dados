import numpy as np
import pandas as pan
from scipy.stats import iqr

def resumoEstatistico(quadro: pan.DataFrame):

    semana = (quadro.groupby(["numero_ano", "semana_primaria"],
                            as_index=False)
              .size()
              .rename(columns={"size": "casos"}))

    media = (semana["casos"]
             .mean())

    mediana = (semana["casos"]
               .median())

    moda = (semana["casos"]
            .mode.tolist())

    desvioPadrao = (semana["casos"]
                    .std())

    iqrValor=iqr(semana["casos"],
                  nan_policy="omit")

    #Outliers
    quota1, quota3 = (semana["casos"].
                      quantile([0.25, 0.75]))

    limInferior, limSuperior = (quota1 - 1.5 * (quota3 - quota1),
                                quota3 + 1.5 * (quota3 - quota1))
    outliers = semana[(semana["casos"] < limInferior) |
                      (semana["casos"] > limSuperior)]

    return {
        "media": media,
        "mediana": mediana,
        "moda": moda,
        "desvio padrão": desvioPadrao,
        "IQR": iqrValor,
        "outliers": outliers
    }