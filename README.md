# DDI Predict Analytics Suite

> Predicting and visualizing drug–drug interactions using machine learning and clinical heuristics — before they reach the patient.

**Live demo:** [ddi-lcyj.onrender.com](https://ddi-lcyj.onrender.com)

---

## Overview

Polypharmacy is dangerous. **DDI Predict** combines deterministic FDA evidence databases with predictive machine learning algorithms to identify, analyze, and mitigate complex medication interactions, even for uncatalogued compounds. 

Beyond standard clinical lookup tools, the platform renders pharmacological interactions as **interactive graph networks** and **3D molecular structures** — arming clinical researchers and informaticians with real-time, actionable risk data.

---

## Features

- **Potency AI Lab (pIC50):** Real-time binding affinity prediction for uncatalogued chemicals. (RandomForest + RDKit)
- **Multi-organ Toxicity Engine:** SMARTS-based toxicity screening (hepato-, cardio-, nephro-, endocrine).
- **Adverse Event Predictor:** ML models forecast side-effect risk with confidence scores.
- **Pharmacogenomics Risk Layer:** Patient-specific allele simulation for metabolic risk visibility.

**Visualizations:**
- 3D molecular viewer ([RDKit.AllChem](https://www.rdkit.org/), [3Dmol.js](https://3dmol.csb.pitt.edu/))
- Dosing timeline for interaction mitigation
- Interactive polypharmacy graph (Cytoscape.js)
- Medical AI chatbot for mechanisms, substitutions, and Q&A

---

## Quick Start

> A virtual environment is **strongly recommended** due to RDKit/LightGBM requirements.

```
git clone https://github.com/pandashreyan/DDI.git && cd DDI
python -m venv .venv && source .venv/bin/activate
pip install -r backend/requirements.txt
cd backend && python app.py
```

Server runs at: [http://localhost:5005](http://localhost:5005)

**Docker:**  
```
docker build -t ddi-predict . && docker run -p 10000:10000 ddi-predict
```

---

## Architecture

- **Backend:** Python 3.11, Flask, Waitress, scikit-learn, LightGBM, RDKit, pandas, numpy, PyTDC
- **Frontend:** Vanilla JS, HTML5, Chart.js, Cytoscape.js, 3Dmol.js

---

## Datasets Included

| File                     | Description                        |
|--------------------------|------------------------------------|
| `db_drug_interactions.csv` | Core clinical interaction rules    |
| `SMILES_Big_Data_Set.csv` | Fingerprint mapping dataset        |
| `drug_metadata.json`       | Drug properties + deep-links      |
| `expert_interactions.json` | Curated mechanistic interaction data |

---

## License

MIT.  
See [LICENSE](LICENSE).

---

## Disclaimer

> **DDI Predict is an analytical prediction platform intended for research and educational purposes only. It does not replace certified professional medical advice. Always consult a healthcare provider before making clinical decisions.**

---

## Contributing

Pull requests and issues welcome!  
File issues or ideas [here](https://github.com/pandashreyan/DDI/issues).

---

_Created by Shreyan Panda_