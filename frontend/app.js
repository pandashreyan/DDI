/* ─── DDI Predict — Frontend Logic (Real Data Edition) ─────────────────────────────────
   Updated for 100% compatibility with the 191k row clinical dataset backend.
   Uses 127.0.0.1 for maximum connection reliability.
───────────────────────────────────────────────────────────────── */

const API = "/api";

/* ── State ── */
let allDrugs = [];
let selected = [];

// Clinical Case Scenarios Data
const CASE_SCENARIOS = {
  cardiac_risk: {
    drugs: ["Aspirin", "Warfarin"],
    profile: { age: 72, egfr: 55, liver: "normal", genetics: { "CYP2C19": "poor_metabolizer" } }
  },
  psyc_synergy: {
    drugs: ["Fluoxetine", "Tramadol", "Diazepam"],
    profile: { age: 34, egfr: 95, liver: "normal", genetics: { "CYP2D6": "ultra_rapid_metabolizer" } }
  },
  liver_impairment: {
    drugs: ["Atorvastatin", "Fluconazole"],
    profile: { age: 58, egfr: 70, liver: "impaired", genetics: { "SLCO1B1": "decreased_function" } }
  }
};

function loadCaseScenario(caseId) {
  const scenario = CASE_SCENARIOS[caseId];
  if (!scenario) return;

  // Clear current selection
  selected = [...scenario.drugs];
  renderSelection();

  // Set patient profile
  document.getElementById("patientAge").value = scenario.profile.age;
  document.getElementById("patientEgfr").value = scenario.profile.egfr;
  document.getElementById("patientLiver").value = scenario.profile.liver;
  
  // Update displays for sliders
  const ageVal = document.getElementById("ageValDisplay");
  if(ageVal) ageVal.textContent = scenario.profile.age + " yrs";
  const egfrVal = document.getElementById("egfrValDisplay");
  if(egfrVal) egfrVal.textContent = scenario.profile.egfr + " ml/min";

  // Set genetics
  document.querySelectorAll('#pgxContainer input').forEach(input => {
    const [variant, status] = input.value.split(':');
    input.checked = scenario.profile.genetics[variant] === status;
  });

  // Switch to analyzer tab and run prediction
  switchTab('analyzer');
  predictBtn.click();
}

/* ── DOM refs ── */
const drugListEl = document.getElementById("drugList");
const drugSearchEl = document.getElementById("drugSearch");
const selectedEl = document.getElementById("selectedDrugs");
const selectedCountEl = document.getElementById("selectedCount");
const predictBtn = document.getElementById("predictBtn");
const btnLoader = document.getElementById("btnLoader");
const resultsArea = document.getElementById("resultsArea");
const overallBadge = document.getElementById("overallBadge");
const riskValue = document.getElementById("riskValue");
const riskFill = document.getElementById("riskFill");
const pairsGrid = document.getElementById("pairsGrid");
const drugTableBody = document.getElementById("drugTableBody");
const statsGrid = document.getElementById("statsGrid");
const statusDot = document.getElementById("statusDot");
const statusText = document.getElementById("statusText");
const hDrugs = document.getElementById("hDrugs");
const hInter = document.getElementById("hInter");
const hMeta = document.getElementById("hMeta");
const molModal = document.getElementById("molModal");
const closeModal = document.getElementById("closeModal");
const modalDrugName = document.getElementById("modalDrugName");
const mol3DContainer = document.getElementById("mol3DContainer");
const regimenMatrix = document.getElementById("regimenMatrix");
const heatmapContainer = document.getElementById("heatmapContainer");
const btnExport = document.getElementById("btnExport");

let glviewer = null; // 3Dmol viewer instance

/* ══════════════════════════════════════════════
   1. API HEALTH CHECK
   Verifies if the backend is reachable
══════════════════════════════════════════════ */
async function checkHealth() {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 5000);

    const r = await fetch(`${API}/health`, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (r.ok) {
      const data = await r.json();
      console.log("✅ Health check passed:", data);
      statusDot.className = "status-dot online";
      statusText.textContent = "API Service Online";
      return true;
    }
  } catch (e) {
    console.warn("❌ Health check error:", e.message);
  }
  statusDot.className = "status-dot offline";
  statusText.textContent = "Connecting...";
  return false;
}

/* ── Tabs & Navigation ── */
function switchTab(tabId) {
  console.log("📂 Switching to tab:", tabId);
  // Update Tabs
  document.querySelectorAll(".tab-content").forEach((tab) => {
    tab.classList.remove("active");
  });
  const target = document.getElementById(`tab-${tabId}`);
  if (target) target.classList.add("active");

  // Update Sidebar
  document.querySelectorAll(".nav-menu-item").forEach((item) => {
    item.classList.remove("active");
    if (item.getAttribute("onclick") && item.getAttribute("onclick").includes(tabId)) {
      item.classList.add("active");
    }
  });

  // Handle specific tab loading
  if (tabId === "database") {
     const table = document.getElementById("databaseTabContent");
     const existingTable = document.querySelector(".table-wrap");
     if (table && existingTable && !table.contains(existingTable)) {
        table.appendChild(existingTable);
     }
  }
  
  if (tabId === "pharmacy") {
     // If analysis hasn't been run, we could show a message
  }
}

/* ══════════════════════════════════════════════
   2. LOAD DRUGS (Real Dataset)
══════════════════════════════════════════════ */
async function loadDrugs() {
  try {
    console.log("📊 Loading drugs from backend...");
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 10000);

    const r = await fetch(`${API}/drugs`, { signal: controller.signal });
    clearTimeout(timeoutId);

    if (!r.ok) {
      console.error("❌ Drugs endpoint returned:", r.status);
      throw new Error(`HTTP ${r.status}`);
    }

    const data = await r.json();
    console.log(
      "✅ Received drugs data:",
      data.drugs ? data.drugs.length : 0,
      "drugs",
    );

    allDrugs = data.drugs || [];

    if (allDrugs.length > 0) {
      console.log("✅ Drugs loaded successfully:", allDrugs.length);
      if (hDrugs) hDrugs.textContent = data.total || allDrugs.length;
      if (hMeta && data.total_metadata) hMeta.textContent = data.total_metadata;
      renderDrugList(allDrugs);
      renderDrugTable(allDrugs);
    } else {
      console.warn("⚠️ No drugs in response");
      drugListEl.innerHTML = `<div class="empty-state-small" style="color:var(--warn)">⚠️ No drugs loaded.</div>`;
    }
  } catch (e) {
    console.error("❌ Fetch Error:", e.message);
    drugListEl.innerHTML = `<div class="empty-state-small" style="color:var(--warn)">⚠️ Backend loading... (${e.message})</div>`;
  }
}

/* ══════════════════════════════════════════════
   3. RENDER DRUG LIST (Left Panel)
══════════════════════════════════════════════ */
function renderDrugList(drugs) {
  drugListEl.innerHTML = "";
  if (!drugs.length) {
    drugListEl.innerHTML = `<div class="empty-state-small">No clinical matches found</div>`;
    return;
  }

  drugs.forEach((d) => {
    const item = document.createElement("div");
    item.className =
      "drug-item" + (selected.includes(d.name) ? " selected" : "");
    item.dataset.name = d.name;
    item.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; width:100%">
        <span class="drug-name">${d.name}</span>
        <div style="display:flex; align-items:center; gap:8px">
          <span class="drug-class-badge">${d.class || "Clinical"}</span>
          <span class="info-icon" onclick="event.stopPropagation(); showIndividualSafety('${d.name}')" title="Individual Safety Profile" style="cursor:help; font-size:0.8rem; opacity:0.6">ⓘ</span>
        </div>
      </div>`;
    item.addEventListener("click", () => toggleDrug(d.name));
    drugListEl.appendChild(item);
  });
}

/* ══════════════════════════════════════════════
   4. SEARCH FILTER
══════════════════════════════════════════════ */
drugSearchEl.addEventListener("input", () => {
  const q = drugSearchEl.value.toLowerCase();
  const fil = allDrugs.filter((d) => d.name.toLowerCase().includes(q));
  renderDrugList(fil);
});

/* ══════════════════════════════════════════════
   5. SELECTION LOGIC
══════════════════════════════════════════════ */
function toggleDrug(name) {
  if (selected.includes(name)) {
    selected = selected.filter((s) => s !== name);
  } else {
    selected.push(name);
  }
  renderSelection();
  renderDrugList(
    allDrugs.filter((d) =>
      d.name.toLowerCase().includes(drugSearchEl.value.toLowerCase()),
    ),
  );
  predictBtn.disabled = selected.length < 2;
  selectedCountEl.textContent = selected.length;
}

function renderSelection() {
  if (!selected.length) {
    selectedEl.innerHTML = `<div class="empty-state-small">Select 2+ drugs to begin</div>`;
    return;
  }
  selectedEl.innerHTML = "";
  selected.forEach(async (name) => {
    const chip = document.createElement("div");
    chip.className = "selected-chip";

    // Fetch molecule SVG
    let molSvg = "";
    try {
      const res = await fetch(`${API}/molecule/${encodeURIComponent(name)}`);
      if (res.ok) {
        const molData = await res.json();
        molSvg = `<img src="${molData.svg}" class="mol-preview-sm" style="height:40px; border-radius:4px; background:rgba(255,255,255,0.05); padding:2px">`;
      }
    } catch (e) {}

    chip.innerHTML = `
      <div style="display:flex; align-items:center; gap:12px; cursor:pointer" title="View 3D Structure">
        ${molSvg}
        <div>
          <div class="drug-name">${name}</div>
          <div style="display:flex; align-items:center; gap:5px">
            <div style="font-size:.7rem;color:var(--accent1);font-weight:600">3D Ready</div>
            <div id="admet-badge-${name.replace(/\s+/g, '-')}" style="font-size:.6rem; font-weight:800; padding:1px 4px; border-radius:3px; background:rgba(255,255,255,0.05); color:var(--text-mute)">Tox: ...</div>
          </div>
        </div>
      </div>
      <button class="chip-remove" data-name="${name}" title="Remove">✕</button>`;

    // Fetch Pharmacy Price Badge
    const priceContainer = document.createElement("div");
    priceContainer.style.marginTop = "5px";
    chip.querySelector(".drug-name").parentElement.appendChild(priceContainer);
    renderPriceBadge(name, priceContainer);

    chip.querySelector(".drug-name").parentElement.onclick = () => showPharmacyPricing(name);
    
    // Fetch ADMET for badge
    fetchAdmetBadge(name);
    
    // Add Info Icon to chip
    const infoBtn = document.createElement("span");
    infoBtn.innerHTML = "ⓘ";
    infoBtn.style.cssText = "position:absolute; top:5px; right:30px; font-size:0.8rem; color:var(--accent1); cursor:help; opacity:0.6";
    infoBtn.onclick = (e) => { e.stopPropagation(); showIndividualSafety(name); };
    chip.appendChild(infoBtn);

    chip.querySelector(".chip-remove").addEventListener("click", (e) => {
      e.stopPropagation();
      toggleDrug(name);
    });
    selectedEl.appendChild(chip);
  });
}

async function renderPriceBadge(name, container) {
  try {
    const insurance = document.getElementById("patientInsurance").value || "uninsured";
    const r = await fetch(`${API}/pharmacy?drug=${encodeURIComponent(name)}&insurance=${insurance}`);
    if (r.ok) {
      const data = await r.json();
      const color = data.est_patient_copay > 100 ? "#ef4444" : data.est_patient_copay > 20 ? "#f59e0b" : "#22c55e";
      container.innerHTML = `<span style="font-size:0.65rem; color:${color}; font-weight:700; background:rgba(255,255,255,0.05); padding:2px 6px; border-radius:4px">Est. $${data.est_patient_copay}</span>`;
    }
  } catch (e) {}
}

async function fetchAdmetBadge(name) {
  try {
    const r = await fetch(`${API}/admet`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ drug: name })
    });
    if (r.ok) {
        const data = await r.json();
        const badge = document.getElementById(`admet-badge-${name.replace(/\s+/g, '-')}`);
        if (badge && data.toxicity) {
            const color = data.toxicity.level === "High" ? "#ef4444" : data.toxicity.level === "Medium" ? "#f59e0b" : "#22c55e";
            badge.style.background = `${color}22`;
            badge.style.color = color;
            badge.style.border = `1px solid ${color}44`;
            badge.textContent = `Tox: ${data.toxicity.level}`;
            badge.title = `${data.toxicity.marker}: ${(data.toxicity.score * 100).toFixed(1)}%`;
        }
    }
  } catch (e) {}
}

/* ══════════════════════════════════════════════
   6. PREDICTION CALL
══════════════════════════════════════════════ */
predictBtn.addEventListener("click", async () => {
  if (selected.length < 2) return;
  setLoading(true);

  // Collect Patient Profile Data
  const genetics = {};
  document.querySelectorAll('#pgxContainer input:checked').forEach(input => {
    const [variant, status] = input.value.split(':');
    genetics[variant] = status;
  });

  const patientProfile = {
    age: document.getElementById("patientAge").value || 40,
    egfr: document.getElementById("patientEgfr").value || 90,
    liver: document.getElementById("patientLiver").value || "normal",
    genetics: genetics,
  };

  // Collect Lifestyle Profile Data
  const lifestyleProfile = {
    alcohol: document.getElementById("lifestyleAlcohol").value || "none",
    tobacco: document.getElementById("lifestyleTobacco").checked,
    grapefruit: document.getElementById("lifestyleGrapefruit").checked,
    dairy: document.getElementById("lifestyleDairy").checked,
  };

  try {
    const r = await fetch(`${API}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        drugs: selected,
        patient_profile: patientProfile,
        lifestyle_profile: lifestyleProfile,
      }),
    });
    const data = await r.json();
    if (data.error) {
      alert("Analysis Rejected: " + data.error);
      return;
    }
    showResults(data);
  } catch (e) {
    alert("Connection Error. Is the backend server running?");
  } finally {
    setLoading(false);
  }
});

