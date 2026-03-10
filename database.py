import sqlite3

DB_FILE = "pharmagraph.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row  # access columns by name
    return conn

def setup_database():

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS drugs(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        drug_class TEXT,
        moa TEXT,
        metabolism TEXT
    );
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS interactions(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug1 TEXT,
        drug2 TEXT,
        severity TEXT,
        mechanism TEXT,
        clinical_effect TEXT,
        management TEXT
    )
    """)

    conn.commit()
    conn.close()