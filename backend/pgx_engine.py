"""
Pharmacogenomics (PGx) Engine
Adjusts drug interaction risks based on patient genetic profile.
"""

import logging

logger = logging.getLogger(__name__)

# Genetic variations and their impacts on specific metabolic pathways
# Values represent risk multiplier for the interaction score
PGX_RULES = {
    "CYP2C19": {
        "poor_metabolizer": {
            "impact_on": ["clopidogrel", "omeprazole", "citalopram", "voriconazole"],
            "multiplier": 1.5,
            "warning": "Poor metabolizer status may lead to reduced conversion of prodrugs (e.g. clopidogrel) or toxicity of substrates."
        },
        "ultra_rapid_metabolizer": {
            "impact_on": ["clopidogrel", "citalopram"],
            "multiplier": 1.3,
            "warning": "Ultra-rapid metabolizer status may lead to excessive metabolite levels or reduced therapeutic effect."
        }
    },
    "CYP2D6": {
        "poor_metabolizer": {
            "impact_on": ["codeine", "tamoxifen", "fluoxetine", "metoprolol", "venlafaxine"],
            "multiplier": 1.6,
            "warning": "Poor metabolizer status significantly impairs conversion of codeine to morphine and increases risk from beta-blockers."
        },
        "ultra_rapid_metabolizer": {
            "impact_on": ["codeine", "tramadol"],
            "multiplier": 2.0,
            "warning": "CRITICAL: Ultra-rapid metabolism of codeine leads to rapid morphine toxicity risk."
        }
    },
    "SLCO1B1": {
        "decreased_function": {
            "impact_on": ["simvastatin", "atorvastatin", "rosuvastatin"],
            "multiplier": 1.8,
            "warning": "Genetic variant detected: Increased risk of statin-induced myopathy (muscle toxicity)."
        }
    }
}

def calculate_pgx_risk(base_score, drug_a_meta, drug_b_meta, genetic_profile):
    """
    Adjusts the interaction score based on patient genetic variants.
    """
    adjusted_score = base_score
    pgx_warnings = []
    
    if not genetic_profile:
        return adjusted_score, pgx_warnings
        
    drugs = [drug_a_meta, drug_b_meta]
    
    for variant, status in genetic_profile.items():
        if variant in PGX_RULES and status in PGX_RULES[variant]:
            rule = PGX_RULES[variant][status]
            
            # Check if either drug is impacted by this variant
            impacted_drugs = []
            for d in drugs:
                d_name = d.get('name', '').lower()
                d_cyp = d.get('cyp', [])
                
                # Direct match or enzyme overlap
                if d_name in rule['impact_on'] or variant in d_cyp:
                    impacted_drugs.append(d_name)
                    
            if impacted_drugs:
                adjusted_score *= rule['multiplier']
                pgx_warnings.append(f"PGx Warning ({variant} {status.replace('_',' ')}): {rule['warning']}")
                
    return min(1.0, adjusted_score), pgx_warnings
