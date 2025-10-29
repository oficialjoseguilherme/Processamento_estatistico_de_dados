import pandas as pan

def leitor_dengue(path):
    separators = [',', ';', '\t']

    for separator in separators:
        try:

            quadro = pan.read_csv(path, sep=separator)

            print(f"Codigo 1: Separador {separator}")
            return quadro

        except pan.errors.ParserError as exception:
            print(f"{exception} ! Erro ao ler separador {separator}")
        except FileNotFoundError as exception:
            print(f"{exception} ! Arquivo não encontrado")
            return None
        except Exception as exception:
            print(f"{exception} ! Erro ao ler arquivo")
            return None

    print("Codigo -1: Falha grave")
    return None

