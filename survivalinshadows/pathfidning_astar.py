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
    start_AStar = AStar(None, start)
    end_AStar = AStar(None, end)
    open_list = []  
    heappush(open_list, start_AStar)
    open_set = {start}

    closed_list = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]
    closed_list[start[1]][start[0]] = True

    AStars_visited = 0
    while open_list:
        AStars_visited += 1
        if AStars_visited == 1200:
            return
        current_AStar = heappop(open_list)
        open_set.remove(current_AStar.position)

        if current_AStar == end_AStar:
            path = []
            current = current_AStar
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            AStar_position = (current_AStar.position[0] + new_position[0], current_AStar.position[1] + new_position[1])

            if not(0 <= AStar_position[1] < len(maze)) or not(0 <= AStar_position[0] < len(maze[0])):
                continue

            if maze[AStar_position[1]][AStar_position[0]] == "0":
                continue

            if closed_list[AStar_position[1]][AStar_position[0]]:
                continue

            closed_list[AStar_position[1]][AStar_position[0]] = True
            new_AStar = AStar(current_AStar, AStar_position)
            new_AStar.g = current_AStar.g + 1
            new_AStar.h = abs(AStar_position[0] - end_AStar.position[0]) + abs(AStar_position[1] - end_AStar.position[1])
            new_AStar.f = new_AStar.g + new_AStar.h

            if new_AStar.position in open_set:
                continue

            heappush(open_list, new_AStar)
            open_set.add(new_AStar.position)

    print(f"No path found after visiting {AStars_visited} AStars")
    return None