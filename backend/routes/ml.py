import math
from flask import Blueprint, jsonify, request
from services.rule_engine import (
    compute_salary,
    compute_sss,
    compute_philhealth,
    compute_pagibig,
    get_minimum_wage,
    check_withholding_tax,
    enforce_deduction_cap,
)
from services.ml_service import ml_service

ml_bp = Blueprint("ml", __name__)


@ml_bp.route("/api/ml/compute-salary", methods=["POST"])
def api_compute_salary():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    monthly_wage = data.get("monthly_wage")
    region = data.get("region")
    if monthly_wage is None or region is None:
        return jsonify({"error": "monthly_wage and region are required"}), 400

    tenure_months = data.get("tenure_months", 12)

    try:
        result = compute_salary(
            monthly_wage=float(monthly_wage),
            region=region,
            tenure_months=int(tenure_months),
        )
        return jsonify(result)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@ml_bp.route("/api/ml/minimum-wage", methods=["GET"])
def api_minimum_wage():
    region = request.args.get("region", "NCR")
    try:
        wage = get_minimum_wage(region)
        return jsonify({"region": region, "minimum_wage_monthly": wage})
    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@ml_bp.route("/api/ml/score-transaction", methods=["POST"])
def api_score_transaction():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    required_fields = [
        "amount", "amount_log", "amount_deviation",
        "velocity_24h", "velocity_7d", "hour_of_day",
        "is_weekend", "is_holiday", "balance_delta",
        "is_new_payee", "amount_ratio_to_avg",
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    result = ml_service.predict_fraud(data)
    if "error" in result:
        return jsonify(result), 503

    return jsonify(result)


@ml_bp.route("/api/ml/employer-risk", methods=["POST"])
def api_employer_risk():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    required_fields = [
        "payment_regularity", "wage_vs_min_ratio", "compliance_score",
        "turnover_rate", "complaint_count", "registered_employees",
        "total_disbursements",
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    result = ml_service.predict_employer_risk(data)
    if "error" in result:
        return jsonify(result), 503

    return jsonify(result)


@ml_bp.route("/api/ml/employee-risk", methods=["POST"])
def api_employee_risk():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    required_fields = [
        "region", "tenure_months", "monthly_wage",
        "dispute_count", "employment_months",
        "has_13th_month", "sss_paid", "philhealth_paid", "pagibig_paid",
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    result = ml_service.predict_employee_risk(data)
    if "error" in result:
        return jsonify(result), 503

    return jsonify(result)


@ml_bp.route("/api/ml/contract-safety", methods=["POST"])
def api_contract_safety():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    required_fields = [
        "push_count", "sstore_count", "sload_count", "call_count",
        "delegatecall_count", "selfdestruct_count",
        "callvalue_check", "reentrancy_guard", "has_events",
        "function_count", "state_var_count", "external_calls",
        "timestamp_usage", "assembly_usage",
    ]
    missing = [f for f in required_fields if f not in data]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    result = ml_service.predict_contract_safety(data)
    if "error" in result:
        return jsonify(result), 503

    return jsonify(result)


@ml_bp.route("/api/ml/validate-payout", methods=["POST"])
def api_validate_payout():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body required"}), 400

    monthly_wage = data.get("monthly_wage")
    region = data.get("region")
    to_address = data.get("to_address")
    if monthly_wage is None or region is None or to_address is None:
        return jsonify({"error": "monthly_wage, region, and to_address are required"}), 400

    salary_result = compute_salary(
        monthly_wage=float(monthly_wage),
        region=region,
        tenure_months=int(data.get("tenure_months", 12)),
    )

    ml_warnings = []
    employer_risk = data.get("employer_risk_features")
    if employer_risk:
        risk = ml_service.predict_employer_risk(employer_risk)
        if risk.get("risk_level") in ("medium", "high"):
            ml_warnings.append(f"Employer risk: {risk['risk_level']}")

    employee_risk = data.get("employee_risk_features")
    if employee_risk:
        risk = ml_service.predict_employee_risk(employee_risk)
        if risk.get("risk_level") in ("medium", "high"):
            ml_warnings.append(f"Employee risk: {risk['risk_level']}")

    approved = salary_result["compliance"]["minimum_wage_met"] and not salary_result["compliance"]["deduction_cap_enforced"]

    return jsonify({
        "approved": approved,
        "salary_breakdown": salary_result,
        "ml_warnings": ml_warnings,
        "compliance_flags": {
            "minimum_wage_met": salary_result["compliance"]["minimum_wage_met"],
            "deduction_cap_enforced": salary_result["compliance"]["deduction_cap_enforced"],
            "tax_exempt": salary_result["compliance"]["tax_exempt"],
        },
    })
