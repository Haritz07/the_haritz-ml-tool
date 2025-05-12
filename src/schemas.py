from pydantic import BaseModel
from typing import Optional

class WalletAddressRequest(BaseModel):
    wallet_address: str

class WalletRiskResponse(BaseModel):
    wallet_address: str
    risk_score: int
    risk_level: float