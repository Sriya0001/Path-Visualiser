def dfs_algorithm(grid, start, stop):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    parent = [[None for _ in range(cols)] for _ in range(rows)]

    stack = [start]
    visited_cells = []

    while stack:
        x, y = stack.pop()
        if visited[y][x]:
            continue
        visited[y][x] = True
        visited_cells.append([x, y])

        if (x, y) == stop:
            break

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if not visited[ny][nx] and grid[ny][nx] == 0:
                    stack.append((nx, ny))
                    parent[ny][nx] = (x, y)

    # Reconstruct path
    path = []
    if visited[stop[1]][stop[0]]:
        x, y = stop
        while (x, y) != start:
            path.append([x, y])
            x, y = parent[y][x]
        path.reverse()

    return visited_cells, path
