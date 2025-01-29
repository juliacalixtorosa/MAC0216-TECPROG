import pytest
import os
from partida import Partida


@pytest.fixture()
def partida_teste():
    partida = Partida("Teste", 10, 10)
    partida.peça_atual.matriz_peça = partida.peça_atual.gera_peça("T")
    return partida


class Test_Partida():
    def test_desenha_na_matriz_peça_posiçao_inicial(self, partida_teste):
        """
        testa se a peça gerada vai ser colocada na  posição  inicial correta
        """
        partida_teste.desenha_peça_na_matriz()

        matriz_jogo_esperada = [
            [ " ", " ", " ", " ", '+', '+', '+', " ", " ", " "],
            [ " ", " ", " ", " ", " ", '+', " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
            
        ]

        assert partida_teste.matriz_jogo == matriz_jogo_esperada

    def test_desenha_na_matriz_peça_posiçao_qualquer(self, partida_teste):

        partida_teste.peça_atual.pos_x = 5
        partida_teste.peça_atual.pos_y = 5
        partida_teste.desenha_peça_na_matriz()

        matriz_jogo_esperada = [
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", '+', '+', '+', " ", " "],
            [ " ", " ", " ", " ", " ", " ", '+', " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
            
        ]

        assert partida_teste.matriz_jogo == matriz_jogo_esperada

    def test_apaga_na_matriz(self, partida_teste):

        partida_teste.peça_atual.pos_x = 5
        partida_teste.peça_atual.pos_y = 5
        partida_teste.desenha_peça_na_matriz()
        partida_teste.apaga_peça_na_matriz()

        matriz_jogo_esperada = [
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
            
        ]

        assert partida_teste.matriz_jogo == matriz_jogo_esperada

    def test_peça_move_na_vertical(self, partida_teste):

        partida_teste.peça_atual.pos_x = 5
        partida_teste.peça_atual.pos_y = 5
        partida_teste.desenha_peça_na_matriz()
        partida_teste.movimento_vertical()

        matriz_jogo_esperada = [
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", '+', '+', '+', " ", " "],
            [ " ", " ", " ", " ", " ", " ", '+', " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
            
        ]

        assert partida_teste.matriz_jogo == matriz_jogo_esperada

    def test_peça_nao_move_na_vertical(self, partida_teste):

        # inclui a peça mais abaixo
        partida_teste.peça_atual.pos_x = 7
        partida_teste.peça_atual.pos_y = 5
        partida_teste.desenha_peça_na_matriz()

        # inclui a peça mais acima
        partida_teste.peça_atual.gera_peça("T")
        partida_teste.peça_atual.pos_x = 5
        partida_teste.peça_atual.pos_y = 5
        partida_teste.desenha_peça_na_matriz()

        # tenta mover a peça mais acima para baixo 
        # o movimento não é realizado e peça permanece imóvel
        partida_teste.movimento_vertical()

        matriz_jogo_esperada = [
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", '+', '+', '+', " ", " "],
            [ " ", " ", " ", " ", " ", " ", '+', " ", " ", " "],
            [ " ", " ", " ", " ", " ", '+', '+', '+', " ", " "],
            [ " ", " ", " ", " ", " ", " ", '+', " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "]
            
        ]

        assert partida_teste.matriz_jogo == matriz_jogo_esperada

    def test_atualiza_pontuaçao(self, partida_teste):

        matriz_esperada = [
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "] 
        ]
        
        ## teste para pontuação = 1 ##
        partida_teste.matriz_jogo[9] = ["+"] * 10  
        partida_teste.atualiza_pontuaçao()
        assert partida_teste.matriz_jogo == matriz_esperada
        assert partida_teste.pontuacao == 1

        ## teste para pontuação = 3 ##
        # reinicia o estado da partida
        partida_teste.matriz_jogo = [
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "] 
        ]

        partida_teste.matriz_jogo[8] = ["+"] * 10
        partida_teste.matriz_jogo[9] = ["+"] * 10
        partida_teste.atualiza_pontuaçao()
        assert partida_teste.matriz_jogo == matriz_esperada
        assert partida_teste.pontuacao == 4 # 1 ponto anterior + 3

        ## teste para pontuação = 5 ##
        partida_teste.matriz_jogo = [
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "] 
        ]

        partida_teste.matriz_jogo[7] = ["+"] * 10
        partida_teste.matriz_jogo[8] = ["+"] * 10
        partida_teste.matriz_jogo[9] = ["+"] * 10
        partida_teste.atualiza_pontuaçao()
        assert partida_teste.matriz_jogo == matriz_esperada
        assert partida_teste.pontuacao == 9 # 4 pontos anterior + 5

        ## teste para pontuação = 7 ##
        partida_teste.matriz_jogo = [
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [ " ", " ", " ", " ", " ", " ", " ", " ", " ", " "] 
        ]

        partida_teste.matriz_jogo[6] = ["+"] * 10
        partida_teste.matriz_jogo[7] = ["+"] * 10
        partida_teste.matriz_jogo[8] = ["+"] * 10
        partida_teste.matriz_jogo[9] = ["+"] * 10
        partida_teste.atualiza_pontuaçao()
        assert partida_teste.matriz_jogo == matriz_esperada
        assert partida_teste.pontuacao == 16 # 9 pontos anterior + 7 

    def test_peça_move_na_horizontal(self, partida_teste):

        partida_teste.peça_atual.pos_y = 5  # seta a posição inicial na coluna 5
        partida_teste.movimento_horizontal("direita") # move para direita
        assert partida_teste.peça_atual.pos_y == 6

        partida_teste.movimento_horizontal("esquerda") # move para esquerda
        assert partida_teste.peça_atual.pos_y == 5

    def test_peça_nao_move_na_horizontal(self, partida_teste):

        partida_teste.peça_atual.pos_y = 9 # última coluna disponivel
        partida_teste.movimento_horizontal("direita") # tentamos mover

        assert partida_teste.peça_atual.pos_y == 9
    
    def test_peça_rotaciona(self, partida_teste):

        partida_teste.peça_atual.pos_x = 5
        partida_teste.peça_atual.pos_y = 5
        partida_teste.peça_atual.matriz_peça = partida_teste.peça_atual.gera_peça("T")
        partida_teste.desenha_peça_na_matriz()

        partida_teste.movimento_rotaciona("direita")
        matriz_esperada_rotacao_direita = [
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", "+", " ", " ", " "],
            [" ", " ", " ", " ", " ", "+", "+", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", "+", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        ]
        assert partida_teste.matriz_jogo == matriz_esperada_rotacao_direita

        partida_teste.movimento_rotaciona("esquerda")
        matriz_esperada_rotacao_esquerda = [
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", "+", "+", "+", " ", " "],
            [" ", " ", " ", " ", " ", " ", "+", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
        ]
        assert partida_teste.matriz_jogo == matriz_esperada_rotacao_esquerda
        
    def test_peça_não_rotaciona(self, partida_teste):
        
        # desenhamos ela na base, sem chance de rotacionar
        partida_teste.peça_atual.pos_x = 8
        partida_teste.peça_atual.pos_y = 3
        partida_teste.peça_atual.matriz_peça = partida_teste.peça_atual.gera_peça("T")
        partida_teste.desenha_peça_na_matriz()

        matriz_antes_rotacao = [
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " ", " ", " ", " ", " "],
            [" ", " ", " ", "+", "+", "+", " ", " ", " ", " "],
            [" ", " ", " ", " ", "+", " ", " ", " ", " ", " "],
        ]   
        
        partida_teste.movimento_rotaciona("direita")
        assert partida_teste.matriz_jogo == matriz_antes_rotacao # não mudou 

    def test_grava_sai_partida(self, partida_teste):
        
        partida_teste.grava_sai_partida()

        arquivos_criados = [
            arquivo for arquivo in os.listdir(".") if arquivo.endswith(".pkl")
        ]
        assert len(arquivos_criados) == 1

        # remove o arquivo gerado após o teste
        for arquivo in arquivos_criados:
            os.remove(os.path.join(arquivo))

