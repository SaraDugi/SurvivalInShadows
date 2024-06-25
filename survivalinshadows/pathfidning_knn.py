from collections import deque

def get_neighbors(matrix, pos):
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    neighbors = []
    
    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy

        if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
            neighbors.append((x, y))
    
    return neighbors

def knn_pathfinding(matrix, start, goal, k=3):
    visited = set()
    queue = deque([(start, [start])])
    
    while queue:
        vertex, path = queue.popleft()
        
        if vertex == goal:
            return path
        
        if vertex not in visited:
            for neighbor in get_neighbors(matrix, vertex):
                if neighbor not in visited:
                    queue.append((neighbor, path + [neighbor])) 
                
            visited.add(vertex)
    
    return None
