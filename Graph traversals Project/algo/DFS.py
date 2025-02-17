def DFS(adj, current, goal, visited=None, path:list[int]=[], entire_path: list[list[int]] = []):
    if visited == None:
        visited = [False for i in range(len(adj))]
        path.clear()
        entire_path.clear()
    if visited[current]:
        return None
    
    path.append(current)
    entire_path.append(path + [])
    visited[current] = True
    
    if current == goal:
        return entire_path

    for neighbour in adj[current]:
        result = DFS(adj, neighbour, goal, visited, path, entire_path)
        if result:
            return result

    return None