<div align="center">
  <img src="./frontend/favicon.ico" alt="Logo" width="80" height="80">
  <h1 align="center">DDI Predict Analytics Suite</h1>

  <p align="center">
    A comprehensive, venture-backed-level Pharmaceutical Intelligence Platform for predicting and visualizing Drug-Drug Interactions using Machine Learning and Clinical Heuristics.
    <br />
    <br />
    <a href="#-key-features">View Features</a>
    ·
    <a href="#%EF%B8%8F-architecture--tech-stack">Architecture</a>
    ·
    <a href="#-quick-start">Quick Start</a>
  </p>
</div>

---

## 🎯 Overview
**DDI Predict** is an advanced AI/Clinical tool designed to identify, analyze, and mitigate complex polypharmacy risks. Built on a hybrid intelligence model combining deterministic FDA evidence databases with highly-scalable predictive Machine Learning algorithms. 

The software goes beyond traditional clinical lookup tools by rendering the actual pharmacological interactions natively (via interactive graph networks and 3D molecular structures) and actively generating safe chronopharmacological dosing regimens.

## ✨ Key Features

### 🧠 Core Intelligence Modules
* **Potency AI Lab (pIC50 Engine)**: Real-time calculation of drug binding affinities (pIC50) for completely unknown or uncatalogued chemical structures using a `RandomForestRegressor` and RDKit Morgan Fingerprints.
* **Multi-Organ Toxicity Engine**: RDKit structural scanning (SMARTS) detecting molecular toxicophores associated with Hepatotoxicity, Cardiotoxicity (hERG), Nephrotoxicity, and Endocrine disruption.
* **Adverse Event Predictor**: Machine learning likelihood modeling forecasting secondary physiological side-effects natively.
* **Pharmacogenomics (PGx) Risk Layer**: Integrated precision-medicine tracking simulating patient-specific CYP450/SLCO allele vulnerabilities against drug metabolic clearance routes.

### 🧬 Clinical Visualizations & UI
* **3D Interactive Molecular Viewer**: Spinnable 3D ball-and-stick rendering driven locally using `RDKit.AllChem` and `3Dmol.js`.
* **Chronopharmacological Dosing Timeline**: Live engine logic staggering individual pill administration across 24 hours to entirely bypass simultaneous serum metabolic collisions.
* **Interactive Polypharmacy Graph Network**: `Cytoscape.js` neural webbing showing complex >2 multidrug combinations, identifying the "worst-offenders" dynamically.
* **Medical AI Chatbot Simulation**: Context-aware clinical assistant interface generating deterministic structural mechanics breakdowns and bioisostere substitution recommendations.

---

## 🛠️ Architecture & Tech Stack

### Backend Engine
- **Framework**: Python 3.11 with `Flask` and `Waitress` WSGI server.
- **Machine Learning**: `scikit-learn` (RandomForest classifers), `LightGBM`.
- **Chemoinformatics**: `RDKit` (for SMILES deserialization, descriptor calculations, and 3D coordinate embeddings).
- **Data Parsing**: `pandas` and `numpy`.

### Frontend Interface
- **Framework**: Vanilla JS/CSS implementation avoiding massive framework bloat.
- **Visuals**: `Chart.js` (Radar/Bar/Heatmaps), `Cytoscape.js` (Network Maps), `3Dmol.js` (Spatial rendering).

---

## 🚀 Quick Start

### 1. Local Development deployment
We highly recommend running in a contained virtual environment due to the heavy C++ binding requirements of RDKit and LightGBM.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/DDI-Predict.git
cd DDI-Predict

# 2. Setup your virtual environment
python -m venv .venv
source .venv/bin/activate # (Unix) or .venv\Scripts\activate (Windows)

# 3. Install core dependencies
pip install -r backend/requirements.txt

# 4. Start the Application
cd backend
python app.py
```
*The service will launch the web UI directly on http://localhost:5005.*

### 2. Production Docker Deployment (Recommended)
This build natively incorporates heavy system dependencies (like `libxrender1`). Make sure Docker is running:

```bash
docker build -t ddi-predict .
docker run -p 5005:5005 ddi-predict
```

---

## 🏗️ Data Structure Notice

This repository requires three critical datasets to run mapping and inference at an industrial scale:
1. `db_drug_interactions.csv`: Sourced core clinical rules.
2. `SMILES_Big_Data_Set.csv`: Fingerprint dataset mapping.
3. `ddi_model.pkl` / `pic50_model.pkl` / `toxicity_model.pkl`: Recompiled ML models.
*(Note: Be cautious when deploying statically to Serverless hosts (e.g. Vercel) as Lambda limits sit around 250MB. See `Dockerfile` structure for robust hosting on Render, Railway, or Heroku).*

## 🛡️ License
Distributed under the MIT License. See `LICENSE` for more information.

> **Disclaimer**: This tool is an analytical prediction platform intended for research and presentation purposes. It should not replace certified professional medical advice or FDA/EMA clinical safety standards.
