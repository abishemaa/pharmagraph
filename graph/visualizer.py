# visualizer.py
import networkx as nx
import matplotlib.pyplot as plt
from .builder import build_graph


def visualize_graph(drug_name=None):
    G = build_graph(drug_name)

    if G is None:
        return

    pos = nx.spring_layout(G, seed=42, weight="weight")

    plt.figure(figsize=(10, 7))

    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=800,
        arrows=True
    )

    plt.title("Drug Interaction Network")
    plt.axis("off")
    plt.tight_layout()
    plt.show()