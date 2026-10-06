import cv2


class Deteccao:
    CORES = {
    0: (255, 200, 150),  # azul
    1: (180, 105, 255)   # rosa
}

    def __init__(self, classe_id, x_min, y_min, x_max, y_max):
        self.classe_id = int(classe_id)
        self.x_min = int(x_min)
        self.y_min = int(y_min)
        self.x_max = int(x_max)
        self.y_max = int(y_max)

    def desenhar(self, imagem):
        cor = self.CORES[self.classe_id]

        ponto_inicial = (self.x_min, self.y_min)
        ponto_final = (self.x_max, self.y_max)

        cv2.rectangle(
            imagem,
            ponto_inicial,
            ponto_final,
            cor,
            2
        )


class ImagemAnotada:
    def __init__(self, nome, caminho):
        self.nome = nome
        self.caminho = caminho
        self.deteccoes = []

    def adicionar_deteccao(self, deteccao):
        self.deteccoes.append(deteccao)

    def gerar_imagem_anotada(self, imagem):
        imagem_anotada = imagem.copy()

        for deteccao in self.deteccoes:
            deteccao.desenhar(imagem_anotada)

        return imagem_anotada