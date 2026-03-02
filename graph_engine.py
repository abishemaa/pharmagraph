# NetworkX logic
import networkx as nx
import matplotlib.pyplot as plt
from models import list_drugs, get_interactions

def build_graph():
    G = nx.Graph()

    # Add all drugs as nodes
    for drug in list_drugs():
        G.add_node(drug)

    # Add edges from interactions
    for drug in list_drugs():
        interactions = get_interactions(drug)
        for item in interactions:
            other = item['drug']
            severity = item['severity']
            mechanism = item['mechanism']

            # Avoid duplicate edges (undirected)
            if not G.has_edge(drug, other):
                # Store severity and mechanism as edge attributes
                G.add_edge(drug, other, severity=severity, mechanism=mechanism)

    return G

def visualize_graph():
    G = build_graph()

    # Position nodes nicely
    pos = nx.spring_layout(G, seed=42)

    # Edge colors by severity
    edge_colors = []
    for u, v, data in G.edges(data=True):
        if data['severity'] == 'severe':
            edge_colors.append('red')
        elif data['severity'] == 'moderate':
            edge_colors.append('orange')
        else:
            edge_colors.append('green')

    edge_widths = []
    for u, v, data in G.edges(data=True):
        if data['severity'] == 'severe':
            edge_widths.append(4)    # thickest
        elif data['severity'] == 'moderate':
            edge_widths.append(2.5)
        else:
            edge_widths.append(1.5)  # mild, thinnest

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=800)

    # Draw edges with varying widths
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Optional: add a legend
    import matplotlib.patches as mpatches
    red_patch = mpatches.Patch(color='red', label='Severe')
    orange_patch = mpatches.Patch(color='orange', label='Moderate')
    green_patch = mpatches.Patch(color='green', label='Mild')
    plt.legend(handles=[red_patch, orange_patch, green_patch])

    plt.title("PharmaGraph v1 - Drug Interactions")
    plt.axis('off')
    plt.show()