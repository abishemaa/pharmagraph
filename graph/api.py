import networkx as nx
from .builder import build_graph


def graph_to_json(drug_name=None):
    G = build_graph(drug_name)

    if G is None:
        return {"nodes": [], "edges": []}

    nodes = []
    edges = []

    for node in G.nodes():
        nodes.append({"data": {"id": node, "label": node}})

    for u, v, data in G.edges(data=True):
        edges.append({
            "data": {
                "source": u,
                "target": v,
                "weight": data.get("weight", 1)
            }
        })

    return {"nodes": nodes, "edges": edges}