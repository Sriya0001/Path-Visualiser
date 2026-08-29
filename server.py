import time
import os
from flask import Flask, request, jsonify, render_template
from algorithms.bfs import bfs_algorithm
from algorithms.dfs import dfs_algorithm
from algorithms.dijkstra import dijkstra_algorithm
from algorithms.astar import astar_algorithm
from algorithms.bidirectional import bidirectional_bfs
from models import db, RunHistory

app = Flask(__name__)

# DB config
db_user = os.environ.get('DB_USER', 'app')
db_password = os.environ.get('DB_PASSWORD', 'app')
db_host = os.environ.get('DB_HOST', 'localhost')
db_port = os.environ.get('DB_PORT', '3307')
db_name = os.environ.get('DB_NAME', 'pathfinder')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bfs', methods=['POST'])
def bfs_route():
    data = request.get_json()
    grid = data['grid']
    start = tuple(data['start'])
    stop = tuple(data['stop'])

    start_time = time.time()
    visited, path = bfs_algorithm(grid, start, stop)
    duration_ms = (time.time() - start_time) * 1000

    record = RunHistory(
        algorithm='BFS',
        grid_rows=len(grid),
        grid_cols=len(grid[0]) if grid else 0,
        wall_count=sum(row.count(1) for row in grid),
        start_coords=str(start),
        stop_coords=str(stop),
        nodes_visited=len(visited),
        path_length=len(path),
        path_found=len(path) > 0,
        duration_ms=duration_ms
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'visited': visited,
        'path': path
    })

@app.route('/dfs', methods=['POST'])
def dfs_route():
    data = request.get_json()
    grid = data['grid']
    start = tuple(data['start'])
    stop = tuple(data['stop'])

    start_time = time.time()
    visited, path = dfs_algorithm(grid, start, stop)
    duration_ms = (time.time() - start_time) * 1000

    record = RunHistory(
        algorithm='DFS',
        grid_rows=len(grid),
        grid_cols=len(grid[0]) if grid else 0,
        wall_count=sum(row.count(1) for row in grid),
        start_coords=str(start),
        stop_coords=str(stop),
        nodes_visited=len(visited),
        path_length=len(path),
        path_found=len(path) > 0,
        duration_ms=duration_ms
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({
        'visited': visited,
        'path': path
    })
    
@app.route('/dijkstra', methods=['POST'])
def dijkstra_route():
    data = request.get_json()
    grid = data['grid']
    start = tuple(data['start'])
    stop = tuple(data['stop'])

    start_time = time.time()
    visited, path = dijkstra_algorithm(grid, start, stop)
    duration_ms = (time.time() - start_time) * 1000

    record = RunHistory(
        algorithm='Dijkstra',
        grid_rows=len(grid),
        grid_cols=len(grid[0]) if grid else 0,
        wall_count=sum(row.count(1) for row in grid),
        start_coords=str(start),
        stop_coords=str(stop),
        nodes_visited=len(visited),
        path_length=len(path),
        path_found=len(path) > 0,
        duration_ms=duration_ms
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({'visited': visited, 'path': path})

@app.route('/astar', methods=['POST'])
def astar_route():
    data = request.get_json()
    grid = data['grid']
    start = tuple(data['start'])
    stop = tuple(data['stop'])

    start_time = time.time()
    visited, path = astar_algorithm(grid, start, stop)
    duration_ms = (time.time() - start_time) * 1000

    record = RunHistory(
        algorithm='A*',
        grid_rows=len(grid),
        grid_cols=len(grid[0]) if grid else 0,
        wall_count=sum(row.count(1) for row in grid),
        start_coords=str(start),
        stop_coords=str(stop),
        nodes_visited=len(visited),
        path_length=len(path),
        path_found=len(path) > 0,
        duration_ms=duration_ms
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({'visited': visited, 'path': path})

@app.route('/bidirectional', methods=['POST'])
def bidirectional_route():
    data = request.get_json()
    grid = data['grid']
    start = tuple(data['start'])
    stop = tuple(data['stop'])

    start_time = time.time()
    visited, path = bidirectional_bfs(grid, start, stop)
    duration_ms = (time.time() - start_time) * 1000

    record = RunHistory(
        algorithm='Bidirectional',
        grid_rows=len(grid),
        grid_cols=len(grid[0]) if grid else 0,
        wall_count=sum(row.count(1) for row in grid),
        start_coords=str(start),
        stop_coords=str(stop),
        nodes_visited=len(visited),
        path_length=len(path),
        path_found=len(path) > 0,
        duration_ms=duration_ms
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({'visited': visited, 'path': path})

@app.route('/history', methods=['GET'])
def get_history():
    runs = RunHistory.query.order_by(RunHistory.id.desc()).limit(50).all()
    return jsonify([run.to_dict() for run in runs])
    
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
