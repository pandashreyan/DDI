"""
Multi-Organ Toxicity Prediction Engine
Predicts organ-specific toxicity risk from SMILES using:
  1. Known toxicophore substructure scanning (SMARTS)
  2. Molecular descriptor heuristics (MW, LogP, PSA, etc.)
  3. NR-ER ML model (existing ADMET engine) for endocrine axis

Organs covered:
  - Liver (Hepatotoxicity)
  - Heart (Cardiotoxicity / hERG)
  - Kidney (Nephrotoxicity)
  - Endocrine (NR-ER model)
"""

import numpy as np
from rdkit import Chem
from rdkit.Chem import Descriptors, rdMolDescriptors

# ──────────────────────────────────────────
#  TOXICOPHORE LIBRARIES (SMARTS patterns)
# ──────────────────────────────────────────

# Known structural alerts for hepatotoxicity (Liver)
HEPATOTOX_ALERTS = [
    ("[NX3][NX2]=[NX1]", "Azide group — mitochondrial toxin"),
    ("C(=O)Cl", "Acyl chloride — reactive hepatotoxin"),
    ("[N;X2]=[N;X2]", "Diazo compound — liver metabolism hazard"),
    ("c1cc(c(cc1[N+](=O)[O-])[N+](=O)[O-])", "Dinitrobenzene — hepatocyte damage"),
    ("[OH]c1ccccc1", "Phenol — potential quinone formation"),
    ("C=CC(=O)", "Michael acceptor — GSH depletion"),
    ("C(#N)", "Nitrile — cyanide release risk"),
    ("[N;X3](=O)=O", "Nitro group — nitroreductase activation"),
    ("S(=O)(=O)F", "Sulfonyl fluoride — reactive metabolite"),
    ("c1ccc2c(c1)c(=O)c1ccccc1o2", "Coumarin scaffold — hepatotoxicity marker"),
]

# Known structural alerts for cardiotoxicity (hERG channel binding)
CARDIOTOX_ALERTS = [
    ("c1ccc(cc1)CCN", "Phenylethylamine — hERG affinity"),
    ("c1ccc2c(c1)cccc2N", "Aminonaphthalene — QT prolongation risk"),
    ("C(=O)c1ccc(cc1)F", "Fluorophenyl ketone — cardiac ion channel blocker"),
    ("[N+](C)(C)C", "Quaternary amine — ion channel interaction"),
    ("c1cnc2ccccc2n1", "Quinazoline — hERG binding scaffold"),
    ("c1ccc2[nH]c3ccccc3c2c1", "Carbazole — hERG liability"),
    ("c1ccc(cc1)c2ccccn2", "2-Phenylpyridine — hERG risk"),
    ("c1c2ccccc2c3ccccc13", "Anthracene — cardiotoxin"),
]

# Known structural alerts for nephrotoxicity (Kidney)
NEPHROTOX_ALERTS = [
    ("OS(=O)(=O)O", "Sulfate ester — renal tubular toxin"),
    ("[As]", "Arsenic compound — nephrotoxin"),
    ("[Hg]", "Mercury compound — kidney damage"),
    ("[Cd]", "Cadmium compound — kidney damage"),
    ("[Pt]", "Platinum group — cisplatin-like nephrotoxicity"),
    ("C(=O)[O-]", "Carboxylate — potential crystal nephropathy"),
    ("c1cc(ccc1O)O", "Catechol — oxidative kidney stress"),
    ("CC(C)(C)OC(=O)", "Tert-butyl ester — renal metabolism load"),
]


