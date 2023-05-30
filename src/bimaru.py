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
        self.count = [0 for _ in range(4)]
        
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
    
    def boat_pos_values(self, x: int, y: int, size: int, ver: bool):
        values = []
        if ver:
            values += [(x, b) for b in range(y, y+size) if 0<=b<10]
        else:
            values += [(a, y) for a in range(x, x+size) if 0<=a<10]

        if len(values) == size:
            return values
        else:
            raise ValueError("WRONG: impossible to put boat here")

    def clear_surronding(self, x: int, y: int):
        values = self.diagonal_values(x, y)
        tile = self.get_value(x, y).lower()
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

    
    def add_boat(self, x: int, y: int, size: int, ver: bool):
        boat = BOATS_VER[size-1] if ver else BOATS_HOR[size-1]
        i = 0
        pos = self.boat_pos_values(x, y, size, ver)
        for p in pos:
            if not self.is_empty(x, y):
                raise ValueError("WRONG: already filled")
            self.set_value(p[0], p[1], boat[i])
            i += 1

    @staticmethod
    def parse_instance():
        """Lê o test do standard input (stdin) e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 bimaru.py < input_T01

            > from sys import stdin
            > line = stdin.readline().split()
        """
        # TODO
        row = np.array(list(map(int, sys.stdin.readline().split()[1:])))
        col = np.array(list(map(int, sys.stdin.readline().split()[1:])))
        print(f"{col}\n{row}\n\n")

        boats = np.empty((10, 10), str)

        board = Board(row, col, boats)
        
        for _ in range(int(sys.stdin.readline())):
            line = sys.stdin.readline().split()[1:]
            y = int(line[0])
            x = int(line[1])
            board.set_value(x, y, line[2])
       
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
        pass

    def actions(self, state: BimaruState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: BimaruState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: BimaruState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas de acordo com as regras do problema."""
        # TODO
        pass

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
    #problem = Bimaru(board)

    #depth_first_tree_search(problem)

    pass
