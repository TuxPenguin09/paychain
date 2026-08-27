import numpy as np
import pandas as pd
from pathlib import Path


REGION_MIN_WAGES = {
    "NCR": 16770,
    "Region III": 13000,
    "Region IV-A": 13500,
    "Region V": 11000,
    "Region VI": 11500,
    "Region VII": 11800,
    "Region VIII": 10500,
    "Region IX": 10200,
    "Region X": 11200,
    "Region XI": 11000,
    "Region XII": 10800,
    "CAR": 11000,
    "BARMM": 9500,
    "Others": 10000,
}


def generate_fraud_data(n_samples: int = 2000, fraud_ratio: float = 0.15) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n_fraud = int(n_samples * fraud_ratio)
    n_normal = n_samples - n_fraud

    normal = {
        "amount": rng.normal(12000, 4000, n_normal).clip(5000, 30000),
        "amount_log": np.log1p(rng.normal(9.3, 0.4, n_normal)).clip(8, 11),
        "amount_deviation": rng.normal(0, 0.8, n_normal).clip(-2, 2),
        "velocity_24h": rng.poisson(1, n_normal).clip(0, 5),
        "velocity_7d": rng.poisson(4, n_normal).clip(0, 15),
        "hour_of_day": rng.integers(8, 18, n_normal),
        "is_weekend": rng.choice([0, 1], n_normal, p=[0.7, 0.3]),
        "is_holiday": rng.choice([0, 1], n_normal, p=[0.95, 0.05]),
        "balance_delta": rng.normal(-12000, 4000, n_normal).clip(-30000, -500),
        "is_new_payee": rng.choice([0, 1], n_normal, p=[0.85, 0.15]),
        "amount_ratio_to_avg": rng.normal(1.0, 0.3, n_normal).clip(0.3, 2.5),
        "is_fraud": 0,
    }

    fraud = {
        "amount": rng.choice(
            [rng.uniform(1, 500, n_fraud // 2), rng.uniform(80000, 500000, n_fraud - n_fraud // 2)]
        ).flatten()[:n_fraud],
        "amount_log": np.log1p(rng.uniform(1, 500000, n_fraud)),
        "amount_deviation": rng.normal(3.5, 1.5, n_fraud).clip(1.5, 8),
        "velocity_24h": rng.poisson(8, n_fraud).clip(3, 30),
        "velocity_7d": rng.poisson(20, n_fraud).clip(5, 60),
        "hour_of_day": rng.integers(0, 24, n_fraud),
        "is_weekend": rng.choice([0, 1], n_fraud, p=[0.4, 0.6]),
        "is_holiday": rng.choice([0, 1], n_fraud, p=[0.7, 0.3]),
        "balance_delta": rng.choice(
            [rng.normal(-500, 200, n_fraud // 3),
             rng.normal(-200000, 80000, n_fraud - n_fraud // 3)]
        ).flatten()[:n_fraud],
        "is_new_payee": rng.choice([0, 1], n_fraud, p=[0.3, 0.7]),
        "amount_ratio_to_avg": rng.normal(8.0, 4.0, n_fraud).clip(2.0, 30.0),
        "is_fraud": 1,
    }

    df_normal = pd.DataFrame(normal)
    df_fraud = pd.DataFrame(fraud)
    df = pd.concat([df_normal, df_fraud], ignore_index=True)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    return df


def generate_employer_risk_data(n_samples: int = 1500) -> pd.DataFrame:
    rng = np.random.default_rng(42)

    n_good = int(n_samples * 0.6)
    n_medium = int(n_samples * 0.25)
    n_bad = n_samples - n_good - n_medium

    def make_employer(n, risk_level):
        if risk_level == "low":
            return {
                "payment_regularity": rng.normal(0.95, 0.03, n).clip(0.85, 1.0),
                "wage_vs_min_ratio": rng.normal(1.2, 0.15, n).clip(1.0, 2.0),
                "compliance_score": rng.normal(0.92, 0.05, n).clip(0.8, 1.0),
                "turnover_rate": rng.normal(0.10, 0.05, n).clip(0.0, 0.25),
                "complaint_count": rng.poisson(0, n).clip(0, 1),
                "registered_employees": rng.integers(3, 20, n),
                "total_disbursements": rng.integers(24, 120, n),
                "risk_level": 0,
            }
        elif risk_level == "medium":
            return {
                "payment_regularity": rng.normal(0.78, 0.08, n).clip(0.5, 0.9),
                "wage_vs_min_ratio": rng.normal(1.02, 0.05, n).clip(0.9, 1.15),
                "compliance_score": rng.normal(0.70, 0.1, n).clip(0.45, 0.85),
                "turnover_rate": rng.normal(0.30, 0.1, n).clip(0.15, 0.55),
                "complaint_count": rng.poisson(2, n).clip(0, 5),
                "registered_employees": rng.integers(1, 10, n),
                "total_disbursements": rng.integers(6, 48, n),
                "risk_level": 1,
            }
        else:
            return {
                "payment_regularity": rng.normal(0.50, 0.15, n).clip(0.1, 0.7),
                "wage_vs_min_ratio": rng.normal(0.85, 0.1, n).clip(0.5, 1.0),
                "compliance_score": rng.normal(0.35, 0.12, n).clip(0.0, 0.55),
                "turnover_rate": rng.normal(0.60, 0.15, n).clip(0.35, 0.9),
                "complaint_count": rng.poisson(6, n).clip(2, 15),
                "registered_employees": rng.integers(1, 5, n),
                "total_disbursements": rng.integers(0, 12, n),
                "risk_level": 2,
            }

    data = {}
    for level, count in [("low", n_good), ("medium", n_medium), ("bad", n_bad)]:
        subset = make_employer(count, level)
        for k, v in subset.items():
            data.setdefault(k, []).extend(v)

    df = pd.DataFrame(data)
    return df.sample(frac=1, random_state=42).reset_index(drop=True)


def generate_employee_risk_data(n_samples: int = 1500) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    regions = list(REGION_MIN_WAGES.keys())

    n_low = int(n_samples * 0.65)
    n_medium = int(n_samples * 0.25)
    n_high = n_samples - n_low - n_medium

    def make_employee(n, risk_level):
        if risk_level == "low":
            return {
                "region": rng.choice(regions, n),
                "tenure_months": rng.integers(12, 120, n),
                "monthly_wage": rng.normal(13000, 3000, n).clip(8000, 30000),
                "dispute_count": rng.poisson(0, n).clip(0, 1),
                "employment_months": rng.integers(12, 120, n),
                "has_13th_month": rng.choice([1, 1, 1, 1, 0], n),
                "sss_paid": rng.choice([1, 1, 1, 1, 0], n),
                "philhealth_paid": rng.choice([1, 1, 1, 1, 0], n),
                "pagibig_paid": rng.choice([1, 1, 1, 1, 0], n),
                "risk_level": 0,
            }
        elif risk_level == "medium":
            return {
                "region": rng.choice(regions, n),
                "tenure_months": rng.integers(3, 24, n),
                "monthly_wage": rng.normal(11000, 2000, n).clip(6000, 20000),
                "dispute_count": rng.poisson(1, n).clip(0, 3),
                "employment_months": rng.integers(3, 24, n),
                "has_13th_month": rng.choice([1, 1, 0, 0, 0], n),
                "sss_paid": rng.choice([1, 1, 1, 0, 0], n),
                "philhealth_paid": rng.choice([1, 1, 1, 0, 0], n),
                "pagibig_paid": rng.choice([1, 1, 1, 0, 0], n),
                "risk_level": 1,
            }
        else:
            return {
                "region": rng.choice(regions, n),
                "tenure_months": rng.integers(0, 6, n),
                "monthly_wage": rng.normal(8000, 2000, n).clip(4000, 15000),
                "dispute_count": rng.poisson(3, n).clip(1, 10),
                "employment_months": rng.integers(1, 6, n),
                "has_13th_month": rng.choice([0, 0, 0, 1, 1], n),
                "sss_paid": rng.choice([0, 0, 0, 1, 1], n),
                "philhealth_paid": rng.choice([0, 0, 0, 1, 1], n),
                "pagibig_paid": rng.choice([0, 0, 0, 1, 1], n),
                "risk_level": 2,
            }

    data = {}
    for level, count in [("low", n_low), ("medium", n_medium), ("high", n_high)]:
        subset = make_employee(count, level)
        for k, v in subset.items():
            data.setdefault(k, []).extend(v)

    df = pd.DataFrame(data)
    return df.sample(frac=1, random_state=42).reset_index(drop=True)


def generate_contract_data(n_samples: int = 1000) -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n_safe = int(n_samples * 0.7)
    n_vuln = n_samples - n_safe

    safe_opcodes = {
        "push_count": rng.poisson(15, n_safe).clip(5, 30),
        "sstore_count": rng.poisson(3, n_safe).clip(0, 8),
        "sload_count": rng.poisson(4, n_safe).clip(1, 10),
        "call_count": rng.poisson(1, n_safe).clip(0, 4),
        "delegatecall_count": np.zeros(n_safe, dtype=int),
        "selfdestruct_count": np.zeros(n_safe, dtype=int),
        "callvalue_check": rng.choice([1, 1, 1, 1, 0], n_safe),
        "reentrancy_guard": rng.choice([1, 1, 1, 0, 0], n_safe),
        "has_events": rng.choice([1, 1, 1, 1, 0], n_safe),
        "function_count": rng.integers(2, 15, n_safe),
        "state_var_count": rng.integers(1, 8, n_safe),
        "external_calls": rng.poisson(1, n_safe).clip(0, 5),
        "timestamp_usage": rng.choice([0, 0, 0, 1, 1], n_safe),
        "assembly_usage": rng.choice([0, 0, 0, 0, 1], n_safe),
        "is_vulnerable": 0,
    }

    vuln_opcodes = {
        "push_count": rng.poisson(20, n_vuln).clip(8, 40),
        "sstore_count": rng.poisson(5, n_vuln).clip(1, 15),
        "sload_count": rng.poisson(6, n_vuln).clip(2, 15),
        "call_count": rng.poisson(4, n_vuln).clip(1, 12),
        "delegatecall_count": rng.poisson(1, n_vuln).clip(0, 4),
        "selfdestruct_count": rng.choice([0, 0, 0, 0, 0, 1], n_vuln),
        "callvalue_check": rng.choice([0, 0, 1, 1, 1], n_vuln),
        "reentrancy_guard": rng.choice([0, 0, 0, 1, 1], n_vuln),
        "has_events": rng.choice([0, 0, 1, 1, 1], n_vuln),
        "function_count": rng.integers(3, 20, n_vuln),
        "state_var_count": rng.integers(2, 10, n_vuln),
        "external_calls": rng.poisson(5, n_vuln).clip(2, 15),
        "timestamp_usage": rng.choice([1, 1, 1, 1, 0], n_vuln),
        "assembly_usage": rng.choice([1, 1, 1, 0, 0], n_vuln),
        "is_vulnerable": 1,
    }

    data = {}
    for d in [safe_opcodes, vuln_opcodes]:
        for k, v in d.items():
            data.setdefault(k, []).extend(v)

    df = pd.DataFrame(data)
    return df.sample(frac=1, random_state=42).reset_index(drop=True)


if __name__ == "__main__":
    data_dir = Path(__file__).parent / "data"

    print("Generating fraud detection data...")
    fraud_df = generate_fraud_data()
    fraud_df.to_csv(data_dir / "fraud_data.csv", index=False)
    print(f"  {len(fraud_df)} samples ({fraud_df['is_fraud'].sum()} fraud)")

    print("Generating employer risk data...")
    employer_df = generate_employer_risk_data()
    employer_df.to_csv(data_dir / "employer_risk_data.csv", index=False)
    print(f"  {len(employer_df)} samples")

    print("Generating employee risk data...")
    employee_df = generate_employee_risk_data()
    employee_df.to_csv(data_dir / "employee_risk_data.csv", index=False)
    print(f"  {len(employee_df)} samples")

    print("Generating contract vulnerability data...")
    contract_df = generate_contract_data()
    contract_df.to_csv(data_dir / "contract_data.csv", index=False)
    print(f"  {len(contract_df)} samples ({contract_df['is_vulnerable'].sum()} vulnerable)")

    print("All synthetic data generated in training/data/")
