<div align="center">

# 🧬 DDI Predict Analytics Suite

**A venture-ready Pharmaceutical Intelligence Platform for predicting and visualizing Drug-Drug Interactions (DDIs) using Machine Learning and Clinical Heuristics.**

[![Live Demo](https://img.shields.io/badge/Demo-Live_on_Render-00B289?style=for-the-badge&logo=render)](https://ddi-lcyj.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)]()
[![Flask](https://img.shields.io/badge/Flask-Waitress-000000?style=for-the-badge&logo=flask&logoColor=white)]()
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge&logo=docker&logoColor=white)]()
[![License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)]()

[View Live Platform](https://ddi-lcyj.onrender.com) · [Report Bug](https://github.com/pandashreyan/DDI/issues) · [Request Feature](https://github.com/pandashreyan/DDI/issues)

</div>

---

## 🎯 Overview

**Polypharmacy is dangerous.** DDI Predict is an advanced AI and clinical tool built to identify, analyze, and mitigate complex medication risks before they hit the patient. 

Built on a hybrid intelligence model, DDI Predict seamlessly combines deterministic FDA evidence databases with highly-scalable predictive Machine Learning algorithms. The software goes far beyond traditional clinical lookup tools by rendering the actual pharmacological interactions natively (via interactive graph networks and 3D molecular structures) and actively generating safe chronopharmacological dosing regimens.

---

## ✨ Key Platform Features

### 🧠 Core Intelligence Modules
* **Potency AI Lab (pIC50 Engine)**: Real-time calculation of drug binding affinities (pIC50) for uncatalogued chemical structures using a `RandomForestRegressor` and RDKit Morgan Fingerprints.
* **Multi-Organ Toxicity Engine**: RDKit structural scanning (SMARTS) detecting molecular toxicophores associated with Hepatotoxicity, Cardiotoxicity (hERG), Nephrotoxicity, and Endocrine disruption.
* **Adverse Event Predictor**: Machine learning likelihood modeling forecasting secondary physiological side-effects natively.
* **Pharmacogenomics (PGx) Risk Layer**: Integrated precision-medicine tracking simulating patient-specific CYP450/SLCO allele vulnerabilities against drug metabolic clearance routes.

### 🧬 Clinical Visualizations & UI
* **3D Interactive Molecular Viewer**: Spinnable 3D ball-and-stick rendering driven locally using `RDKit.AllChem` and `3Dmol.js`.
* **Chronopharmacological Dosing Timeline**: Live engine logic staggering individual pill administration across 24 hours to entirely bypass simultaneous serum metabolic collisions.
* **Interactive Polypharmacy Graph Network**: `Cytoscape.js` neural webbing showing complex >2 multidrug combinations, identifying the "worst-offenders" dynamically.
* **Medical AI Chatbot Simulation**: Context-aware clinical assistant interface generating deterministic structural mechanics breakdowns and bioisostere substitution recommendations.

---

## 🏗️ Architecture & Tech Stack

### Backend Engine
- **Framework**: Python 3.11 with `Flask` and `Waitress` WSGI server (Production-grade).
- **Machine Learning**: `scikit-learn` (Random Forest Classifiers), `LightGBM`.
- **Chemoinformatics**: `RDKit` (for SMILES deserialization, descriptor calculations, and 3D coordinate embeddings).
- **Data Parsing & Modeling**: `pandas`, `numpy`, `PyTDC`.

### Frontend Interface
- **Framework**: High-performance Vanilla JS/HTML5 implementation (Zero framework bloat).
- **Visuals**: `Chart.js` (Radar/Bar/Heatmaps), `Cytoscape.js` (Network Maps), `3Dmol.js` (Spatial rendering).

---

## 🚀 Quick Start (Local Development)

We highly recommend running in a contained virtual environment due to the heavy C++ binding requirements of RDKit and LightGBM.

```bash
# 1. Clone the repository
git clone https://github.com/pandashreyan/DDI.git
cd DDI

# 2. Setup your virtual environment
python -m venv .venv

# Activate the virtual environment:
# On Unix/macOS:
source .venv/bin/activate 
# On Windows:
.venv\Scripts\activate 

# 3. Install core dependencies
pip install -r backend/requirements.txt

# 4. Start the Application
cd backend
python app.py
```
*The service will launch the web UI directly on http://localhost:5005.*

---

## 🐋 Production Deployment (Docker / Render.com)

DDI Predict is fully containerized and currently deployed on **Render.com**. 
To deploy your own instance using Docker:

```bash
# 1. Build the Docker image
docker build -t ddi-predict .

# 2. Run the container
docker run -p 10000:10000 ddi-predict
```
*The `render.yaml` file is included in the root directory for instantaneous CI/CD deployments directly from GitHub to Render's infrastructure.*

---

## 📂 System Data & Models

This repository requires critical datasets to run mapping and inference at scale. 
> **Note**: Large `.pkl` models and `.npy` arrays are excluded via `.gitignore` to maintain a lightweight repository. The system is engineered to degrade gracefully and will train missing models (like the pIC50 engine) at startup or rely on the deterministic clinical rules engine.

Data files included:
- `db_drug_interactions.csv`: Sourced core clinical rules.
- `SMILES_Big_Data_Set.csv`: Fingerprint dataset mapping.
- `drug_metadata.json` / `expert_interactions.json`: Deep linking for mechanisms and drug properties.

---

## 🛡️ License & Disclaimer

Distributed under the MIT License. See `LICENSE` for more information.

> **Disclaimer**: This tool is an analytical prediction platform intended for research, presentation, and educational purposes. **It should not replace certified professional medical advice or FDA/EMA clinical safety standards.**
