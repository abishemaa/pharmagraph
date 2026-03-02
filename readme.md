Project Structure (Clean Separation From Day One)
pharmagraph/
│
├── database.py      # SQLite connection + setup
├── models.py        # Data layer functions
├── graph_engine.py  # NetworkX logic
├── cli.py           # Command-line interface
├── pharmagraph.db
└── main.py

Small. Surgical. Expandable.


How to Run CLI + Graph

CLI:

python cli.py

Type drug name → see interactions

Type exit → quit

Graph:

python
from graph_engine import visualize_graph
visualize_graph()  

Explain node color = drug class

Edge color/thickness = severity