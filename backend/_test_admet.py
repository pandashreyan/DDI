import requests
import json

def test_admet_point():
    print("\n--- TEST: ADMET Point Prediction ---")
    url = "http://localhost:5005/api/admet"
    payload = {"drug": "aspirin"}
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        print(json.dumps(data, indent=2))
        if 'toxicity' in data:
            print("[PASS] ADMET point prediction success.")
    except Exception as e:
        print(f"[ERROR] {e}")

def test_integrated_predict():
    print("\n--- TEST: Integrated Prediction with ADMET ---")
    url = "http://localhost:5005/api/predict"
    payload = {
        "drugs": ["Warfarin", "Ibuprofen"],
        "patient_profile": {}
    }
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        if 'admet_safety' in data:
            print("[PASS] ADMET safety payload found in predict response.")
            print(f"Drugs covered: {list(data['admet_safety'].keys())}")
            print(json.dumps(data['admet_safety'], indent=2))
        else:
            print("[FAIL] ADMET safety payload missing.")
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    test_admet_point()
    test_integrated_predict()
