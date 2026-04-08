<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DDI Predict Analytics Suite</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #020810;
  --bg2: #060f1e;
  --panel: rgba(10,25,50,0.7);
  --teal: #00e5c4;
  --teal2: #00b89e;
  --blue: #0077ff;
  --purple: #7c3aed;
  --amber: #f59e0b;
  --danger: #ef4444;
  --text: #e2f0ff;
  --muted: #6b8db5;
  --border: rgba(0,229,196,0.15);
}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:'Syne',sans-serif;overflow-x:hidden;min-height:100vh}

/* ── CANVAS BACKGROUND ── */
#bg-canvas{position:fixed;top:0;left:0;width:100%;height:100%;z-index:0;opacity:0.35}

/* ── LAYOUT ── */
.wrap{position:relative;z-index:1;max-width:860px;margin:0 auto;padding:0 24px}

/* ── HERO ── */
.hero{min-height:100vh;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:80px 24px 60px;position:relative;z-index:1}
.dna-ring{width:120px;height:120px;margin:0 auto 32px;position:relative}
.dna-ring svg{width:100%;height:100%}

.hero-eyebrow{font-family:'Space Mono',monospace;font-size:11px;letter-spacing:0.2em;color:var(--teal);text-transform:uppercase;margin-bottom:20px;opacity:0;animation:fadeUp 0.8s 0.3s forwards}
.hero h1{font-size:clamp(36px,6vw,72px);font-weight:800;line-height:1.05;margin-bottom:16px;opacity:0;animation:fadeUp 0.8s 0.5s forwards}
.hero h1 span{background:linear-gradient(135deg,var(--teal),var(--blue));-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:16px;color:var(--muted);line-height:1.7;max-width:540px;margin:0 auto 36px;opacity:0;animation:fadeUp 0.8s 0.7s forwards}

/* badges */
.badges{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin-bottom:36px;opacity:0;animation:fadeUp 0.8s 0.9s forwards}
.badge{display:inline-flex;align-items:center;gap:6px;padding:5px 12px;border-radius:4px;border:1px solid var(--border);background:rgba(0,229,196,0.05);font-family:'Space Mono',monospace;font-size:10px;color:var(--teal);letter-spacing:0.05em}
.badge-dot{width:6px;height:6px;border-radius:50%;background:var(--teal);animation:pulse 2s infinite}

