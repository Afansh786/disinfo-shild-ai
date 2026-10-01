"""
Disinfo Shield AI 2026 — Reddit Data Connector
------------------------------------------------
Provides synthetic realistic Reddit submission data for demo/development.
Replace with PRAW calls for production use.
"""

import uuid
import random
from typing import Any, Dict, List


_DISINFO_TEMPLATES = [
    {
        "author": "u/Red_Dawn_99",
        "content": "URGENT: Liquidity crisis at Regional Capital Bank. Branch manager confirmed cash transfers frozen today. People are lining up at ATMs. This is not a drill. #BankCollapse26",
        "subreddit": "finance",
        "campaign": "bank_run",
    },
    {
        "author": "u/BankInsider_Leak",
        "content": "I work in risk management at a major bank. We received internal memo today ordering freeze on all international wire transfers. Something big is about to break.",
        "subreddit": "wallstreetbets",
        "campaign": "bank_run",
    },
    {
        "author": "u/DeepState_Hunter",
        "content": "Exposed: Secret government documents reveal bio-weapon program operating in 14 countries. The evidence is overwhelming. MSM blackout is proof of cover-up.",
        "subreddit": "conspiracy",
        "campaign": "biolab_panic",
    },
    {
        "author": "u/CitizenJournalist42",
        "content": "Confirmed with multiple city council sources: emergency vote passed to ban all private vehicles downtown. Implementation starts Monday. This is real.",
        "subreddit": "urbanplanning",
        "campaign": "civic_fud",
    },
    {
        "author": "u/EconAnalyst_PhD",
        "content": "Q3 employment figures came in at 150k nonfarm, slightly above consensus. Fed likely to hold rates. Nothing dramatic, steady as she goes.",
        "subreddit": "economics",
        "campaign": None,
    },
    {
        "author": "u/FinAlert_Mod",
        "content": "Attention! Multiple accounts reporting cash transfer frozen in SBI bank branches today! Net banking and UPI transactions returning timeout errors.",
        "subreddit": "india",
        "campaign": "bank_run",
    },
    {
        "author": "u/OSINT_AeroObserver",
        "content": "Analyst Breakdown: Tracing Pakistan DGISPR coordinated psyops distributing AI-synthesized deepfakes of JCO and recycling 2021 MiG-21 crash footage claiming Rafale kill during Op Sindoor.",
        "subreddit": "geopolitics",
        "campaign": "dgispr_ops",
    },
    {
        "author": "u/DefenceAvGeek",
        "content": "Chinese state media and aligned bot swarms are flooding international forums claiming Indian Rafale air combat deficits to commercially promote Chengdu J-20 / J-35 to Middle Eastern buyers.",
        "subreddit": "aviation",
        "campaign": "chinese_rafale_fud",
    },
    {
        "author": "u/MediaWatch_India",
        "content": "TV news channels literally aired Arma 3 video game combat footage claiming it was live breaking airstrikes on national prime-time TV. CJP has issued a comprehensive critique.",
        "subreddit": "television",
        "campaign": "tv_rating_rush",
    },
    {
        "author": "u/FogOfWar_Tracker",
        "content": "Echo chambers on social media justifying the deliberate propagation of fake military news under fog of war doctrine while actively mass-reporting independent fact checkers.",
        "subreddit": "technology",
        "campaign": "fog_of_war",
    },
    {
        "author": "u/HealthWatchdog",
        "content": "New peer-reviewed study in The Lancet found no significant adverse effects beyond normal parameters. Sample size of 45,000 across 12 countries. Robust methodology.",
        "subreddit": "science",
        "campaign": None,
    },
]


def fetch_recent_submissions(subreddit: str = "all", limit: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch recent Reddit submissions from a subreddit.

    In production, this would use PRAW with OAuth credentials.
    For demo purposes, returns synthetic realistic Reddit posts.

    Args:
        subreddit: Target subreddit name.
        limit: Maximum number of submissions to return.

    Returns:
        List of post dicts with keys: platform, post_id, author, content, url.
    """
    templates = _DISINFO_TEMPLATES.copy()
    random.shuffle(templates)
    selected = templates[:min(limit, len(templates))]

    posts = []
    for t in selected:
        post = {
            "platform": "reddit",
            "post_id": f"rd_{uuid.uuid4().hex[:12]}",
            "author": t["author"],
            "content": t["content"],
            "url": f"https://reddit.com/r/{t['subreddit']}/comments/{uuid.uuid4().hex[:8]}",
        }
        posts.append(post)

    return posts
