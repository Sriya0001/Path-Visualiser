import random
import json
from locust import HttpUser, task, between

def generate_random_grid(rows, cols, wall_probability):
    grid = []
    for _ in range(rows):
        row = [1 if random.random() < wall_probability else 0 for _ in range(cols)]
        grid.append(row)
    return grid

class PathfindingUser(HttpUser):
    wait_time = between(0.1, 1.0)
    
    def generate_payload(self):
        size_choice = random.choice(['small', 'medium', 'large'])
        if size_choice == 'small':
            rows, cols = 10, 10
        elif size_choice == 'medium':
            rows, cols = 19, 34
        else:
            rows, cols = 40, 60
            
        wall_prob = random.choice([0.0, 0.15, 0.30])
        grid = generate_random_grid(rows, cols, wall_prob)
        
        start = (random.randint(0, cols-1), random.randint(0, rows-1))
        stop = (random.randint(0, cols-1), random.randint(0, rows-1))
        
        # ensure start/stop aren't walls
        grid[start[1]][start[0]] = 0
        grid[stop[1]][stop[0]] = 0
        
        return {
            "grid": grid,
            "start": list(start),
            "stop": list(stop)
        }

    @task(1)
    def test_bfs(self):
        self.client.post("/bfs", json=self.generate_payload(), name="/bfs")

    @task(1)
    def test_dfs(self):
        self.client.post("/dfs", json=self.generate_payload(), name="/dfs")

    @task(1)
    def test_dijkstra(self):
        self.client.post("/dijkstra", json=self.generate_payload(), name="/dijkstra")

    @task(1)
    def test_astar(self):
        self.client.post("/astar", json=self.generate_payload(), name="/astar")

    @task(1)
    def test_bidirectional(self):
        self.client.post("/bidirectional", json=self.generate_payload(), name="/bidirectional")