/* CTA */
.cta-row{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;opacity:0;animation:fadeUp 0.8s 1.1s forwards}
.btn-primary{padding:12px 28px;border-radius:6px;background:linear-gradient(135deg,var(--teal2),var(--blue));color:#000;font-family:'Syne',sans-serif;font-weight:700;font-size:14px;border:none;cursor:pointer;text-decoration:none;display:inline-block;transition:transform 0.2s,box-shadow 0.2s}
.btn-primary:hover{transform:translateY(-2px);box-shadow:0 8px 24px rgba(0,229,196,0.3)}
.btn-ghost{padding:12px 28px;border-radius:6px;background:transparent;color:var(--teal);font-family:'Syne',sans-serif;font-weight:600;font-size:14px;border:1px solid var(--border);cursor:pointer;text-decoration:none;display:inline-block;transition:background 0.2s,transform 0.2s}
.btn-ghost:hover{background:rgba(0,229,196,0.08);transform:translateY(-2px)}

/* scroll indicator */
.scroll-hint{margin-top:60px;opacity:0;animation:fadeUp 0.8s 1.4s forwards;display:flex;flex-direction:column;align-items:center;gap:8px;color:var(--muted);font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.1em}
.scroll-line{width:1px;height:40px;background:linear-gradient(to bottom,var(--teal),transparent);animation:scrollPulse 2s 2s infinite}

/* ── SECTIONS ── */
section{padding:80px 0;position:relative;z-index:1}
.section-tag{font-family:'Space Mono',monospace;font-size:10px;letter-spacing:0.2em;color:var(--teal);text-transform:uppercase;margin-bottom:12px;display:flex;align-items:center;gap:8px}
.section-tag::before{content:'';display:block;width:20px;height:1px;background:var(--teal)}
.section-title{font-size:32px;font-weight:700;margin-bottom:8px}
.section-desc{color:var(--muted);font-size:15px;line-height:1.7;max-width:560px;margin-bottom:40px}

/* ── OVERVIEW STRIP ── */
.overview{background:linear-gradient(135deg,rgba(0,229,196,0.05),rgba(0,119,255,0.05));border:1px solid var(--border);border-radius:12px;padding:32px;margin-bottom:0;position:relative;overflow:hidden}
.overview::before{content:'POLYPHARMACY IS DANGEROUS';position:absolute;top:16px;right:20px;font-family:'Space Mono',monospace;font-size:9px;color:rgba(0,229,196,0.2);letter-spacing:0.15em}
.overview p{font-size:16px;line-height:1.8;color:var(--text)}
.overview strong{color:var(--teal)}

/* ── TRANSMISSION ANIMATION CARD ── */
.transmission-wrapper{margin:40px 0;border:1px solid var(--border);border-radius:12px;overflow:hidden;background:var(--panel)}
.transmission-header{padding:16px 24px;border-bottom:1px solid var(--border);display:flex;align-items:center;gap:10px;font-family:'Space Mono',monospace;font-size:11px;color:var(--teal)}
.dot{width:8px;height:8px;border-radius:50%}
.dot-r{background:#ef4444}
.dot-y{background:#f59e0b}
.dot-g{background:#22c55e}
#transmission-canvas{width:100%;height:220px;display:block}

/* ── MODULE CARDS ── */
.module-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}
.module-card{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:24px;position:relative;overflow:hidden;transition:border-color 0.3s,transform 0.3s;cursor:default}
.module-card:hover{border-color:var(--teal);transform:translateY(-4px)}
.module-card::after{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(0,229,196,0.04),transparent);opacity:0;transition:opacity 0.3s}
.module-card:hover::after{opacity:1}
.module-icon{width:36px;height:36px;border-radius:8px;background:rgba(0,229,196,0.1);border:1px solid rgba(0,229,196,0.2);display:flex;align-items:center;justify-content:center;font-size:18px;margin-bottom:14px}
.module-title{font-size:14px;font-weight:700;color:var(--text);margin-bottom:6px}
.module-desc{font-size:12px;color:var(--muted);line-height:1.7}
.module-tag{display:inline-block;margin-top:12px;padding:2px 8px;border-radius:3px;font-family:'Space Mono',monospace;font-size:9px;background:rgba(0,229,196,0.08);color:var(--teal);border:1px solid rgba(0,229,196,0.2)}

/* ── VISUALIZATION TABLE ── */
.viz-table{width:100%;border-collapse:collapse;font-size:13px}
.viz-table th{padding:10px 16px;text-align:left;font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.1em;color:var(--muted);border-bottom:1px solid var(--border);text-transform:uppercase}
.viz-table td{padding:14px 16px;border-bottom:1px solid rgba(0,229,196,0.06);color:var(--text);vertical-align:top}
.viz-table tr:last-child td{border-bottom:none}
.viz-table tr:hover td{background:rgba(0,229,196,0.03)}
.viz-table td strong{color:var(--teal)}
.viz-table .tech-badge{font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);background:rgba(255,255,255,0.04);padding:2px 6px;border-radius:3px;border:1px solid rgba(255,255,255,0.08)}

/* ── STACK ── */
.stack-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.stack-panel{background:var(--panel);border:1px solid var(--border);border-radius:10px;padding:20px}
.stack-label{font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.15em;color:var(--teal);text-transform:uppercase;margin-bottom:14px}
.pill-grid{display:flex;flex-wrap:wrap;gap:6px}
.pill{padding:3px 10px;border-radius:20px;font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);border:1px solid var(--border);background:rgba(255,255,255,0.02)}

