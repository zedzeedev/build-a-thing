from grid import Grid, add_pos
from maze.helpers import MazeCell, POSSIBLE_DIRECTIONS, negate_direction, Maze
from random import choice


class HuntAndKillGrid(Grid, Maze):
    def __init__(self, rows: int, columns: int):
        super().__init__(rows, columns, MazeCell())
        self.visited_cells = []
        self.current_cell = self.get_random_cell_pos()
        self.hunted_row = -1
        self.completed_rows = []
        self.completed = False
    
    def step(self):
        if self.current_cell not in self.visited_cells:
            self.visited_cells.append(self.current_cell)
        directions = self.get_unvisited_directions()
        if len(directions) == 0:
            for y in range(self.columns):
                if y in self.completed_rows:
                    continue
                completed_tiles = 0
                for x in range(self.rows):
                    self.hunted_row = y
                    pos = (x, y)

                    if pos not in self.visited_cells:
                        visited_directions = self.get_visited_directions(pos)
                        if len(visited_directions) == 0:
                            continue
                        self.current_cell = pos
                        dir = choice(visited_directions)
                        self[self.current_cell].destroy_wall(dir)
                        self[add_pos(self.current_cell, dir)].destroy_wall(negate_direction(dir))
                        return True
                    else:
                        completed_tiles += 1
                if completed_tiles == self.rows:
                    self.completed_rows.append(y)
            self.hunted_row = -1
            self.completed = True
            return False
        dir = choice(directions)
        self[self.current_cell].destroy_wall(dir)
        self.current_cell = add_pos(self.current_cell, dir)
        self[self.current_cell].destroy_wall(negate_direction(dir))
        return True

    def get_unvisited_directions(self):
        unvisited_directions = []
        for dir in POSSIBLE_DIRECTIONS:
            with_cell = add_pos(dir, self.current_cell)
            if with_cell in self.grid and with_cell not in self.visited_cells and with_cell:
                unvisited_directions.append(dir)
        return unvisited_directions
    
    def get_visited_directions(self, pos):
        visited_driections = []
        for dir in POSSIBLE_DIRECTIONS:
            with_cell = add_pos(dir, pos)
            if with_cell in self.grid and with_cell in self.visited_cells:
                visited_driections.append(dir)
        return visited_driections

    def accept(self, visitor):
        visitor.visit_hunt_and_kill(self)