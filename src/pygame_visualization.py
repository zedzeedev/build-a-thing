import pygame as pg
from maze.recursive_backtracking import RecursiveBacktrackerGrid
from maze.aldous_broder import AldousBroderGrid
from maze.hunt_and_kill import HuntAndKillGrid
from maze.helpers import MazeVisitor
from pathfinding import find_path_astar
import time


CELL_SIZE = (12, 12)


def draw_cell(screen, cell, pos, cell_color, wall_color):
    pg.draw.rect(screen, cell_color, pg.Rect(pos[0], pos[1], CELL_SIZE[0], CELL_SIZE[1]))

    if cell.walls[0]:
        pg.draw.line(screen, wall_color, pos, (pos[0], pos[1] + CELL_SIZE[1]))
    if cell.walls[1]:
        pg.draw.line(screen, wall_color, (pos[0] + CELL_SIZE[0], pos[1]), (pos[0] + CELL_SIZE[0], pos[1] + CELL_SIZE[1]))
    if cell.walls[2]:
        pg.draw.line(screen, wall_color, pos, (pos[0] + CELL_SIZE[0], pos[1]))
    if cell.walls[3]:
        pg.draw.line(screen, wall_color, (pos[0], pos[1] + CELL_SIZE[1]), (pos[0] + CELL_SIZE[0], pos[1] + CELL_SIZE[1]))


class PygameGridVisitor(MazeVisitor):
    def __init__(self, screen, cell_color, wall_color, offset=(0, 0), **kwargs) -> None:
        super().__init__()
        self.screen = screen
        self.cell_color = cell_color
        self.wall_color = wall_color
        self.offset = offset
        self.kwargs = kwargs
        self.vars = {}

    def visit_aldous_broder(self, maze):
        if maze.completed and "path" not in self.vars:
            self.vars["path"] = self.kwargs["pathfinding"](maze, (0, 0), (maze.rows - 1, maze.columns - 1))
        def cell_color_decider(pos):
            if maze.completed and pos in self.vars["path"]:
                return self.kwargs["path_color"]
            elif pos in maze.visited_cells:
                return self.kwargs["visited_color"]
            elif pos == maze.current_cell:
                return self.kwargs["current_color"]
            return self.cell_color
        self.draw_grid(maze, cell_color_decider)
    
    def visit_hunt_and_kill(self, maze):
        if maze.completed and "path" not in self.vars:
            self.vars["path"] = self.kwargs["pathfinding"](maze, (0, 0), (maze.rows - 1, maze.columns - 1))
        def cell_color_decider(pos):
            if maze.completed and pos in self.vars["path"]:
                return self.kwargs["path_color"]
            elif pos[1] in maze.completed_rows:
                return self.kwargs["completed_color"]
            elif pos == maze.current_cell:
                return self.kwargs["current_color"]
            elif maze.hunted_row != -1 and maze.hunted_row == pos[1]:
                return self.kwargs["hunted_color"]
            elif pos in maze.visited_cells:
                return self.kwargs["visited_color"]
            return self.cell_color
        self.draw_grid(maze, cell_color_decider)

    def visit_recursive_backtracking(self, maze):
        if maze.completed and "path" not in self.vars:
            self.vars["path"] = self.kwargs["pathfinding"](maze, (0, 0), (maze.rows - 1, maze.columns - 1))
        def cell_color_decider(pos):
            if maze.completed and pos in self.vars["path"]:
                return self.kwargs["path_color"]
            elif pos in maze.completed_cells:
                return self.kwargs["completed_color"]
            elif pos == maze.current_cell:
                return self.kwargs["current_color"]
            elif pos in maze.visited_cells:
                return self.kwargs["visited_color"]
            return self.cell_color
        self.draw_grid(maze, cell_color_decider)
    

    def draw_grid(self, maze, cell_color_decider):
        for y in range(maze.columns):
            for x in range(maze.rows):
                pos = (x, y)
                cell = maze[pos]
                cell_pos = ((x * CELL_SIZE[0]) + self.offset[0], (y * CELL_SIZE[1]) + self.offset[1])
                color = cell_color_decider(pos)
                draw_cell(screen, cell, cell_pos, color, self.wall_color)


screen = pg.display.set_mode((1161, 361))
running = True


backtracker = RecursiveBacktrackerGrid(30, 30)
aldous = AldousBroderGrid(30, 30)
hunt_and_kill = HuntAndKillGrid(30, 30)

first_visitor = PygameGridVisitor(screen, (0, 0, 0), (255, 255, 255), current_color=(255, 255, 0), 
                       visited_color=(255, 0, 0), completed_color=(0, 255, 0),
                       pathfinding=find_path_astar, path_color=(255, 125, 0))
second_visitor = PygameGridVisitor(screen, (0, 0, 0), (255, 255, 255), (800, 0), current_color=(255, 255, 0), 
                        visited_color=(0, 0, 255), hunted_color=(255, 0, 0), 
                        completed_color=(0, 255, 0), pathfinding=find_path_astar,
                        path_color=(255, 125, 0))
third_visitor = PygameGridVisitor(screen, (0, 0, 0), (255, 255, 255), (400, 0), current_color=(255, 255, 0), 
                        visited_color=(0, 255, 0), pathfinding=find_path_astar,
                        path_color=(255, 125, 0))

start_time = time.time()


step_hunt_and_kill = True
step_aldous = True
step_backtracking = True

while running:
    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    if step_backtracking and not backtracker.step():
        print(f"Recursive backtracking took: {time.time() - start_time} seconds")
        step_backtracking = False
    
    if step_hunt_and_kill and not hunt_and_kill.step():
        print(f"Hunt and Kill took: {time.time() - start_time} seconds")
        step_hunt_and_kill = False
    
    if step_aldous and not aldous.step():
        print(f"Aldous-Broder took: {time.time() - start_time} seconds")
        step_aldous = False
    
    backtracker.accept(first_visitor)
    hunt_and_kill.accept(second_visitor)
    aldous.accept(third_visitor)
    
    pg.display.flip()
    


pg.quit()