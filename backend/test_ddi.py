"""
Comprehensive End-to-End Test for DDI System
"""
import requests
import json

BASE_URL = "http://127.0.0.1:5000/api"

def run_tests():
    print("[TEST] Starting DDI Backend Tests...")
    
    # 1. Health
    try:
        r = requests.get(f"{BASE_URL}/health")
        print(f"1. Health Check: {r.status_code} | DB Size: {r.json().get('db_size', 0)}")
    except Exception as e:
        print(f"❌ Health Failed: {e}")

    # 2. Stats
    try:
        r = requests.get(f"{BASE_URL}/stats")
        print(f"2. System Stats: {r.status_code} | Total Pairs: {r.json().get('total_interactions_loaded', 0)}")
    except Exception as e:
        print(f"❌ Stats Failed: {e}")

    # 3. Drugs
    try:
        r = requests.get(f"{BASE_URL}/drugs")
        print(f"3. Drugs List sample size: {len(r.json().get('drugs', []))}")
    except Exception as e:
        print(f"❌ Drugs Failed: {e}")

    # 4. Known Positive Interaction
    try:
        r = requests.post(f"{BASE_URL}/predict", json={"drugs": ["trioxsalen", "verteporfin"]})
        inter = r.json().get('interactions', [{}])[0]
        print(f"4. Match trioxsalen+verteporfin: {r.status_code}")
        print(f"   - Desc: {inter.get('mechanism')[:50]}...")
        print(f"   - Severity: {inter.get('severity')}")
    except Exception as e:
        print(f"❌ Prediction Positive Failed: {e}")

    # 5. Unknown Negative Interaction
    try:
        r = requests.post(f"{BASE_URL}/predict", json={"drugs": ["trioxsalen", "metformin"]})
        inter = r.json().get('interactions', [{}])[0]
        print(f"5. Match trioxsalen+metformin: {r.status_code} | Severity: {inter.get('severity')}")
    except Exception as e:
        print(f"❌ Prediction Negative Failed: {e}")

if __name__ == "__main__":
    run_tests()
