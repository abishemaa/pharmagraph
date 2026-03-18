# builder.py (fix severity mapping)
import networkx as nx
from models import get_all_interactions, get_drug_class

def build_graph(drug_name=None):
    interactions = get_all_interactions()
    
    if not interactions:
        return None

    G = nx.Graph()
    
    # Consistent severity mapping
    severity_map = {
        "minor": 1,
        "moderate": 2, 
        "major": 3,
        "contraindicated": 4
    }

    for inter in interactions:
        d1 = inter["drug1"]
        d2 = inter["drug2"]
        
        # Add nodes with basic info from full schema
        G.add_node(d1, drug_class=get_drug_class(d1))
        G.add_node(d2, drug_class=get_drug_class(d2))
        
        # Get severity and normalize to lowercase for mapping
        severity_raw = inter.get("severity", "unknown")
        if severity_raw:
            severity_lower = severity_raw.lower()
            weight = severity_map.get(severity_lower, 0)
        else:
            weight = 0
        
        # Add edges with all fields from interactions table
        G.add_edge(
            d1,
            d2,
            weight=weight,
            severity_text=severity_raw,  # Keep original text
            mechanism=inter.get("mechanism", "Unknown mechanism"),
            clinical_effect=inter.get("clinical_effect", "Unknown effect"),
            management=inter.get("management", "Unknown management")
        )

    return G