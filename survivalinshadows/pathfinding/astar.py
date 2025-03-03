from heapq import heappop, heappush

class Cell:
    def __init__(self, parent=None, g = -1.0, h = -1.0, f = -1.0):
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f

def distance(pos, dest):
    return ((pos[0] - dest[0]) ** 2 + (pos[1] - dest[1]) ** 2) ** 0.5

def astar_pathfinding(maze, start, end, max_steps):
    open_list = []
    heappush(open_list, (0.0, start))
    closed_list = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    cell_details = [[Cell() for _ in range(len(maze[0]))] for _ in range(len(maze))]
    cell_details[start[1]][start[0]].f = 0.0
    cell_details[start[1]][start[0]].g = 0.0
    cell_details[start[1]][start[0]].h = 0.0

    AStars_visited = 0
    while open_list:
        if AStars_visited == max_steps:  
            print(f"Visited {AStars_visited} AStars, open list size is {len(open_list)}")
            return

        AStars_visited += 1
        current = heappop(open_list)[1]
        closed_list[current[1]][current[0]] = True

        if current[0] == end[0] and current[1] == end[1]:
            path = []
            while current is not None:
                path.append(current)
                current = cell_details[current[1]][current[0]].parent
            return path[::-1]
        
        for direction in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            next_position = (current[0] + direction[0], current[1] + direction[1])
            
            if not(0 <= next_position[1] < len(maze)) or not(0 <= next_position[0] < len(maze[0])) or \
                closed_list[next_position[1]][next_position[0]] or \
                maze[next_position[1]][next_position[0]] == "0":
                continue

            new_g = cell_details[current[1]][current[0]].g + 1.0
            new_h = distance(next_position, end)
            new_f = new_g + new_h
            if cell_details[next_position[1]][next_position[0]].f == -1 or cell_details[next_position[1]][next_position[0]].f > new_f:
                heappush(open_list, (new_f, next_position))
                cell_details[next_position[1]][next_position[0]].f = new_f
                cell_details[next_position[1]][next_position[0]].g = new_g
                cell_details[next_position[1]][next_position[0]].h = new_h
                cell_details[next_position[1]][next_position[0]].parent = current

    print(f"No path found after visiting {AStars_visited} AStars")
    return None