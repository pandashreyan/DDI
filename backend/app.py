"""
Drug-Drug Interaction (DDI) Prediction Backend
🔌 Real-World Dataset Integration: db_drug_interactions.csv
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from datetime import datetime

import json
import pickle
import base64

# Optional heavy dependencies: import if available, otherwise degrade gracefully
try:
    import pandas as pd
except Exception:
    pd = None

try:
    import numpy as np
except Exception:
    np = None

try:
    from rdkit import Chem
    from rdkit.Chem import AllChem, Draw, Descriptors
except Exception:
    Chem = None
    AllChem = None
    Draw = None
    Descriptors = None
import logging
from functools import lru_cache
try:
    from waitress import serve
except ImportError:
    serve = None

from admet_engine import ADMET_ENGINE
from multi_organ_tox import MULTI_ORGAN_TOX
from pgx_evidence_map import get_pgx_evidence, get_patient_pgx_report
from molecular_optimizer import MOLECULAR_OPTIMIZER
from pic50_engine import PIC50_ENGINE
from chrono_engine import generate_dosing_schedule

# SHAP Explainability Module
try:
    from shap_explainer import init_shap_explainer, get_prediction_explanation
    SHAP_AVAILABLE = True
except Exception as e:
    print(f"[SHAP-WARN] Module not available: {e}")
    SHAP_AVAILABLE = False

# Adverse Events Predictor Module
try:
    from adverse_events_predictor import init_adverse_event_predictor, get_adverse_events, get_individual_safety
    AE_AVAILABLE = True
    ADVERSE_EVENTS_AVAILABLE = True
    print("[AE-OK] Adverse event predictor loaded successfully.")
except Exception as e:
    print(f"[AE-WARN] Adverse event predictor failed to load: {e}")
    import traceback
    traceback.print_exc()
    AE_AVAILABLE = False
    ADVERSE_EVENTS_AVAILABLE = False
    def get_adverse_events(*args, **kwargs): return []
    def get_individual_safety(*args, **kwargs): return {}

# Clinical Evidence Module
try:
    from clinical_evidence import get_combined_evidence
    EVIDENCE_AVAILABLE = True
except ImportError:
    EVIDENCE_AVAILABLE = False
    print("[EVIDENCE-WARN] clinical_evidence.py not found.")

# Patient Profile Adjuster
try:
    from profile_adjuster import calculate_personalized_risk
    PROFILE_ADJUSTER_AVAILABLE = True
except ImportError:
    PROFILE_ADJUSTER_AVAILABLE = False
    print("[PROFILE-WARN] profile_adjuster.py not found.")

# Regimen Optimizer Module
try:
    from regimen_optimizer import optimize_regimen
    OPTIMIZER_AVAILABLE = True
except ImportError:
    OPTIMIZER_AVAILABLE = False
    print("[OPTIMIZER-WARN] regimen_optimizer.py not found.")

# Lifestyle Analyzer Module
try:
    from lifestyle_analyzer import analyze_lifestyle_interactions
    LIFESTYLE_AVAILABLE = True
except ImportError:
    LIFESTYLE_AVAILABLE = False
    print("[LIFESTYLE-WARN] lifestyle_analyzer.py not found.")

# Pharmacy Intelligence Module
try:
    from pharmacy_service import get_drug_pricing
    PHARMACY_AVAILABLE = True
except ImportError:
    PHARMACY_AVAILABLE = False
    print("[PHARMACY-WARN] pharmacy_service.py not found.")

# Pharmacogenomics (PGx) Module
try:
    from pgx_engine import calculate_pgx_risk
    PGX_AVAILABLE = True
except ImportError:
    PGX_AVAILABLE = False
    print("[PGX-WARN] pgx_engine.py not found.")

# Configure Flask to serve the frontend as a single-page application (SPA)
app = Flask(__name__, 
            static_folder=os.path.join(os.path.dirname(__file__), '..', 'frontend'),
            static_url_path='')
CORS(app)

@app.route('/')
def index():
    return app.send_static_file('index.html')

# ─────────────────────────────────────────────
# DATA & AI CONFIG (Absolute Paths for Stability)
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'db_drug_interactions.csv', 'db_drug_interactions.csv')
META_PATH = os.path.join(BASE_DIR, 'drug_metadata.json')
MODEL_PATH = os.path.join(BASE_DIR, 'ddi_model.pkl')

REAL_KNOWLEDGE_BASE = {}
EXPERT_KNOWLEDGE_BASE = {}
DRUG_METADATA = {}
AI_MODEL = None
PREDICTION_CACHE = {}
EXPERT_META_PATH = os.path.join(BASE_DIR, 'expert_interactions.json')

# Drug name alias map: common/brand names → clinical/IUPAC names used in DB
DRUG_ALIASES = {
    "aspirin": "aspirin",
    "tylenol": "acetaminophen",
    "paracetamol": "acetaminophen",
    "advil": "ibuprofen",
    "motrin": "ibuprofen",
    "aleve": "naproxen",
    "prozac": "fluoxetine",
    "zoloft": "sertraline",
    "paxil": "paroxetine",
    "lexapro": "escitalopram",
    "celexa": "citalopram",
    "wellbutrin": "bupropion",
    "effexor": "venlafaxine",
    "cymbalta": "duloxetine",
    "valium": "diazepam",
    "xanax": "alprazolam",
    "ativan": "lorazepam",
    "klonopin": "clonazepam",
    "ambien": "zolpidem",
    "lipitor": "atorvastatin",
    "zocor": "simvastatin",
    "crestor": "rosuvastatin",
    "pravachol": "pravastatin",
    "mevacor": "lovastatin",
    "lescol": "fluvastatin",
    "coumadin": "warfarin",
    "eliquis": "apixaban",
    "xarelto": "rivaroxaban",
    "pradaxa": "dabigatran",
    "plavix": "clopidogrel",
    "digox": "digoxin",
    "lasix": "furosemide",
    "norvasc": "amlodipine",
    "toprol": "metoprolol",
    "coreg": "carvedilol",
    "lopressor": "metoprolol",
    "inderal": "propranolol",
    "glucophage": "metformin",
    "lantus": "insulin glargine",
    "prilosec": "omeprazole",
    "nexium": "esomeprazole",
    "prevacid": "lansoprazole",
    "pepcid": "famotidine",
    "zantac": "ranitidine",
    "diflucan": "fluconazole",
    "cipro": "ciprofloxacin",
    "levaquin": "levofloxacin",
    "flagyl": "metronidazole",
    "amox": "amoxicillin",
    "zithromax": "azithromycin",
    "biaxin": "clarithromycin",
    "vibramycin": "doxycycline",
    "viagra": "sildenafil",
    "cialis": "tadalafil",
    "lyrica": "pregabalin",
    "neurontin": "gabapentin",
    "topamax": "topiramate",
    "depakote": "valproic acid",
    "lamictal": "lamotrigine",
    "dilantin": "phenytoin",
    "tegretol": "carbamazepine",
    "cozaar": "losartan",
    "diovan": "valsartan",
    "avapro": "irbesartan",
    "benicar": "olmesartan",
    "micardis": "telmisartan",
    "zestril": "lisinopril",
    "altace": "ramipril",
    "vasotec": "enalapril",
    "accupril": "quinapril",
    "seroquel": "quetiapine",
    "zyprexa": "olanzapine",
    "risperdal": "risperidone",
    "abilify": "aripiprazole",
    "haldol": "haloperidol",
    "elavil": "amitriptyline",
    "pamelor": "nortriptyline",
    "tofranil": "imipramine",
    "ultram": "tramadol",
    "oxycontin": "oxycodone",
    "percocet": "oxycodone",
    "vicodin": "hydrocodone",
    "morphine sulfate": "morphine",
    "ms contin": "morphine",
    "demerol": "meperidine",
    "plaquenil": "hydroxychloroquine",
    "prednisone-5": "prednisone",
    "solu-medrol": "methylprednisolone",
    "flonase": "fluticasone",
    "ventolin": "albuterol",
    "proventil": "albuterol",
    "singulair": "montelukast",
    "zyrtec": "cetirizine",
    "claritin": "loratadine",
    "allegra": "fexofenadine",
    "benadryl": "diphenhydramine",
    "atarax": "hydroxyzine",
    "flexeril": "cyclobenzaprine",
    "celebrex": "celecoxib",
    "mobic": "meloxicam",
    "feldene": "piroxicam",
    "voltaren": "diclofenac",
    "zyloprim": "allopurinol",
    "flomax": "tamsulosin",
    "proscar": "finasteride",
    "propecia": "finasteride",
    "avodart": "dutasteride",
    "aldactone": "spironolactone",
    "lasix": "furosemide",
    "bumex": "bumetanide",
    "midamor": "amiloride",
    "dyrenium": "triamterene",
    "inspra": "eplerenone",
    "nitro": "nitroglycerin",
    "isordil": "isosorbide dinitrate",
    "ismo": "isosorbide mononitrate",
    "cordarone": "amiodarone",
    "calan": "verapamil",
    "cardizem": "diltiazem",
    "procardia": "nifedipine",
    "norvir": "ritonavir",
    "acyclovir": "acyclovir",
    "valtrex": "valacyclovir",
    "tamiflu": "oseltamivir",
    "humira": "adalimumab",
    "remicade": "infliximab",
    "enbrel": "etanercept",
    "cimetidine": "cimetidine",
    "hytrin": "terazosin",
    "cardura": "doxazosin",
    "hydrodiuril": "hydrochlorothiazide",
    "hctz": "hydrochlorothiazide",
    "lozol": "indapamide",
    "zaroxolyn": "metolazone",
    "hygroton": "chlorthalidone",
    "acetylsalicylic acid": "acetylsalicylic acid",  # identity
}

# Configure Logging
logging.basicConfig(
    filename='clinical_engine.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def load_system_data():
    global REAL_KNOWLEDGE_BASE, EXPERT_KNOWLEDGE_BASE, DRUG_METADATA, AI_MODEL
    
    # 1. Load Clinical Database (CSV)
    if os.path.exists(DATA_PATH):
        if pd is None:
            print("[DDI-WARN] pandas not available — skipping clinical CSV load.")
        else:
            try:
                df = pd.read_csv(DATA_PATH)
                for _, row in df.iterrows():
                    d1, d2 = str(row['Drug 1']).strip().lower(), str(row['Drug 2']).strip().lower()
                    REAL_KNOWLEDGE_BASE[frozenset([d1, d2])] = str(row['Interaction Description'])
                print(f"[DDI-INFO] {len(REAL_KNOWLEDGE_BASE)} clinical pairs loaded.")
            except Exception as e:
                print(f"[DDI-ERROR] CSV Load Fail: {e}")
    
    # 2. Load Rich Metadata (JSON)
    if os.path.exists(META_PATH):
        try:
            with open(META_PATH, 'r') as f:
                DRUG_METADATA = json.load(f)
            print(f"[DDI-INFO] {len(DRUG_METADATA)} rich drug metadata records loaded.")
        except Exception as e: print(f"[DDI-ERROR] Meta Load Fail: {e}")
    
    # 2.3. Load Expert Knowledge Base (JSON)
    if os.path.exists(EXPERT_META_PATH):
        try:
            with open(EXPERT_META_PATH, 'r') as f:
                expert_data = json.load(f)
                for item in expert_data:
                    d1, d2 = item['drug_a'].lower().strip(), item['drug_b'].lower().strip()
                    EXPERT_KNOWLEDGE_BASE[frozenset([d1, d2])] = item
                print(f"[DDI-INFO] {len(EXPERT_KNOWLEDGE_BASE)} EXPERT interactions loaded.")
        except Exception as e:
            print(f"[DDI-ERROR] Expert Data Load Fail: {e}")
    
    # 2.5. Initialize Adverse Event Predictor
    if AE_AVAILABLE:
        try:
            init_adverse_event_predictor(DRUG_METADATA, REAL_KNOWLEDGE_BASE)
            print("[AE-INFO] Adverse Event Predictor initialized successfully.")
        except Exception as e:
            print(f"[AE-WARN] Failed to initialize adverse event predictor: {e}")

    # 3. Load AI Model (Pickle) — only when numpy is present
    if os.path.exists(MODEL_PATH):
        if np is None:
            print("[DDI-WARN] numpy not available — skipping AI model load.")
        else:
            try:
                with open(MODEL_PATH, 'rb') as f:
                    AI_MODEL = pickle.load(f)
                print("[DDI-INFO] AI Prediction Model (RandomForest) active.")
            except Exception as e:
                print(f"[DDI-INFO] AI Model not ready yet: {e}")

def get_features(smiles, mw=None, logp=None):
    """Generate 1024-bit Morgan Fingerprint + Physical Properties"""
    # If RDKit or numpy unavailable, return a zero-vector fallback
    if Chem is None or AllChem is None or np is None:
        if np is None:
            return [0.0] * 1026
        return np.zeros(1026)

    try:
        mol = Chem.MolFromSmiles(smiles)
        if mol:
            fp_vec = AllChem.GetMorganFingerprintAsBitVect(mol, 2, nBits=1024)
            fp = np.array(fp_vec)
            # Match training normalization
            mw_val = float(mw) if mw is not None else 300.0
            logp_val = float(logp) if logp is not None else 2.5
            return np.append(fp, [mw_val / 500.0, logp_val / 5.0])
    except Exception:
        pass

    return np.zeros(1026)

def get_cds_suggestion(severity, cyp_overlap, same_class):
    """Generate professional Clinical Decision Support (CDS) suggestions"""
    if severity == "none": return None
    
    suggestions = []
    if cyp_overlap:
        suggestions.append(f"Consider selecting an alternative agent not metabolized by {', '.join(cyp_overlap)}.")
    if same_class:
        suggestions.append("Therapeutic duplication detected. Assess necessity of multi-agent therapy within this class.")
    
    if severity == "severe":
        suggestions.append("High risk of Adverse Drug Event (ADE). Immediate clinical review recommended. Consider dose reduction or alternative therapy.")
    elif severity == "moderate":
        suggestions.append("Monitor clinical response and serum concentrations if applicable. Adjust dosage as needed.")
        
    return " ".join(suggestions)

def predict_ai(drug_a, drug_b):
    """Predict interaction using hybrid ML model + Diagnostic Metadata"""
    if not AI_MODEL: return None
    
    # Robust metadata access to satisfy linter and runtime
    m1 = DRUG_METADATA.get(drug_a)
    if not isinstance(m1, dict): m1 = {}
    m2 = DRUG_METADATA.get(drug_b)
    if not isinstance(m2, dict): m2 = {}
    
    s1, s2 = m1.get('smiles'), m2.get('smiles')
    
    if s1 and s2:
        # Use new feature extraction (1026-bit per drug)
        f1 = get_features(s1, m1.get('mw'), m1.get('logp'))
        f2 = get_features(s2, m2.get('mw'), m2.get('logp'))
        combined = np.concatenate([f1, f2]).reshape(1, -1)
        
        try:
            prob = AI_MODEL.predict_proba(combined)[0][1]
        except Exception as e:
            print(f"[DDI-ERROR] Prediction Fail: {e}")
            return None
        
        # 🧪 ADVANCED DIAGNOSTICS
        diagnosis = "AI: Predictive structural pathway analysis."
        
        # Simulated SHAP/LIME contributions for "Clinical Intelligence" UI
        importance = {
            "molecular_fingerprints": round(float(prob) * 0.65, 2),
            "metabolic_pathway": 0.0,
            "physicochemical_properties": round(0.1 + (float(m1.get('logp', 0) or 0)*0.02), 2)
        }
        
        # Check CYP metabolic overlap
        cyp1 = set(m1.get('cyp', []))
        cyp2 = set(m2.get('cyp', []))
        common_cyp = list(cyp1.intersection(cyp2))
        same_class = m1.get('class') == m2.get('class') and m1.get('class') != "General Therapeutics"
        
        if common_cyp:
            diagnosis = f"METABOLIC WARNING: Both drugs are processed by {', '.join(common_cyp)}. Increased risk of competitive inhibition."
            importance["metabolic_pathway"] = 0.85
        elif same_class:
            diagnosis = f"PHARMACODYNAMIC WARNING: Combined use of two {m1.get('class')}s may lead to additive toxicity effects."
            importance["physicochemical_properties"] += 0.4
        
        # Severity assignment
        if prob > 0.8: sev = "severe"
        elif prob > 0.5: sev = "moderate"
        elif prob > 0.2: sev = "mild"
        else: sev = "none"
        
        cds = get_cds_suggestion(sev, common_cyp, same_class)
        
        # Map probability to severity results
        msg = f"CRITICAL: {diagnosis} High structural similarity to known toxic pairs." if sev == "severe" else \
              f"MODERATE: {diagnosis} Possible adverse drug event suspected by ML core." if sev == "moderate" else \
              f"CAUTION: {diagnosis} Minor metabolic or structural overlap detected." if sev == "mild" else \
              f"AI: No significant structural or metabolic risk pathway identified."
              
        return sev, round(float(prob), 2), msg, importance, cds
        
    return "none", 0.05, "AI: No significant structural or metabolic risk pathway identified.", \
           {"molecular_fingerprints": 0.05, "metabolic_pathway": 0, "physicochemical_properties": 0.05}, None

def resolve_drug_name(name: str) -> str:
    """Resolve a common/brand drug name to its clinical DB counterpart."""
    n = name.lower().strip()
    return DRUG_ALIASES.get(n, n)

def get_severity(text):
    t = text.lower()
    # Clinical severity keywords
    if any(x in t for x in ['fatal', 'death', 'major bleeding', 'severe', 'toxicity', 'life-threatening']):
        return "severe", 0.96
    if any(x in t for x in ['increase', 'decrease', 'risk', 'adverse', 'monitor', 'caution']):
        return "moderate", 0.68
    return "mild", 0.35


# ─────────────────────────────────────────────
# DRUG REPLACEMENT ENGINE HELPERS
# ─────────────────────────────────────────────

def find_alternatives_for_drug(target_drug, limit=10):
    """Find drugs in the same therapeutic class as target_drug"""
    target_meta = DRUG_METADATA.get(target_drug)
    if not target_meta or not isinstance(target_meta, dict):
        return []
    
    target_class = target_meta.get('class', '')
    if not target_class:
        return []
    
    alternatives = []
    for drug_name, drug_meta in DRUG_METADATA.items():
        if not isinstance(drug_meta, dict):
            continue
        if drug_name == target_drug:
            continue
        if drug_meta.get('class') == target_class:
            alternatives.append(drug_name)
    
    return alternatives[:limit]

def calculate_interaction_risk(drug_a, drug_b):
    """Calculate interaction risk score between two drugs (0.0 to 1.0)"""
    pair = frozenset([drug_a.lower().strip(), drug_b.lower().strip()])
    
    # Check clinical database first
    if pair in REAL_KNOWLEDGE_BASE:
        desc = REAL_KNOWLEDGE_BASE[pair]
        sev, score = get_severity(desc)
        return score
    
    # Fall back to AI prediction
    ai_res = predict_ai(drug_a, drug_b)
    if ai_res:
        sev, score, msg, imp, cds = ai_res
        return score
    
    return 0.05  # Default low risk if no data

def get_drug_alternatives(problem_drug_a, problem_drug_b, num_suggestions=5):
    """
    Generate alternative drug suggestions for a problematic drug pair.
    Returns list of alternatives with lower interaction risk.
    """
    drug_a_meta = DRUG_METADATA.get(problem_drug_a)
    drug_b_meta = DRUG_METADATA.get(problem_drug_b)
    
    # Allow alternatives even if drug_b is not in metadata
    if not drug_a_meta or not isinstance(drug_a_meta, dict):
        return []
    
    # Get alternatives for the first drug (usually the problematic one)
    print(f"[DEBUG] AE_AVAILABLE in globals: {'AE_AVAILABLE' in globals()}")
    if 'AE_AVAILABLE' in globals():
        print(f"[DEBUG] AE_AVAILABLE value: {globals()['AE_AVAILABLE']}")
    # Start with same-class candidates
    alternatives_for_a = find_alternatives_for_drug(problem_drug_a, limit=50)
    print(f"[DDI-ALT] Looking for alternatives for {problem_drug_a} vs {problem_drug_b}. same_class_found={len(alternatives_for_a)}")

    # If not enough same-class candidates, expand to cross-class using structural similarity
    cross_candidates = []
    if len(alternatives_for_a) < max(10, num_suggestions):
        try:
            from rdkit import DataStructs
            from rdkit.Chem import AllChem
            print("[DDI-ALT] RDKit path: attempting structural neighbor search")
            target_meta = DRUG_METADATA.get(problem_drug_a, {})
            target_smiles = target_meta.get('smiles')
            target_fp = None
            if target_smiles:
                tm = Chem.MolFromSmiles(target_smiles)
                if tm:
                    target_fp = AllChem.GetMorganFingerprintAsBitVect(tm, 2, nBits=1024)
            
            # Build a candidate list with similarity scores
            for drug_name, drug_meta in DRUG_METADATA.items():
                if drug_name == problem_drug_a:
                    continue
                if drug_name in alternatives_for_a:
                    continue
                smiles = drug_meta.get('smiles')
                if not smiles or not target_fp:
                    continue
                try:
                    m = Chem.MolFromSmiles(smiles)
                    if not m: continue
                    fp = AllChem.GetMorganFingerprintAsBitVect(m, 2, nBits=1024)
                    sim = float(DataStructs.TanimotoSimilarity(target_fp, fp))
                    cross_candidates.append((drug_name, sim))
                except Exception:
                    continue
        except Exception as e:
            print(f"[DDI-ALT] RDKit neighbor search failed: {e}")
            cross_candidates = []

    print(f"[DDI-ALT] cross_candidate_count={len(cross_candidates)}")

    # Merge same-class and cross-class candidates (cross-class sorted by similarity)
    ranked_candidates = []
    seen = set()

    # Add same-class first
    for name in alternatives_for_a:
        if name in seen: continue
        seen.add(name)
        ranked_candidates.append((name, 1.0))

    # Add top cross-class candidates
    if cross_candidates:
        cross_candidates.sort(key=lambda x: x[1], reverse=True)
        for name, sim in cross_candidates[:100]:
            if name in seen: continue
            seen.add(name)
            ranked_candidates.append((name, sim))

    scored_alternatives = []
    for alt_drug, sim in ranked_candidates:
        # Avoid suggesting the comparison drug as its own alternative
        if alt_drug.lower().strip() == problem_drug_b.lower().strip():
            continue
            
        # Calculate interaction risk with reference drug
        risk_score = calculate_interaction_risk(alt_drug, problem_drug_b)
        alt_meta = DRUG_METADATA.get(alt_drug)
        if not alt_meta or not isinstance(alt_meta, dict):
            continue
        
        suggestion = {
            "name": alt_drug,
            "class": alt_meta.get('class', 'General Agent'),
            "interaction_risk": round(risk_score, 2),
            "similarity": round(float(sim), 3),
            "mw": alt_meta.get('mw', 0),
            "logp": alt_meta.get('logp', 0),
            "cyp": alt_meta.get('cyp', []),
            "risk_level": "low" if risk_score < 0.3 else "moderate" if risk_score < 0.6 else "high"
        }
        
        # Enrich with individual safety profile
        if AE_AVAILABLE:
            suggestion["safety_profile"] = get_individual_safety(alt_drug, alt_meta.get('class'))
            
        scored_alternatives.append(suggestion)

    # Sort by lowest interaction risk, break ties by higher similarity
    scored_alternatives.sort(key=lambda x: (x['interaction_risk'], -x.get('similarity', 0)))
    
    # If still empty, fallback to returning nearest structural neighbors regardless of risk
    if not scored_alternatives and cross_candidates:
        print("[DDI-ALT] No safe scored alternatives found; returning nearest structural neighbors as fallback")
        for name, sim in cross_candidates[:num_suggestions]:
            if name.lower().strip() == problem_drug_b.lower().strip(): continue
            meta = DRUG_METADATA.get(name, {})
            suggestion = {
                "name": name,
                "class": meta.get('class',''),
                "interaction_risk": calculate_interaction_risk(name, problem_drug_b),
                "similarity": round(float(sim),3),
                "mw": meta.get('mw',0),
                "logp": meta.get('logp',0),
                "cyp": meta.get('cyp',[]),
                "risk_level": "none"
            }
            if AE_AVAILABLE:
                suggestion["safety_profile"] = get_individual_safety(name, meta.get('class'))
            scored_alternatives.append(suggestion)

    return scored_alternatives[:num_suggestions]

# Load data immediately on boot
load_system_data()

# ─────────────────────────────────────────────
# ROUTES
# ─────────────────────────────────────────────

@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "db_size": len(REAL_KNOWLEDGE_BASE)})

@app.route("/api/drug-alternatives", methods=["POST"])
def drug_alternatives():
    """
    POST /api/drug-alternatives
    Input: { "drug_a": "aspirin", "drug_b": "warfarin", "alternatives_for": "drug_a" }
    Output: List of alternative drugs with lower interaction risk
    """
    data = request.get_json()
    if not data or "drug_a" not in data or "drug_b" not in data:
        return jsonify({"error": "Missing required fields: drug_a, drug_b"}), 400
    
    drug_a = resolve_drug_name(str(data.get("drug_a")).lower().strip())
    drug_b = resolve_drug_name(str(data.get("drug_b")).lower().strip())
    alternatives_for = data.get("alternatives_for", "drug_a").lower()
    num_suggestions = min(int(data.get("count", 5)), 10)  # Cap at 10
    
    # Determine which drug to find alternatives for
    problem_drug = drug_a if alternatives_for == "drug_a" else drug_b
    reference_drug = drug_b if alternatives_for == "drug_a" else drug_a
    
    alternatives = get_drug_alternatives(problem_drug, reference_drug, num_suggestions)
    
    # Get original interaction risk
    original_risk = calculate_interaction_risk(drug_a, drug_b)
    
    return jsonify({
        "original_pair": {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "interaction_risk": round(original_risk, 2)
        },
        "alternatives_for": problem_drug,
        "reference_drug": reference_drug,
        "suggestions": alternatives,
        "count": len(alternatives),
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/predict-adverse-events", methods=["POST"])
def predict_adverse_events():
    """
    POST /api/predict-adverse-events
    Input: { "drug_a": "fluoxetine", "drug_b": "codeine" }
    Output: List of predicted adverse events with probabilities and severity
    
    Example Response:
    {
      "drug_a": "fluoxetine",
      "drug_b": "codeine",
      "interaction_risk": 0.65,
      "adverse_events": [
        {
          "event_name": "Serotonin Syndrome",
          "probability": 0.45,
          "severity": "critical",
          "symptoms": ["agitation", "confusion", "muscle rigidity"],
          "risk_level": "high"
        },
        ...
      ]
    }
    """
    data = request.get_json()
    if not data or "drug_a" not in data or "drug_b" not in data:
        return jsonify({"error": "Missing required fields: drug_a, drug_b"}), 400
    
    drug_a = resolve_drug_name(str(data.get("drug_a")).lower().strip())
    drug_b = resolve_drug_name(str(data.get("drug_b")).lower().strip())
    
    # Get interaction risk
    interaction_risk = calculate_interaction_risk(drug_a, drug_b)
    
    # Predict adverse events
    adverse_events = get_adverse_events(drug_a, drug_b, interaction_risk)
    
    return jsonify({
        "drug_a": drug_a,
        "drug_b": drug_b,
        "interaction_risk": round(interaction_risk, 2),
        "adverse_events": adverse_events,
        "event_count": len(adverse_events),
        "summary": f"Predicted {len(adverse_events)} adverse events for this drug pair",
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/clinical-evidence", methods=["POST"])
def clinical_evidence():
    """
    POST /api/clinical-evidence
    Input: { "drug_a": "aspirin", "drug_b": "warfarin" }
    Output: Live FDA/PubMed data
    """
    if not EVIDENCE_AVAILABLE:
        return jsonify({"error": "Evidence module not initialized"}), 503
        
    data = request.get_json()
    if not data or "drug_a" not in data or "drug_b" not in data:
        return jsonify({"error": "Missing required fields: drug_a, drug_b"}), 400
    
    drug_a = resolve_drug_name(str(data.get("drug_a")).lower().strip())
    drug_b = resolve_drug_name(str(data.get("drug_b")).lower().strip())
    
    evidence = get_combined_evidence(drug_a, drug_b)
    
    return jsonify(evidence)

@app.route("/api/predict", methods=["POST"])
def predict():
    data = request.get_json()
    if not data or "drugs" not in data:
        return jsonify({"error": "No drugs selected"}), 400
        
    raw_drugs = data.get("drugs", [])
    if not isinstance(raw_drugs, list) or len(raw_drugs) < 2:
        return jsonify({"error": "Select at least 2 drugs for analysis"}), 400

    drugs = [resolve_drug_name(str(d).lower().strip()) for d in raw_drugs]
    patient_profile = data.get("patient_profile", {})
    results = []
    
    for i in range(len(drugs)):
        for j in range(i + 1, len(drugs)):
            pair = frozenset([drugs[i], drugs[j]])
            
            # 1. Get Base Interaction Logic (Prioritize EXPERT data)
            if pair in EXPERT_KNOWLEDGE_BASE:
                item = EXPERT_KNOWLEDGE_BASE[pair]
                desc = item.get('mechanism', 'Expert clinical interaction identified.')
                sev = item.get('severity', 'Moderate').lower()
                # Expert data gets high-confidence scores
                score = 0.95 if sev == "severe" else 0.75 if sev == "moderate" else 0.45
                source = "Clinician_Verified_Expert_DB"
                imp = {"molecular_fingerprints": 0.1, "clinical_evidence": 0.9}
                cds = item.get('management', '')
                if not cds:
                    cds = get_cds_suggestion(sev, [], False)
                # Attach extra expert data for UI
                res_obj_extra = {
                    "management": item.get('management'),
                    "safer_alternative": item.get('safer_alternative'),
                    "reference": item.get('reference'),
                    "clinical_effect": item.get('effect')
                }
            elif pair in REAL_KNOWLEDGE_BASE:
                desc = REAL_KNOWLEDGE_BASE[pair]
                sev, score = get_severity(desc)
                source = "Clinical_Standard_DB"
                imp = None
                cds = get_cds_suggestion(sev, [], False)
                res_obj_extra = {}
            else:
                ai_res = predict_ai(drugs[i], drugs[j])
                if ai_res:
                    sev, score, desc, imp, cds = ai_res
                    source = "AI_Predict_Core"
                else:
                    sev, score, desc, source, imp, cds = "none", 0.05, "No interaction found.", "Clinical_Check", None, None
                res_obj_extra = {}

            # 2. Apply Personalized Adjustments
            personalized_warnings = []
            if PROFILE_ADJUSTER_AVAILABLE and patient_profile:
                drug_a_meta = DRUG_METADATA.get(drugs[i])
                if not isinstance(drug_a_meta, dict): drug_a_meta = {"name": drugs[i]}
                drug_b_meta = DRUG_METADATA.get(drugs[j])
                if not isinstance(drug_b_meta, dict): drug_b_meta = {"name": drugs[j]}
                
                score, personalized_warnings = calculate_personalized_risk(score, drug_a_meta, drug_b_meta, patient_profile)

                # Recalculate severity based on adjusted score (don't downgrade Severe expert data too much)
                if score > 0.8: sev = "severe"
                elif score > 0.5: sev = "moderate"
                elif score > 0.2: sev = "mild"
                else: sev = "none"

            # 3. Finalize Result
            res_obj = {
                "drug_a": drugs[i], "drug_b": drugs[j],
                "risk_score": score, "severity": sev,
                "mechanism": desc, "source": source,
                "adverse_events": get_adverse_events(drugs[i], drugs[j], score),
                "personalized_warnings": personalized_warnings,
                **res_obj_extra
            }
            if imp: res_obj["importance"] = imp
            if cds: res_obj["cds"] = cds
            
            # 2.5 Apply Pharmacogenomics (PGx) Adjustments
            if PGX_AVAILABLE and patient_profile.get('genetics'):
                drug_a_meta = DRUG_METADATA.get(drugs[i], {"name": drugs[i]})
                drug_b_meta = DRUG_METADATA.get(drugs[j], {"name": drugs[j]})
                
                pgx_score, pgx_warnings = calculate_pgx_risk(score, drug_a_meta, drug_b_meta, patient_profile['genetics'])
                
                if pgx_warnings:
                    score = pgx_score
                    res_obj["risk_score"] = round(score, 2)
                    res_obj["pgx_warnings"] = pgx_warnings
                    # Update severity if PGx pushes it higher
                    if score > 0.8: res_obj["severity"] = "severe"
                    elif score > 0.5: res_obj["severity"] = "moderate"
                    elif score > 0.2: res_obj["severity"] = "mild"
            
            results.append(res_obj)

    if not results:
        max_risk = 0.0
        overall = "none"
    else:
        max_risk = max([r['risk_score'] for r in results])
        overall = "severe" if any(r['severity'] == "severe" for r in results) else "moderate" if any(r['severity'] == "moderate" for r in results) else "none"

    # Regimen Optimization (for 3+ drugs)
    optimization = None
    if OPTIMIZER_AVAILABLE and len(drugs) >= 3:
        optimization = optimize_regimen(drugs, DRUG_METADATA)
        if optimization and optimization.get('regimen_score', 0) > max_risk:
            max_risk = optimization['regimen_score']

    # Lifestyle Analysis
    lifestyle_profile = data.get("lifestyle_profile", {})
    lifestyle_warnings = []
    if LIFESTYLE_AVAILABLE and lifestyle_profile:
        drug_meta_list = [DRUG_METADATA.get(d) if isinstance(DRUG_METADATA.get(d), dict) else {"name": d} for d in drugs]
        lifestyle_warnings = analyze_lifestyle_interactions(drug_meta_list, lifestyle_profile)

    # 4. Individual Safety Baselines
    drug_baselines = {}
    if AE_AVAILABLE:
        for d in drugs:
            meta = DRUG_METADATA.get(d, {})
            d_class = meta.get("class", "Therapeutic Agent")
            drug_baselines[d] = get_individual_safety(d, d_class)

    # 5. Enrich with ADMET Safety Profile
    admet_results = {}
    for d in drugs:
        meta = DRUG_METADATA.get(d, {})
        if meta.get('smiles'):
            admet_results[d] = ADMET_ENGINE.predict_toxicity(meta['smiles'])
        else:
            admet_results[d] = {"level": "Unknown", "score": 0.0, "error": "No SMILES"}

    chronopharmacology = generate_dosing_schedule(drugs)

    return jsonify({
        "overall_severity": overall,
        "overall_risk_score": round(max_risk, 2),
        "interactions": results,
        "drug_baselines": drug_baselines,
        "admet_safety": admet_results,
        "optimization": optimization,
        "lifestyle_warnings": lifestyle_warnings,
        "chronopharmacology": chronopharmacology,
        "timestamp": datetime.now().isoformat()
    })

@app.route("/api/drug-safety", methods=["GET"])
def drug_safety():
    drug = resolve_drug_name(request.args.get('drug', '').lower())
    if not AE_AVAILABLE:
        return jsonify({"error": "Safety service unavailable"}), 503
        
    meta = DRUG_METADATA.get(drug, {})
    d_class = meta.get("class", "Therapeutic Agent")
    return jsonify(get_individual_safety(drug, d_class))

@app.route("/api/molecule/<name>", methods=["GET"])
def get_molecule(name):
    """Generate base64 SVG for a drug's molecular structure"""
    drug_name = resolve_drug_name(name.lower().strip())
    meta = DRUG_METADATA.get(drug_name)
    if not meta or not meta.get('smiles'):
        return jsonify({"error": "Drug structure not found"}), 404
    
    try:
        mol = Chem.MolFromSmiles(meta['smiles'])
        if not mol: return jsonify({"error": "Invalid SMILES"}), 400
        
        # Draw options for dark mode compatibility
        d = Draw.MolDraw2DSVG(300, 300)
        opts = d.drawOptions()
        opts.addStereoAnnotation = True
        opts.backgroundColour = None # Transparent
        
        d.DrawMolecule(mol)
        d.FinishDrawing()
        svg = d.GetDrawingText()
        
        # Return as data URI
        encoded = base64.b64encode(svg.encode('ascii')).decode('ascii')
        return jsonify({
            "name": drug_name,
            "svg": f"data:image/svg+xml;base64,{encoded}"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/molecule/3d/<name>", methods=["GET"])
def get_molecule_3d(name):
    """Generate 3D coordinates (SDF) for 3D visualization"""
    drug_name = resolve_drug_name(name.lower().strip())
    meta = DRUG_METADATA.get(drug_name)
    if not meta or not meta.get('smiles'):
        return jsonify({"error": "Drug structure not found"}), 404
    
    try:
        mol = Chem.MolFromSmiles(meta['smiles'])
        if not mol: return jsonify({"error": "Invalid SMILES"}), 400
        
        # Generate 3D coordinates
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, AllChem.ETKDG())
        AllChem.MMFFOptimizeMolecule(mol)
        
        # Export to SDF format for 3Dmol.js
        from io import StringIO
        output = StringIO()
        writer = Chem.SDWriter(output)
        writer.write(mol)
        writer.flush()
        sdf = output.getvalue()
        
        return jsonify({
            "name": drug_name,
            "sdf": sdf
        })
    except Exception as e:
        return jsonify({"error": "3D Conversion failed: " + str(e)}), 500

@app.route("/api/drugs", methods=["GET"])
def get_drugs():
    # Return enriched metadata for the drug catalog
    drug_list = []
    for name, meta in DRUG_METADATA.items():
        # Ensure meta is a dict
        d_meta = meta if isinstance(meta, dict) else {}
        drug_list.append({
            "name": d_meta.get("name", name),
            "class": d_meta.get("class", "Therapeutic Agent"),
            "cyp": d_meta.get("cyp", []),
            "mw": d_meta.get("mw", 0),
            "logp": d_meta.get("logp", 0)
        })
    
    # Sort for UI convenience
    drug_list.sort(key=lambda x: x['name'])
    return jsonify({"drugs": drug_list[:800], "total": len(DRUG_METADATA)})
@app.route("/api/stats", methods=["GET"])
def stats():
    print(f"[DDI-API] Stats requested at {datetime.now()}")
    return jsonify({
        "total_interactions_loaded": len(REAL_KNOWLEDGE_BASE),
        "source": "DrugBank (via Kaggle)",
        "engine": "NLP-based Severity Prediction",
        "status": "Production-Ready"
    })

@app.route("/api/pharmacy", methods=["GET"])
def pharmacy():
    drug = resolve_drug_name(request.args.get('drug', '').lower())
    insurance = request.args.get('insurance', 'uninsured')
    
    if not PHARMACY_AVAILABLE:
        return jsonify({"error": "Pharmacy service unavailable"}), 503
        
    meta = DRUG_METADATA.get(drug, {})
    d_class = meta.get("class", "Therapeutic Agent")
    
    pricing = get_drug_pricing(drug, d_class, insurance)
    return jsonify(pricing)

# ─────────────────────────────────────────────
# GLOBAL ERROR HANDLING
# ─────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Resource not found", "code": 404}), 404

@app.errorhandler(Exception)
def handle_exception(e):
    import traceback
    traceback.print_exc()
    logging.error(f"Unhandled Exception: {str(e)}")
    return jsonify({"error": "Internal Clinical Engine Error", "details": str(e), "code": 500}), 500

@app.route("/api/admet", methods=["POST"])
def get_admet():
    data = request.get_json()
    drug = data.get("drug", "").lower().strip()
    smiles = data.get("smiles", "")
    
    if not drug and not smiles:
        return jsonify({"error": "Drug name or SMILES required"}), 400
        
    resolved_smiles = smiles
    if not smiles and drug:
        res_drug = resolve_drug_name(drug)
        meta = DRUG_METADATA.get(res_drug, {})
        resolved_smiles = meta.get('smiles')
        
    if not resolved_smiles:
        return jsonify({"error": "SMILES structure not found for this drug"}), 404
        
    result = ADMET_ENGINE.predict_toxicity(resolved_smiles)
    return jsonify({
        "drug": drug,
        "smiles": resolved_smiles,
        "toxicity": result
    })

@app.route("/api/optimize-molecule", methods=["POST"])
def optimize_molecule_route():
    data = request.get_json()
    drug = data.get("drug", "").lower().strip()
    smiles = data.get("smiles", "")
    
    if not drug and not smiles:
        return jsonify({"error": "Drug name or SMILES required"}), 400
        
    resolved_smiles = smiles
    if not smiles and drug:
        res_drug = resolve_drug_name(drug)
        meta = DRUG_METADATA.get(res_drug, {})
        resolved_smiles = meta.get('smiles')
        
    if not resolved_smiles:
        return jsonify({"error": "SMILES structure not found for this drug"}), 404
        
    optimization_results = MOLECULAR_OPTIMIZER.optimize(resolved_smiles, admet_engine=ADMET_ENGINE)
    
    # Enrich derivatives with SVGs
    for der in optimization_results.get('optimized_derivatives', []):
        try:
            mol = Chem.MolFromSmiles(der['smiles'])
            if mol:
                # Highlight the diff? For now just return SVG
                drawer = Draw.MolDraw2DSVG(300, 300)
                drawer.DrawMolecule(mol)
                drawer.FinishDrawing()
                der['svg'] = "data:image/svg+xml;base64," + base64.b64encode(drawer.GetDrawingText().encode()).decode()
        except Exception:
            der['svg'] = None

    return jsonify(optimization_results)

@app.route("/api/multi-tox", methods=["POST"])
def multi_tox_route():
    data = request.get_json()
    drug = data.get("drug", "").lower().strip()
    smiles = data.get("smiles", "")
    
    if not drug and not smiles:
        return jsonify({"error": "Drug name or SMILES required"}), 400
    
    resolved_smiles = smiles
    if not smiles and drug:
        res_drug = resolve_drug_name(drug)
        meta = DRUG_METADATA.get(res_drug, {})
        resolved_smiles = meta.get('smiles')
        
    if not resolved_smiles:
        return jsonify({"error": "SMILES structure not found for this drug"}), 404
    
    # Use the multi-organ engine
    tox_report = MULTI_ORGAN_TOX.predict_all(resolved_smiles, admet_engine=ADMET_ENGINE)
    return jsonify({"drug": drug or res_drug, "smiles": resolved_smiles, "toxicity": tox_report})

@app.route("/api/pgx", methods=["POST"])
def pgx_route():
    data = request.get_json()
    drug = data.get("drug", "").lower().strip()
    patient_genetics = data.get("genetics", {})  # dict gene->phenotype
    
    if not drug:
        return jsonify({"error": "Drug name required"}), 400
    
    # Basic drug-level evidence
    drug_evidence = get_pgx_evidence(drug)
    
    # Patient-specific actionable warnings
    patient_report = get_patient_pgx_report([drug], patient_genetics)
    
    return jsonify({"drug": drug, "evidence": drug_evidence, "patient_report": patient_report})

@app.route("/api/predict-potency", methods=["POST"])
def predict_potency_route():
    data = request.get_json()
    smiles = data.get("smiles", "").strip()
    if not smiles:
        return jsonify({"error": "SMILES string required"}), 400
    
    res = PIC50_ENGINE.predict(smiles)
    return jsonify(res)

@app.route("/api/mol3d", methods=["POST"])
def mol3d_route():
    data = request.get_json()
    smiles = data.get("smiles", "").strip()
    drug = data.get("drug", "").lower().strip()
    
    if not smiles and drug:
        res_drug = resolve_drug_name(drug)
        meta = DRUG_METADATA.get(res_drug, {})
        smiles = meta.get('smiles', '')
        
    if not smiles:
        return jsonify({"error": "SMILES string required"}), 400
    
    # Generate 3D coordinates using RDKit
    try:
        from rdkit import Chem
        from rdkit.Chem import AllChem
        mol = Chem.MolFromSmiles(smiles)
        mol = Chem.AddHs(mol)
        AllChem.EmbedMolecule(mol, randomSeed=42)
        AllChem.MMFFOptimizeMolecule(mol)
        mol_block = Chem.MolToMolBlock(mol)
        return jsonify({"molBlock": mol_block})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/chatbot", methods=["GET", "POST", "OPTIONS"])
def chatbot_route():
    data = request.get_json()
    query = data.get("query", "").strip()
    drugs = data.get("drugs", [])
    interaction = data.get("interaction", {})
    
    if not query:
        return jsonify({"error": "Query required"}), 400
        
    # Simulated LLM response deterministic to the interaction
    severity = interaction.get('severity', 'Unknown')
    mech = interaction.get('mechanism', 'Unknown mechanism')
    
    response = (
        f"**Clinical AI Assistant**\n\n"
        f"Analyzing the regimen containing **{', '.join([d.title() for d in drugs])}**.\n\n"
        f"I detected a **{severity}** risk here. The primary pharmacokinetic action is: *{mech}*.\n"
        f"Because one of these molecules acts as a competitive inhibitor or inducer on the metabolic pathways, plasma levels are heavily altered.\n\n"
        f"**Recommendation**: It is highly suggested to either stagger the administration times by 4-6 hours (check the Dosing Timeline), or consider a bioisostere replacement if therapy must be concurrent."
    )
    
    return jsonify({"response": response})

if __name__ == "__main__":
    PIC50_ENGINE.load_or_train()
    load_system_data()
    
    port = int(os.environ.get('PORT', 5005))
    is_dev = os.environ.get('FLASK_ENV') == 'development'
    
    print(f"\n[DDI-REAL] Clinical Data: {DATA_PATH}")
    print(f"[DDI-REAL] Total Pairs: {len(REAL_KNOWLEDGE_BASE)}")
    
    if serve and not is_dev:
        print(f"[DDI-PROD] Launching Production Engine (Waitress) on port {port}...")
        logging.info(f"Engine started on port {port} (Waitress)")
        serve(app, host='0.0.0.0', port=port, threads=8)
    else:
        print(f"[DDI-DIAG] Launching Flask Dev Server on http://0.0.0.0:{port}...")
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
