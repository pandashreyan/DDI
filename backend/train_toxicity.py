import pandas as pd
import numpy as np
import os
import pickle
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, f1_score

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRAIN_DIR = os.path.join(BASE_DIR, 'NR-ER-train')
TEST_DIR = os.path.join(BASE_DIR, 'NR-ER-test')
MODEL_PATH = os.path.join(BASE_DIR, 'toxicity_model.pkl')

def get_fingerprint(smiles, n_bits=2048):
    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=n_bits)
            return np.array(fp)
        return None
    except:
        return None

def load_and_preprocess(data_dir):
    print(f"[DDI-ML] Loading data from {data_dir}...")
    smiles_df = pd.read_csv(os.path.join(data_dir, 'names_smiles.csv'), header=None, names=['id', 'smiles'])
    labels_df = pd.read_csv(os.path.join(data_dir, 'names_labels.csv'), header=None, names=['id', 'label'])
    
    df = pd.merge(smiles_df, labels_df, on='id')
    print(f"[DDI-ML] Total samples: {len(df)}")
    
    # Generate fingerprints
    print("[DDI-ML] Generating fingerprints (this may take a minute)...")
    fps = []
    labels = []
    
    for i, row in df.iterrows():
        fp = get_fingerprint(row['smiles'])
        if fp is not None:
            fps.append(fp)
            labels.append(row['label'])
            
    return np.array(fps), np.array(labels)

def train_toxicity():
    X, y = load_and_preprocess(TRAIN_DIR)
    
    print(f"[DDI-ML] Training on {len(X)} valid samples.")
    print(f"[DDI-ML] Class distribution: {np.bincount(y)}")
    
    # To handle imbalance, we use class_weight='balanced'
    model = RandomForestClassifier(n_estimators=100, class_weight='balanced', n_jobs=-1, random_state=42)
    
    # Split for internal validation
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)
    
    print("[DDI-ML] Fitting model...")
    model.fit(X_train, y_train)
    
    # internal Val
    y_pred = model.predict(X_val)
    print("\n--- Internal Validation ---")
    print(classification_report(y_val, y_pred))
    print(f"ROC-AUC: {roc_auc_score(y_val, model.predict_proba(X_val)[:, 1]):.4f}")
    
    # Final eval on the official test set
    try:
        X_test, y_test = load_and_preprocess(TEST_DIR)
        y_test_pred = model.predict(X_test)
        print("\n--- Official Test Set Results ---")
        print(classification_report(y_test, y_test_pred))
        print(f"ROC-AUC: {roc_auc_score(y_test, model.predict_proba(X_test)[:, 1]):.4f}")
    except Exception as e:
        print(f"[DDI-ML] Official Test set evaluation failed: {e}")

    # Save model
    print(f"[DDI-ML] Saving model to {MODEL_PATH}")
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
    
    print("[DDI-ML] Model export complete.")

if __name__ == "__main__":
    train_toxicity()
