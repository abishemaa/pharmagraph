#seed data for drugs
from models import add_drug, add_interaction

# --- Step 1: Add Drugs ---
drugs = [
    ("Warfarin", "Anticoagulant", "Vitamin K antagonist"),
    ("Aspirin", "Antiplatelet", "COX-1 inhibitor"),
    ("Clopidogrel", "Antiplatelet", "P2Y12 inhibitor"),
    ("Simvastatin", "Statin", "HMG-CoA reductase inhibitor"),
    ("Clarithromycin", "Macrolide", "CYP3A4 inhibitor"),
    ("Metformin", "Antidiabetic", "Biguanide"),
    ("Insulin", "Antidiabetic", "Exogenous hormone"),
    ("Lisinopril", "ACE inhibitor", "Reduces blood pressure"),
    ("Spironolactone", "Diuretic", "Aldosterone antagonist"),
    ("Digoxin", "Cardiac glycoside", "Positive inotrope"),
    ("Amiodarone", "Antiarrhythmic", "Class III antiarrhythmic"),
    ("Fluoxetine", "SSRI", "Selective serotonin reuptake inhibitor"),
    ("Sertraline", "SSRI", "Selective serotonin reuptake inhibitor"),
    ("Tramadol", "Opioid analgesic", "Serotonergic effect"),
    ("Omeprazole", "PPI", "Proton pump inhibitor"),
    ("Rifampicin", "Antibiotic", "CYP3A4 inducer"),
    ("Phenytoin", "Anticonvulsant", "CYP3A4 inducer"),
    ("Carbamazepine", "Anticonvulsant", "CYP3A4 inducer"),
    ("Verapamil", "CCB", "Calcium channel blocker"),
    ("Diltiazem", "CCB", "Calcium channel blocker")
]

print("Drugs added successfully.")

# --- Step 2: Add Interactions ---
interactions = [
    ("Warfarin", "Aspirin", "severe", "Additive anticoagulant effect increases bleeding risk"),
    ("Warfarin", "Clopidogrel", "severe", "Additive antiplatelet effect increases bleeding risk"),
    ("Simvastatin", "Clarithromycin", "severe", "CYP3A4 inhibition increases statin levels and risk of myopathy"),
    ("Metformin", "Rifampicin", "moderate", "CYP induction may reduce metformin efficacy"),
    ("Insulin", "Metformin", "mild", "Additive hypoglycemic effect"),
    ("Digoxin", "Amiodarone", "moderate", "Amiodarone increases digoxin levels"),
    ("Fluoxetine", "Tramadol", "moderate", "Increased risk of serotonin syndrome"),
    ("Sertraline", "Tramadol", "moderate", "Increased risk of serotonin syndrome"),
    ("Omeprazole", "Clopidogrel", "moderate", "PPI may reduce clopidogrel activation"),
    ("Rifampicin", "Warfarin", "severe", "CYP induction decreases warfarin efficacy, risk of clotting"),
    ("Phenytoin", "Warfarin", "moderate", "CYP induction decreases warfarin efficacy"),
    ("Carbamazepine", "Simvastatin", "moderate", "CYP induction reduces statin levels"),
    ("Verapamil", "Simvastatin", "moderate", "CYP3A4 inhibition increases statin levels"),
    ("Diltiazem", "Simvastatin", "moderate", "CYP3A4 inhibition increases statin levels"),
    ("Lisinopril", "Spironolactone", "moderate", "Additive hyperkalemia risk"),
    ("Digoxin", "Verapamil", "moderate", "Verapamil increases digoxin levels"),
    ("Amiodarone", "Warfarin", "moderate", "Amiodarone increases warfarin levels"),
    ("Fluoxetine", "Sertraline", "mild", "Additive serotonergic effect"),
    ("Omeprazole", "Clarithromycin", "mild", "Minor CYP3A4 interaction"),
    ("Tramadol", "Carbamazepine", "moderate", "CYP induction may reduce tramadol efficacy")
]

print("Interactions added successfully.")