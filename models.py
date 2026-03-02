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

def get_drug_class(drug_name):
    """Return the class of a drug."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT drug_class FROM drugs WHERE name = ?", (drug_name,))
    result = cursor.fetchone()
    conn.close()
    if result and result[0]:
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

def get_interactions(drug_name):
    conn = get_connection()
    cursor = conn.cursor()

    # Get the ID of the drug
    drug_id = get_drug_id(drug_name)
    if not drug_id:
        print(f"{drug_name} not found in database.")
        conn.close()
        return []

    # Query interactions where this drug is either drug_a or drug_b
    cursor.execute("""
        SELECT d1.name, d2.name, i.severity, i.mechanism
        FROM interactions i
        JOIN drugs d1 ON i.drug_a_id = d1.id
        JOIN drugs d2 ON i.drug_b_id = d2.id
        WHERE i.drug_a_id = ? OR i.drug_b_id = ?
    """, (drug_id, drug_id))

    results = cursor.fetchall()
    conn.close()

    interactions = []

    for d1_name, d2_name, severity, mechanism in results:
        # Determine which one is the "other" drug
        other = d2_name if d1_name == drug_name else d1_name
        interactions.append({
            "drug": other,
            "severity": severity,
            "mechanism": mechanism
        })

    return interactions