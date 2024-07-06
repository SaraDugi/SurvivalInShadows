from heapq import heappush, heappop

class Node:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.children = []
        self.cost = 0

    def __lt__(self, other):  
        return self.cost < other.cost

    def __eq__(self, other):
        return self.position == other.position

def heuristic(node_position, goal_position):
    return abs(node_position[0] - goal_position[0]) + abs(node_position[1] - goal_position[1])

def greedy_pathfinding(maze, start, end, max_steps):
    start_node = Node(None, start)
    end_node = Node(None, end)

    open_list = []
    heappush(open_list, (0, start_node))

    visited = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]

    nodes_visited = 0
    while open_list:
        nodes_visited += 1
        if nodes_visited == max_steps:
            print(f"Visited {nodes_visited} nodes")
            return

        _, current_node = heappop(open_list)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]

        visited[current_node.position[1]][current_node.position[0]] = True

        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if not(0 <= node_position[1] < len(maze)) or not(0 <= node_position[0] < len(maze[0])):
                continue

            if maze[node_position[1]][node_position[0]] == "0":
                continue

            if visited[node_position[1]][node_position[0]]:
                continue

            new_node = Node(current_node, node_position)
            new_node.cost = current_node.cost + 1 + heuristic(node_position, end_node.position)
            current_node.children.append(new_node)

            heappush(open_list, (new_node.cost, new_node))

    print(f"No path found after visiting {nodes_visited} nodes")
    return None