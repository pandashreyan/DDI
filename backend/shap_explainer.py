"""
SHAP Model Interpretability Module
Explains DDI predictions with feature contributions
"""

import shap
import numpy as np
import pickle
import os
from functools import lru_cache

EXPLAINER = None
FEATURE_NAMES = None

def init_shap_explainer(model, X_train_sample=None):
    """Initialize SHAP explainer with your trained model"""
    global EXPLAINER, FEATURE_NAMES
    
    try:
        # For tree-based models (RandomForest, XGBoost)
        EXPLAINER = shap.TreeExplainer(model)
        
        # Feature names: 1024 fingerprint bits + MW + LogP (per drug) * 2
        fp_names = [f"fp_{i}" for i in range(1024)]
        other_names = ["molecular_weight", "logp"]
        FEATURE_NAMES = fp_names + other_names + fp_names + other_names
        
        print("[SHAP] Explainer initialized successfully")
        return True
    except Exception as e:
        print(f"[SHAP-ERROR] Failed to initialize: {e}")
        return False

def get_prediction_explanation(model, feature_vector, drug_a, drug_b):
    """
    Get SHAP explanation for a single prediction
    
    Args:
        model: Trained ML model
        feature_vector: Combined feature vector [drug_a_features + drug_b_features]
        drug_a: First drug name (for context)
        drug_b: Second drug name (for context)
    
    Returns:
        dict with explanation data suitable for REST API
    """
    if EXPLAINER is None:
        print("[SHAP-WARN] Explainer not initialized. Initializing now...")
        init_shap_explainer(model)
    
    if EXPLAINER is None:
        return None
    
    try:
        # Reshape feature vector for prediction and explanation
        X = feature_vector.reshape(1, -1)
        
        # Get SHAP values
        shap_values = EXPLAINER.shap_values(X)
        base_value = EXPLAINER.expected_value
        
        # Handle multi-class output (for binary classification)
        if isinstance(shap_values, list):
            shap_values = shap_values[1]  # Use class 1 (positive interaction)
        
        # Get top features contributing to the prediction
        feature_importance = np.abs(shap_values[0])
        top_indices = np.argsort(feature_importance)[-10:][::-1]  # Top 10 features
        
        # Build explanation for API response
        explanation = {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "base_risk": float(base_value),
            "top_features": []
        }
        
        for idx in top_indices:
            if idx < len(FEATURE_NAMES):
                feature_name = FEATURE_NAMES[idx]
                contribution = float(shap_values[0][idx])
                feature_value = float(X[0][idx])
                
                # Clean up feature names for display
                if "fp_" in feature_name:
                    display_name = f"Fingerprint Bit {feature_name.split('_')[1]}"
                else:
                    display_name = feature_name.replace("_", " ").title()
                
                explanation["top_features"].append({
                    "name": display_name,
                    "contribution": contribution,
                    "direction": "increases risk" if contribution > 0 else "decreases risk",
                    "magnitude": abs(contribution),
                    "feature_value": feature_value
                })
        
        # Sort by magnitude (descending)
        explanation["top_features"].sort(key=lambda x: x["magnitude"], reverse=True)
        
        return explanation
    
    except Exception as e:
        print(f"[SHAP-ERROR] Explanation failed: {e}")
        return None


def get_summary_statistics(model, X_test):
    """
    Generate summary statistics for model explainability
    Shows which features are important across the entire dataset
    
    Args:
        model: Trained ML model
        X_test: Test feature set
    
    Returns:
        dict with summary feature importance
    """
    if EXPLAINER is None:
        init_shap_explainer(model)
    
    if EXPLAINER is None:
        return None
    
    try:
        # Calculate SHAP values for entire test set
        shap_values = EXPLAINER.shap_values(X_test)
        
        # Handle multi-class
        if isinstance(shap_values, list):
            shap_values = shap_values[1]
        
        # Mean absolute SHAP values = feature importance
        mean_abs_shap = np.mean(np.abs(shap_values), axis=0)
        top_indices = np.argsort(mean_abs_shap)[-15:][::-1]
        
        summary = {
            "total_predictions_analyzed": int(X_test.shape[0]),
            "top_important_features": []
        }
        
        for idx in top_indices:
            if idx < len(FEATURE_NAMES):
                summary["top_important_features"].append({
                    "name": FEATURE_NAMES[idx],
                    "importance": float(mean_abs_shap[idx])
                })
        
        return summary
    
    except Exception as e:
        print(f"[SHAP-ERROR] Summary stats failed: {e}")
        return None
