from rdkit import Chem
from rdkit.Chem import AllChem
s = "CCC(C)(C)C(=O)OC1CC(C=C2C1C(C(C=C2)C)CCC3CC(CC(=O)O3)O)C"
m = Chem.MolFromSmiles(s)
print('mol', bool(m))
if m:
    fp = AllChem.GetMorganFingerprintAsBitVect(m,2,nBits=1024)
    print('fp_len', len(fp))
else:
    print('no mol')
