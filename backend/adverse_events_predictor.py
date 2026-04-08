"""
Adverse Event Predictor for Drug-Drug Interactions
Predicts specific side effects and adverse events from drug combinations
"""

import json
from typing import List, Dict, Tuple

# Adverse Events Knowledge Base
# Maps interaction characteristics to predicted adverse events with probabilities
ADVERSE_EVENTS_DB = {
    # Serotonin-Related Adverse Events
    "serotonin_syndrome": {
        "name": "Serotonin Syndrome",
        "severity": "critical",
        "symptoms": ["agitation", "confusion", "rapid heart rate", "muscle rigidity", "fever"],
        "triggers": ["SSRI", "MAOI", "Opioid", "Stimulant"],
        "base_probability": 0.35
    },
    
    # Bleeding/Anticoagulation Events
    "bleeding_risk": {
        "name": "Increased Bleeding Risk",
        "severity": "high",
        "symptoms": ["easy bruising", "nosebleeds", "GI bleeding", "heavy menstrual bleeding"],
        "triggers": ["Anticoagulant", "Antiplatelet", "NSAID"],
        "base_probability": 0.45
    },
    
    # Respiratory Events
    "respiratory_depression": {
        "name": "Respiratory Depression",
        "severity": "critical",
        "symptoms": ["shallow breathing", "drowsiness", "difficulty breathing"],
        "triggers": ["Opioid", "SSRI", "Benzodiazepine"],
        "base_probability": 0.30
    },
    
    # Cardiovascular Events
    "qT_prolongation": {
        "name": "QT Prolongation",
        "severity": "high",
        "symptoms": ["palpitations", "syncope", "arrhythmia"],
        "triggers": ["Antiarrhythmic", "Antiviral", "Fluoroquinolone"],
        "base_probability": 0.25
    },
    
    "hypotension": {
        "name": "Severe Hypotension",
        "severity": "high",
        "symptoms": ["dizziness", "fainting", "weakness", "shock"],
        "triggers": ["ACE Inhibitor", "Beta-blocker", "Calcium Channel Blocker"],
        "base_probability": 0.28
    },
    
    # Metabolic Events
    "statin_myopathy": {
        "name": "Statin-Induced Myopathy",
        "severity": "high",
        "symptoms": ["muscle pain", "weakness", "dark urine", "kidney damage"],
        "triggers": ["Statin", "Antiviral", "Antifungal"],
        "base_probability": 0.40
    },
    
    # GI Events
    "GI_bleeding": {
        "name": "Gastrointestinal Bleeding",
        "severity": "critical",
        "symptoms": ["black stools", "vomiting blood", "abdominal pain"],
        "triggers": ["NSAID", "Anticoagulant", "Antiplatelet"],
        "base_probability": 0.35
    },
    
    # CNS Events
    "seizures": {
        "name": "Increased Seizure Risk",
        "severity": "critical",
        "symptoms": ["convulsions", "altered consciousness"],
        "triggers": ["Anticonvulsant", "Antidepressant", "Stimulant"],
        "base_probability": 0.22
    },
    
    # Hepatotoxicity
    "hepatotoxicity": {
        "name": "Liver Toxicity (Hepatotoxicity)",
        "severity": "high",
        "symptoms": ["jaundice", "dark urine", "abdominal pain", "nausea"],
        "triggers": ["Statin", "Antifungal", "Anticonvulsant"],
        "base_probability": 0.25
    },
    
    # Nephrotoxicity
    "nephrotoxicity": {
        "name": "Kidney Toxicity (Nephrotoxicity)",
        "severity": "high",
        "symptoms": ["elevated creatinine", "reduced urine output", "edema"],
        "triggers": ["Antibiotic", "NSAID", "ACE Inhibitor"],
        "base_probability": 0.20
    },
    
    # Insulin/Diabetes Events
    "hypoglycemia": {
        "name": "Severe Hypoglycemia",
        "severity": "critical",
        "symptoms": ["confusion", "sweating", "tremor", "loss of consciousness"],
        "triggers": ["Antidiabetic", "Beta-blocker", "Salicylate"],
        "base_probability": 0.28
    },
    
    # Photosensitivity
    "photosensitivity": {
        "name": "Photosensitivity Reaction",
        "severity": "moderate",
        "symptoms": ["severe sunburn", "skin blistering", "rash"],
        "triggers": ["Fluoroquinolone", "NSAID", "Tetracycline"],
        "base_probability": 0.18
    },
}

