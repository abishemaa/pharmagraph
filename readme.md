# PharmaGraph - Drug Interaction Network Analysis

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

Project Link: https://github.com/abishemaa/pharmagraph

---