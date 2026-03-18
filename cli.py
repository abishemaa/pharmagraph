# cli.py - KISS version (clean, readable, no distractions)
import sys
import networkx as nx
from graph.builder import build_graph
from graph.analyzer import enrich_graph_with_metrics
from graph.visualizer import visualize_graph

# Severity ordering for consistent sorting
SEVERITY_ORDER = ["Contraindicated", "Major", "Moderate", "Minor"]

def display_network_summary(G):
    """Display global network statistics"""
    total_drugs = G.number_of_nodes()
    total_interactions = G.number_of_edges()
    density = nx.density(G)
    
    # Degree centrality
    degree_centrality = nx.degree_centrality(G)
    top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)
    
    # Betweenness centrality
    try:
        betweenness_centrality = nx.betweenness_centrality(G)
        top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)
    except:
        top_betweenness = []
        print("[Warning] Betweenness centrality calculation failed")
    
    # Severity distribution
    severity_counts = {sev: 0 for sev in SEVERITY_ORDER}
    for u, v, data in G.edges(data=True):
        sev = data.get('severity_text', 'Unknown')
        if sev in severity_counts:
            severity_counts[sev] += 1
    
    print("\n" + "="*60)
    print("NETWORK SUMMARY")
    print("="*60)
    print(f"\nOverview:")
    print(f"  Total Drugs: {total_drugs}")
    print(f"  Total Interactions: {total_interactions}")
    print(f"  Network Density: {density:.3f}")
    
    print(f"\nTop 5 Most Connected Drugs (by degree):")
    for drug, degree in top_degree[:5]:
        print(f"  {drug}: {degree:.3f}")
    
    if top_betweenness:
        print(f"\nTop 5 Bridge Drugs (by betweenness):")
        for drug, betweenness in top_betweenness[:5]:
            print(f"  {drug}: {betweenness:.3f}")
    
    print(f"\nSeverity Distribution:")
    for sev, count in severity_counts.items():
        if count > 0:
            print(f"  {sev}: {count}")
    
    # Most and least connected
    if G.nodes():
        most_connected = max(G.nodes(), key=lambda n: G.degree(n))
        least_connected = min(G.nodes(), key=lambda n: G.degree(n))
        print(f"\nMost Connected: {most_connected} ({G.degree(most_connected)} interactions)")
        print(f"Most Isolated: {least_connected} ({G.degree(least_connected)} interactions)")

def display_drug_info(G, drug):
    """Display drug details with interactions"""
    print("\n" + "="*60)
    print(f"DRUG: {drug}")
    print("="*60)
    
    # Display centrality metrics
    print("\nNetwork Centrality:")
    degree = G.nodes[drug].get("degree_centrality", 0)
    betweenness = G.nodes[drug].get("betweenness_centrality", 0)
    print(f"  Degree: {degree:.3f} (connectedness)")
    print(f"  Betweenness: {betweenness:.3f} (bridge potential)")
    
    # Group interactions by severity
    grouped = {sev: [] for sev in SEVERITY_ORDER}
    
    for neighbor in G.neighbors(drug):
        edge = G[drug][neighbor]
        
        severity = edge.get("severity_text", "Unknown")
        mechanism = edge.get("mechanism", "N/A")
        effect = edge.get("clinical_effect", "N/A")
        management = edge.get("management", "N/A")
        
        if severity in grouped:
            grouped[severity].append((neighbor, mechanism, effect, management))
    
    # Display grouped interactions
    print("\nInteractions:")
    
    has_interactions = False
    for sev in SEVERITY_ORDER:
        if grouped[sev]:
            has_interactions = True
            print(f"\n[{sev}]")
            
            for n, mech, eff, mgmt in sorted(grouped[sev], key=lambda x: x[0]):
                print(f"\n  - {n}")
                if mech != "N/A" and mech != "Unknown mechanism":
                    print(f"    Mechanism: {mech}")
                if eff != "N/A" and eff != "Unknown effect":
                    print(f"    Effect: {eff}")
                if mgmt != "N/A" and mgmt != "Unknown management":
                    print(f"    Management: {mgmt}")
    
    if not has_interactions:
        print("  No interactions found")

def explain_interaction(G, d1, d2):
    """Explain a specific drug-drug interaction"""
    # Check if drugs exist
    if d1 not in G:
        print(f"Error: Drug not found: {d1}")
        return
    if d2 not in G:
        print(f"Error: Drug not found: {d2}")
        return
    
    # Check if interaction exists
    if not G.has_edge(d1, d2):
        print(f"\nNo direct interaction found between {d1} and {d2}")
        return
    
    edge = G[d1][d2]
    
    print("\n" + "="*60)
    print(f"INTERACTION: {d1} <-> {d2}")
    print("="*60 + "\n")
    
    severity = edge.get('severity_text', 'Unknown')
    print(f"Severity: {severity}")
    
    mechanism = edge.get('mechanism', 'N/A')
    if mechanism != 'N/A' and mechanism != 'Unknown mechanism':
        print(f"\nMechanism:")
        print(f"  {mechanism}")
    
    effect = edge.get('clinical_effect', 'N/A')
    if effect != 'N/A' and effect != 'Unknown effect':
        print(f"\nClinical Effect:")
        print(f"  {effect}")
    
    management = edge.get('management', 'N/A')
    if management != 'N/A' and management != 'Unknown management':
        print(f"\nManagement:")
        print(f"  {management}")

