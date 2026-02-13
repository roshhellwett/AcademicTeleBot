import re
import unicodedata
from datetime import datetime
from core.config import TARGET_YEARS

# EXPANDED PATTERN: Matches "12-02-2026", "12 Feb 2026", "12th February 2026"
DATE_PATTERN = r"(?i)(\d{1,2})(?:st|nd|rd|th)?[\s\-\/\.]*([a-z]{3,10}|\d{1,2})[\s\-\/\.]*(\d{2,4})"

def extract_date(text: str):
    if not text: return None
    
    # Normalize text
    clean = unicodedata.normalize("NFKD", text)
    clean = " ".join(clean.split()).strip()

    # Search for date patterns
    matches = re.findall(DATE_PATTERN, clean)
    
    for day, month, year in matches:
        try:
            # Normalize Year (26 -> 2026)
            if len(year) == 2: year = f"20{year}"
            
            # Normalize Month (Feb -> 2, February -> 2)
            month_str = month.lower()
            if month_str.isdigit():
                m_num = int(month_str)
            else:
                # Map textual months
                months = {
                    'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
                    'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12
                }
                # Handle full names (february) by taking first 3 chars
                m_num = months.get(month_str[:3], 0)

            if m_num == 0: continue # Invalid month

            dt = datetime(int(year), m_num, int(day))

            # TARGET CHECK: Check against the list of valid years
            if dt.year in TARGET_YEARS:
                return dt

        except ValueError:
            continue
            
    return None
        #@academictelebotbyroshhellwett