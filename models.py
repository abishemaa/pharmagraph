from database import get_db_connection

def add_drug(name, drug_class):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO drugs (name, drug_class) VALUES (?, ?)",
        (name, drug_class)
    )
    conn.commit()
    conn.close()

def add_interaction(drug1, drug2, severity=1, mechanism='unknown'):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO interactions (drug1, drug2, severity, mechanism) VALUES (?, ?, ?, ?)",
        (drug1, drug2, severity, mechanism)
    )
    conn.commit()
    conn.close()

def get_interactions(drug_name=None):
    """
    Fetch interactions from DB.
    If drug_name is None, return all interactions.
    """

    conn = get_db_connection()
    cursor = conn.cursor()

    if drug_name:
        drug_name = drug_name.lower()

        cursor.execute(
            """
            SELECT * FROM interactions
            WHERE LOWER(drug1)=? OR LOWER(drug2)=?
            """,
            (drug_name, drug_name)
        )

    else:
        cursor.execute("SELECT * FROM interactions")

    rows = cursor.fetchall()
    conn.close()

    interactions = []

    for row in rows:
        interactions.append({
            "drug1": row["drug1"],
            "drug2": row["drug2"],
            "severity": row["severity"] or 1,
            "mechanism": row["mechanism"] or "unknown",
        })

    return interactions

def get_drug_class(name):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT drug_class FROM drugs WHERE name=?", (name,))
    row = cursor.fetchone()
    conn.close()
    return row['drug_class'] if row else 'Unknown'