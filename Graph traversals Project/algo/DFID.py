def DFS(adj, visited, current:int , goal, path:list[int]=[]):  
  if visited[current]:
    return None
  
  path.append(current)
  visited[current] = True
  
  if current == goal:
    return path

  for neighbour in adj[current]:
    result = DFS(adj.copy(), visited.copy(), neighbour, goal, path.copy())  
    if result:
      return result

  return None

def DF_ID(adj, start, goal, max_depth=100):
  
  for depth in range(max_depth):
    visited = [False] * len(adj) 
    path = []
    result = DFS(adj, visited, start, goal, path)
    if result:
      return [result]
  
  return None
