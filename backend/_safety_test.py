import urllib.request, json

BASE = 'http://localhost:5005/api'

def post(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(BASE + path, data=body, headers={'Content-Type':'application/json'}, method='POST')
    r = urllib.request.urlopen(req)
    return json.loads(r.read())

print('=== DDI Predict - Safety Profile Test ===')

# Test Simvastatin + Ritonavir (Statin + Antiviral)
# Alternatives for Simvastatin should be other statins like Pravastatin/Rosuvastatin
print('Fetching alternatives for Simvastatin + Ritonavir...')
alt = post('/drug-alternatives', {
    'drug_a': 'simvastatin', 
    'drug_b': 'ritonavir', 
    'alternatives_for': 'drug_a',
    'count': 3
})

if alt.get('suggestions'):
    print(f"Found {len(alt['suggestions'])} suggestions.")
    for s in alt['suggestions']:
        print(f"Suggestion: {s['name']}")
        if 'safety_profile' in s:
            print(f"  [PASS] Safety Profile found: {s['safety_profile']['common'][:2]}...")
        else:
            print(f"  [FAIL] Safety Profile MISSING!")
else:
    print("No suggestions found for this pair.")
