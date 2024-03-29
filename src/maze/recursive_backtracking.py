from grid import Grid, add_pos
from maze.helpers import MazeCell, POSSIBLE_DIRECTIONS, negate_direction, Maze
from random import choice


class RecursiveBacktrackerGrid(Grid, Maze):
    # [True, True, True, True]
    # This corrosponds to all walls being activea
    # [0] -> Left, [1] -> Right, [2] -> Up, [3] -> Down


    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns, MazeCell())
        self.visited_cells = []
        self.completed_cells = []
        self.current_cell = self.get_random_cell_pos()
        self.completed = False
    
    def step(self):
        if len(self.completed_cells) == len(self.grid):
            self.completed = True
            return False
        
        if self.current_cell not in self.visited_cells:
            self.visited_cells.append(self.current_cell)
        unvisited_directions = self.get_unvisited_directions()
        if len(unvisited_directions) == 0:
            self.completed_cells.append(self.current_cell)
            self.visited_cells = self.visited_cells[:-1]
            if len(self.visited_cells) > 0:
                self.current_cell = self.visited_cells[-1]
            return True
        dir = choice(unvisited_directions)
        self[self.current_cell].destroy_wall(dir)
        self.current_cell = add_pos(self.current_cell, dir)
        self[self.current_cell].destroy_wall(negate_direction(dir))
        return True

    def get_unvisited_directions(self):
        unvisited_directions = []
        for dir in POSSIBLE_DIRECTIONS:
            with_cell = add_pos(dir, self.current_cell)
            if with_cell in self.grid and with_cell not in self.visited_cells and with_cell not in self.completed_cells:
                unvisited_directions.append(dir)
        return unvisited_directions


    def accept(self, visitor):
        visitor.visit_recursive_backtracking(self)