def find_path(G, drug1, drug2):
    """Find and analyze path between two drugs"""
    try:
        if drug1 not in G:
            print(f"Error: Drug not found: {drug1}")
            return
        if drug2 not in G:
            print(f"Error: Drug not found: {drug2}")
            return
            
        path = nx.shortest_path(G, drug1, drug2)
        
        print("\n" + "="*60)
        print(f"PATH: {drug1} -> {drug2}")
        print("="*60)
        
        print(f"\nPath found ({len(path)-1} steps):")
        
        high_risk_edges = 0
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            edge = G[u][v]
            severity = edge.get('severity_text', 'Unknown')
            
            if severity in ["Contraindicated", "Major"]:
                high_risk_edges += 1
            
            print(f"\n  {i+1}. {u} -> {v}")
            print(f"     Severity: {severity}")
            
            # Show mechanism briefly
            mechanism = edge.get('mechanism', '')
            if mechanism and mechanism != 'Unknown mechanism':
                short_mech = mechanism[:60] + "..." if len(mechanism) > 60 else mechanism
                print(f"     Mechanism: {short_mech}")
        
        if high_risk_edges > 0:
            print(f"\nWarning: Path contains {high_risk_edges} high-risk interaction(s)")
        
    except nx.NetworkXNoPath:
        print(f"\nNo path found between {drug1} and {drug2}")

def run_cli():
    print("\nPharmaGraph - Drug Interaction Network Analysis")
    print("="*60)
    print("Loading network...")
    
    G = build_graph()
    if G is None or len(G.nodes) == 0:
        print("Error: No data loaded. Please check database.")
        return
        
    G = enrich_graph_with_metrics(G)
    drug_lookup = {node.lower(): node for node in G.nodes()}
    
    print(f"Loaded {len(G.nodes)} drugs with {len(G.edges)} interactions\n")
    print("Commands:")
    print("  <drug>              - Show drug details and interactions")
    print("  all                 - List all drugs")
    print("  stats               - Show network statistics")
    print("  graph               - Visualize full network")
    print("  graph <drug>        - Visualize drug subgraph")
    print("  explain <d1> <d2>   - Explain interaction between two drugs")
    print("  path <d1> <d2>      - Find path between drugs")
    print("  exit                - Exit program\n")

    while True:
        try:
            cmd = input("> ").strip().lower()
            
            if not cmd:
                continue
                
            if cmd == "exit":
                print("\nGoodbye!")
                break
                
            elif cmd == "all":
                print("\nDrugs in network:")
                for node in sorted(G.nodes()):
                    degree = G.nodes[node].get("degree_centrality", 0)
                    print(f"  {node} (centrality: {degree:.3f})")
                print()
                
            elif cmd == "stats":
                display_network_summary(G)
                
            elif cmd == "graph":
                visualize_graph(G)
                
            elif cmd.startswith("graph "):
                drug_name = cmd[6:]
                drug = drug_lookup.get(drug_name)
                
                if drug:
                    visualize_graph(G, drug)
                else:
                    print(f"Error: Drug not found: {drug_name}")
                    
            elif cmd.startswith("explain "):
                parts = cmd.split()
                if len(parts) == 3:
                    _, d1, d2 = parts
                    drug1 = drug_lookup.get(d1)
                    drug2 = drug_lookup.get(d2)
                    
                    if drug1 and drug2:
                        explain_interaction(G, drug1, drug2)
                    else:
                        if not drug1:
                            print(f"Error: Drug not found: {d1}")
                        if not drug2:
                            print(f"Error: Drug not found: {d2}")
                else:
                    print("Usage: explain <drug1> <drug2>")
                    
            elif cmd.startswith("path "):
                parts = cmd.split()
                if len(parts) == 3:
                    _, d1, d2 = parts
                    drug1 = drug_lookup.get(d1)
                    drug2 = drug_lookup.get(d2)
                    
                    if drug1 and drug2:
                        find_path(G, drug1, drug2)
                    else:
                        if not drug1:
                            print(f"Error: Drug not found: {d1}")
                        if not drug2:
                            print(f"Error: Drug not found: {d2}")
                else:
                    print("Usage: path <drug1> <drug2>")
                    
            elif cmd in drug_lookup:
                display_drug_info(G, drug_lookup[cmd])
                
            else:
                # Try fuzzy matching
                matches = [name for name in drug_lookup.keys() if cmd in name]
                if matches:
                    print(f"Did you mean: {', '.join(matches[:5])}?")
                else:
                    print(f"Unknown command or drug: {cmd}")
                    
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_cli()