function setLoading(v) {
  predictBtn.disabled = v;
  btnLoader.className = v
    ? "btn-predict-loader spinning"
    : "btn-predict-loader";
}

/* ══════════════════════════════════════════════
   7. SHOW CLINICAL RESULTS
══════════════════════════════════════════════ */
function showResults(data) {
  resultsArea.style.display = "block";
  resultsArea.scrollIntoView({ behavior: "smooth", block: "center" });

  const sev = data.overall_severity;
  const score = data.overall_risk_score;

  overallBadge.className = `overall-badge sev-${sev}`;
  overallBadge.textContent = severityLabel(sev);
  riskValue.textContent = score.toFixed(2);
  riskValue.style.color = severityColor(sev);

  // Animate the risk gauge
  setTimeout(() => {
    riskFill.style.width = `${(score / 1.0) * 100}%`;
    riskFill.style.background = severityColor(sev);
  }, 60);

  // Individual Drug Safety Profiles (Baselines)
  const safetySection = document.getElementById("baselineSafetySection");
  const safetyTabGrid = document.getElementById("safetyTabGrid");

  if (data.drug_baselines && Object.keys(data.drug_baselines).length > 0) {
    if (safetySection) safetySection.style.display = "block";
    renderBaselineSafetyGrid(data.drug_baselines);
    
    // Also clone to the dedicated Safety Tab
    if (safetyTabGrid) {
       safetyTabGrid.innerHTML = "";
       renderBaselineSafetyGrid(data.drug_baselines, "safetyTabGrid");
       // Populate drug pills for deep-dive organ radar + PGx
       populateSafetyDrugSelector(Object.keys(data.drug_baselines));
    }
  }

  // PROACTIVE MITIGATION
  renderProactiveMitigation(data);

  // 🕸️ POLYPHARMACY GRAPH & 🕒 CHRONO TIMELINE
  renderPolypharmacyGraph(data.interactions);
  renderChronopharmacologyTimeline(data.chronopharmacology);

  // Clear and render all interaction cards
  pairsGrid.innerHTML = "";
  data.interactions.forEach(async (inter, i) => {
    const card = document.createElement("div");
    card.className = "pair-card";
    card.style.borderLeftColor = severityColor(inter.severity);
    card.style.borderLeftWidth = "4px";

    // Async molecule pair fetch
    let molRow = "";
    try {
      const [m1, m2] = await Promise.all([
        fetch(`${API}/molecule/${encodeURIComponent(inter.drug_a)}`).then((r) =>
          r.json(),
        ),
        fetch(`${API}/molecule/${encodeURIComponent(inter.drug_b)}`).then((r) =>
          r.json(),
        ),
      ]);
      if (m1.svg && m2.svg) {
        molRow = `
          <div style="display:flex; gap:10px; margin-bottom:15px; background:rgba(255,255,255,0.03); padding:10px; border-radius:8px">
            <img src="${m1.svg}" style="height:60px">
            <div style="color:var(--text-mute); align-self:center; font-weight:900">+</div>
            <img src="${m2.svg}" style="height:60px">
          </div>
        `;
      }
    } catch (e) {}

    // Importance Bars (SHAP-like)
    let impHtml = "";
    if (inter.importance) {
      impHtml = `
        <div style="margin-top:15px; border-top:1px solid rgba(255,255,255,0.05); padding-top:10px">
          <div style="font-size:0.75rem; color:var(--text-mute); margin-bottom:8px; font-weight:600">Clinical Logic Attribution</div>
          <div style="display:flex; flex-direction:column; gap:6px">
            ${Object.entries(inter.importance)
              .map(
                ([key, val]) => `
              <div style="display:flex; align-items:center; gap:10px">
                <span style="font-size:0.65rem; color:var(--text-mute); width:80px; text-transform:uppercase">${key.replace(/_/g, " ")}</span>
                <div style="flex:1; height:4px; background:rgba(255,255,255,0.1); border-radius:2px; overflow:hidden">
                  <div style="width:${Math.min(val * 100, 100)}%; height:100%; background:var(--accent1)"></div>
                </div>
                <span style="font-size:0.65rem; color:var(--accent1)">${(val * 100).toFixed(0)}%</span>
              </div>
            `,
              )
              .join("")}
          </div>
        </div>
      `;
    }

    // Clinical Decision Support (CDS)
    let cdsHtml = "";
    if (inter.cds) {
      cdsHtml = `
        <div style="margin-top:15px; background:rgba(21,128,61,0.05); border:1px solid rgba(21,128,61,0.1); padding:12px; border-radius:10px">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:5px">
             <span style="font-size:1.1rem">⚕️</span>
             <span style="font-size:0.75rem; color:var(--accent1); font-weight:800; text-transform:uppercase; letter-spacing:0.05em">Clinical Decision Support</span>
          </div>
          <p style="font-size:0.85rem; color:var(--text); line-height:1.4; margin:0">${inter.cds}</p>
        </div>
      `;
    }

    let aeHtml = "";
    if (inter.adverse_events && inter.adverse_events.length > 0) {
      aeHtml = `
        <div style="margin-top:15px; border-top:1px solid rgba(255,255,255,0.05); padding-top:10px">
          <div style="font-size:0.75rem; color:var(--text-mute); margin-bottom:8px; font-weight:600">Predicted Adverse Events (Side Effects)</div>
          <div style="display:flex; flex-direction:column; gap:8px">
            ${inter.adverse_events
              .map((ae) => {
                const pColor =
                  ae.probability > 0.5
                    ? "#ef4444"
                    : ae.probability > 0.2
                      ? "#f59e0b"
                      : "#3b82f6";
                return `
              <div style="background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); border-radius:8px; padding:10px">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px">
                  <span style="font-size:0.85rem; font-weight:700; color:var(--text)">${ae.event_name} <span style="font-size:0.7rem; color:var(--text-mute); text-transform:uppercase">(${ae.severity})</span></span>
                  <span style="font-size:0.75rem; color:${pColor}; font-weight:700">${(ae.probability * 100).toFixed(0)}% Risk</span>
                </div>
                <div style="font-size:0.75rem; color:var(--text-mute)">
                  ${ae.symptoms ? "Symptoms: " + ae.symptoms.join(", ") : ""}
                </div>
              </div>
            `;
              })
              .join("")}
          </div>
        </div>
      `;
    }

    // Personalized Patient Warnings
    let persHtml = "";
    if (inter.personalized_warnings && inter.personalized_warnings.length > 0) {
      persHtml = `
        <div style="margin-top:15px; background:rgba(239,68,68,0.05); border:1px solid rgba(239,68,68,0.1); padding:12px; border-radius:10px; border-left: 4px solid #ef4444">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:5px">
             <span style="font-size:1.1rem">👤</span>
             <span style="font-size:0.75rem; color:#ef4444; font-weight:800; text-transform:uppercase; letter-spacing:0.05em">Personalized Advisory</span>
          </div>
          <ul style="margin:0; padding-left:20px; color:var(--text); font-size:0.85rem; line-height:1.4">
            ${inter.personalized_warnings.map((w) => `<li>${w}</li>`).join("")}
          </ul>
        </div>
      `;
    }

    // Pharmacogenomics Warnings
    let pgxHtml = "";
    if (inter.pgx_warnings && inter.pgx_warnings.length > 0) {
      pgxHtml = `
        <div style="margin-top:15px; background:rgba(167,139,250,0.05); border:1px solid rgba(167,139,250,0.1); padding:12px; border-radius:10px; border-left: 4px solid var(--accent2)">
          <div style="display:flex; align-items:center; gap:8px; margin-bottom:5px">
             <span style="font-size:1.1rem">🧬</span>
             <span style="font-size:0.75rem; color:var(--accent2); font-weight:800; text-transform:uppercase; letter-spacing:0.05em">Genetic Impact (PGx)</span>
          </div>
          <ul style="margin:0; padding-left:20px; color:var(--text); font-size:0.85rem; line-height:1.4">
            ${inter.pgx_warnings.map((w) => `<li>${w}</li>`).join("")}
          </ul>
        </div>
      `;
    }

    card.innerHTML = `
      ${molRow}
      <div class="pair-header">
        <div class="pair-drugs">
          <span>${inter.drug_a}</span>
          <span class="pair-plus">+</span>
          <span>${inter.drug_b}</span>
        </div>
        <div class="pair-meta">
          <span class="pair-tag" style="border:1px solid ${severityColor(inter.severity)};color:${severityColor(inter.severity)}">${severityLabel(inter.severity)}</span>
          <span class="pair-source-badge" style="${inter.source.includes("AI") ? "background:rgba(167,139,250,0.1);color:var(--accent2);border-color:rgba(167,139,250,0.2)" : ""}">${inter.source.replace(/_/g, " ")}</span>
        </div>
        <span class="pair-score" style="color:${severityColor(inter.severity)}">${inter.risk_score.toFixed(2)}</span>
      </div>
      <p class="pair-mechanism" style="font-size:0.95rem; line-height:1.5; color:var(--text); margin-top:10px">${inter.mechanism}</p>
      ${persHtml}
      ${impHtml}
      ${cdsHtml}
      ${aeHtml}
      <div style="display:flex; gap:10px; margin-top:15px">
        <button class="btn-suggestion" style="flex:1; background:rgba(168,85,247,0.1); border:1px solid rgba(168,85,247,0.2); color:var(--accent2); padding:8px 16px; border-radius:8px; cursor:pointer; font-size:0.85rem; font-weight:600; display:${inter.severity === "severe" || inter.severity === "moderate" ? "inline-block" : "none"}; transition:all 0.3s ease">
          🔄 Find Alternatives
        </button>
        <button class="btn-optimize" style="flex:1; background:rgba(34,197,94,0.1); border:1px solid rgba(34,197,94,0.2); color:#22c55e; padding:8px 16px; border-radius:8px; cursor:pointer; font-size:0.85rem; font-weight:600; display:${inter.severity === "severe" || inter.severity === "moderate" ? "inline-block" : "none"}; transition:all 0.3s ease">
          🧬 Optimize Molecule
        </button>
      </div>
    `;
    // Add "Ask AI" button onto pair card
    const aiBtn = document.createElement("button");
    aiBtn.style.cssText = "margin-top:15px; width:100%; padding:8px; border-radius:8px; background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:var(--accent1); font-size:0.8rem; font-weight:700; cursor:pointer;";
    aiBtn.innerHTML = "🤖 Ask Medical AI";
    aiBtn.onclick = () => askAIChatbot([inter.drug_a, inter.drug_b], inter);
    card.appendChild(aiBtn);

    card.style.animationDelay = `${i * 0.1}s`;
    pairsGrid.appendChild(card);

    // Add click listener to alternatives button
    const altBtn = card.querySelector(".btn-suggestion");
    if (altBtn && (inter.severity === "severe" || inter.severity === "moderate")) {
      altBtn.onclick = () => loadAndShowAlternatives(inter.drug_a, inter.drug_b);
    }
    
    // Add click listener to optimize button
    const optBtn = card.querySelector(".btn-optimize");
    if (optBtn && (inter.severity === "severe" || inter.severity === "moderate")) {
      optBtn.onclick = () => loadAndShowOptimization(inter.drug_a);
    }
  });

  // Render Heatmap if 3+ drugs
  if (selected.length >= 3) {
    renderHeatmap(data.interactions);
  } else {
    regimenMatrix.style.display = "none";
  }

  // Auto-load alternatives for high-risk pairs
  const highRiskInteractions = data.interactions.filter(
    (i) => i.severity === "severe" || i.severity === "moderate",
  );
  if (highRiskInteractions.length > 0 && selected.length === 2) {
    const first = highRiskInteractions[0];
    loadAndShowAlternatives(first.drug_a, first.drug_b);
  } else {
    document.getElementById("alternativesPanel").style.display = "none";
  }

  // Load Live Clinical Evidence (FDA/PubMed)
  if (selected.length === 2) {
    fetchClinicalEvidence(selected[0], selected[1]);
  } else {
    document.getElementById("evidencePanel").style.display = "none";
  }

  // Render Regimen Optimization (3+ drugs)
  if (selected.length >= 3) {
    renderOptimizationTimeline(data.optimization);
  } else {
    document.getElementById("optimizationPanel").style.display = "none";
  }

  // Render Lifestyle Warnings
  renderLifestyleWarnings(data.lifestyle_warnings);
}

