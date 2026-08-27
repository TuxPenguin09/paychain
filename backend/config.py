import os
from dotenv import load_dotenv

load_dotenv()

POLYGON_AMOY_RPC_URL = os.getenv(
    "POLYGON_AMOY_RPC_URL",
    "https://polygon-amoy-bor-rpc.publicnode.com",
)
POLYGON_AMOY_CHAIN_ID = 80002
PAYCHAIN_CONTRACT_ADDRESS = os.getenv("PAYCHAIN_CONTRACT_ADDRESS", "")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-me-in-production")
