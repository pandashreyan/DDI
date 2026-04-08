import requests
import json
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cache to avoid hitting external APIs too frequently
EVIDENCE_CACHE = {}

def get_combined_evidence(drug_a, drug_b):
    """
    Orchestrates fetching FDA warnings and PubMed clinical trials.
    """
    pair_id = "-".join(sorted([drug_a.lower().strip(), drug_b.lower().strip()]))
    if pair_id in EVIDENCE_CACHE:
        return EVIDENCE_CACHE[pair_id]

    logger.info(f"Fetching clinical evidence for {drug_a} + {drug_b}")
    
    # 1. Fetch FDA Boxed Warnings for both drugs
    fda_a = fetch_fda_warnings(drug_a)
    fda_b = fetch_fda_warnings(drug_b)
    
    # 2. Fetch PubMed Clinical Trials for the pair
    pubmed_trials = fetch_pubmed_trials(drug_a, drug_b)
    
    # 3. Global Regulation Mock (FDA vs EMA)
    # In a real app, this would query a regulatory database.
    # Here we add a status indicator.
    reg_status = {
        "fda": "Approved" if fda_a or fda_b else "Verified",
        "ema": "Centralized Authorization",
        "diff_flag": False # Set true if we detect a rating discrepancy
    }

    result = {
        "drug_a_warning": fda_a,
        "drug_b_warning": fda_b,
        "pubmed_trials": pubmed_trials,
        "regulatory_sync": reg_status,
        "timestamp": datetime.now().isoformat()
    }
    
    EVIDENCE_CACHE[pair_id] = result
    return result

def fetch_fda_warnings(drug_name):
    """
    Queries OpenFDA for Boxed Warnings.
    """
    try:
        # Search by generic name or brand name
        url = f"https://api.fda.gov/drug/label.json?search=(openfda.generic_name:\"{drug_name}\"+OR+openfda.brand_name:\"{drug_name}\")+AND+_exists_:boxed_warning&limit=1"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            if "results" in data and len(data["results"]) > 0:
                warning_text = data["results"][0].get("boxed_warning", [])
                return warning_text[0] if isinstance(warning_text, list) else str(warning_text)
    except Exception as e:
        logger.error(f"FDA API Error for {drug_name}: {e}")
    return None

def fetch_pubmed_trials(drug_a, drug_b):
    """
    Queries PubMed for Clinical Trials involving the drug interaction.
    """
    try:
        # Step 1: Search for IDs
        search_query = f"({drug_a}[Title/Abstract] AND {drug_b}[Title/Abstract] AND \"interaction\"[Title/Abstract])"
        search_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={search_query}&retmode=json&retmax=3"
        
        search_res = requests.get(search_url, timeout=5)
        if search_res.status_code != 200:
            return []
            
        ids = search_res.json().get("esearchresult", {}).get("idlist", [])
        if not ids:
            return []
            
        # Step 2: Fetch summaries for those IDs
        summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={','.join(ids)}&retmode=json"
        summary_res = requests.get(summary_url, timeout=5)
        
        if summary_res.status_code == 200:
            sum_data = summary_res.json().get("result", {})
            trials = []
            for uid in ids:
                article = sum_data.get(uid, {})
                if article:
                    trials.append({
                        "id": uid,
                        "title": article.get("title"),
                        "source": article.get("source"),
                        "pubdate": article.get("pubdate"),
                        "url": f"https://pubmed.ncbi.nlm.nih.gov/{uid}/"
                    })
            return trials
    except Exception as e:
        logger.error(f"PubMed API Error for {drug_a}+{drug_b}: {e}")
    return []

if __name__ == "__main__":
    # Test call
    res = get_combined_evidence("aspirin", "warfarin")
    print(json.dumps(res, indent=2))
