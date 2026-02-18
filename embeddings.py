from node2vec import Node2Vec
import config

def train(graph):
    model_path = config.DATA_DIR.parent / "processed" / "node2vec.model"
    
    if model_path.exists():
        from gensim.models import Word2Vec
        return Word2Vec.load(str(model_path))
    
    node2vec = Node2Vec(
        graph,
        dimensions=config.EMBEDDING_DIM,
        walk_length=config.WALK_LENGTH,
        num_walks=config.NUM_WALKS,
        workers=4,
        quiet=True
    )
    model = node2vec.fit(window=10, min_count=1, batch_words=4)
    model.save(str(model_path))
    return model
