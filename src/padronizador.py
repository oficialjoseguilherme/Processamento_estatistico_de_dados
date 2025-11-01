import pandas as pan

def filtrar(quadro: pan.DataFrame):

    if "classificados" in quadro.columns:

        mascara_desclassificados = (quadro["classificados"]
                                    .str.contains("desclassi",
                                                  case=False,
                                                  na=False))

        quadro = (quadro[~mascara_desclassificados]
                  .copy())

    return quadro

def converterData(quadro: pan.DataFrame):

    if "data_sintoma_primario" in quadro.columns:
        quadro["data_sintoma_primario"] = pan.to_datetime(quadro["data_sintoma_primario"],
                                                          dayfirst=True,
                                                          errors="coerce")

    if "data_notificacao" in quadro.columns:
        quadro["data_notificacao"] = pan.to_datetime(quadro["data_notificacao"],
                                                     dayfirst=True,
                                                     errors="coerce")

    return quadro

def filtrarUF(quadro: pan.DataFrame, UF: str):
    return (quadro[quadro["sigla_uf"] == UF]
            .copy())


