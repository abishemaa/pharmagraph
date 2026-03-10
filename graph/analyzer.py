# analyzer.py
import networkx as nx

def enrich_graph_with_metrics(G):
    if G is None:
        return G
        
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)

    for node in G.nodes():
        G.nodes[node]["degree_centrality"] = degree[node]
        G.nodes[node]["betweenness_centrality"] = betweenness[node]

    return G