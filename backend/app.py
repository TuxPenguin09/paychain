from flask import Flask, jsonify
from flask_cors import CORS
from config import PAYCHAIN_CONTRACT_ADDRESS, POLYGON_AMOY_RPC_URL, JWT_SECRET_KEY
from services.web3_service import web3_service
from routes.ml import ml_bp

app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY
CORS(app)

app.register_blueprint(ml_bp)


@app.route("/")
def index():
    return jsonify({
        "name": "PayChain API",
        "version": "1.0.0",
        "network": "Polygon Amoy",
        "rpc_url": POLYGON_AMOY_RPC_URL,
        "contract_address": PAYCHAIN_CONTRACT_ADDRESS,
        "blockchain_connected": web3_service.connected,
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "blockchain_connected": web3_service.connected,
        "block_number": web3_service.get_block_number() if web3_service.connected else None,
    })


@app.route("/api/contract/info")
def contract_info():
    return jsonify({
        "contract_address": PAYCHAIN_CONTRACT_ADDRESS,
        "owner": web3_service.get_contract_owner(),
        "total_deposited": web3_service.get_total_deposited(),
    })


if __name__ == "__main__":
    app.run(debug=True)
