import numpy as np
from collections import deque

def k_nearest_neighbors(matrika, pos, k):
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    neighbors = []
    
    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy

        if 0 <= x < len(matrika) and 0 <= y < len(matrika[0]):
            neighbors.append((x, y))
    
    return neighbors[:k]

def knn_pathfinding(matrika, start, goal, k=3):
    visited = set()
    queue = deque([(start, [start])])
    
    while queue:
        (vertex, path) = queue.popleft()
        
        if vertex == goal:
            return path
        
        if vertex not in visited:
            for neighbor in k_nearest_neighbors(matrika, vertex, k):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append((neighbor, new_path))
                
            visited.add(vertex)
    
    return None