/* ══════════════════════════════════════════════
   10. LIFESTYLE HABITS RENDERING
   ══════════════════════════════════════════════ */
function renderLifestyleWarnings(warnings) {
  const container = document.getElementById("lifestyleWarningsContainer");
  if (!container) return;

  if (!warnings || warnings.length === 0) {
    container.innerHTML = "";
    return;
  }

  let html = `
    <div style="margin-top:20px; background:rgba(245,158,11,0.05); border:1px solid rgba(245,158,11,0.1); padding:20px; border-radius:16px">
      <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px">
        <span style="font-size:1.3rem">🍎</span>
        <h4 style="margin:0; font-weight:800; color:#f59e0b; text-transform:uppercase; letter-spacing:0.05em">Dietary & Lifestyle Alerts</h4>
      </div>
      <div style="display:grid; grid-template-columns: 1fr; gap:10px">
  `;

  warnings.forEach((w) => {
    const color =
      w.severity === "severe"
        ? "#ef4444"
        : w.severity === "high"
          ? "#f59e0b"
          : "#3b82f6";
    html += `
      <div style="background:rgba(255,255,255,0.02); border-left:4px solid ${color}; padding:12px; border-radius:8px">
        <div style="font-size:0.7rem; color:${color}; font-weight:800; text-transform:uppercase; margin-bottom:4px">${w.factor} Interaction</div>
        <div style="font-size:0.85rem; color:var(--text); line-height:1.4">${w.msg}</div>
      </div>
    `;
  });

  html += `</div></div>`;
  container.innerHTML = html;
}

/* ══════════════════════════════════════════════
   11. VOICE ANALYSIS (WEB SPEECH API)
   ══════════════════════════════════════════════ */
function initVoiceRecognition() {
  const voiceBtn = document.getElementById("voiceBtn");
  const SpeechRecognition =
    window.SpeechRecognition || window.webkitSpeechRecognition;

  if (!SpeechRecognition) {
    voiceBtn.style.display = "none";
    return;
  }

  const recognition = new SpeechRecognition();
  recognition.continuous = false;
  recognition.lang = "en-US";
  recognition.interimResults = false;

  voiceBtn.onclick = () => {
    try {
      recognition.start();
      voiceBtn.style.color = "#ef4444";
      voiceBtn.textContent = "⏺️";
    } catch (e) {
      recognition.stop();
    }
  };

  recognition.onresult = (event) => {
    const text = event.results[0][0].transcript.toLowerCase();
    voiceBtn.style.color = "var(--accent1)";
    voiceBtn.textContent = "🎙️";
    handleVoiceCommand(text);
  };

  recognition.onend = () => {
    voiceBtn.style.color = "var(--accent1)";
    voiceBtn.textContent = "🎙️";
  };

  recognition.onerror = () => {
    voiceBtn.style.color = "var(--accent1)";
    voiceBtn.textContent = "🎙️";
  };
}

function handleVoiceCommand(cmd) {
  console.log("Voice Command:", cmd);
  if (cmd.includes("add")) {
    const drugName = cmd.split("add")[1].trim().toLowerCase();
    if (drugName) {
      drugSearchEl.value = drugName;
      drugSearchEl.dispatchEvent(new Event("input"));
      // Auto-toggle if unique
      setTimeout(() => {
        const matches = allDrugs.filter(
          (d) => d.name.toLowerCase() === drugName,
        );
        if (matches.length === 1) toggleDrug(matches[0].name);
      }, 500);
    }
  } else if (cmd.includes("analyze") || cmd.includes("predict")) {
    predictBtn.click();
  } else if (cmd.includes("clear")) {
    selected = [];
    renderSelection();
    renderDrugList(allDrugs);
  }
}

/* ══════════════════════════════════════════════
   9. REGIMEN OPTIMIZATION & TIMELINE
   ══════════════════════════════════════════════ */
