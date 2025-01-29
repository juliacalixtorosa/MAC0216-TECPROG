import pytest
from peça import Peça
from partida import Partida


@pytest.fixture()
def peça_teste():
    peça = Peça(5,5)
    peça.matriz_peça = peça.gera_peça("T")
    return peça


@pytest.fixture()
def dic_peças():
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

    return dicionario_peças


class Test_Peça():

    def test_gera_peça_aleatoria(self, dic_peças):

        peça_teste = Peça(0,0)

        foi_gerada = False
        for alguma_peça in dic_peças.values():
            if peça_teste.matriz_peça == alguma_peça:
                foi_gerada = True
                break
            
        assert foi_gerada == True
    
    def test_rotacionar_pra_direita(self, peça_teste):

        nova_peça_teste = peça_teste.rotacionar_direita(peça_teste.matriz_peça)

        peça_esperada = [
            [" ", '+'],
            ['+', '+'],
            [" ", '+']
        ]

        assert nova_peça_teste == peça_esperada

    def test_rotacionar_pra_esquerda(self, peça_teste):

        nova_peça_teste = peça_teste.rotacionar_esquerda(peça_teste.matriz_peça)

        peça_esperada = [
            ['+', " "],
            ['+', '+'],
            ['+', " "]
        ]

        assert nova_peça_teste == peça_esperada
