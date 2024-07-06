from collections import deque

def bfs_pathfinding(grid_map, start, end, max_steps):
    start = (start[1], start[0])
    end = (end[1], end[0])
    rows, cols = len(grid_map), len(grid_map[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque([(start, [])]) 
    visited[start[0]][start[1]] = True
    nodes_visited = 0
    while queue:
        if nodes_visited == max_steps:
            print(f"Visited {nodes_visited} nodes")
            return 

        nodes_visited += 1
        (x, y), path = queue.popleft()
        if (x, y) == end: 
            return path + [(y, x)]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols and grid_map[nx][ny] != "0" and not visited[nx][ny]:  
                queue.append(((nx, ny), path + [(y, x)]))
                visited[nx][ny] = True
    
    print(f"No path found after visiting {nodes_visited} nodes")
    return None