function renderOptimizationTimeline(opt) {
  const panel = document.getElementById("optimizationPanel");
  const grid = document.getElementById("timelineGrid");
  const adviceList = document.getElementById("optimizationAdvice");
  const synergyList = document.getElementById("synergyList");
  const scoreBadge = document.getElementById("regimenScoreBadge");

  if (!opt) {
    panel.style.display = "none";
    return;
  }

  panel.style.display = "block";
  scoreBadge.textContent = `REGIMEN RISK: ${opt.regimen_score.toFixed(2)}`;
  scoreBadge.style.color = opt.regimen_score > 0.5 ? "#ef4444" : "#a78bfa";

  // 1. Clear previous rows (except headers)
  const headers = Array.from(grid.children).slice(0, 5);
  grid.innerHTML = "";
  headers.forEach((h) => grid.appendChild(h));

  // 2. Render Rows
  const allDrugsInOpt = new Set();
  Object.values(opt.schedule).forEach((list) =>
    list.forEach((d) => allDrugsInOpt.add(d)),
  );

  allDrugsInOpt.forEach((drug) => {
    // Drug Title Cell
    const titleCell = document.createElement("div");
    titleCell.style.cssText =
      "background:rgba(255,255,255,0.02); padding:12px; font-size:0.75rem; font-weight:700; color:var(--text); display:flex; align-items:center; border-top:1px solid rgba(255,255,255,0.05)";
    titleCell.textContent = drug.toUpperCase();
    grid.appendChild(titleCell);

    // Slots
    ["morning", "noon", "evening", "night"].forEach((slot) => {
      const slotCell = document.createElement("div");
      slotCell.style.cssText =
        "background:rgba(255,255,255,0.01); display:flex; justify-content:center; align-items:center; border-top:1px solid rgba(255,255,255,0.05); border-left:1px solid rgba(255,255,255,0.05)";

      if (opt.schedule[slot].includes(drug)) {
        slotCell.innerHTML = `<div style="width:14px; height:14px; background:#a78bfa; border-radius:50%; box-shadow:0 0 10px rgba(167,139,250,0.5)"></div>`;
      }
      grid.appendChild(slotCell);
    });
  });

  // 3. Render Advice
  adviceList.innerHTML = `<h4 style="margin:0 0 5px; font-size:0.75rem; text-transform:uppercase; color:var(--text-mute); letter-spacing:0.05em">Intake Instructions</h4>`;
  if (opt.advice && opt.advice.length > 0) {
    opt.advice.forEach((msg) => {
      const item = document.createElement("div");
      item.style.cssText =
        "font-size:0.8rem; color:var(--text); padding:8px; background:rgba(255,255,255,0.02); border-radius:6px; border-left:3px solid var(--accent1)";
      item.textContent = msg;
      adviceList.appendChild(item);
    });
  } else {
    adviceList.innerHTML += `<div style="color:var(--text-mute); font-size:0.8rem">No special timing requirements detected.</div>`;
  }

  // 4. Render Synergies
  synergyList.innerHTML = `<h4 style="margin:0 0 5px; font-size:0.75rem; text-transform:uppercase; color:var(--text-mute); letter-spacing:0.05em">Cumulative Synergies</h4>`;
  if (opt.synergies && opt.synergies.length > 0) {
    opt.synergies.forEach((syn) => {
      const item = document.createElement("div");
      const color = syn.severity === "high" ? "#ef4444" : "#f59e0b";
      item.style.cssText = `font-size:0.8rem; color:var(--text); padding:8px; background:rgba(255,255,255,0.02); border-radius:6px; border-left:3px solid ${color}`;
      item.innerHTML = `<strong style="color:${color}">${syn.type}:</strong> ${syn.msg}`;
      synergyList.appendChild(item);
    });
  } else {
    synergyList.innerHTML += `<div style="color:var(--text-mute); font-size:0.8rem">No cumulative synergistic risks found for this combination.</div>`;
  }
}

/* ══════════════════════════════════════════════
   7.5 LIVE CLINICAL EVIDENCE (FDA/PUBMED)
   ══════════════════════════════════════════════ */
async function fetchClinicalEvidence(drugA, drugB) {
  const panel = document.getElementById("evidencePanel");
  const fdaContent = document.getElementById("fdaContent");
  const pubmedContent = document.getElementById("pubmedContent");

  panel.style.display = "block";
  fdaContent.innerHTML = `<div style="color:var(--text-mute)">Checking FDA label database...</div>`;
  pubmedContent.innerHTML = `<div style="color:var(--text-mute)">Searching PubMed clinical trials...</div>`;

  try {
    const res = await fetch(`${API}/clinical-evidence`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ drug_a: drugA, drug_b: drugB }),
    });

    const data = await res.json();
    if (data.error) throw new Error(data.error);

    // 1. Render FDA Warnings
    let fdaHtml = "";
    if (data.drug_a_warning) {
      fdaHtml += `<div style="margin-bottom:10px"><strong>${drugA.toUpperCase()}:</strong><br>${data.drug_a_warning}</div>`;
    }
    if (data.drug_b_warning) {
      fdaHtml += `<div><strong>${drugB.toUpperCase()}:</strong><br>${data.drug_b_warning}</div>`;
    }
    fdaContent.innerHTML =
      fdaHtml || "No boxed warnings found for these specific agents.";

    // 2. Render PubMed Trials
    if (data.pubmed_trials && data.pubmed_trials.length > 0) {
      pubmedContent.innerHTML = data.pubmed_trials
        .map(
          (trial) => `
        <div class="trial-item" style="padding:10px; border-radius:8px; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.05)">
          <div style="font-size:0.85rem; font-weight:700; color:var(--text); margin-bottom:4px">${trial.title}</div>
          <div style="display:flex; justify-content:space-between; align-items:center; font-size:0.75rem; color:var(--text-mute)">
            <span>${trial.source} (${trial.pubdate})</span>
            <a href="${trial.url}" target="_blank" style="color:var(--accent1); text-decoration:none; font-weight:600">View Paper ↗</a>
          </div>
        </div>
      `,
        )
        .join("");
    } else {
      pubmedContent.innerHTML = `<div style="color:var(--text-mute); font-size:0.85rem">No recent clinical trials found for this specific interaction in PubMed.</div>`;
    }

    // 3. Render Regulatory Badges
    const regBadges = document.getElementById("regBadges");
    if (data.regulatory_sync && regBadges) {
      regBadges.innerHTML = `
        <span class="reg-badge" title="Food and Drug Administration (USA)" style="background:rgba(34,197,94,0.1); color:#22c55e; padding:2px 8px; border-radius:4px; font-size:0.7rem; font-weight:700; border:1px solid rgba(34,197,94,0.2)">FDA ${data.regulatory_sync.fda.toUpperCase()}</span>
        <span class="reg-badge" title="European Medicines Agency (EU)" style="background:rgba(59,130,246,0.1); color:#3b82f6; padding:2px 8px; border-radius:4px; font-size:0.7rem; font-weight:700; border:1px solid rgba(59,130,246,0.2)">EMA ${data.regulatory_sync.ema.split(" ")[0].toUpperCase()}</span>
      `;
    }
  } catch (e) {
    console.error("Evidence Fetch Error:", e);
    fdaContent.innerHTML = `<div style="color:var(--warn)">Failed to connect to clinical evidence service.</div>`;
    pubmedContent.innerHTML = "";
  }
}

/* ══════════════════════════════════════════════
   8. DRUG REPLACEMENT ENGINE - Smart Alternatives
   ══════════════════════════════════════════════ */

async function loadAndShowAlternatives(drugA, drugB) {
  // Fetch alternative drugs with lower interaction risk
  const altPanel = document.getElementById("alternativesPanel");
  const altGrid = document.getElementById("alternativesGrid");

  altPanel.style.display = "block";
  altGrid.innerHTML = `<div style="grid-column:1/-1; padding:30px; text-align:center; color:var(--text-mute)">🔄 Finding safer alternatives...</div>`;

  try {
    const res = await fetch(`${API}/drug-alternatives`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        drug_a: drugA,
        drug_b: drugB,
        alternatives_for: "drug_a",
        count: 5,
      }),
    });

    const data = await res.json();
    if (data.error) {
      altGrid.innerHTML = `<div style="grid-column:1/-1; padding:20px; color:var(--sev-severe)">⚠️ ${data.error}</div>`;
      return;
    }

    if (!data.suggestions || data.suggestions.length === 0) {
      altGrid.innerHTML = `<div style="grid-column:1/-1; padding:20px; color:var(--text-mute)">No alternatives found in this therapeutic class.</div>`;
      return;
    }

    altGrid.innerHTML = "";
    data.suggestions.forEach((alt, idx) => {
      const riskColor =
        alt.risk_level === "low"
          ? "#22c55e"
          : alt.risk_level === "moderate"
            ? "#f59e0b"
            : "#ef4444";
      const riskBg =
        alt.risk_level === "low"
          ? "rgba(34,197,94,0.1)"
          : alt.risk_level === "moderate"
            ? "rgba(245,158,11,0.1)"
            : "rgba(239,68,68,0.1)";

      const altCard = document.createElement("div");
      altCard.className = "alt-card"; // Using a class for easier styling if needed
      altCard.style.cssText = `
        padding:16px; border-radius:12px; background:rgba(255,255,255,0.02); 
        border:1px solid rgba(255,255,255,0.05); cursor:pointer;
        transition:all 0.3s ease; position:relative; overflow:hidden;
      `;

      // Price Placeholder
      const priceId = `price-alt-${idx}`;
      
      altCard.onmouseover = () => {
        altCard.style.borderColor = riskColor;
        altCard.style.background = riskBg;
        altCard.style.transform = "translateY(-2px)";
      };
      altCard.onmouseout = () => {
        altCard.style.borderColor = "rgba(255,255,255,0.05)";
        altCard.style.background = "rgba(255,255,255,0.02)";
        altCard.style.transform = "translateY(0)";
      };

      const riskEmoji = alt.risk_level === "low" ? "✅" : alt.risk_level === "moderate" ? "⚠️" : "❌";
      const savingsPercent = Math.round((1 - alt.interaction_risk) * 100);

      altCard.innerHTML = `
        <div style="display:flex; justify-content:space-between; align-items:start; margin-bottom:10px">
          <div>
            <h4 style="margin:0; color:var(--text); font-size:1rem; font-weight:700; text-transform:capitalize">${alt.name}</h4>
            <div id="${priceId}" style="font-size:0.7rem; margin-top:2px"></div>
          </div>
          <span style="font-size:1.2rem">${riskEmoji}</span>
        </div>
        <div style="display:grid; gap:8px; font-size:0.85rem; margin-bottom:12px">
          <div><span style="color:var(--text-mute)">Class:</span> <span style="color:var(--accent1); font-weight:600">${alt.class}</span></div>
          <div style="display:flex; align-items:center; gap:10px">
            <span style="color:var(--text-mute); width:70px">Safety Profile:</span>
            <div style="flex:1; height:6px; background:rgba(255,255,255,0.05); border-radius:3px; overflow:hidden">
              <div style="width:${savingsPercent}%; height:100%; background:linear-gradient(90deg, ${riskColor}, var(--success))"></div>
            </div>
            <span style="color:${riskColor}; font-weight:800">${savingsPercent}%</span>
          </div>
          ${alt.safety_profile ? `
          <div style="margin-top:5px">
            <div style="font-size:0.65rem; color:var(--text-mute); margin-bottom:4px; text-transform:uppercase">Common Side Effects</div>
            <div style="display:flex; flex-wrap:wrap; gap:4px">
              ${alt.safety_profile.common.slice(0, 3).map(eff => `<span style="font-size:0.6rem; background:rgba(255,255,255,0.05); padding:2px 6px; border-radius:4px; color:var(--text-dim)">${eff}</span>`).join('')}
            </div>
          </div>
          ` : ''}
        </div>
        <div style="border-top:1px solid rgba(255,255,255,0.05); padding-top:10px; margin-top:10px; font-size:0.75rem; color:var(--text-mute); display:flex; justify-content:space-between">
          <span style="color:var(--success); font-weight:700">Recommended Alternative</span>
          <div style="display:flex; gap:10px">
            <span style="color:var(--accent1); font-weight:700; cursor:help" onclick="event.stopPropagation(); showIndividualSafety('${alt.name}')">Safety Info ⚕️</span>
            <span style="color:var(--accent2); font-weight:700; cursor:help" onclick="event.stopPropagation(); showPharmacyPricing('${alt.name}')">Price IQ 🏛️</span>
          </div>
        </div>
      `;
      
      // Async Price Fetch for Alternative
      renderPriceBadge(alt.name, altCard.querySelector(`#${priceId}`));

      altCard.onclick = () => {
        // Replace drug A with alternative and re-run prediction
        const newSelected = selected.slice();
        newSelected[newSelected.indexOf(drugA)] = alt.name;
        selected = newSelected;
        renderSelection();
        predictBtn.click();
      };

      altGrid.appendChild(altCard);
    });
  } catch (e) {
    console.error("Alternatives fetch error:", e);
    altGrid.innerHTML = `<div style="grid-column:1/-1; padding:20px; color:var(--sev-severe)">Connection error loading alternatives</div>`;
  }
}

