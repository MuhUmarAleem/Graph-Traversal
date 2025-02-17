from collections import deque

def BFS(adj, start, goal):
    q = deque()
    q.append(start)
    visited = [False for i in range(len(adj))]
    path = []
    entire_path: list[list[int]] = []

    while q:
        current = q.popleft()
        path.append(current)
        entire_path.append(path + [])
        visited[current] = True
        if current == goal:
            return entire_path
        for neighbor in adj[current]:
            if visited[neighbor] == False:
                q.append(neighbor)

    return -1