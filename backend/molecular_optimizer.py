import os
import json
import numpy as np
from rdkit import Chem
from rdkit.Chem import AllChem, Descriptors, rdMolDescriptors
from rdkit.Chem.rdChemReactions import ChemicalReaction

# We import the existing engines for screening
# Note: These will be imported inside methods to avoid circular dependencies if needed
# from admet_engine import ADMET_ENGINE

class MolecularOptimizer:
    def __init__(self):
        # Define a library of medicinal chemistry transformations (SMARTS-based)
        # Transformation format: (name, smarts_reaction, description)
        self.transformations = [
            ("F-Stabilization", "[c:1][H:2]>>[c:1][F:2]", "Replacing aromatic hydrogen with fluorine to increase metabolic stability."),
            ("Hydroxyl-Polarity", "[C:1][H:2]>>[C:1][O][H]", "Adding a hydroxyl group to increase solubility and potentially reduce off-target toxicity."),
            ("Pyridine-Switch", "[c:1]1[c:2][c:3][c:4][c:5][c:6]1>>[c:1]1[n:2][c:3][c:4][c:5][c:6]1", "Bioisosteric swap of Phenyl to Pyridine to reduce lipophilicity."),
            ("CF3-Enhancement", "[C:1][H:2]>>[C:1](F)(F)F", "Adding a trifluoromethyl group to modulate binding affinity and distribution."),
            ("De-Halogenation", "[Cl,Br,I:1]>>[H]", "Removing heavy halogens to reduce potential environmental toxicity or metabolic reactivity."),
            ("Methyl-Shift", "[c:1][H:2]>>[c:1][C]", "Adding a methyl group to fill a hydrophobic pocket (Magic Methyl effect)."),
        ]
        
    def _apply_transformation(self, mol, reaction_smarts):
        try:
            rxn = AllChem.ReactionFromSmarts(reaction_smarts)
            products = rxn.RunReactants((mol,))
            valid_products = []
            for prod in products:
                p = prod[0]
                try:
                    Chem.SanitizeMol(p)
                    valid_products.append(p)
                except:
                    continue
            return valid_products
        except:
            return []

    def optimize(self, smiles, target_other_smiles=None, admet_engine=None, ddi_model_func=None):
        """
        Generates and ranks derivatives based on safety gains.
        """
        original_mol = Chem.MolFromSmiles(smiles)
        if not original_mol:
            return {"error": "Invalid SMILES"}

        # 1. Get original scores
        original_tox = admet_engine.predict_toxicity(smiles) if admet_engine else {"score": 0.5}
        
        results = []
        seen_smiles = {Chem.MolToSmiles(original_mol)}

        for name, smat, desc in self.transformations:
            derivatives = self._apply_transformation(original_mol, smat)
            
            for d_mol in derivatives:
                d_smiles = Chem.MolToSmiles(d_mol)
                if d_smiles in seen_smiles:
                    continue
                seen_smiles.add(d_smiles)

                # 2. Check Drug-Likeness (Lipinski-ish)
                mw = Descriptors.MolWt(d_mol)
                logp = Descriptors.MolLogP(d_mol)
                hbd = rdMolDescriptors.CalcNumHBD(d_mol)
                hba = rdMolDescriptors.CalcNumHBA(d_mol)
                
                # Loose filters to keep it "drug-like"
                if mw > 600 or logp > 6.0:
                    continue

                # 3. Predict Safety Gains
                safety_improvement = 0
                tox_data = {}
                
                if admet_engine:
                    tox_data = admet_engine.predict_toxicity(d_smiles)
                    # Improvement in toxicity score (lower is better)
                    safety_improvement += (original_tox['score'] - tox_data['score']) * 100

                # DDI Improvement (if other drug smiles provided)
                ddi_gain = 0
                if ddi_model_func and target_other_smiles:
                    # This would involve predicting the DDI between derivative and original partner
                    pass 

                results.append({
                    "name": f"{name} Derivative",
                    "smiles": d_smiles,
                    "description": desc,
                    "metrics": {
                        "mw": round(mw, 2),
                        "logp": round(logp, 2),
                        "hbd": hbd,
                        "hba": hba
                    },
                    "safety": {
                        "toxicity": tox_data,
                        "improvement_score": round(safety_improvement, 2)
                    }
                })

        # Rank by safety improvement
        results.sort(key=lambda x: x['safety']['improvement_score'], reverse=True)
        
        return {
            "original": {
                "smiles": smiles,
                "toxicity": original_tox
            },
            "optimized_derivatives": results[:3] # Return top 3
        }

# Singleton
MOLECULAR_OPTIMIZER = MolecularOptimizer()
