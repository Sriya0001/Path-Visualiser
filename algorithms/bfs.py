from collections import deque

def bfs_algorithm(grid, start, stop):
    rows = len(grid)
    cols = len(grid[0])
    visited = [[False for _ in range(cols)] for _ in range(rows)]
    parent = [[None for _ in range(cols)] for _ in range(rows)]

    queue = deque()
    queue.append(start)
    visited[start[1]][start[0]] = True

    visited_cells = []

    found = False
    while queue:
        x, y = queue.popleft()
        visited_cells.append([x, y])

        if (x, y) == stop:
            found = True
            break

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows:
                if not visited[ny][nx] and grid[ny][nx] == 0:
                    visited[ny][nx] = True
                    parent[ny][nx] = (x, y)
                    queue.append((nx, ny))

    path = []
    if found:
        x, y = stop
        while (x, y) != start:
            path.append([x, y])
            x, y = parent[y][x]
        path.reverse()

    return visited_cells, path
