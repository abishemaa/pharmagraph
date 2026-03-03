https://github.com/abishemaa/pharmagraph

# Drug Interaction Network – V1

## Overview

This project visualizes drug–drug interactions using a graph-based approach.

Each drug is represented as a node.
Each interaction is represented as an edge.

The graph encodes:

* **Node color** → Drug class
* **Edge color** → Interaction mechanism

  * Red → Pharmacodynamic
  * Blue → Pharmacokinetic
  * Gray → Other
* **Edge width** → Interaction severity

The goal of V1 is structural visualization, not clinical validation.

---

## Project Structure

```
project/
│
├── models.py          # Data access and drug classification logic
├── graph_engine.py    # Graph construction and visualization
├── seed.py            # Seed interaction data
├── main.py            # Entry point
└── README.md
```

---

## How It Works

### 1. Data Retrieval

`get_interactions(drug_name=None)`
Returns all interactions or interactions for a specific drug.

`get_drug_class(drug_name)`
Returns the drug class for visualization grouping.

---

### 2. Graph Construction

A `networkx.Graph()` object is built dynamically:

* Nodes are created with a `drug_class` attribute.
* Edges are created with:

  * `mechanism`
  * `severity`

---

### 3. Visualization

The graph uses:

* `spring_layout()` for positioning
* Matplotlib for rendering
* Dynamic color mapping for drug classes
* A legend generated from node and edge styles

The layout is deterministic (`seed=42`) for reproducibility.

---

## Installation

Install dependencies:

```bash
pip install networkx matplotlib
```

Optional (for future interactive features):

```bash
pip install mplcursors
```

---

## Running the Project

Run the full interaction graph:

```bash
python main.py
```

Visualize a specific drug (inside Python):

```python
visualize_graph("Aspirin")
```

---

## Example Output

The graph will display:

* Nodes grouped by drug class
* Colored edges by interaction mechanism
* Thicker edges indicating higher severity
* A legend explaining visual encoding

---

## Design Principles (V1)

* Separation of data, graph logic, and presentation
* Deterministic visualization
* Attribute-driven styling
* Minimal UI complexity

---

## Limitations (V1)

* Seed data is static and limited
* Severity scaling is linear
* No filtering or dynamic controls
* No analytical metrics (centrality, clustering)
* No database integration

---

## Roadmap (V2 Ideas)

* Centrality metrics (degree, betweenness)
* Risk scoring visualization
* Interactive filtering
* Database-backed interaction data
* Severity normalization
* Hover tooltips
* Drug clustering analysis

---

## Disclaimer

This project is for educational and structural exploration purposes only.
It does not replace clinical decision tools or validated drug interaction databases.
