import joblib
import pandas as pd

# Load model once
model = joblib.load(r'C:\Users\ayemi\OneDrive\Documents\The_Haritz\src\model\xgb_model.pkl')


def predict_wallet_risk(features: dict):
    """Make a prediction for a given wallet feature dictionary."""
    df = pd.DataFrame([features])
    
    prediction = model.predict(df)[0]
    probability = model.predict_proba(df)[0][1] 
    
    return {
        "risk_label": int(prediction),
        "risk_probability": round(float(probability), 4)
    }
