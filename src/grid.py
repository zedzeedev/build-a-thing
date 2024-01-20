from random import choice
from copy import deepcopy


def add_pos(a, b):
    return (a[0] + b[0], a[1] + b[1])


class Grid:
    def __init__(self, rows: int, columns: int, default=None):
        self.rows = rows
        self.columns = columns
        self.grid = {}

        for y in range(self.columns):
            for x in range(self.rows):
                self[(x, y)] = deepcopy(default)
    
    def __getitem__(self, pos):
        return self.grid[pos]

    def __setitem__(self, pos, value) -> None:
        self.grid[pos] = value
    
    def has_cell(self, pos):
        return pos[0] <= 0 and pos[1] <= 0 and pos[0] < self.rows and\
            pos[1] < self.columns

    def get_random_cell_pos(self):
        return choice(list(self.grid.keys()))
    
    def __str__(self) -> str:
        s = ""
        for y in range(self.columns):
            for x in range(self.rows):
                s += str(self[(x, y)])
            s += "\n"
        return s
