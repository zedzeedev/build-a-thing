from grid import Grid, add_pos
from maze_helpers import MazeCell, POSSIBLE_DIRECTIONS, negate_direction, Maze
from random import choice


class AldousBroderGrid(Grid, Maze):
    def __init__(self, rows: int, columns: int, default=None):
        super().__init__(rows, columns, MazeCell())
        self.visited_cells = []
        self.current_cell = self.get_random_cell_pos()
    
    def step(self):
        if len(self.visited_cells) == len(self.grid):
            return False
        
        if self.current_cell not in self.visited_cells:
            self.visited_cells.append(self.current_cell)
        dir = choice(self.get_possible_dir())
        pos = add_pos(self.current_cell, dir)
        
        if pos not in self.visited_cells:
            self[self.current_cell].destroy_wall(dir)
            self[pos].destroy_wall(negate_direction(dir))
        
        self.current_cell = pos
        return True
    
    def get_possible_dir(self):
        directions = []
        for dir in POSSIBLE_DIRECTIONS:
            with_dir = add_pos(self.current_cell, dir)
            if with_dir in self.grid:
                directions.append(dir)
        return directions


    def accept(self, visitor):
        visitor.visit_aldous_broder(self)
