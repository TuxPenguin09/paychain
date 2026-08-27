import React from "react";
import { StyleSheet, View, TouchableOpacity, Platform, Linking } from "react-native";
import { ThemedText } from "@/components/themed-text";
import { ThemedView } from "@/components/themed-view";
import { useWallet } from "@/lib/web3/provider";
import { POLYGON_AMOY } from "@/lib/web3/config";

export default function WalletScreen() {
  const { address, connected, connecting, balance, error, connectWallet, disconnectWallet } =
    useWallet();

  const formatAddress = (addr: string) => `${addr.slice(0, 6)}...${addr.slice(-4)}`;

  const formatBalance = (bal: string) => {
    try {
      const wei = BigInt(bal);
      const ether = Number(wei) / 1e18;
      return ether.toFixed(4);
    } catch {
      return "0.0000";
    }
  };

  const openMetaMask = () => {
    if (Platform.OS === "web") {
      window.open("https://metamask.io/download/", "_blank");
    }
  };

  return (
    <ThemedView style={styles.container}>
      <ThemedText type="title" style={styles.title}>
        Wallet
      </ThemedText>
      <ThemedText style={styles.subtitle}>
        {POLYGON_AMOY.name} — Chain ID {POLYGON_AMOY.chainId}
      </ThemedText>

      {!connected ? (
        <View style={styles.center}>
          {Platform.OS === "web" ? (
            <>
              <ThemedText style={styles.description}>
                Connect your MetaMask wallet to interact with PayChain on Polygon.
              </ThemedText>
              {error && (
                <View style={styles.errorBox}>
                  <ThemedText style={styles.errorText}>{error}</ThemedText>
                  {!window.ethereum && (
                    <TouchableOpacity style={styles.installButton} onPress={openMetaMask}>
                      <ThemedText style={styles.installButtonText}>Install MetaMask</ThemedText>
                    </TouchableOpacity>
                  )}
                </View>
              )}
              <TouchableOpacity
                style={[styles.connectButton, connecting && styles.connectButtonDisabled]}
                onPress={connectWallet}
                disabled={connecting}
              >
                <ThemedText style={styles.connectButtonText}>
                  {connecting ? "Connecting..." : "Connect MetaMask"}
                </ThemedText>
              </TouchableOpacity>
            </>
          ) : (
            <>
              <ThemedText style={styles.description}>
                Wallet connection is currently only available on the web version of PayChain.
              </ThemedText>
              <ThemedText style={styles.nativeHint}>
                Open PayChain in a web browser to connect your MetaMask wallet.
              </ThemedText>
            </>
          )}
        </View>
      ) : (
        <View style={styles.card}>
          <View style={styles.cardHeader}>
            <ThemedText type="subtitle">Connected</ThemedText>
            <View style={styles.connectedDot} />
          </View>
          <ThemedText style={styles.address}>{formatAddress(address!)}</ThemedText>

          <View style={styles.divider} />

          <ThemedText type="subtitle">Balance</ThemedText>
          <ThemedText style={styles.balance}>
            {formatBalance(balance)} MATIC
          </ThemedText>

          <View style={styles.divider} />

          <View style={styles.infoRow}>
            <ThemedText style={styles.infoLabel}>Network</ThemedText>
            <ThemedText style={styles.infoValue}>{POLYGON_AMOY.name}</ThemedText>
          </View>
          <View style={styles.infoRow}>
            <ThemedText style={styles.infoLabel}>RPC</ThemedText>
            <ThemedText style={styles.infoValue} numberOfLines={1}>
              {POLYGON_AMOY.rpcUrl}
            </ThemedText>
          </View>
          <View style={styles.infoRow}>
            <ThemedText style={styles.infoLabel}>Explorer</ThemedText>
            <ThemedText style={styles.infoValue} numberOfLines={1}>
              {POLYGON_AMOY.blockExplorerUrl}
            </ThemedText>
          </View>

          <TouchableOpacity style={styles.disconnectButton} onPress={disconnectWallet}>
            <ThemedText style={styles.disconnectButtonText}>Disconnect</ThemedText>
          </TouchableOpacity>
        </View>
      )}
    </ThemedView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
    paddingTop: 60,
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    opacity: 0.6,
    marginBottom: 32,
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    gap: 20,
  },
  description: {
    textAlign: "center",
    opacity: 0.7,
    paddingHorizontal: 20,
  },
  nativeHint: {
    textAlign: "center",
    opacity: 0.5,
    fontSize: 13,
    paddingHorizontal: 40,
  },
  errorBox: {
    backgroundColor: "rgba(239, 68, 68, 0.1)",
    borderRadius: 12,
    padding: 16,
    width: "100%",
    alignItems: "center",
    gap: 12,
  },
  errorText: {
    color: "#EF4444",
    fontSize: 14,
    textAlign: "center",
  },
  installButton: {
    backgroundColor: "#F6851B",
    paddingVertical: 10,
    paddingHorizontal: 20,
    borderRadius: 8,
  },
  installButtonText: {
    color: "#FFFFFF",
    fontSize: 14,
    fontWeight: "600",
  },
  connectButton: {
    backgroundColor: "#7C3AED",
    paddingVertical: 16,
    paddingHorizontal: 32,
    borderRadius: 12,
    width: "100%",
    alignItems: "center",
  },
  connectButtonDisabled: {
    opacity: 0.6,
  },
  connectButtonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
  card: {
    backgroundColor: "rgba(124, 58, 237, 0.08)",
    borderRadius: 16,
    padding: 24,
    gap: 8,
  },
  cardHeader: {
    flexDirection: "row",
    alignItems: "center",
    gap: 8,
  },
  connectedDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    backgroundColor: "#22C55E",
  },
  address: {
    fontSize: 16,
    fontFamily: "monospace",
    opacity: 0.8,
  },
  divider: {
    height: 1,
    backgroundColor: "rgba(0,0,0,0.1)",
    marginVertical: 12,
  },
  balance: {
    fontSize: 24,
    fontWeight: "bold",
    color: "#7C3AED",
  },
  infoRow: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingVertical: 4,
  },
  infoLabel: {
    fontSize: 13,
    opacity: 0.5,
  },
  infoValue: {
    fontSize: 13,
    opacity: 0.7,
    maxWidth: "60%",
  },
  disconnectButton: {
    marginTop: 16,
    paddingVertical: 12,
    alignItems: "center",
    borderRadius: 8,
    borderWidth: 1,
    borderColor: "rgba(0,0,0,0.15)",
  },
  disconnectButtonText: {
    opacity: 0.7,
    fontSize: 14,
  },
});