/* ── CODE STEPS ── */
.code-steps{border:1px solid var(--border);border-radius:10px;overflow:hidden;background:var(--panel)}
.code-step{display:flex;gap:0;border-bottom:1px solid var(--border)}
.code-step:last-child{border-bottom:none}
.step-num{min-width:48px;display:flex;align-items:center;justify-content:center;font-family:'Space Mono',monospace;font-size:10px;color:var(--teal);background:rgba(0,229,196,0.04);border-right:1px solid var(--border);padding:14px 0}
.step-body{padding:14px 20px;flex:1}
.step-label{font-size:11px;color:var(--muted);margin-bottom:5px}
.step-cmd{font-family:'Space Mono',monospace;font-size:12px;color:var(--text);word-break:break-all}
.step-cmd .cmd-green{color:var(--teal)}
.step-cmd .cmd-muted{color:var(--muted)}

/* ── DATA TABLE ── */
.data-table{width:100%;border-collapse:collapse;font-size:13px;margin-top:16px}
.data-table th{padding:8px 16px;text-align:left;font-family:'Space Mono',monospace;font-size:9px;letter-spacing:0.1em;color:var(--muted);border-bottom:1px solid var(--border);text-transform:uppercase}
.data-table td{padding:12px 16px;border-bottom:1px solid rgba(0,229,196,0.06);color:var(--text)}
.data-table td:first-child{font-family:'Space Mono',monospace;font-size:11px;color:var(--teal)}
.data-table tr:last-child td{border-bottom:none}

/* ── DISCLAIMER ── */
.disclaimer{margin-top:60px;padding:20px 24px;border-radius:10px;border:1px solid rgba(245,158,11,0.3);background:rgba(245,158,11,0.05);display:flex;gap:12px;align-items:flex-start}
.disclaimer-icon{color:var(--amber);font-size:16px;flex-shrink:0;margin-top:1px}
.disclaimer p{font-size:12px;color:#b3975e;line-height:1.7}
.disclaimer strong{color:var(--amber)}

/* ── FOOTER ── */
footer{border-top:1px solid var(--border);padding:32px 0;text-align:center;position:relative;z-index:1}
footer p{font-family:'Space Mono',monospace;font-size:10px;color:var(--muted);letter-spacing:0.05em}
footer a{color:var(--teal);text-decoration:none}

/* ── DIVIDER ── */
.divider{border:none;border-top:1px solid var(--border);margin:0}

/* ── ANIMATIONS ── */
@keyframes fadeUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:0.5;transform:scale(0.8)}}
@keyframes scrollPulse{0%,100%{opacity:0.4}50%{opacity:1}}
@keyframes spin{from{transform:rotate(0deg)}to{transform:rotate(360deg)}}

/* reveal on scroll */
.reveal{opacity:0;transform:translateY(30px);transition:opacity 0.7s,transform 0.7s}
.reveal.visible{opacity:1;transform:translateY(0)}

@media(max-width:600px){
  .stack-grid{grid-template-columns:1fr}
  .module-grid{grid-template-columns:1fr}
  .hero h1{font-size:36px}
}
</style>
</head>
<body>

<canvas id="bg-canvas"></canvas>

