import sqlite3

DB_PATH = "ddi.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def setup_database():

    conn = get_connection()
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

# CRUD operations
def add_drug(name, drug_class, moa, metabolism):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT OR IGNORE INTO drugs(name, drug_class, moa, metabolism)
        VALUES (?, ?, ?, ?)
        """,
        (name, drug_class, moa, metabolism)
    )

    conn.commit()
    conn.close()


def add_interaction(d1, d2, severity, mechanism, effect, management):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO interactions
        (drug1,drug2,severity,mechanism,clinical_effect,management)
        VALUES (?,?,?,?,?,?)
    """, (d1, d2, severity, mechanism, effect, management))

    conn.commit()
    conn.close()


def get_all_drugs():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT name, drug_class, moa, metabolism
        FROM drugs
    """)

    rows = cur.fetchall()

    conn.close()

    return rows


def get_all_interactions():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT drug1,drug2,severity FROM interactions")
    rows = cur.fetchall()

    conn.close()

    return rows