/* ══════════════════════════════════════════════
   6. ADVANCED CLINICAL FEATURES (3D, HEATMAP, PDF)
   ══════════════════════════════════════════════ */

async function open3DViewer(name) {
  molModal.style.display = "flex";
  modalDrugName.textContent = `${name.toUpperCase()} (3D Structure)`;
  mol3DContainer.innerHTML = `<div style="display:flex; align-items:center; justify-content:center; height:100%; color:var(--accent1)">Generating 3D Coordinates...</div>`;

  try {
    const res = await fetch(`${API}/molecule/3d/${encodeURIComponent(name)}`);
    const data = await res.json();
    if (data.sdf) {
      mol3DContainer.innerHTML = "";
      glviewer = $3Dmol.createViewer(mol3DContainer, {
        backgroundColor: "#050505",
      });
      glviewer.addModel(data.sdf, "sdf");
      glviewer.setStyle(
        {},
        { stick: { radius: 0.15 }, sphere: { scale: 0.3 } },
      );
      glviewer.zoomTo();
      glviewer.render();
      glviewer.animate({ loop: "forward", interval: 100 });
    } else {
      mol3DContainer.innerHTML = `<div style="padding:40px; color:var(--sev-severe)">3D Data Unavailable for ${name}</div>`;
    }
  } catch (e) {
    mol3DContainer.innerHTML = `<div style="padding:40px; color:var(--sev-severe)">Connection Error</div>`;
  }
}

closeModal.onclick = () => {
  molModal.style.display = "none";
  if (glviewer) glviewer.clear();
};

function renderHeatmap(interactions) {
  regimenMatrix.style.display = "block";
  const drugs = selected;
  const size = drugs.length;

  let html = `<table class="heatmap"><thead><tr><th></th>`;
  drugs.forEach((d) => (html += `<th>${d}</th>`));
  html += `</tr></thead><tbody>`;

  drugs.forEach((d1) => {
    html += `<tr><th>${d1}</th>`;
    drugs.forEach((d2) => {
      if (d1 === d2) {
        html += `<td style="background:rgba(255,255,255,0.05)">-</td>`;
      } else {
        const match = interactions.find(
          (it) =>
            (it.drug_a === d1 && it.drug_b === d2) ||
            (it.drug_a === d2 && it.drug_b === d1),
        );
        const color = match ? severityColor(match.severity) : "transparent";
        const score = match ? match.risk_score.toFixed(1) : "0.0";
        const pulseClass = match && match.risk_score > 0.8 ? "risk-pulse" : "";
        html += `<td style="background:${color}33; color:${color}; border:1px solid ${color}44; font-weight:800" class="${pulseClass}">${score}</td>`;
      }
    });
    html += `</tr>`;
  });

  html += `</tbody></table>`;
  heatmapContainer.innerHTML = html;
}

btnExport.onclick = () => {
  const { jsPDF } = window.jspdf;
  const doc = new jsPDF("p", "mm", "a4");

  html2canvas(document.body).then((canvas) => {
    const imgData = canvas.toDataURL("image/png");
    const imgProps = doc.getImageProperties(imgData);
    const pdfWidth = doc.internal.pageSize.getWidth();
    const pdfHeight = (imgProps.height * pdfWidth) / imgProps.width;
    doc.addImage(imgData, "PNG", 0, 0, pdfWidth, pdfHeight);
    doc.save(`DDI_Report_${new Date().getTime()}.pdf`);
  });
};

/* ══════════════════════════════════════════════
   8. DRUG CATALOG TABLE
══════════════════════════════════════════════ */
function renderDrugTable(drugs) {
  drugTableBody.innerHTML = "";
  drugs.forEach((d) => {
    const tr = document.createElement("tr");
    const cyps =
      (d.cyp || []).map((c) => `<span class="cyp-tag">${c}</span>`).join("") ||
      '<span style="color:var(--text-mute)">—</span>';
    tr.innerHTML = `
      <td><strong style="text-transform:capitalize">${d.name}</strong></td>
      <td><span class="class-pill">${d.class || "General"}</span></td>
      <td>${cyps}</td>
      <td><span class="status-badge" style="background:rgba(34,197,94,0.1); color:var(--success); border:1px solid rgba(34,197,94,0.2); font-size:0.7rem; padding:2px 6px; border-radius:4px">Ready</span></td>
      <td class="mw-val">${d.mw ? d.mw.toFixed(1) : "—"}</td>
      <td class="mw-val">${d.logp ? d.logp.toFixed(2) : "—"}</td>`;
    drugTableBody.appendChild(tr);
  });
}

/* ══════════════════════════════════════════════
   9. SYSTEM STATISTICS
══════════════════════════════════════════════ */
async function loadStats() {
  try {
    const r = await fetch(`${API}/stats`);
    const data = await r.json();

    if (hInter)
      hInter.textContent = data.total_interactions_loaded.toLocaleString();

    statsGrid.innerHTML = `
      <div class="stat-card">
        <div class="stat-icon">💊</div>
        <div class="stat-val">${data.total_interactions_loaded.toLocaleString()}</div>
        <div class="stat-lbl">Pairs in Knowledge Base</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">📚</div>
        <div class="stat-val" style="font-size:1rem">${data.source}</div>
        <div class="stat-lbl">Primary Source</div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">⚙️</div>
        <div class="stat-val" style="font-size:1rem">${data.engine}</div>
        <div class="stat-lbl">Inference Engine</div>
      </div>
       <div class="stat-card" style="border-right: none">
        <div class="stat-icon">🛡️</div>
        <div class="stat-val" style="font-size:1.1rem; color:var(--safe)">${data.status}</div>
        <div class="stat-lbl">Server Status</div>
      </div>`;
  } catch (e) {
    statsGrid.innerHTML = `<div style="color:var(--warn);grid-column:1/-1;text-align:center">⚠️ Connection to backend failed. Stats offline.</div>`;
  }
}

/* ══════════════════════════════════════════════
   10. HELPERS
══════════════════════════════════════════════ */
function severityLabel(sev) {
  return (
    {
      none: "✅ Normal",
      mild: "⚡ Minor",
      moderate: "⚠️ Warning",
      severe: "🚨 CRITICAL",
    }[sev] || sev
  );
}
function severityColor(sev) {
  return (
    {
      none: "#10b981",
      mild: "#3b82f6",
      moderate: "#f59e0b",
      severe: "#ef4444",
    }[sev] || "#fff"
  );
}

/* ══════════════════════════════════════════════
   11. INITIALIZATION
══════════════════════════════════════════════ */
console.log("🚀 DDI Predict initializing...");

// Start loading data immediately (don't wait for health check)
(async () => {
  console.log("📋 Step 1: Loading initial data...");

  // Load drugs and stats in parallel
  const drugPromise = loadDrugs();
  const statsPromise = loadStats();

  try {
    await Promise.all([drugPromise, statsPromise]);
    console.log("✅ Initial data loaded");
  } catch (e) {
    console.error("⚠️ Error loading initial data:", e);
  }

  // Check health status
  console.log("❤️ Step 2: Checking backend health...");
  await checkHealth();

  // Keep checking health and reloading if needed
  setInterval(async () => {
    const isHealthy = await checkHealth();
    if (isHealthy && allDrugs.length === 0) {
      console.log("🔄 Connection restored, reloading data...");
      await Promise.all([loadDrugs(), loadStats()]);
    }
  }, 3000);

  // eGFR Input Listener
  const egfrIn = document.getElementById("patientEgfr");
  const egfrVal = document.getElementById("egfrValDisplay");
  if (egfrIn && egfrVal) {
    egfrIn.oninput = () => {
      egfrVal.textContent = `${egfrIn.value} ml/min`;
      const color =
        egfrIn.value < 30 ? "#ef4444" : egfrIn.value < 60 ? "#f59e0b" : "#22c55e";
      egfrVal.style.color = color;
    };
  }

  // Initialize Voice
  initVoiceRecognition();
})();

/* ══════════════════════════════════════════════
   12. PHARMACY & INSURANCE LOGIC
   ══════════════════════════════════════════════ */
