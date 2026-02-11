import logging
import sys
from core.config import LOG_LEVEL

def setup_logger():
    # Force UTF-8 encoding for Windows terminals
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
    if sys.platform.startswith('win'):
        # This fix allows emojis on Windows consoles
        import codecs
        sys.stdout.reconfigure(encoding='utf-8')

    logging.basicConfig(
        level=LOG_LEVEL,
        handlers=[handler]
    )
    
    # Silence noisy libraries
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)