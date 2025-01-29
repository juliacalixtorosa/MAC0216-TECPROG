import pytest
import os
from unittest.mock import patch
from jogo import Jogo

@pytest.fixture
def jogo():
    # fixture para criar uma instância de Jogo
    return Jogo()

class Test_Jogo():
    def test_carregar_partida(self, capsys, jogo):

        ## testando para quando não há arquivos ##
        jogo.arquivos_gravados = []

        jogo.carregar_partida()
        captured = capsys.readouterr()

        assert "Não há partidas salvas." in captured.out

        ## testando quando há arquivos e o arquivo requerido existe ##
        jogo.arquivos_gravados = ["thai_2024_12_07.pkl"]
        
        with patch("builtins.input", return_value="thai_2024_12_07.pkl"):
            jogo.carregar_partida()
            captured = capsys.readouterr()

            assert "Partidas salvas:" in captured.out
            assert "thai_2024_12_07.pkl" in captured.out

        ## testando quando há arquivos e o arquivo requerido NÃO existe ##

        jogo.arquivos_gravados = ["thai_2024_12_07.pkl"]
        
        with patch("builtins.input", return_value="ju_2024_12_06.pkl"):
            jogo.carregar_partida()
            captured = capsys.readouterr()

            assert "Partidas salvas:" in captured.out
            assert "thai_2024_12_07.pkl" in captured.out
            assert "Essa partida não existe." in captured.out
        


    def test_sair_jogo(self, jogo):

        jogo.arquivos_gravados = ["thai_2024_12_07.pkl", "ju_2024_12_06.pkl"]

        # cria os arquivos para simulaçao
        for arquivo in jogo.arquivos_gravados:
            with open(arquivo, "w") as f:
                f.write("simulação")

        jogo.sair_jogo()

        # verifica se os arquivos foram removidos
        for arquivo in jogo.arquivos_gravados:
            assert not os.path.exists(arquivo)  

    

