# visualizer.py - KISS version (clean, readable)
import networkx as nx
import matplotlib.pyplot as plt

SEVERITY_COLORS = {
    "Contraindicated": "red",
    "Major": "orange",
    "Moderate": "gold",
    "Minor": "lightgreen",
    "Unknown": "gray"
}

def get_edge_color(severity_text):
    """Map severity text to edge color"""
    return SEVERITY_COLORS.get(severity_text, "gray")

def visualize_graph(G, drug_name=None):
    """
    Visualize drug interaction network.
    For subgraphs, show mechanism labels. For full graph, keep clean.
    """
    if G is None or len(G.nodes) == 0:
        print("Error: No graph to visualize")
        return

    # Create subgraph if drug specified
    is_subgraph = drug_name is not None
    
    if is_subgraph:
        if drug_name not in G:
            print(f"Error: Drug '{drug_name}' not found")
            return
        
        # Get all neighbors
        nodes = list(G.neighbors(drug_name)) + [drug_name]
        G = G.subgraph(nodes)
        print(f"Showing {len(nodes)-1} interactions for {drug_name}")

    if len(G.nodes) == 0:
        print("Error: No nodes to visualize")
        return

    # Calculate layout
    pos = nx.spring_layout(G, seed=42, k=2, iterations=50)

    # Create figure
    plt.figure(figsize=(14, 10))
    
    # Node styling - simple and clean
    node_sizes = []
    for node in G.nodes():
        # Size based on degree (importance)
        degree = G.degree(node)
        size = 500 + 200 * degree
        node_sizes.append(size)
    
    # All nodes light blue - simple and readable
    node_colors = ["lightblue" for _ in G.nodes()]
    
    if is_subgraph and drug_name:
        # Highlight the queried drug
        node_idx = list(G.nodes()).index(drug_name)
        node_colors[node_idx] = "yellow"

    # Edge styling based on severity
    edge_colors = []
    edge_widths = []
    
    for u, v, data in G.edges(data=True):
        severity = data.get("severity_text", "Unknown")
        edge_colors.append(get_edge_color(severity))
        
        # Width based on severity
        if severity == "Contraindicated":
            width = 3.0
        elif severity == "Major":
            width = 2.5
        elif severity == "Moderate":
            width = 2.0
        elif severity == "Minor":
            width = 1.5
        else:
            width = 1.0
        edge_widths.append(width)

    # Draw nodes
    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=node_colors,
        alpha=0.8,
        edgecolors='black',
        linewidths=1
    )
    
    # Draw edges
    nx.draw_networkx_edges(
        G, pos,
        edge_color=edge_colors,
        width=edge_widths,
        alpha=0.7,
        style='solid'
    )
    
    # Draw labels
    nx.draw_networkx_labels(
        G, pos,
        font_size=9,
        font_weight='bold'
    )
    
    # Add mechanism labels ONLY for subgraph view
    if is_subgraph and len(G.edges) <= 15:
        edge_labels = {}
        for u, v, data in G.edges(data=True):
            mechanism = data.get("mechanism", "")
            if mechanism and mechanism != "Unknown mechanism":
                # Truncate long mechanisms
                short_mech = mechanism[:20] + "..." if len(mechanism) > 20 else mechanism
                edge_labels[(u, v)] = short_mech
        
        if edge_labels:
            nx.draw_networkx_edge_labels(
                G, pos,
                edge_labels=edge_labels,
                font_size=6
            )

    # Add legend for severity
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', alpha=0.7, label='Contraindicated'),
        Patch(facecolor='orange', alpha=0.7, label='Major'),
        Patch(facecolor='gold', alpha=0.7, label='Moderate'),
        Patch(facecolor='lightgreen', alpha=0.7, label='Minor'),
    ]
    plt.legend(handles=legend_elements, loc='upper right', title='Severity')

    # Title
    title = "Drug Interaction Network"
    if is_subgraph:
        title += f" - {drug_name}"
    plt.title(title, fontsize=16, fontweight='bold')
    plt.axis('off')
    
    # Stats
    stats = f"Drugs: {len(G.nodes)} | Interactions: {len(G.edges)}"
    plt.text(0.02, 0.02, stats, transform=plt.gca().transAxes,
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='gray'),
            fontsize=10)
    
    plt.tight_layout()
    plt.show()