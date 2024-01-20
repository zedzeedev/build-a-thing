import pygame as pg
from recursive_backtracking import RecursiveBacktrackerGrid


CELL_SIZE = (30, 30)


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


def draw_grid(screen, grid, cell_color, wall_color):
    for y in range(grid.columns):
        for x in range(grid.rows):
            pos = (x, y)
            cell = grid[pos]
            cell_pos = (x * CELL_SIZE[0], y * CELL_SIZE[1])
            draw_cell(screen, cell, cell_pos, cell_color, wall_color)


screen = pg.display.set_mode((900, 900))
running = True
grid = RecursiveBacktrackerGrid(30, 30)


while running:
    screen.fill((255, 255, 255))

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    draw_grid(screen, grid, (255, 255, 255), (0, 0, 0))
    grid.step()
    pg.display.flip()

pg.quit()