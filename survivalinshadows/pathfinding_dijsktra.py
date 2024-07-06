from heapq import heappop, heappush

class Dijkstra:
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0

    def __lt__(self, other):  
        return self.g < other.g

    def __eq__(self, other):
        return self.position == other.position

def dijkstra_pathfinding(maze, start, end, max_steps):
    start_node = Dijkstra(None, start)
    end_node = Dijkstra(None, end)
    open_list = []  
    heappush(open_list, start_node)
    open_set = {start}

    closed_list = [[False for _ in range(len(maze[0]))] for _ in range(len(maze))]

    nodes_visited = 0
    while open_list:
        nodes_visited += 1
        if nodes_visited == max_steps:  
            print(f"Visited {nodes_visited} nodes, open list size is {len(open_list)}")
            return
        current_node = heappop(open_list)
        open_set.remove(current_node.position)

        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]
            
        closed_list[current_node.position[1]][current_node.position[0]] = True
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            if not(0 <= node_position[1] < len(maze)) or not(0 <= node_position[0] < len(maze[0])):
                continue

            if maze[node_position[1]][node_position[0]] == "0":
                continue

            if closed_list[node_position[1]][node_position[0]]:
                continue

            new_node = Dijkstra(current_node, node_position)
            new_node.g = current_node.g + 1

            if new_node.position in open_set:
                continue

            heappush(open_list, new_node)
            open_set.add(new_node.position)

    print(f"No path found after visiting {nodes_visited} nodes")
    return None