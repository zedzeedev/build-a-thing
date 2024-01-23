from random import choice


POSSIBLE_DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]
DIRECTION_MAP = {
    (-1, 0): 0,
    (1, 0): 1,
    (0, -1): 2,
    (0, 1): 3
}


def negate_direction(dir):
    return (-dir[0], -dir[1])


def get_random_dir():
    choice(POSSIBLE_DIRECTIONS)


class MazeCell:
    def __init__(self) -> None:
        self.walls = [True, True, True, True]

    def destroy_wall(self, dir):
        self.walls[DIRECTION_MAP[dir]] = False
    
    def __str__(self) -> str:
        return str(self.walls)


class MazeVisitor:
    def visit_aldous_broder(self, maze):
        pass

    def visit_recursive_backtracking(self, maze):
        pass

    def visit_hunt_and_kill(self, maze):
        pass


class Maze:
    def accept(self, visitor):
        pass