import os

class Tela:
    """
    Classe responsável por exibir o estado do jogo no terminal.

    A classe cuida da renderização da matriz do jogo, exibindo as peças no terminal e os comandos
    do jogo, além de fornecer mensagens relacionadas ao andamento da partida, como pontuação e
    mensagens de fim de jogo.
    """

    def __init__(self, matriz_partida):
        """
        Inicializa a classe Tela.

        @param matriz_partida: Matriz que representa o estado atual do jogo, 
        contendo as peças e o layout do tabuleiro.
        """

        self.matriz_tela = matriz_partida

    def exibe_matriz(self):
        """
        Exibe a matriz do jogo no terminal, com as bordas e as peças, representando o estado
        atual da partida.

        A função limpa a tela e, em seguida, exibe a matriz com uma borda ao redor dela.
        """

        self.limpa_tela()

        print("+" + "-" * (len (self.matriz_tela[0])) + "+")  

        for linha in self.matriz_tela:
            linha_formatada = "|"
            for caracter in linha:
                linha_formatada += caracter
            linha_formatada += "|"
            print(linha_formatada)

        print("+" + "-" * (len (self.matriz_tela[0])) + "+")  

    def exibe_comandos(self, pontuacao):
        """
        Exibe as instruções e os controles do jogo no terminal.

        Esta função exibe as teclas de comando disponíveis e a pontuação atual do jogador.

        @param pontuacao: A pontuação atual do jogador, que será exibida ao lado das instruções.
        """

        print("\nPontuação:", pontuacao)
        print("Teclas do jogo:")
        print("← move esquerda | → move direita | ↓ move baixo")
        print("<Page Down> rotaciona esquerda | <Page Up> rotaciona direita")
        print("<s> sai da partida | <g> grava e sai da partida")


    def exibe_comandos_game_over(self, pontuacao):
        """
        Exibe uma mensagem de fim de jogo, incluindo a pontuação final.

        Esta função é chamada quando a partida chega ao fim, e mostra ao jogador sua pontuação final.

        @param pontuacao: A pontuação final do jogador, que será exibida na tela.
        """
        print("Fim da partida!")
        print("Pontuação final:", pontuacao)
        print("\n*** Jogo Textris - um tetris em modo texto ***")
    
    def exibe_comandos_salvamento_partida(self):
        print("Sua partida foi salva!")
        print("\n*** Jogo Textris - um tetris em modo texto ***")

    def limpa_tela(self):
        """
        Limpa a tela do terminal para atualizar a visualização do jogo.
        """
        os.system('cls || clear')