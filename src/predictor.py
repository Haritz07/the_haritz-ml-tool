import joblib
from fastapi import FastAPI
import pandas as pd
from src.schemas import WalletRiskResponse, WalletAddressRequest
from fastapi import HTTPException

model = joblib.load(r'C:\Users\ayemi\OneDrive\Documents\The_Haritz\src\model\xgb_model.pkl')

app = FastAPI(
    title="Wallet Risk Detection API",
    version="1.0",
    description="API to detect risky/scam wallets based on transaction behaviors."
)
@app.post("/predict-wallet-risk", response_model=WalletRiskResponse)
def predict_wallet_risk(request: WalletAddressRequest):
    wallet_address = request.wallet_address

    # Your logic to generate features for the wallet
    features_df = pd.read_csv(r'C:\Users\ayemi\OneDrive\Documents\The_Haritz\data\wallet_features.csv')

    if features_df is None or features_df.empty:
        raise HTTPException(status_code=404, detail="Wallet not found or no data available")

    # Drop wallet_address column for model input
    model_input = features_df.drop(columns=["wallet_address"], errors="ignore")
    model_input = model_input.astype(float)

    risk_score = int(model.predict(model_input)[0])
    risk_level = model.predict_proba(model_input)[0][risk_score]


    return WalletRiskResponse(
        wallet_address=wallet_address,
        risk_score=risk_score,
        risk_level=round(float(risk_level) * 100, 2)
    )
