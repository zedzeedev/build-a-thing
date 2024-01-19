from random import randint


def get_random_dir():
    x = randint(-1, 1)
    y = 0 if x != 0 else [-1, 1][randint(0, 1)]
    return (x, y)


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