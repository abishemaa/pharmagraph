# core/engine.py
"""
PharmaGraph Core Engine
- All graph logic in one place
- Loads from JSON files
"""
import json
import os
import networkx as nx

# Global graph instance (loaded once)
_graph = None
_drug_lookup = None

# Severity order for consistent sorting
SEVERITY_ORDER = ["Contraindicated", "Major", "Moderate", "Minor"]

def load_json_data():
    """Load drugs and interactions from JSON files"""
    # Get the project root directory
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(current_dir, 'data')
    
    # Load drugs
    drugs_file = os.path.join(data_dir, 'drugs.json')
    interactions_file = os.path.join(data_dir, 'interactions.json')
    
    # Check if files exist
    if not os.path.exists(drugs_file):
        print(f"Error: {drugs_file} not found")
        return None, None
    
    if not os.path.exists(interactions_file):
        print(f"Error: {interactions_file} not found")
        return None, None
    
    # Load JSON data
    with open(drugs_file, 'r') as f:
        drugs = json.load(f)
    
    with open(interactions_file, 'r') as f:
        interactions = json.load(f)
    
    return drugs, interactions

def build_graph_from_json():
    """Build NetworkX graph from JSON data"""
    drugs, interactions = load_json_data()
    if not drugs or not interactions:
        return None
    
    G = nx.Graph()
    
    # Add drug nodes
    for drug in drugs:
        G.add_node(
            drug['name'],
            drug_class=drug.get('class', 'Unknown'),
            mechanism=drug.get('mechanism', 'Unknown')
        )
    
    # Add interaction edges
    severity_map = {
        "minor": 1,
        "moderate": 2,
        "major": 3,
        "contraindicated": 4
    }
    
    for inter in interactions:
        d1 = inter['drug1']
        d2 = inter['drug2']
        
        # Only add if both drugs exist
        if d1 in G and d2 in G:
            severity_raw = inter.get('severity', 'unknown')
            severity_lower = severity_raw.lower()
            weight = severity_map.get(severity_lower, 0)
            
            G.add_edge(
                d1,
                d2,
                weight=weight,
                severity_text=inter.get('severity', 'Unknown'),
                mechanism=inter.get('mechanism', 'N/A'),
                clinical_effect=inter.get('clinical_effect', 'N/A'),
                management=inter.get('management', 'N/A')
            )
    
    return G

def enrich_graph_with_metrics(G):
    """Add essential network metrics to graph"""
    if G is None or len(G.nodes) == 0:
        return G
    
    # Core centrality metrics
    degree = nx.degree_centrality(G)
    
    try:
        betweenness = nx.betweenness_centrality(G)
    except:
        betweenness = {node: 0 for node in G.nodes()}
        print("[Warning] Betweenness centrality calculation failed")
    
    for node in G.nodes():
        G.nodes[node]["degree_centrality"] = degree[node]
        G.nodes[node]["betweenness_centrality"] = betweenness.get(node, 0)
        G.nodes[node]["degree"] = G.degree(node)
    
    return G

def init():
    """Initialize the engine - load and enrich graph"""
    global _graph, _drug_lookup
    if _graph is None:
        _graph = build_graph_from_json()
        if _graph and len(_graph.nodes) > 0:
            _graph = enrich_graph_with_metrics(_graph)
            _drug_lookup = {node.lower(): node for node in _graph.nodes()}
    return _graph is not None

def get_graph():
    """Get the graph instance (for visualizer)"""
    return _graph

def lookup_drug(name):
    """Find drug by case-insensitive name"""
    if not _drug_lookup:
        return None
    return _drug_lookup.get(name.lower())

def get_all_drugs():
    """Return list of all drugs with basic info"""
    if not _graph:
        return []
    return sorted([(node, _graph.nodes[node].get("degree_centrality", 0)) 
                   for node in _graph.nodes()], key=lambda x: x[0])

