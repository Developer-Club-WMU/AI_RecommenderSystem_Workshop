import networkx as nx
from tqdm import tqdm
import config

def build(ratings, movies, genres):
    G = nx.Graph()
    
    # User → Movie edges (high ratings only)
    high_ratings = ratings[ratings['rating'] >= config.MIN_RATING]
    for _, row in tqdm(high_ratings.iterrows(), total=len(high_ratings), desc="User-Movie"):
        G.add_edge(f"user_{row['userId']}", f"movie_{row['movieId']}", rating=row['rating'])
    
    # Movie → Genre edges
    for _, row in tqdm(movies.iterrows(), total=len(movies), desc="Movie-Genre"):
        movie = f"movie_{row['movieId']}"
        if movie in G:
            for genre in genres:
                if row[genre] == 1:
                    G.add_edge(movie, f"genre_{genre}")
    
    return G