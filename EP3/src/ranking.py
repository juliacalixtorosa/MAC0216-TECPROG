class Ranking:
    """
    Classe que gerencia o ranking de pontuações no jogo.

    A classe 'Ranking' armazena as pontuações dos jogadores e fornece métodos para exibir 
    as melhores pontuações em ordem decrescente. O ranking pode ser atualizado dinamicamente
    durante o jogo, adicionando novos jogadores e suas pontuações.

    @note O ranking é armazenado na lista 'ranks', que contém objetos de jogadores com 
    atributos 'nome' e 'pontuacao'.
    """

    ranks = []

    def exibir_rankings(self):
        """
        Mostra as melhores pontuações já alcançadas no jogo em execução.

        Este método exibe o ranking dos jogadores em ordem decrescente de pontuação. Apenas
        os 10 melhores jogadores são exibidos. Caso não haja jogadores no ranking, uma mensagem
        indicando a ausência de pontuações será mostrada.

        @note A lista 'ranks' é ordenada em ordem decrescente de pontuação antes da exibição.
        """

        print("\n*** Ranking ***")

        # iremos ordenar a lista de ranks por pontuação dos jogadores, da maior para a menor
        self.ranks.sort(key=lambda jogador: jogador.pontuacao, reverse=True)

        if not self.ranks:
            print("Nenhuma pontuação registrada ainda.\n")
            return
        else:
            # f-strings
            # f"{valor:preenchimento<largura}"
            print(f"{'Posição':<10}{'Jogador':<10}{'Pontuação':<10}")
            print("-" * 40)

            for i in range(min(len(self.ranks), 10)):
                print(f"{i+1:<10}{self.ranks[i].nome:<10}{self.ranks[i].pontuacao:<10}")
            
            print("\n")