import data
import graph
import embeddings
import recommend
import visualize

def run(user_id=1, n_recs=10): 
    # Pipeline
    ratings, movies, genres = data.load()
    G = graph.build(ratings, movies, genres)
    model = embeddings.train(G)
    
    # Recommend
    recs = recommend.get_recommendations(user_id, G, model, movies, n=n_recs)
    
    
    for i, rec in enumerate(recs, 1):
        print(f"{i:<4} {rec['title'][:44]:<45} {rec['similarity']:.3f}    {rec['rating']:.1f}/5")
    
    # Explain
    for i, rec in enumerate(recs[:3], 1):
        path = recommend.explain(user_id, rec['movie_node'], G)
        if path:
            print(f"{i}. {rec['title']}")
            print(f"   Path: {' → '.join([p.split('_')[1] for p in path])}\n")
    
    # Visualize
    visualize.create(user_id, recs, G, movies)

if __name__ == "__main__":
    run(user_id=1, n_recs=10)