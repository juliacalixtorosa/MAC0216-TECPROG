# EP3 - TEXTRIS 🕹️🧩👾

## AUTORES: 

- Júlia Calixto Rosa
- Thainara de Assis Goulart 

## DESCRIÇÃO:

Textris é uma versão simplificada do clássico jogo **Tetris**, desenvolvida para ser jogada no terminal e na **forma de texto**. O jogo exibe um tabuleiro de Tetris em formato de matriz no terminal, e o jogador pode controlar as peças utilizando as teclas do teclado.

Suas funcionalidades incluem:
- Iniciar uma nova partida.
- Gravar partidas.
- Carregar partidas gravadas.
- Exibir rankings das 10 melhores pontuações.
- Encerrar partidas e jogos.

A implementação do projeto segue os princípios da programação orientada a objetos e está devidamente documentada e testada.

## COMO EXECUTAR:

### **Passo a Passo**
- Utilizamos um ambiente virtual para executar o programa. Para isso, siga os passos abaixo:

    1. Criar um Ambiente Virtual:

        ```bash
        python3.12 -m venv venv
        ```

    2. Ativar o Ambiente Virtual:

        ```bash
        source venv/bin/activate
        ```

    3. Instalar os Pacotes Necessários:

        ```bash
        pip install readchar
        ```
        ```bash
        pip install pytest
        ```

    4. Executar o Programa:

        ```bash
        python src/main.py
        ```

    5. Para desativar o Ambiente Virtual:

        ```bash
        deactivate
        ```

### Gerando a Documentação
- Para gerar a documentação, siga os passos abaixo:

    1. Certifique-se de que o Doxygen está instalado: 
        ```bash
        sudo apt install doxygen
        ```
    2. Certifique-se de que o Graphviz está instalado:
        ```bash
        sudo apt install graphviz
        ```

    3. Geração da documentação:
        ```bash
        make doc
        ```

    4. Acesse a documentação gerada no navegador:
        ```bash
        xdg-open docs/html/index.html
        ```


## TESTES:

Foram realizados testes unitários utilizando a ferramenta pytest para garantir o funcionamento correto das principais funcionalidades do sistema. 

Os testes estão localizados na pasta `test/`, e cada arquivo de teste corresponde a um conjunto de verificações para os principais métodos e componentes que são essenciais para o funcionamento do jogo.

### Executando os Testes
- Para executar os testes, rode o comando:

    ```bash
    make tests
    ```

## DEPENDÊNCIAS:

- **Sistema Operacional**: Ubuntu 24.04 LTS
- **Python**: 3.12.3

    Você pode verificar a versão do python com:

    ```bash
    python3.12 --version
    ```

- **Pacotes**:

    ```bash
    pip install readchar
    ```
    ```bash
    pip install pytest
    ```
- **Dependências do Sistema**:

    ```bash
    sudo apt install doxygen
    ```

    ```bash
    sudo apt install graphviz
    ```