# CYP Enzyme-Related Adverse Events
CYP_ADVERSE_EVENTS = {
    "CYP3A4": {
        "primary": "statin_myopathy",
        "secondary": ["hepatotoxicity", "nephrotoxicity"],
        "mechanism": "Competitive substrate inhibition leading to drug accumulation"
    },
    "CYP2D6": {
        "primary": "serotonin_syndrome",
        "secondary": ["hypotension", "respiratory_depression"],
        "mechanism": "Impaired metabolism of serotonergic/cardioactive drugs"
    },
    "CYP2C9": {
        "primary": "bleeding_risk",
        "secondary": ["GI_bleeding"],
        "mechanism": "Enhanced anticoagulant effect through impaired metabolism"
    }
}

# Individual Drug Baseline Safety Profiles (Therapeutic Class Based)
GENERAL_SIDE_EFFECTS = {
    "SSRI": {
        "common": ["Nausea", "Insomnia", "Anxiety", "Sexual Dysfunction", "Dry Mouth"],
        "serious": ["Suicidal Ideation (Children/Young Adults)", "Serotonin Syndrome", "Seizures"],
        "management": "Take in the morning if insomnia occurs. Do not stop abruptly."
    },
    "SNRI": {
        "common": ["Nausea", "Dizziness", "Excessive Sweating", "Increased Blood Pressure"],
        "serious": ["Hypertension", "Liver Toxicity", "Hemorrhage Risk"],
        "management": "Monitor blood pressure regularly."
    },
    "Statin": {
        "common": ["Muscle Aches (Myalgia)", "Headache", "Digestive Upset"],
        "serious": ["Rhabdomyolysis", "Liver Enzyme Elevation", "Increased Blood Sugar"],
        "management": "Avoid large amounts of grapefruit juice. Report unexplained muscle pain."
    },
    "NSAID": {
        "common": ["Stomach Upset", "Heartburn", "Dizziness"],
        "serious": ["GI Bleeding", "Kidney Dysfunction", "Increased Stroke/MI Risk"],
        "management": "Take with food to minimize stomach irritation."
    },
    "Anticoagulant": {
        "common": ["Easy Bruising", "Minor Prolonged Bleeding"],
        "serious": ["Major Internal Bleeding", "Stroke", "Compartment Syndrome"],
        "management": "Avoid risky activities. Monitor for black/tarry stools."
    },
    "Opioid": {
        "common": ["Constipation", "Drowsiness", "Nausea", "Itching"],
        "serious": ["Respiratory Depression", "Addiction", "Severe Hypotension"],
        "management": "Avoid alcohol. Increase fiber intake for constipation."
    },
    "Benzodiazepine": {
        "common": ["Drowsiness", "Fatigue", "Coordination Issues"],
        "serious": ["Severe Respiratory Depression (especially with alcohol)", "Dependence", "Memory Loss"],
        "management": "Do not drive until you know how this medication affects you."
    },
    "ACE Inhibitor": {
        "common": ["Dry Cough", "Dizziness", "Headache"],
        "serious": ["Angioedema (Swelling of face/throat)", "Hyperkalemia", "Renal Failure"],
        "management": "Avoid potassium supplements unless directed."
    },
    "Beta-blocker": {
        "common": ["Cold Hands/Feet", "Fatigue", "Weight Gain"],
        "serious": ["Bradycardia", "Severe Wheezing/Bronchospasm", "Heart Failure Exacerbation"],
        "management": "Do not stop suddenly, as this can cause rebound hypertension."
    },
    "Antidiabetic": {
        "common": ["GI Distress (Metformin)", "Mild Weight Loss"],
        "serious": ["Hypoglycemia (Sulfonylureas/Insulin)", "Lactic Acidosis (Metformin)", "Ketoacidosis"],
        "management": "Ensure regular meals to prevent low blood sugar."
    }
}

