# SQLite connection + setup
import sqlite3

DB_NAME = "pharmagraph.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS drugs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        drug_class TEXT,
        notes TEXT
    );
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        drug_a_id INTEGER NOT NULL,
        drug_b_id INTEGER NOT NULL,
        severity TEXT CHECK(severity IN ('mild','moderate','severe')) NOT NULL,
        mechanism TEXT NOT NULL,
        FOREIGN KEY (drug_a_id) REFERENCES drugs(id),
        FOREIGN KEY (drug_b_id) REFERENCES drugs(id),
        UNIQUE(drug_a_id, drug_b_id),
        CHECK (drug_a_id < drug_b_id)
    );
    """)

    conn.commit()
    conn.close()