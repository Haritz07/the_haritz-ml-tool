from pydantic import BaseModel
from typing import Optional

class WalletFeatures(BaseModel):
    total_transactions: int
    inflow: float
    outflow: float
    inflow_outflow_ratio: float
    duration_days: int
    transactions_per_day: float
    minted_tokens: int
    avg_mint_time: float
    early_pump_and_dump_flag: int


class PredictionResponse(BaseModel):
    risk_label: int
    risk_probability: float
