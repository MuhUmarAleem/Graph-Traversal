import heapq
infinity = float('inf')

def Dijkstra(graph, start, goal):
  pq = []
  distances = [infinity for _ in range(len(graph))]
  visited = set()  
  heapq.heappush(pq, (0, start, [start]))
  distances[start] = 0
  entire_path: list[list[int]] = []

  while pq:
    dist_u, u, path = heapq.heappop(pq)
    entire_path.append(path)
    if u in visited:
      continue  
    visited.add(u)
    if u == goal:
      return entire_path
    if dist_u > distances[u]:
      continue

    for neighbour in graph[u]:
      if neighbour in visited:
        continue
      dist_v = neighbour[0]
      v = neighbour[1]
      if dist_v + dist_u < distances[v]:
        distances[v] = dist_v + dist_u
        heapq.heappush(pq, (distances[v], v, path + [v]))

  return -1
