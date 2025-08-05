const canvas = document.getElementById('gridCanvas');
const ctx = canvas.getContext('2d');

const ROWS = 19;
const COLS = 34;
const SIZE = canvas.width / COLS;
let grid = [];

const WALL_COLOR = '#1e2b4d';
const START_COLOR = '#2ecc71';
const STOP_COLOR = '#e74c3c';
const VISITED_COLOR = '#74b9ff';
const PATH_COLOR = '#f39c12';

let startCell = null;
let stopCell = null;
let isMouseDown = false;
let dragMode = null;

let speedValue = 20; // Initial speed from slider

function updateSpeed() {
  const slider = document.getElementById('speedSlider');
  speedValue =parseInt(slider.value);
}

function createGrid() {
  grid = [];
  for (let i = 0; i < ROWS; i++) {
    const row = [];
    for (let j = 0; j < COLS; j++) {
      row.push({ x: j, y: i, visited: false });
    }
    grid.push(row);
  }
}

function drawGrid() {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (let row of grid) {
  for (let cell of row) {
    let x = cell.x * SIZE;
    let y = cell.y * SIZE;

    if (cell === startCell) {
      ctx.fillStyle = START_COLOR;
      ctx.fillRect(x, y, SIZE, SIZE);
    } else if (cell === stopCell) {
      ctx.fillStyle = STOP_COLOR;
      ctx.fillRect(x, y, SIZE, SIZE);
    } else if (cell.type === 'wall') {
      ctx.fillStyle = WALL_COLOR;
      ctx.fillRect(x, y, SIZE, SIZE);
    } else if (cell.visited) {
      ctx.fillStyle = VISITED_COLOR;
      ctx.fillRect(x, y, SIZE, SIZE);
    }
    
    // ✅ Always draw cell border
    ctx.strokeStyle = '#ccc';
    ctx.strokeRect(x, y, SIZE, SIZE);
  }
}

}

function getCellFromEvent(e) {
  const rect = canvas.getBoundingClientRect();
  const x = Math.floor((e.clientX - rect.left) / SIZE);
  const y = Math.floor((e.clientY - rect.top) / SIZE);
  if (x < 0 || y < 0 || x >= COLS || y >= ROWS) return {};
  return { cell: grid[y][x], x, y };
}

canvas.addEventListener('contextmenu', e => e.preventDefault());

canvas.addEventListener('mousedown', (e) => {
  const { cell } = getCellFromEvent(e);
  if (!cell) return;

  isMouseDown = true;

  if (e.button === 0) {
    if (e.ctrlKey) {
      if (!startCell) startCell = cell;
      else if (!stopCell && cell !== startCell) stopCell = cell;
    } else {
      cell.type = 'wall';
      dragMode = 'wall';
    }
  } else if (e.button === 2) {
    if (cell === startCell) startCell = null;
    if (cell === stopCell) stopCell = null;
    delete cell.type;
    cell.visited = false;
    dragMode = 'erase';
  }

  drawGrid();
});

canvas.addEventListener('mousemove', (e) => {
  if (!isMouseDown) return;
  const { cell } = getCellFromEvent(e);
  if (!cell) return;

  if (dragMode === 'wall') {
    if (!cell.type && cell !== startCell && cell !== stopCell) {
      cell.type = 'wall';
    }
  } else if (dragMode === 'erase') {
    if (cell === startCell) startCell = null;
    if (cell === stopCell) stopCell = null;
    delete cell.type;
    cell.visited = false;
  }

  drawGrid();
});

canvas.addEventListener('mouseup', () => {
  isMouseDown = false;
  dragMode = null;
});

canvas.addEventListener('mouseleave', () => {
  isMouseDown = false;
  dragMode = null;
});

function resetGrid() {
  startCell = null;
  stopCell = null;
  createGrid();
  drawGrid();
}

async function runAlgorithm(endpoint) {
  if (!startCell || !stopCell) return alert("Start and stop cells must be set!");

  const simplifiedGrid = grid.map(row => row.map(cell => cell.type === 'wall' ? 1 : 0));
  const start = [startCell.x, startCell.y];
  const stop = [stopCell.x, stopCell.y];

  const res = await fetch(endpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ grid: simplifiedGrid, start, stop })
  });

  const data = await res.json();
  const visited = data.visited;
  const path = data.path;

  if (!visited.length) {
    alert('No path found.');
    return;
  }

  animateVisited(visited, () => animatePath(path));
}

function animateVisited(visited, onComplete) {
  let i = 0;
  for (let row of grid) {
    for (let cell of row) {
      cell.visited = false;
    }
  }

  const interval = setInterval(() => {
    if (i >= visited.length) {
      clearInterval(interval);
      onComplete();
      return;
    }
    const [x, y] = visited[i];
    const cell = grid[y][x];
    if (cell !== startCell && cell !== stopCell) {
      cell.visited = true;
    }
    drawGrid();
    i++;
  }, speedValue);
}

function animatePath(path) {
  let i = 0;
  const interval = setInterval(() => {
    if (i >= path.length) {
      clearInterval(interval);
      return;
    }
    const [x, y] = path[i];
    const cell = grid[y][x];
    if (cell !== startCell && cell !== stopCell) {
      ctx.fillStyle = PATH_COLOR;
      ctx.fillRect(x * SIZE, y * SIZE, SIZE, SIZE);
      ctx.strokeStyle = '#ccc';
      ctx.strokeRect(x * SIZE, y * SIZE, SIZE, SIZE);
    }
    i++;
  }, speedValue);
}

async function startBFS() {
  await runAlgorithm('/bfs');
}

async function startDFS() {
  await runAlgorithm('/dfs');
}

async function startDijkstra() {
  await runAlgorithm('/dijkstra');
}

async function startAStar() {
  await runAlgorithm('/astar');
}

async function startBidirectional() {
  await runAlgorithm('/bidirectional');
}

function generateRandomMaze() {
  resetGrid();
  for (let row of grid) {
    for (let cell of row) {
      if (Math.random() < 0.3 && cell !== startCell && cell !== stopCell) {
        cell.type = 'wall';
      }
    }
  }
  drawGrid();
}

// Init
document.addEventListener('DOMContentLoaded', () => {
  createGrid();
  drawGrid();
});