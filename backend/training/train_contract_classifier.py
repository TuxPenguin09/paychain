import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix

sys.path.insert(0, str(Path(__file__).parent.parent))

from training.generate_data import generate_contract_data


def train():
    print("=" * 60)
    print("Training Smart Contract Classifier (MultinomialNB)")
    print("=" * 60)

    df = generate_contract_data(n_samples=2000)
    print(f"\nDataset: {len(df)} samples, {df['is_vulnerable'].sum()} vulnerable")

    feature_cols = [
        "push_count", "sstore_count", "sload_count", "call_count",
        "delegatecall_count", "selfdestruct_count",
        "callvalue_check", "reentrancy_guard", "has_events",
        "function_count", "state_var_count", "external_calls",
        "timestamp_usage", "assembly_usage",
    ]

    X = df[feature_cols].values
    y = df["is_vulnerable"].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    X_train_nb = np.clip(X_train, 0, None).astype(int)
    X_test_nb = np.clip(X_test, 0, None).astype(int)

    model = MultinomialNB(alpha=1.0)
    model.fit(X_train_nb, y_train)

    y_pred = model.predict(X_test_nb)

    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, target_names=["Safe", "Vulnerable"]))

    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    cv_scores = cross_val_score(model, X_train_nb, y_train, cv=5, scoring="f1")
    print(f"\nCross-validation F1: {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")

    model_path = Path(__file__).parent.parent / "services" / "models"
    model_path.mkdir(exist_ok=True)
    joblib.dump(model, model_path / "contract_classifier.joblib")
    print(f"Model saved to {model_path / 'contract_classifier.joblib'}")

    return model


if __name__ == "__main__":
    train()
