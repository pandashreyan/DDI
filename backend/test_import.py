try:
    import rdkit
    from rdkit import Chem
    print("RDKit version:", rdkit.__version__)
    print("Chem imported successfully")
except ImportError as e:
    print("ImportError:", e)
except Exception as e:
    print("Error:", e)
