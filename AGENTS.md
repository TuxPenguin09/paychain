# PayChain

Salary disbursement platform powered by blockchain (iACADEMY thesis). Three independent subprojects — no root build tooling, no CI, no root manifests. Each subproject has its own `package.json`/`node_modules`; work inside the relevant directory.

## Git policy (hard rule)

Do NOT use any Git commands that write or alter repository history: no `commit`, `push`, `pull`/`fetch` with writes, `rebase`, `reset`, `stash`, `tag`, `checkout -b`, or branch operations. Read-only Git commands (e.g. `status`, `log`, `diff`) are allowed. Make file edits only and leave all Git state to the user.

## backend/ — Flask (Python)

- Fresh stub: `app.py`, `models/`, `routes/`, `services/` are empty placeholders; there is no `requirements.txt` and nothing runnable yet. Don't invent dependencies or setup.
- `venv/` is a Windows-built Python 3.13 venv (untracked, gitignored). Do not try to use it from this Linux/WSL environment; don't treat it as a working environment.

## contracts/ — Hardhat 3

- Read `contracts/AGENTS.md` first: it points to the local `hardhat` skill (`.agents/skills/`) covering Solidity `.t.sol` unit tests vs TypeScript mocha tests, the compile-then-typecheck workflow, and `network.create()`.
- Commands: `npx hardhat test` (run one layer with `npx hardhat test solidity` or `npx hardhat test mocha`), deploy with `npx hardhat ignition deploy ignition/modules/<name>.ts`.
- This is Hardhat **3**, not v2 — `hardhat.config.ts` uses `defineConfig`/`configVariable`, and Sepolia requires `SEPOLIA_RPC_URL` + `SEPOLIA_PRIVATE_KEY` config variables. Solidity 0.8.28; a `production` build profile (optimizer on) is defined.

## frontend/ — Expo SDK 54 (React Native 0.81)

- Read `frontend/AGENTS.md`: consult the exact versioned Expo docs (`https://docs.expo.dev/versions/v54.0.0/`) before writing code — this is a newer SDK and APIs have changed.
- expo-router file-based routing (`app/`), typed routes and React Compiler experiments enabled in `app.json` (`"newArchEnabled": true`).
- Still the untouched create-expo-app starter. `npm run reset-project` wipes/moves the starter layout — do not run it.
- Lint: `npm run lint` (runs `expo lint`). No typecheck script is defined.