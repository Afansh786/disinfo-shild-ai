"""
Disinfo Shield AI 2026 — Twitter / X Data Connector
-----------------------------------------------------
Provides synthetic realistic tweet data for demo/development.
Replace with Tweepy or Twitter API v2 calls for production use.
"""

import uuid
import random
from typing import Any, Dict, List


# Realistic synthetic tweet templates for demonstration
_DISINFO_TEMPLATES = [
    {
        "author": "@EchoMatrix_99",
        "content": "BREAKING: Leaked classified Pentagon report confirms secret biological laboratories operating under civilian hospitals! Government is actively hiding this! Share before taken down!! #BioLabCoverup",
        "campaign": "biolab_panic",
    },
    {
        "author": "@ViralVector_44",
        "content": "Military insider just confirmed bio-weapon research ongoing in Eastern Europe. MSM won't report this. RT to expose the truth!! #BioWeapon #Whistleblower",
        "campaign": "biolab_panic",
    },
    {
        "author": "@MarketPanic_Now",
        "content": "EMERGENCY: Massive liquidity failure at Regional Capital Bank! ATM withdrawals capped at $100, online transfers frozen. Get your savings out NOW!! #BankCollapse26",
        "campaign": "bank_run",
    },
    {
        "author": "@CityRumor_Pulse",
        "content": "*BREAKING: City Hall announces mandatory city-wide ban on all personal vehicles starting next Monday! Fines of $500 for non-compliance!",
        "campaign": "civic_fud",
    },
    {
        "author": "@FactCheck_Daily",
        "content": "The Federal Reserve concluded its scheduled two-day policy meeting today, holding interest rates steady as economic growth metrics aligned with quarterly forecasts.",
        "campaign": None,
    },
    {
        "author": "@VoteWatch_Alert",
        "content": "VOTING NOTICE: Due to emergency software glitch, all ballots in precinct 12 must be submitted before 12PM today instead of 8PM. Pass this to your neighbors! #VoteNotice",
        "campaign": "election_fud",
    },
    {
        "author": "@TruthSeeker_X",
        "content": "Just in: CDC admits vaccine side effects data was suppressed for 2 years. The documents are right here. Share before Big Tech censors this! #CDCLeaks",
        "campaign": "health_disinfo",
    },
    {
        "author": "@FinAlerts_Direct",
        "content": "Attention! Cash transfer frozen in SBI bank! All online transactions halted immediately. Withdraw your savings now before branches close!! #SBIBankFreeze #CashFrozen",
        "campaign": "bank_run",
    },
    {
        "author": "@BankingScamAlert",
        "content": "Claims your SBI YONO app, PAN, or Aadhaar is expired and the account will be blocked today! Update immediately to avoid deactivation. #SBIBankAlert #YONOExpired #PANCardBlocked #AadhaarUpdate #BankFraudAlert",
        "campaign": "bank_run",
    },
    {
        "author": "@DGISPR_Monitor_Alert",
        "content": "URGENT LEAK: Pakistan DGISPR circulating AI-generated deepfake video of Army Air Defence JCO alleging air defence system failures in Punjab. Old 2021 MiG-21 crash clips recycled claiming downed Rafale jet! #OpSindoor #DGISPR #FactCheck",
        "campaign": "dgispr_ops",
    },
    {
        "author": "@AeroGlobal_Intel",
        "content": "EXCLUSIVE OSINT: Chinese state media bot swarms pushing fabricated reports of Indian Rafale combat losses across international aviation forums to market Chinese J-35 stealth fighters to foreign defense buyers! #AviationOSINT #ChinaDisinfo",
        "campaign": "chinese_rafale_fud",
    },
    {
        "author": "@PrimeTime_WarAlert",
        "content": "PRIME TIME TV ALERT: Breaking news broadcast aired video game simulation gameplay (Arma 3) as exclusive real-time nighttime air strike footage! Military forced to dedicate 15% operational time debunking TV studio claims. #MediaEthics #FakeNewsAlert",
        "campaign": "tv_rating_rush",
    },
    {
        "author": "@PatriotSwarm_Echo",
        "content": "FOG OF WAR NOTICE: Swarm accounts defending the spread of false casualty numbers arguing it is acceptable for psychological warfare, while mass-reporting and harassing verified PIB fact-checking handles. #FogOfWar #CyberAstroturf",
        "campaign": "fog_of_war",
    },
    {
        "author": "@LocalNewsWire",
        "content": "Department of Labor released employment numbers showing a modest gain of 150,000 nonfarm jobs, in line with analyst expectations for Q3.",
        "campaign": None,
    },
]


def fetch_recent_tweets(query: str = "", max_results: int = 10) -> List[Dict[str, Any]]:
    """
    Fetch recent tweets matching a query.

    In production, this would call the Twitter API v2 with a Bearer token.
    For demo purposes, returns a selection of synthetic realistic tweets.

    Args:
        query: Search keyword (used to filter templates in demo mode).
        max_results: Maximum number of results to return.

    Returns:
        List of tweet dicts with keys: platform, post_id, author, content, url.
    """
    templates = _DISINFO_TEMPLATES.copy()
    random.shuffle(templates)
    selected = templates[:min(max_results, len(templates))]

    tweets = []
    for t in selected:
        tweet = {
            "platform": "twitter",
            "post_id": f"tw_{uuid.uuid4().hex[:12]}",
            "author": t["author"],
            "content": t["content"],
            "url": f"https://x.com/{t['author'].lstrip('@')}/status/{random.randint(10**17, 10**18)}",
        }
        tweets.append(tweet)

    return tweets
