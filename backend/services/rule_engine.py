from datetime import date
import pandas as pd

RULES = pd.DataFrame([
    {"component": "minimum_wage_monthly", "region": "NCR", "value": 16770,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region III", "value": 13000,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region IV-A", "value": 13500,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region V", "value": 11000,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region VI", "value": 11500,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region VII", "value": 11800,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region VIII", "value": 10500,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region IX", "value": 10200,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region X", "value": 11200,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region XI", "value": 11000,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Region XII", "value": 10800,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "CAR", "value": 11000,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "BARMM", "value": 9500,
     "effective_from": "2024-07-17", "effective_to": None},
    {"component": "minimum_wage_monthly", "region": "Others", "value": 10000,
     "effective_from": "2024-07-17", "effective_to": None},

    {"component": "sss_employer_rate", "region": "ALL", "value": 0.10,
     "effective_from": "2025-01-01", "effective_to": None},
    {"component": "sss_employee_rate", "region": "ALL", "value": 0.05,
     "effective_from": "2025-01-01", "effective_to": None},
    {"component": "sss_msc_min", "region": "ALL", "value": 4000,
     "effective_from": "2025-01-01", "effective_to": None},
    {"component": "sss_msc_max", "region": "ALL", "value": 35000,
     "effective_from": "2025-01-01", "effective_to": None},
    {"component": "sss_employer_pays_full_below", "region": "ALL", "value": 5000,
     "effective_from": "2025-01-01", "effective_to": None},

    {"component": "philhealth_rate", "region": "ALL", "value": 0.05,
     "effective_from": "2024-01-01", "effective_to": None},
    {"component": "philhealth_mwe_employee_waived", "region": "ALL", "value": 1,
     "effective_from": "2024-01-01", "effective_to": None},

    {"component": "pagibig_employee_rate", "region": "ALL", "value": 0.02,
     "effective_from": "2024-01-01", "effective_to": None},
    {"component": "pagibig_employer_rate", "region": "ALL", "value": 0.02,
     "effective_from": "2024-01-01", "effective_to": None},
    {"component": "pagibig_cap", "region": "ALL", "value": 100,
     "effective_from": "2024-01-01", "effective_to": None},

    {"component": "tax_free_ceiling_annual", "region": "ALL", "value": 250000,
     "effective_from": "2018-01-01", "effective_to": None},
    {"component": "benefits_tax_ceiling", "region": "ALL", "value": 90000,
     "effective_from": "2018-01-01", "effective_to": None},

    {"component": "max_loss_deduction_pct", "region": "ALL", "value": 0.20,
     "effective_from": None, "effective_to": None},
    {"component": "max_loan_deduction_pct", "region": "ALL", "value": 0.20,
     "effective_from": None, "effective_to": None},

    {"component": "service_incentive_leave_days", "region": "ALL", "value": 5,
     "effective_from": None, "effective_to": None},
    {"component": "service_incentive_leave_tenure_months", "region": "ALL", "value": 12,
     "effective_from": None, "effective_to": None},

    {"component": "unjust_dismissal_indemnity_days", "region": "ALL", "value": 15,
     "effective_from": None, "effective_to": None},
    {"component": "forfeitable_unpaid_days", "region": "ALL", "value": 15,
     "effective_from": None, "effective_to": None},
    {"component": "deployment_expense_recovery_months", "region": "ALL", "value": 6,
     "effective_from": None, "effective_to": None},
])


def _get_rule(component: str, region: str, as_of: date | None = None) -> float | None:
    as_of = as_of or date.today()
    df = RULES[RULES["component"] == component]

    if region != "ALL":
        df = df[(df["region"] == region) | (df["region"] == "ALL")]

    df = df[
        (df["effective_from"].isna() | (df["effective_from"] <= as_of.isoformat()))
        & (df["effective_to"].isna() | (df["effective_to"] >= as_of.isoformat()))
    ]

    if df.empty:
        return None
    return df.iloc[-1]["value"]


def get_minimum_wage(region: str, as_of: date | None = None) -> float:
    val = _get_rule("minimum_wage_monthly", region, as_of)
    if val is None:
        raise ValueError(f"No minimum wage rule found for region: {region}")
    return val


def compute_sss(monthly_wage: float, as_of: date | None = None) -> dict:
    msc_min = _get_rule("sss_msc_min", "ALL", as_of) or 4000
    msc_max = _get_rule("sss_msc_max", "ALL", as_of) or 35000
    employer_rate = _get_rule("sss_employer_rate", "ALL", as_of) or 0.10
    employee_rate = _get_rule("sss_employee_rate", "ALL", as_of) or 0.05
    employer_pays_full_below = _get_rule("sss_employer_pays_full_below", "ALL", as_of) or 5000

    msc = max(msc_min, min(monthly_wage, msc_max))

    if monthly_wage < employer_pays_full_below:
        employer_share = msc * employer_rate
        employee_share = 0.0
    else:
        employer_share = msc * employer_rate
        employee_share = msc * employee_rate

    return {
        "msc": msc,
        "employer_share": round(employer_share, 2),
        "employee_share": round(employee_share, 2),
        "total": round(employer_share + employee_share, 2),
    }


