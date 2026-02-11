from datetime import datetime

def _format_date(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value.strftime("%d %b %Y")
    try:
        parsed = datetime.fromisoformat(str(value))
        return parsed.strftime("%d %b %Y")
    except:
        return None

def get_category_icon(title):
    t = title.lower()
    if "result" in t or "mark" in t:
        return "🏆" 
    if "exam" in t or "schedule" in t or "routine" in t:
        return "📝"
    if "tender" in t or "quotation" in t:
        return "💰"
    if "vacanc" in t or "recruit" in t or "job" in t:
        return "💼" 
    if "admission" in t:
        return "🎓"
    return "📌"

def format_message(n):
    
    title = n.get("title", "No Title")
    url = n.get("source_url", "")
    source = n.get("source", "MAKAUT")
    
    # Escape special HTML characters in title to prevent errors
    title = title.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    
    is_pdf = n.get("pdf_url") is not None
    type_label = "PDF Document" if is_pdf else "Web Link"
    
    icon = get_category_icon(title)
    action_text = "📄 Download PDF" if is_pdf else "🔗 Open Link"
    
    date_str = _format_date(n.get("published_date"))
    date_line = f"🗓 <b>Date:</b> {date_str}\n" if date_str else ""
    
    # HTML FORMATTING
    return (
        f"{icon} <b>{source}</b> | {type_label}\n\n"
        f"<b>{title}</b>\n\n"
        f"{date_line}"
        f"<a href='{url}'>{action_text}</a>"
    )