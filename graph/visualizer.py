# visualizer.py
import networkx as nx
import matplotlib.pyplot as plt
from graph.builder import build_graph

def visualize_graph(G, drug_name=None):

    if G is None or len(G.nodes) == 0:
        print("No graph to visualize")
        return

    if drug_name:
        if drug_name not in G:
            print(f"Drug '{drug_name}' not found")
            return

        nodes = list(G.neighbors(drug_name)) + [drug_name]
        G = G.subgraph(nodes)

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(12, 8))
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_color="lightblue",
        node_size=800,
        font_size=8
    )

    title = "Drug Interaction Network"
    if drug_name:
        title += f" - {drug_name}"

    plt.title(title)
    plt.show()