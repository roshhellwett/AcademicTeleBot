import time
from collections import deque

# Configuration for Supreme Flood Control
MAX_MESSAGES = 5          # Max messages allowed in the time window
TIME_WINDOW = 10          # Time window in seconds
DUPLICATE_LIMIT = 2       # How many times the exact same message can be sent

# User activity storage: {user_id: [timestamps]}
user_history = {}
# Duplicate message storage: {user_id: {"text": str, "count": int}}
user_duplicates = {}

def is_flooding(user_id: int, message_text: str) -> (bool, str):
    """
    Checks if a user is flooding or repeating messages.
    """
    now = time.time()
    
    # --- 1. Flood Detection (Frequency) ---
    if user_id not in user_history:
        user_history[user_id] = deque()
    
    timestamps = user_history[user_id]
    timestamps.append(now)
    
    # Remove timestamps outside the window
    while timestamps and timestamps[0] < now - TIME_WINDOW:
        timestamps.popleft()
    
    if len(timestamps) > MAX_MESSAGES:
        return True, "Spamming (Message Flooding)"

    # --- 2. Duplicate Detection (Repetition) ---
    text_clean = message_text.lower().strip()
    if user_id not in user_duplicates:
        user_duplicates[user_id] = {"text": "", "count": 0}
    
    if user_duplicates[user_id]["text"] == text_clean:
        user_duplicates[user_id]["count"] += 1
    else:
        user_duplicates[user_id]["text"] = text_clean
        user_duplicates[user_id]["count"] = 1
        
    if user_duplicates[user_id]["count"] > DUPLICATE_LIMIT:
        return True, "Spamming (Repeated Content)"

    return False, None