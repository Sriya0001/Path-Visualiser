CREATE TABLE run_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    algorithm VARCHAR(50) NOT NULL,
    grid_rows INT NOT NULL,
    grid_cols INT NOT NULL,
    wall_count INT NOT NULL,
    start_coords VARCHAR(20) NOT NULL,
    stop_coords VARCHAR(20) NOT NULL,
    nodes_visited INT NOT NULL,
    path_length INT NOT NULL,
    path_found BOOLEAN NOT NULL,
    duration_ms FLOAT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
