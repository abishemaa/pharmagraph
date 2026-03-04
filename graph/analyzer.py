# analyzer.py
import networkx as nx


def compute_metrics(G):
    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)

    return {
        "degree": degree,
        "betweenness": betweenness
    }