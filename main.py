from controlador.controlador import executar_analise

if __name__ == "__main__":
    caminhos_zip = [
        "dados/DENGBR20.zip",
        "dados/DENGBR21.zip",
        "dados/DENGBR22.zip",
        "dados/DENGBR23.zip",
        "dados/DENGBR24.zip",
        "dados/DENGBR25.zip",
    ]

    colunas_necessarias = [
        "DT_NOTIFIC",
        "SEM_NOT",
        "NU_ANO",
        "SG_UF_NOT",
        "DT_SIN_PRI",
        "NU_IDADE_N",
        "CS_SEXO",
        "CLASSI_FIN",
    ]

    executar_analise(caminhos_zip, colunas_necessarias, "SP")
