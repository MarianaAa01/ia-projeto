# nuruomino.py: Template para implementação do projeto de Inteligência Artificial 2024/2025.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes sugeridas, podem acrescentar outras que considerem pertinentes.

# Grupo 142:
# 109974 Mariana Carvalho
# 110390 Gustavo Cerqueira

from search import (
    Problem, 
    Node,
    depth_first_tree_search,
)

from constants import *







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
    
    def get_board(self) -> 'Board':
        return self.board


class Board:
    """Representação interna de um tabuleiro do Puzzle Nuruomino."""
    
    #define o tabuleiro 
    def __init__(self, grid):
        self.impossible = False
        self.grid = grid
        self.length_matrix = len(grid)

        self.list_regions = [[0]] # [0][0] = número de regiões, [0][regiao] = número de posições da regiao, [regiao] = tuplo com posições na região
        self.list_nr_free = [[0]] # Semelhante ao List_regions mas vamos alterar para ficar com o estado atual do board (só vai conter as livres)
        self.list_pieces = [] # tuplos com (<número_da_região_da_peça>, <tipo_de_peça>, <lista_de_posições_ocupadas>) tipo de peça é (L1, L2, L3, etc...)
        self.list_X = [] # tuplos com posições X (pode haver posições repetidas) (<coordenada>, <nº_da_região>)

        #self.regions_with_four()

    def copy(self):
        #Deep copy do Board
        
        new_grid = [row[:] for row in self.grid]  # Copia profunda da grid

        new_board = Board(new_grid)

        new_board.impossible = self.impossible
        new_board.length_matrix = self.length_matrix

        new_board.list_regions = [r[:] for r in self.list_regions]
        new_board.list_nr_free = [r[:] for r in self.list_nr_free]
        new_board.list_pieces = [tuple(p) for p in self.list_pieces]
        new_board.list_X = [tuple(x) for x in self.list_X]

        return new_board

    def find_regions(self):
        for row in range(self.length_matrix):
            for col in range(self.length_matrix):

                val = self.grid[row][col]

                #atualiza o número de regiões, quantidade de posições na região e adiciona a posição à região
                while len(self.list_regions) <= val:
                    #adiciona lista para registar posições da região
                    self.list_regions.append([])
                    self.list_nr_free.append([])

                    #adiciona contador do número de posições por região 
                    self.list_regions[0].append(0)
                    self.list_nr_free[0].append(0)

                    #aumenta o número de regiões
                    self.list_regions[0][0] += 1
                    self.list_nr_free[0][0] += 1

                #aumenta o nr de posições na região
                self.list_regions[0][val] += 1
                self.list_nr_free[0][val] += 1

                #adiciona a posição na lista da região
                self.list_regions[val].append((row, col))
                self.list_nr_free[val].append((row, col))
                    
        return
    


    def adjacent_regions(self, region:int) -> list:
        """Devolve uma lista das regiões que fazem fronteira com a região enviada no argumento."""

        #TODO função retorna regiões na diagonal que não fazem realmente fronteira

        #Criar uma lista vazia que não aceita duplicados
        adjacents = set()

        #Percorrer as posições da região
        for pos in self.list_regions[region]:
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
        #Percorre um loop que coloca as peças nas regiões com 4 posições livres
        
        # Fazer uma cópia da grid para não alterar a original e dar isto como output
        #new_board = [[str(cell) for cell in row] for row in self.grid]  
  
        #se essa região tem exatamente 4 coordenadas/células

        #TODO mudar list_regions para list_nr_free
        
        #AQUI
        #print(self.list_nr_free)
        region = 1
        loop = 0
        # AQUI
        #print(self.list_nr_free[0])
        #print(self.list_nr_free[0][region])
        while(loop != 1 or region != self.list_regions[0][0]+1):
            if (region == self.list_regions[0][0]+1): #chega aqui quando loop = 0
                loop = 1
                region = 1 #repõe região inical

            if(self.list_nr_free[0][region] == 4 ):
                region_cells = self.list_nr_free[region]
                loop = 0 #modificou portanto o loop foi util
                shape = self.find_shape(region_cells) # I1, I2, L1, L2, etc...
                self.insert_shape(self, region, shape, region_cells)

            region += 1
        
        #print("AAAAAAAAAAAAAAAAAAAAH\n")
        """for row in self.grid:
            print("\t".join(
                f"{COLORS.get(cell, '')}{cell}{COLORS['END']}" if cell in COLORS else str(cell)
                for cell in row
            ))
        print("\n")"""

        # AQUI
        #first = self.list_pieces[0]
        #print("Primeira peça: " + str(first) + "\n\n")


        # AQUI
        # Chama a função para imprimir o tabuleiro
        #self.print_board_colors()



    
    @staticmethod
    def insert_shape(self, region_number: int, shape: str, region_cells: list):
        """Insere a peça na região correspondente quando a região tem apenas 4 coordenadas."""
        # quando o shape vem igual a None isto dá erro
        shape_letter = shape[0] # L, I, T ou S

        # Marca as células da região com a letra da forma
        for (row, col) in region_cells:
            self.grid[row][col] = shape_letter
                    
        # Adiciona a peça à lista
        self.list_pieces.append((region_number, shape, region_cells))
                    
        # Remove posições da list_nr_free
        self.list_nr_free[0][0] -= 1
        self.list_nr_free[0][region_number] -= 4

        # Marca as posições inválidas com 'X'
        invalids = self.mark_invalid_positions(shape, region_cells)
        if invalids:
            for r, c in invalids:
                reg = self.grid[r][c]
                # Evita sobrescrever letras já marcadas (vamos fazer isto e adicionar a coordenada do X na lista das regioes invalidas)
                if isinstance(reg, int) and self.list_nr_free[0][reg] > 0:
                    self.grid[r][c] = "X"
                    self.list_nr_free[0][reg] -= 1

                    # Remover a coordenada (r, c) da lista das posições livres da região
                    if (r, c) in self.list_nr_free[reg]:
                        self.list_nr_free[reg].remove((r, c))
                
         
                # Adiciona a coordenada a lista de X
                self.list_X.append(((r, c), reg))


    @staticmethod
    def find_shape(region_cells):
        """Devolve a letra da forma (I, L, S, T) correspondente à região."""

        region_set = set(region_cells)
        (a, b) = region_cells[0]  # Coordenada principal da region_cells (da regiao onde está a peça)

        for shape, offsets in positions.items():
            test_coords = [(a+x, b+y) for (x, y) in offsets]
            if set(test_coords) == region_set:
                return shape  # Retorna o tipo de shape tipo 'I1'

    
    def mark_invalid_positions(self, shape, region_cells):
        """Devolve uma lista de posições (r, c) inválidas para colocar novas formas."""

        invalid_positions = []

        if shape not in cant_be_position:
            return []

        base_row, base_col = region_cells[0]

        for (x, y) in cant_be_position[shape]:
            (r, c) = (base_row+x, base_col+y)
            invalid_positions.append((r, c))

        return invalid_positions

    ##############################################################################################################################################################################
    # POSSIBLE_ACTIONS COMEÇA AQUI

    
    def possible_actions(self) -> list:
        actions = []

        # 1. Encontrar a região menor com mais de 4 coordenadas livres
        smaller_region = 1
        min_free = float('inf')
        #print("livres: " + str(self.list_nr_free[0][7]))
        for region in range(1, self.list_regions[0][0] + 1):
            nr_free = len(self.list_nr_free[region])  # número de células livres da região
            
            if nr_free > 4 and nr_free < min_free and nr_free>0:
        
                smaller_region = region
                min_free = nr_free
        
        #print("Smaller_region: " + str(smaller_region))
            

        if smaller_region is None:
            return actions  # não há regiões válidas

        region_cells = self.list_nr_free[smaller_region]  # células livres da região

        # 2. Para cada célula livre, tentar colocar cada forma
        for start_cell in region_cells:
            for shape in positions.keys():
                bool = False
                # Verificar se a forma cabe na região
                if self.shape_fits_in_region(shape, start_cell, region_cells):
                    shape_letter = shape[0]  # L, I, T, S etc.
                    shape_coords = [(start_cell[0] + dx, start_cell[1] + dy) for dx, dy in positions[shape]]

                    
                    if not (self.find_square(shape_coords) or self.impossible_neighbor(shape_coords, shape_letter)):
                        actions.append((smaller_region, shape, start_cell))
        
            #print("Actions: " + str(actions))

        return actions
                 

    def is_isolated_region(self, region: int) -> bool:
        """Verifica se a região está completamente rodeada por peças e nenhuma toca na sua fronteira."""
        for neighbor in self.cross_regions(region):
            if self.list_nr_free[0][neighbor] > 0:
                return False  # há regiões adjacentes ainda livres

            # verifica se alguma das células da peça toca esta região
            for (r, c) in self.list_pieces[neighbor - 1][2]:  # pega posições da peça vizinha
                for adj in self.cross_positions(r, c):
                    if adj in self.list_nr_free[region]:
                        return False  # há contacto com a região A
        return True
    
    def impossible_neighbor(self, shape_coords, shape_letter: str) -> bool:
        ''' Confirma que a peça é adjacente a uma região diferente e se tem peças iguais como adjacentes Retorna True se for impossivel'''
        count = 0
        region = self.grid[shape_coords[0][0]][shape_coords[0][1]]

        for (r,c) in shape_coords:
            for (adj_r, adj_c) in self.cross_positions(r, c):
                adj = self.grid[adj_r][adj_c]

                if adj == shape_letter:
                    return True
                if adj != region and adj != 'X':
                    count += 1

        return count == 0



    def shape_fits_in_region(self, shape, start_cell, region_cells):
        ''' Confiram se a peça numa posição e orientação cabe na região'''
        offsets = positions[shape]
        for dx, dy in offsets:
            cell = (start_cell[0] + dx, start_cell[1] + dy)
            if cell not in region_cells:
                return False
        return True


    def find_square(self, list_pos):
        ''' Procura quadrados colados a peça
        retorna True se encontrar quadrado 2x2'''

        for pos_r, pos_c in list_pos:

            if pos_r != 0:
                if pos_c != 0:
                    count = 0
                    for dr, dc in [(-1,-1),(-1,0),(0,-1)]:
                        if (pos_r + dr, pos_c + dc) in list_pos or self.grid[pos_r + dr][pos_c + dc] in ('L','I','T','S'):
                            count += 1
                    if count == 3: return True

                if pos_c != self.length_matrix-1:
                    count = 0
                    for dr, dc in [(-1, 1),(-1,0),(0, 1)]:
                        if (pos_r + dr, pos_c + dc) in list_pos or self.grid[pos_r + dr][pos_c + dc] in ('L','I','T','S'):
                            count += 1
                    if count == 3: return True

            if pos_r != self.length_matrix-1:
                if pos_c != 0:
                    count = 0
                    for dr, dc in [( 1,-1),( 1,0),(0,-1)]:
                        if (pos_r + dr, pos_c + dc) in list_pos or self.grid[pos_r + dr][pos_c + dc] in ('L','I','T','S'):
                            count += 1
                    if count == 3: return True

                if pos_c != self.length_matrix-1:
                    count = 0
                    for dr, dc in [( 1, 1),( 1,0),(0, 1)]:
                        if (pos_r + dr, pos_c + dc) in list_pos or self.grid[pos_r + dr][pos_c + dc] in ('L','I','T','S'):
                            count += 1
                    if count == 3: return True
        return False
   

    def apply_action(self, action):
        """Aplica a próxima action (especificada no result) no board"""
        #(<nª_região>, <tipo_de_peça>, <coordenada_inicial>)
        (region, shape, first_coord) = action
        shape_letter = shape[0] 

        
        # retirar coordenadas que começam em first_coord do tipo de peça de list_nr_free[region]
        # Obter as coordenadas da peça com base na posição inicial e offsets da shape
        shape_coords = [(first_coord[0] + dx, first_coord[1] + dy) for dx, dy in positions[shape]]

        # Colocar as peças no sítiooo
        for (r, c) in shape_coords:
            self.grid[r][c] = shape_letter

        # Atualizar list_pieces
        self.list_pieces.append((region, shape, shape_coords))

        #print(self.list_nr_free[0][0])
        # numero de coordenadas livres
        #self.list_nr_free[0][region] -= 4
        #self.list_nr_free[0][0] -= 1
        #print(self.list_nr_free[0][0])
        #print("\n")

        #Remover posições da list_nr_free da região
        for coord in shape_coords:
            if coord in self.list_nr_free[region]:
                self.list_nr_free[region].remove(coord)
            
        # Marcar posições inválidas com "X"
        invalids = self.mark_invalid_positions(shape, shape_coords)
        for (r, c) in invalids:
            if (0 <= r < self.length_matrix and 0 <= c < self.length_matrix):
                reg = self.grid[r][c]
                if isinstance(reg, int) and (r, c) in self.list_nr_free[reg]:
                    self.grid[r][c] = 'X'
                    self.list_nr_free[0][reg] -= 1
                    self.list_nr_free[reg].remove((r, c))
                    self.list_X.append(((r, c), reg))
        
        # MARCAR O RESTO DA REGIÃO COMO 'X' 
        # REVER
        """for coord in self.list_nr_free[region][:]:  # cópia para iterar
            r, c = coord
            self.grid[r][c] = 'X'
            self.list_X.append(coord)
            self.list_nr_free[0][region] -= 1
            self.list_nr_free[region].remove(coord)"""
        
        # Em vez de colocar 'X' em todas as coordenadas da região, colocamos apenas o nº de coordenadas da região a zero
        self.list_nr_free[0][region] = 0
        self.list_nr_free[region] = []

        # ver se a peça fez um quadrado e se fizer coloco como impossible
        if self.find_square(shape_coords):
            self.impossible = True

        



    """def copy(self):
        grid2 = [[str(cell) for cell in row] for row in self.grid] 
        new_board = Board(grid2)
        new_board.list_regions = self.list_regions
        new_board.list_nr_free = self.list_nr_free
        new_board.list_pieces = self.list_pieces
        new_board.list_X = self.list_X
        new_board.impossible = self.impossible
        return new_board"""

    def connected(self):
        """Função Verifica se todas as posições estão conectadas
        contador de posições a 0
        procurar peças adjacentes e adicona a pilha se não tiverem sido visitadas
        peças já visitadas marca com 0, adiciona ao contador e retira da pilha
        quando acabar tudo, se o contador for igual ao nr_regioes x 4 ent esta certo
        """
        
        count = 0
        stack = []
        stack.append(self.list_pieces[0][2][0]) #list_pieces contem a primeira peça e queremos uma posição
        visited = set()

        while stack:
            pos = stack.pop() #TODO corrigir para remover primeiro elemento da stack
            
            if pos not in visited: #confiram que pos não foi visitada ainda

                visited.add(pos) #marca como visitada
                count += 1

                for adj in self.cross_positions(pos[0], pos[1]):
                    if self.grid[adj[0]][adj[1]] in ('L','I','T','S'):
                        stack.append(adj) #adiciona ao final da stack
            

        
        return count == self.list_regions[0][0] * 4

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

        # AQUI
        #print(grid)

        return Board(grid)  
        
    # usado pra debugging
    def print_board_color(self):
        for position in self.list_X:
            #print(self.list_X)
            (coord, region) = position
            #print(position)
            self.grid[coord[0]][coord[1]] = region

        for row in self.grid:
            print("\t".join(
                f"{COLORS.get(cell, '')}{cell}{COLORS['END']}" if cell in COLORS else str(cell)
                for cell in row
            ))
            
    def print_board(self):
        for position in self.list_X:
            (coord, region) = position
            self.grid[coord[0]][coord[1]] = region

        for row in self.grid:
            print("\t".join(str(cell) for cell in row))
        

    # TODO: outros metodos da classe Board


