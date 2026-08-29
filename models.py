from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class RunHistory(db.Model):
    __tablename__ = 'run_history'

    id = db.Column(db.Integer, primary_key=True)
    algorithm = db.Column(db.String(50), nullable=False)
    grid_rows = db.Column(db.Integer, nullable=False)
    grid_cols = db.Column(db.Integer, nullable=False)
    wall_count = db.Column(db.Integer, nullable=False)
    start_coords = db.Column(db.String(20), nullable=False)
    stop_coords = db.Column(db.String(20), nullable=False)
    nodes_visited = db.Column(db.Integer, nullable=False)
    path_length = db.Column(db.Integer, nullable=False)
    path_found = db.Column(db.Boolean, nullable=False)
    duration_ms = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'algorithm': self.algorithm,
            'grid_rows': self.grid_rows,
            'grid_cols': self.grid_cols,
            'wall_count': self.wall_count,
            'start_coords': self.start_coords,
            'stop_coords': self.stop_coords,
            'nodes_visited': self.nodes_visited,
            'path_length': self.path_length,
            'path_found': self.path_found,
            'duration_ms': self.duration_ms,
            'created_at': self.created_at.isoformat() + 'Z'
        }
