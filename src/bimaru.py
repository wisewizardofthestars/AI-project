# bimaru.py: Template para implementação do projeto de Inteligência Artificial 2022/2023.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

import sys
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import numpy as np

VER = True
HOR = False

BOATS_VER = [
    ["c"],
    ["t", "b"],
    ["t", "m", "b"],
    ["t", "m", "m", "b"]
]
BOATS_HOR = [
    ["c"],
    ["l", "r"],
    ["l", "m", "r"],
    ["l", "m", "m", "r"]
]

class BimaruState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = BimaruState.state_id
        BimaruState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Bimaru."""
    def __init__(self, row, col, boats, count=[4, 3, 2, 1]):
        self.row = row
        self.col = col
        self.boats = boats
        self.count = count
        
    def get_value(self, x: int, y: int) -> str:
        return self.boats[y][x]
    
    def set_value(self, x: int, y: int, type: str):
        self.boats[y][x] = type
        if type not in (".", "W"):
            self.row[y] -= 1
            self.col[x] -= 1

    def is_empty(self, x: int, y: int):
        return self.get_value(x, y) == ""
    
    def is_water(self, x: int, y: int):
        return self.get_value(x, y) in (".", "W")

    def adjacent_vertical_values(self, x: int, y: int):
        """Devolve os valores imediatamente acima e abaixo,
        respectivamente."""
        return list(filter(lambda p: 0<=p[0]<10 and 0<=p[1]<10, [
            (x, y+1),
            (x, y-1),
        ]))

    def adjacent_horizontal_values(self, x: int, y: int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return list(filter(lambda p: 0<=p[0]<10 and 0<=p[1]<10, [
            (x+1, y),
            (x-1, y),
        ]))

    def diagonal_values(self, x: int, y: int):
        return list(filter(lambda p: 0<=p[0]<10 and 0<=p[1]<10, [
            (x+1, y+1),
            (x+1, y-1),
            (x-1, y+1),
            (x-1, y-1)
        ]))
    
    def clear_lines(self):
        for i in range(10):
            if self.row[i] == 0:
                for j in range(10):
                    if self.is_empty(j, i):
                        self.set_value(j, i, ".")
            if self.row[i] < 0:
                print("Invalid board:")
                self.print()
                raise Exception("Invalid board")
        for i in range(10):
            if self.col[i] == 0:
                for j in range(10):
                    if self.is_empty(i, j):
                        self.set_value(i, j, ".")
            if self.col[i] < 0:
                self.print()
                raise Exception("Invalid board")

    def boat_position(self, x: int, y: int, size: int, ver: bool):
        if ver:
            values = [(x, b) for b in range(y, y+size) if 0<=b<10]
        else:
            values = [(a, y) for a in range(x, x+size) if 0<=a<10]

        if len(values) != size:
            return []
        return values
    
    def valid_boat(self, pos: list, ver: bool):
        if not pos:
            return False
        size = len(pos)
        boat = BOATS_VER[size-1] if ver else BOATS_HOR[size-1]
        i = 0
        new_tiles = 0

        for p in pos:
            val = self.get_value(p[0], p[1])
            if self.is_empty(p[0], p[1]):
                new_tiles += 1
            elif val != boat[i].upper(): #TODO: mistake here
                return False
            elif self.is_water(p[0], p[1]):
                return False

            sur = self.get_surronding(p[0], p[1], boat[i])
            for s in sur:
                if not self.is_empty(s[0], s[1]) and not self.is_water(s[0], s[1]):
                    return False
                
            i += 1
        
        if ver:
            if self.col[pos[0][0]] < new_tiles:
                return False
        else:
            if self.row[pos[0][1]] < new_tiles:
                return False
            
        return True
            

    def get_surronding(self, x: int, y: int, tile: str=""):
        if tile == "":
            tile = self.get_value(x, y).lower()
            if self.is_water(x, y):
                return []

        values = self.diagonal_values(x, y)
        if tile == "c":
            values += self.adjacent_horizontal_values(x, y)
            values += self.adjacent_vertical_values(x, y)
        elif tile == "t":
            values += self.adjacent_horizontal_values(x, y)
            if y-1 >= 0:
                values += [(x, y-1)]
        elif tile == "b":
            values += self.adjacent_horizontal_values(x, y)
            if y+1 < 10:
                values += [(x, y+1)]
        elif tile == "l":
            values += self.adjacent_vertical_values(x, y)
            if x-1 >= 0:
                values += [(x-1, y)]
        elif tile == "r":
            values += self.adjacent_vertical_values(x, y)
            if x+1 < 10:
                values += [(x+1, y)]

        return values
    
    def clear_surronding(self, x: int, y: int):
        values = self.get_surronding(x, y)
        for pos in values:
            if self.is_empty(pos[0], pos[1]):
                self.set_value(pos[0], pos[1], ".")
        
    def add_boat(self, pos: list, size: int, ver: bool):
        boat = BOATS_VER[size-1] if ver else BOATS_HOR[size-1]
        i = 0
        for p in pos:
            if self.is_empty(p[0], p[1]):
                self.set_value(p[0], p[1], boat[i])
            self.clear_surronding(p[0], p[1])
            i += 1
        self.clear_lines()
        #TODO: clear lines só das lines q sofreram alterações
        self.count[size-1] -= 1

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        row = list(map(int, sys.stdin.readline().split()[1:]))
        col = list(map(int, sys.stdin.readline().split()[1:]))
        #print(f"{col}\n{row}\n\n")

        boats = np.empty((10, 10), str)

        board = Board(row, col, boats)
        
        for _ in range(int(sys.stdin.readline())):
            line = sys.stdin.readline().split()[1:]
            y = int(line[0])
            x = int(line[1])
            board.set_value(x, y, line[2])
            board.clear_surronding(x, y)

        board.clear_lines()
        return board

    # TODO: outros metodos da classe
    def print(self):
        #TODO: this version of print is only for debug purposes
        i = 0
        string = " "
        # for num in self.col:
        #     string += f"{num}"
        #print(string)
        for line in self.boats:
            #string = f"{self.row[i]}"
            string = ""
            for char in line:
                string += char
                if char == "":
                    string += "-"
            print(string)
            i += 1


class Bimaru(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        # TODO
        self.board = board
        self.initial = BimaruState(board)

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        board: Board = state.board
        #board.print()
        actions = []
        for size in range(4, -1, -1):
            if board.count[size-1] != 0:
                for i in range(10):
                    for j in range(10-size+1):
                        pos = board.boat_position(i, j, size, VER)
                        if board.valid_boat(pos, VER):
                            actions += [(pos, size, VER)]
                for j in range(10):
                    for i in range(10-size+1):
                        pos = board.boat_position(i, j, size, HOR)
                        if board.valid_boat(pos, HOR):
                            actions += [(pos, size, HOR)]
                break
        #print("actions: ", actions)
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new = Board(state.board.row.copy(), state.board.col.copy(), state.board.boats.copy(), state.board.count.copy())
        new.add_boat(action[0], action[1], action[2])
        #print("\naction taken:", action)
        #new.print()
        #print(new.count)
        #print()
        return BimaruState(new)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        for num in state.board.row:
            if num != 0:
                return False
        for num in state.board.col:
            if num != 0:
                return False
        for num in state.board.count:
            if num != 0:
                return False
        state.board.print()
        return True

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    board = Board.parse_instance()
    #board.print()
    problem = Bimaru(board)

    depth_first_tree_search(problem)

    pass
