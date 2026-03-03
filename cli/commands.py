from core.interaction_service import InteractionService
from graph.graph_builder import GraphBuilder
import matplotlib.pyplot as plt
import networkx as nx

svc = InteractionService()
builder = GraphBuilder()

def list_drugs():
    drugs = svc.get_all_drugs()
    for d in drugs:
        print(f"- {d}")

def show_interactions(drug_name):
    interactions = svc.get_interactions(drug_name)
    if not interactions:
        print(f"No interactions found for {drug_name}")
        return

    for inter in interactions:
        print(f"{inter['drug']} → {inter['mechanism']} (Severity: {inter['severity']})")

def visualize_interactions(drug_name):
    interactions = svc.get_interactions(drug_name)
    if not interactions:
        print(f"No interactions to visualize for {drug_name}")
        return

    G = builder.build_from_interactions(interactions)
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', font_size=10)
    plt.show()