from controlador.controlador import (
    executar_evolucao_temporal_sp, 
    executar_evolucao_e_gravidade_sp, 
    executar_perfil_demografico_sp, 
    executar_analise_municipios_sp
)

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
        "ID_MN_RESI",
        "MUNICIPIO"
    ]

    executar_evolucao_temporal_sp(caminhos_zip, colunas_necessarias)

    # executar_evolucao_e_gravidade_sp(caminhos_zip, colunas_necessarias)

    # executar_perfil_demografico_sp(caminhos_zip, colunas_necessarias)

    # executar_analise_municipios_sp(caminhos_zip, colunas_necessarias)
