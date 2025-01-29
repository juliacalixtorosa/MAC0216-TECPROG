import pytest
from movimento import Movimento
from partida import Partida


@pytest.fixture()
def partida_teste():
    partida = Partida("Teste", 10, 10)
    partida.peça_atual.matriz_peça = partida.peça_atual.gera_peça("T")
    # desenha peças já na matriz?
    return partida

class Test_Movimento():
    
    def test_pode_mover_peça_para_baixo(self, partida_teste):
        
        partida_teste.desenha_peça_na_matriz()

        pode_mover_baixo = Movimento.pode_mover_para_baixo(partida_teste.peça_atual.matriz_peça, partida_teste.matriz_jogo, partida_teste.peça_atual.pos_x, partida_teste.peça_atual.pos_y)
        
        assert pode_mover_baixo == True

    def test_nao_pode_mover_peça_para_baixo(self, partida_teste):

        # inclui a peça mais abaixo
        partida_teste.peça_atual.pos_x = 7
        partida_teste.peça_atual.pos_y = 5
        partida_teste.desenha_peça_na_matriz()

        # inclui a peça mais acima
        partida_teste.peça_atual.gera_peça("T")
        partida_teste.peça_atual.pos_x = 5
        partida_teste.peça_atual.pos_y = 5
        partida_teste.desenha_peça_na_matriz()

        nao_pode_mover_baixo = Movimento.pode_mover_para_baixo(partida_teste.peça_atual.matriz_peça, partida_teste.matriz_jogo, partida_teste.peça_atual.pos_x, partida_teste.peça_atual.pos_y)
        
        assert nao_pode_mover_baixo == False

    def test_pode_mover_peça_para_esquerda(self, partida_teste):
    
        partida_teste.desenha_peça_na_matriz()

        pode_mover_esquerda = Movimento.pode_mover_para_esquerda(partida_teste.peça_atual.matriz_peça, partida_teste.matriz_jogo, partida_teste.peça_atual.pos_x, partida_teste.peça_atual.pos_y)
        
        assert pode_mover_esquerda == True

    def test_nao_pode_mover_peça_para_esquerda(self, partida_teste):

        partida_teste.peça_atual.pos_x = 0
        partida_teste.peça_atual.pos_y = 1
        partida_teste.desenha_peça_na_matriz()

        partida_teste.peça_atual.gera_peça("T")
        partida_teste.peça_atual.pos_x = 0
        partida_teste.peça_atual.pos_y = 4
        partida_teste.desenha_peça_na_matriz()

        nao_pode_mover_esquerda = Movimento.pode_mover_para_esquerda(partida_teste.peça_atual.matriz_peça, partida_teste.matriz_jogo, partida_teste.peça_atual.pos_x, partida_teste.peça_atual.pos_y)
        
        assert nao_pode_mover_esquerda == False

    def test_pode_mover_peça_para_direita(self, partida_teste):
    
        partida_teste.desenha_peça_na_matriz()

        pode_mover_direita = Movimento.pode_mover_para_direita(partida_teste.peça_atual.matriz_peça, partida_teste.matriz_jogo, partida_teste.peça_atual.pos_x, partida_teste.peça_atual.pos_y)
        
        assert pode_mover_direita == True


    def test_nao_pode_mover_peça_para_direita(self, partida_teste):

        partida_teste.peça_atual.pos_x = 0
        partida_teste.peça_atual.pos_y = 4
        partida_teste.desenha_peça_na_matriz()

        partida_teste.peça_atual.gera_peça("T")
        partida_teste.peça_atual.pos_x = 0
        partida_teste.peça_atual.pos_y = 1
        partida_teste.desenha_peça_na_matriz()

        nao_pode_mover_direita = Movimento.pode_mover_para_direita(partida_teste.peça_atual.matriz_peça, partida_teste.matriz_jogo, partida_teste.peça_atual.pos_x, partida_teste.peça_atual.pos_y)
        
        assert nao_pode_mover_direita == False

    def test_pode_colocar_peça(self, partida_teste):

        pode_colocar_peça = Movimento.pode_colocar_na_posicao(partida_teste.peça_atual.matriz_peça, partida_teste.matriz_jogo, partida_teste.peça_atual.pos_x, partida_teste.peça_atual.pos_y)
        
        assert pode_colocar_peça == True

    def test_nao_pode_colocar_peça(self, partida_teste):
      
        partida_teste.desenha_peça_na_matriz()
        partida_teste.peça_atual.gera_peça("T")

        nao_pode_colocar_peça = Movimento.pode_colocar_na_posicao(partida_teste.peça_atual.matriz_peça, partida_teste.matriz_jogo, partida_teste.peça_atual.pos_x, partida_teste.peça_atual.pos_y)

        assert nao_pode_colocar_peça == False