class AdverseEventPredictor:
    def __init__(self, drug_metadata: Dict = None, interaction_db: Dict = None):
        """
        Initialize the adverse event predictor
        
        Args:
            drug_metadata: Dictionary of drug properties
            interaction_db: Dictionary of known interactions
        """
        self.drug_metadata = drug_metadata or {}
        self.interaction_db = interaction_db or {}
    
    def predict_adverse_events(self, drug_a: str, drug_b: str, risk_score: float = None) -> List[Dict]:
        """
        Predict adverse events for a drug pair
        
        Args:
            drug_a: First drug name
            drug_b: Second drug name
            risk_score: Overall interaction risk score (0-1)
        
        Returns:
            List of predicted adverse events with probabilities and severity
        """
        drug_a = drug_a.lower().strip()
        drug_b = drug_b.lower().strip()
        
        event_scores = {}
        
        # Get drug classes and properties
        meta_a = self.drug_metadata.get(drug_a, {})
        meta_b = self.drug_metadata.get(drug_b, {})
        
        class_a = meta_a.get('class', '').lower()
        class_b = meta_b.get('class', '').lower()
        cyp_a = set(meta_a.get('cyp', []))
        cyp_b = set(meta_b.get('cyp', []))
        
        # Rule 1: Check drug class combinations for specific adverse events
        if class_a or class_b:  # Only if we have class info
            self._get_class_based_events(class_a, class_b, event_scores)
        
        # Rule 1b: Check drug name patterns for common interactions
        self._get_name_based_events(drug_a, drug_b, event_scores)
        
        # Rule 2: Check CYP enzyme overlaps
        if cyp_overlap := cyp_a.intersection(cyp_b):
            self._get_cyp_based_events(cyp_overlap, event_scores)
        
        # Rule 3: Score modulation based on interaction risk
        if risk_score:
            event_scores = self._modulate_by_risk(event_scores, risk_score)
        
        # Rule 4: Parameter-based adjustments
        if meta_a or meta_b:
            self._adjust_by_parameters(event_scores, meta_a, meta_b)
        
        # Convert scores to event list
        predicted_events = self._convert_scores_to_events(event_scores)
        
        return predicted_events[:5]  # Return top 5 events
    
    def _get_name_based_events(self, drug_a: str, drug_b: str, event_scores: Dict) -> None:
        """Predict events based on drug name patterns"""
        
        # Fluoroquinolones (e.g., ciprofloxacin, levofloxacin, gatifloxacin)
        if ("fluoroquinolone" in drug_a or "floxacin" in drug_a or drug_a in ["gatifloxacin", "levofloxacin", "ciprofloxacin", "moxifloxacin"]) or \
           ("fluoroquinolone" in drug_b or "floxacin" in drug_b or drug_b in ["gatifloxacin", "levofloxacin", "ciprofloxacin", "moxifloxacin"]):
            
            # Fluoroquinolone + Anticoagulant
            if "warfarin" in drug_a or "warfarin" in drug_b:
                event_scores["bleeding_risk"] = event_scores.get("bleeding_risk", 0) + 0.50
                event_scores["GI_bleeding"] = event_scores.get("GI_bleeding", 0) + 0.40
                event_scores["qT_prolongation"] = event_scores.get("qT_prolongation", 0) + 0.28
                event_scores["photosensitivity"] = event_scores.get("photosensitivity", 0) + 0.22
        
        # Opioids + SSRIs
        if ("opioid" in drug_a or drug_a in ["codeine", "morphine", "tramadol"]) or \
           ("opioid" in drug_b or drug_b in ["codeine", "morphine", "tramadol"]):
            if ("ssri" in drug_a or "fluoxetine" in drug_a or "sertraline" in drug_a or "escitalopram" in drug_a) or \
               ("ssri" in drug_b or "fluoxetine" in drug_b or "sertraline" in drug_b or "escitalopram" in drug_b):
                event_scores["serotonin_syndrome"] = event_scores.get("serotonin_syndrome", 0) + 0.48
                event_scores["respiratory_depression"] = event_scores.get("respiratory_depression", 0) + 0.42
        
        # Statins + Strong CYP3A4 Inhibitors (e.g., ritonavir)
        if ("statin" in drug_a or "simvastatin" in drug_a or "atorvastatin" in drug_a) or \
           ("statin" in drug_b or "simvastatin" in drug_b or "atorvastatin" in drug_b):
            if "ritonavir" in drug_a or "ritonavir" in drug_b:
                event_scores["statin_myopathy"] = event_scores.get("statin_myopathy", 0) + 0.65
                event_scores["hepatotoxicity"] = event_scores.get("hepatotoxicity", 0) + 0.40
        
        # NSAIDs + Anticoagulants
        if ("nsaid" in drug_a or "ibuprofen" in drug_a or "aspirin" in drug_a) or \
           ("nsaid" in drug_b or "ibuprofen" in drug_b or "aspirin" in drug_b):
            if "warfarin" in drug_a or "warfarin" in drug_b:
                event_scores["bleeding_risk"] = event_scores.get("bleeding_risk", 0) + 0.58
                event_scores["GI_bleeding"] = event_scores.get("GI_bleeding", 0) + 0.48
    
    def _get_class_based_events(self, class_a: str, class_b: str, event_scores: Dict) -> None:
        """Predict events based on drug class combinations"""
        
        # SSRIs/SNRIs with Opioids -> Serotonin Syndrome
        if self._class_match(class_a, class_b, ["ssri", "snri"], ["opioid"]):
            event_scores["serotonin_syndrome"] = event_scores.get("serotonin_syndrome", 0) + 0.45
            event_scores["respiratory_depression"] = event_scores.get("respiratory_depression", 0) + 0.38
        
        # Anticoagulants with NSAIDs -> Bleeding Risk
        if self._class_match(class_a, class_b, ["anticoagulant"], ["nsaid", "antiplatelet"]):
            event_scores["bleeding_risk"] = event_scores.get("bleeding_risk", 0) + 0.55
            event_scores["GI_bleeding"] = event_scores.get("GI_bleeding", 0) + 0.42
        
        # Statins with CYP3A4 Inhibitors -> Myopathy
        if self._class_match(class_a, class_b, ["statin"], ["antiviral", "antifungal"]):
            event_scores["statin_myopathy"] = event_scores.get("statin_myopathy", 0) + 0.60
            event_scores["hepatotoxicity"] = event_scores.get("hepatotoxicity", 0) + 0.35
        
        # Beta-blockers with ACE Inhibitors -> Hypotension
        if self._class_match(class_a, class_b, ["beta-blocker"], ["ace inhibitor"]):
            event_scores["hypotension"] = event_scores.get("hypotension", 0) + 0.42
        
        # Fluoroquinolones with Anticoagulants -> Bleeding + QT
        if self._class_match(class_a, class_b, ["fluoroquinolone"], ["anticoagulant"]):
            event_scores["bleeding_risk"] = event_scores.get("bleeding_risk", 0) + 0.48
            event_scores["qT_prolongation"] = event_scores.get("qT_prolongation", 0) + 0.30
            event_scores["photosensitivity"] = event_scores.get("photosensitivity", 0) + 0.25
        
        # Antidiabetics + NSAIDs -> Hypoglycemia + Nephro
        if self._class_match(class_a, class_b, ["antidiabetic"], ["nsaid"]):
            event_scores["hypoglycemia"] = event_scores.get("hypoglycemia", 0) + 0.38
            event_scores["nephrotoxicity"] = event_scores.get("nephrotoxicity", 0) + 0.35
        
        # Benzodiazepines + Opioids -> Respiratory
        if self._class_match(class_a, class_b, ["benzodiazepine"], ["opioid"]):
            event_scores["respiratory_depression"] = event_scores.get("respiratory_depression", 0) + 0.52
    
    def _get_cyp_based_events(self, cyp_overlap: set, event_scores: Dict) -> None:
        """Predict events based on CYP enzyme overlaps"""
        
        for cyp in cyp_overlap:
            if cyp in CYP_ADVERSE_EVENTS:
                cyp_info = CYP_ADVERSE_EVENTS[cyp]
                primary = cyp_info["primary"]
                secondaries = cyp_info["secondary"]
                
                # Higher probability for primary event
                event_scores[primary] = event_scores.get(primary, 0) + 0.25
                
                # Lower probability for secondary events
                for secondary in secondaries:
                    event_scores[secondary] = event_scores.get(secondary, 0) + 0.12
    
    def _modulate_by_risk(self, event_scores: Dict, risk_score: float) -> Dict:
        """Scale event probabilities by overall interaction risk"""
        modulation_factor = min(1.0, risk_score * 1.5)  # Scale up to 150% for high risk
        
        return {
            event: min(0.95, score * modulation_factor)
            for event, score in event_scores.items()
        }
    
    def _adjust_by_parameters(self, event_scores: Dict, meta_a: Dict, meta_b: Dict) -> None:
        """Adjust predictions based on molecular properties"""
        
        logp_a = meta_a.get('logp', 0)
        logp_b = meta_b.get('logp', 0)
        mw_a = meta_a.get('mw', 0)
        mw_b = meta_b.get('mw', 0)
        
        # Highly lipophilic drugs (high logp) increase CNS/organ toxicity risk
        if logp_a > 3.5 or logp_b > 3.5:
            event_scores["hepatotoxicity"] = event_scores.get("hepatotoxicity", 0) + 0.15
            event_scores["nephrotoxicity"] = event_scores.get("nephrotoxicity", 0) + 0.10
        
        # Large molecular weight drugs increase accumulation risk
        if mw_a > 400 or mw_b > 400:
            event_scores["statin_myopathy"] = event_scores.get("statin_myopathy", 0) + 0.10
            event_scores["hepatotoxicity"] = event_scores.get("hepatotoxicity", 0) + 0.10
    
    def _class_match(self, class_a: str, class_b: str, classes_group1: List, classes_group2: List) -> bool:
        """Check if classes match expected combination"""
        match_a = any(c in class_a for c in classes_group1)
        match_b = any(c in class_b for c in classes_group2)
        match_b_reversed = any(c in class_b for c in classes_group1) and any(c in class_a for c in classes_group2)
        
        return (match_a and match_b) or match_b_reversed
    
    def _convert_scores_to_events(self, event_scores: Dict) -> List[Dict]:
        """Convert event scores to structured event list"""
        
        events = []
        for event_id, score in event_scores.items():
            if score > 0.10 and event_id in ADVERSE_EVENTS_DB:  # Filter out very low probabilities
                event_info = ADVERSE_EVENTS_DB[event_id]
                events.append({
                    "event_id": event_id,
                    "event_name": event_info["name"],
                    "probability": round(min(0.99, score), 2),
                    "severity": event_info["severity"],
                    "symptoms": event_info["symptoms"],
                    "risk_level": self._probability_to_risk_level(score)
                })
        
        # Sort by probability (descending)
        events.sort(key=lambda x: x["probability"], reverse=True)
        return events
    
    @staticmethod
    def _probability_to_risk_level(probability: float) -> str:
        """Convert probability to risk level"""
        if probability >= 0.60:
            return "very_high"
        elif probability >= 0.40:
            return "high"
        elif probability >= 0.20:
            return "moderate"
        else:
            return "low"


