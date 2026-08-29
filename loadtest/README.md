# Load Testing

This directory contains a Locust test script to load test the pathfinding API endpoints.

## Prerequisites

1. Ensure your application is running locally.
2. Install Locust:
   ```bash
   pip install locust
   ```

## Running the Test

Run the following command from the repository root to start the load test against the local server (assuming it's running on port 8000). This command runs Locust without the web UI, simulating 50 concurrent users for 60 seconds.

```bash
venv\Scripts\locust -f loadtest/locustfile.py --host=http://localhost:5000 --headless -u 50 -r 10 --run-time 1m
```

Alternatively, to use the web UI:
```bash
venv\Scripts\locust -f loadtest/locustfile.py --host=http://localhost:5000
```
Then open `http://localhost:8089` in your browser.
