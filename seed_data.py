#seed data for drugs
from models import add_drug

drugs = [
    ("Warfarin", "Anticoagulant", "Vitamin K antagonist"),
    ("Aspirin", "Antiplatelet", "COX-1 inhibitor"),
    ("Clopidogrel", "Antiplatelet", "P2Y12 inhibitor"),
    ("Simvastatin", "Statin", "HMG-CoA reductase inhibitor"),
    ("Clarithromycin", "Macrolide", "CYP3A4 inhibitor"),
]

for name, drug_class, notes in drugs:
    add_drug(name, drug_class, notes)

print("Drugs inserted.")