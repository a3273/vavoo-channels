"""Provider Vavoo via worker Cloudflare (piano B: forza l'ordine provider).

URL stabili con &p=vavoo: il worker prova Vavoo per primo e, se fallisce,
ripiega su NTV e Matchora. Il resolve vavoo reale avviene nel worker
(mirror multipli + API v2 /live/resolve + mediahubmx, failover automatico).
"""

WORKER_BASE = "https://resolvers.simone-scorrano-2011.workers.dev"


def resolve(channel, stream):
    slug = str(stream.get("slug") or "").strip()
    query = str(stream.get("query") or "").strip()
    ch = slug or query.replace(" ", "-")
    if not ch:
        raise ValueError("Vavoo: slug o query mancanti")
    return {
        "url": f"{WORKER_BASE}/live?ch={ch}&p=vavoo",
        "provider": "vavoo",
        "quality": "HD",
        "headers": {},
        "extra_vlcopts": ["network-caching=10000"],
    }
