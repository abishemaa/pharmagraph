```markdown
# PharmaGraph - Code Dissection Guide

## Table of Contents
1. [Project Overview](#project-overview)
2. [Database Layer](#database-layer)
3. [Data Models](#data-models)
4. [Data Loading](#data-loading)
5. [Graph Building](#graph-building)
6. [Graph Analysis](#graph-analysis)
7. [Visualization](#visualization)
8. [Command Line Interface](#command-line-interface)
9. [Data Flow](#data-flow)
10. [Key Concepts Explained](#key-concepts-explained)

---

## Project Overview

PharmaGraph is a drug interaction network analysis tool. It reads drug and interaction data from CSV files, stores them in SQLite, builds a graph structure, and allows you to explore relationships between drugs through a CLI.

**What it does:**
- Stores drug information (name, class, mechanism of action, metabolism)
- Stores drug-drug interactions (severity, mechanism, clinical effects)
- Builds a directed graph where drugs are nodes and interactions are edges
- Calculates network metrics (centrality)
- Visualizes the network
- Provides CLI for exploration

---

## Database Layer (`database.py`)

```python
import sqlite3

DB_FILE = "pharmagraph.db"  # SQLite database file

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # This lets us access columns by name
    return conn

def setup_database():
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Create drugs table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS drugs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,           # Drug name (unique)
        drug_class TEXT,             # e.g., Antibiotic, Antifungal
        moa TEXT,                    # Mechanism of Action
        metabolism TEXT              # How the body processes it
    );
    """)
    
    # Create interactions table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS interactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug1 TEXT,                   # First drug name
        drug2 TEXT,                   # Second drug name
        severity TEXT,                 # Major/Moderate/Minor
        mechanism TEXT,                # How they interact
        clinical_effect TEXT,          # What happens to patient
        management TEXT                 # How to handle interaction
    )
    """)
    
    conn.commit()
    conn.close()
```

**Key Points:**
- `sqlite3.Row` allows dictionary-like access: `row['column_name']`
- `IF NOT EXISTS` prevents errors if tables already exist
- `AUTOINCREMENT` automatically assigns IDs
- `UNIQUE` ensures no duplicate drug names

---

## Data Models (`models.py`)

This file handles all database operations (CRUD - Create, Read, Update, Delete).

```python
from database import get_db_connection

# CREATE operations
def add_drug(name, drug_class, moa, metabolism):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # INSERT OR IGNORE - adds only if name doesn't exist
    cur.execute("""
        INSERT OR IGNORE INTO drugs(name, drug_class, moa, metabolism)
        VALUES (?, ?, ?, ?)
        """,
        (name, drug_class, moa, metabolism)
    )
    
    conn.commit()
    conn.close()

