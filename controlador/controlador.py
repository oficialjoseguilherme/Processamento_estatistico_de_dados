from algoritmos.limpeza_dados import leitor_geral_especifico_zip, converter_datas
from algoritmos.filtragem import filtrar_classificados, filtrar_uf
from algoritmos.estatisticas import resumo_estatistico_semanais, calcular_proporcao_graves
from visualizacao.grafico import graficoBox, graficoTemporal


def executar_analise(caminhos_zip: list[str], colunas_necessarias: list[str], uf_sigla: str):
    # 1) Leitura
    dados = leitor_geral_especifico_zip(caminhos_zip, colunas_necessarias)

    # 2) Conversão de datas
    dados = converter_datas(dados)

    # 3) Filtro por UF (SP, RJ, etc.)
    dados = filtrar_uf(dados, uf_sigla)

    # 4) Remover descartados
    dados = filtrar_classificados(dados)

    # 5) Estatísticas semanais
    estatisticas = resumo_estatistico_semanais(dados)
    print("\nEstatísticas de Casos Semanais:")
    print(estatisticas)

    # 6) Proporção de casos graves
    proporcao_graves = calcular_proporcao_graves(dados)
    print(f"\nProporção de Casos Graves na UF {uf_sigla}: {proporcao_graves:.6f}")

    # 7) Gráficos
    graficoBox(dados)
    graficoTemporal(dados)
