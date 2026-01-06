from typing import Tuple


def analisar_dimob(conteudo: str) -> Tuple[int, int, int, int]:
    """
    Recebe o conteúdo completo do arquivo DIMOB (string)
    e devolve:
      total_linhas, qtd_r01, qtd_r02, qtd_outros
    """
    total_linhas = 0
    count_r01 = 0
    count_r02 = 0

    for linha in conteudo.splitlines():
        linha = linha.rstrip("\n")
        if not linha.strip():
            # ignora linhas totalmente em branco
            continue

        total_linhas += 1

        if linha.startswith("R01"):
            count_r01 += 1
        elif linha.startswith("R02"):
            count_r02 += 1

    outros = total_linhas - (count_r01 + count_r02)
    return total_linhas, count_r01, count_r02, outros