# Initialize global predictor
adverse_event_predictor = None

def init_adverse_event_predictor(drug_metadata: Dict, interaction_db: Dict):
    """Initialize the global adverse event predictor"""
    global adverse_event_predictor
    adverse_event_predictor = AdverseEventPredictor(drug_metadata, interaction_db)

def get_adverse_events(drug_a: str, drug_b: str, risk_score: float = None) -> List[Dict]:
    """Get predicted adverse events for a drug pair"""
    if adverse_event_predictor:
        return adverse_event_predictor.predict_adverse_events(drug_a, drug_b, risk_score)
    return []

def get_individual_safety(drug_name: str, drug_class: str = None) -> Dict:
    """Gets the baseline safety profile for an individual drug"""
    name = drug_name.lower().strip()
    d_class = drug_class or "Therapeutic Agent"
    
    # Check for direct class match
    profile = None
    for key in GENERAL_SIDE_EFFECTS:
        if key.lower() in d_class.lower():
            profile = GENERAL_SIDE_EFFECTS[key]
            break
            
    if not profile:
        return {
            "name": drug_name.title(),
            "class": d_class,
            "common": ["No specific data for this class. Consult pharmacist."],
            "serious": ["Hypersensitivity/Allergy"],
            "management": "Take exactly as prescribed."
        }
        
    return {
        "name": drug_name.title(),
        "class": d_class,
        "common": profile["common"],
        "serious": profile["serious"],
        "management": profile["management"]
    }
