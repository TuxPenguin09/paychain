from pydantic import BaseModel, Field
from enum import Enum


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    SALARY_DISBURSEMENT = "salary_disbursement"
    WITHDRAWAL = "withdrawal"
    REFUND = "refund"


class Transaction(BaseModel):
    tx_hash: str = Field(..., description="Blockchain transaction hash")
    from_address: str
    to_address: str
    amount: float = Field(..., gt=0, description="Amount in PHP")
    tx_type: TransactionType
    timestamp: float = Field(..., description="Unix timestamp")
    block_number: int | None = None


class TransactionFraudFeatures(BaseModel):
    """Features extracted for Naive Bayes fraud detection."""
    amount: float
    amount_log: float
    amount_deviation: float = Field(..., description="Z-score deviation from average")
    velocity_24h: int = Field(..., description="Number of transactions in last 24h")
    velocity_7d: int = Field(..., description="Number of transactions in last 7 days")
    hour_of_day: int = Field(..., ge=0, le=23)
    is_weekend: bool
    is_holiday: bool
    balance_delta: float = Field(..., description="Change in account balance")
    is_new_payee: bool = Field(False, description="First time sending to this address")
    amount_ratio_to_avg: float = Field(
        1.0, description="Amount / average transaction amount"
    )


class FraudPrediction(BaseModel):
    is_fraud: bool
    fraud_probability: float = Field(..., ge=0, le=1)
    risk_level: str = Field(..., description="low, medium, or high")
    flagged_reasons: list[str] = Field(default_factory=list)
