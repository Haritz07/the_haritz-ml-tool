from fastapi import FastAPI
from src.predictor import predict_wallet_risk
from src.schemas import WalletFeatures, PredictionResponse

app = FastAPI(
    title="Wallet Risk Detection API",
    version="1.0",
    description="API to detect risky/scam wallets based on transaction behaviors."
)

@app.post("/predict", response_model=PredictionResponse)
def predict_risk(features: WalletFeatures):
    prediction = predict_wallet_risk(features.dict())
    return prediction

@app.get("/")
def home():
    return {"message": "Wallet Risk Detection API!"}
