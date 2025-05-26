# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 142:
# 109974 Mariana Carvalho
# 110390 Gustavo Cerqueira

class NuruominoState:
    state_id = 0

    #guarda o tabuleiro (APAGAR COMENTÁRIO)
    def __init__(self, board):
        self.board = board
        self.id = Nuroumino.state_id
        Nuroumino.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""

    #define o tabuleiro 
    def __init__(self, grid):
        self.grid = grid

    def adjacent_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""
        #TODO
        #Criar uma lista vazia
        adjacents = set()
        #Percorrer a matriz dada
        #Quando encontrar o inteiro nessa matriz tenho de encontrar os seus adjacentes (fazer com o adjacent_values)
        tamanho=len(self.grid)
        for row in range(tamanho):
            for col in range(tamanho):
                #encontrei o inteiro nessa matriz
                if self.grid[row][col] == region:
                    #percorrer as posições adjacentes que eu calcular
                    for r, c in self.adjacent_positions(row, col):
                        #temporário
                        val = self.grid[r][c]
                        #comparar se a adjacente é diferente do inteiro
                        if val != region:
                            adjacents.add(val)
        return list(adjacents)
    
    def adjacent_positions(self, row:int, col:int) -> list:
        """Devolve as posições adjacentes à região, em todas as direções, incluindo diagonais."""
        #TODO
        #Lista vazia onde vou colocar os adjacentes da posição recebida (APAGAR COMENTÁRIO)
        positions = []
        #estes deslocamentos vão obter as 8 adjacentes (4 diagonais e 4 em cruz/diretas whatever)
        for dr in [-1, 0, 1]: #delta row
            for dc in [-1, 0, 1]: #delta column
                if dr == 0 and dc == 0: #não mudou nada
                    continue
                r, c = row + dr, col + dc #calculo a "nova posição" a analisar com base no desvio criado nos fors
                #testar os limites da matriz
                if 0 <= r < len(self.grid) and 0 <= c < len(self.grid[0]):
                    positions.append((r, c))
        return positions

    def adjacent_values(self, row:int, col:int) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""
        #TODO
        #percorre todas as posições da grid (row, col) e devolve os pares (r,c)
        #para cada (r,c) (posição dum vizinho, faz o self.grid[r][c] nessa posição)
        return [self.grid[r][c] for r, c in self.adjacent_positions(row, col)]
    
    
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt

            > from sys import stdin
            > line = stdin.readline().split()
        """
        from sys import stdin

        grid = []
        for line in stdin:
            #Ignora linhas vazias
            if line.strip() == "":
                continue
            #Converte a linha em inteiros
            row = list(map(int, line.strip().split()))
            grid.append(row)

        return Board(grid)   


    # TODO: outros metodos da classe Board

class Nuruomino(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        #TODO
        pass 

    def actions(self, state: NuruominoState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        #TODO
        pass 

    def result(self, state: NuruominoState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        #TODO
        pass 
        

    def goal_test(self, state: NuruominoState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        #TODO
        pass 

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass