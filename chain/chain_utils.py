import time
import json
import hashlib
import requests
from chain.db_handler import get_db

def create_block(block_type, data_dict):
    """Generic block creation function to store data on the blockchain."""
    db = get_db()
    blocks_table = db.table("blocks")

    # Get last block (if any)
    all_blocks = blocks_table.all()
    if all_blocks:
        # Sort by index to get highest
        all_blocks_sorted = sorted(all_blocks, key=lambda b: b['index'])
        previous_block = all_blocks_sorted[-1]
        index = previous_block['index'] + 1
        prev_hash = previous_block['hash']
    else:
        # Genesis block (first block in the chain)
        index = 0
        prev_hash = "0"

    # Define new block structure
    block = {
        "index": index,
        "timestamp": time.time(),
        "block_type": block_type,
        "data": data_dict,  # e.g., fingerprint, minted tokens
        "prev_hash": prev_hash
    }
    
    # Serialize & compute hash
    block_str = json.dumps(block, sort_keys=True)
    block_hash = hashlib.sha256(block_str.encode()).hexdigest()
    block["hash"] = block_hash

    return block

def broadcast_block(block, peers):
    """Send the new block to all known peers (decentralized sync)."""
    for peer in peers:
        try:
            url = f"{peer}/receive_block"
            resp = requests.post(url, json=block, timeout=5)
            print(f"Broadcasted block to {peer}, status={resp.status_code}")
        except Exception as e:
            print(f"Failed to broadcast to {peer}: {e}")

def get_local_chain():
    """Return entire blockchain (list of blocks) from local DB."""
    db = get_db()
    blocks_table = db.table("blocks")
    chain_data = blocks_table.all()
    # Sort by index to ensure correct order
    chain_data_sorted = sorted(chain_data, key=lambda b: b['index'])
    return chain_data_sorted

def replace_local_chain(new_chain):
    """Replace local blockchain with a validated new_chain."""
    db = get_db()
    blocks_table = db.table("blocks")
    blocks_table.purge()
    blocks_table.insert_multiple(new_chain)
