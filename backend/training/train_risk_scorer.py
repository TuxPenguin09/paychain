import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB, CategoricalNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.pipeline import Pipeline

sys.path.insert(0, str(Path(__file__).parent.parent))

from training.generate_data import generate_employer_risk_data, generate_employee_risk_data


def train_employer_risk():
    print("=" * 60)
    print("Training Employer Risk Scorer (GaussianNB)")
    print("=" * 60)

    df = generate_employer_risk_data(n_samples=2000)
    print(f"\nDataset: {len(df)} samples")

    feature_cols = [
        "payment_regularity", "wage_vs_min_ratio", "compliance_score",
        "turnover_rate", "complaint_count", "registered_employees",
        "total_disbursements",
    ]

    X = df[feature_cols].values
    y = df["risk_level"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", GaussianNB(var_smoothing=1e-8)),
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    risk_labels = {0: "Low", 1: "Medium", 2: "High"}
    target_names = [risk_labels[i] for i in sorted(risk_labels.keys())]

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=target_names))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="f1_weighted")
    print(f"\nCross-validation F1 (weighted): {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    model_path = Path(__file__).parent.parent / "services" / "models"
    model_path.mkdir(exist_ok=True)
    joblib.dump(pipeline, model_path / "employer_risk_scorer.joblib")
    print(f"Model saved to {model_path / 'employer_risk_scorer.joblib'}")

    return pipeline


def train_employee_risk():
    print("\n" + "=" * 60)
    print("Training Employee Risk Scorer (CategoricalNB)")
    print("=" * 60)

    df = generate_employee_risk_data(n_samples=2000)
    print(f"\nDataset: {len(df)} samples")

    region_encoder = LabelEncoder()
    df["region_encoded"] = region_encoder.fit_transform(df["region"])

    feature_cols = [
        "region_encoded", "tenure_months", "monthly_wage",
        "dispute_count", "employment_months",
        "has_13th_month", "sss_paid", "philhealth_paid", "pagibig_paid",
    ]

    X = df[feature_cols].values
    y = df["risk_level"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", GaussianNB(var_smoothing=1e-7)),
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)

    risk_labels = {0: "Low", 1: "Medium", 2: "High"}
    target_names = [risk_labels[i] for i in sorted(risk_labels.keys())]

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=target_names))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="f1_weighted")
    print(f"\nCross-validation F1 (weighted): {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    model_path = Path(__file__).parent.parent / "services" / "models"
    model_path.mkdir(exist_ok=True)
    joblib.dump(pipeline, model_path / "employee_risk_scorer.joblib")
    joblib.dump(region_encoder, model_path / "region_encoder.joblib")
    print(f"Models saved to {model_path / 'employee_risk_scorer.joblib'}")

    return pipeline


if __name__ == "__main__":
    train_employer_risk()
    train_employee_risk()
