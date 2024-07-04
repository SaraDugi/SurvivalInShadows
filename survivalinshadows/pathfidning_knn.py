from collections import deque

def get_neighbors(matrix, pos):
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    neighbors = []
    
    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy

        if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
            neighbors.append((x, y))
    
    return neighbors

def knn_pathfinding(matrix, start, end, max_steps, k=4):
    start = (start[1], start[0])
    end = (end[1], end[0])
    visited = set()
    queue = deque([(start, [(start[1], start[0])])])
    
    steps = 0
    while queue:
        if steps == max_steps:
            print(f"Visited {steps} nodes")
            return 

        steps += 1
        vertex, path = queue.popleft()
        if vertex == end:
            return path
        
        if vertex not in visited:
            for neighbor in get_neighbors(matrix, vertex):
                if neighbor not in visited:
                    queue.append((neighbor, path + [(neighbor[1], neighbor[0])])) 
                
            visited.add(vertex)
    
    return None
