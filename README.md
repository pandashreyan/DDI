<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DDI Predict — README</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,600;1,9..40,300&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #07090f;
    --bg2: #0d1117;
    --bg3: #111620;
    --card: #131926;
    --border: rgba(255,255,255,0.07);
    --border-glow: rgba(64,196,148,0.25);
    --text: #e8edf5;
    --muted: #6b7a94;
    --accent: #40c494;
    --accent2: #4fa8e0;
    --accent3: #c97ef7;
    --warn: #f5a623;
    --red: #f0606a;
    --mono: 'Space Mono', monospace;
    --sans: 'DM Sans', sans-serif;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    font-family: var(--sans);
    background: var(--bg);
    color: var(--text);
    line-height: 1.7;
    font-size: 15px;
  }

  /* ─── HERO ─── */
  .hero {
    position: relative;
    overflow: hidden;
    padding: 80px 40px 64px;
    text-align: center;
    border-bottom: 1px solid var(--border);
  }

  .hero::before {
    content: '';
    position: absolute;
    top: -120px; left: 50%;
    transform: translateX(-50%);
    width: 700px; height: 420px;
    background: radial-gradient(ellipse at center, rgba(64,196,148,0.12) 0%, rgba(79,168,224,0.06) 45%, transparent 75%);
    pointer-events: none;
  }

  .hero-badge {
    display: inline-block;
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--accent);
    border: 1px solid rgba(64,196,148,0.35);
    padding: 5px 14px;
    border-radius: 100px;
    margin-bottom: 28px;
    background: rgba(64,196,148,0.06);
  }

  .hero h1 {
    font-family: var(--mono);
    font-size: clamp(28px, 5vw, 48px);
    font-weight: 700;
    letter-spacing: -0.02em;
    line-height: 1.15;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #e8edf5 0%, #40c494 50%, #4fa8e0 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }

  .hero p {
    max-width: 600px;
    margin: 0 auto 36px;
    color: var(--muted);
    font-size: 16px;
    font-weight: 300;
    line-height: 1.8;
  }

  .hero-links {
    display: flex;
    gap: 12px;
    justify-content: center;
    flex-wrap: wrap;
  }

  .btn {
    font-family: var(--mono);
    font-size: 12px;
    letter-spacing: 0.06em;
    padding: 10px 22px;
    border-radius: 6px;
    text-decoration: none;
    transition: all 0.18s ease;
    cursor: pointer;
    border: none;
  }

  .btn-primary {
    background: var(--accent);
    color: #07090f;
    font-weight: 700;
  }
  .btn-primary:hover { background: #56d9ac; transform: translateY(-1px); }

  .btn-outline {
    background: transparent;
    color: var(--text);
    border: 1px solid var(--border);
  }
  .btn-outline:hover { border-color: rgba(255,255,255,0.2); background: rgba(255,255,255,0.04); }

  /* ─── BADGES ─── */
  .badges {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    justify-content: center;
    padding: 24px 40px;
    border-bottom: 1px solid var(--border);
  }

  .badge {
    font-family: var(--mono);
    font-size: 11px;
    padding: 4px 12px;
    border-radius: 4px;
    letter-spacing: 0.04em;
  }
  .badge-green { background: rgba(64,196,148,0.12); color: var(--accent); border: 1px solid rgba(64,196,148,0.2); }
  .badge-blue { background: rgba(79,168,224,0.12); color: var(--accent2); border: 1px solid rgba(79,168,224,0.2); }
  .badge-purple { background: rgba(201,126,247,0.12); color: var(--accent3); border: 1px solid rgba(201,126,247,0.2); }
  .badge-warn { background: rgba(245,166,35,0.12); color: var(--warn); border: 1px solid rgba(245,166,35,0.2); }

  /* ─── LAYOUT ─── */
  .content {
    max-width: 900px;
    margin: 0 auto;
    padding: 60px 40px;
  }

  /* ─── SECTION HEADER ─── */
  .section-label {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
  }

  h2 {
    font-family: var(--mono);
    font-size: 22px;
    font-weight: 700;
    color: var(--text);
    margin-bottom: 24px;
    letter-spacing: -0.01em;
  }

  h3 {
    font-family: var(--sans);
    font-size: 14px;
    font-weight: 600;
    color: var(--text);
    margin-bottom: 8px;
    letter-spacing: 0.01em;
  }

  p { color: var(--muted); margin-bottom: 16px; line-height: 1.8; }

  section { margin-bottom: 60px; }

  /* ─── FEATURE GRID ─── */
  .feature-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
    gap: 1px;
    background: var(--border);
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
  }

  .feature-card {
    background: var(--card);
    padding: 24px;
    transition: background 0.15s;
  }
  .feature-card:hover { background: #161d2e; }

  .feature-icon {
    font-size: 18px;
    margin-bottom: 12px;
    display: block;
    width: 36px; height: 36px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 8px;
    margin-bottom: 14px;
  }

  .icon-green { background: rgba(64,196,148,0.12); }
  .icon-blue { background: rgba(79,168,224,0.12); }
  .icon-purple { background: rgba(201,126,247,0.12); }
  .icon-warn { background: rgba(245,166,35,0.12); }

  .feature-card h3 { font-size: 13px; margin-bottom: 6px; }
  .feature-card p { font-size: 13px; margin-bottom: 0; color: #5a6880; line-height: 1.65; }

  /* ─── TECH STACK ─── */
  .stack-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 16px;
  }

  @media (max-width: 600px) {
    .stack-grid { grid-template-columns: 1fr; }
  }

  .stack-card {
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 22px;
    background: var(--card);
  }

  .stack-card-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 16px;
    padding-bottom: 14px;
    border-bottom: 1px solid var(--border);
  }

  .stack-dot {
    width: 8px; height: 8px;
    border-radius: 50%;
  }

  .stack-dot-green { background: var(--accent); box-shadow: 0 0 8px var(--accent); }
  .stack-dot-blue { background: var(--accent2); box-shadow: 0 0 8px var(--accent2); }

  .stack-card-header span {
    font-family: var(--mono);
    font-size: 11px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--muted);
  }

  .chip-list { display: flex; flex-wrap: wrap; gap: 7px; }

  .chip {
    font-family: var(--mono);
    font-size: 11px;
    padding: 4px 10px;
    border-radius: 4px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    color: var(--muted);
    letter-spacing: 0.03em;
  }

  /* ─── CODE BLOCK ─── */
  .code-block {
    background: #06080d;
    border: 1px solid var(--border);
    border-radius: 10px;
    overflow: hidden;
    margin: 20px 0;
  }

  .code-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 16px;
    background: rgba(255,255,255,0.025);
    border-bottom: 1px solid var(--border);
  }

  .code-dots { display: flex; gap: 6px; }
  .code-dot { width: 10px; height: 10px; border-radius: 50%; }
  .cd-r { background: #f0606a; } .cd-y { background: #f5a623; } .cd-g { background: #40c494; }

  .code-title {
    font-family: var(--mono);
    font-size: 11px;
    color: var(--muted);
    letter-spacing: 0.06em;
  }

  pre {
    padding: 20px 18px;
    overflow-x: auto;
    font-family: var(--mono);
    font-size: 12.5px;
    line-height: 1.8;
    color: #afc0d5;
  }

  .c-comment { color: #3d5070; }
  .c-green { color: var(--accent); }
  .c-blue { color: var(--accent2); }
  .c-purple { color: var(--accent3); }
  .c-warn { color: var(--warn); }
  .c-muted { color: #5a6880; }

  /* ─── QUICKSTART STEPS ─── */
  .steps { counter-reset: step; display: flex; flex-direction: column; gap: 0; }

  .step {
    display: flex;
    gap: 20px;
    padding: 0 0 32px 0;
    position: relative;
  }

  .step::before {
    content: '';
    position: absolute;
    left: 18px;
    top: 38px;
    bottom: 0;
    width: 1px;
    background: var(--border);
  }

  .step:last-child::before { display: none; }

  .step-num {
    width: 38px; height: 38px;
    border-radius: 50%;
    border: 1px solid var(--border-glow);
    background: rgba(64,196,148,0.08);
    display: flex; align-items: center; justify-content: center;
    font-family: var(--mono);
    font-size: 13px;
    color: var(--accent);
    flex-shrink: 0;
  }

  .step-body { padding-top: 6px; flex: 1; }
  .step-body h3 { font-size: 15px; margin-bottom: 6px; color: var(--text); }
  .step-body p { font-size: 13.5px; margin-bottom: 10px; }

  /* ─── DATA TABLE ─── */
  .data-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 13px;
  }

  .data-table th {
    font-family: var(--mono);
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    text-align: left;
    padding: 10px 14px;
    border-bottom: 1px solid var(--border);
  }

  .data-table td {
    padding: 12px 14px;
    border-bottom: 1px solid rgba(255,255,255,0.03);
    color: var(--muted);
    vertical-align: top;
  }

  .data-table td:first-child {
    font-family: var(--mono);
    color: var(--accent2);
    font-size: 12px;
    white-space: nowrap;
  }

  .data-table tr:last-child td { border-bottom: none; }

  /* ─── CALLOUT ─── */
  .callout {
    padding: 16px 20px;
    border-radius: 8px;
    border-left: 3px solid;
    margin: 20px 0;
    font-size: 13.5px;
  }

  .callout-warn {
    background: rgba(245,166,35,0.06);
    border-color: var(--warn);
    color: #a57c40;
  }

  .callout-info {
    background: rgba(79,168,224,0.06);
    border-color: var(--accent2);
    color: #5a7ea0;
  }

  .callout strong { color: var(--warn); }
  .callout-info strong { color: var(--accent2); }

  /* ─── DISCLAIMER ─── */
  .disclaimer {
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 24px;
    background: var(--card);
    margin-top: 40px;
    font-size: 12.5px;
    color: #404c62;
    line-height: 1.75;
  }

  .disclaimer strong { color: var(--muted); }

  /* ─── FOOTER ─── */
  footer {
    text-align: center;
    padding: 32px 40px;
    border-top: 1px solid var(--border);
    font-family: var(--mono);
    font-size: 11px;
    color: #2e3a4d;
    letter-spacing: 0.06em;
  }

  footer span { color: var(--accent); }

  /* ─── INLINE CODE ─── */
  code {
    font-family: var(--mono);
    font-size: 12px;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    padding: 1px 6px;
    border-radius: 4px;
    color: var(--accent2);
  }

  a { color: var(--accent); text-decoration: none; }
  a:hover { text-decoration: underline; }

  @media (max-width: 640px) {
    .hero { padding: 60px 24px 48px; }
    .content { padding: 48px 24px; }
    .badges { padding: 16px 24px; }
  }
</style>
</head>
<body>

<!-- ══════════════════════════════════════════
     HERO
══════════════════════════════════════════ -->
<header class="hero">
  <div class="hero-badge">⬡ Pharmaceutical Intelligence Platform</div>
  <h1>DDI Predict<br>Analytics Suite</h1>
  <p>A production-grade AI/Clinical platform for predicting, visualizing, and mitigating complex polypharmacy risks — powered by hybrid ML intelligence and FDA-grade evidence databases.</p>
  <div class="hero-links">
    <a href="#quickstart" class="btn btn-primary">Quick Start →</a>
    <a href="#features" class="btn btn-outline">View Features</a>
    <a href="#architecture" class="btn btn-outline">Architecture</a>
  </div>
</header>

<!-- ══════════════════════════════════════════
     BADGES
══════════════════════════════════════════ -->
<div class="badges">
  <span class="badge badge-green">Python 3.11</span>
  <span class="badge badge-blue">Flask + Waitress</span>
  <span class="badge badge-purple">scikit-learn · LightGBM</span>
  <span class="badge badge-green">RDKit</span>
  <span class="badge badge-blue">Cytoscape.js</span>
  <span class="badge badge-purple">3Dmol.js</span>
  <span class="badge badge-warn">MIT License</span>
  <span class="badge badge-blue">Docker Ready</span>
</div>

<!-- ══════════════════════════════════════════
     CONTENT
══════════════════════════════════════════ -->
<main class="content">

  <!-- OVERVIEW -->
  <section>
    <div class="section-label">Overview</div>
    <h2>Beyond clinical lookup.</h2>
    <p>
      DDI Predict goes far beyond traditional drug interaction checkers. It operates on a <strong style="color: var(--text); font-weight: 600;">hybrid intelligence model</strong> — combining deterministic FDA evidence databases with scalable predictive machine learning algorithms to surface risks that static tables simply cannot see.
    </p>
    <p>
      The platform renders the underlying pharmacology natively: spinnable 3D molecular structures, interactive polypharmacy graph networks, and a real-time chronopharmacological dosing timeline that actively stagger administrations to bypass simultaneous metabolic collisions.
    </p>

    <div class="callout callout-info">
      <strong>Research Platform</strong> — DDI Predict is an analytical prediction tool intended for research and clinical education. It does not replace certified medical advice or FDA/EMA safety standards.
    </div>
  </section>

  <!-- FEATURES -->
  <section id="features">
    <div class="section-label">Core Modules</div>
    <h2>Intelligence, rendered.</h2>

    <div class="feature-grid">
      <div class="feature-card">
        <div class="feature-icon icon-green">🧪</div>
        <h3>Potency AI Lab — pIC50 Engine</h3>
        <p>Real-time binding affinity calculation for unknown or uncatalogued chemical structures using a RandomForestRegressor trained on RDKit Morgan Fingerprints.</p>
      </div>

      <div class="feature-card">
        <div class="feature-icon icon-blue">🫀</div>
        <h3>Multi-Organ Toxicity Engine</h3>
        <p>RDKit SMARTS structural scanning detects molecular toxicophores associated with Hepatotoxicity, Cardiotoxicity (hERG), Nephrotoxicity, and Endocrine disruption.</p>
      </div>

      <div class="feature-card">
        <div class="feature-icon icon-purple">📊</div>
        <h3>Adverse Event Predictor</h3>
        <p>ML likelihood modelling forecasting secondary physiological side-effects natively, surfaced with risk-ranked confidence scores per drug combination.</p>
      </div>

      <div class="feature-card">
        <div class="feature-icon icon-warn">🧬</div>
        <h3>Pharmacogenomics Risk Layer</h3>
        <p>Precision-medicine tracking simulating patient-specific CYP450/SLCO allele vulnerabilities mapped against drug metabolic clearance routes.</p>
      </div>

      <div class="feature-card">
        <div class="feature-icon icon-blue">🔬</div>
        <h3>3D Molecular Viewer</h3>
        <p>Spinnable 3D ball-and-stick rendering driven locally using RDKit.AllChem for coordinate embedding and 3Dmol.js for GPU-accelerated display.</p>
      </div>

      <div class="feature-card">
        <div class="feature-icon icon-green">⏱</div>
        <h3>Chronopharmacological Timeline</h3>
        <p>Live engine logic staggering individual drug administrations across a 24-hour window to entirely bypass simultaneous serum metabolic collisions.</p>
      </div>

      <div class="feature-card">
        <div class="feature-icon icon-purple">🕸</div>
        <h3>Polypharmacy Graph Network</h3>
        <p>Cytoscape.js neural webbing visualising complex multi-drug combinations (>2 drugs), dynamically identifying worst-offender interaction nodes.</p>
      </div>

      <div class="feature-card">
        <div class="feature-icon icon-warn">🤖</div>
        <h3>Medical AI Chatbot</h3>
        <p>Context-aware clinical assistant generating deterministic structural mechanics breakdowns and bioisostere substitution recommendations on demand.</p>
      </div>
    </div>
  </section>

  <!-- ARCHITECTURE -->
  <section id="architecture">
    <div class="section-label">Architecture</div>
    <h2>Tech stack.</h2>

    <div class="stack-grid">
      <div class="stack-card">
        <div class="stack-card-header">
          <div class="stack-dot stack-dot-green"></div>
          <span>Backend Engine</span>
        </div>
        <div class="chip-list">
          <span class="chip">Python 3.11</span>
          <span class="chip">Flask</span>
          <span class="chip">Waitress WSGI</span>
          <span class="chip">scikit-learn</span>
          <span class="chip">LightGBM</span>
          <span class="chip">RDKit</span>
          <span class="chip">pandas</span>
          <span class="chip">numpy</span>
        </div>
      </div>

      <div class="stack-card">
        <div class="stack-card-header">
          <div class="stack-dot stack-dot-blue"></div>
          <span>Frontend Interface</span>
        </div>
        <div class="chip-list">
          <span class="chip">Vanilla JS/CSS</span>
          <span class="chip">Chart.js</span>
          <span class="chip">Cytoscape.js</span>
          <span class="chip">3Dmol.js</span>
        </div>
      </div>
    </div>
  </section>

  <!-- QUICK START -->
  <section id="quickstart">
    <div class="section-label">Quick Start</div>
    <h2>Up in minutes.</h2>

    <div class="steps">
      <div class="step">
        <div class="step-num">1</div>
        <div class="step-body">
          <h3>Clone the repository</h3>
          <p>Pull the project and navigate into the directory.</p>
          <div class="code-block">
            <div class="code-header">
              <div class="code-dots"><div class="code-dot cd-r"></div><div class="code-dot cd-y"></div><div class="code-dot cd-g"></div></div>
              <div class="code-title">terminal</div>
            </div>
            <pre><span class="c-comment"># Clone and enter the project</span>
git clone https://github.com/your-username/DDI-Predict.git
cd DDI-Predict</pre>
          </div>
        </div>
      </div>

      <div class="step">
        <div class="step-num">2</div>
        <div class="step-body">
          <h3>Create a virtual environment</h3>
          <p>Strongly recommended — RDKit and LightGBM carry heavy C++ binding requirements that can conflict with system packages.</p>
          <div class="code-block">
            <div class="code-header">
              <div class="code-dots"><div class="code-dot cd-r"></div><div class="code-dot cd-y"></div><div class="code-dot cd-g"></div></div>
              <div class="code-title">terminal</div>
            </div>
            <pre>python -m venv .venv
<span class="c-comment"># Unix / macOS</span>
source .venv/bin/activate
<span class="c-comment"># Windows</span>
.venv\Scripts\activate</pre>
          </div>
        </div>
      </div>

      <div class="step">
        <div class="step-num">3</div>
        <div class="step-body">
          <h3>Install dependencies</h3>
          <div class="code-block">
            <div class="code-header">
              <div class="code-dots"><div class="code-dot cd-r"></div><div class="code-dot cd-y"></div><div class="code-dot cd-g"></div></div>
              <div class="code-title">terminal</div>
            </div>
            <pre>pip install -r backend/requirements.txt</pre>
          </div>
        </div>
      </div>

      <div class="step">
        <div class="step-num">4</div>
        <div class="step-body">
          <h3>Launch the application</h3>
          <p>The service spins up the web UI on port 5005.</p>
          <div class="code-block">
            <div class="code-header">
              <div class="code-dots"><div class="code-dot cd-r"></div><div class="code-dot cd-y"></div><div class="code-dot cd-g"></div></div>
              <div class="code-title">terminal</div>
            </div>
            <pre>cd backend
python app.py
<span class="c-comment"># → http://localhost:5005</span></pre>
          </div>
        </div>
      </div>
    </div>

    <div class="section-label" style="margin-top: 12px;">Docker</div>
    <p>Includes native system dependencies like <code>libxrender1</code>. Recommended for all production deployments.</p>
    <div class="code-block">
      <div class="code-header">
        <div class="code-dots"><div class="code-dot cd-r"></div><div class="code-dot cd-y"></div><div class="code-dot cd-g"></div></div>
        <div class="code-title">dockerfile</div>
      </div>
      <pre>docker build -t ddi-predict .
docker run -p 5005:5005 ddi-predict</pre>
    </div>
  </section>

  <!-- DATA STRUCTURE -->
  <section>
    <div class="section-label">Data Requirements</div>
    <h2>Required datasets.</h2>
    <p>Three critical files are required before running mapping and inference at scale. These are not bundled in the repository.</p>

    <div class="code-block" style="margin-bottom: 0;">
      <div class="code-header">
        <div class="code-dots"><div class="code-dot cd-r"></div><div class="code-dot cd-y"></div><div class="code-dot cd-g"></div></div>
        <div class="code-title">required files</div>
      </div>
      <table class="data-table">
        <thead>
          <tr>
            <th>File</th>
            <th>Purpose</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>db_drug_interactions.csv</td>
            <td>Sourced core clinical interaction rules</td>
          </tr>
          <tr>
            <td>SMILES_Big_Data_Set.csv</td>
            <td>Fingerprint dataset mapping for pIC50 and toxicity engines</td>
          </tr>
          <tr>
            <td>ddi_model.pkl</td>
            <td>Compiled DDI classification model</td>
          </tr>
          <tr>
            <td>pic50_model.pkl</td>
            <td>Compiled binding affinity regression model</td>
          </tr>
          <tr>
            <td>toxicity_model.pkl</td>
            <td>Compiled multi-organ toxicity prediction model</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div class="callout callout-warn" style="margin-top: 20px;">
      <strong>Serverless hosts:</strong> Lambda function size limits (~250MB) on platforms like Vercel will be exceeded by the ML model artifacts. Use containerised hosts — Render, Railway, or Heroku are well-suited. See <code>Dockerfile</code> for the recommended production configuration.
    </div>
  </section>

  <!-- DISCLAIMER + LICENSE -->
  <section>
    <div class="section-label">License</div>
    <h2>Open source.</h2>
    <p>Distributed under the <strong style="color: var(--text);">MIT License</strong>. See <code>LICENSE</code> for full terms.</p>

    <div class="disclaimer">
      <strong>Research Disclaimer —</strong> DDI Predict is an analytical prediction platform built for research and academic presentation. All predictions are probabilistic and should be interpreted accordingly. This tool does not constitute certified professional medical advice and must not be used as a substitute for validated FDA/EMA clinical safety evaluation processes.
    </div>
  </section>

</main>

<footer>
  DDI Predict Analytics Suite &nbsp;·&nbsp; MIT License &nbsp;·&nbsp; Built with <span>♥</span> for the clinical research community
</footer>

</body>
</html>
