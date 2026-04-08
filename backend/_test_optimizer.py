import requests
import json

def test_molecular_optimization():
    print("\n--- TEST: Generative Molecular Optimization ---")
    url = "http://localhost:5005/api/optimize-molecule"
    # Ibuprofen is a good test case (Medium toxicity 0.51)
    payload = {"drug": "ibuprofen"}
    try:
        response = requests.post(url, json=payload)
        data = response.json()
        print(f"Status: {response.status_code}")
        if 'optimized_derivatives' in data:
            print(f"[PASS] Optimizer returned {len(data['optimized_derivatives'])} derivatives.")
            for i, der in enumerate(data['optimized_derivatives']):
                print(f"\nDerivative {i+1}: {der['name']}")
                print(f"Logic: {der['description']}")
                print(f"Improvement Score: {der['safety']['improvement_score']}")
                # print(f"SMILES: {der['smiles']}")
                if 'svg' in der and der['svg']:
                    print("[PASS] Molecule SVG generated.")
        else:
            print("[FAIL] No optimization results found.")
            print(json.dumps(data, indent=2))
    except Exception as e:
        print(f"[ERROR] {e}")

if __name__ == "__main__":
    test_molecular_optimization()
