from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

def get_recommendations(user_id, graph, model, movies_df, n=10):
    user_node = f"user_{user_id}"
    if user_node not in model.wv:
        return []
    
    user_vec = model.wv[user_node].reshape(1, -1)
    rated = set(graph.neighbors(user_node))
    candidates = [n for n in graph.nodes() if n.startswith('movie_') and n not in rated]
    
    recs = []
    for movie_node in candidates:
        if movie_node not in model.wv:
            continue
        
        movie_vec = model.wv[movie_node].reshape(1, -1)
        sim = cosine_similarity(user_vec, movie_vec)[0][0]
        movie_id = int(movie_node.split('_')[1])
        title = movies_df[movies_df['movieId'] == movie_id].iloc[0]['title']
        
        recs.append({'movie_node': movie_node, 'title': title, 'similarity': sim, 'rating': 1 + sim * 4})
    
    recs.sort(key=lambda x: x['similarity'], reverse=True)
    return recs[:n]

def explain(user_id, movie_node, graph):
    try:
        return nx.shortest_path(graph, f"user_{user_id}", movie_node)
    except:
        return None