import json
import os
import re

def refine_metadata():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    meta_path = os.path.join(base_dir, 'drug_metadata.json')
    expert_path = os.path.join(base_dir, 'expert_interactions.json')
    
    if not os.path.exists(meta_path) or not os.path.exists(expert_path):
        print("[!] Files missing.")
        return

    with open(meta_path, 'r') as f:
        metadata = json.load(f)
    
    with open(expert_path, 'r') as f:
        expert_data = json.load(f)

    # 1. Map drug names to potential classes and CYPs found in mechanisms
    refinement_map = {}
    
    # Common CYP keywords
    cyp_keywords = ["CYP3A4", "CYP2C9", "CYP2D6", "CYP2C19", "CYP1A2", "CYP2E1"]
    
    for item in expert_data:
        for d in [item['drug_a'], item['drug_b']]:
            d = d.lower().strip()
            if d not in refinement_map:
                refinement_map[d] = {"cyp": set(), "class": None}
            
            # Extract CYP mentions
            mech = item['mechanism']
            for cyp in cyp_keywords:
                if cyp in mech:
                    refinement_map[d]["cyp"].add(cyp)
            
            # Extract Class hints from management or mechanism (if specific words used)
            # e.g. "Statin", "PPI", "NSAID", "Beta-blocker"
            common_classes = ["Statin", "PPI", "NSAID", "Beta-blocker", "Anticoagulant", "Antiviral", "Antidiabetic", "SSRI", "SNRI", "Opioid"]
            for cls in common_classes:
                if cls in mech or cls in item['management']:
                    refinement_map[d]["class"] = cls

    # 2. Update Metadata
    updates = 0
    for drug, info in refinement_map.items():
        if drug in metadata:
            # Update CYP
            if info['cyp']:
                existing_cyp = set(metadata[drug].get('cyp', []))
                new_cyp = list(existing_cyp | info['cyp'])
                if len(new_cyp) > len(existing_cyp):
                    metadata[drug]['cyp'] = new_cyp
                    updates += 1
            
            # Update Class if it was "General Therapeutics" or missing
            if info['class'] and (metadata[drug].get('class') == "General Therapeutics" or not metadata[drug].get('class')):
                metadata[drug]['class'] = info['class']
                updates += 1

    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    
    print(f"[SUCCESS] Metadata refined: {updates} fields updated across {len(metadata)} drugs.")

if __name__ == "__main__":
    refine_metadata()
