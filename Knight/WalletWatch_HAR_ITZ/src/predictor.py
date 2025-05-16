from datetime import datetime
import joblib
import math
from fastapi import FastAPI
import pandas as pd
from src.schemas import WalletRiskResponse, WalletAddressRequest
from fastapi import HTTPException

features_df = pd.read_csv("data/wallet_features_with_risk_score.csv")

model = joblib.load(r'C:\Users\Josh\Desktop\Knight\WalletWatch_HAR_ITZ/src/model/xgb_model.pkl')

app = FastAPI(
    title="Wallet Risk Detection API",
    version="1.0",
    description="API to detect risky/scam wallets based on transaction behaviors."
)
def sanitize_float(value: float) -> float:
    if math.isnan(value) or math.isinf(value):
        return 0.0
    return value
@app.post("/predict-wallet-risk", response_model=WalletRiskResponse)
def predict_wallet_risk(request: WalletAddressRequest):
    wallet_address = request.wallet_address


    # 2. Select just the row for this wallet
    wallet_row = features_df[features_df["wallet_address"] == wallet_address]
    if wallet_row.empty:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # 3. Extract the feature dict *before* you drop columns
    feature_columns = [
        c for c in wallet_row.columns 
        if c not in ("wallet_address", "risk_score", "risk_label")
    ]
    features = wallet_row.iloc[0][feature_columns].to_dict()

    # 4. Prepare model input by dropping non-features
    model_input = wallet_row.drop(
        columns=["wallet_address", "risk_score", "risk_label"],
        errors="ignore"
    ).astype(float)
    
    model_input = model_input.map(sanitize_float)

    # 5. Run your ML model
    risk_score = int(model.predict(model_input)[0])
    risk_level_prob = model.predict_proba(model_input)[0][risk_score]
    risk_level = round(float(risk_level_prob) * 100, 2)
    
    # 6. I convert features to float values
    features = {k: float(v) for k, v in model_input.iloc[0].to_dict().items()}

    # 7. Return everything together
    return WalletRiskResponse(
        wallet_address=wallet_address,
        risk_score=risk_score,
        risk_level=risk_level,
        timestamp=datetime.utcnow().isoformat() + "Z",
        features=model_input.iloc[0].to_dict()
    )
