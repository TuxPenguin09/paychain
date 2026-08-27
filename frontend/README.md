# PayChain Frontend

React Native (Expo SDK 54) frontend for the PayChain salary disbursement platform, targeting Filipino *kasambahay* on **Polygon Amoy testnet**. Supports **iOS, Android, and Web** from a single codebase.

## Setup

```bash
npm install
npx expo start
```

### Run on Web

```bash
npx expo start --web
```

Opens in browser at `http://localhost:8081`. MetaMask extension required for wallet connection.

### Run on Native

```bash
npx expo start --android
npx expo start --ios
```

> Wallet connection is currently web-only (MetaMask). Native apps show a message to use the web version.

### Web3 Dependencies

Install Web3 packages (run from Windows due to WSL limitations):

```bash
npm install ethers expo-secure-store
```

### Environment Variables

Create a `.env` file or set in `app.json` under `expo.extra`:

```
EXPO_PUBLIC_PAYCHAIN_CONTRACT_ADDRESS=your-deployed-contract-address
```

## Platform Support

| Feature | Web | iOS | Android |
|---------|-----|-----|---------|
| App shell + navigation | ✅ | ✅ | ✅ |
| Home screen | ✅ | ✅ | ✅ |
| Explore screen | ✅ | ✅ | ✅ |
| Wallet connection | ✅ MetaMask | ⚠️ Web only | ⚠️ Web only |
| LocalStorage persistence | ✅ | N/A | N/A |
| SecureStore persistence | N/A | ✅ | ✅ |

## Structure

```
frontend/
├── app/
│   ├── _layout.tsx          Root layout (Web3Provider wrapper)
│   ├── modal.tsx            Modal screen
│   └── (tabs)/
│       ├── _layout.tsx      Tab navigator (Home, Explore, Wallet)
│       ├── index.tsx        Home screen
│       ├── explore.tsx      Explore screen
│       └── wallet.tsx       Wallet connection screen (platform-aware)
├── lib/
│   └── web3/
│       ├── config.ts        Polygon Amoy chain config
│       ├── provider.tsx     Wallet context (localStorage on web, SecureStore on native)
│       └── contracts.ts     PayChain ABI
└── components/              Shared UI components
```

## Web3 Integration

- **ethers.js v6** — Wallet and contract interaction
- **Platform-aware storage** — `localStorage` on web, `expo-secure-store` on native
- **WalletContext** — React context providing `address`, `provider`, `signer`, `contract`, `connectWallet()`, `disconnectWallet()`, `error`
- **MetaMask events** — Listens for `accountsChanged` and `chainChanged` to auto-disconnect

The `useWallet()` hook provides all wallet state and actions.

## Network

- **Polygon Amoy Testnet** (Chain ID: 80002)
- RPC: `https://polygon-amoy-bor-rpc.publicnode.com`
- Explorer: `https://amoy.polygonscan.com`
