import os
from tinydb import TinyDB

_db_instance = None

def init_db(port):
    """Initialize or load a TinyDB file for this node's chain."""
    global _db_instance
    db_path = f"chain_{port}.json"
    if not os.path.exists(db_path):
        open(db_path, 'a').close()  # Create empty file if missing
    _db_instance = TinyDB(db_path)

def get_db():
    """Return the database instance, ensuring it's initialized first."""
    global _db_instance
    if _db_instance is None:
        raise Exception("DB not initialized! Call init_db(port) first.")
    return _db_instance
