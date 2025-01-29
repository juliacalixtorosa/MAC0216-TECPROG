from readchar import readkey, key
from tela import Tela
from peça import Peça
from movimento import Movimento
from matriz import Matriz
from time import sleep
from jogador import Jogador
from ranking import Ranking
from datetime import datetime
import pickle

class Partida:
    """
    Classe que representa uma partida de Tetris.

    Ela gerencia a execução do jogo, capturando os movimentos do jogador, gerenciando a matriz de jogo, 
    e verificando as condições de término, além de manipular as peças e pontuação.
    """
    
    def __init__(self, nome_jogador, num_linhas, num_colunas):
        """
        Constrói uma nova partida.

        @param nome_jogador: Nome do jogador.
        @param num_linhas: Número de linhas da matriz de jogo.
        @param num_colunas: Número de colunas da matriz de jogo.
        """

        self.jogador = Jogador(nome_jogador)
        self.num_linhas = int(num_linhas)
        self.num_colunas = int(num_colunas)
        self.pontuacao = 0
        self.partida_rodando = True
        self.peça_atual = Peça(0, ((self.num_colunas - 1) // 2) )
        self.matriz_jogo = Matriz.devolve_matriz_vazia(self.num_linhas,self.num_colunas)
        self.tela = Tela(self.matriz_jogo) 
        self.nova_peça = False
        self.exibe_salvamento = False
    
    def jogar(self):
        """
        Inicia o loop principal do jogo, onde a peça é desenhada na matriz e o jogador captura teclas
        para mover as peças, além de verificar se a partida terminou.

        O loop continua até que a partida seja encerrada, seja por término ou por uma ação do jogador.
        """

        while self.partida_rodando:

            self.desenha_peça_na_matriz()
            self.tela.matriz_jogo = Matriz.copia_matriz(self.matriz_jogo)

            self.tela.exibe_matriz()
            self.tela.exibe_comandos(self.pontuacao)

            # Captura os movimentos do jogador
            self.captura_teclas()

            # Verifica se uma nova peça deve ser gerada
            if self.nova_peça:
                self.peça_atual = Peça(0, ((self.num_colunas - 1) // 2)) 
                self.nova_peça = False  
                self.verifica_fim_de_jogo(self.peça_atual.matriz_peça, self.peça_atual.pos_x, self.peça_atual.pos_y)
                self.atualiza_pontuaçao()  
                

            self.tela.limpa_tela()

        if self.exibe_salvamento:
            self.tela.exibe_comandos_salvamento_partida()
        else:    
            Ranking.ranks.append(self.jogador)
            self.tela.exibe_comandos_game_over(self.pontuacao)
 
    def captura_teclas(self):
        """
        Captura a entrada de teclas do jogador para realizar os movimentos da peça.

        O jogador pode mover a peça para baixo, para a esquerda, para a direita ou rotacioná-la.
        Também pode salvar ou encerrar a partida.
        """

        while True:
            tecla = readkey()

            if tecla == key.DOWN:
                self.movimento_vertical()
                break
            
            elif tecla == key.RIGHT:
                self.movimento_horizontal("direita")
                break
            
            elif tecla == key.LEFT:
                self.movimento_horizontal("esquerda")
                break
            
            elif tecla == key.PAGE_DOWN:
                self.movimento_rotaciona("esquerda")
                break
            
            elif tecla == key.PAGE_UP: 
                self.movimento_rotaciona("direita")
                break

            elif tecla == "s" or tecla == "S":
                self.para_partida()
                break
            elif tecla == "g" or tecla == "G":
                self.grava_sai_partida()
                break
            else:
                self.tela.limpa_tela()
                self.tela.exibe_matriz()
                self.tela.exibe_comandos(self.pontuacao)
                
    def desenha_peça_na_matriz(self):
        """
        Desenha a peça atual na matriz do jogo, posicionando-a na posição indicada por `pos_x` e `pos_y`.

        A peça é desenhada na matriz de jogo, modificando a matriz conforme sua posição.
        """

        for i in range(len(self.peça_atual.matriz_peça)):  
            for j in range(len(self.peça_atual.matriz_peça[i])):  
                caracter = self.peça_atual.matriz_peça[i][j]
                if caracter != " ":
                    x = self.peça_atual.pos_x + i  # calcula x na matriz do jogo
                    y = self.peça_atual.pos_y + j  # calcula y na matriz do jogo

                    if 0 <= x < len(self.matriz_jogo) and 0 <= y < len(self.matriz_jogo[0]):
                        self.matriz_jogo[x][y] = caracter  
                        

    def apaga_peça_na_matriz(self):
        """
        Apaga a peça atual da matriz do jogo.

        A peça é apagada da matriz de jogo, substituindo as posições ocupadas por ela com espaços.
        """

        for i in range(len(self.peça_atual.matriz_peça)):
            for j in range(len(self.peça_atual.matriz_peça[i])):
                caracter = self.peça_atual.matriz_peça[i][j]
                if caracter != " ":
                    x = self.peça_atual.pos_x + i 
                    y = self.peça_atual.pos_y + j
                    if 0 <= x < self.num_linhas and 0 <= y < self.num_colunas:
                        self.matriz_jogo[x][y] = " "  


    def atualiza_pontuaçao(self):
        """
        Atualiza a pontuação e remove linhas preenchidas da matriz do jogo.

        Este método verifica todas as linhas da matriz do jogo para identificar quais estão totalmente preenchidas.
        As linhas preenchidas são removidas, e as linhas acima delas são "descidas" para preencher o espaço vazio.
        A pontuação é atualizada com base no número de linhas removidas.

        Esquema de pontuação:
        - 1 linha: +1 ponto
        - 2 linhas: +3 pontos
        - 3 linhas: +5 pontos
        - 4 ou mais linhas: +7 pontos

        @note O método também atualiza a pontuação do jogador associado à partida.
        """

        linhas_remover = [] # vai guardar os índices das linhas para remover

        # agora, vamos percorrer todos elementos da matriz
        # se temos que uma linha todos elementos NÃO são " ", que dizer que a linha está preenchida
        # e podemos removê-las
        for i in range(len(self.matriz_jogo)):  
            linha_preenchida = True  

            for c in self.matriz_jogo[i]:  
                if c == " ":  
                    linha_preenchida = False
                    break  

            if linha_preenchida:  
                linhas_remover.append(i)

        # remover as linhas completas e "descer" as linhas acima delas
        linhas_remover.sort()

        for lin in linhas_remover:
            for i in range(lin, 0, -1):  
                for j in range(self.num_colunas):  
                    self.matriz_jogo[i][j] = self.matriz_jogo[i - 1][j]  # substitui pela linha acima
        
        # limpar a primeira linha
        for j in range(self.num_colunas):
            self.matriz_jogo[0][j] = " "
        
        # esquema de pontuação
        pontos = 0
        if(len(linhas_remover) == 1):
            pontos = 1
        elif(len(linhas_remover) == 2):
            pontos = 3
        elif(len(linhas_remover) == 3):
            pontos = 5
        elif(len(linhas_remover) >= 4):
            pontos = 7

        self.pontuacao += pontos
        self.jogador.atualizar_pontuacao(pontos)


    def verifica_fim_de_jogo(self, matriz_peça, pos_x_peça, pos_y_peça):
        """
        Verifica se a nova peça pode ser colocada no topo da matriz sem colidir com outras peças.

        @param matriz_peça: A matriz da peça que será verificada.
        @param pos_x_peça: A posição x da peça na matriz de jogo.
        @param pos_y_peça: A posição y da peça na matriz de jogo.
        """
        if Movimento.pode_colocar_na_posicao(matriz_peça, self.matriz_jogo, pos_x_peça, pos_y_peça):
            self.partida_rodando = True
        
        else:
            self.partida_rodando = False

    
    def movimento_vertical(self):
        """
        Move a peça para baixo, se possível, e redesenha a matriz de jogo.

        Se a peça não puder se mover para baixo, marca que uma nova peça deve ser gerada.
        """
        if Movimento.pode_mover_para_baixo(self.peça_atual.matriz_peça, self.matriz_jogo, self.peça_atual.pos_x, self.peça_atual.pos_y):
            self.apaga_peça_na_matriz()
            self.peça_atual.pos_x += 1
            self.desenha_peça_na_matriz()
        else:
            self.desenha_peça_na_matriz()
            self.nova_peça = True  


    def movimento_horizontal(self,direçao):
        """
        Move a peça para a esquerda ou direita, se possível, e redesenha a matriz de jogo.

        @param direçao: A direção do movimento ("direita" ou "esquerda").
        """

        if direçao == "direita" and Movimento.pode_mover_para_direita(self.peça_atual.matriz_peça, self.matriz_jogo, self.peça_atual.pos_x, self.peça_atual.pos_y):
            self.apaga_peça_na_matriz()
            self.peça_atual.pos_y += 1 
            self.desenha_peça_na_matriz()

        elif direçao == "esquerda" and Movimento.pode_mover_para_esquerda(self.peça_atual.matriz_peça, self.matriz_jogo, self.peça_atual.pos_x, self.peça_atual.pos_y):
            self.apaga_peça_na_matriz()
            self.peça_atual.pos_y -= 1  
            self.desenha_peça_na_matriz()


    def movimento_rotaciona(self,direçao):
        """
        Rotaciona a peça atual 90° para a direita ou para a esquerda, se possível.

        @param direçao: A direção da rotação ("direita" ou "esquerda").
        """

        self.peça_auxiliar = Peça(self.peça_atual.pos_x, self.peça_atual.pos_y)
        matriz_atual_peça = self.peça_auxiliar.matriz_peça = Matriz.copia_matriz(self.peça_atual.matriz_peça)

        # Rotações baseadas na direção
        if direçao == "direita":
            nova_matriz_rotacionada = self.peça_auxiliar.rotacionar_direita(matriz_atual_peça)
        elif direçao == "esquerda":
            nova_matriz_rotacionada = self.peça_auxiliar.rotacionar_esquerda(matriz_atual_peça)

        self.apaga_peça_na_matriz()

        if Movimento.pode_colocar_na_posicao(nova_matriz_rotacionada, self.matriz_jogo, self.peça_auxiliar.pos_x, self.peça_auxiliar.pos_y):
            # aplica a rotação na peça atual
            self.peça_atual.matriz_peça = Matriz.copia_matriz(nova_matriz_rotacionada)
            
            self.peça_atual.pos_x = self.peça_auxiliar.pos_x
            self.peça_atual.pos_y = self.peça_auxiliar.pos_y

        self.desenha_peça_na_matriz()


    def para_partida(self):
        """
        Encerra a partida antes de seu término natural.

        Este método altera o estado de 'partida_rodando' para 'False', sinalizando que a partida foi encerrada 
        de forma antecipada. Pode ser utilizado para interromper a partida em situações como salvamento ou saída.
        """

        self.partida_rodando = False


    def grava_sai_partida(self):
        """
        Salva o estado atual da partida e encerra.

        Este método salva o estado atual da partida em um arquivo no formato .pkl. O nome do arquivo
        inclui o nome do jogador e o timestamp do momento em que o salvamento foi feito. Após salvar
        o estado, a partida é encerrada chamando o método 'para_partida'.

        @note O arquivo gerado é registrado no atributo 'arquivos_gravados' da classe 'Jogo'.
        """
        
        time = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_arquivo = f"{self.jogador.nome}_{time}.pkl"
        with open(nome_arquivo, "wb") as f:
            pickle.dump(self, f)

        from jogo import Jogo # importação localizada
        Jogo.arquivos_gravados.append(nome_arquivo)
        self.exibe_salvamento = True
        self.para_partida()
