from partida import Partida
from ranking import Ranking
import pickle
import os

class Jogo:
    """
    Classe principal que gerencia o jogo.

    A classe 'Jogo' gerencia a execução do jogo, permitindo que o jogador inicie uma nova partida,
    carregue uma partida salva, veja o ranking e saia do jogo. A classe mantém o controle das partidas 
    salvas e interage com o sistema de pontuação e salvamento.
    """
    arquivos_gravados =[]

    def __init__(self):
        """
        Inicializa a classe Jogo.

        O construtor inicializa o objeto 'partida' como 'None', já que a partida será iniciada
        através das opções do menu.
        """
        self.partida = None

    def menu(self):
        """
        Exibe o menu principal do jogo e gerencia as opções do jogador.

        O método apresenta as opções de início de partida, carregamento de partidas salvas, exibição de
        ranking e saída do jogo. O jogador pode escolher uma dessas opções, e o método chamará os métodos
        correspondentes para cada ação.

        As opções disponíveis são:
        - Iniciar nova partida
        - Carregar uma partida salva
        - Exibir ranking
        - Sair do jogo
        """

        print("*** Jogo Textris - um tetris em modo texto ***")
        while True:
            print("Opções do jogo:")
            print("- <i> Iniciar uma nova partida")
            print("- <c> Carregar uma partida gravada e continuá-la")
            print("- <p> Ver as 10 melhores pontuações")
            print("- <s> Sair do jogo")
            opçao = input("Digite a opção desejada: ").strip().lower()

            if opçao == "i":
                self.iniciar_partida()
            elif opçao == "c":
                self.carregar_partida()
            elif opçao == "p":
                self.exibir_rankings()
            elif opçao == "s":
                self.sair_jogo()
                break
            else:
                print("Opção inválida!")
    
    def iniciar_partida(self):
        """
        Inicia uma nova partida.

        Este método solicita ao jogador o seu nome e as dimensões da tela (número de linhas e colunas),
        e cria um novo objeto 'Partida'. Após a criação da partida, o método inicia a execução do jogo.

        """

        nome_jogador = input("Digite o nome do jogador: ")
        num_linhas = input("Digite o número de linhas da tela do jogo: ")
        num_colunas = input("Digite o número de colunas da tela do jogo: ")
        self.partida = Partida(nome_jogador, num_linhas, num_colunas)
        self.partida.jogar()
    
    def carregar_partida(self):
        """
        Carrega uma partida salva anteriormente.

        Este método verifica se há arquivos de partida salvos registrados no atributo 'arquivos_gravados'.
        Caso existam, exibe os nomes das partidas disponíveis e solicita ao jogador que escolha uma para carregar.
        A partida selecionada será carregada e executada.

        @note Se o arquivo escolhido não existir no diretório, uma mensagem será exibida e o carregamento será cancelado.
        """

        if not self.arquivos_gravados:
            print("\nNão há partidas salvas.\n")
            return
        else:
            print("\nPartidas salvas:\n")
            for item in self.arquivos_gravados:
                print(item)

            nome_arquivo = input("\nDigite o nome da partida que deseja retomar:\n")

            if os.path.exists(nome_arquivo):
                with open(nome_arquivo, "rb") as f:
                    self.partida = pickle.load(f)
                self.partida.jogar()
            else:
                print("\nEssa partida não existe.\n")

    def exibir_rankings(self):
        """
        Exibe os rankings do jogo.

        O método utiliza a classe 'Ranking' para exibir as melhores pontuações já alcançadas,
        acompanhadas pelos nomes dos respectivos jogadores.
        """

        ranking = Ranking()  
        ranking.exibir_rankings()

    def sair_jogo(self):
        """
        Exclui todos os arquivos de partidas salvos no diretório atual.

        O método remove todos os arquivos registrados no atributo 'arquivos_gravados',
        garantindo que os dados de partidas anteriores sejam excluídos do sistema.
        """
        
        for arq in self.arquivos_gravados:
            os.remove(arq)