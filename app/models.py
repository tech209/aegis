from web3 import Web3
import json

# Connect to Hardhat local node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Use the deployed contract address from Hardhat
contract_address = "0x5FbDB2315678afecb367f032d93F642f64180aa3"  # Replace with your actual deployed address

# Load ABI from Hardhat artifacts
with open("artifacts/contracts/AegisCredit.sol/AegisCredit.json") as f:
    contract_abi = json.load(f)["abi"]

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

def submit_credit_snapshot(user_address, credit_score, report_hash):
    """Sends a transaction to store a credit snapshot"""
    txn = contract.functions.storeCreditSnapshot(credit_score, report_hash).build_transaction({
        "from": user_address,
        "gas": 1000000,
        "gasPrice": w3.to_wei("5", "gwei"),
        "nonce": w3.eth.get_transaction_count(user_address)
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key="0xYOUR_PRIVATE_KEY")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return w3.to_hex(tx_hash)

def store_credit_snapshot(user_address, credit_score, report_hash):
    """Sends a transaction to store a credit snapshot"""
    txn = contract.functions.storeCreditSnapshot(credit_score, report_hash).build_transaction({
        "from": user_address,
        "gas": 1000000,
        "gasPrice": w3.to_wei("5", "gwei"),
        "nonce": w3.eth.get_transaction_count(user_address)
    })

    signed_txn = w3.eth.account.sign_transaction(txn, private_key="0xYOUR_PRIVATE_KEY")
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    return w3.to_hex(tx_hash)

def get_credit_snapshot(user_address):
    """Fetches a credit snapshot from the blockchain"""
    return contract.functions.getCreditSnapshot(user_address).call()

def verify_credit_snapshot(user_address, expected_hash):
    """Verifies if a stored credit snapshot matches the expected hash"""
    snapshot = get_credit_snapshot(user_address)
    if not snapshot:
        return {"error": "No snapshot found"}

    actual_hash = snapshot[3]  # Assuming snapshot[3] is the stored hash
    return {
        "verified": actual_hash == expected_hash,
        "snapshot": snapshot
    }
