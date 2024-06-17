from settings import matrika

start_position = (53, 47)
goal_position = (53, 42)
grid_map = matrika

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.children = []

    def add_child(self, node):
        self.children.append(node)

def decision_tree_pathfinding(grid_map, start, goal):
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
                if 0 <= nx < len(grid_map) and 0 <= ny < len(grid_map[0]) and grid_map[nx][ny] != 0 and (nx, ny) not in visited:  
                    child_node = Node((nx, ny), parent=current_node)
                    current_node.add_child(child_node)
                    stack.append(child_node)

    return None

path = decision_tree_pathfinding(grid_map, start_position, goal_position)