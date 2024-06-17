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

def astar(maze, start, end):
    start_AStar = AStar(None, start)
    end_AStar = AStar(None, end)
    open_list = []  
    heappush(open_list, start_AStar)

    closed_list = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]

    AStars_visited = 0
    while open_list:
        AStars_visited += 1
        if AStars_visited % 1000 == 0:  
            print(f"Visited {AStars_visited} AStars, open list size is {len(open_list)}")
        if AStars_visited == 1200:
            return
        current_AStar = heappop(open_list)

        if current_AStar == end_AStar:
            path = []
            current = current_AStar
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
        closed_list[current_AStar.position[0]][current_AStar.position[1]] = True
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            AStar_position = (current_AStar.position[0] + new_position[0], current_AStar.position[1] + new_position[1])

            if not(0 <= AStar_position[0] < len(maze)) or not(0 <= AStar_position[1] < len(maze[0])):
                continue

            if maze[AStar_position[0]][AStar_position[1]] == -1:
                continue

            if closed_list[AStar_position[0]][AStar_position[1]]:
                continue

            new_AStar = AStar(current_AStar, AStar_position)
            new_AStar.g = current_AStar.g + 1
            new_AStar.h = abs(AStar_position[0] - end_AStar.position[0]) + abs(AStar_position[1] - end_AStar.position[1])
            new_AStar.f = new_AStar.g + new_AStar.h

            for open_AStar in open_list:
                if new_AStar == open_AStar and new_AStar.g > open_AStar.g:
                    continue
            if maze[new_AStar.position[0]][new_AStar.position[1]] == -1:
                continue
            heappush(open_list, new_AStar)

    print(f"No path found after visiting {AStars_visited} AStars")