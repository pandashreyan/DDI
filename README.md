<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DDI Predict — README</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0;}
:root{--bg:#07090f;--bg2:#0d1117;--card:#131926;--bdr:rgba(255,255,255,0.07);--glow:rgba(64,196,148,0.25);--tx:#e8edf5;--mt:#6b7a94;--ac:#40c494;--ac2:#4fa8e0;--ac3:#c97ef7;--wn:#f5a623;--mono:'Space Mono',monospace;--sans:'DM Sans',sans-serif;}
body{font-family:var(--sans);background:var(--bg);color:var(--tx);line-height:1.7;font-size:15px;}
/* hero */
.rm-hero{position:relative;overflow:hidden;padding:80px 40px 64px;text-align:center;border-bottom:1px solid var(--bdr);}
.rm-hero::before{content:'';position:absolute;top:-100px;left:50%;transform:translateX(-50%);width:700px;height:420px;background:radial-gradient(ellipse,rgba(64,196,148,0.13) 0%,rgba(79,168,224,0.06) 45%,transparent 75%);pointer-events:none;}
.rm-pill{display:inline-block;font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--ac);border:1px solid rgba(64,196,148,.35);padding:5px 14px;border-radius:100px;margin-bottom:26px;background:rgba(64,196,148,.06);}
.rm-h1{font-family:var(--mono);font-size:clamp(28px,5vw,48px);font-weight:700;line-height:1.15;margin-bottom:18px;background:linear-gradient(135deg,#e8edf5 0%,#40c494 50%,#4fa8e0 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;}
.rm-hero p{max-width:600px;margin:0 auto 34px;color:var(--mt);font-size:15px;font-weight:300;line-height:1.85;}
.rm-btns{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;}
.rm-btn{font-family:var(--mono);font-size:11px;letter-spacing:.06em;padding:10px 22px;border-radius:6px;text-decoration:none;cursor:pointer;border:none;transition:all .15s;}
.rm-btn-p{background:var(--ac);color:#07090f;font-weight:700;}
.rm-btn-p:hover{background:#56d9ac;}
.rm-btn-o{background:transparent;color:var(--tx);border:1px solid var(--bdr);}
.rm-btn-o:hover{border-color:rgba(255,255,255,.2);background:rgba(255,255,255,.04);}
/* badges */
.rm-badges{display:flex;flex-wrap:wrap;gap:7px;justify-content:center;padding:20px 32px;border-bottom:1px solid var(--bdr);}
.rm-badge{font-family:var(--mono);font-size:10px;padding:4px 11px;border-radius:4px;letter-spacing:.04em;}
.bg{background:rgba(64,196,148,.12);color:var(--ac);border:1px solid rgba(64,196,148,.2);}
.bb{background:rgba(79,168,224,.12);color:var(--ac2);border:1px solid rgba(79,168,224,.2);}
.bp{background:rgba(201,126,247,.12);color:var(--ac3);border:1px solid rgba(201,126,247,.2);}
.bw{background:rgba(245,166,35,.12);color:var(--wn);border:1px solid rgba(245,166,35,.2);}
/* content */
.rm-content{max-width:880px;margin:0 auto;padding:60px 40px;}
.rm-sl{font-family:var(--mono);font-size:10px;letter-spacing:.18em;text-transform:uppercase;color:var(--mt);margin-bottom:10px;display:flex;align-items:center;gap:10px;}
.rm-sl::after{content:'';flex:1;height:1px;background:var(--bdr);}
.rm-h2{font-family:var(--mono);font-size:21px;font-weight:700;color:var(--tx);margin-bottom:20px;}
.rm-p{color:var(--mt);margin-bottom:14px;line-height:1.85;font-size:14px;}
.rm-section{margin-bottom:56px;}
/* callout */
.rm-callout{padding:14px 18px;border-radius:8px;border-left:3px solid;margin:18px 0;font-size:13px;line-height:1.75;}
.rm-ci{background:rgba(79,168,224,.06);border-color:var(--ac2);color:#5a7ea0;}
.rm-cw{background:rgba(245,166,35,.06);border-color:var(--wn);color:#8a6f35;}
.rm-ci strong{color:var(--ac2);}.rm-cw strong{color:var(--wn);}
/* feature grid */
.rm-fgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:1px;background:var(--bdr);border:1px solid var(--bdr);border-radius:10px;overflow:hidden;}
.rm-fc{background:var(--card);padding:22px;transition:background .15s;}
.rm-fc:hover{background:#161d2e;}
.rm-ficon{width:34px;height:34px;border-radius:7px;display:flex;align-items:center;justify-content:center;font-size:16px;margin-bottom:12px;}
.ig{background:rgba(64,196,148,.12);}.ib{background:rgba(79,168,224,.12);}.ip{background:rgba(201,126,247,.12);}.iw{background:rgba(245,166,35,.12);}
.rm-fc h3{font-size:12.5px;font-weight:600;color:var(--tx);margin-bottom:6px;}
.rm-fc p{font-size:12.5px;color:#4d5e77;line-height:1.65;margin:0;}
/* stack */
.rm-sgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.rm-sc{border:1px solid var(--bdr);border-radius:10px;padding:20px;background:var(--card);}
.rm-sch{display:flex;align-items:center;gap:10px;margin-bottom:14px;padding-bottom:12px;border-bottom:1px solid var(--bdr);}
.rm-dot{width:8px;height:8px;border-radius:50%;}
.dg{background:var(--ac);box-shadow:0 0 8px var(--ac);}.db{background:var(--ac2);box-shadow:0 0 8px var(--ac2);}
.rm-sch span{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mt);}
.chips{display:flex;flex-wrap:wrap;gap:6px;}
.chip{font-family:var(--mono);font-size:10px;padding:4px 9px;border-radius:4px;background:rgba(255,255,255,.04);border:1px solid var(--bdr);color:var(--mt);}
/* code blocks */
.rm-cb{background:#06080d;border:1px solid var(--bdr);border-radius:10px;overflow:hidden;margin:16px 0;}
.rm-ch{display:flex;align-items:center;justify-content:space-between;padding:9px 14px;background:rgba(255,255,255,.025);border-bottom:1px solid var(--bdr);}
.dots{display:flex;gap:5px;}.dot{width:9px;height:9px;border-radius:50%;}
.dr{background:#f0606a;}.dy{background:#f5a623;}.dg2{background:#40c494;}
.rm-ct{font-family:var(--mono);font-size:10px;color:var(--mt);letter-spacing:.06em;}
pre{padding:18px 16px;overflow-x:auto;font-family:'Space Mono',monospace;font-size:12px;line-height:1.85;color:#afc0d5;}
.cc{color:#3d5070;}.cg{color:var(--ac);}.cb2{color:var(--ac2);}
/* steps */
.steps{display:flex;flex-direction:column;}
.step{display:flex;gap:18px;padding-bottom:28px;position:relative;}
.step::before{content:'';position:absolute;left:16px;top:36px;bottom:0;width:1px;background:var(--bdr);}
.step:last-child::before{display:none;}
.snum{width:34px;height:34px;border-radius:50%;border:1px solid var(--glow);background:rgba(64,196,148,.08);display:flex;align-items:center;justify-content:center;font-family:var(--mono);font-size:12px;color:var(--ac);flex-shrink:0;}
.sbody{padding-top:5px;flex:1;}
.sbody h3{font-size:14px;font-weight:600;color:var(--tx);margin-bottom:5px;}
.sbody p{font-size:13px;color:var(--mt);margin-bottom:8px;}
/* table */
.dtbl{width:100%;border-collapse:collapse;font-size:12.5px;}
.dtbl th{font-family:var(--mono);font-size:9.5px;letter-spacing:.12em;text-transform:uppercase;color:var(--mt);text-align:left;padding:9px 14px;border-bottom:1px solid var(--bdr);}
.dtbl td{padding:11px 14px;border-bottom:1px solid rgba(255,255,255,.03);color:var(--mt);vertical-align:top;}
.dtbl td:first-child{font-family:var(--mono);color:var(--ac2);font-size:11px;white-space:nowrap;}
.dtbl tr:last-child td{border-bottom:none;}
/* inline code */
.ic{font-family:var(--mono);font-size:11px;background:rgba(255,255,255,.05);border:1px solid var(--bdr);padding:1px 6px;border-radius:4px;color:var(--ac2);}
/* disclaimer */
.discl{border:1px solid var(--bdr);border-radius:10px;padding:18px 22px;background:var(--card);margin-top:32px;font-size:12px;color:#404c62;line-height:1.8;}
.discl strong{color:var(--mt);}
/* footer */
.rm-footer{text-align:center;padding:28px 40px;border-top:1px solid var(--bdr);font-family:var(--mono);font-size:10px;color:#2e3a4d;letter-spacing:.06em;}
.rm-footer span{color:var(--ac);}
@media(max-width:600px){.rm-sgrid{grid-template-columns:1fr;}.rm-content{padding:36px 20px;}.rm-hero{padding:52px 24px 44px;}}
</style>
</head>
<body>

<header class="rm-hero">
  <div class="rm-pill">⬡ Pharmaceutical Intelligence Platform</div>
  <div class="rm-h1">DDI Predict<br>Analytics Suite</div>
  <p>A production-grade AI/Clinical platform for predicting, visualizing, and mitigating complex polypharmacy risks — powered by hybrid ML intelligence and FDA-grade evidence databases.</p>
  <div class="rm-btns">
    <button class="rm-btn rm-btn-p" onclick="document.getElementById('qs').scrollIntoView({behavior:'smooth'})">Quick Start →</button>
    <button class="rm-btn rm-btn-o" onclick="document.getElementById('feat').scrollIntoView({behavior:'smooth'})">Features</button>
    <button class="rm-btn rm-btn-o" onclick="document.getElementById('arch').scrollIntoView({behavior:'smooth'})">Architecture</button>
  </div>
</header>

<div class="rm-badges">
  <span class="rm-badge bg">Python 3.11</span>
  <span class="rm-badge bb">Flask + Waitress</span>
  <span class="rm-badge bp">scikit-learn · LightGBM</span>
  <span class="rm-badge bg">RDKit</span>
  <span class="rm-badge bb">Cytoscape.js</span>
  <span class="rm-badge bp">3Dmol.js</span>
  <span class="rm-badge bw">MIT License</span>
  <span class="rm-badge bb">Docker Ready</span>
</div>

<main class="rm-content">

  <!-- OVERVIEW -->
  <div class="rm-section">
    <div class="rm-sl">Overview</div>
    <div class="rm-h2">Beyond clinical lookup.</div>
    <p class="rm-p">DDI Predict operates on a <strong style="color:#e8edf5;font-weight:600;">hybrid intelligence model</strong> — combining deterministic FDA evidence databases with scalable predictive ML algorithms to surface risks that static tables simply cannot see.</p>
    <p class="rm-p">The platform renders underlying pharmacology natively: spinnable 3D molecular structures, interactive polypharmacy graph networks, and a real-time chronopharmacological dosing timeline that actively staggers administrations to bypass simultaneous metabolic collisions.</p>
    <div class="rm-callout rm-ci"><strong>Research Platform —</strong> DDI Predict is an analytical prediction tool intended for research and clinical education. It does not replace certified medical advice or FDA/EMA safety standards.</div>
  </div>

  <!-- FEATURES -->
  <div class="rm-section" id="feat">
    <div class="rm-sl">Core Modules</div>
    <div class="rm-h2">Intelligence, rendered.</div>
    <div class="rm-fgrid">
      <div class="rm-fc"><div class="rm-ficon ig">🧪</div><h3>Potency AI Lab — pIC50 Engine</h3><p>Real-time binding affinity calculation for unknown structures using RandomForestRegressor trained on RDKit Morgan Fingerprints.</p></div>
      <div class="rm-fc"><div class="rm-ficon ib">🫀</div><h3>Multi-Organ Toxicity Engine</h3><p>RDKit SMARTS scanning detects toxicophores linked to Hepatotoxicity, Cardiotoxicity (hERG), Nephrotoxicity, and Endocrine disruption.</p></div>
      <div class="rm-fc"><div class="rm-ficon ip">📊</div><h3>Adverse Event Predictor</h3><p>ML likelihood modelling forecasting secondary side-effects, surfaced with risk-ranked confidence scores per drug combination.</p></div>
      <div class="rm-fc"><div class="rm-ficon iw">🧬</div><h3>Pharmacogenomics Risk Layer</h3><p>Precision-medicine tracking simulating patient-specific CYP450/SLCO allele vulnerabilities against drug metabolic clearance routes.</p></div>
      <div class="rm-fc"><div class="rm-ficon ib">🔬</div><h3>3D Molecular Viewer</h3><p>Spinnable ball-and-stick rendering via RDKit.AllChem coordinate embedding and 3Dmol.js GPU-accelerated display.</p></div>
      <div class="rm-fc"><div class="rm-ficon ig">⏱</div><h3>Chronopharmacological Timeline</h3><p>Live engine staggering drug administrations across 24 hours to bypass simultaneous serum metabolic collisions.</p></div>
      <div class="rm-fc"><div class="rm-ficon ip">🕸</div><h3>Polypharmacy Graph Network</h3><p>Cytoscape.js neural webbing visualising complex multi-drug combos (&gt;2 drugs), dynamically identifying worst-offender nodes.</p></div>
      <div class="rm-fc"><div class="rm-ficon iw">🤖</div><h3>Medical AI Chatbot</h3><p>Context-aware clinical assistant generating structural mechanics breakdowns and bioisostere substitution recommendations.</p></div>
    </div>
  </div>

  <!-- ARCHITECTURE -->
  <div class="rm-section" id="arch">
    <div class="rm-sl">Architecture</div>
    <div class="rm-h2">Tech stack.</div>
    <div class="rm-sgrid">
      <div class="rm-sc">
        <div class="rm-sch"><div class="rm-dot dg"></div><span>Backend Engine</span></div>
        <div class="chips"><span class="chip">Python 3.11</span><span class="chip">Flask</span><span class="chip">Waitress WSGI</span><span class="chip">scikit-learn</span><span class="chip">LightGBM</span><span class="chip">RDKit</span><span class="chip">pandas</span><span class="chip">numpy</span></div>
      </div>
      <div class="rm-sc">
        <div class="rm-sch"><div class="rm-dot db"></div><span>Frontend Interface</span></div>
        <div class="chips"><span class="chip">Vanilla JS/CSS</span><span class="chip">Chart.js</span><span class="chip">Cytoscape.js</span><span class="chip">3Dmol.js</span></div>
      </div>
    </div>
  </div>

  <!-- QUICK START -->
  <div class="rm-section" id="qs">
    <div class="rm-sl">Quick Start</div>
    <div class="rm-h2">Up in minutes.</div>
    <div class="steps">
      <div class="step">
        <div class="snum">1</div>
        <div class="sbody">
          <h3>Clone the repository</h3>
          <div class="rm-cb"><div class="rm-ch"><div class="dots"><div class="dot dr"></div><div class="dot dy"></div><div class="dot dg2"></div></div><div class="rm-ct">terminal</div></div><pre><span class="cc"># Clone and enter the project</span>
git clone https://github.com/your-username/DDI-Predict.git
cd DDI-Predict</pre></div>
        </div>
      </div>
      <div class="step">
        <div class="snum">2</div>
        <div class="sbody">
          <h3>Create a virtual environment</h3>
          <p>Strongly recommended — RDKit and LightGBM carry heavy C++ binding requirements.</p>
          <div class="rm-cb"><div class="rm-ch"><div class="dots"><div class="dot dr"></div><div class="dot dy"></div><div class="dot dg2"></div></div><div class="rm-ct">terminal</div></div><pre>python -m venv .venv
<span class="cc"># Unix / macOS</span>
source .venv/bin/activate
<span class="cc"># Windows</span>
.venv\Scripts\activate</pre></div>
        </div>
      </div>
      <div class="step">
        <div class="snum">3</div>
        <div class="sbody">
          <h3>Install dependencies</h3>
          <div class="rm-cb"><div class="rm-ch"><div class="dots"><div class="dot dr"></div><div class="dot dy"></div><div class="dot dg2"></div></div><div class="rm-ct">terminal</div></div><pre>pip install -r backend/requirements.txt</pre></div>
        </div>
      </div>
      <div class="step">
        <div class="snum">4</div>
        <div class="sbody">
          <h3>Launch the application</h3>
          <p>The service spins up the web UI on port 5005.</p>
          <div class="rm-cb"><div class="rm-ch"><div class="dots"><div class="dot dr"></div><div class="dot dy"></div><div class="dot dg2"></div></div><div class="rm-ct">terminal</div></div><pre>cd backend
python app.py
<span class="cc"># → http://localhost:5005</span></pre></div>
        </div>
      </div>
    </div>

    <div class="rm-sl" style="margin-top:8px;">Docker</div>
    <p class="rm-p">Recommended for all production deployments — includes native system deps like <span class="ic">libxrender1</span>.</p>
    <div class="rm-cb"><div class="rm-ch"><div class="dots"><div class="dot dr"></div><div class="dot dy"></div><div class="dot dg2"></div></div><div class="rm-ct">dockerfile</div></div><pre>docker build -t ddi-predict .
docker run -p 5005:5005 ddi-predict</pre></div>
  </div>

  <!-- DATA -->
  <div class="rm-section">
    <div class="rm-sl">Data Requirements</div>
    <div class="rm-h2">Required datasets.</div>
    <p class="rm-p">Three critical files must be present before running mapping and inference at scale. These are not bundled in the repository.</p>
    <div class="rm-cb" style="margin-bottom:0;">
      <div class="rm-ch"><div class="dots"><div class="dot dr"></div><div class="dot dy"></div><div class="dot dg2"></div></div><div class="rm-ct">required files</div></div>
      <table class="dtbl">
        <thead><tr><th>File</th><th>Purpose</th></tr></thead>
        <tbody>
          <tr><td>db_drug_interactions.csv</td><td>Sourced core clinical interaction rules</td></tr>
          <tr><td>SMILES_Big_Data_Set.csv</td><td>Fingerprint dataset mapping for pIC50 and toxicity engines</td></tr>
          <tr><td>ddi_model.pkl</td><td>Compiled DDI classification model</td></tr>
          <tr><td>pic50_model.pkl</td><td>Compiled binding affinity regression model</td></tr>
          <tr><td>toxicity_model.pkl</td><td>Compiled multi-organ toxicity prediction model</td></tr>
        </tbody>
      </table>
    </div>
    <div class="rm-callout rm-cw" style="margin-top:18px;"><strong>Serverless hosts:</strong> Lambda size limits (~250MB) on platforms like Vercel will be exceeded by ML model artifacts. Use containerised hosts — Render, Railway, or Heroku. See <span class="ic">Dockerfile</span> for the recommended config.</div>
  </div>

  <!-- LICENSE -->
  <div class="rm-section">
    <div class="rm-sl">License</div>
    <div class="rm-h2">Open source.</div>
    <p class="rm-p">Distributed under the <strong style="color:#e8edf5;">MIT License</strong>. See <span class="ic">LICENSE</span> for full terms.</p>
    <div class="discl"><strong>Research Disclaimer —</strong> DDI Predict is an analytical prediction platform built for research and academic presentation. All predictions are probabilistic and should be interpreted accordingly. This tool does not constitute certified professional medical advice and must not be used as a substitute for validated FDA/EMA clinical safety evaluation processes.</div>
  </div>

</main>

<footer class="rm-footer">
  DDI Predict Analytics Suite &nbsp;·&nbsp; MIT License &nbsp;·&nbsp; Built with <span>♥</span> for the clinical research community
</footer>

</body>
</html>
