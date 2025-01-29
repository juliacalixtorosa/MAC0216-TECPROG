class Movimento:
    """
    Classe que contém métodos estáticos responsáveis por verificar os movimentos das peças no jogo.

    Esses métodos permitem que as peças se movam para a esquerda, direita, para baixo, além de rotacioná-las. 
    Eles verificam as condições necessárias para o movimento, como limites da matriz e colisões com outras peças.
    """

    @staticmethod
    def pode_mover_para_esquerda(matriz_da_peça, matriz_do_jogo, pos_x_peça, pos_y_peça):
        """
        Verifica se a peça pode se mover para a esquerda.

        Esse método percorre a matriz da peça e verifica se existe alguma parte da peça na borda esquerda. 
        Se houver espaço livre à esquerda ou se a peça não colidir com outras peças, o movimento é permitido.

        @param matriz_da_peça: A matriz que representa a forma da peça.
        @param matriz_do_jogo: A matriz que representa o estado atual do jogo, incluindo as peças fixadas.
        @param pos_x_peça: A coordenada x da peça na matriz de jogo.
        @param pos_y_peça: A coordenada y da peça na matriz de jogo.

        @return: True se o movimento para a esquerda for possível, False caso contrário.
        """
        for i in range(len(matriz_da_peça)):  
            for j in range(len(matriz_da_peça[0])):  
                if matriz_da_peça[i][j] != " ":  
                    coluna_a_esquerda = j - 1  

                    # verifica as células na borda esquerda ou que possuem " " à esquerda na peça
                    if coluna_a_esquerda < 0 or matriz_da_peça[i][coluna_a_esquerda] == " ":
                        x = pos_x_peça + i  # coordenada x na matriz do jogo
                        y = pos_y_peça + j - 1  # coordenada y na matriz do jogo

                        # verifica limites ou colisão
                        if y < 0 or matriz_do_jogo[x][y] != " ":
                            return False  

        return True  

    @staticmethod
    def pode_mover_para_direita(matriz_da_peça, matriz_do_jogo, pos_x_peça, pos_y_peça):
        """
        Verifica se a peça pode se mover para a direita.

        Esse método percorre a matriz da peça e verifica se existe alguma parte da peça na borda direita.
        Se houver espaço livre à direita ou se a peça não colidir com outras peças, o movimento é permitido.

        @param matriz_da_peça: A matriz que representa a forma da peça.
        @param matriz_do_jogo: A matriz que representa o estado atual do jogo, incluindo as peças fixadas.
        @param pos_x_peça: A coordenada x da peça na matriz de jogo.
        @param pos_y_peça: A coordenada y da peça na matriz de jogo.

        @return: True se o movimento para a direita for possível, False caso contrário.
        """

        for i in range(len(matriz_da_peça)):  
            for j in range(len(matriz_da_peça[0])):  
                if matriz_da_peça[i][j] != " ": 
                    coluna_a_direita = j + 1  

                    # verifica as células na borda direita ou que possuem " " à direita na peça
                    if coluna_a_direita >= len(matriz_da_peça[0]) or matriz_da_peça[i][coluna_a_direita] == " ":
                        x = pos_x_peça + i  # coordenada x na matriz do jogo
                        y = pos_y_peça + j + 1  # coordenada y  na matriz do jogo

                        # verifica limites ou colisão
                        if y >= len(matriz_do_jogo[0]) or matriz_do_jogo[x][y] != " ":
                            return False  
        return True 

    @staticmethod
    def pode_mover_para_baixo(matriz_da_peça, matriz_do_jogo, pos_x_peça, pos_y_peça):
        """
        Verifica se a peça pode se mover para a direita.

        Esse método percorre a matriz da peça e verifica se existe alguma parte da peça na borda direita.
        Se houver espaço livre à direita ou se a peça não colidir com outras peças, o movimento é permitido.

        @param matriz_da_peça: A matriz que representa a forma da peça.
        @param matriz_do_jogo: A matriz que representa o estado atual do jogo, incluindo as peças fixadas.
        @param pos_x_peça: A coordenada x da peça na matriz de jogo.
        @param pos_y_peça: A coordenada y da peça na matriz de jogo.

        @return: True se o movimento para a direita for possível, False caso contrário.
        """

        for i in range(len(matriz_da_peça)):  
            for j in range(len(matriz_da_peça[0])):  
                
                if matriz_da_peça[i][j] != " ":  
                    proxima_linha_peça = i + 1  

                    # verifica as células da peça que estão na última linha ou
                    # as que abaixo é vazio
                    if ((proxima_linha_peça >= len(matriz_da_peça))
                        or (matriz_da_peça[proxima_linha_peça][j] == " ")):

                        # verifica a célula abaixo na matriz do jogo
                        x = pos_x_peça + i + 1  
                        y = pos_y_peça + j  

                        # colide com outra peça ou a grade
                        if x >= len(matriz_do_jogo) or matriz_do_jogo[x][y] != " ":
                            return False

        return True  

    @staticmethod
    def pode_colocar_na_posicao(nova_matriz_peça, matriz_do_jogo, nova_pos_x, nova_pos_y):
        """
        Verifica se a nova matriz da peça pode ser colocada na nova posição sem ultrapassar limites
        ou colidir com outras peças.

        @param nova_matriz_peça: A nova matriz da peça após rotação.
        @param matriz_do_jogo: A matriz que representa o estado atual do jogo, incluindo as peças fixadas.
        @param nova_pos_x: A nova coordenada x onde a peça será colocada.
        @param nova_pos_y: A nova coordenada y onde a peça será colocada.

        @return: True se a peça pode ser colocada na nova posição, False caso contrário.
        """
        for i in range(len(nova_matriz_peça)):
            for j in range(len(nova_matriz_peça[0])):
                if nova_matriz_peça[i][j] != " ":
                    x = nova_pos_x + i
                    y = nova_pos_y + j

                    # Verifica limites da grade
                    if x < 0 or x >= len(matriz_do_jogo) or y < 0 or y >= len(matriz_do_jogo[0]):
                        return False

                    # Verifica colisão com outra peça
                    if matriz_do_jogo[x][y] != " ":
                        return False
        return True
