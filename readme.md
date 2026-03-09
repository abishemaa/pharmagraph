# Drug Interaction Network

A lightweight web application for visualizing drug–drug interactions as an interactive network graph.

The application stores drugs and their pharmacological properties in a SQLite database and displays their relationships using an interactive force-directed graph.

## Features

* Interactive drug interaction graph
* Search for a specific drug to filter its interactions
* Hover over nodes to view pharmacological details
* Drug metadata stored in a SQLite database
* Simple Flask backend
* Force-directed visualization in the browser

## Tech Stack

Backend:

* Python
* Flask
* SQLite

Frontend:

* JavaScript
* ForceGraph
* HTML/CSS

## Project Structure

```
pharmagraph/
│
├── database.py        # Database schema and CRUD functions
├── loader.py          # Loads sample drug data into the database
├── ddi.db             # SQLite database
│
├── web/
│   ├── app.py         # Flask application
│   ├── templates/
│   │   └── index.html # Main UI
│   └── static/
│       └── graph.js   # Graph rendering logic
│
└── README.md
```

## Installation

1. Clone the repository

```
git clone <repo-url>
cd pharmagraph
```

2. Install dependencies

```
pip install flask
```

3. Run the application

```
python -m web.app
```

4. Open in your browser

```
http://127.0.0.1:5000
```

## Usage

* The graph loads automatically showing all drugs and interactions.
* Enter a drug name in the search box to filter interactions related to that drug.
* Hover over a node to view:

  * Drug class
  * Mechanism of action
  * Metabolism pathway

## Database Schema

### drugs

| column     | type    |
| ---------- | ------- |
| id         | INTEGER |
| name       | TEXT    |
| drug_class | TEXT    |
| moa        | TEXT    |
| metabolism | TEXT    |

### interactions

| column          | type    |
| --------------- | ------- |
| id              | INTEGER |
| drug1           | TEXT    |
| drug2           | TEXT    |
| severity        | TEXT    |
| mechanism       | TEXT    |
| clinical_effect | TEXT    |
| management      | TEXT    |

## Future Improvements

* Display interaction mechanism on edge hover
* Severity color coding for interactions
* Drug class clustering
* Advanced pharmacogenomics integration
* External data sources (DrugBank, PharmGKB)
