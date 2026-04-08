import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier

# Create a tiny dummy model that takes 2048-bit inputs
# (1024 bits per drug, concatenated)
X = np.random.randint(0, 2, (10, 2048))
y = np.random.randint(0, 2, 10)

model = RandomForestClassifier(n_estimators=10)
model.fit(X, y)

with open('c:/Users/KIIT/OneDrive/Desktop/ml/backend/ddi_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Mock AI model generated successfully for verification.")
