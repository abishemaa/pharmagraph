import networkx as nx
import matplotlib.pyplot as plt
import mplcursors
from models import get_interactions, get_drug_class

def visualize_graph(drug_name=None):
    G = nx.Graph()
    interactions = get_interactions(drug_name)

    if not interactions:
        print("No interactions found for", drug_name or "all drugs")
        return

    # Build graph
    for inter in interactions:
        d1, d2 = inter['drug1'], inter['drug2']
        class1, class2 = get_drug_class(d1), get_drug_class(d2)
        G.add_node(d1, drug_class=class1)
        G.add_node(d2, drug_class=class2)
        G.add_edge(d1, d2,
                   weight=inter['severity'],
                   mechanism=inter['mechanism'])

    # Node colors by class
    classes = list(set(nx.get_node_attributes(G, 'drug_class').values()))
    color_dict = {cls: plt.cm.tab20(i/len(classes)) for i, cls in enumerate(classes)}
    node_colors = [color_dict[G.nodes[n]['drug_class']] for n in G.nodes()]

    # Edge colors/widths
    edge_colors = ['red' if G[u][v]['mechanism']=='pharmacodynamic'
                   else 'blue' if G[u][v]['mechanism']=='pharmacokinetic'
                   else 'gray' for u,v in G.edges()]
    edge_widths = [G[u][v]['weight'] for u,v in G.edges()]

    pos = nx.spring_layout(G)  # random layout
    fig, ax = plt.subplots(figsize=(12, 8))

    nodes = nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=600, ax=ax)
    edges = nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold', ax=ax)

    plt.title(f"Drug Interaction Network{' for ' + drug_name if drug_name else ''}")
    plt.axis('off')

    # Add hover info for nodes
    cursor = mplcursors.cursor(nodes, hover=True)
    @cursor.connect("add")
    def on_add(sel):
        node = list(G.nodes())[sel.index]
        sel.annotation.set(text=f"{node}\nClass: {G.nodes[node]['drug_class']}")

    # Add hover info for edges
    cursor_edges = mplcursors.cursor(edges, hover=True)
    @cursor_edges.connect("add")
    def on_edge(sel):
        line = sel.artist
        ind = sel.index
        u, v = list(G.edges())[ind]
        mech = G[u][v]['mechanism']
        sev = G[u][v]['weight']
        sel.annotation.set(text=f"{u} ↔ {v}\nSeverity: {sev}\nMechanism: {mech}")

    plt.show()