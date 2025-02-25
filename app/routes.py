from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from web3 import Web3
import json
import hashlib
import time
from app.identity import generate_fingerprint

routes = Blueprint("routes", __name__)

# Connect to Hardhat's Local Testnet (No real ETH transactions)
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Load Hardhat Deployed Contract
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Replace with your deployed contract address
with open("artifacts/contracts/AegisCredit.sol/AegisCredit.json") as f:
    contract_abi = json.load(f)["abi"]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# 🌐 **Web Routes**
@routes.route('/')
def home():
    """Landing page."""
    return render_template("index.html")

@routes.route('/upload')
def upload_page():
    """Page for uploading a credit snapshot."""
    return render_template("upload.html")

@routes.route('/verify')
def verify_page():
    """Page for verifying a stored snapshot."""
    return render_template("verify.html")

@routes.route('/submission_success')
def submission_success():
    """Display transaction success details."""
    tx_hash = request.args.get("tx_hash")
    user_id = request.args.get("user_id")
    return render_template("submission_success.html", tx_hash=tx_hash, user_id=user_id)

# 🔗 **Blockchain API Routes**
@routes.route('/upload_credit_report', methods=['POST'])
def upload_credit_report():
    """Hashes and submits a credit snapshot directly to Hardhat blockchain."""
    data = request.json
    phrase1 = data.get("phrase1")
    phrase2 = data.get("phrase2")
    biometric_proof = data.get("biometric_proof")
    credit_score = data.get("credit_score")

    if not phrase1 or not phrase2 or not biometric_proof or not credit_score:
        return jsonify({"error": "Missing required fields"}), 400

    # 🔑 Generate user fingerprint
    user_id = generate_fingerprint(phrase1, phrase2, biometric_proof)

    # 🔒 Hash credit score for security
    hashed_score = hashlib.sha256(str(credit_score).encode()).hexdigest()

    # 🚀 Check if fingerprint already exists in Hardhat
    try:
        existing_snapshot = contract.functions.getCreditSnapshotByFingerprint(user_id).call()
        if existing_snapshot[1] != 0:  # If creditScore is nonzero, fingerprint exists
            return jsonify({
                "message": "Duplicate submission detected. Redirecting to verify.",
                "redirect_url": url_for('routes.verify_page', user_id=user_id)
            })
    except:
        pass  # No data found, safe to continue submission

    # 🚀 Call Hardhat contract function
    tx_hash = contract.functions.storeCreditSnapshot(
        int(credit_score), hashed_score, user_id
    ).transact({
        "from": w3.eth.accounts[0]
    })

    # ✅ Wait for the transaction to be mined
    tx_receipt = None
    while tx_receipt is None:
        try:
            tx_receipt = w3.eth.get_transaction_receipt(tx_hash)
        except:
            time.sleep(1)  # Wait before retrying

    return jsonify({
        "message": "Credit snapshot stored on Hardhat testnet",
        "redirect_url": url_for('routes.submission_success', tx_hash=tx_receipt.transactionHash.hex(), user_id=user_id)
    })

@routes.route('/get_chain', methods=['GET'])
def get_chain():
    """Retrieve blockchain data from Hardhat testnet."""
    total_blocks = contract.functions.getTotalBlocks().call()
    chain_data = [contract.functions.getBlock(i).call() for i in range(total_blocks)]
    return jsonify(chain_data)

@routes.route('/get_credit_report', methods=['POST'])
def get_credit_report():
    """Retrieves a stored credit snapshot using the fingerprint (user_id)."""
    data = request.json
    user_id = data.get("user_id")

    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    # Query the blockchain
    snapshot = contract.functions.getCreditSnapshotByFingerprint(user_id).call()

    return jsonify({
        "user_address": snapshot[0],
        "credit_score": snapshot[1],
        "timestamp": snapshot[2],
        "report_hash": snapshot[3]
    })
