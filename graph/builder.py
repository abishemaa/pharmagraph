# builder.py
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

    severity_map = {
    "minor": 1,
    "moderate": 2,
    "major": 3,
    "contraindicated": 4
    }

    for inter in interactions:
        d1 = inter.get("drug1")
        d2 = inter.get("drug2")

        if not d1 or not d2:
            continue

        G.add_node(d1, drug_class=get_class_cached(d1))
        G.add_node(d2, drug_class=get_class_cached(d2))

        severity = inter["severity"].strip().lower()

        G.add_edge(
            d1,
            d2,
            weight=severity_map.get(severity, 1),
            severity=severity,
            mechanism=inter.get("mechanism"),
            clinical_effect=inter.get("clinical_effect"),
            evidence=inter.get("evidence"),
            management=inter.get("management")
        )

    return G

drug_cache = {}

def get_class_cached(drug):
    if drug not in drug_cache:
        drug_cache[drug] = get_drug_class(drug)
    return drug_cache[drug]