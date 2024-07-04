from collections import deque
from settings import *
import sys

def bfs_pathfinding(grid_map, start, end, max_steps):
    start = (start[1], start[0])
    end = (end[1], end[0])
    rows, cols = len(grid_map), len(grid_map[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque([(start, [])]) 
    visited[start[0]][start[1]] = True
    steps = 0
    while queue:
        if steps == max_steps:
            print(f"Visited {steps} nodes")
            return 

        steps += 1
        (x, y), path = queue.popleft()
        if (x, y) == end: 
            return path + [(y, x)]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid_map[nx][ny] != "0" and not visited[nx][ny]:  
                queue.append(((nx, ny), path + [(ny, nx)]))
                visited[nx][ny] = True
    
    print("No path found")
    return None