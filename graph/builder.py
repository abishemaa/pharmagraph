import networkx as nx
from models import get_interactions, get_drug_class


def build_graph(drug_name=None):

    if drug_name:
        drug_name = drug_name.strip().lower()

    interactions = get_interactions(drug_name)

    if not interactions:
        print(f"No interactions found for {drug_name or 'all drugs'}")
        return None

    G = nx.DiGraph()

    for inter in interactions:
        d1 = inter["drug1"]
        d2 = inter["drug2"]

        G.add_node(d1, drug_class=get_drug_class(d1))
        G.add_node(d2, drug_class=get_drug_class(d2))

        G.add_edge(
            d1,
            d2,
            weight=inter["severity"],
            mechanism=inter["mechanism"]
        )

    return G