<!-- HERO -->
<div class="hero">
  <div style="opacity:0;animation:fadeUp 1s 0.1s forwards">
    <!-- DNA ring SVG -->
    <div class="dna-ring">
      <svg viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="60" cy="60" r="54" stroke="rgba(0,229,196,0.15)" stroke-width="1"/>
        <circle cx="60" cy="60" r="42" stroke="rgba(0,229,196,0.1)" stroke-width="1" stroke-dasharray="4 4"/>
        <g id="dna-rotate" style="transform-origin:60px 60px;animation:spin 8s linear infinite">
          <circle cx="60" cy="6" r="5" fill="var(--teal)" opacity="0.9"/>
          <circle cx="60" cy="114" r="5" fill="var(--blue)" opacity="0.9"/>
          <line x1="60" y1="6" x2="60" y2="114" stroke="rgba(0,229,196,0.2)" stroke-width="1" stroke-dasharray="3 5"/>
        </g>
        <g id="dna-rotate2" style="transform-origin:60px 60px;animation:spin 8s linear infinite reverse">
          <circle cx="6" cy="60" r="4" fill="var(--purple)" opacity="0.9"/>
          <circle cx="114" cy="60" r="4" fill="var(--amber)" opacity="0.9"/>
          <line x1="6" y1="60" x2="114" y2="60" stroke="rgba(0,119,255,0.2)" stroke-width="1" stroke-dasharray="3 5"/>
        </g>
        <g id="dna-rotate3" style="transform-origin:60px 60px;animation:spin 12s linear infinite">
          <circle cx="98" cy="17" r="3.5" fill="var(--teal)" opacity="0.6"/>
          <circle cx="22" cy="103" r="3.5" fill="var(--blue)" opacity="0.6"/>
        </g>
        <circle cx="60" cy="60" r="18" stroke="rgba(0,229,196,0.4)" stroke-width="1.5"/>
        <circle cx="60" cy="60" r="10" fill="rgba(0,229,196,0.1)" stroke="rgba(0,229,196,0.6)" stroke-width="1.5"/>
        <circle cx="60" cy="60" r="4" fill="var(--teal)"/>
      </svg>
    </div>
  </div>

  <p class="hero-eyebrow">Pharmaceutical Intelligence Platform</p>
  <h1>DDI Predict<br><span>Analytics Suite</span></h1>
  <p class="hero-sub">Predicting and visualizing drug–drug interactions using machine learning and clinical heuristics — before they reach the patient.</p>

  <div class="badges">
    <span class="badge"><span class="badge-dot"></span>Live on Render</span>
    <span class="badge">Python 3.11</span>
    <span class="badge">Flask · Waitress</span>
    <span class="badge">Docker Ready</span>
    <span class="badge">MIT License</span>
  </div>

  <div class="cta-row">
    <a href="https://ddi-lcyj.onrender.com" class="btn-primary" target="_blank">View live platform ↗</a>
    <a href="https://github.com/pandashreyan/DDI/issues" class="btn-ghost" target="_blank">Report a bug</a>
  </div>

  <div class="scroll-hint">
    <div class="scroll-line"></div>
    <span>scroll to explore</span>
  </div>
</div>

