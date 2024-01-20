from grid import Grid, add_pos
from maze_helpers import MazeCell, POSSIBLE_DIRECTIONS, get_random_dir, negate_direction
from random import choice


class RecursiveBacktrackerGrid(Grid):
    # [True, True, True, True]
    # This corrosponds to all walls being active
    # [0] -> Left, [1] -> Right, [2] -> Up, [3] -> Down


    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns, MazeCell())
        self.visited_cells = []
        self.completed_cells = []
        self.current_cell = self.get_random_cell_pos()
    
    def step(self):
        if len(self.completed_cells) == len(self.grid):
            return False
        
        if self.current_cell not in self.visited_cells:
            self.visited_cells.append(self.current_cell)
        unvisited_directions = self.get_unvisited_directions()
        if len(unvisited_directions) == 0:
            self.completed_cells.append(self.current_cell)
            self.visited_cells = self.visited_cells[:-2]
            if len(self.visited_cells) > 0:
                self.current_cell = self.visited_cells[-1]
            return True
        dir = choice(unvisited_directions)
        self.grid[self.current_cell].destroy_wall(dir)
        self.current_cell = add_pos(self.current_cell, dir)
        self.grid[self.current_cell].destroy_wall(negate_direction(dir))
        return True

    def get_unvisited_directions(self):
        unvisited_directions = []
        for dir in POSSIBLE_DIRECTIONS:
            with_cell = add_pos(dir, self.current_cell)
            if with_cell in self.grid and with_cell not in self.visited_cells and with_cell not in self.completed_cells:
                unvisited_directions.append(dir)
        return unvisited_directions


g = RecursiveBacktrackerGrid(3, 3)

i = 0
while g.step():
    i += 1
print(g)