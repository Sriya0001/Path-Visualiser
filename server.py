from flask import Flask, request, jsonify, render_template
from algorithms.bfs import bfs_algorithm
from algorithms.dfs import dfs_algorithm
from algorithms.dijkstra import dijkstra_algorithm
from algorithms.astar import astar_algorithm
from algorithms.bidirectional import bidirectional_bfs

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/bfs', methods=['POST'])
def bfs_route():
    data = request.get_json()
    grid = data['grid']
    start = tuple(data['start'])
    stop = tuple(data['stop'])

    visited, path = bfs_algorithm(grid, start, stop)

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

    visited, path = dfs_algorithm(grid, start, stop)

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

    visited, path = dijkstra_algorithm(grid, start, stop)
    return jsonify({'visited': visited, 'path': path})

@app.route('/astar', methods=['POST'])
def astar_route():
    data = request.get_json()
    grid = data['grid']
    start = tuple(data['start'])
    stop = tuple(data['stop'])

    visited, path = astar_algorithm(grid, start, stop)
    return jsonify({'visited': visited, 'path': path})

@app.route('/bidirectional', methods=['POST'])
def bidirectional_route():
    data = request.get_json()
    grid = data['grid']
    start = tuple(data['start'])
    stop = tuple(data['stop'])

    visited, path = bidirectional_bfs(grid, start, stop)
    return jsonify({'visited': visited, 'path': path})
    
if __name__ == '__main__':
    app.run(debug=True)
