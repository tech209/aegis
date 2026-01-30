from web3 import Web3
import json

# Connect to Hardhat local node
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

# Deployed contract address - update after running deploy.js
CONTRACT_ADDRESS = "0x5FbDB2315678afecb367f032d93F642f64180aa3"

# Load ABI from Hardhat artifacts
with open("artifacts/contracts/CreditSnapshotNFT.sol/CreditSnapshotNFT.json") as f:
    contract_abi = json.load(f)["abi"]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=contract_abi)


def mint_snapshot(wallet_address, credit_score):
    """Mint a credit snapshot NFT to the given wallet address."""
    tx_hash = contract.functions.mint(
        wallet_address, int(credit_score)
    ).transact({"from": w3.eth.accounts[0]})

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

    # Extract token ID from SnapshotMinted event
    logs = contract.events.SnapshotMinted().process_receipt(receipt)
    token_id = logs[0]["args"]["tokenId"] if logs else None

    return {
        "tx_hash": receipt.transactionHash.hex(),
        "token_id": token_id,
    }


def get_snapshot(token_id):
    """Get snapshot data for a specific token ID."""
    credit_score, timestamp, owner = contract.functions.getSnapshot(int(token_id)).call()
    return {
        "token_id": int(token_id),
        "credit_score": credit_score,
        "timestamp": timestamp,
        "owner": owner,
    }


def get_snapshots_by_owner(wallet_address):
    """Get all snapshots for a wallet address."""
    token_ids, scores, timestamps = contract.functions.getSnapshotsByOwner(wallet_address).call()
    return [
        {"token_id": tid, "credit_score": score, "timestamp": ts}
        for tid, score, ts in zip(token_ids, scores, timestamps)
    ]
