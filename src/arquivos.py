import csv

from modelos import Deteccao, ImagemAnotada


def ler_anotacoes(caminho_csv):
    anotacoes_por_imagem = {}

    with open(caminho_csv, mode="r", encoding="utf-8", newline="") as arquivo:
        leitor = csv.DictReader(arquivo)

        for linha in leitor:
            nome_imagem = linha["imagem"]

            deteccao = Deteccao(
                classe_id=int(linha["classe_id"]),
                x_min=int(linha["x_min"]),
                y_min=int(linha["y_min"]),
                x_max=int(linha["x_max"]),
                y_max=int(linha["y_max"])
            )

            if nome_imagem not in anotacoes_por_imagem:
                anotacoes_por_imagem[nome_imagem] = []

            anotacoes_por_imagem[nome_imagem].append(deteccao)

    return anotacoes_por_imagem


def criar_imagens_anotadas(caminho_csv, pasta_imagens):
    anotacoes_por_imagem = ler_anotacoes(caminho_csv)
    imagens_anotadas = {}

    for nome_imagem, deteccoes in anotacoes_por_imagem.items():
        caminho_imagem = pasta_imagens / nome_imagem

        imagem_anotada = ImagemAnotada(
            nome=nome_imagem,
            caminho=caminho_imagem
        )

        for deteccao in deteccoes:
            imagem_anotada.adicionar_deteccao(deteccao)

        imagens_anotadas[nome_imagem] = imagem_anotada

    return imagens_anotadas