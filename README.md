# Entregável 2 - Anotações de imagens com OpenCV

**Autora:** Ana Clara dos Santos

## Objetivo

Visualizador de imagens anotadas em Python. O programa lê as bounding boxes de `dados/anotacoes.csv`, transforma cada anotação em um objeto, agrupa as caixas por imagem e desenha todas elas com OpenCV. As dez imagens são exibidas uma por vez, e as versões anotadas são salvas em `resultados/`.

## Dependências

- Python 3
- opencv-python (listado em `requirements.txt`)
- Ambiente com suporte a janelas gráficas

## Como executar

A partir da raiz do repositório (Linux ou WSL com suporte gráfico):

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python src/main.py
```

## Controles do visualizador

| Tecla | Ação |
|---|---|
| Espaço | Avança para a próxima imagem |
| `q` | Encerra o programa |
| Outras teclas | Mantêm a imagem atual |

Ao chegar ao fim das dez imagens, as janelas são fechadas. Se `q` for pressionado antes, o programa encerra após a imagem atual.

A janela mostra o nome da imagem, a quantidade de caixas e uma legenda de cores (azul para a classe 0 e rosa para a classe 1). Essas informações aparecem só na janela: as imagens salvas em `resultados/` têm apenas as caixas e mantêm a resolução original.

No terminal, o programa imprime o nome da imagem atual e a quantidade de caixas desenhadas.

## Estrutura

- `src/main.py`: programa principal, validação, exibição e loop de visualização.
- `src/modelos.py`: classes `Deteccao` e `ImagemAnotada`.
- `src/arquivos.py`: funções de leitura do CSV e organização dos objetos.
- `dados/`: `anotacoes.csv` e `mapeamento_imagens.csv`.
- `imagens/`: dez imagens originais (não são alteradas).
- `resultados/`: imagens anotadas geradas pela execução.
- `evidencias/`: capturas do terminal e do visualizador.

## Classes

**`Deteccao`**: guarda `classe_id`, `x_min`, `y_min`, `x_max` e `y_max`. O método `desenhar(imagem)` desenha a própria caixa na imagem recebida, usando uma cor por classe.

**`ImagemAnotada`**: guarda o nome e o caminho da imagem e uma lista de objetos `Deteccao`. O método `adicionar_deteccao` inclui uma caixa na lista, e `gerar_imagem_anotada(imagem)` devolve uma cópia da imagem com todas as caixas, chamando o `desenhar` de cada detecção.

## Validações

O programa mostra uma mensagem e encerra se o CSV ou uma imagem não puderem ser lidos, se uma linha tiver campos inválidos ou se as coordenadas não respeitarem `0 ≤ x_min < x_max < largura` e `0 ≤ y_min < y_max < altura`.