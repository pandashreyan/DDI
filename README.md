<div align="center">

# 🧬 DDI Predict Analytics Suite

**A venture-ready pharmaceutical intelligence platform for predicting and visualizing drug–drug interactions (DDIs) using machine learning and clinical heuristics.**

[![Live Demo](https://img.shields.io/badge/Demo-Live_on_Render-00B289?style=for-the-badge&logo=render)](https://ddi-lcyj.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Flask](https://img.shields.io/badge/Flask-Waitress-000000?style=for-the-badge&logo=flask&logoColor=white)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)]()

[View Live Platform](https://ddi-lcyj.onrender.com) · [Report Bug](https://github.com/pandashreyan/DDI/issues) · [Request Feature](https://github.com/pandashreyan/DDI/issues)

</div>

---

## Overview

**Polypharmacy is dangerous.** DDI Predict combines deterministic FDA evidence databases with predictive ML algorithms to identify, analyze, and mitigate complex medication risks before they reach the patient.

Beyond standard clinical lookup tools, the platform renders pharmacological interactions as interactive graph networks and 3D molecular structures — and automatically generates safe, chronopharmacological dosing regimens for polypharmacy patients.

---

## Core Intelligence Modules

### 🔬 Potency AI Lab (pIC50 Engine)
Real-time binding affinity calculation for uncatalogued chemical structures using a `RandomForestRegressor` trained on RDKit Morgan fingerprints. Supports SMILES input for any novel compound.

### ☣️ Multi-Organ Toxicity Engine
RDKit SMARTS-based structural scanning that detects molecular toxicophores associated with hepatotoxicity, hERG cardiotoxicity, nephrotoxicity, and endocrine disruption — all from a single molecular structure.

### 📈 Adverse Event Predictor
ML likelihood modeling that forecasts secondary physiological side-effects with probabilistic confidence scoring, enabling proactive clinical risk management.

### 🧬 Pharmacogenomics (PGx) Risk Layer
Precision-medicine tracking that simulates patient-specific CYP450/SLCO allele vulnerabilities against drug metabolic clearance routes — surfacing personalized interaction risks invisible to population-level lookups.

---

## Clinical Visualizations

| Feature | Description | Powered by |
|---|---|---|
| **3D molecular viewer** | Spinnable ball-and-stick rendering for any compound | `RDKit.AllChem` + `3Dmol.js` |
| **Dosing timeline** | 24-hour staggered scheduling to prevent serum metabolic collisions | Custom chronopharmacology engine |
| **Polypharmacy graph** | Interactive network map for >2-drug combinations, flagging worst-offender pairs | `Cytoscape.js` |
| **Medical AI chatbot** | Context-aware assistant for mechanism breakdowns and bioisostere substitution advice | Deterministic rules engine |

---

## Architecture & Tech Stack

### Backend
- **Framework**: Python 3.11 · Flask · Waitress WSGI (production-grade)
- **Machine learning**: `scikit-learn` (Random Forest) · `LightGBM`
- **Chemoinformatics**: `RDKit` — SMILES parsing, descriptor calculation, 3D coordinate embedding
- **Data**: `pandas` · `numpy` · `PyTDC`

### Frontend
- **Core**: Vanilla JS / HTML5 — no framework overhead
- **Visualizations**: `Chart.js` (radar, bar, heatmaps) · `Cytoscape.js` (network graphs) · `3Dmol.js` (3D rendering)

---

## Quick Start (Local)

> **Note**: A virtual environment is strongly recommended due to RDKit and LightGBM's C++ binding requirements.

```bash
# 1. Clone the repository
git clone https://github.com/pandashreyan/DDI.git
cd DDI

# 2. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# .venv\Scripts\activate        # Windows

# 3. Install dependencies
pip install -r backend/requirements.txt

# 4. Start the server
cd backend
python app.py
```

The app will be available at **http://localhost:5005**.

---

## Production Deployment (Docker / Render)

DDI Predict is fully containerized and deployed on [Render.com](https://render.com). A `render.yaml` is included for instant CI/CD from GitHub.

```bash
# Build the image
docker build -t ddi-predict .

# Run the container
docker run -p 10000:10000 ddi-predict
```

---

## Data & Models

Large `.pkl` model files and `.npy` arrays are excluded from the repository via `.gitignore`. The system degrades gracefully — missing models (e.g. the pIC50 engine) are retrained at startup, and the deterministic clinical rules engine remains fully operational regardless.

**Included data files:**

| File | Description |
|---|---|
| `db_drug_interactions.csv` | Core clinical interaction rules |
| `SMILES_Big_Data_Set.csv` | Fingerprint mapping dataset |
| `drug_metadata.json` | Drug properties and deep-link references |
| `expert_interactions.json` | Curated mechanistic interaction data |

---

## License & Disclaimer

Distributed under the **MIT License**. See [`LICENSE`](LICENSE) for details.

> ⚠️ **Disclaimer**: DDI Predict is an analytical prediction platform intended for research and educational purposes only. It does not replace certified professional medical advice or FDA/EMA clinical safety standards.
