import pandas as pd
import os
import re
import json
from tqdm import tqdm

DB_PATH = os.path.join('db_drug_interactions.csv', 'db_drug_interactions.csv')
TAB_PATH = os.path.join('data', 'drugbank.tab')
OUTPUT_MAP = 'drug_smiles_map.json'

def generate_mapping():
    print(f"[*] Starting Fuzzy structural-clinical mapping...")
    if not os.path.exists(TAB_PATH) or not os.path.exists(DB_PATH):
        print("[!] Files missing.")
        return

    # 1. Load drugbank.tab and build pattern lookup
    # Map: Pattern -> list of (ID1, SMILES1, ID2, SMILES2)
    print("[*] Indexing drugbank.tab patterns...")
    tab_df = pd.read_csv(TAB_PATH, sep='\t')
    pattern_to_smiles = {}
    
    # Sample 40k rows to get a good spread of patterns
    for _, row in tqdm(tab_df.sample(min(40000, len(tab_df))).iterrows(), total=min(40000, len(tab_df))):
        pat = str(row['Map']).strip()
        if pat not in pattern_to_smiles:
            pattern_to_smiles[pat] = []
        pattern_to_smiles[pat].append((row['X1'], row['X2']))

    # 2. Load Clinical CSV and find matches
    print("[*] Cross-referencing CSV descriptions with patterns...")
    db_df = pd.read_csv(DB_PATH)
    smiles_map = {} # Name -> SMILES
    
    # We only need to process a few thousand rows to get most drug names
    # Priority: Rows that match known patterns
    for _, row in tqdm(db_df.head(100000).iterrows(), total=100000):
        desc = str(row['Interaction Description']).strip()
        d1, d2 = str(row['Drug 1']).strip().lower(), str(row['Drug 2']).strip().lower()
        
        # Heuristic: Replace names with placeholders to see if it matches a pattern
        # This is tricky because the description might be slightly different.
        # But usually it's "Name1 Verb Name2." vs "#Drug1 Verb #Drug2."
        
        # Try a few common pattern translations
        pat_candidate = desc.replace(str(row['Drug 1']), "#Drug1").replace(str(row['Drug 2']), "#Drug2")
        
        if pat_candidate in pattern_to_smiles:
            # We found a match! Grab the first SMILES pair
            s1, s2 = pattern_to_smiles[pat_candidate][0]
            smiles_map[d1] = s1
            smiles_map[d2] = s2

    print(f"[*] Mapping complete. Resolved {len(smiles_map)} drug SMILES.")
    
    # 3. Save
    with open(OUTPUT_MAP, 'w') as f:
        json.dump(smiles_map, f)
    print(f"[*] Mapping saved to {OUTPUT_MAP}")

if __name__ == "__main__":
    generate_mapping()
