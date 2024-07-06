from collections import deque

def bfs(maze, queue, visited):
    m, n = len(maze), len(maze[0])
    x, y = queue.popleft()
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < m and 0 <= ny < n and maze[nx][ny] != "0" and (nx, ny) not in visited:  
            queue.append((nx, ny))
            visited[(nx, ny)] = ((x, y), visited[(x, y)][1] + [(y, x)])

def is_intersecting(s_visited, e_visited):
    for node in s_visited:
        if node in e_visited:
            return node
    
    return None

def create_path(s_visited, e_visited, intersect_node):
    path1 = s_visited[intersect_node][1] + [(intersect_node[1], intersect_node[0])]
    path2 = e_visited[intersect_node][1]
    path1.extend(path2[len(path2)-1::-1])
    return path1

def bidirectional_pathfinding(maze, start, end, max_steps):
    start = (start[1], start[0])
    end = (end[1], end[0])
    m, n = len(maze), len(maze[0])
    s_visited = {start: (None, [])}
    e_visited = {end: (None, [])}
    
    s_queue = deque()
    s_queue.append(start)

    e_queue = deque()
    e_queue.append(end)

    nodes_visited = 0
    while s_queue and e_queue:
        if nodes_visited == max_steps:
            print(f"Visited {nodes_visited} nodes")
            return 

        nodes_visited += 1
        bfs(maze, s_queue, s_visited)
        bfs(maze, e_queue, e_visited)
        intersect_node = is_intersecting(s_visited, e_visited)
        if intersect_node != None:
            print(create_path(s_visited, e_visited, intersect_node))
            return create_path(s_visited, e_visited, intersect_node)

    print(f"No path found after visiting {nodes_visited} nodes")
    return None