def compute_philhealth(monthly_wage: float, as_of: date | None = None) -> dict:
    rate = _get_rule("philhealth_rate", "ALL", as_of) or 0.05
    mwe_waived = _get_rule("philhealth_mwe_employee_waived", "ALL", as_of)

    min_wage = get_minimum_wage("NCR", as_of)
    is_mwe = monthly_wage <= min_wage

    total_premium = monthly_wage * rate

    if is_mwe and mwe_waived:
        employer_share = total_premium
        employee_share = 0.0
    else:
        employer_share = total_premium / 2
        employee_share = total_premium / 2

    return {
        "rate": rate,
        "total_premium": round(total_premium, 2),
        "employer_share": round(employer_share, 2),
        "employee_share": round(employee_share, 2),
        "is_mwe": is_mwe,
    }


def compute_pagibig(monthly_wage: float, as_of: date | None = None) -> dict:
    emp_rate = _get_rule("pagibig_employee_rate", "ALL", as_of) or 0.02
    er_rate = _get_rule("pagibig_employer_rate", "ALL", as_of) or 0.02
    cap = _get_rule("pagibig_cap", "ALL", as_of) or 100

    employee_share = min(monthly_wage * emp_rate, cap)
    employer_share = min(monthly_wage * er_rate, cap)

    return {
        "employee_rate": emp_rate,
        "employer_rate": er_rate,
        "cap": cap,
        "employee_share": round(employee_share, 2),
        "employer_share": round(employer_share, 2),
    }


def compute_13th_month(total_basic_salary: float) -> dict:
    monthly_13th = total_basic_salary / 12
    return {
        "annual_basic": total_basic_salary,
        "monthly_13th": round(monthly_13th, 2),
        "total_13th_month": round(total_basic_salary, 2),
    }


def check_withholding_tax(
    annual_compensation: float,
    annual_benefits: float,
    as_of: date | None = None,
) -> dict:
    tax_free_ceiling = _get_rule("tax_free_ceiling_annual", "ALL", as_of) or 250000
    benefits_ceiling = _get_rule("benefits_tax_ceiling", "ALL", as_of) or 90000

    is_tax_exempt = annual_compensation <= tax_free_ceiling
    taxable_benefits = max(0, annual_benefits - benefits_ceiling)

    return {
        "annual_compensation": annual_compensation,
        "is_tax_exempt": is_tax_exempt,
        "tax_free_ceiling": tax_free_ceiling,
        "benefits_ceiling": benefits_ceiling,
        "taxable_benefits": round(taxable_benefits, 2),
    }


def enforce_deduction_cap(monthly_wage: float, total_deductions: float) -> dict:
    max_pct = _get_rule("max_loss_deduction_pct", "ALL") or 0.20
    max_deduction = monthly_wage * max_pct
    capped = min(total_deductions, max_deduction)
    exceeded = total_deductions > max_deduction

    return {
        "original_deductions": round(total_deductions, 2),
        "max_allowed": round(max_deduction, 2),
        "applied": round(capped, 2),
        "exceeded": exceeded,
    }


def compute_salary(
    monthly_wage: float,
    region: str,
    tenure_months: int = 12,
    pay_date: date | None = None,
) -> dict:
    pay_date = pay_date or date.today()
    min_wage = get_minimum_wage(region, pay_date)

    below_minimum = monthly_wage < min_wage

    sss = compute_sss(monthly_wage, pay_date)
    philhealth = compute_philhealth(monthly_wage, pay_date)
    pagibig = compute_pagibig(monthly_wage, pay_date)

    total_statutory_deductions = sss["employee_share"] + philhealth["employee_share"] + pagibig["employee_share"]

    has_sil = tenure_months >= (_get_rule("service_incentive_leave_tenure_months", "ALL") or 12)
    sil_days = (_get_rule("service_incentive_leave_days", "ALL") or 5) if has_sil else 0
    daily_rate = monthly_wage / 26
    sil_amount = daily_rate * sil_days

    annual_compensation = monthly_wage * 12
    tax_info = check_withholding_tax(annual_compensation, 0, pay_date)
    monthly_tax = 0 if tax_info["is_tax_exempt"] else 0

    total_deductions = total_statutory_deductions + monthly_tax
    deduction_check = enforce_deduction_cap(monthly_wage, total_deductions)
    if deduction_check["exceeded"]:
        total_deductions = deduction_check["applied"]

    net_salary = monthly_wage - total_deductions

    return {
        "region": region,
        "minimum_wage": min_wage,
        "below_minimum": below_minimum,
        "monthly_wage": monthly_wage,
        "statutory_deductions": {
            "sss": sss,
            "philhealth": philhealth,
            "pagibig": pagibig,
        },
        "total_statutory_deductions": round(total_statutory_deductions, 2),
        "withholding_tax": monthly_tax,
        "total_deductions": round(total_deductions, 2),
        "net_salary": round(net_salary, 2),
        "service_incentive_leave": {
            "eligible": has_sil,
            "days": sil_days,
            "amount": round(sil_amount, 2),
        },
        "compliance": {
            "minimum_wage_met": not below_minimum,
            "deduction_cap_enforced": deduction_check["exceeded"],
            "tax_exempt": tax_info["is_tax_exempt"],
        },
    }
