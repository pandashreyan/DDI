import logging

logger = logging.getLogger(__name__)

def analyze_lifestyle_interactions(drug_list_meta, lifestyle_profile):
    """
    Analyzes interactions between drugs and lifestyle factors (Alcohol, Tobacco, Diet).
    Returns a list of lifestyle warnings.
    """
    if not lifestyle_profile:
        return []

    warnings = []
    
    alcohol = lifestyle_profile.get("alcohol", "none") # none, social, frequent
    tobacco = lifestyle_profile.get("tobacco", False)
    grapefruit = lifestyle_profile.get("grapefruit", False)
    dairy = lifestyle_profile.get("dairy", False)

    for meta in drug_list_meta:
        name = meta.get("name", "").lower()
        d_class = meta.get("class", "")
        cyp = meta.get("cyp", [])

        # 1. ALCOHOL INTERACTIONS
        if alcohol != "none":
            # CNS Depression Synergy
            cns_depressants = ["Opioid", "Benzodiazepine", "Muscle Relaxant", "Antipsychotic", "Tricyclic Antidepressant", "SNRI", "SSRI"]
            if d_class in cns_depressants:
                warnings.append({
                    "factor": "Alcohol",
                    "drug": name,
                    "severity": "high",
                    "msg": f"CRITICAL: Alcohol combined with {name.capitalize()} ({d_class}) exponentially increases respiratory depression and sedation risk."
                })
            
            # Disulfiram-like reactions
            disulfiram_drugs = ["metronidazole", "tinidazole", "sulfamethoxazole", "cefotetan"]
            if name in disulfiram_drugs:
                warnings.append({
                    "factor": "Alcohol",
                    "drug": name,
                    "severity": "severe",
                    "msg": f"ABSOLUTE CONTRAINDICATION: Alcohol + {name.capitalize()} causes severe nausea, vomiting, and tachycardia (Disulfiram-like reaction)."
                })
            
            # GI Bleed Risk
            if d_class == "NSAID":
                warnings.append({
                    "factor": "Alcohol",
                    "drug": name,
                    "severity": "moderate",
                    "msg": f"GI ALERT: Alcohol increases the risk of gastric ulcers and bleeding when taken with {name.capitalize()}."
                })

        # 2. TOBACCO (CYP1A2 Induction)
        if tobacco:
            if "CYP1A2" in cyp:
                warnings.append({
                    "factor": "Tobacco",
                    "drug": name,
                    "severity": "moderate",
                    "msg": f"METABOLISM ALERT: Tobacco smoke induces CYP1A2, significantly lowering blood levels (and efficacy) of {name.capitalize()}."
                })

        # 3. GRAPEFRUIT (CYP3A4 Inhibition)
        if grapefruit:
            if "CYP3A4" in cyp:
                # Statins are particularly sensitive
                sev = "high" if d_class == "Statin" else "moderate"
                warnings.append({
                    "factor": "Grapefruit",
                    "drug": name,
                    "severity": sev,
                    "msg": f"BIOAVAILABILITY ALERT: Grapefruit juice inhibits CYP3A4, potentially causing toxic levels of {name.capitalize()} in the blood."
                })

        # 4. DAIRY (Chelation)
        if dairy:
            chelation_classes = ["Fluoroquinolone", "Tetracycline"]
            if d_class in chelation_classes or name == "levothyroxine":
                warnings.append({
                    "factor": "Dairy/Calcium",
                    "drug": name,
                    "severity": "moderate",
                    "msg": f"ABSORPTION ALERT: Calcium in dairy products binds to {name.capitalize()}, preventing it from being absorbed correctly. Separate by 2-4 hours."
                })

    return warnings
