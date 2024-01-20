from random import randint, choice
from maze_helpers import MazeGrid, get_random_dir, POSSIBLE_DIRECTIONS
from grid import TextGrid


class RecursiveBacktrackingGrid(MazeGrid):
    def __init__(self, grid) -> None:
        super().__init__(grid)
        self.checked_cells = []
        self.current_cell = self.get_random_path()
    
    def step(self):
        if self.checked_cells == len(self.paths):
            return True
        
        directions = self.get_unchecked_directions()
        if len(directions) == 0:
            self.current_cell = self.checked_cells[-2]
            return False
        dir = choice(directions)
        wall = self.get_neighboring_wall_pos(self.current_cell, dir)
        self.destroy_wall(wall)
        self.current_cell = self.get_neighboring_cell_pos(self.current_cell, dir)
        return False

    def get_unchecked_directions(self):
        unchecked_directions = []
        for dir in POSSIBLE_DIRECTIONS:
            cell = self.get_neighboring_cell_pos(self.current_cell, dir)
            if not cell in self.checked_cells:
                unchecked_directions.append(dir)
        return unchecked_directions

    def destroy_wall(self, wall_pos):
        self.grid[wall_pos] = " "


g = TextGrid(101, 201, "#")
maze = RecursiveBacktrackingGrid(g)
while not maze.step():
    continue
print(maze)
