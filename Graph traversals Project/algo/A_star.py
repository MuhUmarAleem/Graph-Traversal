import heapq
infinity = float('inf')

def A_star(graph, heuristics, start, goal):
    pq = []
    distances = [infinity for i in range(len(graph))]
    heapq.heappush(pq, (0, start, [start]))
    distances[start] = 0
    visited = set()
    entire_path: list[list[int]] = []

    while pq:
        dist_u, u, path = heapq.heappop(pq)
        entire_path.append(path)
        if u in visited:
            continue
        visited.add(u)
        if u == goal:
            return entire_path
        if distances[u] < dist_u:
            continue
        for neighbour in graph[u]:
            if neighbour in visited:
                continue
            dist_v = neighbour[0]
            v = neighbour[1]
            if dist_u + dist_v + heuristics[v] < distances[v]:
                distances[v] = dist_u + dist_v + heuristics[v]
                heapq.heappush(pq, (distances[v], v, path + [v]))

    return -1
