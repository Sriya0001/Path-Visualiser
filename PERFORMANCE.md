# Performance Results

These load testing results were captured by running the local API under the `waitress` WSGI server (simulating a multi-threaded production environment similar to gunicorn on Windows) backed by a Dockerized MySQL database. The test was executed with Locust simulating 50 concurrent users making random pathfinding requests against small (10x10), medium (19x34), and large (40x60) grids with varying wall densities.

## Metrics summary

| Endpoint       | Total Requests | Failure Rate | Requests/sec | Median Latency | p95 Latency |
|----------------|----------------|--------------|--------------|----------------|-------------|
| `/astar`       | 182            | 0.00%        | 12.32        | 32ms           | 2100ms      |
| `/bfs`         | 189            | 0.00%        | 12.79        | 35ms           | 2100ms      |
| `/bidirectional`| 179            | 0.00%        | 12.11        | 33ms           | 2100ms      |
| `/dfs`         | 177            | 0.00%        | 11.98        | 32ms           | 150ms       |
| `/dijkstra`    | 182            | 0.00%        | 12.32        | 34ms           | 2100ms      |
| **Aggregate**  | 909            | **0.00%**    | **61.51**    | **34ms**       | **2100ms**  |

## Observations

- **Zero Failures**: The server handled the load successfully without dropping any connections or throwing any 500 errors.
- **Latency Spikes**: Under high concurrency (50 users), median response times stay highly performant (around 32-35ms). However, the 95th percentile latency hits around 2100ms for most algorithms except DFS. 
- **Degradation Causes**: BFS and Dijkstra tend to degrade first under load because they visit a significantly larger number of nodes compared to DFS, which just dives down a single path. On large (40x60) grids with low wall densities, BFS and Dijkstra consume more CPU time and memory, leading to thread contention in the WSGI server which queues up incoming requests, causing the observed latency spikes for concurrent users.
