from app import get_drug_alternatives, AE_AVAILABLE, DRUG_METADATA
import json

print(f"AE_AVAILABLE: {AE_AVAILABLE}")
res = get_drug_alternatives("simvastatin", "ritonavir", 3)
print("Result:")
print(json.dumps(res, indent=2))
