import logging
import sys
from core.config import LOG_LEVEL

def setup_logger():
    # Force UTF-8 encoding for Windows terminals to prevent UnicodeEncodeError
    if sys.platform.startswith('win'):
        # This reconfigures the standard output to handle emojis correctly
        sys.stdout.reconfigure(encoding='utf-8')

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

    logging.basicConfig(
        level=LOG_LEVEL,
        handlers=[handler]
    )
    
    # Silence noisy library logs
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)