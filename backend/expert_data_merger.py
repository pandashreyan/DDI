import json
import os

def merge_expert_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    json_dir = os.path.join(base_dir, 'db_drug_interactions.csv')
    
    file1 = os.path.join(json_dir, 'DDI 2.0.json')
    file2 = os.path.join(json_dir, 'DDI Database.json')
    output_file = os.path.join(base_dir, 'expert_interactions.json')
    
    merged_data = {}
    
    # 1. Process DDI 2.0.json
    if os.path.exists(file1):
        with open(file1, 'r') as f:
            data = json.load(f)
            for item in data.get('ddi_database', []):
                d1 = item['drug_a'].lower().strip()
                d2 = item['drug_b'].lower().strip()
                pair = tuple(sorted([d1, d2]))
                
                merged_data[pair] = {
                    "drug_a": d1,
                    "drug_b": d2,
                    "severity": item.get('severity', 'Moderate').title(),
                    "mechanism": item.get('mechanism', ''),
                    "effect": item.get('clinical_effect', ''),
                    "safer_alternative": item.get('safer_alternative', ''),
                    "management": item.get('clinical_management', ''),
                    "reference": item.get('reference', '')
                }
    
    # 2. Process DDI Database.json (Enriching existing or adding new)
    if os.path.exists(file2):
        with open(file2, 'r') as f:
            data = json.load(f)
            # This file has 'major', 'moderate' keys
            interactions = data.get('drug_interactions', {})
            for sev_key in ['major', 'moderate', 'minor']:
                for item in interactions.get(sev_key, []):
                    d1 = item['drug_a'].lower().strip()
                    d2 = item['drug_b'].lower().strip()
                    pair = tuple(sorted([d1, d2]))
                    
                    if pair in merged_data:
                        # Update missing fields or refine
                        existing = merged_data[pair]
                        if not existing['safer_alternative']:
                            existing['safer_alternative'] = item.get('Safer_alternative', '')
                        if not existing['management']:
                            existing['management'] = item.get('rationale', '')
                    else:
                        merged_data[pair] = {
                            "drug_a": d1,
                            "drug_b": d2,
                            "severity": item.get('severity', sev_key.title()).title(),
                            "mechanism": item.get('mechanism', ''),
                            "effect": item.get('effect', ''),
                            "safer_alternative": item.get('Safer_alternative', ''),
                            "management": item.get('rationale', ''),
                            "reference": item.get('reference', '')
                        }
    
    # Convert back to list for JSON export
    final_list = list(merged_data.values())
    
    with open(output_file, 'w') as f:
        json.dump(final_list, f, indent=2)
    
    print(f"[SUCCESS] Expert interactions merged: {len(final_list)} pairs saved to {output_file}")

if __name__ == "__main__":
    merge_expert_data()
