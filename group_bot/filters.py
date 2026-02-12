import re
import unicodedata
from group_bot.word_list import BANNED_WORDS, SPAM_DOMAINS

def is_inappropriate(text: str) -> (bool, str):
    """
    Zenith Multi-lingual forensic scan.
    Handles English, Hindi, and Bengali scripts simultaneously. [cite: 41, 42]
    """
    if not text:
        return False, None

    # Normalization to catch variants and fix encoding artifacts 
    normalized_text = unicodedata.normalize("NFKD", text).lower()
    
    # Forensic Abuse Detection using Word Boundaries
    # This prevents accidental deletion of innocent words 
    abuse_pattern = r"(?i)\b(" + "|".join(re.escape(word) for word in BANNED_WORDS) + r")\b"
    
    if re.search(abuse_pattern, normalized_text):
        return True, "Abusive/Inappropriate Language"

    # Smart Link Protection 
    if "makaut" not in normalized_text:
        for domain in SPAM_DOMAINS:
            if domain in normalized_text:
                return True, "Unauthorized/Suspicious Link"

    return False, None