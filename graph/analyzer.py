# analyzer.py - Minimal metrics for CLI
import networkx as nx

def enrich_graph_with_metrics(G):
    """Add basic network metrics to graph"""
    if G is None or len(G.nodes) == 0:
        return G
    
    # Calculate centrality
    degree = nx.degree_centrality(G)
    
    try:
        betweenness = nx.betweenness_centrality(G)
    except:
        betweenness = {node: 0 for node in G.nodes()}
    
    # Add to graph
    for node in G.nodes():
        G.nodes[node]["degree_centrality"] = degree[node]
        G.nodes[node]["betweenness_centrality"] = betweenness.get(node, 0)
        G.nodes[node]["degree"] = G.degree(node)
    
    return G