import logging
from datetime import datetime

logger = logging.getLogger(__name__)

# Clinical Category Definitions
ABSORPTION_BLOCKERS = ["PPI", "H2 Receptor Antagonist", "Antacid"]
SENSITIVE_ABSORPTION = ["Thyroid Hormone", "Fluoroquinolone", "Bisphosphonate"]
CNS_DEPRESSANTS = ["Opioid", "Benzodiazepine", "Muscle Relaxant", "Tricyclic Antidepressant", "Antipsychotic"]

def optimize_regimen(drug_names, drug_metadata):
    """
    Analyzes a collection of drugs and suggests an optimized administration schedule.
    """
    if len(drug_names) < 2:
        return None

    # 1. Group drugs by clinical characteristics
    blockers = []
    sensitive = []
    cns_active = []
    others = []

    active_meta = []
    for name in drug_names:
        meta = drug_metadata.get(name.lower())
        if not meta:
            continue
        active_meta.append(meta)
        
        d_class = meta.get("class", "")
        if d_class in ABSORPTION_BLOCKERS:
            blockers.append(meta)
        elif d_class in SENSITIVE_ABSORPTION:
            sensitive.append(meta)
        
        if d_class in CNS_DEPRESSANTS:
            cns_active.append(meta)
        
        if d_class not in ABSORPTION_BLOCKERS and d_class not in SENSITIVE_ABSORPTION:
            others.append(meta)

    # 2. Build Schedule (Simplified 4-slot model)
    # Morning (08:00), Noon (12:00), Evening (18:00), Night (22:00)
    schedule = {
        "morning": [],
        "noon": [],
        "evening": [],
        "night": []
    }
    
    advice = []

    # Rule: Thyroid hormones always Morning (Fasted)
    for s in sensitive:
        if s.get("class") == "Thyroid Hormone":
            schedule["morning"].append(s["name"])
            advice.append(f"Take {s['name'].capitalize()} at least 30-60 mins before breakfast for optimal absorption.")

    # Rule: PPIs usually Morning (Fasted)
    for b in blockers:
        if b.get("class") == "PPI":
            schedule["morning"].append(b["name"])
            advice.append(f"Take {b['name'].capitalize()} on an empty stomach, 30 mins before your first meal.")
        else:
            schedule["noon"].append(b["name"])

    # Rule: CNS Depressants preferably Evening/Night
    for c in cns_active:
        schedule["night"].append(c["name"])
        advice.append(f"Take {c['name'].capitalize()} before bed as it may cause drowsiness.")

    # Rule: Distribute others
    for o in others:
        if o["name"] not in [item for sublist in schedule.values() for item in sublist]:
            if not schedule["noon"]:
                schedule["noon"].append(o["name"])
            elif not schedule["morning"]:
                schedule["morning"].append(o["name"])
            else:
                schedule["evening"].append(o["name"])

    # 3. Analyze Cumulative Risks (Synergies)
    synergies = []
    if len(cns_active) >= 2:
        synergies.append({
            "type": "CNS Depression",
            "severity": "high",
            "msg": f"Cumulative sedation risk detected between {', '.join([c['name'] for c in cns_active])}. Monitor for respiratory depression."
        })

    # Bleeding risk synergy
    bleeding_risk_classes = ["Anticoagulant", "Antiplatelet", "NSAID", "SSRI"]
    bleeding_drugs = [m for m in active_meta if m.get("class") in bleeding_risk_classes]
    if len(bleeding_drugs) >= 2:
        synergies.append({
            "type": "Increased Hemorrhage Risk",
            "severity": "moderate",
            "msg": f"Additive bleeding risk from multiple agents: {', '.join([d['name'] for d in bleeding_drugs])}."
        })

    return {
        "schedule": schedule,
        "advice": advice,
        "synergies": synergies,
        "regimen_score": round(min(1.0, 0.1 * len(drug_names) + (0.2 if synergies else 0)), 2)
    }
