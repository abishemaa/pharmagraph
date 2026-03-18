# interface/cli.py
"""
PharmaGraph CLI - Interface to the engine
No graph logic, just input/output
"""
import sys
import os

# Add parent directory to path so we can import core
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import engine
from visualize import plot

def print_header(text):
    """Print a section header"""
    print(f"\n{'='*60}")
    print(text)
    print('='*60)

def cmd_drug(name):
    """Handle drug lookup command"""
    drug = engine.lookup_drug(name)
    if not drug:
        print(f"Error: Drug not found: {name}")
        return
    
    summary = engine.get_drug_summary(drug)
    if not summary:
        print(f"Error: Could not get data for {drug}")
        return
    
    print_header(f"DRUG: {drug}")
    
    print("\nNetwork Centrality:")
    print(f"  Degree: {summary['degree_centrality']:.3f} (connectedness)")
    print(f"  Betweenness: {summary['betweenness_centrality']:.3f} (bridge potential)")
    
    print("\nInteractions:")
    
    has_interactions = False
    for severity in engine.SEVERITY_ORDER:
        interactions = summary['interactions'][severity]
        if interactions:
            has_interactions = True
            print(f"\n[{severity}]")
            
            for inter in interactions:
                print(f"\n  - {inter['drug']}")
                if inter['mechanism'] != "N/A":
                    print(f"    Mechanism: {inter['mechanism']}")
                if inter['effect'] != "N/A":
                    print(f"    Effect: {inter['effect']}")
                if inter['management'] != "N/A":
                    print(f"    Management: {inter['management']}")
    
    if not has_interactions:
        print("  No interactions found")

def cmd_all():
    """List all drugs"""
    drugs = engine.get_all_drugs()
    if not drugs:
        print("Error: No drugs loaded")
        return
    
    print("\nDrugs in network:")
    for drug, centrality in drugs:
        print(f"  {drug} (centrality: {centrality:.3f})")
    print()

def cmd_stats():
    """Show network statistics"""
    stats = engine.get_network_stats()
    if not stats:
        print("Error: Could not get network stats")
        return
    
    print_header("NETWORK SUMMARY")
    
    print(f"\nOverview:")
    print(f"  Total Drugs: {stats['total_drugs']}")
    print(f"  Total Interactions: {stats['total_interactions']}")
    print(f"  Network Density: {stats['density']:.3f}")
    
    print(f"\nTop 5 Most Connected Drugs:")
    for drug, degree in stats['top_degree']:
        print(f"  {drug}: {degree:.3f}")
    
    if stats['top_betweenness']:
        print(f"\nTop 5 Bridge Drugs:")
        for drug, betweenness in stats['top_betweenness']:
            print(f"  {drug}: {betweenness:.3f}")
    
    print(f"\nSeverity Distribution:")
    for sev, count in stats['severity_distribution'].items():
        if count > 0:
            print(f"  {sev}: {count}")
    
    most, most_count = stats['most_connected']
    least, least_count = stats['most_isolated']
    print(f"\nMost Connected: {most} ({most_count} interactions)")
    print(f"Most Isolated: {least} ({least_count} interactions)")

def cmd_explain(d1, d2):
    """Explain interaction between two drugs"""
    drug1 = engine.lookup_drug(d1)
    drug2 = engine.lookup_drug(d2)
    
    if not drug1:
        print(f"Error: Drug not found: {d1}")
        return
    if not drug2:
        print(f"Error: Drug not found: {d2}")
        return
    
    inter = engine.get_interaction(drug1, drug2)
    if not inter:
        print(f"\nNo direct interaction found between {drug1} and {drug2}")
        return
    
    print_header(f"INTERACTION: {drug1} <-> {drug2}")
    
    print(f"\nSeverity: {inter['severity']}")
    
    if inter['mechanism'] != "N/A":
        print(f"\nMechanism:")
        print(f"  {inter['mechanism']}")
    
    if inter['effect'] != "N/A":
        print(f"\nClinical Effect:")
        print(f"  {inter['effect']}")
    
    if inter['management'] != "N/A":
        print(f"\nManagement:")
        print(f"  {inter['management']}")

def cmd_path(d1, d2):
    """Find path between two drugs"""
    drug1 = engine.lookup_drug(d1)
    drug2 = engine.lookup_drug(d2)
    
    if not drug1:
        print(f"Error: Drug not found: {d1}")
        return
    if not drug2:
        print(f"Error: Drug not found: {d2}")
        return
    
    result = engine.find_path(drug1, drug2)
    
    if not result:
        print(f"Error: Could not find path")
        return
    
    if result.get("error") == "no_path":
        print(f"\nNo path found between {drug1} and {drug2}")
        return
    
    print_header(f"PATH: {drug1} -> {drug2}")
    print(f"\nPath found ({len(result['path'])-1} steps):")
    
    for i, step in enumerate(result['steps'], 1):
        print(f"\n  {i}. {step['from']} -> {step['to']}")
        print(f"     Severity: {step['severity']}")
        if step['mechanism'] and step['mechanism'] != "Unknown mechanism":
            short = step['mechanism'][:60] + "..." if len(step['mechanism']) > 60 else step['mechanism']
            print(f"     Mechanism: {short}")
    
    if result['high_risk_count'] > 0:
        print(f"\nWarning: Path contains {result['high_risk_count']} high-risk interaction(s)")

def run_cli():
    """Main CLI loop"""
    print("\nPharmaGraph - Drug Interaction Network Analysis")
    print("="*60)
    print("Initializing engine...")
    
    if not engine.init():
        print("Error: Could not initialize engine. Check data files.")
        return
    
    graph = engine.get_graph()
    print(f"Loaded {len(graph.nodes)} drugs with {len(graph.edges)} interactions\n")
    
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
                cmd_all()
                
            elif cmd == "stats":
                cmd_stats()
                
            elif cmd == "graph":
                plot.visualize_graph(graph)
                
            elif cmd.startswith("graph "):
                drug_name = cmd[6:]
                drug = engine.lookup_drug(drug_name)
                if drug:
                    plot.visualize_graph(graph, drug)
                else:
                    print(f"Error: Drug not found: {drug_name}")
                    
            elif cmd.startswith("explain "):
                parts = cmd.split()
                if len(parts) == 3:
                    _, d1, d2 = parts
                    cmd_explain(d1, d2)
                else:
                    print("Usage: explain <drug1> <drug2>")
                    
            elif cmd.startswith("path "):
                parts = cmd.split()
                if len(parts) == 3:
                    _, d1, d2 = parts
                    cmd_path(d1, d2)
                else:
                    print("Usage: path <drug1> <drug2>")
                    
            else:
                # Assume it's a drug name
                cmd_drug(cmd)
                    
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_cli()