async function showPharmacyPricing(drugName) {
  const modal = document.getElementById("pricingModal");
  const nameEl = document.getElementById("pricingDrugName");
  const tierEl = document.getElementById("modalDrugTier");
  const contentEl = document.getElementById("modalPricingContent");
  const savingsEl = document.getElementById("modalSavingsAlert");
  const insurance = document.getElementById("patientInsurance") ? document.getElementById("patientInsurance").value : "uninsured";

  nameEl.textContent = drugName.toUpperCase();
  tierEl.textContent = "Loading pharmacy data...";
  contentEl.innerHTML = `<div class="spinning" style="margin:20px auto; width:30px; height:30px; border:3px solid rgba(255,255,255,0.1); border-top-color:var(--accent2); border-radius:50%"></div>`;
  modal.style.display = "flex";

  try {
    const r = await fetch(`${API}/pharmacy?drug=${encodeURIComponent(drugName)}&insurance=${insurance}`);
    const data = await r.json();

    tierEl.textContent = data.tier;
    savingsEl.textContent = data.savings_alert || "No specific generic savings found for this agent.";
    
    let html = `
      <div style="background:rgba(255,255,255,0.03); padding:15px; border-radius:12px; margin-bottom:15px; border:1px solid rgba(255,255,255,0.05)">
        <div style="display:flex; justify-content:space-between; align-items:center">
          <span style="color:var(--text-mute); font-size:0.8rem">Estimated ${data.insurance_plan} Copay</span>
          <span style="font-size:1.5rem; font-weight:800; color:var(--accent2)">$${data.est_patient_copay}</span>
        </div>
        <div style="font-size:0.7rem; color:var(--text-mute); text-align:right; margin-top:4px">Retail Avg: $${data.retail_avg}</div>
      </div>
      <table style="width:100%; border-collapse:collapse; font-size:0.85rem">
        <thead>
          <tr style="border-bottom:1px solid rgba(255,255,255,0.05); color:var(--text-mute)">
            <th style="text-align:left; padding:10px 5px">Pharmacy</th>
            <th style="text-align:right; padding:10px 5px">Local Price</th>
            <th style="text-align:right; padding:10px 5px">Status</th>
          </tr>
        </thead>
        <tbody>
    `;

    data.pharmacy_rows.forEach(row => {
      html += `
        <tr style="border-bottom:1px solid rgba(255,255,255,0.02)">
          <td style="padding:12px 5px; font-weight:600">${row.pharmacy}</td>
          <td style="padding:12px 5px; text-align:right; color:var(--accent1)">$${row.discount_price}</td>
          <td style="padding:12px 5px; text-align:right; font-size:0.7rem; color:${row.availability === 'In Stock' ? '#22c55e' : '#f59e0b'}">${row.availability}</td>
        </tr>
      `;
    });

    html += `</tbody></table>`;
    contentEl.innerHTML = html;
  } catch (e) {
    contentEl.innerHTML = `<p style="color:#ef4444">Error loading pharmacy data. Please check connectivity.</p>`;
  }
}

async function showIndividualSafety(drugName) {
  const modal = document.getElementById("safetyModal");
  const nameEl = document.getElementById("safetyDrugName");
  const classEl = document.getElementById("safetyDrugClass");
  const commonEl = document.getElementById("safetyCommonList");
  const seriousEl = document.getElementById("safetySeriousList");
  const managementEl = document.getElementById("safetyManagement");

  nameEl.textContent = drugName.toUpperCase();
  classEl.textContent = "Fetching clinical data...";
  commonEl.innerHTML = "";
  seriousEl.innerHTML = "";
  managementEl.textContent = "";
  modal.style.display = "flex";

  try {
    const r = await fetch(`${API}/drug-safety?drug=${encodeURIComponent(drugName)}`);
    const data = await r.json();

    classEl.textContent = data.class;
    
    data.common.forEach(eff => {
      const tag = document.createElement("span");
      tag.style.cssText = "background:rgba(255,255,255,0.05); color:var(--text); padding:4px 10px; border-radius:30px; font-size:0.75rem; border:1px solid rgba(255,255,255,0.1)";
      tag.textContent = eff;
      commonEl.appendChild(tag);
    });

    data.serious.forEach(eff => {
      const item = document.createElement("div");
      item.style.cssText = "background:rgba(239,68,68,0.05); border-left:3px solid #ef4444; padding:8px 12px; border-radius:6px; font-size:0.8rem; color:var(--text)";
      item.innerHTML = `<strong style="color:#ef4444">Warning:</strong> ${eff}`;
      seriousEl.appendChild(item);
    });

    managementEl.textContent = data.management;

    // Fetch ADMET for detailed view
    const admetR = await fetch(`${API}/admet`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ drug: drugName })
    });
    if (admetR.ok) {
        const admetData = await admetR.json();
        if (admetData.toxicity) {
            const admetSec = document.getElementById('modalAdmetSection');
            const admetBadge = document.getElementById('modalAdmetBadge');
            const admetContent = document.getElementById('modalAdmetContent');
            if (admetSec && admetContent) {
                const color = admetData.toxicity.level === 'High' ? '#ef4444' : admetData.toxicity.level === 'Medium' ? '#f59e0b' : '#22c55e';
                admetBadge.style.cssText = `background:${color}22; color:${color}; padding:2px 8px; border-radius:10px;`;
                admetBadge.textContent = `${admetData.toxicity.level} RISK`;
                admetContent.innerHTML = `<strong>${admetData.toxicity.marker}</strong>: Score ${admetData.toxicity.score.toFixed(3)}`;
                admetSec.style.display = 'block';
            } else {
                // Fallback for old DOM (append to management el)
                const toxEl = document.createElement('div');
                const color = admetData.toxicity.level === 'High' ? '#ef4444' : admetData.toxicity.level === 'Medium' ? '#f59e0b' : '#22c55e';
                toxEl.style.cssText = `margin-top:15px; background:${color}11; border:1px solid ${color}33; padding:12px; border-radius:10px`;
                toxEl.innerHTML = `
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:5px">
                        <span style="font-size:0.75rem; color:${color}; font-weight:800; text-transform:uppercase">Molecular Toxicity Assessment (AI)</span>
                        <span style="font-size:0.75rem; color:${color}; font-weight:900">${admetData.toxicity.level} RISK</span>
                    </div>
                    <div style="font-size:0.85rem; color:var(--text); line-height:1.4">
                        <strong>${admetData.toxicity.marker}</strong>: Score: ${admetData.toxicity.score.toFixed(3)}.
                    </div>
                `;
                managementEl.parentElement.appendChild(toxEl);
            }
        }
    }

    // Load multi-organ radar + PGx into modal (async, non-blocking)
    enrichSafetyModal(drugName);

  } catch (e) {
    classEl.textContent = "Error loading data";
  }
}

