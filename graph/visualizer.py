# visualizer.py
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
from .builder import build_graph
from .analyzer import compute_metrics


def visualize_graph(drug_name=None):
    G = build_graph(drug_name)

    if G is None:
        return

    metrics = compute_metrics(G)
    degree = metrics["degree"]
    betweenness = metrics["betweenness"]

    pos = nx.spring_layout(G, seed=42)

    # ---- Node Size Based on Degree ----
    node_sizes = [
        300 + degree[n] * 2000
        for n in G.nodes()
    ]

    # ---- Node Colors (by class) ----
    classes = sorted(set(nx.get_node_attributes(G, "drug_class").values()))
    class_colors = {
        cls: plt.cm.tab20(i / len(classes))
        for i, cls in enumerate(classes)
    }

    node_colors = [
        class_colors[G.nodes[n]["drug_class"]]
        for n in G.nodes()
    ]

    # ---- Edge Styling ----
    mechanism_colors = {
        "pharmacodynamic": "red",
        "pharmacokinetic": "blue"
    }

    edge_colors = [
        mechanism_colors.get(G[u][v]["mechanism"], "gray")
        for u, v in G.edges()
    ]

    edge_widths = [
        G[u][v]["weight"]
        for u, v in G.edges()
    ]

    # ---- Draw ----
    fig, ax = plt.subplots(figsize=(12, 8))

    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=700, ax=ax)
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight="bold", ax=ax)

    # ---- Legend ----
    node_legend = [
        Patch(facecolor=color, label=cls)
        for cls, color in class_colors.items()
    ]

    edge_legend = [
        Line2D([0], [0], color=color, lw=3, label=mech)
        for mech, color in mechanism_colors.items()
    ]

        # ---- Metric Legends (Top 3) ----
    top_degree = sorted(degree.items(), key=lambda x: x[1], reverse=True)[:3]
    top_betweenness = sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:3]

    metric_legend = [
        Line2D([0], [0], color='white', label="Top Degree Centrality:")
    ]

    metric_legend += [
        Line2D([0], [0], color='white',
            label=f"{drug}: {value:.3f}")
        for drug, value in top_degree
    ]

    metric_legend += [
        Line2D([0], [0], color='white', label=" ")
    ]

    metric_legend += [
        Line2D([0], [0], color='white', label="Top Betweenness:")
    ]

    metric_legend += [
        Line2D([0], [0], color='white',
            label=f"{drug}: {value:.3f}")
        for drug, value in top_betweenness
    ]
    plt.legend(
        handles=node_legend + edge_legend + metric_legend,
        title="Legend",
        bbox_to_anchor=(1.05, 1),
        loc="upper left"
    )

    plt.title(f"Drug Interaction Network{' for ' + drug_name if drug_name else ''}")
    plt.axis("off")
    plt.tight_layout()
    plt.show()