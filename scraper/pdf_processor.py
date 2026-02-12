import logging
import pdfplumber
import httpx
import io
from scraper.date_extractor import extract_date

logger = logging.getLogger("PDF_PROCESSOR")

async def get_date_from_pdf(pdf_url):
    try:
        async with httpx.AsyncClient(verify=False) as client:
            response = await client.get(pdf_url, timeout=15)
            if response.status_code != 200: return None
            pdf_bytes = io.BytesIO(response.content)

        with pdfplumber.open(pdf_bytes) as pdf:
            if not pdf.pages: return None
            
            # Metadata Check
            meta_date = pdf.metadata.get('CreationDate')
            if meta_date and "2026" in meta_date:
                try:
                    from datetime import datetime
                    return datetime.strptime(meta_date[2:10], "%Y%m%d")
                except: pass

            # Zenith Header Check (Top 25%)
            p = pdf.pages[0]
            header = p.within_bbox((0, 0, p.width, p.height * 0.25)).extract_text()
            return extract_date(header) or extract_date(p.extract_text())

    except Exception as e:
        logger.error(f"❌ PDF Async Error: {e}")
    return None