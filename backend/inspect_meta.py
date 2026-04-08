import json
from pathlib import Path
p=Path('drug_metadata.json')
js=json.load(p.open())
matches=[k for k in js.keys() if 'simvastatin' in k.lower()]
print('matches',matches)
if matches:
    key=matches[0]
    print('meta', js[key])
    cls=js[key].get('class')
    same=[k for k,v in js.items() if v.get('class')==cls and k!=key]
    print('class',cls,'same_class_count',len(same),'examples',same[:10])
else:
    print('no simvastatin entry')
