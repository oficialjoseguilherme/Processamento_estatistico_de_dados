from algoritmos.limpeza_dados import leitor_geral_especifico_zip, converter_datas
from algoritmos.filtragem import filtrar_classificados
from algoritmos.estatisticas import (
    contagem_semanal_uf,
    contagem_anual_uf,
    resumo_temporal_por_ano,
    tabela_gravidade_por_ano_uf,
    perfil_demografico,
    perfil_por_ano,
    casos_por_municipio_sp,
    casos_graves_por_municipio_sp
)
from visualizacao.grafico import (
    grafico_linha_semanal_sp,
    grafico_barras_anual_sp,
    grafico_proporcao_graves_sp,
    grafico_perfil_demografico,
    grafico_perfil_por_ano,
    grafico_top_municipios_casos_sp,
    grafico_top_municipios_graves_sp
)
from algoritmos.municipios import carregar_mapa_municipios_sp_de_txt

def executar_evolucao_temporal_sp(caminhos_zip: list[str], colunas_necessarias: list[str]):
    # 1) Ler e limpar
    dados = leitor_geral_especifico_zip(caminhos_zip, colunas_necessarias)
    dados = converter_datas(dados)
    dados = filtrar_classificados(dados)

    # 2) Contagens
    semana_sp = contagem_semanal_uf(dados, uf_cod=35)
    ano_sp = contagem_anual_uf(dados, uf_cod=35)

    print("Primeiras linhas da contagem semanal em SP (agora com semana_ep):")
    print(semana_sp.head())

    print("\nContagem anual em SP:")
    print(ano_sp)

    # 3) Estatísticas por ano
    resumo_ano, outliers = resumo_temporal_por_ano(semana_sp)

    print("\nResumo estatístico por ano – São Paulo:")
    print(resumo_ano)

    print("\nOutliers semanais por ano (semanas muito acima/abaixo do esperado):")
    print(outliers)

    # 4) Gráficos
    grafico_linha_semanal_sp(semana_sp)
    grafico_barras_anual_sp(ano_sp)





def executar_evolucao_e_gravidade_sp(caminhos_zip: list[str], colunas_necessarias: list[str]):
    # 1) Ler e limpar
    dados = leitor_geral_especifico_zip(caminhos_zip, colunas_necessarias)
    print(f"Total de linhas após leitura geral (zip): {len(dados)}")
    print(f"Colunas do DataFrame final: {list(dados.columns)}")

    dados = converter_datas(dados)
    dados = filtrar_classificados(dados)

    # 2) Evolução temporal
    semana_sp = contagem_semanal_uf(dados, uf_cod=35)
    ano_sp = contagem_anual_uf(dados, uf_cod=35)

    resumo_ano, outliers = resumo_temporal_por_ano(semana_sp)

    print("\nContagem anual em SP:")
    print(ano_sp)

    print("\nResumo estatístico por ano – São Paulo:")
    print(resumo_ano)

    print("\nOutliers semanais por ano (semanas muito acima/abaixo do esperado):")
    print(outliers)

    grafico_linha_semanal_sp(semana_sp)
    grafico_barras_anual_sp(ano_sp)

    # 3) Gravidade por ano
    tabela_grav = tabela_gravidade_por_ano_uf(dados, uf_cod=35)

    print("\nTabela de gravidade por ano – São Paulo:")
    print(tabela_grav)

    grafico_proporcao_graves_sp(tabela_grav)





def executar_perfil_demografico_sp(caminhos_zip: list[str], colunas_necessarias: list[str]):
    # 1) Leitura e limpeza
    dados = leitor_geral_especifico_zip(caminhos_zip, colunas_necessarias)
    dados = converter_datas(dados)
    dados = filtrar_classificados(dados)

    # 2) Perfil demográfico
    perfil = perfil_demografico(dados)

    print("\nPerfil demográfico (idade e sexo) dos casos de dengue – São Paulo:")
    print(perfil)

    # 3) Perfil por ano
    perfil_ano = perfil_por_ano(dados)

    print("\nPerfil demográfico por ano – São Paulo:")
    print(perfil_ano)

    # 4) Gráficos
    grafico_perfil_demografico(perfil)
    grafico_perfil_por_ano(perfil_ano)




def executar_analise_municipios_sp(caminhos_zip, colunas_necessarias):
    dados = leitor_geral_especifico_zip(caminhos_zip, colunas_necessarias)
    dados = converter_datas(dados)
    dados = filtrar_classificados(dados)

    # 2) carrega mapa de municípios a partir do txt do IBGE
    mapa_mun_sp = carregar_mapa_municipios_sp_de_txt(
        "dados/municipios_sp_lista.txt"
    )

    # 3) tabelas
    tabela_mun = casos_por_municipio_sp(dados, mapa_mun_sp, uf_cod=35, top_n=20)
    tabela_mun_graves = casos_graves_por_municipio_sp(dados, mapa_mun_sp, uf_cod=35, top_n=20)

    print("Top 20 municípios de SP com mais casos:")
    print(tabela_mun.head(20))

    print("\nTop 20 municípios de SP com mais casos graves:")
    print(tabela_mun_graves.head(20))

    # gráfico de total de casos
    grafico_top_municipios_casos_sp(
        tabela_mun,
        titulo="Top 20 municípios de SP com mais casos notificados de dengue",
        caminho_saida="resultados/top_municipios_casos_sp.png",
    )

    # gráficos de casos graves (sua função já gera DOIS arquivos)
    grafico_top_municipios_graves_sp(
        tabela_mun_graves,
        titulo="Top 20 municípios de SP com mais casos graves de dengue",
        caminho_saida="resultados/top_municipios_graves_sp.png",
    )

    return tabela_mun, tabela_mun_graves