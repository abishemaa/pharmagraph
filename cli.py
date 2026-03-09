from tabulate import tabulate
from graph.builder import build_graph
from graph.analyzer import enrich_graph_with_metrics
from graph.visualizer import visualize_graph


def print_drug_info(G, drug_lookup, user_input):
    key = drug_lookup.get(user_input.lower())

    if not key:
        print(f"\nDrug '{user_input}' not found.\n")
        return

    node = G.nodes[key]

    print(f"\nDrug: {key}")
    print(f"Degree Centrality: {node.get('degree_centrality', 0):.3f}")
    print(f"Betweenness Centrality: {node.get('betweenness_centrality', 0):.3f}")

    rows = []

    for target in G.successors(key):
        edge = G[key][target]
        rows.append([
            target,
            "outgoing",
            edge.get("weight"),
            edge.get("mechanism")
        ])

    for source in G.predecessors(key):
        edge = G[source][key]
        rows.append([
            source,
            "incoming",
            edge.get("weight"),
            edge.get("mechanism")
        ])

    if rows:
        print("\nInteractions:")
        print(tabulate(
            rows,
            headers=["Drug", "Direction", "Severity", "Mechanism"],
            tablefmt="grid"
        ))
    else:
        print("\nNo interactions found.")


def print_all_drugs(G):
    rows = []

    for node in G.nodes():
        data = G.nodes[node]
        rows.append([
            node,
            f"{data.get('degree_centrality', 0):.3f}",
            f"{data.get('betweenness_centrality', 0):.3f}",
            G.degree(node)
        ])

    print("\nAll Drugs:")
    print(tabulate(
        rows,
        headers=["Drug", "Degree Centrality", "Betweenness", "Total Connections"],
        tablefmt="grid"
    ))


def run_cli():
    print("PharmaGraph CLI")
    print("Commands:")
    print("  <drug name>       → show drug info")
    print("  all               → list all drugs")
    print("  graph             → show full network graph")
    print("  graph <drug>      → show graph for specific drug")
    print("  exit              → quit\n")

    G = build_graph()
    enrich_graph_with_metrics(G)

    drug_lookup = {node.lower(): node for node in G.nodes()}

    while True:
        cmd = input("Enter command > ").strip()

        if not cmd:
            print("Please enter a valid command.")
            continue

        lower_cmd = cmd.lower()

        if lower_cmd == "exit":
            break

        elif lower_cmd == "all":
            print_all_drugs(G)

        elif lower_cmd == "graph":
            visualize_graph()

        elif lower_cmd.startswith("graph "):
            drug_name = cmd[6:].strip()
            key = drug_lookup.get(drug_name.lower())

            if not key:
                print(f"\nDrug '{drug_name}' not found.\n")
            else:
                visualize_graph(key)

        else:
            print_drug_info(G, drug_lookup, cmd)


if __name__ == "__main__":
    run_cli()