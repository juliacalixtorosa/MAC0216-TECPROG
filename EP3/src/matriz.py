class Matriz:
    """
    Classe que contém métodos estáticos para manipulação de matrizes.

    Esta classe cria matrizes vazias e copia uma matriz existente.
    """

    @staticmethod
    def devolve_matriz_vazia(num_linhas,num_colunas):
        """
        Cria e retorna uma matriz vazia com o número especificado de linhas e colunas.

        Cada célula da matriz é inicializada com o valor `" "`.

        @param num_linhas: Número de linhas da matriz.
        @param num_colunas: Número de colunas da matriz.

        @return: Uma matriz de tamanho `num_linhas` por `num_colunas`, preenchida com espaços vazios.
        """

        matriz_inicial = []  

        for _ in range(num_linhas):  
            linha = []  
            for _ in range(num_colunas):  
                linha.append(" ")  
            matriz_inicial.append(linha)  

        return matriz_inicial
    
    @staticmethod
    def copia_matriz(matriz_ref):
        """
        Cria uma cópia de uma matriz existente.

        Este método copia todos os elementos de `matriz_ref` para uma nova matriz, preservando seus valores.

        @param matriz_ref: A matriz a ser copiada.

        @return: Uma nova matriz contendo os mesmos elementos de `matriz_ref`.
        """
        matriz_copia = []  

        for i in range(len(matriz_ref)):  
            linha = []  
            for j in range(len(matriz_ref[0])):  
                linha.append(matriz_ref[i][j])  

            matriz_copia.append(linha)  

        return matriz_copia