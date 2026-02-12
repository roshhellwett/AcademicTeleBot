import time

# Configuration
STRIKE_LIMIT = 3
MUTE_DURATION_SECONDS = 3600 # 1 Hour [cite: 61]

# In-memory strike storage: {user_id: count}
strike_records = {}

def add_strike(user_id: int) -> bool:
    """
    Increments strikes for a user. 
    Returns True if they hit the limit, False otherwise.
    """
    strike_records[user_id] = strike_records.get(user_id, 0) + 1
    if strike_records[user_id] >= STRIKE_LIMIT:
        strike_records[user_id] = 0 # Reset after mute
        return True
    return False