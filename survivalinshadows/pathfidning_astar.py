from heapq import heappop, heappush
from settings import *
import math

class AStar:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

    def __eq__(self, other):
        return self.position == other.position

def astar_pathfinding(maze, start, end):
    start_node = AStar(None, start)
    end_node = AStar(None, end)
    open_list = []
    heappush(open_list, start_node)
    open_set = {start}

    closed_list = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]

    while open_list:
        current_node = heappop(open_list)
        open_set.remove(current_node.position)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        closed_list[current_node.position[0]][current_node.position[1]] = True

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            x, y = current_node.position
            nx, ny = x + dx, y + dy

            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny]!= -1 and not closed_list[nx][ny]:
                neighbor = AStar(current_node, (nx, ny))
                neighbor.g = current_node.g + 1
                neighbor.h = abs(nx - end_node.position[0]) + abs(ny - end_node.position[1])
                neighbor.f = neighbor.g + neighbor.h

                if neighbor.position not in open_set:
                    heappush(open_list, neighbor)
                    open_set.add(neighbor.position)

    return None