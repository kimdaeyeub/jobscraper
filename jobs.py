import logging

from get_berlinstartupjobs import get_berlinstartupjobs
from get_rework import get_rework
from get_web3_career import get_web3_career

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


def _safe_fetch(fetcher, source_name, *args, **kwargs):
    try:
        return fetcher(*args, **kwargs) or []
    except Exception as e:
        logger.error("%s fetch failed: %s", source_name, e)
        return []


def fetch_jobs(skill):
    berlin = _safe_fetch(
        get_berlinstartupjobs,
        "Berlin Startup Jobs",
        f"https://berlinstartupjobs.com/skill-areas/{skill}/",
        USER_AGENT,
    )
    rework = _safe_fetch(get_rework, "We Work Remotely", skill)
    web = _safe_fetch(get_web3_career, "Web3 Career", skill)
    return berlin + rework + web
