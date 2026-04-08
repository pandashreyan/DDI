"""
AI Training Pipeline for Drug-Drug Interaction (DDI)
Source: Therapeutics Data Commons (TDC) - DrugBank Dataset
Model: RandomForestClassifier with Morgan Fingerprints
"""

import pandas as pd
import numpy as np
from tdc.multi_pred import DDI
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
import pickle
import os
from tqdm import tqdm
import re
import json

def get_features(smiles, mw=None, logp=None):
    """Generate 1024-bit Morgan Fingerprint + Physical Properties"""
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol is not None:
            # 1024-bit Morgan Fingerprint (Radius 2)
            fp_vec = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
            fp = np.array(fp_vec)
            
            # Append MW and LogP as features (scaled/normalized ideally, but raw is a start)
            # Default to average drug values if not provided
            mw_val = mw if mw is not None else 300.0
            logp_val = logp if logp is not None else 2.5
            
            # Concatenate
            return np.append(fp, [mw_val / 500.0, logp_val / 5.0]) # Simple normalization
    except:
        pass
    return np.zeros(1026)

def train():
    print("[*] Ingesting localized expanded database...")
    DB_PATH = os.path.join('db_drug_interactions.csv', 'db_drug_interactions.csv')
    EXPERT_PATH = 'expert_interactions.json'
    
    if not os.path.exists(DB_PATH):
        print("[!] CSV data file missing. Aborting training.")
        return

    # Load pre-generated mapping
    MAP_FILE = 'drug_smiles_map.json'
    if os.path.exists(MAP_FILE):
        with open(MAP_FILE, 'r') as f:
            smiles_map = json.load(f)
    else:
        smiles_map = {}
            
    expanded_df = pd.read_csv(DB_PATH)
    print(f"[*] Expanded Dataset loaded: {len(expanded_df)} interaction pairs.")
    
    # Load Expert Data
    expert_pairs = []
    if os.path.exists(EXPERT_PATH):
        with open(EXPERT_PATH, 'r') as f:
            expert_data = json.load(f)
            for item in expert_data:
                expert_pairs.append({
                    "Drug 1": item['drug_a'],
                    "Drug 2": item['drug_b'],
                    "weight": 5
                })
        print(f"[*] Expert Interactions loaded: {len(expert_pairs)} pairs.")

    known_positives = set()
    for _, row in expanded_df.iterrows():
        known_positives.add(frozenset([str(row['Drug 1']).lower().strip(), str(row['Drug 2']).lower().strip()]))
    for item in expert_pairs:
        known_positives.add(frozenset([item['Drug 1'].lower().strip(), item['Drug 2'].lower().strip()]))

    unique_drugs = [d for d in (set(expanded_df['Drug 1'].str.lower()) | set(expanded_df['Drug 2'].str.lower())) if d in smiles_map]
    
    X = []
    y = []
    weights = []
    
    print("[*] Generating Positive Samples...")
    
    # Expert Data
    for item in expert_pairs:
        d1, d2 = item['Drug 1'].lower(), item['Drug 2'].lower()
        s1, s2 = smiles_map.get(d1), smiles_map.get(d2)
        if s1 and s2:
            m1, m2 = Chem.MolFromSmiles(s1), Chem.MolFromSmiles(s2)
            if m1 and m2:
                mw1, lp1 = Descriptors.MolWt(m1), Descriptors.MolLogP(m1)
                mw2, lp2 = Descriptors.MolWt(m2), Descriptors.MolLogP(m2)
                f1 = get_features(s1, mw1, lp1)
                f2 = get_features(s2, mw2, lp2)
                X.append(np.concatenate([f1, f2]))
                y.append(1)
                weights.append(item['weight'])

    # CSV Data
    subset_df = expanded_df.sample(min(15000, len(expanded_df)), random_state=42)
    for _, row in tqdm(subset_df.iterrows(), total=len(subset_df), desc="CSV Positives"):
        d1, d2 = str(row['Drug 1']).strip().lower(), str(row['Drug 2']).strip().lower()
        s1, s2 = smiles_map.get(d1), smiles_map.get(d2)
        if s1 and s2:
            m1, m2 = Chem.MolFromSmiles(s1), Chem.MolFromSmiles(s2)
            if m1 and m2:
                mw1, lp1 = Descriptors.MolWt(m1), Descriptors.MolLogP(m1)
                mw2, lp2 = Descriptors.MolWt(m2), Descriptors.MolLogP(m2)
                f1 = get_features(s1, mw1, lp1)
                f2 = get_features(s2, mw2, lp2)
                X.append(np.concatenate([f1, f2]))
                y.append(1)
                weights.append(1)

    pos_count = len(y)
    print(f"[*] Generating {pos_count} Negative Samples...")
    neg_added = 0
    import random
    while neg_added < pos_count:
        d1, d2 = random.sample(unique_drugs, 2)
        if frozenset([d1, d2]) not in known_positives:
            s1, s2 = smiles_map.get(d1), smiles_map.get(d2)
            m1, m2 = Chem.MolFromSmiles(s1), Chem.MolFromSmiles(s2)
            if m1 and m2:
                mw1, lp1 = Descriptors.MolWt(m1), Descriptors.MolLogP(m1)
                mw2, lp2 = Descriptors.MolWt(m2), Descriptors.MolLogP(m2)
                f1 = get_features(s1, mw1, lp1)
                f2 = get_features(s2, mw2, lp2)
                X.append(np.concatenate([f1, f2]))
                y.append(0)
                weights.append(1)
                neg_added += 1

    X = np.array(X)
    y = np.array(y)
    weights = np.array(weights)
    
    print(f"[*] Training Upgraded RandomForest on {len(X)} samples...")
    # Stratified split if needed, but simple is fine for now
    X_train, X_test, y_train, y_test, w_train, w_test = train_test_split(X, y, weights, test_size=0.2, random_state=42)
    
    model = RandomForestClassifier(n_estimators=100, n_jobs=-1, random_state=42)
    model.fit(X_train, y_train, sample_weight=w_train)
    
    y_pred = model.predict(X_test)
    print("\nModel Performance:")
    print(classification_report(y_test, y_pred))
    
    try:
        auc = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
        print(f"ROC-AUC Score: {auc:.4f}")
    except:
        pass

    model_path = 'ddi_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Upgraded AI Model saved to {model_path}")

if __name__ == "__main__":
    train()
