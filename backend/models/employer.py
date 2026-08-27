from pydantic import BaseModel, Field


class Employer(BaseModel):
    address: str = Field(..., description="Blockchain wallet address")
    name: str
    payment_regularity: float = Field(
        1.0, ge=0, le=1, description="Percentage of on-time payments (0-1)"
    )
    wage_vs_min_ratio: float = Field(
        1.0, gt=0, description="Ratio of paid wage to regional minimum"
    )
    compliance_score: float = Field(
        1.0, ge=0, le=1, description="Overall compliance score (0-1)"
    )
    turnover_rate: float = Field(
        0.0, ge=0, le=1, description="Percentage of employees leaving within 1 year"
    )
    complaint_count: int = Field(0, ge=0)
    registered_employees: int = Field(0, ge=0)
    total_disbursements: int = Field(0, ge=0)


class EmployerRiskFeatures(BaseModel):
    """Features extracted for Naive Bayes risk scoring."""
    payment_regularity: float
    wage_vs_min_ratio: float
    compliance_score: float
    turnover_rate: float
    complaint_count: int
    registered_employees: int
    total_disbursements: int
