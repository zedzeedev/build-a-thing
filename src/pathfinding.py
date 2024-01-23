from maze.helpers import POSSIBLE_DIRECTIONS, DIRECTION_MAP
from grid import add_pos


def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def dijkstra_heuristic(p1, p2):
    return 0


def find_path_astar(maze, start, end, heuristic=manhattan_distance):
    open_list = [start]
    closed_list = []
    
    came_from = {}

    g_costs = {}
    g_costs[start] = 0

    h_costs = {}
    h_costs[start] = heuristic(start, end)

    f_costs = {}
    f_costs[start] = h_costs[start]

    while len(open_list) != 0:
        current = open_list[0]
        lowest = f_costs[current]
        for cell in open_list:
            if cell in f_costs and f_costs[cell] < lowest:
                lowest = f_costs[cell]
                current = cell
        
        closed_list.append(current)

        if current == end:
            return reconstruct_path(came_from, current)

        open_list.remove(current)


        for neighbor in get_possible_neighbors(maze, current):
            if neighbor in closed_list:
                continue

            if neighbor not in open_list:
                open_list.append(neighbor)
                came_from[neighbor] = current
                g_costs[neighbor] = manhattan_distance(start, neighbor)
                h_costs[neighbor] = heuristic(neighbor, end)
                f_costs[neighbor] = g_costs[neighbor] + h_costs[neighbor]
            else:
                if g_costs[neighbor] < g_costs[current]:
                    came_from[neighbor] = current
                    g_costs[neighbor] = manhattan_distance(start, neighbor)
                    h_costs[neighbor] = heuristic(neighbor, end)
                    f_costs[neighbor] = g_costs[neighbor] + h_costs[neighbor]




def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)
    return path


def get_possible_neighbors(maze, pos):
    neighbors = []
    for dir in POSSIBLE_DIRECTIONS:
        with_dir = add_pos(pos, dir)
        if with_dir in maze.grid and not maze.grid[pos].walls[DIRECTION_MAP[dir]]:
            neighbors.append(with_dir)
    return neighbors