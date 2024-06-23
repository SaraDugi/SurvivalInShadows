from collections import deque
from settings import *

def bfs_pathfinding(grid_map, start, goal):
    rows, cols = len(grid_map), len(grid_map[0])
    visited = [[False]*cols for _ in range(rows)]
    
    queue = deque([(start, [])])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)] 

    visited[start[0]][start[1]] = True

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == goal: 
            return path + [(x, y)]

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid_map[nx][ny]!= 0 and not visited[nx][ny]:  
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited[nx][ny] = True
    return None