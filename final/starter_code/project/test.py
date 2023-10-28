from collections import deque

def is_valid(x, y, graph):
    return 0 <= x < len(graph) and 0 <= y < len(graph[0])

def shortest_path_to_vertex(graph, start_x, start_y, target_x, target_y):
    movements = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    queue = deque([(start_x, start_y, [])])  # (x, y, path)
    visited = set()

    while queue:
        x, y, path = queue.popleft()
        visited.add((x, y))

        if (x, y) == (target_x, target_y):
            return path

        for dx, dy in movements:
            new_x, new_y = x + dx, y + dy
            if is_valid(new_x, new_y, graph) and (new_x, new_y) not in visited:
                new_path = path + [(new_x, new_y)]
                queue.append((new_x, new_y, new_path))

    return None  # No path found

graph = [
    [0, 0, 1, 0],
    [0, 0, 0, 2],
    [0, 0, 0, 1],
    [0, 0, 0, 0]
]

start_x, start_y = 2, 2
target_x, target_y = 1, 3

path = shortest_path_to_vertex(graph, start_x, start_y, target_x, target_y)

if path is not None:
    print("Shortest path:", path)
else:
    print("No path found.")

