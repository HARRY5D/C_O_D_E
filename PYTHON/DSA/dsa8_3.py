def maximumDetonation(bombs):
    def isDetonated(bomb1, bomb2):
        x1, y1, r1 = bomb1
        x2, y2, r2 = bomb2
        return (x1 - x2) ** 2 + (y1 - y2) ** 2 <= r1 ** 2

    graph = [[] for _ in range(len(bombs))]
    for i in range(len(bombs)):
        for j in range(len(bombs)):
            if i != j and isDetonated(bombs[i], bombs[j]):
                graph[i].append(j)

    def dfs(node, visited):
        visited.add(node)
        for neighbor in graph[node]:
            if neighbor not in visited:
                dfs(neighbor, visited)

    max_detonation = 0
    for i in range(len(bombs)):
        visited = set()
        dfs(i, visited)
        max_detonation = max(max_detonation, len(visited))

    return max_detonation

bombs = [[2, 1, 3], [6, 1, 4]]
print(maximumDetonation(bombs)) 