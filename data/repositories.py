from .database import get_connection

def get_drug_by_name(name):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drugs WHERE name = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    return result

def get_interactions_for_drug(drug_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM interactions WHERE drug_id = ?", (drug_id,))
    results = cursor.fetchall()
    conn.close()
    return results

def get_all_drugs():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM drugs")
    results = cursor.fetchall()
    conn.close()
    return results