<!-- OVERVIEW -->
<div class="wrap">
  <section class="reveal">
    <div class="section-tag">Overview</div>
    <div class="overview">
      <p><strong>Polypharmacy is dangerous.</strong> DDI Predict combines deterministic FDA evidence databases with predictive ML algorithms to identify, analyze, and mitigate complex medication risks before they reach the patient.</p>
      <br>
      <p>Beyond standard clinical lookup tools, the platform renders pharmacological interactions as <strong>interactive graph networks</strong> and <strong>3D molecular structures</strong> — and automatically generates safe, chronopharmacological dosing regimens for polypharmacy patients.</p>
    </div>
  </section>

  <!-- TRANSMISSION ANIMATION -->
  <section class="reveal">
    <div class="section-tag">Live signal</div>
    <div class="transmission-wrapper">
      <div class="transmission-header">
        <span class="dot dot-r"></span>
        <span class="dot dot-y"></span>
        <span class="dot dot-g"></span>
        <span style="margin-left:8px">DDI · Real-time interaction transmission monitor</span>
        <span style="margin-left:auto;color:var(--teal);animation:pulse 1.5s infinite">● LIVE</span>
      </div>
      <canvas id="transmission-canvas"></canvas>
    </div>
  </section>

  <!-- MODULES -->
  <section class="reveal">
    <div class="section-tag">Core intelligence</div>
    <div class="section-title">Four prediction engines</div>
    <p class="section-desc">A hybrid intelligence model — deterministic rules meet scalable ML across the full pharmacological stack.</p>
    <div class="module-grid">
      <div class="module-card">
        <div class="module-icon">🔬</div>
        <div class="module-title">Potency AI Lab (pIC50)</div>
        <div class="module-desc">Real-time binding affinity calculation for uncatalogued chemical structures via RandomForestRegressor and RDKit Morgan fingerprints. Supports SMILES input for any novel compound.</div>
        <span class="module-tag">RandomForest · RDKit</span>
      </div>
      <div class="module-card">
        <div class="module-icon">☣️</div>
        <div class="module-title">Multi-organ toxicity engine</div>
        <div class="module-desc">SMARTS-based structural scanning detecting toxicophores for hepatotoxicity, hERG cardiotoxicity, nephrotoxicity, and endocrine disruption from a single molecular structure.</div>
        <span class="module-tag">SMARTS · RDKit</span>
      </div>
      <div class="module-card">
        <div class="module-icon">📈</div>
        <div class="module-title">Adverse event predictor</div>
        <div class="module-desc">ML likelihood modeling forecasting secondary physiological side-effects with probabilistic confidence scoring — enabling proactive clinical risk management.</div>
        <span class="module-tag">ML classification</span>
      </div>
      <div class="module-card">
        <div class="module-icon">🧬</div>
        <div class="module-title">Pharmacogenomics risk layer</div>
        <div class="module-desc">Precision-medicine tracking simulating patient-specific CYP450/SLCO allele vulnerabilities against drug metabolic clearance routes — surfacing risks invisible to population-level lookups.</div>
        <span class="module-tag">PGx · CYP450</span>
      </div>
    </div>
  </section>

  <hr class="divider">

  <!-- VISUALIZATIONS -->
  <section class="reveal">
    <div class="section-tag">Visualizations</div>
    <div class="section-title">Clinical-grade rendering</div>
    <table class="viz-table">
      <thead>
        <tr>
          <th>Feature</th>
          <th>Description</th>
          <th>Powered by</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>3D molecular viewer</strong></td>
          <td>Spinnable ball-and-stick rendering for any compound in the database</td>
          <td><span class="tech-badge">RDKit.AllChem</span> <span class="tech-badge">3Dmol.js</span></td>
        </tr>
        <tr>
          <td><strong>Dosing timeline</strong></td>
          <td>24-hour staggered scheduling to prevent serum metabolic collisions</td>
          <td><span class="tech-badge">Custom engine</span></td>
        </tr>
        <tr>
          <td><strong>Polypharmacy graph</strong></td>
          <td>Interactive network map for &gt;2-drug combos, flagging worst-offender pairs</td>
          <td><span class="tech-badge">Cytoscape.js</span></td>
        </tr>
        <tr>
          <td><strong>Medical AI chatbot</strong></td>
          <td>Context-aware assistant for mechanism breakdowns and bioisostere substitution</td>
          <td><span class="tech-badge">Rules engine</span></td>
        </tr>
      </tbody>
    </table>
  </section>

  <hr class="divider">

  <!-- STACK -->
  <section class="reveal">
    <div class="section-tag">Architecture</div>
    <div class="section-title">Tech stack</div>
    <div class="stack-grid">
      <div class="stack-panel">
        <div class="stack-label">Backend</div>
        <div class="pill-grid">
          <span class="pill">Python 3.11</span>
          <span class="pill">Flask</span>
          <span class="pill">Waitress WSGI</span>
          <span class="pill">scikit-learn</span>
          <span class="pill">LightGBM</span>
          <span class="pill">RDKit</span>
          <span class="pill">pandas</span>
          <span class="pill">numpy</span>
          <span class="pill">PyTDC</span>
        </div>
      </div>
      <div class="stack-panel">
        <div class="stack-label">Frontend</div>
        <div class="pill-grid">
          <span class="pill">Vanilla JS</span>
          <span class="pill">HTML5</span>
          <span class="pill">Chart.js</span>
          <span class="pill">Cytoscape.js</span>
          <span class="pill">3Dmol.js</span>
        </div>
      </div>
    </div>
  </section>

  <hr class="divider">

  <!-- QUICK START -->
  <section class="reveal">
    <div class="section-tag">Getting started</div>
    <div class="section-title">Quick start</div>
    <p class="section-desc">A virtual environment is strongly recommended due to RDKit and LightGBM's C++ binding requirements.</p>
    <div class="code-steps">
      <div class="code-step">
        <div class="step-num">01</div>
        <div class="step-body">
          <div class="step-label">Clone the repository</div>
          <div class="step-cmd"><span class="cmd-green">git clone</span> https://github.com/pandashreyan/DDI.git <span class="cmd-muted">&amp;&amp; cd DDI</span></div>
        </div>
      </div>
      <div class="code-step">
        <div class="step-num">02</div>
        <div class="step-body">
          <div class="step-label">Create and activate a virtual environment</div>
          <div class="step-cmd"><span class="cmd-green">python -m venv</span> .venv <span class="cmd-muted">&amp;&amp; source .venv/bin/activate</span></div>
        </div>
      </div>
      <div class="code-step">
        <div class="step-num">03</div>
        <div class="step-body">
          <div class="step-label">Install dependencies</div>
          <div class="step-cmd"><span class="cmd-green">pip install</span> -r backend/requirements.txt</div>
        </div>
      </div>
      <div class="code-step">
        <div class="step-num">04</div>
        <div class="step-body">
          <div class="step-label">Start the server → http://localhost:5005</div>
          <div class="step-cmd"><span class="cmd-muted">cd backend &&</span> <span class="cmd-green">python</span> app.py</div>
        </div>
      </div>
    </div>
    <p style="font-size:12px;color:var(--muted);margin-top:12px;font-family:'Space Mono',monospace">Docker: docker build -t ddi-predict . &amp;&amp; docker run -p 10000:10000 ddi-predict</p>
  </section>

  <hr class="divider">

  <!-- DATA -->
  <section class="reveal">
    <div class="section-tag">Data &amp; Models</div>
    <div class="section-title">Included datasets</div>
    <p class="section-desc">Large <code style="font-family:'Space Mono',monospace;color:var(--teal);font-size:12px">.pkl</code> model files and <code style="font-family:'Space Mono',monospace;color:var(--teal);font-size:12px">.npy</code> arrays are excluded via <code style="font-family:'Space Mono',monospace;color:var(--teal);font-size:12px">.gitignore</code>. The system degrades gracefully — missing models retrain at startup.</p>
    <table class="data-table">
      <thead>
        <tr><th>File</th><th>Description</th></tr>
      </thead>
      <tbody>
        <tr><td>db_drug_interactions.csv</td><td>Core clinical interaction rules</td></tr>
        <tr><td>SMILES_Big_Data_Set.csv</td><td>Fingerprint mapping dataset</td></tr>
        <tr><td>drug_metadata.json</td><td>Drug properties and deep-link references</td></tr>
        <tr><td>expert_interactions.json</td><td>Curated mechanistic interaction data</td></tr>
      </tbody>
    </table>
  </section>

  <!-- DISCLAIMER -->
  <div class="disclaimer reveal">
    <div class="disclaimer-icon">⚠</div>
    <p><strong>Disclaimer:</strong> DDI Predict is an analytical prediction platform intended for research and educational purposes only. It does not replace certified professional medical advice or FDA/EMA clinical safety standards.</p>
  </div>
