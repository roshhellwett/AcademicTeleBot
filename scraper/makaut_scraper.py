import requests
from bs4 import BeautifulSoup
from datetime import datetime
import hashlib
import logging
import time
from urllib.parse import urljoin
import urllib3
import re

from core.sources import URLS
from scraper.date_extractor import extract_date

# Suppress SSL warnings for legacy university sites
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

logger = logging.getLogger("SCRAPER")

SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
})

# 1. STRICT BLOCKLIST: Always ignore these (Strict Junk)
STRICT_BLOCKLIST = [
    "about us", "contact", "directory", "staff", "genesis", "vision", 
    "mission", "campus", "library", "login", "register", "sitemap", 
    "disclaimer", "university", "chancellor", "vice-chancellor", "registrar",
    "convocation", "antiragging", "rti", "forms", "archive", "tenders",
    "defaulter", "ordinance", "statutes", "officers", "recognition"
]

# 2. AMBIGUOUS TERMS: Block ONLY if they appear as short "Menu Buttons"
MENU_BUTTON_TERMS = [
    "administration", "committees", "affiliated", "academics", 
    "rules", "regulations", "right to information", "governance", "act"
]

def generate_hash(title, url):
    return hashlib.sha256(f"{title}{url}".encode()).hexdigest()

def build_item(title, url, source_name, date_context=None):
    if not title or not url:
        return None
    
    title_lower = title.strip().lower()

    # --- FILTER LEVEL 1: Strict Junk ---
    if any(k in title_lower for k in STRICT_BLOCKLIST):
        return None
        
    # --- FILTER LEVEL 2: Menu Button Detection ---
    # If title has a "Menu Word" AND is very short (< 25 chars), block it.
    if any(k in title_lower for k in MENU_BUTTON_TERMS):
        if len(title) < 25: 
            return None

    # --- FILTER LEVEL 3: General sanity check ---
    if len(title) < 5:
        return None

    if any(x in url.lower() for x in ["javascript", "mailto", "tel:", "#"]):
        return None

    # --- DATE EXTRACTION ---
    real_date = extract_date(title)
    if not real_date and date_context:
        real_date = extract_date(date_context)

    is_pdf = ".pdf" in url.lower()

    return {
        "title": title.strip(),
        "source": source_name,
        "source_url": url,
        "pdf_url": url if is_pdf else None,
        "content_hash": generate_hash(title, url),
        "published_date": real_date,
        "scraped_at": datetime.utcnow()
    }

def parse_generic_links(base_url, source_name):
    data = []
    seen = set()

    # MAKAUT Exam portal often has SSL issues
    verify_ssl = False if "makautexam" in base_url else True
    
    try:
        r = SESSION.get(base_url, timeout=30, verify=verify_ssl)
        r.raise_for_status()

        soup = BeautifulSoup(r.text, "html.parser")
        
        # HTML HELPER: Try to find the 'main' content to avoid header/footer menus
        main_body = soup.find("div", {"id": "content"}) or soup.find("div", class_="content") or soup.find("table") or soup
        
        tags = main_body.find_all("a")
        
        for a in tags:
            title = a.get_text(" ", strip=True)
            href = a.get("href")

            if not title or not href:
                continue

            full_url = urljoin(base_url, href)

            if not full_url.startswith(("http:", "https:")):
                continue
            
            # Context Extraction: Get text from the parent line
            context_text = ""
            if a.parent:
                context_text = a.parent.get_text(" ", strip=True)

            h = generate_hash(title, full_url)
            if h in seen:
                continue
            seen.add(h)

            item = build_item(title, full_url, source_name, context_text)
            if item:
                data.append(item)

    except Exception as e:
        # Re-raise to let scrape_source handle retries
        raise e

    return data

def scrape_source(source_key, source_config):
    url = source_config["url"]
    source_name = source_config["source"]

    for attempt in range(3):
        try:
            return parse_generic_links(url, source_name)
        except Exception as e:
            logger.warning(f"{source_key} attempt {attempt+1}/3 failed: {e}")
            time.sleep(2)

    logger.error(f"{source_key} FAILED AFTER 3 RETRIES")
    return []

def scrape_all_sources():
    all_data = []
    try:
        for key, config in URLS.items():
            logger.info(f"SCRAPING SOURCE {key}")
            source_data = scrape_source(key, config)
            logger.info(f"{key} -> {len(source_data)} items")
            all_data.extend(source_data)
        
        logger.info(f"TOTAL SCRAPED SAFE ITEMS {len(all_data)}")
        
    except Exception as e:
        logger.error(f"SCRAPE ALL ERROR {e}")

    return all_data