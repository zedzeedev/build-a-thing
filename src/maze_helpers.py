from random import randint, choice


POSSIBLE_DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, 1)]


def get_random_dir():
    choice(POSSIBLE_DIRECTIONS)


class MazeGrid:
    def __init__(self, grid) -> None:
        self.grid = grid
        self.paths = {}
        
        for y in range(self.grid.columns):
            for x in range(self.grid.rows):
                if (x + 1) % 2 == 0 and (y + 1) % 2 == 0:
                    self[(int(x / 2), int(y / 2))] = (x, y)

    def __getitem__(self, pos):
        return self.paths[pos]

    def __setitem__(self, pos, value):
        self.paths[pos] = value
    
    def __str__(self) -> str:
        return str(self.grid)

    def get_neighboring_wall_pos(self, pos, dir):
        grid_pos = self[pos]
        return ((grid_pos[0] + dir[0]), (grid_pos[1] + dir[1]))
    
    def get_neighboring_cell_pos(self, pos, dir):
        return ((pos[0] + dir[0]), (pos[1] + dir[1]))
    
    def get_random_path(self):
        return choice(self.paths.keys())