class Nuruomino(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        super().__init__(NuruominoState(board))


    def actions(self, state: NuruominoState) -> list:
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board = state.get_board()
        if board.impossible:
            return []
        #actions = board.possible_actions()
        return board.possible_actions()


    def result(self, state: NuruominoState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        #cópia do board ("cria" um estado)
        #print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA " + str(action[0]))
        board_copy = state.board.copy() 
        board_copy.apply_action(action)
        region = action[0]
        board_copy.list_nr_free[0][region] = 0
        board_copy.list_nr_free[0][0] -= 1
        #print("A merda que to a fazer: " + str(board_copy.list_nr_free[0][0]))
        child_state = NuruominoState(board_copy)
        
        #child_state.get_board().print_board_colors() 
        #print("\n\n")
        
        return child_state
    

    def goal_test(self, state: NuruominoState):
        #Retorna True se e só se o estado passado como argumento é
        #um estado objetivo. Deve verificar se todas as posições do tabuleiro
        #estão preenchidas de acordo com as regras do problema.
        #TODO
        board = state.get_board()
        if board.impossible:
            return False
        

        # Confirma se todas as regiões têm uma peça
        #          se nº de regiões = nº de peças
        # Verifica se está tudo conectado no final

        
        #confirma que todas as regiões têm uma peça
        if any(i != 0 for i in board.list_nr_free[0]):
            return False

        #número de peças igual ao número de regiões 
        #TODO se confirmar que é realmente preciso, acredito q n mas prefiro ter a certeza q é feito
        if len(board.list_pieces) != board.list_regions[0][0]:
            return False

        return board.connected()
    
    """def goal_test(self, state: NuruominoState):
        board = state.get_board()

        if board.impossible:
            print("[goal_test] Estado impossível detectado.")
            return False

        # Verifica se todas as regiões têm 0 posições livres
        if any(i != 0 for i in board.list_nr_free[0]):
            #print("[goal_test] Regiões ainda têm posições livres:", board.list_nr_free[0])
            return False

        # Verifica se número de peças é igual ao número de regiões
        if len(board.list_pieces) != board.list_regions[0][0]:
            print(f"[goal_test] Número de peças ({len(board.list_pieces)}) diferente do número de regiões ({board.list_regions[0][0]})")
            return False

        connected = board.connected()
        if not connected:
            print("[goal_test] Tabuleiro não está ligado.")
        else:
            print("[goal_test] Estado objetivo! :p")

        return connected"""



    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # Não foi necessário
        """
        Valorizar numero de peças possíveis
        ou
        nr de posições e desvalorizar quadrados 2x2 livres (permitem várias peças serem postas nos msm quadrado)
        """
        pass




if __name__ == "__main__":
    board = Board.parse_instance()
    board.find_regions()
    board.regions_with_four()
    #for row in board.grid:
    #    print(" ".join(str(cell).rjust(2) for cell in row))
    problem = Nuruomino(board)
    goal_node = depth_first_tree_search(problem)  # ou outra busca mais adequada
    if goal_node is not None:
        goal_node.state.get_board().print_board()
    '''else:
        print("Nenhuma solução encontrada.")'''

    