function renderBaselineSafetyGrid(baselines, containerId = "baselineSafetyGrid") {
  const container = document.getElementById(containerId);
  if (!container) return;
  container.innerHTML = "";

  Object.entries(baselines).forEach(([name, data]) => {
    const card = document.createElement("div");
    card.className = "glass-panel";
    card.style.cssText = "padding:20px; border-radius:12px; background:rgba(255,255,255,0.01); border:1px solid rgba(255,255,255,0.05); position:relative;";
    
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px">
        <strong style="text-transform:capitalize; color:var(--accent1)">${name}</strong>
        <span style="font-size:0.65rem; color:var(--accent2); font-weight:800; letter-spacing:0.05em">${data.class}</span>
      </div>
      <div style="font-size:0.75rem; color:var(--text-mute); margin-bottom:10px">Clinical Profile:</div>
      <div style="display:flex; flex-wrap:wrap; gap:5px; margin-bottom:20px">
        ${data.common.slice(0,4).map(eff => `<span style="background:rgba(100,112,255,0.1); padding:3px 8px; border-radius:6px; font-size:0.7rem; color:var(--text)">${eff}</span>`).join('')}
      </div>
      <button onclick="showIndividualSafety('${name}')" style="width:100%; padding:10px; border-radius:8px; background:rgba(167,139,250,0.15); border:1px solid rgba(167,139,250,0.3); color:#fff; font-size:0.8rem; font-weight:700; cursor:pointer; transition:all 0.2s;">Full Risk Analysis</button>
    `;
    container.appendChild(card);
  });
}

function renderProactiveMitigation(data) {
  const container = document.getElementById("riskMitigationContainer");
  if (!container) return;
  container.innerHTML = "";

  const highRisk = data.interactions.find(i => i.severity === 'severe' || i.severity === 'moderate');
  if (!highRisk) return;

  const bar = document.createElement("div");
  bar.className = "mitigation-bar";
  bar.innerHTML = `
    <div style="display:flex; align-items:center; gap:15px">
       <div style="width:40px; height:40px; background:var(--danger); border-radius:50%; display:flex; align-items:center; justify-content:center; font-size:1.2rem; animation: pulse 2s infinite">⚠️</div>
       <div>
          <div style="font-weight:800; font-size:0.95rem; color:#fff">Action Recommended: Elevated Risk Detected</div>
          <div style="font-size:0.8rem; color:rgba(255,255,255,0.7)">Significant interaction between <strong>${highRisk.drug_a}</strong> and <strong>${highRisk.drug_b}</strong></div>
       </div>
    </div>
    <div style="display:flex; gap:10px;">
       <button onclick="switchTab('analyzer'); document.getElementById('alternativesPanel').scrollIntoView();" style="background:#fff; color:var(--bg); border:none; padding:8px 16px; border-radius:8px; font-weight:700; font-size:0.8rem; cursor:pointer">View Alternatives</button>
       <button onclick="this.parentElement.parentElement.remove()" style="background:rgba(255,255,255,0.1); border:none; color:#fff; width:34px; height:34px; border-radius:50%; cursor:pointer">✕</button>
    </div>
  `;
  container.appendChild(bar);
}

async function loadAndShowOptimization(drugName) {
  const panel = document.getElementById("optimizationPanel");
  const resultsGrid = document.getElementById("optimizationResults");
  
  panel.style.display = "block";
  resultsGrid.innerHTML = `<div style="text-align:center; padding:40px; color:var(--text-mute)">🤖 Generative AI is calculating bioisosteric derivatives...</div>`;
  panel.scrollIntoView({ behavior: "smooth", block: "center" });

  try {
    const r = await fetch(`${API}/optimize-molecule`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ drug: drugName })
    });
    const data = await r.json();
    
    if (!data.optimized_derivatives || data.optimized_derivatives.length === 0) {
        resultsGrid.innerHTML = `<div style="color:#ef4444; padding:20px">No safer derivatives found for this structural scaffold.</div>`;
        return;
    }

    resultsGrid.innerHTML = "";
    data.optimized_derivatives.forEach(der => {
        const item = document.createElement("div");
        item.style.cssText = "background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.05); padding:20px; border-radius:16px; display:grid; grid-template-columns: 200px 1fr; gap:25px; align-items:center";
        
        item.innerHTML = `
            <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:12px; height:200px; display:flex; align-items:center; justify-content:center">
                <img src="${der.svg}" style="max-width:100%; max-height:100%">
            </div>
            <div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px">
                    <h4 style="margin:0; color:#22c55e; font-size:1.1rem">${der.name}</h4>
                    <div style="background:rgba(34,197,94,0.1); color:#22c55e; padding:4px 10px; border-radius:20px; font-size:0.8rem; font-weight:800">
                        +${der.safety.improvement_score}% Safety Gain
                    </div>
                </div>
                <p style="font-size:0.9rem; color:var(--text); line-height:1.5; margin-bottom:15px">${der.description}</p>
                <div style="display:grid; grid-template-columns:repeat(4,1fr); gap:10px; background:rgba(0,0,0,0.2); padding:10px; border-radius:8px">
                    <div style="text-align:center"><div style="font-size:0.6rem; color:var(--text-mute)">MW</div><div style="font-size:0.8rem; font-weight:700">${der.metrics.mw}</div></div>
                    <div style="text-align:center"><div style="font-size:0.6rem; color:var(--text-mute)">LogP</div><div style="font-size:0.8rem; font-weight:700">${der.metrics.logp}</div></div>
                    <div style="text-align:center"><div style="font-size:0.6rem; color:var(--text-mute)">HBD</div><div style="font-size:0.8rem; font-weight:700">${der.metrics.hbd}</div></div>
                    <div style="text-align:center"><div style="font-size:0.6rem; color:var(--text-mute)">HBA</div><div style="font-size:0.8rem; font-weight:700">${der.metrics.hba}</div></div>
                </div>
                <div style="margin-top:15px; font-size:0.75rem; color:var(--accent1); font-weight:700">Derivative Screening: ${der.safety.toxicity.level} Toxicity Risk</div>
            </div>
        `;
        resultsGrid.appendChild(item);
    });
  } catch (e) {
    resultsGrid.innerHTML = `<div style="color:#ef4444; padding:20px">Generation Error: Backend server unreachable.</div>`;
  }
}

/* ═══════════════════════════════════════════════════════════════
   MULTI-ORGAN TOXICITY + PGx DEEP-DIVE ENGINE
   ═══════════════════════════════════════════════════════════════ */

// Singleton chart instances (so we can destroy & rebuild without ghosting)
let _organRadarChart = null;
let _modalRadarChart = null;

const ORGAN_COLORS = {
  hepatotoxicity: { color: '#f97316', icon: '🫁', label: 'Liver (Hepato)' },
  cardiotoxicity:  { color: '#ef4444', icon: '🫀', label: 'Heart (Cardio)' },
  nephrotoxicity:  { color: '#3b82f6', icon: '🫘', label: 'Kidney (Nephro)' },
  endocrine:       { color: '#a78bfa', icon: '🔬', label: 'Endocrine (NR-ER)' },
};

const LEVEL_COLORS = { '1A':'#ef4444','1B':'#f97316','2A':'#eab308','2B':'#3b82f6','3':'#6b7280','4':'#6b7280' };

function levelBg(l) { return `${LEVEL_COLORS[l] || '#6b7280'}22`; }

function riskColor(score) {
  if (score >= 0.6) return '#ef4444';
  if (score >= 0.3) return '#f97316';
  return '#22c55e';
}

function buildRadarChart(canvasId, toxData, existing) {
  const ctx = document.getElementById(canvasId);
  if (!ctx) return null;
  if (existing) { try { existing.destroy(); } catch(e){} }

  const organs = ['hepatotoxicity','cardiotoxicity','nephrotoxicity','endocrine'];
  const scores = organs.map(o => Math.round((toxData[o]?.score || 0) * 100));
  const colors = organs.map(o => ORGAN_COLORS[o].color);

  return new Chart(ctx, {
    type: 'radar',
    data: {
      labels: ['Liver','Heart','Kidney','Endocrine'],
      datasets: [{
        label: 'Organ Risk %',
        data: scores,
        backgroundColor: 'rgba(239,68,68,0.08)',
        borderColor: '#ef4444',
        borderWidth: 2,
        pointBackgroundColor: colors,
        pointRadius: 5,
        pointHoverRadius: 7,
      }]
    },
    options: {
      responsive: false,
      plugins: { legend: { display: false } },
      scales: {
        r: {
          min: 0, max: 100,
          ticks: { color:'rgba(255,255,255,0.3)', backdropColor:'transparent', stepSize: 25 },
          grid: { color:'rgba(255,255,255,0.06)' },
          pointLabels: { color:'rgba(255,255,255,0.6)', font:{ size:11, weight:'700' } }
        }
      }
    }
  });
}

function buildOrganCards(container, toxData) {
  if (!container) return;
  container.innerHTML = '';
  const organs = ['hepatotoxicity','cardiotoxicity','nephrotoxicity','endocrine'];
  organs.forEach(organ => {
    const d = toxData[organ];
    if (!d) return;
    const meta = ORGAN_COLORS[organ];
    const pct = Math.round((d.score || 0) * 100);
    const col = riskColor(d.score || 0);
    const alerts = d.alerts?.slice(0,2).map(a => `<li style="font-size:0.72rem; color:var(--text-mute); line-height:1.4">${a}</li>`).join('') || '';
    const card = document.createElement('div');
    card.style.cssText = `background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:12px; padding:14px; border-left:3px solid ${col};`;
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px">
        <div style="font-size:0.85rem; font-weight:700;">${meta.icon} ${meta.label}</div>
        <div style="background:${col}22; color:${col}; font-size:0.75rem; font-weight:800; padding:2px 8px; border-radius:10px;">${d.level}</div>
      </div>
      <div style="height:4px; background:rgba(255,255,255,0.05); border-radius:2px; margin-bottom:8px; overflow:hidden;">
        <div style="height:100%; width:${pct}%; background:${col}; border-radius:2px; transition:width 0.6s ease;"></div>
      </div>
      ${alerts ? `<ul style="margin:0; padding-left:14px;">${alerts}</ul>` : ''}
    `;
    container.appendChild(card);
  });
}

