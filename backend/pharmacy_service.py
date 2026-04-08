import random
import logging

logger = logging.getLogger(__name__)

# Specialized Class-based Pricing Categories
# (Mock values reflecting real-world US retail/GoodRx averages)
SPECIALTY_CLASSES = ["Biologic", "Monoclonal Antibody", "Antiretroviral", "Chemotherapy"]
BRAND_ONLY_CLASSES = ["SGLT2 Inhibitor", "DOAC", "PCSK9 Inhibitor", "IL-17 Antagonist"]
COMMON_GENERICS = ["NSAID", "Statin", "Antidiabetic", "ACE Inhibitor", "Diuretic", "Beta-Blocker"]

def get_drug_pricing(drug_name, drug_class="Therapeutic Agent", insurance_type="uninsured"):
    """
    Estimates Pharmacy Pricing and local availability for a given drug.
    """
    name = drug_name.lower()
    d_class = drug_class
    
    # Base Price logic
    if any(s in d_class for s in SPECIALTY_CLASSES):
        base_retail = random.uniform(2500, 8000)
        tier = "Tier 4 (Specialty)"
    elif any(b in d_class for b in BRAND_ONLY_CLASSES) or name in ["apixaban", "eliquis", "rivaroxaban", "xarelto"]:
        base_retail = random.uniform(450, 750)
        tier = "Tier 3 (Preferred Brand)"
    elif d_class in COMMON_GENERICS:
        base_retail = random.uniform(10, 45)
        tier = "Tier 1 (Preferred Generic)"
    else:
        base_retail = random.uniform(50, 150)
        tier = "Tier 2 (Non-Preferred)"

    # Insurance adjustment (Simulated Copay)
    copay_multiplier = {
        "uninsured": 1.0,         # Full price
        "private_ppo": 0.15,      # 15% copay
        "medicare": 0.25,         # 25% copay (before donut hole)
        "high_deductible": 0.8    # 80% until deductible reached
    }
    
    insurance_name = insurance_type.replace("_", " ").title()
    est_copay = base_retail * copay_multiplier.get(insurance_type, 1.0)
    
    # Pharmacy Local Discounts (Simulated GoodRx-style rows)
    pharmacies = [
        {"name": "CVS Pharmacy", "discount": random.uniform(0.7, 0.95)},
        {"name": "Walgreens", "discount": random.uniform(0.75, 0.98)},
        {"name": "Walmart", "discount": random.uniform(0.6, 0.85)},
        {"name": "Costco", "discount": random.uniform(0.55, 0.8)}
    ]

    pharmacy_prices = []
    for phar in pharmacies:
        pharmacy_prices.append({
            "pharmacy": phar["name"],
            "retail": round(base_retail, 2),
            "discount_price": round(base_retail * phar["discount"], 2),
            "availability": "In Stock" if random.random() > 0.1 else "Limited Stock"
        })

    return {
        "drug": drug_name,
        "tier": tier,
        "insurance_plan": insurance_name,
        "est_patient_copay": round(est_copay, 2),
        "retail_avg": round(base_retail, 2),
        "pharmacy_rows": pharmacy_prices,
        "savings_alert": "High Generic Availability" if d_class in COMMON_GENERICS else "Specialty Patient Assistance Available" if "Specialty" in tier else None
    }
