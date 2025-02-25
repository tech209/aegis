import hashlib
import uuid
import json
import time

def generate_report_id():
    """Generates a unique report ID."""
    return str(uuid.uuid4())

def hash_credit_report(report_json):
    """Hashes the credit report JSON using SHA-256."""
    return hashlib.sha256(json.dumps(report_json, sort_keys=True).encode()).hexdigest()

def create_credit_snapshot(user_id, credit_score):
    """Creates a structured credit snapshot for blockchain submission."""
    timestamp = int(time.time())
    report_id = generate_report_id()
    
    report_data = {
        "user_id": user_id,
        "credit_score": credit_score,
        "timestamp": timestamp,
        "report_id": report_id
    }
    
    report_hash = hash_credit_report(report_data)
    
    return {
        "data": report_data,
        "hash": report_hash
    }