</div>

<!-- FOOTER -->
<footer>
  <div class="wrap">
    <p>MIT License · <a href="https://github.com/pandashreyan/DDI" target="_blank">github.com/pandashreyan/DDI</a> · Built by Shreyan Panda</p>
  </div>
</footer>

<script>
/* ── PARTICLE BACKGROUND ── */
const bgCanvas = document.getElementById('bg-canvas');
const bgCtx = bgCanvas.getContext('2d');
let W, H, particles = [], connections = [];

function resize(){
  W = bgCanvas.width = window.innerWidth;
  H = bgCanvas.height = window.innerHeight;
}
resize();
window.addEventListener('resize', resize);

class Particle {
  constructor(){this.reset()}
  reset(){
    this.x = Math.random()*W;
    this.y = Math.random()*H;
    this.vx = (Math.random()-0.5)*0.4;
    this.vy = (Math.random()-0.5)*0.4;
    this.r = Math.random()*2+0.5;
    this.color = Math.random()>0.5?'rgba(0,229,196,':'rgba(0,119,255,';
    this.alpha = Math.random()*0.5+0.2;
  }
  update(){
    this.x+=this.vx; this.y+=this.vy;
    if(this.x<0||this.x>W||this.y<0||this.y>H) this.reset();
  }
  draw(){
    bgCtx.beginPath();
    bgCtx.arc(this.x,this.y,this.r,0,Math.PI*2);
    bgCtx.fillStyle=this.color+this.alpha+')';
    bgCtx.fill();
  }
}

