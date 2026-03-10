# visualizer.py
import networkx as nx
import matplotlib.pyplot as plt
from graph.builder import build_graph

def visualize_graph(drug_name=None):
    G = build_graph(drug_name)

    if G is None:
        print("No graph to visualize")
        return

    # Create a copy without weights for layout
    G_unweighted = nx.DiGraph()
    G_unweighted.add_nodes_from(G.nodes())
    G_unweighted.add_edges_from(G.edges())
    
    # Use unweighted layout
    pos = nx.spring_layout(G_unweighted, seed=42)
    
    plt.figure(figsize=(12, 8))
    nx.draw(G_unweighted, pos, with_labels=True, node_color='lightblue', 
            node_size=800, font_size=8, arrows=True)
    plt.title(f"Drug Interaction Network{f' - {drug_name}' if drug_name else ''}")
    plt.show()