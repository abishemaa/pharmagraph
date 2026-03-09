# models.py
from database import get_db_connection
import csv
import pandas as pd

# CSV LOADING
def load_excel_data():

    file_path = "data/pg_drug_bank.xlsx"

    drugs_df = pd.read_excel(file_path, sheet_name="drugs")
    interactions_df = pd.read_excel(file_path, sheet_name="interactions")

    # load drugs
    for _, row in drugs_df.iterrows():

        if not row["name"]:
            continue

        add_drug(
            str(row["name"]).strip(),
            str(row["class"]).strip()
        )

    # load interactions
    for _, row in interactions_df.iterrows():

        if not row["drug1"] or not row["drug2"]:
            continue

        add_interaction(
            str(row["drug1"]).strip(),
            str(row["drug2"]).strip(),
            str(row.get("severity", "minor")).strip(),
            str(row.get("mechanism", "unknown")).strip(),
            str(row.get("clinical_effect", "")).strip(),
            str(row.get("evidence", "")).strip(),
            str(row.get("management", "")).strip()
        )

# DRUG OPERATIONS
def add_drug(name, drug_class):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT OR IGNORE INTO drugs (name, drug_class)
        VALUES (?, ?)
        """,
        (name, drug_class)
    )

    conn.commit()
    conn.close()

def get_drug_class(name):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT drug_class FROM drugs WHERE name=?",
        (name,)
    )

    row = cursor.fetchone()

    conn.close()

    return row["drug_class"] if row else "Unknown"

# INTERACTION OPERATIONS
def add_interaction(
    drug1,
    drug2,
    severity="minor",
    mechanism="unknown",
    clinical_effect="",
    evidence="",
    management=""
    ):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO interactions
        (drug1, drug2, severity, mechanism, clinical_effect, evidence, management)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            drug1,
            drug2,
            severity,
            mechanism,
            clinical_effect,
            evidence,
            management
        )
    )

    conn.commit()
    conn.close()

# QUERY FUNCTIONS
def get_interactions(drug_name=None):
    conn = get_db_connection()
    cursor = conn.cursor()

    if drug_name:
        cursor.execute(
            """
            SELECT * FROM interactions
            WHERE LOWER(drug1)=LOWER(?) OR LOWER(drug2)=LOWER(?)
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
            "severity": row["severity"] or "minor",
            "mechanism": row["mechanism"] or "unknown",
            "clinical_effect": row["clinical_effect"] or "",
            "evidence": row["evidence"] or "",
            "management": row["management"] or ""
        })

    return interactions