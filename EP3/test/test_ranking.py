import pytest
from ranking import Ranking
from jogador import Jogador

@pytest.fixture
def ranking():

    # fixture para criar um objeto Ranking com alguns jogadores
    r = Ranking()
    r.ranks = [
        Jogador("Kelly", 21),
        Jogador("Livia", 18),
        Jogador("Matheus", 16),
        Jogador("Julia", 17),
        Jogador("Thainara", 9),
    ]
    return r

class Test_Ranking():
    def test_exibir_rankings(self, capsys, ranking):
        
        ranking.exibir_rankings()
        captured = capsys.readouterr()

        assert "*** Ranking ***" in captured.out
        assert "1         Kelly     21        " in captured.out
        assert "2         Livia     18        " in captured.out
        assert "3         Julia     17        " in captured.out
        assert "4         Matheus   16        " in captured.out
        assert "5         Thainara  9         " in captured.out


    def test_exibir_rankings_sem_pontuacao(self, capsys):
        
        r = Ranking()
        r.ranks = []  
        r.exibir_rankings()
        captured = capsys.readouterr()

        assert "Nenhuma pontuação registrada ainda." in captured.out
