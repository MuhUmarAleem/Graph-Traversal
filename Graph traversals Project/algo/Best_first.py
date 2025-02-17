import heapq

def Greedy_Best_First(graph, heuristic, start, goal):
    pq = []
    heapq.heappush(pq, (heuristic[start], start, [start]))
    visited = [False for i in range(len(graph))]
    entire_path:list[list[int]] = []

    while pq:
        current_heuristic, current, path = heapq.heappop(pq)
        entire_path.append(path)
        visited[current] = True
        if current == goal:
            return entire_path
        for neighbor in graph[current]:
            if not visited[neighbor]:
                heapq.heappush(pq, (heuristic[neighbor], neighbor, path + [neighbor]))
    return -1
