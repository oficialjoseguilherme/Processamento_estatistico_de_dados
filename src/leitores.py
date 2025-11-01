import pandas as pan

def leitorCsv(caminho: str):
    delimitadores = [',', ';', '\t']

    for delimitador in delimitadores:
        try:

            quadro = pan.read_csv(caminho,
                                  sep=delimitador)

            print(f"Codigo 1: Separador {delimitador}")

            return quadro

        except pan.errors.ParserError as exception:
            print(f"{exception} ! Erro ao ler separador {delimitador}")

        except FileNotFoundError as exception:
            print(f"{exception} ! Arquivo não encontrado")

            return None

        except Exception as exception:
            print(f"{exception} ! Erro ao ler arquivo")

            return None

    print("Codigo -1: Falha grave")
    return None

def leitorGeral(caminhos: list):

    qds = [leitorCsv(item) for item in caminhos]

    qds = [quadro
           for quadro in qds
           if quadro is not None]

    if not qds:
        return (pan
                .DataFrame())

    return (pan
            .concat(qds,
                    ignore_index=True))