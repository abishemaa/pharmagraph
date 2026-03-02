
import networkx as nx
import matplotlib.pyplot as plt
from models import list_drugs, get_interactions, get_drug_class

def build_graph():
    G = nx.Graph()

    # Add all drugs as nodes with class info
    for drug in list_drugs():
        drug_class = get_drug_class(drug)  # function to fetch drug_class from DB
        G.add_node(drug, drug_class=drug_class)

    # Add edges from interactions
    for drug in list_drugs():
        interactions = get_interactions(drug)
        for item in interactions:
            other = item['drug']
            severity = item['severity']
            mechanism = item['mechanism']

            if not G.has_edge(drug, other):
                # Store severity and mechanism as edge attributes
                G.add_edge(drug, other, severity=severity, mechanism=mechanism)

    return G

def visualize_graph():
    G = build_graph()

    # Use spring layout for spacing
    pos = nx.spring_layout(G, k=1, seed=42)

    # Node colors by drug class
    class_colors = {}
    color_map = ['lightblue', 'lightgreen', 'orange', 'pink', 'yellow', 'violet']
    all_classes = list({G.nodes[n]['drug_class'] for n in G.nodes})
    for i, cls in enumerate(all_classes):
        class_colors[cls] = color_map[i % len(color_map)]

    node_colors = [class_colors[G.nodes[n]['drug_class']] for n in G.nodes]

    # Node size by number of interactions (degree)
    node_sizes = [300 + 150*G.degree(n) for n in G.nodes]

    # Edge colors and widths by severity
    edge_colors = []
    edge_widths = []
    for u, v, data in G.edges(data=True):
        if data['severity'] == 'severe':
            edge_colors.append('red')
            edge_widths.append(4)
        elif data['severity'] == 'moderate':
            edge_colors.append('orange')
            edge_widths.append(2.5)
        else:
            edge_colors.append('green')
            edge_widths.append(1.5)

    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=node_sizes)

    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths)

    # Draw labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')

    # Legend for severity
    import matplotlib.patches as mpatches
    red_patch = mpatches.Patch(color='red', label='Severe')
    orange_patch = mpatches.Patch(color='orange', label='Moderate')
    green_patch = mpatches.Patch(color='green', label='Mild')
    plt.legend(handles=[red_patch, orange_patch, green_patch], loc='upper right')

    plt.title("PharmaGraph v1 - Drug Interactions")
    plt.axis('off')
    plt.show()