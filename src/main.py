from pathlib import Path

import cv2

from arquivos import criar_imagens_anotadas
from modelos import Deteccao


COR_TEXTO = (255, 255, 255)

LARGURA_MAXIMA = 1200
ALTURA_MAXIMA = 800


def validar_deteccoes(imagem, imagem_anotada):
    altura, largura = imagem.shape[:2]

    for deteccao in imagem_anotada.deteccoes:
        if deteccao.classe_id not in (0, 1):
            raise ValueError(
                f"Classe inválida na imagem {imagem_anotada.nome}: "
                f"{deteccao.classe_id}"
            )

        if not (
            0 <= deteccao.x_min < deteccao.x_max < largura
            and
            0 <= deteccao.y_min < deteccao.y_max < altura
        ):
            raise ValueError(
                f"Coordenadas inválidas na imagem "
                f"{imagem_anotada.nome}: "
                f"({deteccao.x_min}, {deteccao.y_min}) - "
                f"({deteccao.x_max}, {deteccao.y_max})"
            )


def redimensionar_para_exibicao(imagem):
    altura, largura = imagem.shape[:2]

    escala_largura = LARGURA_MAXIMA / largura
    escala_altura = ALTURA_MAXIMA / altura
    escala = min(escala_largura, escala_altura, 1)

    if escala == 1:
        return imagem.copy()

    nova_largura = int(largura * escala)
    nova_altura = int(altura * escala)

    return cv2.resize(
        imagem,
        (nova_largura, nova_altura)
    )


def adicionar_informacoes_na_tela(imagem, nome, quantidade):
    faixa = 32
    visualizacao = cv2.copyMakeBorder(
        imagem, 0, faixa, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)
    )
    altura, largura = visualizacao.shape[:2]
    y = altura - 11
    fonte = cv2.FONT_HERSHEY_SIMPLEX

    cv2.putText(
        visualizacao, f"{nome}  |  {quantidade} caixas",
        (10, y), fonte, 0.5, (255, 255, 255), 1
    )

    x = largura - 200
    for classe_id in (0, 1):
        cor = Deteccao.CORES[classe_id]
        cv2.rectangle(visualizacao, (x, y - 12), (x + 14, y + 2), cor, -1)
        cv2.putText(
            visualizacao, f"Classe {classe_id}",
            (x + 20, y), fonte, 0.5, (255, 255, 255), 1
        )
        x += 100

    return visualizacao


def esperar_comando():
    while True:
        tecla = cv2.waitKey(0) & 0xFF

        if tecla == ord("q"):
            return "sair"

        if tecla == 32:
            return "proxima"


def main():
    caminho_csv = Path("dados/anotacoes.csv")
    pasta_imagens = Path("imagens")
    pasta_resultados = Path("resultados")

    pasta_resultados.mkdir(parents=True, exist_ok=True)

    try:
        imagens_anotadas = criar_imagens_anotadas(
            caminho_csv,
            pasta_imagens
        )
    except (OSError, KeyError, ValueError) as erro:
        print(f"Erro ao ler as anotações: {erro}")
        return

    nomes_imagens = sorted(imagens_anotadas.keys())

    for nome_imagem in nomes_imagens:
        imagem_anotada = imagens_anotadas[nome_imagem]

        imagem_original = cv2.imread(
            str(imagem_anotada.caminho)
        )

        if imagem_original is None:
            print(
                f"Erro: não foi possível ler a imagem "
                f"{imagem_anotada.caminho}"
            )
            cv2.destroyAllWindows()
            return

        try:
            validar_deteccoes(
                imagem_original,
                imagem_anotada
            )
        except ValueError as erro:
            print(f"Erro nas anotações: {erro}")
            cv2.destroyAllWindows()
            return

        imagem_com_caixas = imagem_anotada.gerar_imagem_anotada(
            imagem_original
        )

        caminho_resultado = pasta_resultados / nome_imagem

        if not cv2.imwrite(
            str(caminho_resultado),
            imagem_com_caixas
        ):
            print(
                f"Erro: não foi possível salvar "
                f"{caminho_resultado}"
            )
            cv2.destroyAllWindows()
            return

        visualizacao = redimensionar_para_exibicao(
            imagem_com_caixas
        )

        visualizacao = adicionar_informacoes_na_tela(
            visualizacao,
            nome_imagem,
            len(imagem_anotada.deteccoes)
        )

        print(
            f"Imagem atual: {nome_imagem} | "
            f"Caixas desenhadas: "
            f"{len(imagem_anotada.deteccoes)}"
        )

        cv2.imshow(
            "Visualizador de anotacoes",
            visualizacao
        )

        comando = esperar_comando()

        if comando == "sair":
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()