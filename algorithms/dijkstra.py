import heapq

def dijkstra_algorithm(grid, start, stop):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    distance = [[float('inf')] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]

    distance[start[1]][start[0]] = 0
    heap = [(0, start)]
    visited_order = []

    while heap:
        dist, (x, y) = heapq.heappop(heap)

        if visited[y][x]:
            continue
        visited[y][x] = True
        visited_order.append([x, y])

        if (x, y) == stop:
            break

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if not visited[ny][nx] and grid[ny][nx] == 0:
                    new_dist = dist + 1
                    if new_dist < distance[ny][nx]:
                        distance[ny][nx] = new_dist
                        parent[ny][nx] = (x, y)
                        heapq.heappush(heap, (new_dist, (nx, ny)))

    path = []
    if visited[stop[1]][stop[0]]:
        x, y = stop
        while (x, y) != start:
            path.append([x, y])
            x, y = parent[y][x]
        path.reverse()

    return visited_order, path
