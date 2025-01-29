class Jogador:
    """
    Classe que representa um jogador na partida.

    A classe contém o nome do jogador e sua pontuação, permitindo
    a atualização dos pontos durante a partida.
    """
    
    def __init__(self, nome, pontuacao=0):
        """
        Inicializa um jogador com um nome e uma pontuação inicial.

        @param nome: Nome do jogador.
        @param pontuacao: Pontuação inicial do jogador (padrão: 0).
        """

        self.nome = nome
        self.pontuacao = pontuacao

    def atualizar_pontuacao(self, pontos):
        """
        Atualiza a pontuação do jogador somando os pontos fornecidos.

        @param pontos: Quantidade de pontos a serem adicionados à pontuação atual.
        """
        
        self.pontuacao += pontos