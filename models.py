#models.py
from database import get_db_connection

def add_drug(name, drug_class, moa, metabolism):
    conn = get_db_connection()
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
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO interactions
        (drug1,drug2,severity,mechanism,clinical_effect,management)
        VALUES (?,?,?,?,?,?)
    """, (d1, d2, severity, mechanism, effect, management))
    conn.commit()
    conn.close()

def get_all_drugs():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT name, drug_class, moa, metabolism FROM drugs")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_all_interactions():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT drug1,drug2,severity,mechanism,clinical_effect,management FROM interactions")
    rows = cur.fetchall()
    conn.close()
    return [dict(row) for row in rows]

def get_drug_class(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT drug_class FROM drugs WHERE name=?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row['drug_class'] if row else 'Unknown'