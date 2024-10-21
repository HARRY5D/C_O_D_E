from collections import deque

def bfs(graph, start):
    visited = set()
    traversal_order = []
    queue = deque([start])
    visited.add(start)
    while queue:
        node = queue.popleft()
        traversal_order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    return traversal_order

graph = {
    0: [1, 2, 3],
    1: [],
    2: [],
    3: [],
    4: []
}

print(bfs(graph, 0)) 