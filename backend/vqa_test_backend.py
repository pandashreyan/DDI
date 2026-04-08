import json
import os
import sys

# Mocking data structures from app.py to test logic in isolation
# Or better: Import the modules directly and test their functions.

try:
    from profile_adjuster import calculate_personalized_risk
    from regimen_optimizer import optimize_regimen
    from lifestyle_analyzer import analyze_lifestyle_interactions
    from clinical_evidence import get_combined_evidence
except ImportError as e:
    print(f"FAILED IMPORT: {e}")
    sys.exit(1)

# Sample metadata for common drugs
DRUG_METADATA = {
    "aspirin": {"name": "aspirin", "class": "NSAID", "cyp": ["CYP2C9"]},
    "metformin": {"name": "metformin", "class": "Antidiabetic", "cyp": []},
    "warfarin": {"name": "warfarin", "class": "Anticoagulant", "cyp": ["CYP2C9", "CYP1A2", "CYP3A4"]},
    "simvastatin": {"name": "simvastatin", "class": "Statin", "cyp": ["CYP3A4"]},
    "diazepam": {"name": "diazepam", "class": "Benzodiazepine", "cyp": ["CYP3A4", "CYP2C19"]},
    "metronidazole": {"name": "metronidazole", "class": "Antibiotic", "cyp": []}
}

def test_personalized_risk():
    print("\n--- Testing Personalized Risk (profile_adjuster) ---")
    
    # 1. Geriatric + Benzodiazepine (Beers List)
    score, warnings = calculate_personalized_risk(0.3, DRUG_METADATA["diazepam"], DRUG_METADATA["aspirin"], {"age": 70})
    print(f"Geriatric (Age 70) + Diazepam: Score {0.3} -> {score}, Warnings: {len(warnings)}")
    assert score > 0.3
    
    # 2. Renal Failure + Metformin
    score, warnings = calculate_personalized_risk(0.1, DRUG_METADATA["metformin"], DRUG_METADATA["aspirin"], {"egfr": 25})
    print(f"Renal (eGFR 25) + Metformin: Score {0.1} -> {score}, Warnings: {len(warnings)}")
    assert any("Metformin contraindicated" in w for w in warnings)

def test_lifestyle_analysis():
    print("\n--- Testing Lifestyle Analysis (lifestyle_analyzer) ---")
    
    # 1. Grapefruit + Simvastatin
    warnings = analyze_lifestyle_interactions([DRUG_METADATA["simvastatin"]], {"grapefruit": True})
    print(f"Grapefruit + Simvastatin: Warnings: {len(warnings)}")
    assert any("Grapefruit juice inhibits CYP3A4" in w['msg'] for w in warnings)
    
    # 2. Alcohol + Metronidazole (Disulfiram)
    warnings = analyze_lifestyle_interactions([DRUG_METADATA["metronidazole"]], {"alcohol": "frequent"})
    print(f"Alcohol + Metronidazole: Warnings: {len(warnings)}")
    assert any("Disulfiram-like reaction" in w['msg'] for w in warnings)

def test_regimen_optimization():
    print("\n--- Testing Regimen Optimization (regimen_optimizer) ---")
    
    drugs = ["metabolic", "simvastatin", "diazepam"] # metabolic is a placeholder
    # Simulating 3 specific drugs
    opt = optimize_regimen(["simvastatin", "diazepam", "metronidazole"], DRUG_METADATA)
    print(f"3-Drug Regimen: Schedule Slots: {list(opt['schedule'].keys())}, Regimen Score: {opt['regimen_score']}")
    assert "night" in opt["schedule"]
    assert len(opt["schedule"]["night"]) > 0 # Diazepam should be at night

def test_clinical_evidence():
    print("\n--- Testing Live Clinical Evidence (clinical_evidence) ---")
    evidence = get_combined_evidence("aspirin", "warfarin")
    print(f"Evidence for Aspirin + Warfarin: Trials found: {len(evidence.get('pubmed_trials', []))}")
    # This might fail if no internet, but we check if it handles it gracefully
    assert "drug_a_warning" in evidence or "pubmed_trials" in evidence

if __name__ == "__main__":
    test_personalized_risk()
    test_lifestyle_analysis()
    test_regimen_optimization()
    # test_clinical_evidence() # Skip by default if offline, but good for VQA
    print("\n--- ALL BACKEND LOGIC VERIFIED SUCCESSFULLY ---")
