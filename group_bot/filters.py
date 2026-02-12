import re

# Comprehensive list of inappropriate patterns
# Includes common abuses, NSFW keywords, and suspicious link patterns
INAPPROPRIATE_KEYWORDS = [
    r"(?i)\b(abuse1|abuse2|slang1)\b", # Add specific abusive words here
    r"(?i)\b(porn|sex|dating|casino|bet|crypto-earn)\b",
]

# Patterns for suspicious/spam links (non-educational)
SPAM_LINK_PATTERNS = [
    r"t\.me/joinchat", # Prevents invite link spam
    r"bit\.ly", r"goo\.gl", r"t\.co", # Shortened links often used for phishing
    r"(?i).*(whatsapp\.com/join).*",
]

def is_inappropriate(text: str) -> (bool, str):
    """
    Checks if a message is abusive or contains inappropriate links.
    Returns (True, Reason) if caught, else (False, None).
    """
    if not text:
        return False, None

    # 1. Check for Abuses/NSFW
    for pattern in INAPPROPRIATE_KEYWORDS:
        if re.search(pattern, text):
            return True, "Abusive/Inappropriate Language"

    # 2. Check for Spam Links
    # Allow university links but block generic spam
    if "makaut" not in text.lower():
        for pattern in SPAM_LINK_PATTERNS:
            if re.search(pattern, text):
                return True, "Unauthorized/Suspicious Link"

    return False, None