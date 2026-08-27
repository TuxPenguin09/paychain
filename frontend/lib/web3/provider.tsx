import React, { createContext, useContext, useState, useCallback, useEffect } from "react";
import { Platform } from "react-native";
import { BrowserProvider, JsonRpcSigner, Contract } from "ethers";
import { PAYCHAIN_CONTRACT_ADDRESS } from "./config";
import { PAYCHAIN_ABI } from "./contracts";

interface WalletState {
  address: string | null;
  provider: BrowserProvider | null;
  signer: JsonRpcSigner | null;
  contract: Contract | null;
  connected: boolean;
  connecting: boolean;
  balance: string;
  error: string | null;
}

interface WalletContextType extends WalletState {
  connectWallet: () => Promise<void>;
  disconnectWallet: () => void;
}

const WalletContext = createContext<WalletContextType>({
  address: null,
  provider: null,
  signer: null,
  contract: null,
  connected: false,
  connecting: false,
  balance: "0",
  error: null,
  connectWallet: async () => {},
  disconnectWallet: () => {},
});

const WALLET_KEY = "paychain_wallet_address";

declare global {
  interface Window {
    ethereum?: {
      isMetaMask?: boolean;
      request: (args: { method: string; params?: unknown[] }) => Promise<unknown>;
      on: (event: string, callback: (...args: unknown[]) => void) => void;
      removeListener: (event: string, callback: (...args: unknown[]) => void) => void;
    };
  }
}

const storage = {
  getItem: async (key: string): Promise<string | null> => {
    if (Platform.OS === "web" && typeof window !== "undefined") {
      return localStorage.getItem(key);
    }
    const SecureStore = await import("expo-secure-store");
    return SecureStore.getItemAsync(key);
  },
  setItem: async (key: string, value: string): Promise<void> => {
    if (Platform.OS === "web" && typeof window !== "undefined") {
      localStorage.setItem(key, value);
      return;
    }
    const SecureStore = await import("expo-secure-store");
    await SecureStore.setItemAsync(key, value);
  },
  deleteItem: async (key: string): Promise<void> => {
    if (Platform.OS === "web" && typeof window !== "undefined") {
      localStorage.removeItem(key);
      return;
    }
    const SecureStore = await import("expo-secure-store");
    await SecureStore.deleteItemAsync(key);
  },
};

export function Web3Provider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState<WalletState>({
    address: null,
    provider: null,
    signer: null,
    contract: null,
    connected: false,
    connecting: false,
    balance: "0",
    error: null,
  });

  const connectWallet = useCallback(async () => {
    setState((prev) => ({ ...prev, connecting: true, error: null }));

    try {
      if (Platform.OS === "web" && typeof window !== "undefined") {
        if (!window.ethereum) {
          setState((prev) => ({
            ...prev,
            connecting: false,
            error: "MetaMask not detected. Please install MetaMask to connect your wallet.",
          }));
          return;
        }

        const provider = new BrowserProvider(window.ethereum);
        const signer = await provider.getSigner();
        const address = await signer.getAddress();
        const balance = await provider.getBalance(address);

        let contract: Contract | null = null;
        if (PAYCHAIN_CONTRACT_ADDRESS) {
          contract = new Contract(PAYCHAIN_CONTRACT_ADDRESS, PAYCHAIN_ABI, signer);
        }

        await storage.setItem(WALLET_KEY, address);

        setState({
          address,
          provider,
          signer,
          contract,
          connected: true,
          connecting: false,
          balance: balance.toString(),
          error: null,
        });

        window.ethereum.on("accountsChanged", () => {
          disconnectWallet();
        });

        window.ethereum.on("chainChanged", () => {
          disconnectWallet();
        });
      } else {
        setState((prev) => ({
          ...prev,
          connecting: false,
          error: "Wallet connection is only available on web with MetaMask.",
        }));
      }
    } catch (error: unknown) {
      const message = error instanceof Error ? error.message : "Failed to connect wallet";
      console.error("Failed to connect wallet:", error);
      setState((prev) => ({ ...prev, connecting: false, error: message }));
    }
  }, []);

  const disconnectWallet = useCallback(() => {
    storage.deleteItem(WALLET_KEY);
    setState({
      address: null,
      provider: null,
      signer: null,
      contract: null,
      connected: false,
      connecting: false,
      balance: "0",
      error: null,
    });
  }, []);

  useEffect(() => {
    storage.getItem(WALLET_KEY).then((stored) => {
      if (stored && Platform.OS === "web" && window.ethereum) {
        connectWallet();
      }
    });
  }, [connectWallet]);

  return (
    <WalletContext.Provider value={{ ...state, connectWallet, disconnectWallet }}>
      {children}
    </WalletContext.Provider>
  );
}

export const useWallet = () => useContext(WalletContext);
