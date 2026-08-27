# PayChain Smart Contracts

Salary disbursement platform for Filipino *kasambahay* (domestic workers), built with Hardhat 3 on **Polygon Amoy testnet**.

## Project Overview

- **PayChain.sol** — Core contract for salary management: employer registers employees, deposits MATIC, and records salary disbursements.
- **MockERC20.sol** — Simple ERC-20 mock for future stablecoin integration.
- Solidity 0.8.28 with Foundry-compatible unit tests and TypeScript integration tests.

## Usage

### Running Tests

```shell
npx hardhat test
```

Selectively run Solidity or Mocha tests:

```shell
npx hardhat test solidity
npx hardhat test mocha
```

### Typecheck

```shell
npx hardhat build && npx tsc --noEmit
```

### Deploy to Polygon Amoy

Set environment variables:

```shell
export POLYGON_AMOY_RPC_URL=https://polygon-amoy-bor-rpc.publicnode.com
export POLYGON_AMOY_PRIVATE_KEY=<your-deployer-private-key>
```

Deploy with Ignition:

```shell
npx hardhat ignition deploy ignition/modules/PayChain.ts --network polygonAmoy
```

### Deploy locally

```shell
npx hardhat ignition deploy ignition/modules/PayChain.ts
```
