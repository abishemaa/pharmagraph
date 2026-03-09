import networkx as nx
import matplotlib.pyplot as plt
from database import get_all_drugs, get_all_interactions


def build_graph():

    G = nx.Graph()

    for (drug,) in get_all_drugs():
        G.add_node(drug)

    for d1, d2, severity in get_all_interactions():
        G.add_edge(d1, d2, severity=severity)

    return G


import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(G):

    pos = nx.spring_layout(G, k=0.7)

    # node size = number of interactions
    degrees = dict(G.degree())
    node_sizes = [degrees[n] * 800 for n in G.nodes()]

    # edge color based on severity
    edge_colors = []

    for u, v, data in G.edges(data=True):

        severity = data.get("severity", "minor")

        if severity == "major":
            edge_colors.append("red")

        elif severity == "moderate":
            edge_colors.append("orange")

        else:
            edge_colors.append("green")

    nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edge_color=edge_colors
    )

    # label only important nodes
    labels = {}

    for node, deg in degrees.items():

        if deg >= 2:
            labels[node] = node

    nx.draw_networkx_labels(G, pos, labels)

    plt.title("Drug Interaction Network")
    plt.axis("off")
    plt.show()
