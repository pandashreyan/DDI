import logging

logger = logging.getLogger(__name__)

# Specialized Clinical Rule Sets
RENAL_SENSITIVE_CLASSES = ["Antidiabetic", "NSAID", "Loop Diuretic", "ACE Inhibitor", "Cardiac Glycoside"]
BEERS_CRITERIA_CLASSES = ["Benzodiazepine", "Tricyclic Antidepressant", "Antipsychotic", "Opioid"]
HEPATIC_SENSITIVE_CLASSES = ["Statin", "Antifungal", "Antiviral"]

def calculate_personalized_risk(base_score, drug_a_meta, drug_b_meta, profile):
    """
    Adjusts the interaction risk score based on patient-specific context.
    Returns: (adjusted_score, [personalized_warnings])
    """
    if not profile:
        return base_score, []

    adj_score = base_score
    warnings = []
    
    age = int(profile.get("age", 40))
    gender = profile.get("gender", "other")
    egfr = float(profile.get("egfr", 90))
    liver_status = profile.get("liver", "normal")
    genetics = profile.get("genetics", {}) # e.g. {"CYP2D6": "poor"}

    # 1. RENAL ADJUSTMENT (eGFR)
    if egfr < 60:
        for meta in [drug_a_meta, drug_b_meta]:
            if not meta:
                continue
            d_class = meta.get("class", "")
            d_name = meta.get("name", "")
            
            if d_class == "NSAID":
                adj_score += 0.25
                warnings.append(f"RENAL WARNING: {d_name.capitalize()} (NSAID) poses significant AKI risk at eGFR < 60.")
            elif d_class == "Antidiabetic" and d_name.lower() == "metformin" and egfr < 30:
                adj_score += 0.4
                warnings.append("CRITICAL: Metformin contraindicated at eGFR < 30 due to Lactic Acidosis risk.")
            elif d_class in RENAL_SENSITIVE_CLASSES:
                adj_score += 0.1
                warnings.append(f"REDUCED CLEARANCE: {d_name.capitalize()} requires dosage monitoring due to renal impairment.")

    # 2. GERIATRIC ADJUSTMENT (BEERS CRITERIA)
    if age > 65:
        for meta in [drug_a_meta, drug_b_meta]:
            if not meta:
                continue
            d_class = meta.get("class", "")
            d_name = meta.get("name", "")
            
            if d_class in BEERS_CRITERIA_CLASSES:
                adj_score += 0.2
                warnings.append(f"GERIATRIC ALERT: {d_name.capitalize()} is on the Beers List - increased risk of falls, sedation, and confusion in patients > 65.")
            elif d_class == "NSAID":
                adj_score += 0.15
                warnings.append(f"GERIATRIC ALERT: Chronic NSAID use in elderly increases GI bleed risk.")

    # 3. HEPATIC ADJUSTMENT
    if liver_status == "impaired":
        for meta in [drug_a_meta, drug_b_meta]:
            if not meta:
                continue
            d_class = meta.get("class", "")
            d_name = meta.get("name", "")
            
            if d_class in HEPATIC_SENSITIVE_CLASSES:
                adj_score += 0.3
                warnings.append(f"HEPATIC RISK: {d_name.capitalize()} metabolism is significantly reduced in hepatic impairment.")

    # 4. PHARMACOGENOMIC ADJUSTMENT
    for enzyme, status in genetics.items():
        if status == "poor":
            for meta in [drug_a_meta, drug_b_meta]:
                if not meta:
                    continue
                if enzyme in meta.get("cyp", []):
                    d_name = meta.get("name", "")
                    
                    # Prodrug check (Codeine -> Morphine)
                    if d_name.lower() == "codeine" and enzyme == "CYP2D6":
                        warnings.append("GENETIC ALERT: Codeine may have reduced efficacy due to CYP2D6 Poor Metabolizer status.")
                    else:
                        adj_score += 0.3
                        warnings.append(f"TOXICITY ALERT: Increased {d_name.capitalize()} plasma levels expected (Poor {enzyme} Metabolizer).")

    # Clamp score to 1.0
    final_score = min(1.0, round(adj_score, 2))
    return final_score, warnings
