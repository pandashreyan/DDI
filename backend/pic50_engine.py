import os
import joblib
import pandas as pd
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

MODEL_PATH = os.path.join(os.path.dirname(__file__), "pic50_model.pkl")
DATA_PATH = os.path.join(os.path.dirname(__file__), "db_drug_interactions.csv", "SMILES_Big_Data_Set.csv")

class PotencyPredictor:
    def __init__(self):
        self.model = None

    def load_or_train(self, force_retrain=False):
        if not force_retrain and os.path.exists(MODEL_PATH):
            print(f"[pIC50-ENGINE] Loading cached model from {MODEL_PATH}")
            self.model = joblib.load(MODEL_PATH)
            return True

        if not os.path.exists(DATA_PATH):
            print("[pIC50-ENGINE] WARNING: Training data not found. Potency engine disabled.")
            return False

        print("[pIC50-ENGINE] Training pIC50 Regressor on SMILES_Big_Data_Set.csv (Large Dataset) ... this may take 20s.")
        df = pd.read_csv(DATA_PATH)
        
        # Sample to 8000 for fast RAM training if huge, else all
        if len(df) > 8000:
            df = df.sample(8000, random_state=42)

        X_fps = []
        Y = []
        for i, row in df.iterrows():
            smi = row.get("SMILES")
            pic50 = row.get("pIC50")
            if not smi or pd.isna(pic50): continue
            
            mol = Chem.MolFromSmiles(str(smi))
            if mol:
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
                arr = np.zeros((1,))
                Chem.DataStructs.ConvertToNumpyArray(fp, arr)
                X_fps.append(arr)
                Y.append(float(pic50))

        if not X_fps:
            return False

        X_train = np.array(X_fps)
        Y_train = np.array(Y)

        # Train a light regressor
        self.model = RandomForestRegressor(n_estimators=100, max_depth=15, n_jobs=-1, random_state=42)
        self.model.fit(X_train, Y_train)

        joblib.dump(self.model, MODEL_PATH)
        print("[pIC50-ENGINE] Model trained and cached successfully.")
        return True

    def predict(self, smiles):
        if not self.model:
            return {"error": "Model not loaded"}

        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return {"error": "Invalid SMILES structure"}

        fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
        arr = np.zeros((1,))
        Chem.DataStructs.ConvertToNumpyArray(fp, arr)

        # Predict
        pic50_pred = self.model.predict([arr])[0]

        # Convert to roughly nM IC50
        # pIC50 = -log10(IC50 in M) -> IC50 in nM = 10^(9 - pIC50)
        ic50_nm = 10 ** (9 - pic50_pred)

        # Interpret clinical potency qualitative
        if pic50_pred > 8.0:
            level = "Ultra-Potent (Sub-nM to low nM)"
        elif pic50_pred > 6.0:
            level = "High Potency"
        elif pic50_pred > 5.0:
            level = "Moderate Potency"
        else:
            level = "Weak / Non-Targeted"

        return {
            "pIC50": round(float(pic50_pred), 3),
            "estimated_IC50_nM": round(float(ic50_nm), 2),
            "potency_class": level
        }

# Global Instance
PIC50_ENGINE = PotencyPredictor()

if __name__ == "__main__":
    PIC50_ENGINE.load_or_train(force_retrain=True)
    res = PIC50_ENGINE.predict("CC(=O)Oc1ccccc1C(=O)O") # Aspirin
    print(f"Aspirin Test: {res}")