function buildPgxTable(container, evidenceData) {
  if (!container || !evidenceData?.evidence) return;
  container.innerHTML = '';
  if (!evidenceData.evidence.length) {
    container.innerHTML = '<p style="color:var(--text-mute); font-size:0.85rem;">No pharmacogenomics markers found for this drug in our database.</p>';
    return;
  }
  evidenceData.evidence.forEach(entry => {
    const col = LEVEL_COLORS[entry.evidence_level] || '#6b7280';
    const card = document.createElement('div');
    card.style.cssText = `background:rgba(255,255,255,0.02); border:1px solid rgba(255,255,255,0.06); border-radius:14px; padding:18px; border-left:4px solid ${col};`;
    const phenoHtml = Object.entries(entry.phenotype_impact || {}).map(([k,v]) => `
      <div style="padding:8px 12px; background:rgba(0,0,0,0.2); border-radius:8px; margin-top:6px;">
        <div style="font-size:0.68rem; color:${col}; font-weight:800; text-transform:uppercase; margin-bottom:3px;">${k.replace(/_/g,' ')}</div>
        <div style="font-size:0.8rem; color:var(--text); line-height:1.5">${v}</div>
      </div>`).join('');
    card.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:10px; flex-wrap:wrap; gap:8px;">
        <div>
          <span style="font-weight:800; font-size:0.95rem;">${entry.gene}</span>
          <span style="font-size:0.75rem; color:var(--text-mute); margin-left:8px;">${entry.gene_name}</span>
        </div>
        <div style="display:flex; gap:6px; align-items:center;">
          <span style="background:${col}22; color:${col}; padding:3px 10px; border-radius:20px; font-size:0.75rem; font-weight:900; border:1px solid ${col}55;">Level ${entry.evidence_level}</span>
          <span style="background:rgba(255,255,255,0.05); color:var(--text-mute); padding:3px 8px; border-radius:8px; font-size:0.7rem;">${entry.guideline}</span>
        </div>
      </div>
      <p style="margin:0 0 8px; font-size:0.85rem; color:var(--text); line-height:1.5;"><strong>Recommendation:</strong> ${entry.recommendation}</p>
      <div style="display:flex; flex-direction:column; gap:4px;">${phenoHtml}</div>
    `;
    container.appendChild(card);
  });
}

// Main entry — load multi-tox + PGx for a drug into the Safety tab panels
async function loadSafetyDeepDive(drugName) {
  // Show panels with loading state
  const multiPanel = document.getElementById('multiOrganPanel');
  const pgxPanel   = document.getElementById('pgxEvidencePanel');
  const breakdown  = document.getElementById('organBreakdownGrid');
  const pgxTable   = document.getElementById('pgxEvidenceTable');
  const badge      = document.getElementById('organOverallBadge');
  const pgxBadge   = document.getElementById('pgxActionableBadge');

  multiPanel.style.display = 'block';
  pgxPanel.style.display   = 'block';
  breakdown.innerHTML      = '<div style="color:var(--text-mute); font-size:0.85rem; grid-column:1/-1">Loading organ risk...</div>';
  pgxTable.innerHTML       = '<div style="color:var(--text-mute); font-size:0.85rem">Fetching PGx markers...</div>';

  // Fetch both in parallel
  const [toxRes, pgxRes] = await Promise.all([
    fetch(`${API}/multi-tox`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({drug: drugName}) }).then(r=>r.json()).catch(()=>null),
    fetch(`${API}/pgx`,       { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({drug: drugName}) }).then(r=>r.json()).catch(()=>null),
  ]);

  // Render radar + breakdown
  if (toxRes?.toxicity && !toxRes.error) {
    const tox = toxRes.toxicity;
    const overallCol = riskColor(tox.overall_score || 0);
    badge.style.cssText = `background:${overallCol}22; color:${overallCol}; border:1px solid ${overallCol}55; padding:6px 14px; border-radius:20px; font-size:0.8rem; font-weight:800;`;
    badge.textContent = `Overall: ${tox.overall_level}`;
    _organRadarChart = buildRadarChart('organRadarChart', tox, _organRadarChart);
    buildOrganCards(breakdown, tox);
  } else {
    breakdown.innerHTML = '<div style="color:#ef4444; font-size:0.85rem; grid-column:1/-1">Toxicity data unavailable for this drug (no SMILES structure found).</div>';
    badge.textContent = '';
  }

  // Render PGx table
  if (pgxRes?.evidence && !pgxRes.error) {
    const n = pgxRes.evidence.total_markers || 0;
    pgxBadge.textContent = n > 0 ? `${n} PGx Marker${n>1?'s':''} Found` : 'No PGx Markers';
    buildPgxTable(pgxTable, pgxRes.evidence);
  } else {
    pgxTable.innerHTML = '<p style="color:var(--text-mute); font-size:0.85rem;">No pharmacogenomics data available.</p>';
    pgxBadge.textContent = '';
  }

  // 🧊 3D Molecular Viewer Integration
  const mol3dPanel = document.getElementById('mol3dPanel');
  const glViewerEl = document.getElementById('glViewer');
  const glLoader   = document.getElementById('glLoader');
  
  if (mol3dPanel && glViewerEl) {
      mol3dPanel.style.display = 'block';
      glLoader.style.display = 'flex';
      try {
          const res = await fetch(`${API}/mol3d`, { 
              method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({drug: drugName}) 
          });
          const resJson = await res.json();
          glLoader.style.display = 'none';
          
          if (!resJson.error && resJson.molBlock) {
              // Initialize 3Dmol.js viewer
              glViewerEl.innerHTML = ''; // prevent duplicates
              let config = { backgroundColor: 'transparent' };
              let viewer = $3Dmol.createViewer( glViewerEl, config );
              viewer.addModel( resJson.molBlock, "mol" );
              viewer.setStyle({}, {stick:{radius:0.15}, sphere:{scale:0.3}});
              viewer.zoomTo();
              viewer.render();
          } else {
              glViewerEl.innerHTML = `<div style="padding:20px; color:#ef4444; font-size:0.85rem">Could not render 3D model: ${resJson.error || 'No structure'}</div>`;
          }
      } catch (e) {
          glLoader.style.display = 'none';
          glViewerEl.innerHTML = `<div style="padding:20px; color:#ef4444; font-size:0.85rem">Could not render 3D model.</div>`;
      }
  }

  // Scroll into view
  multiPanel.scrollIntoView({ behavior:'smooth', block:'start' });
}

// Called after analysis completes — populate the drug selector pills in Safety tab
function populateSafetyDrugSelector(drugs) {
  const selector = document.getElementById('safetyDrugSelector');
  const pills    = document.getElementById('safetyDrugPills');
  if (!selector || !pills || !drugs?.length) return;

  selector.style.display = 'flex';
  pills.innerHTML = '';
  drugs.forEach(drug => {
    const pill = document.createElement('button');
    pill.textContent = drug;
    pill.style.cssText = 'background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.1); color:var(--text); padding:6px 14px; border-radius:20px; cursor:pointer; font-size:0.8rem; font-weight:600; transition:all 0.2s;';
    pill.onmouseover = () => { pill.style.background='rgba(139,92,246,0.2)'; pill.style.borderColor='rgba(139,92,246,0.4)'; };
    pill.onmouseout  = () => { pill.style.background='rgba(255,255,255,0.05)'; pill.style.borderColor='rgba(255,255,255,0.1)'; };
    pill.onclick     = () => loadSafetyDeepDive(drug);
    pills.appendChild(pill);
  });
}

// Enrich the individual drug safety modal with organ radar + PGx
async function enrichSafetyModal(drugName) {
  const modalOrgan = document.getElementById('modalOrganSection');
  const modalPgx   = document.getElementById('modalPgxSection');
  if (!modalOrgan) return;

  // Organ radar in modal
  const [toxRes, pgxRes] = await Promise.all([
    fetch(`${API}/multi-tox`, { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({drug: drugName}) }).then(r=>r.json()).catch(()=>null),
    fetch(`${API}/pgx`,       { method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({drug: drugName}) }).then(r=>r.json()).catch(()=>null),
  ]);

  if (toxRes?.toxicity && !toxRes.error) {
    _modalRadarChart = buildRadarChart('modalRadarChart', toxRes.toxicity, _modalRadarChart);
    buildOrganCards(document.getElementById('modalOrganCards'), toxRes.toxicity);
    modalOrgan.style.display = 'block';
  }

  if (pgxRes?.evidence?.evidence?.length) {
    buildPgxTable(document.getElementById('modalPgxContent'), pgxRes.evidence);
    if (modalPgx) modalPgx.style.display = 'block';
  }
}

/* ══════════════════════════════════════════════
   PHASE 3 ADVANCED AI FEATURES
══════════════════════════════════════════════ */

// 1. Polypharmacy Graph Network (Cytoscape)
function renderPolypharmacyGraph(interactions) {
    const cySection = document.getElementById("polypharmacyGraphSection");
    if (!cySection || !interactions || interactions.length === 0) return;
    
    // Only show if 2 or more drugs (and actual interactions exist or we can show disconnected nodes)
    cySection.style.display = "block";
    
    // Build Elements array
    const elements = [];
    const addedNodes = new Set();
    
    interactions.forEach(inter => {
        // Add nodes
        if (!addedNodes.has(inter.drug_a)) {
            elements.push({ data: { id: inter.drug_a, label: inter.drug_a.toUpperCase() } });
            addedNodes.add(inter.drug_a);
        }
        if (!addedNodes.has(inter.drug_b)) {
            elements.push({ data: { id: inter.drug_b, label: inter.drug_b.toUpperCase() } });
            addedNodes.add(inter.drug_b);
        }
        
        // Add edge
        const col = inter.severity === 'severe' ? '#ef4444' : (inter.severity === 'moderate' ? '#f59e0b' : '#3b82f6');
        elements.push({ 
            data: { 
                id: inter.drug_a + '-' + inter.drug_b, 
                source: inter.drug_a, 
                target: inter.drug_b,
                severity: inter.severity
            },
            classes: inter.severity 
        });
    });
    
    if (window.cytoscape) {
        window.cytoscape({
            container: document.getElementById('cy'),
            elements: elements,
            style: [
                {
                    selector: 'node',
                    style: {
                        'background-color': '#1f2937',
                        'label': 'data(label)',
                        'color': '#fff',
                        'font-size': '10px',
                        'text-valign': 'center',
                        'text-halign': 'center',
                        'width': '60px',
                        'height': '60px',
                        'border-width': 2,
                        'border-color': '#3b82f6'
                    }
                },
                {
                    selector: 'edge',
                    style: {
                        'width': 3,
                        'line-color': '#3b82f6',
                        'curve-style': 'bezier'
                    }
                },
                {
                    selector: 'edge.severe',
                    style: { 'line-color': '#ef4444', 'width': 5 }
                },
                {
                    selector: 'edge.moderate',
                    style: { 'line-color': '#f59e0b', 'width': 4 }
                }
            ],
            layout: {
                name: 'circle', // or cose for force-directed
                padding: 30
            }
        });
    }
}

// 2. Chronopharmacology Dosing Timeline
function renderChronopharmacologyTimeline(data) {
    const sec = document.getElementById("chronoSection");
    const grid = document.getElementById("chronoTimelineGrid");
    if (!sec || !grid || !data || !data.timeline || data.timeline.length === 0) return;
    
    sec.style.display = "block";
    grid.innerHTML = "";
    
    // Warnings
    if (data.chronotherapy_alerts && data.chronotherapy_alerts.length > 0) {
        const wdiv = document.createElement("div");
        wdiv.style.cssText = "background:rgba(239,68,68,0.1); border-left:3px solid #ef4444; padding:10px; border-radius:6px; font-size:0.8rem; color:#fca5a5; margin-bottom:15px;";
        wdiv.innerHTML = `<strong>Scheduling Critical Info:</strong><ul style="margin:5px 0 0 15px; padding:0;">` + 
                         data.chronotherapy_alerts.map(a => `<li>${a}</li>`).join('') + `</ul>`;
        grid.appendChild(wdiv);
    }
    
    // Dosing blocks
    data.timeline.forEach(block => {
        const bdiv = document.createElement("div");
        bdiv.style.cssText = "display:flex; justify-content:space-between; align-items:center; background:rgba(255,255,255,0.03); border:1px solid rgba(255,255,255,0.08); padding:15px; border-radius:10px;";
        bdiv.innerHTML = `
            <div style="display:flex; align-items:center; gap:10px; font-weight:700; width:150px;">
                <span>${block.icon}</span> ${block.time}
            </div>
            <div style="flex:1; display:flex; gap:10px; flex-wrap:wrap;">
                ${block.drugs.map(d => `<span style="background:var(--accent1); color:var(--bg); padding:4px 10px; border-radius:15px; font-size:0.75rem; font-weight:800; box-shadow:0 0 10px rgba(167,139,250,0.3);">${d}</span>`).join('')}
            </div>
        `;
        grid.appendChild(bdiv);
    });
}

// 3. Potency Lab Prediction
const btnPredictPotency = document.getElementById("btnPredictPotency");
if (btnPredictPotency) {
    btnPredictPotency.onclick = async () => {
        const inp = document.getElementById("potencySmilesInput").value;
        if(!inp) return alert("Please enter a SMILES string!");
        
        btnPredictPotency.textContent = "Predicting...";
        btnPredictPotency.disabled = true;
        
        try {
            const r = await fetch(`${API}/predict-potency`, {
                method: "POST", headers:{"Content-Type":"application/json"},
                body: JSON.stringify({smiles: inp})
            });
            const data = await r.json();
            
            if (data.error) {
                alert(data.error);
            } else {
                document.getElementById("potencyResultBox").style.display = "block";
                document.getElementById("potencyScore").textContent = data.pIC50;
                document.getElementById("potencyIC50").textContent = data.estimated_IC50_nM;
                document.getElementById("potencyClass").textContent = data.potency_class;
            }
        } catch (e) {
            alert("Error running Deep Learning model.");
        } finally {
            btnPredictPotency.textContent = "Predict pIC50";
            btnPredictPotency.disabled = false;
        }
    };
}

// 4. Medical AI Chatbot
async function askAIChatbot(drugsList, interactionObj) {
    const sec = document.getElementById("aiChatbotSection");
    const msgs = document.getElementById("chatMessages");
    if(!sec || !msgs) return;
    
    // Auto-scroll to chatbot
    sec.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    // Loading state
    msgs.innerHTML = `<div style="color:var(--accent1); display:flex; align-items:center; gap:8px;">
        <span class="btn-predict-loader spinning" style="width:14px; height:14px;"></span>
        *Analyzing specific metabolomic pathways...*
    </div>`;
    
    try {
        const r = await fetch(`${API}/chatbot`, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query: "Analyze", drugs: drugsList, interaction: interactionObj })
        });
        const data = await r.json();
        
        if (data.response) {
            // Typewriter effect formatting (markdown parser primitive)
            let formatted = data.response.replace(/\*\*(.*?)\*\*/g, '<strong style="color:#fff;">$1</strong>');
            formatted = formatted.replace(/\*(.*?)\*/g, '<em style="color:#a78bfa;">$1</em>');
            formatted = formatted.replace(/\n/g, '<br/>');
            
            msgs.innerHTML = `<div style="background:rgba(167,139,250,0.1); border:1px solid rgba(167,139,250,0.2); padding:15px; border-radius:12px; color:var(--text); line-height:1.6;">
                ${formatted}
            </div>`;
        } else {
            console.error("Chatbot failed with info:", data);
            msgs.innerHTML = `<div style="color:#ef4444;">Error generating response. Server details: ${data.details || JSON.stringify(data)}</div>`;
        }
    } catch (e) {
        msgs.innerHTML = `<div style="color:#ef4444;">System Offline.</div>`;
    }
}
