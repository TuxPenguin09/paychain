# PayChain

Salary disbursement platform powered by blockchain (iACADEMY thesis). Three independent subprojects — no root build tooling, no CI, no root manifests. Each subproject has its own `package.json`/`node_modules`; work inside the relevant directory.

## Target

Filipino *kasambahay* (domestic/household workers) — transparent salary disbursement using **Polygon Amoy testnet** (Chain ID 80002).

## Git policy (hard rule)

Do NOT use any Git commands that write or alter repository history: no `commit`, `push`, `pull`/`fetch` with writes, `rebase`, `reset`, `stash`, `tag`, `checkout -b`, or branch operations. Read-only Git commands (e.g. `status`, `log`, `diff`) are allowed. Make file edits only and leave all Git state to the user.

## Web3 stack

| Project | Language | Web3 Library | Purpose |
|---------|----------|-------------|---------|
| `contracts/` | Solidity | forge-std (tests) | PayChain smart contract on Polygon |
| `backend/` | Python | web3.py 7.x | Server-side blockchain interaction |
| `frontend/` | TypeScript | ethers.js v6 | Wallet connection + contract UI |

## backend/ — Flask (Python)

- `app.py` — Flask entry point with blockchain-aware API endpoints.
- `config.py` — Centralized env config (POLYGON_AMOY_RPC_URL, PAYCHAIN_CONTRACT_ADDRESS).
- `services/web3_service.py` — Web3 service: connects to Polygon Amoy, interacts with PayChain contract.
- `services/rule_engine.py` — Data-driven rule tables (pandas) for Philippine labor law compliance (Batas Kasambahay / RA 10361). Computes minimum wage, SSS, PhilHealth, Pag-IBIG, withholding tax, deduction caps.
- `services/ml_service.py` — Four Naive Bayes classifiers: FraudDetector (GaussianNB), EmployerRiskScorer (GaussianNB), EmployeeRiskScorer (GaussianNB), ContractClassifier (MultinomialNB).
- `training/` — Synthetic data generation + model training scripts. Trained models saved to `services/models/*.joblib`.
- `requirements.txt` — Python dependencies (flask, web3, eth-account, pydantic, scikit-learn, pandas, numpy, joblib).
- `venv/` is a Windows-built Python 3.13 venv (untracked, gitignored). Do not try to use it from this Linux/WSL environment.

## contracts/ — Hardhat 3

- Read `contracts/AGENTS.md` first: it points to the local `hardhat` skill (`.agents/skills/`) covering Solidity `.t.sol` unit tests vs TypeScript mocha tests, the compile-then-typecheck workflow, and `network.create()`.
- Commands: `npx hardhat test` (run one layer with `npx hardhat test solidity` or `npx hardhat test mocha`), deploy with `npx hardhat ignition deploy ignition/modules/<name>.ts`.
- This is Hardhat **3**, not v2 — `hardhat.config.ts` uses `defineConfig`/`configVariable`, and Polygon Amoy requires `POLYGON_AMOY_RPC_URL` + `POLYGON_AMOY_PRIVATE_KEY` config variables. Solidity 0.8.28; a `production` build profile (optimizer on) is defined.
- `contracts/PayChain.sol` — Core salary disbursement contract: employer registers employees, deposits MATIC, records salary disbursements.
- `contracts/MockERC20.sol` — Simple ERC-20 mock for future stablecoin testing.

## frontend/ — Expo SDK 54 (React Native 0.81)

- Read `frontend/AGENTS.md`: consult the exact versioned Expo docs (`https://docs.expo.dev/versions/v54.0.0/`) before writing code — this is a newer SDK and APIs have changed.
- Supports **iOS, Android, and Web** from a single codebase (`npx expo start --web` for browser).
- expo-router file-based routing (`app/`), typed routes and React Compiler experiments enabled in `app.json` (`"newArchEnabled": true`).
- `npm run reset-project` wipes/moves the starter layout — do not run it.
- Lint: `npm run lint` (runs `expo lint`). No typecheck script is defined.
- Web3: `ethers` + `expo-secure-store` (install from Windows: `npm install ethers expo-secure-store`).
- `lib/web3/provider.tsx` — Web3Provider wrapping the app, `useWallet()` hook for wallet state. Uses `localStorage` on web, `expo-secure-store` on native (dynamic import to avoid web crashes).
- `app/(tabs)/wallet.tsx` — Wallet connection screen (platform-aware: MetaMask on web, message on native).
- Contract address via `EXPO_PUBLIC_PAYCHAIN_CONTRACT_ADDRESS` env var.