def get_drug_summary(drug):
    """Get complete drug summary with interactions"""
    if not _graph or drug not in _graph:
        return None
    
    # Group interactions by severity
    interactions = {sev: [] for sev in SEVERITY_ORDER}
    
    for neighbor in _graph.neighbors(drug):
        edge = _graph[drug][neighbor]
        severity = edge.get("severity_text", "Unknown")
        
        if severity in interactions:
            interactions[severity].append({
                "drug": neighbor,
                "mechanism": edge.get("mechanism", "N/A"),
                "effect": edge.get("clinical_effect", "N/A"),
                "management": edge.get("management", "N/A")
            })
    
    # Sort interactions within each severity
    for sev in interactions:
        interactions[sev].sort(key=lambda x: x["drug"])
    
    return {
        "drug": drug,
        "degree_centrality": _graph.nodes[drug].get("degree_centrality", 0),
        "betweenness_centrality": _graph.nodes[drug].get("betweenness_centrality", 0),
        "degree": _graph.degree(drug),
        "interactions": interactions
    }

def get_interaction(d1, d2):
    """Get details of interaction between two drugs"""
    if not _graph or d1 not in _graph or d2 not in _graph:
        return None
    
    if not _graph.has_edge(d1, d2):
        return None
    
    edge = _graph[d1][d2]
    return {
        "drug1": d1,
        "drug2": d2,
        "severity": edge.get("severity_text", "Unknown"),
        "mechanism": edge.get("mechanism", "N/A"),
        "effect": edge.get("clinical_effect", "N/A"),
        "management": edge.get("management", "N/A")
    }

def get_network_stats():
    """Get global network statistics"""
    if not _graph:
        return None
    
    total_drugs = _graph.number_of_nodes()
    total_interactions = _graph.number_of_edges()
    
    # Degree centrality
    degree_centrality = nx.degree_centrality(_graph)
    top_degree = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Betweenness centrality
    try:
        betweenness_centrality = nx.betweenness_centrality(_graph)
        top_betweenness = sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    except:
        top_betweenness = []
    
    # Severity distribution
    severity_counts = {sev: 0 for sev in SEVERITY_ORDER}
    for u, v, data in _graph.edges(data=True):
        sev = data.get('severity_text', 'Unknown')
        if sev in severity_counts:
            severity_counts[sev] += 1
    
    # Most/least connected
    most_connected = max(_graph.nodes(), key=lambda n: _graph.degree(n))
    least_connected = min(_graph.nodes(), key=lambda n: _graph.degree(n))
    
    return {
        "total_drugs": total_drugs,
        "total_interactions": total_interactions,
        "density": nx.density(_graph),
        "top_degree": top_degree[:5],
        "top_betweenness": top_betweenness[:5] if top_betweenness else [],
        "severity_distribution": severity_counts,
        "most_connected": (most_connected, _graph.degree(most_connected)),
        "most_isolated": (least_connected, _graph.degree(least_connected))
    }

def find_path(d1, d2):
    """Find shortest path between two drugs"""
    if not _graph or d1 not in _graph or d2 not in _graph:
        return None
    
    try:
        path = nx.shortest_path(_graph, d1, d2)
        
        # Enrich path with interaction details
        path_details = []
        high_risk_count = 0
        
        for i in range(len(path)-1):
            u, v = path[i], path[i+1]
            edge = _graph[u][v]
            severity = edge.get('severity_text', 'Unknown')
            
            if severity in ["Contraindicated", "Major"]:
                high_risk_count += 1
            
            path_details.append({
                "from": u,
                "to": v,
                "severity": severity,
                "mechanism": edge.get('mechanism', '')
            })
        
        return {
            "path": path,
            "steps": path_details,
            "high_risk_count": high_risk_count
        }
    except nx.NetworkXNoPath:
        return {"error": "no_path"}
    except:
        return {"error": "unknown"}