import numpy as np
from settings import matrika

def k_nearest_neighbors(matrix, pos, k=3):
    directions = [(0, -1), (-1, 0), (1, 0), (0, 1)]
    distances = []
    
    for dx, dy in directions:
        x, y = pos[0] + dx, pos[1] + dy

        if 0 <= x < len(matrix) and 0 <= y < len(matrix[0]):
            distances.append((x, y))
    
    distances.sort(key=lambda p: abs(p[0] - pos[0]) + abs(p[1] - pos[1]))
    
    return distances[:k]

def pathfinding(matrix, start, goal, k=3):
    visited = set()
    queue = [(start, [start])]
    
    while queue:
        (vertex, path) = queue.pop(0)
        
        if vertex == goal:
            return path
        
        if vertex not in visited:
            for neighbor in k_nearest_neighbors(matrix, vertex, k=k):
                new_path = list(path)
                new_path.append(neighbor)
                queue.append((neighbor, new_path))
                
            visited.add(vertex)
    
    return None

matrix = matrika

start = (53, 43)
goal = (67, 67)

path = pathfinding(matrix, start, goal, k=3)