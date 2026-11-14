"""Provider Vavoo - risoluzione diretta (senza Val.town)."""
import logging
import re
import requests
from urllib.parse import quote

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "it-IT,it;q=0.9,en;q=0.8",
}

def resolve(channel, stream):
    query = stream.get("query") or channel.get("name", "")
    if not query:
        raise ValueError("Vavoo: query mancante")

    search_url = f"https://vavoo.to/search?q={quote(query)}"
    
    res = requests.get(search_url, headers=HEADERS, timeout=15)
    res.raise_for_status()
    html = res.text

    m3u8_match = re.search(r'(https?://[^\s"\']+\.m3u8[^\s"\']*)', html)
    if not m3u8_match:
        raise ValueError(f"Vavoo: m3u8 non trovato per '{query}'")

    url = m3u8_match.group(1)
    logger.info("Vavoo: %s -> %s", query, url)

    return {
        "url": url,
        "provider": "Vavoo",
        "quality": "HD",
        "headers": {"Referer": "https://vavoo.to/"},
        "extra_vlcopts": ["network-caching=10000"],
    }
