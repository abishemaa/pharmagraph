# cli.py
from graph.builder import build_graph
from graph.analyzer import enrich_graph_with_metrics
from graph.visualizer import visualize_graph

def run_cli():
    print("PharmaGraph CLI")
    print("Commands: <drug> | all | graph | exit\n")

    G = build_graph()
    G = enrich_graph_with_metrics(G)
    drug_lookup = {node.lower(): node for node in G.nodes()}

    while True:
        cmd = input("> ").strip().lower()

        if cmd == "exit":
            break
        elif cmd == "all":
            print("\nDrugs in network:")
            for node in G.nodes():
                print(f"  {node}")
            print()
        elif cmd == "graph":
            visualize_graph()
        elif cmd.startswith("graph "):
            drug_name = cmd[6:]
            visualize_graph(drug_name)
        elif cmd in drug_lookup:
            drug = drug_lookup[cmd]
            print(f"\nDrug: {drug}")
            # Show interactions
            for successor in G.successors(drug):
                edge = G[drug][successor]
                print(f"  → {successor}: {edge.get('weight')}")
            for predecessor in G.predecessors(drug):
                edge = G[predecessor][drug]
                print(f"  ← {predecessor}: {edge.get('weight')}")
            print()
        else:
            print(f"Unknown command or drug: {cmd}")

if __name__ == "__main__":
    run_cli()