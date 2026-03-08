# analyzer.py
import networkx as nx


import networkx as nx


def enrich_graph_with_metrics(G):

    if G is None or len(G.nodes) == 0:
        return G

    degree = nx.degree_centrality(G)
    betweenness = nx.betweenness_centrality(G)

    for node in G.nodes():
        G.nodes[node]["degree_centrality"] = degree[node]
        G.nodes[node]["betweenness_centrality"] = betweenness[node]

    return G

def shortest_interaction_path(graph, drug_a, drug_b):

    try:
        return nx.shortest_path(graph, drug_a, drug_b)
    except nx.NetworkXNoPath:
        return None