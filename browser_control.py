from __future__ import annotations

import webbrowser
from urllib.parse import quote_plus


def open_browser(url: str = "https://www.google.com") -> dict:
    """Open a URL in the default browser."""
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    webbrowser.open_new_tab(url)
    return {"success": True, "url": url}


def open_whatsapp() -> dict:
    """Open WhatsApp Web in the browser."""
    return open_browser("https://web.whatsapp.com")


def search_web(query: str) -> dict:
    """Search the web with the default browser."""
    if not query.strip():
        return {"success": False, "error": "Search query is empty"}
    url = "https://www.google.com/search?q=" + quote_plus(query.strip())
    return open_browser(url)
