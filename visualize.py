from pyvis.network import Network
import config
import recommend

def create(user_id, recs, graph, movies_df, output='demo.html'):
    # Build subgraph
    user_node = f"user_{user_id}"
    nodes = {user_node}
    for rec in recs:
        nodes.add(rec['movie_node'])
        path = recommend.explain(user_id, rec['movie_node'], graph)
        if path:
            nodes.update(path)
    
    for node in list(nodes):
        if node in graph:
            nodes.update(list(graph.neighbors(node))[:5])
    
    subgraph = graph.subgraph(nodes)
    
    # Create network
    net = Network(height='800px', width='100%', bgcolor='#1a1a1a', 
                  font_color='white', notebook=False, cdn_resources='in_line')
    
    # Add nodes
    rec_movies = {r['movie_node'] for r in recs}
    for node in subgraph.nodes():
        color, size = _get_node_style(node, user_node, rec_movies)
        label = _get_label(node, movies_df)
        net.add_node(node, label=label, color=color, size=size, title=node)
    
    # Add edges
    path_edges = _get_path_edges(user_id, recs, graph)
    for u, v in subgraph.edges():
        color = config.COLORS['edge_path'] if (u,v) in path_edges or (v,u) in path_edges else config.COLORS['edge_other']
        width = 4 if color == config.COLORS['edge_path'] else 1
        net.add_edge(u, v, color=color, width=width)
    
    net.set_options('{"physics": {"barnesHut": {"gravitationalConstant": -50000}}, "interaction": {"hover": true}}')
    net.write_html(output, notebook=False)


def _get_node_style(node, user_node, rec_movies):
    if node == user_node: return config.COLORS['user_main'], 50
    if node.startswith('user'): return config.COLORS['user_other'], 20
    if node.startswith('movie'): return (config.COLORS['movie_rec'], 40) if node in rec_movies else (config.COLORS['movie_other'], 25)
    if node.startswith('genre'): return config.COLORS['genre'], 35
    return '#888', 20

def _get_label(node, movies_df):
    if node.startswith(('user', 'genre')): return node.split('_')[1]
    movie_id = int(node.split('_')[1])
    return movies_df[movies_df['movieId'] == movie_id].iloc[0]['title'][:30]

def _get_path_edges(user_id, recs, graph):
    edges = set()
    for rec in recs:
        path = recommend.explain(user_id, rec['movie_node'], graph)
        if path:
            for i in range(len(path)-1):
                edges.add((path[i], path[i+1]))
    return edges