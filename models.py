# Data layer functions
from database import get_connection

def add_drug(name, drug_class=None, notes=None):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO drugs (name, drug_class, notes) VALUES (?, ?, ?)",
        (name, drug_class, notes)
    )

    conn.commit()
    conn.close()

def get_drug_id(name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM drugs WHERE name = ?", (name,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None


def add_interaction(drug_name_a, drug_name_b, severity, mechanism):
    conn = get_connection()
    cursor = conn.cursor()

    id_a = get_drug_id(drug_name_a)
    id_b = get_drug_id(drug_name_b)

    if not id_a or not id_b:
        print("One or both drugs not found.")
        conn.close()
        return

    if id_a == id_b:
        print("Cannot create self-interaction.")
        conn.close()
        return

    # Enforce canonical ordering
    drug_a_id, drug_b_id = sorted([id_a, id_b])

    try:
        cursor.execute("""
            INSERT INTO interactions (drug_a_id, drug_b_id, severity, mechanism)
            VALUES (?, ?, ?, ?)
        """, (drug_a_id, drug_b_id, severity, mechanism))

        conn.commit()
        print("Interaction added successfully.")

    except sqlite3.IntegrityError:
        print("Interaction already exists or violates constraints.")    
    
    conn.close()

def list_drugs():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT name FROM drugs")
    result = cursor.fetchall()

    conn.close()

    if result:
        return [row[0] for row in result]   # returns empty list if no rows
    else:
        return None