# PharmaGraph - Drug Interaction Network Analysis

A powerful tool for building, analyzing, and visualizing drug-drug interaction networks. PharmaGraph transforms drug interaction data from CSV files into a directed graph, calculates network metrics, and provides an intuitive CLI for exploration.

![Drug Interaction Network Example](https://via.placeholder.com/800x400?text=Drug+Interaction+Network+Visualization)

## 📋 Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage Guide](#usage-guide)
- [Data Format](#data-format)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## ✨ Features

- **Graph Construction** - Build directed graphs from drug interaction data
- **Network Analysis** - Calculate degree centrality and betweenness centrality
- **Interactive CLI** - Explore drug interactions with simple commands
- **Visualization** - Generate clear network visualizations
- **SQLite Backend** - Persistent storage with full CRUD operations
- **CSV Import** - Easy data loading from standard CSV files

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Steps

1. **Clone the repository**
```bash
git clone https://github.com/abishemaa/pharmagraph.git
cd pharmagraph
```

2. **Create a virtual environment** (recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install networkx matplotlib tabulate
```

4. **Prepare your data**
Place your CSV files in the `data/` directory:
- `drugs.csv` - Drug information
- `interactions.csv` - Drug interaction data

## 🎯 Quick Start

Run the application:
```bash
python main.py
```

Once running, try these commands:
```
> all              # List all drugs
> aspirin          # Show aspirin details
> graph            # Visualize full network
> graph warfarin   # Visualize warfarin subnet
> exit             # Quit
```

## 📖 Usage Guide

### CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `<drug_name>` | Show drug details and interactions | `> aspirin` |
| `all` | List all drugs in network | `> all` |
| `graph` | Show full interaction network | `> graph` |
| `graph <drug>` | Show subgraph for specific drug | `> graph warfarin` |
| `exit` | Exit the program | `> exit` |

### Example Session

```
PharmaGraph CLI
Commands: <drug> | all | graph | exit

> all

Drugs in network:
  Aspirin
  Warfarin
  Ibuprofen
  Metformin

> aspirin

Drug: Aspirin
  → Warfarin: Major
  → Ibuprofen: Moderate
  ← Metformin: Minor

> graph aspirin
[Visualization window opens]
```

## 📊 Data Format

### drugs.csv
```csv
name,class,moa,metabolism
Aspirin,NSAID,Cyclooxygenase inhibitor,Hepatic
Warfarin,Anticoagulant,Vitamin K antagonist,Hepatic
```

### interactions.csv
```csv
drug1,drug2,severity,mechanism,clinical_effect,management
Aspirin,Warfarin,Major,Increased bleeding risk,Gastrointestinal bleeding,Monitor INR
Aspirin,Ibuprofen,Moderate,Reduced cardioprotection,Decreased aspirin efficacy,Avoid combination
```

## 📁 Project Structure

```
pharmagraph/
│
├── data/                       # CSV data files
│   ├── drugs.csv
│   └── interactions.csv
│
├── graph/                      # Graph operations
│   ├── __init__.py
│   ├── builder.py              # Build NetworkX graph from database
│   ├── analyzer.py             # Calculate network metrics
│   └── visualizer.py           # Generate visualizations
│
├── database.py                  # SQLite database setup
├── models.py                    # Database CRUD operations
├── loader.py                     # CSV data loading
├── cli.py                        # Command-line interface
├── main.py                       # Application entry point
├── pharmagraph.db                # SQLite database (created on first run)
└── README.md
```

## 🔧 How It Works

### Architecture

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   CSV Files │───▶│    Loader   │───▶│   SQLite    │
└─────────────┘    └─────────────┘    └─────────────┘
                                              │
                                              ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│     CLI     │◀──▶│   Builder   │◀──▶│  NetworkX   │
└─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │
       ▼                  ▼                  ▼
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   User I/O  │    │  Analyzer   │    │Visualization│
└─────────────┘    └─────────────┘    └─────────────┘
```

### Data Flow

1. **CSV Import** → `loader.py` reads CSV files
2. **Database Storage** → `models.py` writes to SQLite
3. **Graph Building** → `builder.py` creates NetworkX graph
4. **Analysis** → `analyzer.py` adds centrality metrics
5. **Visualization** → `visualizer.py` generates plots
6. **User Interaction** → `cli.py` provides interface

### Key Components

- **Database Layer**: SQLite with two tables (drugs, interactions)
- **Model Layer**: CRUD operations for data access
- **Graph Layer**: NetworkX directed graph with node/edge attributes
- **Analysis Layer**: Centrality calculations
- **Visualization Layer**: Matplotlib-based network plots
- **Interface Layer**: Command-line interface with tabulate formatting

## 💡 Examples

### Basic Drug Query
```bash
> metformin

Drug: Metformin
  → Aspirin: Minor
  ← Warfarin: Moderate
```

### Network Analysis
```bash
> all

Drugs in network (sorted by centrality):
  Warfarin      0.856   0.423   12
  Aspirin       0.714   0.312   10
  Metformin     0.429   0.156   6
  Ibuprofen     0.286   0.089   4
```

### Visualization Output
The graph visualization shows:
- **Nodes**: Drugs (color-coded by drug class)
- **Edges**: Interactions (colored by severity)
- **Layout**: Spring layout for clear visualization

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add amazing feature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/amazing-feature
   ```
5. **Open a Pull Request**

### Development Setup
```bash
# Install development dependencies
pip install pytest pylint black

# Run tests
pytest tests/

# Format code
black .
```

## 🙏 Acknowledgments

- [NetworkX](https://networkx.org/) - Graph algorithms and structures
- [Matplotlib](https://matplotlib.org/) - Visualization library
- [SQLite](https://www.sqlite.org/) - Lightweight database
- [Tabulate](https://github.com/astanin/python-tabulate) - Pretty CLI tables

## 📧 Contact

Project Link: [https://github.com/abishemaa/pharmagraph](https://github.com/yourusername/pharmagraph)

---

**Made with ❤️ for safer medication practices**
```