import pygame as pg
from recursive_backtracking import RecursiveBacktrackerGrid
from aldous_broder import AldousBroderGrid
from hunt_and_kill import HuntAndKillGrid
from maze_helpers import MazeVisitor


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
    def __init__(self, screen, cell_color, wall_color, current_cell_color, offset=(0, 0)) -> None:
        super().__init__()
        self.screen = screen
        self.cell_color = cell_color
        self.wall_color = wall_color
        self.current_cell_color = current_cell_color
        self.offset = offset

    def visit_aldous_broder(self, maze):
        for y in range(maze.columns):
            for x in range(maze.rows):
                pos = (x, y)
                cell = maze[pos]
                cell_pos = ((x * CELL_SIZE[0]) + self.offset[0], (y * CELL_SIZE[1]) + self.offset[1])
                color = self.cell_color
                
                if pos == maze.current_cell:
                    color = self.current_cell_color

                draw_cell(screen, cell, cell_pos, color, self.wall_color)
    
    def visit_hunt_and_kill(self, maze):
        for y in range(maze.columns):
            for x in range(maze.rows):
                pos = (x, y)
                cell = maze[pos]
                cell_pos = ((x * CELL_SIZE[0]) + self.offset[0], (y * CELL_SIZE[1]) + self.offset[1])
                color = self.cell_color
                
                if pos == maze.current_cell:
                    color = self.current_cell_color
                if maze.hunted_row != -1 and pos[0] == maze.hunted_row:
                    color = (0, 0, 255)

                draw_cell(screen, cell, cell_pos, color, self.wall_color)

    def visit_recursive_backtracking(self, maze):
        for y in range(maze.columns):
            for x in range(maze.rows):
                pos = (x, y)
                cell = maze[pos]
                cell_pos = ((x * CELL_SIZE[0]) + self.offset[0], (y * CELL_SIZE[1]) + self.offset[1])
                color = self.cell_color
                
                if pos == maze.current_cell:
                    color = self.current_cell_color
                if pos in maze.visited_cells:
                    color = (0, 0, 255)
                if pos in maze.completed_cells:
                    color = (0, 255, 0)

                draw_cell(screen, cell, cell_pos, color, self.wall_color)


def draw_grid(screen, grid, cell_color, wall_color, current_cell_color, offset=(0, 0)):
    for y in range(grid.columns):
        for x in range(grid.rows):
            pos = (x, y)
            cell = grid[pos]
            cell_pos = ((x * CELL_SIZE[0]) + offset[0], (y * CELL_SIZE[1]) + offset[1])
            color = cell_color
            
            if pos == grid.current_cell:
                color = current_cell_color

            draw_cell(screen, cell, cell_pos, color, wall_color)


screen = pg.display.set_mode((1200, 400))
running = True

first_visitor = PygameGridVisitor(screen, (0, 0, 0), (255, 255, 255), (255, 255, 0))
second_visitor = PygameGridVisitor(screen, (0, 0, 0), (255, 255, 255), (255, 255, 0), (800, 0))
third_visitor = PygameGridVisitor(screen, (0, 0, 0), (255, 255, 255), (255, 255, 0), (400, 0))
backtracker = RecursiveBacktrackerGrid(30, 30)
aldous = AldousBroderGrid(30, 30)
hunt_and_kill = HuntAndKillGrid(30, 30)


while running:
    screen.fill((0, 0, 0))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    backtracker.accept(first_visitor)
    hunt_and_kill.accept(second_visitor)
    aldous.accept(third_visitor)
    backtracker.step()
    hunt_and_kill.step()
    aldous.step()
    pg.display.flip()


pg.quit()