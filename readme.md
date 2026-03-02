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


