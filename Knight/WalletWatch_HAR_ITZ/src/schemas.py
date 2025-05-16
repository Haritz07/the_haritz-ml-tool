from pydantic import BaseModel
from typing import Dict, Optional

class WalletAddressRequest(BaseModel):
    wallet_address: str

class WalletRiskResponse(BaseModel):
    wallet_address: str
    risk_score: int
    risk_level: float
    timestamp: Optional[str]
    features: Optional[Dict[str, float]]