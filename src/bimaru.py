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
    def __init__(self, row, col, boats):
        self.row = row
        self.col = col
        self.boats = boats
        self.count = [i for i in range(4, 0, -1)]
        
    def get_value(self, x: int, y: int) -> str:
        return self.boats[y][x]
    
    def set_value(self, x: int, y: int, type: str):
        self.boats[y][x] = type
        if type not in (".", "W"):
            self.row[y] -= 1
            self.col[x] -= 1

    def is_empty(self, x: int, y: int):
        return self.get_value(x, y) == ""

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
    
    #TODO: tornar estas duas funções numa só
    # also make it o that something like L l m m r cannot happen
    # also check if row or col becomes negative if boat is added
    def boat_pos_values(self, x: int, y: int, size: int, ver: bool):
        values = []
        if ver:
            values += [(x, b) for b in range(y, y+size) if 0<=b<10]
        else:
            values += [(a, y) for a in range(x, x+size) if 0<=a<10]

        if len(values) == size:
            return values
        else:
            return []
        
    def valid_boat_pos(self, x: int, y: int, size: int, ver: bool):
        pos = self.boat_pos_values(x, y, size, ver)
        if not pos:
            return []
        boat = BOATS_VER[size-1] if ver else BOATS_HOR[size-1]
        i = 0
        for p in pos:
            val = self.get_value(p[0], p[1])
            if (val not in ("", ".", "W") and val.casefold() != boat[i].casefold()) or val in (".", "W"):
                return []
            i += 1

        print(f"valid pos: {pos}")
        return pos
        
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

    def clear_surronding(self, x: int, y: int):
        tile = self.get_value(x, y).lower()
        if tile in (".", "w"):
            return
        values = self.diagonal_values(x, y)
        if tile == "c":
            values += self.adjacent_horizontal_values(x, y)
            values += self.adjacent_vertical_values(x, y)
        elif tile == "t":
            values += self.adjacent_horizontal_values(x, y)
            #TODO add top-top tile
        elif tile == "b":
            values += self.adjacent_horizontal_values(x, y)
            #TODO
        elif tile == "l":
            values += self.adjacent_vertical_values(x, y)
            #TODO
        elif tile == "r":
            values += self.adjacent_vertical_values(x, y)
            #TODO
        for pos in values:
            if self.is_empty(pos[0], pos[1]):
                self.set_value(pos[0], pos[1], ".")

    
    def add_boat(self, pos: list, ver: bool):
        size = len(pos)
        boat = BOATS_VER[size-1] if ver else BOATS_HOR[size-1]
        i = 0
        for p in pos:
            if self.is_empty(p[0], p[1]):
                self.set_value(p[0], p[1], boat[i])
                board.clear_surronding(p[0], p[1])
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
        print(f"{col}\n{row}\n\n")

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
        for num in self.col:
            string += f"{num}"
        print(string)
        for line in self.boats:
            string = f"{self.row[i]}"
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
        actions = []
        for size in range(4, -1, -1):
            if board.count[size-1] != 0:
                for i in range(10):
                    for j in range(10-size):
                        pos = board.valid_boat_pos(i, j, size, VER)
                        if pos:
                            actions += [(pos, VER)]
                for i in range(10-size):
                    for j in range(10):
                        pos = board.valid_boat_pos(i, j, size, HOR)
                        if pos:
                            actions += [(pos, HOR)]
            break
        return actions

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        new = Board(state.board.row.copy(), state.board.col.copy(), state.board.boats.copy())
        new.add_boat(action[0], action[1])
        new.print()
        return BimaruState(new)

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        for row in state.board.boats:
            for char in row:
                if char == "":
                    return False
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
    board.print()
    problem = Bimaru(board)

    depth_first_tree_search(problem)

    pass
