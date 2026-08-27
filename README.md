# PayChain

Salary disbursement platform for Filipino *kasambahay* (domestic workers), powered by blockchain. Built for the iACADEMY thesis.

## Overview

PayChain uses **Polygon Amoy testnet** to provide transparent, tamper-proof salary disbursement records for household workers and their employers.

## Architecture

```
paychain
├── backend/    Flask (Python) — REST API + blockchain service
├── contracts/  Hardhat 3 (Solidity) — PayChain smart contract on Polygon Amoy
└── frontend/   Expo SDK 54 (React Native) — Wallet connection + salary UI
```

### Network

- **Polygon Amoy Testnet** — Chain ID 80002
- RPC: `https://polygon-amoy-bor-rpc.publicnode.com`
- Explorer: `https://amoy.polygonscan.com`

## Setup

### contracts/

```bash
cd contracts
npm install
npx hardhat test
npx hardhat ignition deploy ignition/modules/PayChain.ts
```

### backend/

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

### frontend/

```bash
cd frontend
npm install
npm install ethers expo-secure-store
npx expo start
```

## Members

- Moritz Chester Saribay
- John Matthew De Leon
- Dylan Vitangcul

## License

iACADEMY Thesis Project
