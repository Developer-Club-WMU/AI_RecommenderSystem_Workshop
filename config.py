from pathlib import Path

DATA_DIR = Path("data/ml-100k")
MOVIELENS_URL = "http://files.grouplens.org/datasets/movielens/ml-100k.zip"

MIN_RATING = 3.5
EMBEDDING_DIM = 64
WALK_LENGTH = 30
NUM_WALKS = 200

COLORS = {
    'user_main': '#FFD700',
    'user_other': '#4A90E2',
    'movie_rec': '#FF6B6B', 
    'movie_other': '#C44569',
    'genre': '#4ECDC4',
    'edge_path': '#FFD700',
    'edge_other': '#555555'
    }