def add_interaction(d1, d2, severity, mechanism, effect, management):
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("""
        INSERT INTO interactions
        (drug1, drug2, severity, mechanism, clinical_effect, management)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (d1, d2, severity, mechanism, effect, management))
    
    conn.commit()
    conn.close()

# READ operations
def get_all_drugs():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT name, drug_class, moa, metabolism FROM drugs")
    rows = cur.fetchall()  # Get all results
    
    conn.close()
    return [dict(row) for row in rows]  # Convert to list of dictionaries

def get_all_interactions():
    conn = get_db_connection()
    cur = conn.cursor()
    
    cur.execute("SELECT drug1, drug2, severity, mechanism, clinical_effect, management FROM interactions")
    rows = cur.fetchall()
    
    conn.close()
    return [dict(row) for row in rows]  # Convert to list of dictionaries

def get_drug_class(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT drug_class FROM drugs WHERE name=?", (name,))
    row = cursor.fetchone()  # Get single result
    
    conn.close()
    return row['drug_class'] if row else 'Unknown'
```

**Key Points:**
- `?` placeholders prevent SQL injection
- `fetchall()` gets all rows, `fetchone()` gets first row
- `dict(row)` converts SQLite Row object to Python dictionary
- Each function opens and closes its own connection (simple but not efficient for many operations)

---

## Data Loading (`loader.py`)

Reads CSV files and populates the database using the models.

```python
import csv
from models import add_drug, add_interaction

def load_data():
    # Load drugs from drugs.csv
    with open("data/drugs.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)  # Reads CSV as dictionaries
        
        for row in reader:
            add_drug(
                row["name"],        # Column name in CSV
                row["class"],        # Column name in CSV
                row["moa"],
                row["metabolism"]
            )
    
    # Load interactions from interactions.csv
    with open("data/interactions.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        
        for row in reader:
            add_interaction(
                row["drug1"],
                row["drug2"],
                row["severity"],
                row["mechanism"],
                row["clinical_effect"],
                row["management"]
            )
```

**Key Points:**
- `csv.DictReader` uses first row as column headers
- Each row becomes a dictionary with column names as keys
- `encoding="utf-8"` handles special characters

---

## Graph Building (`graph/builder.py`)

This is where we transform database records into a NetworkX graph.

```python
import networkx as nx
from models import get_all_interactions, get_drug_class

def build_graph(drug_name=None):
    # Get all interactions from database
    interactions = get_all_interactions()
    
    if drug_name and interactions:
        # Filter for specific drug if requested
        filtered_interactions = [
            inter for inter in interactions 
            if inter["drug1"] == drug_name or inter["drug2"] == drug_name
        ]
        interactions = filtered_interactions
    
    if not interactions:
        return None
    
    # Create empty directed graph
    G = nx.DiGraph()
    
    # Build the graph from interactions
    for inter in interactions:
        d1 = inter["drug1"]
        d2 = inter["drug2"]
        
        # Add nodes with drug class attribute
        G.add_node(d1, drug_class=get_drug_class(d1))
        G.add_node(d2, drug_class=get_drug_class(d2))
        
        # Add edge with all interaction data
        G.add_edge(
            d1,
            d2,
            weight=inter["severity"],
            mechanism=inter["mechanism"],
            clinical_effect=inter["clinical_effect"],
            management=inter["management"]
        )
    
    return G
```

**Key Points:**
- `nx.DiGraph()` creates a directed graph (edges have direction)
- Each drug becomes a **node** with attributes
- Each interaction becomes an **edge** with attributes
- Filtering happens at database level (we get all then filter)

---

## Graph Analysis (`graph/analyzer.py`)

Adds network metrics to the graph.

```python
import networkx as nx

def enrich_graph_with_metrics(G):
    if G is None:
        return G
    
    # Calculate centrality metrics
    degree = nx.degree_centrality(G)        # How connected is this node?
    betweenness = nx.betweenness_centrality(G)  # Is this node a bridge?
    
    # Add metrics as node attributes
    for node in G.nodes():
        G.nodes[node]["degree_centrality"] = degree[node]
        G.nodes[node]["betweenness_centrality"] = betweenness[node]
    
    return G
```

**What these metrics mean:**

| Metric | What it measures | Formula | Interpretation |
|--------|-----------------|---------|----------------|
| **Degree Centrality** | How many direct connections | (# of connections) / (max possible) | High = drug interacts with many others |
| **Betweenness Centrality** | How often node lies on shortest paths | (paths through node) / (all paths) | High = drug is a bridge between clusters |

---

## Visualization (`graph/visualizer.py`)

Creates visual representation of the graph.

```python
import networkx as nx
import matplotlib.pyplot as plt
from graph.builder import build_graph

def visualize_graph(drug_name=None):
    # Get the graph (filtered if drug_name provided)
    G = build_graph(drug_name)
    
    if G is None:
        print("No graph to visualize")
        return
    
    # Create unweighted copy for layout (avoids string weight error)
    G_unweighted = nx.DiGraph()
    G_unweighted.add_nodes_from(G.nodes())
    G_unweighted.add_edges_from(G.edges())
    
    # Calculate node positions using spring layout
    pos = nx.spring_layout(G_unweighted, seed=42)  # seed for reproducibility
    
    # Create figure
    plt.figure(figsize=(12, 8))
    
    # Draw the graph
    nx.draw(G_unweighted, pos, 
            with_labels=True,      # Show drug names
            node_color='lightblue', # Node color
            node_size=800,          # Node size
            font_size=8,            # Label size
            arrows=True)             # Show direction
    
    plt.title(f"Drug Interaction Network{f' - {drug_name}' if drug_name else ''}")
    plt.show()
```

**How Layout Works:**
- `spring_layout` simulates physics: nodes repel, edges attract
- `seed=42` ensures same layout each time (random but reproducible)
- We use unweighted copy because severity strings can't be used for physics

---

## Command Line Interface (`cli.py`)

The user interface.

```python
from graph.builder import build_graph
from graph.analyzer import enrich_graph_with_metrics
from graph.visualizer import visualize_graph

def run_cli():
    print("PharmaGraph CLI")
    print("Commands: <drug> | all | graph | exit\n")
    
    # Build and enrich the graph once at startup
    G = build_graph()
    G = enrich_graph_with_metrics(G)
    
    # Create lookup for case-insensitive search
    drug_lookup = {node.lower(): node for node in G.nodes()}
    
    # Main command loop
    while True:
        cmd = input("> ").strip().lower()
        
        if cmd == "exit":
            break
            
        elif cmd == "all":
            # Show all drugs
            print("\nDrugs in network:")
            for node in G.nodes():
                print(f"  {node}")
            print()
            
        elif cmd == "graph":
            # Show full graph
            visualize_graph()
            
        elif cmd.startswith("graph "):
            # Show graph for specific drug
            drug_name = cmd[6:]
            visualize_graph(drug_name)
            
        elif cmd in drug_lookup:
            # Show drug details
            drug = drug_lookup[cmd]
            print(f"\nDrug: {drug}")
            
            # Show outgoing interactions
            for successor in G.successors(drug):
                edge = G[drug][successor]
                print(f"  → {successor}: {edge.get('weight')}")
            
            # Show incoming interactions
            for predecessor in G.predecessors(drug):
                edge = G[predecessor][drug]
                print(f"  ← {predecessor}: {edge.get('weight')}")
            print()
            
        else:
            print(f"Unknown command or drug: {cmd}")
```

**CLI Features:**
- **Case-insensitive** drug lookup
- **Graph built once** at startup for efficiency
- **Three display modes**: all drugs, full graph, drug-specific graph
- **Direction shown** with arrows (→ outgoing, ← incoming)

---

## Main Entry Point (`main.py`)

Orchestrates the entire application.

```python
from database import setup_database
from loader import load_data
from cli import run_cli

def main():
    # 1. Create database tables if they don't exist
    setup_database()
    
    # 2. Load data from CSV into database
    load_data()
    
    # 3. Start the CLI (which builds graph and starts interaction)
    run_cli()

if __name__ == "__main__":
    main()
```

**Flow:**
1. **Setup** → Create empty database structure
2. **Load** → Populate with CSV data
3. **Run** → Start user interaction

---

## Data Flow Diagram

```
CSV Files ──► loader.py ──► models.py ──► SQLite DB
                                          │
                                          ▼
                                     builder.py
                                          │
                                          ▼
                                   NetworkX Graph
                                    │           │
                                    ▼           ▼
                              analyzer.py  visualizer.py
                                    │           │
                                    └─────┬─────┘
                                          ▼
                                        cli.py
                                          │
                                          ▼
                                      User
```

**Step-by-step:**
1. CSV → `loader.py` reads files
2. `loader.py` calls `models.py` functions
3. `models.py` writes to SQLite database
4. `cli.py` calls `builder.py` to create graph
5. `builder.py` reads from database via `models.py`
6. Graph is passed to `analyzer.py` and `visualizer.py`
7. User interacts via CLI

---

## Key Concepts Explained

### 1. **Graph Theory Basics**
- **Node** = Drug
- **Edge** = Interaction between two drugs
- **Directed** = Interaction may not be symmetric
- **Attributes** = Additional data on nodes/edges

### 2. **NetworkX Graph Structure**
```python
# Node with attributes
G.nodes["Aspirin"] = {
    "drug_class": "NSAID",
    "degree_centrality": 0.5
}

# Edge with attributes  
G.edges["Aspirin", "Warfarin"] = {
    "weight": "Major",
    "mechanism": "Binds to plasma proteins"
}
```

### 3. **Centrality Metrics**
- **Degree Centrality**: (node_degree) / (total_nodes - 1)
- **Betweenness Centrality**: (paths through node) / (all shortest paths)

### 4. **SQLite vs NetworkX**
- **SQLite**: Persistent storage, queryable
- **NetworkX**: In-memory graph operations, algorithms

### 5. **The Weight Problem**
NetworkX layout algorithms expect **numeric** weights for physics simulation. Our severity strings ("Major", "Moderate") cause errors. Solutions:
- Convert strings to numbers (1,2,3)
- Use unweighted graph for layout (what we did)
- Create custom layout function

---

## Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `could not convert string to float: 'Major'` | Layout using string weights | Use unweighted copy for layout |
| `No module named 'networkx'` | Missing dependency | `pip install networkx matplotlib` |
| `File not found: data/drugs.csv` | Wrong working directory | Run from project root |
| `Unknown command` | Drug not in database | Check spelling, case-insensitive works |

---

## Debugging Tips

1. **Check database content:**
```python
from models import get_all_drugs, get_all_interactions
print(get_all_drugs())
print(get_all_interactions())
```

2. **Examine graph structure:**
```python
G = build_graph()
print(f"Nodes: {G.nodes()}")
print(f"Edges: {G.edges(data=True)}")
```

3. **Test with small dataset first** - create minimal CSV files for testing

---

This guide should help you understand each component and how they fit together. Start with `main.py` and follow the data flow to see how information moves through the system.
```