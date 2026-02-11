import io
import pdfplumber
import requests
import logging
from scraper.date_extractor import extract_date

logger = logging.getLogger("PDF_PROCESSOR")

def get_date_from_pdf(pdf_url):
    """Enhanced PDF reader for MAKAUT Exam portal links."""
    try:
        # Use a full request instead of stream=True for more stable file delivery
        response = requests.get(
            pdf_url, 
            timeout=20, 
            verify=False,
            headers={"User-Agent": "Mozilla/5.0"} # Prevents some server blocks
        )
        
        if response.status_code != 200:
            return None

        # Wrap the full content in a Byte stream
        with pdfplumber.open(io.BytesIO(response.content)) as pdf:
            if not pdf.pages:
                return None
                
            first_page = pdf.pages[0]
            width, height = first_page.width, first_page.height
            
            # 1. PRIORITY: TOP RIGHT (Box: Top 25%, Right 50%)
            top_right_box = (width * 0.5, 0, width, height * 0.25)
            top_right_text = first_page.within_bbox(top_right_box).extract_text()
            date = extract_date(top_right_text)
            if date: return date

            # 2. SECONDARY: BOTTOM SIGNATURE (Bottom 15%)
            bottom_box = (0, height * 0.85, width, height)
            bottom_text = first_page.within_bbox(bottom_box).extract_text()
            date = extract_date(bottom_text)
            if date: return date

            # 3. FALLBACK: Full Page Search
            return extract_date(first_page.extract_text())
            
    except Exception as e:
        # Only log major failures, ignore minor file structure warnings
        if "No /Root object" not in str(e):
            logger.warning(f"PDF Error at {pdf_url}: {e}")
        return None