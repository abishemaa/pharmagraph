# cli.py
from graph.builder import build_graph
from graph.analyzer import enrich_graph_with_metrics
from graph.visualizer import visualize_graph

def run_cli():

    print("PharmaGraph CLI")
    print("Commands: <drug> | all | graph | graph <drug> | exit\n")

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

            visualize_graph(G)

        elif cmd.startswith("graph "):

            drug_name = cmd[6:]
            drug = drug_lookup.get(drug_name)

            if drug:
                visualize_graph(G, drug)
            else:
                print(f"Drug not found: {drug_name}")

        elif cmd in drug_lookup:

            drug = drug_lookup[cmd]

            print(f"\nDrug: {drug}")
            print("Interactions:")

            for neighbor in G.neighbors(drug):
                edge = G[drug][neighbor]
                severity = edge.get("weight", "unknown")
                print(f"  - {neighbor}: {severity}")

            print()

        else:
            print(f"Unknown command or drug: {cmd}")


if __name__ == "__main__":
    run_cli()