for(let i=0;i<80;i++) particles.push(new Particle());

function bgLoop(){
  bgCtx.clearRect(0,0,W,H);
  for(let i=0;i<particles.length;i++){
    particles[i].update();
    particles[i].draw();
    for(let j=i+1;j<particles.length;j++){
      const dx=particles[i].x-particles[j].x;
      const dy=particles[i].y-particles[j].y;
      const d=Math.sqrt(dx*dx+dy*dy);
      if(d<120){
        bgCtx.beginPath();
        bgCtx.moveTo(particles[i].x,particles[i].y);
        bgCtx.lineTo(particles[j].x,particles[j].y);
        bgCtx.strokeStyle=`rgba(0,229,196,${0.08*(1-d/120)})`;
        bgCtx.lineWidth=0.5;
        bgCtx.stroke();
      }
    }
  }
  requestAnimationFrame(bgLoop);
}
bgLoop();

/* ── TRANSMISSION CANVAS ── */
const txCanvas = document.getElementById('transmission-canvas');
const txCtx = txCanvas.getContext('2d');
let txW, txH;

function txResize(){
  txW = txCanvas.width = txCanvas.offsetWidth * window.devicePixelRatio;
  txH = txCanvas.height = txCanvas.offsetHeight * window.devicePixelRatio;
  txCtx.scale(window.devicePixelRatio, window.devicePixelRatio);
}

const drugs = ['Warfarin','Aspirin','Metformin','Lisinopril','Atorvastatin','Amiodarone','Digoxin','Clopidogrel'];
const drugColors = ['#00e5c4','#0077ff','#7c3aed','#f59e0b','#00e5c4','#ef4444','#0077ff','#7c3aed'];

class Signal {
  constructor(){
    this.drug1 = Math.floor(Math.random()*drugs.length);
    do{this.drug2=Math.floor(Math.random()*drugs.length)}while(this.drug2===this.drug1);
    this.progress = 0;
    this.speed = 0.004 + Math.random()*0.006;
    this.severity = Math.random()>0.6?'high':Math.random()>0.5?'moderate':'low';
    this.color = this.severity==='high'?'#ef4444':this.severity==='moderate'?'#f59e0b':'#00e5c4';
    this.alive = true;
    this.pulses = [];
    for(let i=0;i<3;i++) this.pulses.push({t:Math.random(), v:Math.random()*0.3+0.1});
  }
  update(){
    this.progress += this.speed;
    if(this.progress>1) this.alive=false;
  }
}

let signals = [];
let txTime = 0;
let lastSignalTime = 0;

const nodePositions = [];

