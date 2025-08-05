from collections import deque

def bidirectional_bfs(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    visited_start = set()
    visited_goal = set()
    parent_start = {}
    parent_goal = {}

    queue_start = deque([start])
    queue_goal = deque([goal])
    visited_start.add(start)
    visited_goal.add(goal)

    visited_order = []

    def get_neighbors(x, y):
        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == 0:
                yield (nx, ny)

    meeting_point = None

    while queue_start and queue_goal:
        # Expand from start
        x, y = queue_start.popleft()
        visited_order.append([x, y])
        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in visited_start:
                visited_start.add((nx, ny))
                parent_start[(nx, ny)] = (x, y)
                queue_start.append((nx, ny))
                if (nx, ny) in visited_goal:
                    meeting_point = (nx, ny)
                    break
        if meeting_point:
            break

        # Expand from goal
        x, y = queue_goal.popleft()
        visited_order.append([x, y])
        for nx, ny in get_neighbors(x, y):
            if (nx, ny) not in visited_goal:
                visited_goal.add((nx, ny))
                parent_goal[(nx, ny)] = (x, y)
                queue_goal.append((nx, ny))
                if (nx, ny) in visited_start:
                    meeting_point = (nx, ny)
                    break
        if meeting_point:
            break

    # Reconstruct path
    path = []
    if meeting_point:
        # From meeting point to start
        p = meeting_point
        while p != start:
            path.append([p[0], p[1]])
            p = parent_start[p]
        path.reverse()

        # From meeting point to goal
        p = meeting_point
        while p != goal:
            p = parent_goal[p]
            path.append([p[0], p[1]])

    return visited_order, path
