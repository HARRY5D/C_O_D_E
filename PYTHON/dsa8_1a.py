def dfs(graph, start):
    visited = set()
    traversal_order = []
    def dfs_helper(node):
        visited.add(node)
        traversal_order.append(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs_helper(neighbor)
    dfs_helper(start)
    return traversal_order

graph = {
    0: [2, 3, 1],
    1: [0],
    2: [0, 4],
    3: [0],
    4: [2]
}

print(dfs(graph, 0))  