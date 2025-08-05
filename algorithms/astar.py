import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def astar_algorithm(grid, start, stop):
    rows, cols = len(grid), len(grid[0])
    open_set = []
    heapq.heappush(open_set, (0 + heuristic(start, stop), 0, start))
    came_from = {}
    g_score = { (x, y): float('inf') for y in range(rows) for x in range(cols) }
    g_score[start] = 0
    visited_order = []

    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        x, y = current

        if current == stop:
            break

        if current not in visited_order:
            visited_order.append([x, y])

        for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
            nx, ny = x + dx, y + dy
            neighbor = (nx, ny)
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                tentative_g = g_score[current] + 1
                if tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + heuristic(neighbor, stop)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    # Reconstruct path
    path = []
    node = stop
    if node in came_from:
        while node != start:
            path.append([node[0], node[1]])
            node = came_from[node]
        path.reverse()

    return visited_order, path
