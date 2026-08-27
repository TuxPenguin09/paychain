# Expo + Web3 for PayChain

Read the exact versioned docs at https://docs.expo.dev/versions/v54.0.0/ before writing any code.

## Platform Support

Expo SDK 54 supports **iOS, Android, and Web** from a single codebase. Run with `npx expo start --web` for browser, or `--android`/`--ios` for native.

## Web3 Stack

- **ethers.js v6** for wallet/signer/contract interaction (matches contracts project)
- **Platform-aware storage** — `localStorage` on web, `expo-secure-store` on native (imported dynamically to avoid web crashes)
- **Web3Provider** wraps the root layout in `app/_layout.tsx`
- **useWallet()** hook from `@/lib/web3/provider` provides: `address`, `provider`, `signer`, `contract`, `connected`, `connecting`, `error`, `connectWallet()`, `disconnectWallet()`

## Web vs Native Differences

- **Web**: Wallet connection via `window.ethereum` (MetaMask). Storage uses `localStorage`.
- **Native**: Shows message to use web version. Storage uses `expo-secure-store`.
- **Never import `expo-secure-store` at top level** — use dynamic `import()` inside platform checks to avoid web crashes.

## Polygon Amoy Testnet

- Chain ID: `80002` (hex `0x13882`)
- RPC: `https://polygon-amoy-bor-rpc.publicnode.com`
- Explorer: `https://amoy.polygonscan.com`
- Contract address set via `EXPO_PUBLIC_PAYCHAIN_CONTRACT_ADDRESS`

## Path Alias

`@/` maps to the project root (`./`), configured in `tsconfig.json`.
