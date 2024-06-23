from settings import matrika
from node import * 

def decisiontree_pathfinding(matrika, start, goal):
    root = Node(start)
    stack = [root]
    visited = set()

    while stack:
        current_node = stack.pop()
        x, y = current_node.position

        if (x, y) == goal: 
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  

        if (x, y) not in visited:
            visited.add((x, y))
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(matrika) and 0 <= ny < len(matrika[0]) and matrika[nx][ny] != 0:  
                    if (nx, ny) not in visited:
                        child_node = Node((nx, ny), parent=current_node)
                        stack.append(child_node)

    return None