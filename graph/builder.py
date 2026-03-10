# builder.py
import networkx as nx
from models import get_all_interactions, get_drug_class

def build_graph(drug_name=None):
    interactions = get_all_interactions()
    
    if not interactions:
        return None

    G = nx.DiGraph()

    for inter in interactions:
        d1 = inter["drug1"]
        d2 = inter["drug2"]
        
        # Add nodes with basic info from full schema
        G.add_node(d1, drug_class=get_drug_class(d1))
        G.add_node(d2, drug_class=get_drug_class(d2))
        
        # Add edges with all fields from interactions table
        G.add_edge(
            d1,
            d2,
            weight=inter["severity"],
            mechanism=inter["mechanism"],
            clinical_effect=inter["clinical_effect"],
            management=inter["management"]
        )

    return G