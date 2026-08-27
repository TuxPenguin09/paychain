# Hardhat + ethers project

## Project layout

```
contracts/        Solidity source files (*.sol) and unit tests (*.t.sol)
test/             TypeScript integration tests and Solidity unit tests (*.sol)
ignition/         Hardhat Ignition deployment modules
scripts/          Standalone scripts run with `hardhat run`
hardhat.config.ts
```

## PayChain contracts

Salary disbursement platform for Filipino *kasambahay* (domestic workers) on **Polygon Amoy testnet**.

- `PayChain.sol` — Main contract: employer registers employees, deposits MATIC, records salary disbursements.
- `MockERC20.sol` — Simple ERC-20 mock for future stablecoin testing.

## Working in this project

When writing or modifying tests, configuring `hardhat.config.ts`, or interacting with the network from TypeScript, invoke the **`hardhat`** skill. It covers Solidity and TypeScript testing, how to choose between them, `forge-std` cheatcodes, the `network.create()` API, `networkHelpers`, and the compile-then-typecheck workflow. The skill itself points to the matching `hardhat-toolbox-*` skill for toolbox-specific guidance (signers, contract interaction, assertions).

## Docs

- Hardhat 3 — https://hardhat.org/llms.txt
- ethers.js — https://docs.ethers.org/v6/
- Polygon Amoy — https://polygon.technology/blog/polygon-amoy-testnet-launch