class MultiOrganToxEngine:
    """Predicts organ-specific toxicity from SMILES."""

    def __init__(self):
        self._compile_patterns()

    def _compile_patterns(self):
        """Pre-compile SMARTS for speed."""
        self.hepato_pats = self._compile(HEPATOTOX_ALERTS)
        self.cardio_pats = self._compile(CARDIOTOX_ALERTS)
        self.nephro_pats = self._compile(NEPHROTOX_ALERTS)

    @staticmethod
    def _compile(alerts):
        compiled = []
        for smarts, desc in alerts:
            pat = Chem.MolFromSmarts(smarts)
            if pat:
                compiled.append((pat, desc))
        return compiled

    # ──────────────────────────────────────
    #  Per-organ prediction methods
    # ──────────────────────────────────────

    def _scan_alerts(self, mol, patterns):
        """Scan molecule against a list of compiled toxicophore patterns."""
        hits = []
        for pat, desc in patterns:
            if mol.HasSubstructMatch(pat):
                hits.append(desc)
        return hits

    def predict_hepatotoxicity(self, mol, smiles):
        """Predict risk of liver damage."""
        alerts = self._scan_alerts(mol, self.hepato_pats)
        # Descriptor heuristics: high lipophilicity and MW correlate with DILI
        logp = Descriptors.MolLogP(mol)
        mw = Descriptors.MolWt(mol)
        tpsa = Descriptors.TPSA(mol)

        score = len(alerts) * 0.15
        if logp > 3.0:
            score += 0.15
        if mw > 500:
            score += 0.10
        if tpsa < 75:  # poor solubility → liver accumulation
            score += 0.10
        score = min(score, 1.0)

        return {
            "score": round(score, 3),
            "level": self._level(score),
            "alerts": alerts[:3],
            "factors": {
                "logp": round(logp, 2),
                "mw": round(mw, 1),
                "tpsa": round(tpsa, 1)
            }
        }

    def predict_cardiotoxicity(self, mol, smiles):
        """Predict risk of QT prolongation / hERG liability."""
        alerts = self._scan_alerts(mol, self.cardio_pats)
        logp = Descriptors.MolLogP(mol)
        mw = Descriptors.MolWt(mol)
        n_rings = rdMolDescriptors.CalcNumAromaticRings(mol)
        hba = rdMolDescriptors.CalcNumHBA(mol)

        score = len(alerts) * 0.18
        # hERG blockers tend to be lipophilic, aromatic, basic
        if logp > 3.5:
            score += 0.12
        if n_rings >= 3:
            score += 0.10
        if hba <= 2 and logp > 2.5:
            score += 0.08
        score = min(score, 1.0)

        return {
            "score": round(score, 3),
            "level": self._level(score),
            "alerts": alerts[:3],
            "factors": {
                "logp": round(logp, 2),
                "aromatic_rings": n_rings,
                "hba": hba
            }
        }

    def predict_nephrotoxicity(self, mol, smiles):
        """Predict risk of kidney damage."""
        alerts = self._scan_alerts(mol, self.nephro_pats)
        mw = Descriptors.MolWt(mol)
        logp = Descriptors.MolLogP(mol)
        tpsa = Descriptors.TPSA(mol)

        score = len(alerts) * 0.20
        # Highly polar + high MW compounds stress renal clearance
        if tpsa > 140:
            score += 0.15
        if mw > 450 and logp < 0:
            score += 0.12
        score = min(score, 1.0)

        return {
            "score": round(score, 3),
            "level": self._level(score),
            "alerts": alerts[:3],
            "factors": {
                "mw": round(mw, 1),
                "tpsa": round(tpsa, 1),
                "logp": round(logp, 2)
            }
        }

    # ──────────────────────────────────────
    #  Master predict — all organs at once
    # ──────────────────────────────────────

    def predict_all(self, smiles, admet_engine=None):
        """Returns a dict with per-organ toxicity predictions."""
        mol = Chem.MolFromSmiles(smiles)
        if not mol:
            return {"error": "Invalid SMILES"}

        hepato = self.predict_hepatotoxicity(mol, smiles)
        cardio = self.predict_cardiotoxicity(mol, smiles)
        nephro = self.predict_nephrotoxicity(mol, smiles)

        # Endocrine — use existing ML model
        endo = {"score": 0.0, "level": "Unknown"}
        if admet_engine:
            endo = admet_engine.predict_toxicity(smiles)

        overall = max(hepato["score"], cardio["score"], nephro["score"], endo.get("score", 0))

        return {
            "hepatotoxicity": hepato,
            "cardiotoxicity": cardio,
            "nephrotoxicity": nephro,
            "endocrine": endo,
            "overall_score": round(overall, 3),
            "overall_level": self._level(overall)
        }

    @staticmethod
    def _level(score):
        if score >= 0.6:
            return "High"
        elif score >= 0.3:
            return "Medium"
        return "Low"


# Singleton
MULTI_ORGAN_TOX = MultiOrganToxEngine()
