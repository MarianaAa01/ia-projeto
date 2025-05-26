from pprint import pprint

# Matriz de valores (tudo None, pois ainda não forneceste os valores)
grid = [
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None],
    [None, None, None, None, None, None]
]

# Matriz de regiões (a que forneceste)
regions = [
    [1, 1, 2, 2, 3, 3],
    [1, 2, 2, 2, 3, 3],
    [1, 3, 3, 2, 3, 5],
    [3, 3, 3, 3, 3, 5],
    [4, 4, 4, 3, 3, 5],
    [4, 3, 3, 3, 3, 5]
]

# Classe Board (igual à anterior)
class Board:
    def __init__(self, grid: list[list[int]], regions: list[list[int]]):
        self.grid = grid
        self.regions = regions
        self.rows = len(grid)
        self.cols = len(grid[0])

    def get_value(self, row: int, col: int):
        return self.grid[row][col]

    def adjacent_positions(self, row: int, col: int):
        directions = [(-1, -1), (-1, 0), (-1, 1),
                      (0, -1),           (0, 1),
                      (1, -1),  (1, 0),  (1, 1)]
        adj = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                adj.append((nr, nc))
        return adj

    def adjacent_values(self, row: int, col: int):
        adj = self.adjacent_positions(row, col)
        return [self.grid[r][c] for r, c in adj]

    def adjacent_regions(self, region: int):
        found = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if self.regions[r][c] == region:
                    for nr, nc in self.adjacent_positions(r, c):
                        reg = self.regions[nr][nc]
                        if reg != region:
                            found.add(reg)
        return sorted(found)

    def print_instance(self):
        print("Grid:")
        pprint(self.grid)
        print("Regions:")
        pprint(self.regions)

# Criar o tabuleiro
board = Board(grid, regions)

# Testes
print("=== Testes com tua matriz de regiões ===")

board.print_instance()

print("\nRegiões adjacentes à região 3:")
print(board.adjacent_regions(3))  # Deve devolver regiões como 1, 2, 4, 5, etc.

print("\nPosições adjacentes a (0, 0):")
print(board.adjacent_positions(0, 0))  # Deve devolver posições dentro da grelha

print("\nValores adjacentes a (0, 0):")
print(board.adjacent_values(0, 0))  # Tudo None neste caso, pois grid está vazia