function drawTransmission(){
  const cW = txCanvas.offsetWidth;
  const cH = txCanvas.offsetHeight;
  txCtx.clearRect(0,0,cW,cH);
  txTime+=0.016;

  // spawn signals
  if(txTime-lastSignalTime>1.5+Math.random()*2){
    signals.push(new Signal());
    lastSignalTime=txTime;
  }
  signals=signals.filter(s=>s.alive);

  // node layout
  const cols=4, rows=2;
  const nW=cW, nH=cH;
  const padX=60, padY=30;
  const cellW=(nW-padX*2)/(cols-1);
  const cellH=(nH-padY*2)/(rows-1);

  // draw grid lines
  txCtx.setLineDash([2,6]);
  txCtx.strokeStyle='rgba(0,229,196,0.06)';
  txCtx.lineWidth=0.5;
  for(let r=0;r<rows;r++){
    for(let c=0;c<cols;c++){
      const x=padX+c*cellW, y=padY+r*cellH;
      if(c<cols-1){
        txCtx.beginPath();
        txCtx.moveTo(x,y);
        txCtx.lineTo(x+cellW,y);
        txCtx.stroke();
      }
      if(r<rows-1){
        txCtx.beginPath();
        txCtx.moveTo(x,y);
        txCtx.lineTo(x,y+cellH);
        txCtx.stroke();
      }
    }
  }
  txCtx.setLineDash([]);

  // build node positions
  nodePositions.length=0;
  for(let r=0;r<rows;r++){
    for(let c=0;c<cols;c++){
      const idx=r*cols+c;
      nodePositions.push({x:padX+c*cellW, y:padY+r*cellH, drug:drugs[idx]||'Drug'+(idx+1), color:drugColors[idx]||'#00e5c4'});
    }
  }

  // draw signals as arcs
  signals.forEach(s=>{
    const n1=nodePositions[s.drug1];
    const n2=nodePositions[s.drug2];
    if(!n1||!n2) return;
    s.update();
    const p=s.progress;
    const ex=n1.x+(n2.x-n1.x)*p;
    const ey=n1.y+(n2.y-n1.y)*p;
    // trail
    txCtx.beginPath();
    txCtx.moveTo(n1.x,n1.y);
    txCtx.lineTo(ex,ey);
    txCtx.strokeStyle=s.color;
    txCtx.lineWidth=1;
    txCtx.globalAlpha=0.3;
    txCtx.stroke();
    txCtx.globalAlpha=1;
    // head
    txCtx.beginPath();
    txCtx.arc(ex,ey,4,0,Math.PI*2);
    txCtx.fillStyle=s.color;
    txCtx.fill();
    // glow
    txCtx.beginPath();
    txCtx.arc(ex,ey,8,0,Math.PI*2);
    txCtx.fillStyle=s.color+'33';
    txCtx.fill();
  });

  // draw nodes
  nodePositions.forEach((n,i)=>{
    const pulse=Math.sin(txTime*2+i)*3;
    // outer ring
    txCtx.beginPath();
    txCtx.arc(n.x,n.y,14+pulse*0.3,0,Math.PI*2);
    txCtx.strokeStyle=n.color+'44';
    txCtx.lineWidth=1;
    txCtx.stroke();
    // inner circle
    txCtx.beginPath();
    txCtx.arc(n.x,n.y,9,0,Math.PI*2);
    txCtx.fillStyle=n.color+'22';
    txCtx.fill();
    txCtx.strokeStyle=n.color;
    txCtx.lineWidth=1.5;
    txCtx.stroke();
    // dot
    txCtx.beginPath();
    txCtx.arc(n.x,n.y,3,0,Math.PI*2);
    txCtx.fillStyle=n.color;
    txCtx.fill();
    // label
    txCtx.fillStyle='rgba(180,210,255,0.8)';
    txCtx.font='9px "Space Mono", monospace';
    txCtx.textAlign='center';
    txCtx.fillText(n.drug, n.x, n.y+24);
  });

  // severity legend
  const legends=[{c:'#ef4444',l:'HIGH'},{ c:'#f59e0b',l:'MOD'},{c:'#00e5c4',l:'LOW'}];
  legends.forEach((lv,i)=>{
    const lx=cW-80, ly=12+i*16;
    txCtx.beginPath();
    txCtx.arc(lx,ly,4,0,Math.PI*2);
    txCtx.fillStyle=lv.c;
    txCtx.fill();
    txCtx.fillStyle='rgba(107,141,181,0.9)';
    txCtx.font='9px "Space Mono",monospace';
    txCtx.textAlign='left';
    txCtx.fillText(lv.l,lx+8,ly+3);
  });

  requestAnimationFrame(drawTransmission);
}

setTimeout(()=>{
  txResize();
  drawTransmission();
},200);

window.addEventListener('resize',txResize);

/* ── SCROLL REVEAL ── */
const reveals=document.querySelectorAll('.reveal');
const obs=new IntersectionObserver(entries=>{
  entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target)}});
},{threshold:0.12});
reveals.forEach(r=>obs.observe(r));
</script>
</body>
</html>
