import csv
from database import add_drug, add_interaction


def load_data():
    with open("data/drugs.csv", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for r in reader:

            add_drug(
                r["name"],
                r["class"],
                r["moa"],
                r["metabolism"]
            )

    with open("data/interactions.csv", encoding="utf-8") as f:

        reader = csv.DictReader(f)

        for r in reader:
            add_interaction(
                r["drug1"],
                r["drug2"],
                r["severity"],
                r["mechanism"],
                r["clinical_effect"],
                r["management"]
            )