# Backend — PayChain

Flask (Python) backend for the PayChain salary disbursement platform, targeting Filipino *kasambahay* on **Polygon Amoy testnet**.

## Environment

- `venv/` is a Windows-built Python 3.13 venv (untracked, gitignored). Cannot be used from Linux/WSL.
- Use `pip install -r requirements.txt` to document dependencies; actual installs happen on Windows.

## Dependencies

- Flask + Flask-CORS + Flask-JWT-Extended + Flask-SQLAlchemy for the REST API
- web3 + eth-account + eth-abi for Polygon Amoy blockchain interaction
- pydantic for request validation
- python-dotenv for .env loading
- scikit-learn + pandas + numpy + joblib for Naive Bayes ML classifiers

## Services

- `services/web3_service.py` — Connects to Polygon Amoy, interacts with the PayChain smart contract.
- `services/rule_engine.py` — Data-driven rule tables (pandas) for Philippine labor law compliance (Batas Kasambahay / RA 10361). Computes minimum wage, SSS, PhilHealth, Pag-IBIG, withholding tax, deduction caps.
- `services/ml_service.py` — Four Naive Bayes classifiers:
  - `FraudDetector` (GaussianNB) — Flags suspicious salary transactions
  - `EmployerRiskScorer` (GaussianNB) — Scores employer trustworthiness
  - `EmployeeRiskScorer` (GaussianNB) — Scores employee reliability
  - `ContractClassifier` (MultinomialNB) — Classifies smart contracts as safe/vulnerable

## ML Training

Training scripts and synthetic data generators are in `training/`:

```bash
python training/generate_data.py        # Generate synthetic CSV datasets
python training/train_fraud_detector.py # Train fraud detection model
python training/train_risk_scorer.py    # Train employer + employee risk models
python training/train_contract_classifier.py # Train contract classifier
```

Trained models are saved to `services/models/*.joblib`.

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API info |
| GET | `/health` | Health check |
| GET | `/api/contract/info` | PayChain contract details |
| POST | `/api/ml/compute-salary` | Compute compliant salary with deductions |
| GET | `/api/ml/minimum-wage?region=NCR` | Get regional minimum wage |
| POST | `/api/ml/score-transaction` | Score transaction for fraud risk |
| POST | `/api/ml/employer-risk` | Get employer risk score |
| POST | `/api/ml/employee-risk` | Get employee risk score |
| POST | `/api/ml/contract-safety` | Analyze smart contract for vulnerabilities |
| POST | `/api/ml/validate-payout` | Validate payout (rules + ML) |

## Configuration

All config is in `config.py`, loaded from `.env`:
- `POLYGON_AMOY_RPC_URL` — Polygon Amoy RPC endpoint
- `PAYCHAIN_CONTRACT_ADDRESS` — Deployed PayChain contract address
- `JWT_SECRET_KEY` — JWT signing key
