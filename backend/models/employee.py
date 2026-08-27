from pydantic import BaseModel, Field
from enum import Enum


class Region(str, Enum):
    NCR = "NCR"
    REGION_III = "Region III"
    REGION_IV_A = "Region IV-A"
    REGION_V = "Region V"
    REGION_VI = "Region VI"
    REGION_VII = "Region VII"
    REGION_VIII = "Region VIII"
    REGION_IX = "Region IX"
    REGION_X = "Region X"
    REGION_XI = "Region XI"
    REGION_XII = "Region XII"
    CAR = "CAR"
    BARMM = "BARMM"
    OTHERS = "Others"


class Employee(BaseModel):
    address: str = Field(..., description="Blockchain wallet address")
    name: str
    region: Region
    monthly_wage: float = Field(..., gt=0, description="Monthly wage in PHP")
    tenure_months: int = Field(0, ge=0)
    has_13th_month: bool = True
    sss_paid: bool = True
    philhealth_paid: bool = True
    pagibig_paid: bool = True
    dispute_count: int = Field(0, ge=0)
    employment_months: int = Field(1, ge=1)


class EmployeeRiskFeatures(BaseModel):
    """Features extracted for Naive Bayes risk scoring."""
    region: int
    tenure_months: int
    monthly_wage: float
    dispute_count: int
    employment_months: int
    has_13th_month: bool
    sss_paid: bool
    philhealth_paid: bool
    pagibig_paid: bool
