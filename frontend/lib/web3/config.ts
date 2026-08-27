export const POLYGON_AMOY = {
  chainId: 80002,
  chainIdHex: "0x13882",
  name: "Polygon Amoy Testnet",
  currency: "MATIC",
  rpcUrl: "https://polygon-amoy-bor-rpc.publicnode.com",
  blockExplorerUrl: "https://amoy.polygonscan.com",
} as const;

export const PAYCHAIN_CONTRACT_ADDRESS =
  process.env.EXPO_PUBLIC_PAYCHAIN_CONTRACT_ADDRESS ?? "";
