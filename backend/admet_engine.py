import os
import pickle
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Note: In a real system, multiple models for different toxins (Liver, Heart, etc) would be loaded here.
MODEL_PATH = os.path.join(BASE_DIR, 'toxicity_model.pkl')

class ADMETEngine:
    def __init__(self):
        self.model = None
        self.is_loaded = False
        self._load_model()
        
    def _load_model(self):
        if os.path.exists(MODEL_PATH):
            try:
                with open(MODEL_PATH, 'rb') as f:
                    self.model = pickle.load(f)
                self.is_loaded = True
                print(f"[ADMET-INFO] Toxicity model loaded successfully.")
            except Exception as e:
                print(f"[ADMET-ERROR] Failed to load toxicity model: {e}")
        else:
            print(f"[ADMET-WARNING] Toxicity model not found at {MODEL_PATH}")

    def get_fingerprint(self, smiles, n_bits=2048):
        try:
            mol = Chem.MolFromSmiles(smiles)
            if mol:
                fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=n_bits)
                return np.array(fp).reshape(1, -1)
            return None
        except:
            return None

    def predict_toxicity(self, smiles):
        """Returns the toxicity probability score (0 to 1)"""
        if not self.is_loaded or not self.model:
            return {"score": 0.0, "level": "Unknown", "error": "Model not loaded"}
            
        fp = self.get_fingerprint(smiles)
        if fp is None:
            return {"score": 0.0, "level": "Unknown", "error": "Invalid SMILES"}
            
        # Get probability of class 1 (Toxic)
        prob = self.model.predict_proba(fp)[0][1]
        
        # Risk levels
        level = "Low"
        if prob > 0.7:
            level = "High"
        elif prob > 0.4:
            level = "Medium"
            
        return {
            "score": round(float(prob), 4),
            "level": level,
            "marker": "Endocrine Disruption Potential (NR-ER)"
        }

# Singleton instance
ADMET_ENGINE = ADMETEngine()
