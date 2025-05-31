# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 142:
# 109974 Mariana Carvalho
# 110390 Gustavo Cerqueira

from search import (
    Problem, 
    Node
)

# Dicionário global com formas possíveis
positions = {
    "I1":((0, 0), (1, 0), (2, 0), (3, 0)),
    "I2":((0, 0), (0, 1), (0, 2), (0, 3)),

    "T1":((0, 0), (1, -1), (1, 0), (2, 0)),
    "T2":((0, 0), (1, 0), (1, 1), (2, 0)),
    "T3":((0, 0), (1,-1), (1, 0), (1, 1)),
    "T4":((0, 0), (0, 1), (0, 2), (1, 1)),

    "S1":((0, 0), (0, 1), (1, -1), (1, 0)),
    "S2":((0, 0), (0, 1), (1, 1), (1, 2)),
    "S3":((0, 0), (1, -1), (1, 0), (2, -1)), 
    "S4":((0, 0), (1, 0), (1, 1), (2, 1)),

    "L1":((0, 0), (1, -2), (1, -1), (1, 0)),
    "L2":((0, 0), (1, 0), (1, 1), (1, 2)),
    "L3":((0, 0), (1, 0), (2, 0), (2, 1)),
    "L4":((0, 0), (1, 0), (2, 0), (2, -1)),
    "L5":((0, 0), (0, 1), (0, 2), (1, 0)),
    "L6":((0, 0), (0, 1), (1, 1), (2, 1)),
    "L7":((0, 0), (0, 1), (0, 2), (1, 2)),
    "L8":((0, 0), (0, 1), (1, 0), (2, 0))
}

cant_be_position = {
    "T1":((0, -1), (2, -1)),
    "T2":((0, 1), (2, 1)),
    "T3":((0, -1), (0, 1)),
    "T4":((1, 0), (1, 2)),

    "S1":((0, -1), (1, 1)),
    "S2":((0, 2), (1, 0)),
    "S3":((0, -1), (2, 0)),
    "S4":((0, 1), (2, 0)),

    "L1":((0, -1),),
    "L2":((0, 1),),
    "L3":((1, 1),),
    "L4":((1, -1),),
    "L5":((1, 1),),
    "L6":((1, 0),),
    "L7":((1, 1),),
    "L8":((1, 1),)
}

class NuruominoState:
    state_id = 0

    #guarda o tabuleiro (APAGAR COMENTÁRIO)
    def __init__(self, board):
        self.board = board
        self.id = NuruominoState.state_id
        NuruominoState.state_id += 1

    def __lt__(self, other):
        """ Este método é utilizado em caso de empate na gestão da lista
        de abertos nas procuras informadas. """
        return self.id < other.id


