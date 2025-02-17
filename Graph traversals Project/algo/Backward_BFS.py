from collections import deque

def backward_BFS(graph, start, goal):
  q = deque()
  q.append(start)  
  came_from = {start: None} 

  while (len(q) != 0):
    current = q.popleft()
    if current == goal:
      path = []
      while current is not None:
        path.append(current)
        current = came_from[current]
      return [path]

    for neighbour in graph[current]:
      if neighbour not in came_from:
        q.append(neighbour)
        came_from[neighbour] = current

  return -1