"""Provider Vavoo - salva URL del resolver Cloudflare (non risolve direttamente)."""
import logging
from urllib.parse import quote

logger = logging.getLogger(__name__)

RESOLVER_BASE = "https://resolvers.simone-scorrano-2011.workers.dev/vavoo"

def resolve(channel, stream):
    query = stream.get("query") or channel.get("name", "")
    if not query:
        raise ValueError("Vavoo: query mancante")

    stable_url = f"{RESOLVER_BASE}?ch={quote(query)}"
    logger.info("Vavoo: %s -> %s", query, stable_url)

    return {
        "url": stable_url,
        "provider": "Vavoo",
        "quality": "HD",
        "headers": {},
        "extra_vlcopts": ["network-caching=10000"],
    }
