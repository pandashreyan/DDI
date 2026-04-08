"""
Chronopharmacology & Time-of-Day Dosing Engine
Maps drugs to typical half-life and absorption parameters and generates a safe
spaced timeline (e.g. Morning, Mid-day, Evening, Bedtime) to minimize pharmacokinetic 
collisions.
"""

import json

# Simulated Pharmacokinetic/Half-life database
CHRONO_DB = {
    "aspirin": {"half_life_hr": 0.25, "active_meta_hr": 2.0, "time_preference": "morning", "fasting": False},
    "warfarin": {"half_life_hr": 40.0, "active_meta_hr": 40.0, "time_preference": "evening", "fasting": False},
    "levothyroxine": {"half_life_hr": 168.0, "active_meta_hr": 168.0, "time_preference": "morning", "fasting": True},
    "simvastatin": {"half_life_hr": 3.0, "active_meta_hr": 3.0, "time_preference": "bedtime", "fasting": False},
    "atorvastatin": {"half_life_hr": 14.0, "active_meta_hr": 14.0, "time_preference": "any", "fasting": False},
    "omeprazole": {"half_life_hr": 1.0, "active_meta_hr": 1.0, "time_preference": "morning", "fasting": True},
    "ibuprofen": {"half_life_hr": 2.0, "active_meta_hr": 2.0, "time_preference": "any", "fasting": False},
    "fluoxetine": {"half_life_hr": 96.0, "active_meta_hr": 240.0, "time_preference": "morning", "fasting": False},
    "diazepam": {"half_life_hr": 48.0, "active_meta_hr": 100.0, "time_preference": "bedtime", "fasting": False},
}

DEFAULT_CHRONO = {"half_life_hr": 12.0, "active_meta_hr": 12.0, "time_preference": "any", "fasting": False}

def generate_dosing_schedule(drugs):
    """
    Given a list of drug names, build a recommended time-of-day timeline
    to avoid absorption clashes and align with chronobiological efficacy.
    """
    schedule = {
        "08:00 AM": [],
        "12:00 PM": [],
        "06:00 PM": [],
        "10:00 PM": ([], "Bedtime")
    }
    
    warnings = []
    mapped_drugs = []
    
    for drug in drugs:
        d = drug.lower().strip()
        meta = CHRONO_DB.get(d, DEFAULT_CHRONO)
        
        pref = meta["time_preference"]
        fasting = meta["fasting"]
        
        if fasting:
            schedule["08:00 AM"].append(f"{drug.capitalize()} (Take on empty stomach, 30 min before meal)")
            if d == "levothyroxine":
                warnings.append("Levothyroxine is highly sensitive to absorption interference. Do not take within 4 hours of calcium/iron supplements.")
        elif pref == "morning":
            schedule["08:00 AM"].append(f"{drug.capitalize()}")
        elif pref == "bedtime":
            schedule["10:00 PM"][0].append(f"{drug.capitalize()} (Enhances nighttime efficacy / reduces daytime sedation)")
            if "statin" in d:
                warnings.append(f"{drug.capitalize()} cholesterol synthesis peaks at night. Bedtime dosing recommended.")
        elif pref == "evening":
            schedule["06:00 PM"].append(f"{drug.capitalize()}")
        else:
            # "Any" -> default to Mid-day or Morning to space from Warfarin/Statins
            schedule["12:00 PM"].append(f"{drug.capitalize()}")
            
    # Compile final structure for UI rendering
    timeline = []
    if schedule["08:00 AM"]:
        timeline.append({"time": "Morning (08:00 AM)", "drugs": schedule["08:00 AM"], "icon": "🌅"})
    if schedule["12:00 PM"]:
        timeline.append({"time": "Mid-Day (12:00 PM)", "drugs": schedule["12:00 PM"], "icon": "☀️"})
    if schedule["06:00 PM"]:
        timeline.append({"time": "Evening (06:00 PM)", "drugs": schedule["06:00 PM"], "icon": "🌇"})
    if schedule["10:00 PM"][0]:
        timeline.append({"time": "Bedtime (10:00 PM)", "drugs": schedule["10:00 PM"][0], "icon": "🌙"})
        
    return {
        "timeline": timeline,
        "chronotherapy_alerts": warnings
    }
