import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline

sys.path.insert(0, str(Path(__file__).parent.parent))

from training.generate_data import generate_fraud_data


def train():
    print("=" * 60)
    print("Training Fraud Detection Model (GaussianNB)")
    print("=" * 60)

    df = generate_fraud_data(n_samples=3000, fraud_ratio=0.15)
    print(f"\nDataset: {len(df)} samples, {df['is_fraud'].sum()} fraud ({df['is_fraud'].mean():.1%})")

    feature_cols = [
        "amount", "amount_log", "amount_deviation",
        "velocity_24h", "velocity_7d", "hour_of_day",
        "is_weekend", "is_holiday", "balance_delta",
        "is_new_payee", "amount_ratio_to_avg",
    ]

    X = df[feature_cols].values
    y = df["is_fraud"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("classifier", GaussianNB(var_smoothing=1e-9)),
    ])

    pipeline.fit(X_train, y_train)

    y_pred = pipeline.predict(X_test)
    y_proba = pipeline.predict_proba(X_test)[:, 1]

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Legitimate", "Fraud"]))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    cv_scores = cross_val_score(pipeline, X, y, cv=5, scoring="f1")
    print(f"\nCross-validation F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    model_path = Path(__file__).parent.parent / "services" / "models"
    model_path.mkdir(exist_ok=True)
    joblib.dump(pipeline, model_path / "fraud_detector.joblib")
    print(f"\nModel saved to {model_path / 'fraud_detector.joblib'}")

    return pipeline


if __name__ == "__main__":
    train()
