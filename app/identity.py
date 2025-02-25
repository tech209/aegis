import hashlib
from chain.chain_utils import create_block
from chain.db_handler import get_db

def generate_fingerprint(phrase1, phrase2, biometric_proof):
    """Securely generate a user fingerprint from passphrases & biometrics."""
    combined = phrase1 + phrase2 + biometric_proof
    return hashlib.sha256(combined.encode()).hexdigest()

def register_identity_block(fingerprint, user_tokens, foundation_tokens, foundation_addr):
    """
    Create a 'user_identity' block awarding tokens to user + foundation.
    Returns the newly created block dict.
    """
    data = {
        "fingerprint": fingerprint,  # User's blockchain ID
        "mint": {
            "to_user": user_tokens,
            "to_foundation": foundation_tokens,
            "foundation_address": foundation_addr
        }
    }

    block = create_block("user_identity", data)
    db = get_db()
    db.table("blocks").insert(block)
    return block
