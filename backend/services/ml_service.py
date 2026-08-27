import logging
from pathlib import Path

import joblib
import numpy as np

logger = logging.getLogger(__name__)

MODEL_DIR = Path(__file__).parent / "models"

RISK_LABELS = {0: "low", 1: "medium", 2: "high"}
FRAUD_THRESHOLD = 0.4


class MLService:
    def __init__(self):
        self.fraud_detector = None
        self.employer_risk_scorer = None
        self.employee_risk_scorer = None
        self.contract_classifier = None
        self.region_encoder = None
        self._load_models()

    def _load_models(self):
        try:
            self.fraud_detector = joblib.load(MODEL_DIR / "fraud_detector.joblib")
            logger.info("Loaded fraud_detector model")
        except FileNotFoundError:
            logger.warning("fraud_detector model not found at %s", MODEL_DIR)

        try:
            self.employer_risk_scorer = joblib.load(MODEL_DIR / "employer_risk_scorer.joblib")
            logger.info("Loaded employer_risk_scorer model")
        except FileNotFoundError:
            logger.warning("employer_risk_scorer model not found at %s", MODEL_DIR)

        try:
            self.employee_risk_scorer = joblib.load(MODEL_DIR / "employee_risk_scorer.joblib")
            self.region_encoder = joblib.load(MODEL_DIR / "region_encoder.joblib")
            logger.info("Loaded employee_risk_scorer model")
        except FileNotFoundError:
            logger.warning("employee_risk_scorer model not found at %s", MODEL_DIR)

        try:
            self.contract_classifier = joblib.load(MODEL_DIR / "contract_classifier.joblib")
            logger.info("Loaded contract_classifier model")
        except FileNotFoundError:
            logger.warning("contract_classifier model not found at %s", MODEL_DIR)

    def predict_fraud(self, features: dict) -> dict:
        if self.fraud_detector is None:
            return {"error": "Fraud detector model not loaded. Run training scripts first."}

        X = np.array([[
            features["amount"],
            features["amount_log"],
            features["amount_deviation"],
            features["velocity_24h"],
            features["velocity_7d"],
            features["hour_of_day"],
            features["is_weekend"],
            features["is_holiday"],
            features["balance_delta"],
            features["is_new_payee"],
            features["amount_ratio_to_avg"],
        ]])

        is_fraud = bool(self.fraud_detector.predict(X)[0])
        fraud_proba = float(self.fraud_detector.predict_proba(X)[0][1])

        risk_level = "low"
        if fraud_proba > 0.7:
            risk_level = "high"
        elif fraud_proba > FRAUD_THRESHOLD:
            risk_level = "medium"

        reasons = []
        if features["velocity_24h"] > 5:
            reasons.append("High transaction frequency in 24h")
        if features["amount_deviation"] > 2.0:
            reasons.append("Amount significantly deviates from average")
        if features["is_new_payee"]:
            reasons.append("First-time payee")
        if features["hour_of_day"] < 6 or features["hour_of_day"] > 22:
            reasons.append("Unusual transaction time")
        if features["amount_ratio_to_avg"] > 3.0:
            reasons.append("Amount much higher than usual")

        return {
            "is_fraud": is_fraud,
            "fraud_probability": round(fraud_proba, 4),
            "risk_level": risk_level,
            "flagged_reasons": reasons,
        }

    def predict_employer_risk(self, features: dict) -> dict:
        if self.employer_risk_scorer is None:
            return {"error": "Employer risk model not loaded. Run training scripts first."}

        X = np.array([[
            features["payment_regularity"],
            features["wage_vs_min_ratio"],
            features["compliance_score"],
            features["turnover_rate"],
            features["complaint_count"],
            features["registered_employees"],
            features["total_disbursements"],
        ]])

        risk_level_int = int(self.employer_risk_scorer.predict(X)[0])
        risk_level = RISK_LABELS.get(risk_level_int, "unknown")

        return {
            "risk_level": risk_level,
            "risk_score": risk_level_int,
            "details": {
                "payment_regularity": features["payment_regularity"],
                "compliance_score": features["compliance_score"],
                "turnover_rate": features["turnover_rate"],
                "complaint_count": features["complaint_count"],
            },
        }

    def predict_employee_risk(self, features: dict) -> dict:
        if self.employee_risk_scorer is None or self.region_encoder is None:
            return {"error": "Employee risk model not loaded. Run training scripts first."}

        try:
            region_encoded = self.region_encoder.transform([features["region"]])[0]
        except ValueError:
            region_encoded = 0

        X = np.array([[
            region_encoded,
            features["tenure_months"],
            features["monthly_wage"],
            features["dispute_count"],
            features["employment_months"],
            features["has_13th_month"],
            features["sss_paid"],
            features["philhealth_paid"],
            features["pagibig_paid"],
        ]])

        risk_level_int = int(self.employee_risk_scorer.predict(X)[0])
        risk_level = RISK_LABELS.get(risk_level_int, "unknown")

        return {
            "risk_level": risk_level,
            "risk_score": risk_level_int,
            "details": {
                "region": features["region"],
                "tenure_months": features["tenure_months"],
                "dispute_count": features["dispute_count"],
                "benefits_compliant": all([
                    features.get("sss_paid", False),
                    features.get("philhealth_paid", False),
                    features.get("pagibig_paid", False),
                ]),
            },
        }

    def predict_contract_safety(self, features: dict) -> dict:
        if self.contract_classifier is None:
            return {"error": "Contract classifier model not loaded. Run training scripts first."}

        X = np.array([[
            features["push_count"],
            features["sstore_count"],
            features["sload_count"],
            features["call_count"],
            features["delegatecall_count"],
            features["selfdestruct_count"],
            features["callvalue_check"],
            features["reentrancy_guard"],
            features["has_events"],
            features["function_count"],
            features["state_var_count"],
            features["external_calls"],
            features["timestamp_usage"],
            features["assembly_usage"],
        ]]).clip(0).astype(int)

        is_vulnerable = bool(self.contract_classifier.predict(X)[0])
        vuln_proba = float(self.contract_classifier.predict_proba(X)[0][1])

        vulnerabilities = []
        if features.get("selfdestruct_count", 0) > 0:
            vulnerabilities.append("selfdestruct usage detected")
        if features.get("delegatecall_count", 0) > 0:
            vulnerabilities.append("delegatecall usage detected")
        if features.get("reentrancy_guard", 0) == 0 and features.get("call_count", 0) > 2:
            vulnerabilities.append("potential reentrancy (no guard + external calls)")
        if features.get("callvalue_check", 0) == 0:
            vulnerabilities.append("missing callvalue check")
        if features.get("timestamp_usage", 0) > 0:
            vulnerabilities.append("timestamp dependence")
        if features.get("assembly_usage", 0) > 0:
            vulnerabilities.append("inline assembly usage")

        return {
            "is_vulnerable": is_vulnerable,
            "vulnerability_probability": round(vuln_proba, 4),
            "risk_level": "high" if vuln_proba > 0.7 else "medium" if vuln_proba > 0.4 else "low",
            "detected_issues": vulnerabilities,
        }


ml_service = MLService()
