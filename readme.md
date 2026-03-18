```markdown
# PharmaGraph - Drug Interaction Network

A command-line tool for analyzing drug-drug interaction networks using graph theory.

## Installation

```bash
# Clone the repository
git clone <https://github.com/abishemaa/pharmagraph>
cd pharmagraph

# Install dependencies
pip install networkx matplotlib
```

## Data Format

Place your data files in the `data/` directory:

```
data/
├── drugs.json          # Drug information
└── interactions.json   # Interaction data
```

### JSON Structure

**drugs.json**
```json
[
  {
    "name": "Warfarin",
    "class": "Anticoagulant",
    "moa": "Vitamin K antagonist",
    "metabolism": "CYP2C9, CYP3A4"
  }
]
```

**interactions.json**
```json
[
  {
    "drug1": "Warfarin",
    "drug2": "Ibuprofen",
    "severity": "Major",
    "mechanism": "Pharmacodynamic",
    "clinical_effect": "Increased bleeding risk",
    "management": "Avoid NSAIDs with Warfarin"
  }
]
```

## Usage

Run the program:
```bash
python main.py
```

### Commands

| Command | Description | Example |
|---------|-------------|---------|
| `<drug>` | Show drug details and interactions | `> warfarin` |
| `all` | List all drugs | `> all` |
| `stats` | Show network statistics | `> stats` |
| `graph` | Visualize full network | `> graph` |
| `graph <drug>` | Visualize drug subgraph | `> graph warfarin` |
| `explain <d1> <d2>` | Explain interaction between two drugs | `> explain warfarin ibuprofen` |
| `path <d1> <d2>` | Find path between drugs | `> path warfarin simvastatin` |
| `exit` | Exit program | `> exit` |

## Example Session

```
> warfarin

============================================================
DRUG: Warfarin
============================================================

Network Centrality:
  Degree: 0.389 (connectedness)
  Betweenness: 0.744 (bridge potential)

Interactions:

[Major]
  - Amiodarone
    Mechanism: CYP2C9 Inhibition
    Effect: Significantly increased INR
    Management: Reduce Warfarin dose by 30-50%

  - Ibuprofen
    Mechanism: Pharmacodynamic
    Effect: Increased bleeding risk
    Management: Avoid NSAIDs with Warfarin

> stats

============================================================
NETWORK SUMMARY
============================================================

Overview:
  Total Drugs: 19
  Total Interactions: 25
  Network Density: 0.146

Top 5 Most Connected Drugs:
  Warfarin: 0.389
  Ibuprofen: 0.222
  Simvastatin: 0.222
  Clarithromycin: 0.167
  Rifampin: 0.167

Severity Distribution:
  Major: 12
  Moderate: 12
  Contraindicated: 1

> explain warfarin amiodarone

============================================================
INTERACTION: Warfarin <-> Amiodarone
============================================================

Severity: Major

Mechanism:
  CYP2C9 Inhibition

Clinical Effect:
  Significantly increased INR

Management:
  Reduce Warfarin dose by 30-50%
```

## Project Structure

```
pharmagraph/
├── main.py                 # Entry point
├── core/
│   ├── __init__.py
│   └── engine.py          # Core graph logic
├── interface/
│   ├── __init__.py
│   └── cli.py             # Command-line interface
├── visualize/
│   ├── __init__.py
│   └── plot.py            # Graph visualization
└── data/
    ├── drugs.json
    └── interactions.json
```

## Dependencies

- Python 3.6+
- networkx
- matplotlib