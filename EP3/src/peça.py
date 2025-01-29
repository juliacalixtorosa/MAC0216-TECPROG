import random
from matriz import Matriz

class Peça:
    """
    Classe que representa uma peça do jogo, com métodos para gerar, rotacionar e manipular sua posição na matriz.

    Cada peça é gerada aleatoriamente a partir de um conjunto de formas, e possui métodos para rotacioná-la 
    e definir sua posição na matriz de jogo.
    """

    def __init__(self, posiçao_x, posiçao_y):
        """
        Inicializa uma nova peça na posição especificada.

        @param posiçao_x: A coordenada x da peça na matriz de jogo.
        @param posiçao_y: A coordenada y da peça na matriz de jogo.
        """
        self.pos_x = posiçao_x
        self.pos_y = posiçao_y
        self.matriz_peça = self.gera_peça() 

    def gera_peça(self, nome_aleatorio=None):
        """
        Gera uma peça aleatória ou uma peça específica se o nome for fornecido.

        Caso o parâmetro `nome_aleatorio` não seja fornecido, a peça será gerada aleatoriamente.

        @param nome_aleatorio: O nome da peça (ex: "T", "O", "L"). Se não fornecido, a peça será aleatória.

        @return: A matriz que representa a peça gerada.
        """
        nomes_peças = ["I", "J", "L", "O", "S", "T", "Z"]
        if nome_aleatorio == None:  
            nome_aleatorio = nomes_peças[random.randint(0, len(nomes_peças)-1)]

        return self.peças_do_textris(nome_aleatorio)
    
    def rotacionar_direita(self, peça):
        """
        Rotaciona a matriz da peça 90° para a direita (sentido horário).

        @param peça: A matriz que representa a peça a ser rotacionada.

        @return: A nova matriz da peça após a rotação.
        """

        linhas = len(peça)
        colunas = len(peça[0])

        nova_matriz_peça = Matriz.devolve_matriz_vazia(colunas, linhas)

        for i in range(linhas):
            for j in range(colunas):
                nova_matriz_peça[j][linhas - i - 1] = peça[i][j]  

        return nova_matriz_peça
    
    def rotacionar_esquerda(self, peça):
        """
        Rotaciona a matriz da peça 90° para a esquerda (sentido anti-horário).

        @param peça: A matriz que representa a peça a ser rotacionada.

        @return: A nova matriz da peça após a rotação.
        """

        linhas = len(peça)
        colunas = len(peça[0])

        nova_matriz_peça = Matriz.devolve_matriz_vazia(colunas, linhas)

        for i in range(linhas):
            for j in range(colunas):
                nova_matriz_peça[colunas - j - 1][i] = peça[i][j]  

        return nova_matriz_peça

    def peças_do_textris(self, nome_peça):
        """
        Retorna a matriz que representa a forma da peça com base no nome fornecido.

        @param nome_peça: O nome da peça (ex: "I", "O", "L", etc.).

        @return: A matriz da peça correspondente ao nome fornecido.
        """
        
        dicionario_peças = {
            "I" :   [   ['&'],
                        ['&'],
                        ['&'],
                        ['&']
                    ],
            
            "J" :   [   [" ", '$'],
                        [" ", '$'],
                        [" ", '$'],
                        ['$', '$']
                    ],

            "L" :   [   ['*', " "],
                        ['*', " "],
                        ['*', " "],
                        ['*', '*']

                    ],

            "O" :   [   ['@', '@'],
                        ['@', '@']

                    ],
            
            "S" :   [   [' ', '%', '%'],
                        ['%', '%', ' ']

                    ],

            "T" :   [   ['+', '+', '+'],
                        [' ', '+', ' ']

                    ],

            "Z" :   [   ['#', '#', ' '],
                        [' ', '#', '#']

                    ] 

        }

        return dicionario_peças.get(nome_peça)
    
