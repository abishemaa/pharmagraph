import networkx as nx
from models import get_interactions, get_drug_class


def build_graph():
    G = nx.Graph()

    interactions = get_interactions()

    for drug_a, drug_b, severity, mechanism in interactions:
        G.add_node(drug_a, drug_class=get_drug_class(drug_a))
        G.add_node(drug_b, drug_class=get_drug_class(drug_b))

        G.add_edge(
            drug_a,
            drug_b,
            severity=severity,
            mechanism=mechanism
        )

    return G