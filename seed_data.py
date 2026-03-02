# seed_data.py
from models import add_drug, add_interaction

def seed_database():
    # Clear DB first (optional)
    # You can delete pharmagraph.db before running main.py for a fresh start

    # 20 drugs
    drugs = [
        ('Aspirin', 'NSAID'),
        ('Ibuprofen', 'NSAID'),
        ('Paracetamol', 'Analgesic'),
        ('Warfarin', 'Anticoagulant'),
        ('Metformin', 'Antidiabetic'),
        ('Insulin', 'Antidiabetic'),
        ('Lisinopril', 'ACE inhibitor'),
        ('Losartan', 'ARB'),
        ('Simvastatin', 'Statin'),
        ('Atorvastatin', 'Statin'),
        ('Omeprazole', 'Proton Pump Inhibitor'),
        ('Ranitidine', 'H2 blocker'),
        ('Amoxicillin', 'Antibiotic'),
        ('Ciprofloxacin', 'Antibiotic'),
        ('Prednisone', 'Corticosteroid'),
        ('Hydrocortisone', 'Corticosteroid'),
        ('Diazepam', 'Benzodiazepine'),
        ('Lorazepam', 'Benzodiazepine'),
        ('Furosemide', 'Diuretic'),
        ('Spironolactone', 'Diuretic')
    ]

    for name, cls in drugs:
        add_drug(name, cls)

    # 25+ interactions (some arbitrary for demo purposes)
    interactions = [
        ('Aspirin', 'Warfarin', 3, 'pharmacodynamic'),
        ('Aspirin', 'Ibuprofen', 2, 'pharmacodynamic'),
        ('Warfarin', 'Metformin', 1, 'unknown'),
        ('Lisinopril', 'Losartan', 3, 'pharmacodynamic'),
        ('Simvastatin', 'Atorvastatin', 2, 'pharmacokinetic'),
        ('Omeprazole', 'Ranitidine', 2, 'pharmacodynamic'),
        ('Amoxicillin', 'Ciprofloxacin', 1, 'unknown'),
        ('Prednisone', 'Hydrocortisone', 2, 'pharmacodynamic'),
        ('Diazepam', 'Lorazepam', 3, 'pharmacodynamic'),
        ('Furosemide', 'Spironolactone', 2, 'pharmacodynamic'),
        ('Aspirin', 'Metformin', 1, 'pharmacokinetic'),
        ('Ibuprofen', 'Prednisone', 2, 'pharmacodynamic'),
        ('Warfarin', 'Simvastatin', 3, 'pharmacokinetic'),
        ('Lisinopril', 'Furosemide', 2, 'pharmacodynamic'),
        ('Losartan', 'Spironolactone', 1, 'pharmacodynamic'),
        ('Omeprazole', 'Amoxicillin', 1, 'unknown'),
        ('Paracetamol', 'Diazepam', 1, 'unknown'),
        ('Metformin', 'Insulin', 3, 'pharmacodynamic'),
        ('Ciprofloxacin', 'Warfarin', 2, 'pharmacokinetic'),
        ('Hydrocortisone', 'Lorazepam', 1, 'unknown'),
        ('Atorvastatin', 'Omeprazole', 2, 'pharmacokinetic'),
        ('Furosemide', 'Diazepam', 1, 'unknown'),
        ('Spironolactone', 'Lisinopril', 2, 'pharmacodynamic'),
        ('Ibuprofen', 'Ciprofloxacin', 1, 'pharmacokinetic'),
        ('Prednisone', 'Warfarin', 2, 'pharmacodynamic')
    ]

    for d1, d2, severity, mech in interactions:
        add_interaction(d1, d2, severity, mech)