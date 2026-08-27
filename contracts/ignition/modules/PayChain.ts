import { buildModule } from "@nomicfoundation/hardhat-ignition/modules";

export default buildModule("PayChainModule", (m) => {
  const paychain = m.contract("PayChain");

  return { paychain };
});
