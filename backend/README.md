# PayChain Backend

Flask backend for PayChain salary disbursement platform, targeting Filipino *kasambahay* on **Polygon Amoy testnet**.

## Structure

```
backend/
├── app.py                  Flask app entry point
├── config.py               Environment variables and configuration
├── requirements.txt        Python dependencies
├── models/                 Pydantic data models
│   ├── employee.py         Employee + EmployeeRiskFeatures
│   ├── employer.py         Employer + EmployerRiskFeatures
│   └── transaction.py      Transaction + TransactionFraudFeatures + FraudPrediction
├── routes/
│   └── ml.py               ML API blueprint (salary computation, fraud, risk, contract safety)
├── services/
│   ├── web3_service.py     Web3/Polygon blockchain interaction
│   ├── rule_engine.py      Philippine labor law rules (RA 10361)
│   └── ml_service.py       Naive Bayes classifiers (fraud, risk, contract)
├── training/               ML training pipeline
│   ├── generate_data.py    Synthetic data generation
│   ├── train_fraud_detector.py
│   ├── train_risk_scorer.py
│   ├── train_contract_classifier.py
│   └── data/               Generated CSV datasets
└── venv/                   Virtual environment (Windows-built, gitignored)
```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Train Models

```bash
python training/generate_data.py
python training/train_fraud_detector.py
python training/train_risk_scorer.py
python training/train_contract_classifier.py
```

## Configuration

Create `.env`:
```
POLYGON_AMOY_RPC_URL=https://polygon-amoy-bor-rpc.publicnode.com
POLYGON_AMOY_PRIVATE_KEY=your-deployer-private-key
PAYCHAIN_CONTRACT_ADDRESS=deployed-contract-address
JWT_SECRET_KEY=your-jwt-secret
```

## Run

```bash
python app.py
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info and blockchain status |
| GET | `/health` | Health check with block number |
| GET | `/api/contract/info` | PayChain contract details |
| POST | `/api/ml/compute-salary` | Compute compliant salary (rule engine) |
| GET | `/api/ml/minimum-wage?region=NCR` | Get regional minimum wage |
| POST | `/api/ml/score-transaction` | Fraud detection (Naive Bayes) |
| POST | `/api/ml/employer-risk` | Employer risk scoring |
| POST | `/api/ml/employee-risk` | Employee risk scoring |
| POST | `/api/ml/contract-safety` | Smart contract vulnerability analysis |
| POST | `/api/ml/validate-payout` | Combined rules + ML payout validation |