class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""

    #define o tabuleiro 
    def __init__(self, grid):
        self.grid = grid
        self.length_matrix = len(grid)

    #mapeia tabuleiro
    def find_regions(self):
        #[0][0] nr de regiões, [0][regiao] nr de posicoes da regiao, [regiao][] posições na região
        global list_regions
        list_regions = [[0]]

        for row in range(self.length_matrix):
            for col in range(self.length_matrix):

                val = self.grid[row][col]
                #atualiza o número de regiões, quantidade de posições na região e adiciona a posição à região
                while len(list_regions) <= val:
                    list_regions.append([])
                    list_regions[0].append(0)
                    list_regions[0][0] += 1

                list_regions[0][val] += 1
                list_regions[val].append((row, col))
        # print(self.list_regions) debugging
                    
        return
    


    def adjacent_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""

        #TODO função retorna regiões na diagonal que não fazem realmente fronteira

        #Criar uma lista vazia que não aceita duplicados
        adjacents = set()

        #Percorrer as posições da região
        for pos in list_regions[region]:
            row, col = pos[0], pos[1]

            #percorrer as posições adjacentes que eu calcular, não queremos as diagonais
            for adj in self.cross_positions(row, col): 

                r, c = adj[0], adj[1]

                val = self.grid[r][c]

                #comparar se a adjacente é diferente do inteiro
                if val != region:
                    adjacents.add(val)

        return list(adjacents)
    
    def adjacent_positions(self, row:int, col:int) -> list:
        """Devolve as posições adjacentes à posição, em todas as direções, incluindo diagonais."""
        
        #Lista vazia onde vou colocar os adjacentes da posição recebida
        positions = []
        #estes deslocamentos vão obter as 8 adjacentes (4 diagonais e 4 em cruz/diretas whatever)
        for dr in [-1, 0, 1]: #delta row
            for dc in [-1, 0, 1]: #delta column
                if dr == 0 and dc == 0: #posição original
                    continue
                r, c = row + dr, col + dc #calculo a "nova posição" a analisar com base no desvio criado nos fors
                
                #testar os limites da matriz
                if 0 <= r < self.length_matrix and 0 <= c < self.length_matrix:
                    positions.append((r, c))
                
        return positions
    
    def cross_positions(self, row:int, col:int) -> list:
        """Devolve as posições adjacentes à posição, em todas as direções, não inclui diagonais."""
        
        #Lista vazia onde vou colocar os adjacentes da posição recebida
        positions = []

        #Testa as Adjacentes
        if row > 0:
            positions.append((row-1, col))
        if col > 0:
            positions.append((row, col-1))
        if row < self.length_matrix-1:
            positions.append((row+1, col))
        if col < self.length_matrix-1:
            positions.append((row, col+1))        
                
        return positions

    def adjacent_values(self, row:int, col:int) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, incluindo diagonais."""
        #TODO
        #percorre todas as posições da grid (row, col) e devolve os pares (r,c)
        #para cada (r,c) (posição dum vizinho, faz o self.grid[r][c] nessa posição)
        return [self.grid[pos[0]][pos[1]] for pos in self.adjacent_positions(row, col)]
    
    def cross_values(self, row:int, col:int) -> list:
        """Devolve os valores das celulas adjacentes à região, em todas as direções, não inclui diagonais."""
        #TODO
        #percorre todas as posições da grid (row, col) e devolve os pares (r,c)
        #para cada (r,c) (posição dum vizinho, faz o self.grid[r][c] nessa posição)
        return [self.grid[pos[0]][pos[1]] for pos in self.cross_positions(row, col)]
    
    def regions_with_four(self):
        """Por enquanto vou marcar com I as regiões que têm 4 coordenadas/células"""
        
        # Fazer uma cópia da grid para não alterar a original e dar isto como output
        new_board = [[str(cell) for cell in row] for row in self.grid]  
        
        # percorrer a grid e verificar se tem 4 vizinhos
        # vou de numero em numero até na primeira linha da nossa tabela
        for region_number in range (1, list_regions[0][0]+1): 
            region_cells = list_regions[region_number]
            print("AAAAAAAAAHHHHH   " + str(region_cells))

            #se essa região tem exatamente 4 coordenadas/células, marco com I
            #if (len(region_cells) == 4):
                #for (row, col) in region_cells:
                    #new_board[row][col] = "I"

            if (list_regions[0][region_number] == 4):
                shape = self.find_shape(region_cells)
                for (row, col) in region_cells:
                    new_board[row][col] = shape

        # Print do novo tabuleiro  
        for row in new_board:
            print("\t".join(row))

    @staticmethod
    def find_shape(region_cells):
        """Devolve a letra da forma (I, L, S, T) correspondente à região."""

        region_set = set(region_cells)
        a, b = region_cells[0]  # Célula base da região

        for shape_name, offsets in positions.items():
            test_coords = [(a + dx, b + dy) for dx, dy in offsets]
            if set(test_coords) == region_set:
                return shape_name[0]  # Retorna só 'I', 'L', 'S' ou 'T'


    
    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 pipe.py < test-01.txt
            > from sys import stdin
            > line = stdin.readline().split()
        """
        #O nosso parse_instance funciona admitindo que é tudo inteiros, são matrizes quadradas e que não há caracteres inválidos
        from sys import stdin

        grid = []

        for line in stdin:
            #ignorar linhas vazias
            if line.strip():  
                row = list(map(int, line.strip().split()))
                grid.append(row)

                # como sabemos que os tabuleiros são quadrados, quando o numero de linhas for igual 
                # ao numero de elementos duma linha podemos logo contruir o Board sem ter de dar ctrl+D
                # APAGAR DEPOIS PORQUE ACHO QUE NÃO SERÁ NECESSÁRIO E QUE O PROGRAMA CONTINUARÁ
                if len(grid) == len(row):
                    break

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





#
#    if __name__ == "__main__":
#        board = Board.parse_instance()
#        board.find_regions()
#        
#        for i in range(len(list_regions)):
#            if i == 0:
#                continue
#            print(f"Região {i}: {list_regions[i]}")
#            print(f"Fronteiras da região {i}: {board.adjacent_regions(i)}")
