import sqlite3

DB_FILE = "pharmagraph.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Drugs table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS drugs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            drug_class TEXT,
            mechanism_of_action TEXT,
            metabolism TEXT
        )
    """)

    # Interactions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            drug1 TEXT,
            drug2 TEXT,
            severity INTEGER,
            mechanism TEXT,
            clinical_effect TEXT,
            evidence TEXT,
            management TEXT,
            FOREIGN KEY(drug1) REFERENCES drugs(name),
            FOREIGN KEY(drug2) REFERENCES drugs(name)
        )
    """)

    conn.commit()
    conn.close()