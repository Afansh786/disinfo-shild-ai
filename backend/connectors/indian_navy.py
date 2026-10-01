"""
Disinfo Shield AI 2026 — Indian Navy Media Intelligence Connector
-------------------------------------------------------------------
Aggregates Indian Navy news & updates from 8 official and social media sources.
Returns realistic sample data for demo; each function has upgrade notes for
production API/scraping integration.

Sources:
    1. PIB (Press Information Bureau) — Defence Ministry releases
    2. Ministry of Defence — Official announcements
    3. Indian Navy Official — indiannavy.nic.in
    4. Eastern Naval Command — ENC updates
    5. Western Naval Command — WNC updates
    6. X (Twitter) — @indiannavy, @DefenceMinIndia
    7. YouTube — Indian Navy Official channel
    8. Instagram — @indiannavy

Focus area: Naval Operations (exercises, deployments, humanitarian ops, etc.)
"""

import uuid
import random
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional


# ── Source Metadata ────────────────────────────────────────────

NAVY_SOURCES = {
    "pib": {
        "name": "PIB (Press Information Bureau)",
        "icon": "fa-solid fa-landmark",
        "color": "#FF9933",
        "type": "official",
        "url": "https://pib.gov.in/allRel.aspx",
    },
    "mod": {
        "name": "Ministry of Defence",
        "icon": "fa-solid fa-shield-halved",
        "color": "#138808",
        "type": "official",
        "url": "https://mod.gov.in",
    },
    "navy_official": {
        "name": "Indian Navy Official",
        "icon": "fa-solid fa-anchor",
        "color": "#003366",
        "type": "official",
        "url": "https://indiannavy.nic.in",
    },
    "enc": {
        "name": "Eastern Naval Command",
        "icon": "fa-solid fa-compass",
        "color": "#1a5276",
        "type": "official",
        "url": "https://indiannavy.nic.in/enc",
    },
    "wnc": {
        "name": "Western Naval Command",
        "icon": "fa-solid fa-wind",
        "color": "#1b4f72",
        "type": "official",
        "url": "https://indiannavy.nic.in/wnc",
    },
    "twitter": {
        "name": "X (Twitter)",
        "icon": "fa-brands fa-x-twitter",
        "color": "#1d9bf0",
        "type": "social",
        "url": "https://x.com/indiannavy",
    },
    "youtube": {
        "name": "YouTube",
        "icon": "fa-brands fa-youtube",
        "color": "#ff0033",
        "type": "social",
        "url": "https://youtube.com/@indiannavy",
    },
    "instagram": {
        "name": "Instagram",
        "icon": "fa-brands fa-instagram",
        "color": "#e1306c",
        "type": "social",
        "url": "https://instagram.com/indiannavy",
    },
}


# ── Realistic Sample Data — Operations Focused ────────────────

_PIB_SAMPLES = [
    {
        "title": "Indian Navy Conducts Major Bilateral Exercise TARANG SHAKTI-26 with French Navy",
        "content": "The Indian Navy and French Navy commenced the bilateral exercise TARANG SHAKTI-26 in the Bay of Bengal today. The exercise involves guided missile destroyer INS Mormugao, frigate INS Tarkash, maritime patrol aircraft P-8I, and MiG-29K fighter aircraft from INS Vikrant. The French Navy is represented by carrier group led by FS Charles de Gaulle. The exercise aims to enhance interoperability in anti-submarine warfare, air defence, and maritime domain awareness operations.",
        "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=2065431",
        "category": "operations",
    },
    {
        "title": "Cabinet Committee on Security Approves Procurement of Next-Gen Stealth Frigates Under Project-17B",
        "content": "The Cabinet Committee on Security (CCS) has approved the construction of four additional stealth frigates under the enhanced Project-17B programme. The frigates, to be built at Mazagon Dock Shipbuilders Limited (MDL), Mumbai, will feature indigenous BrahMos-NG missile systems, advanced AESA radar, and integrated combat management system developed by DRDO. Total project cost is estimated at ₹35,000 crore under the 'Buy Indian (IDDM)' category.",
        "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=2065520",
        "category": "acquisition",
    },
    {
        "title": "Indian Navy's HADR Operations: INS Jalashwa Delivers 500 Tonnes of Relief to Cyclone-Affected Myanmar Coast",
        "content": "Indian Navy amphibious vessel INS Jalashwa, along with INS Airavat, completed a Humanitarian Assistance and Disaster Relief (HADR) mission delivering 500 tonnes of relief material including medicines, food packets, portable water purifiers, and tents to cyclone-affected regions along the Myanmar coast. The mission was part of India's 'First Responder' initiative under SAGAR (Security and Growth for All in the Region) doctrine.",
        "url": "https://pib.gov.in/PressReleasePage.aspx?PRID=2065612",
        "category": "operations",
    },
]

_MOD_SAMPLES = [
    {
        "title": "Raksha Mantri Reviews Operational Preparedness of Indian Navy at Naval Headquarters",
        "content": "Raksha Mantri Shri Rajnath Singh reviewed the operational preparedness of the Indian Navy during a high-level meeting at Naval Headquarters, New Delhi. Chief of Naval Staff Admiral R. Hari Kumar briefed the Minister on ongoing deployment patterns, surveillance operations in the Indian Ocean Region (IOR), and the Navy's anti-piracy patrols off the coast of Somalia. The Minister expressed satisfaction with the Navy's enhanced Maritime Domain Awareness capabilities through the Information Fusion Centre – Indian Ocean Region (IFC-IOR).",
        "url": "https://mod.gov.in/press-release/2026-09-22",
        "category": "operations",
    },
    {
        "title": "MoD Signs Contract Worth ₹19,600 Crore for 6 Advanced Submarines Under Project-75(I)",
        "content": "The Ministry of Defence signed a landmark contract with Mazagon Dock Shipbuilders Limited for the construction of six advanced conventional submarines under Project-75(I). The submarines will feature Air Independent Propulsion (AIP) systems, land-attack cruise missiles, and advanced stealth capabilities. This is the largest 'Make in India' defence contract for the Navy, with over 60% indigenous content.",
        "url": "https://mod.gov.in/press-release/2026-09-20",
        "category": "acquisition",
    },
]

_NAVY_OFFICIAL_SAMPLES = [
    {
        "title": "INS Vikrant Carrier Battle Group Deploys for Operational Readiness Exercise in Arabian Sea",
        "content": "Aircraft carrier INS Vikrant, accompanied by guided missile destroyers INS Kochi and INS Chennai, stealth frigate INS Shivalik, fleet tanker INS Deepak, and submarine INS Kalvari, has deployed for a month-long Operational Readiness Exercise (ORE) in the Arabian Sea. The exercise includes live weapon firings, integrated anti-submarine warfare drills, carrier-based air operations with MiG-29K and KA-31 helicopters, and Electronic Warfare scenarios. Over 8,000 personnel are participating in the exercise.",
        "url": "https://indiannavy.nic.in/content/ins-vikrant-cbg-ore-2026",
        "category": "operations",
    },
    {
        "title": "Indian Navy Commissions INS Arnala — First Anti-Submarine Warfare Shallow Water Craft",
        "content": "Indian Navy commissioned INS Arnala, the first of eight indigenously built Anti-Submarine Warfare Shallow Water Craft (ASW-SWC), at Naval Dockyard Mumbai. Built by Garden Reach Shipbuilders & Engineers (GRSE), Kolkata, the 900-tonne vessel is equipped with hull-mounted sonar, torpedo launchers, and 30mm close-in weapon system. INS Arnala will strengthen the Navy's coastal defence and ASW capabilities in littoral waters.",
        "url": "https://indiannavy.nic.in/content/commissioning-ins-arnala",
        "category": "commissioning",
    },
    {
        "title": "Navy Day 2026: Indian Navy Demonstrates Operational Capability at Visakhapatnam",
        "content": "The Indian Navy showcased its operational prowess during the Navy Day celebrations at Visakhapatnam. The demonstration included BrahMos supersonic cruise missile firing, torpedo launches from Scorpene-class submarine, MiG-29K aerial display from INS Vikrant, Marine Commando (MARCOS) combat free-fall and ship assault exercises, and Search & Rescue operations by Chetak and ALH Dhruv helicopters. President of India graced the occasion as Chief Guest.",
        "url": "https://indiannavy.nic.in/content/navy-day-2026",
        "category": "operations",
    },
]

_ENC_SAMPLES = [
    {
        "title": "Eastern Naval Command Conducts Exercise Sea Vigil-26 Along East Coast",
        "content": "Eastern Naval Command (ENC) conducted the coastal defence exercise 'Sea Vigil-26' spanning the entire east coast from West Bengal to Tamil Nadu. The exercise tested the coastal security apparatus including Indian Navy, Coast Guard, Marine Police, Customs, and port authorities. Multiple scenarios including infiltration attempts, rogue vessel interception, and oil spill response were simulated. Vice Admiral Atul Anand, Flag Officer Commanding-in-Chief ENC, oversaw the exercise from the Maritime Operations Centre, Visakhapatnam.",
        "url": "https://indiannavy.nic.in/enc/sea-vigil-26",
        "category": "operations",
    },
    {
        "title": "ENC Ships INS Ranvijay and INS Kavaratti Complete Anti-Piracy Patrol in Gulf of Aden",
        "content": "Eastern Naval Command ships INS Ranvijay (guided missile destroyer) and INS Kavaratti (ASW corvette) returned to Visakhapatnam after completing a three-month anti-piracy deployment in the Gulf of Aden. During the deployment, the ships escorted 147 merchant vessels, investigated 38 suspicious dhows, and provided medical assistance to 12 fishing boats. The deployment reinforced India's commitment to ensuring freedom of navigation in international sea lanes.",
        "url": "https://indiannavy.nic.in/enc/anti-piracy-patrol-2026",
        "category": "operations",
    },
]

_WNC_SAMPLES = [
    {
        "title": "Western Naval Command Hosts Multinational Exercise MILAN 2026 at Mumbai",
        "content": "Western Naval Command hosted the multilateral naval exercise MILAN 2026 at Mumbai, with participation from 25 navies including the US, Japan, Australia, France, and South Korea. The harbour phase included International Maritime Seminar on 'Indo-Pacific Maritime Security Architecture' and Damage Control exercises. The sea phase featured complex tactical manoeuvres, replenishment-at-sea, cross-deck helicopter operations, and anti-submarine warfare exercises. Vice Admiral Dinesh Tripathi, FOC-in-C West, inaugurated the event.",
        "url": "https://indiannavy.nic.in/wnc/milan-2026",
        "category": "operations",
    },
    {
        "title": "INS Vikramaditya Undergoes Major Refit at Naval Dockyard Mumbai",
        "content": "Aircraft carrier INS Vikramaditya entered Naval Dockyard Mumbai for a scheduled Medium Refit and Life Certification (MRLC). The refit will upgrade the ship's combat management system, install new long-range surveillance radar, overhaul the boiler and propulsion systems, and integrate new electronic warfare suite. The refit, expected to take 18 months, will extend the carrier's operational life by 15 years. Western Naval Command's dockyard team of 2,500 personnel will execute the refit.",
        "url": "https://indiannavy.nic.in/wnc/vikramaditya-refit-2026",
        "category": "maintenance",
    },
]

_TWITTER_SAMPLES = [
    {
        "title": "🇮🇳 INS Vikrant CBG at Sea — Operational Readiness",
        "content": "#IndianNavy Aircraft Carrier INS Vikrant along with escort ships & submarine operating in Arabian Sea as part of Operational Readiness Exercise. MiG-29K sorties, ASW drills & live weapon firings conducted. 🌊⚓ #CombatReady #IndianNavyOperations",
        "url": "https://x.com/indiannavy/status/1834567890123456789",
        "author": "@indiannavy",
        "category": "operations",
    },
    {
        "title": "Exercise TARANG SHAKTI with French Navy 🇫🇷🇮🇳",
        "content": "Day 3 of #TarangShakti26 — INS Mormugao & FS Charles de Gaulle conducted coordinated Anti-Submarine Warfare exercise in Bay of Bengal. P-8I Neptune & Rafale-M interoperability demonstrated. 🤝 #IndoFrenchNavalCooperation @MarineNationale",
        "url": "https://x.com/indiannavy/status/1834567890123456790",
        "author": "@indiannavy",
        "category": "operations",
    },
    {
        "title": "MARCOS Training — Amphibious Operations",
        "content": "Marine Commandos (MARCOS) conducting advanced amphibious assault training along western coastline. Night operations, VBSS drills & underwater demolition exercises executed with precision. 💪🇮🇳 #MARCOS #SpecialForces #IndianNavy",
        "url": "https://x.com/indiannavy/status/1834567890123456791",
        "author": "@indiannavy",
        "category": "operations",
    },
    {
        "title": "Raksha Mantri Reviews Navy Ops Readiness",
        "content": "RM Shri @rajaboraofficial reviewed #IndianNavy's operational preparedness at Naval HQ. CNS Admiral R. Hari Kumar briefed on IOR deployments, anti-piracy ops & #IFCIOR updates. India's maritime security architecture continues to strengthen. @DefenceMinIndia",
        "url": "https://x.com/DefenceMinIndia/status/1834567890123456792",
        "author": "@DefenceMinIndia",
        "category": "operations",
    },
]

_YOUTUBE_SAMPLES = [
    {
        "title": "INS Vikrant — India's First Indigenous Aircraft Carrier in Combat Operations",
        "content": "Witness the might of INS Vikrant as the carrier battle group conducts Operational Readiness Exercise in the Arabian Sea. Watch MiG-29K launches, helicopter operations, and coordinated fleet manoeuvres in this exclusive footage from the Indian Navy.",
        "url": "https://youtube.com/watch?v=IN_Navy_Vikrant_OPS",
        "thumbnail": "https://img.youtube.com/vi/IN_Navy_Vikrant_OPS/maxresdefault.jpg",
        "views": "2.4M views",
        "duration": "18:42",
        "category": "operations",
    },
    {
        "title": "Exercise MILAN 2026 — 25 Navies Unite at Mumbai | Indian Navy",
        "content": "The Indian Navy hosted MILAN 2026, one of the largest multilateral naval exercises in the Indo-Pacific, with 25 participating navies. This video covers the International Maritime Seminar, harbour phase activities, and spectacular sea phase operations including anti-submarine warfare and cross-deck flying.",
        "url": "https://youtube.com/watch?v=IN_Navy_MILAN_2026",
        "thumbnail": "https://img.youtube.com/vi/IN_Navy_MILAN_2026/maxresdefault.jpg",
        "views": "1.8M views",
        "duration": "24:15",
        "category": "operations",
    },
    {
        "title": "MARCOS — India's Elite Naval Special Forces in Action",
        "content": "An inside look at the Marine Commandos (MARCOS) — India's naval special forces. Watch combat diving, counter-terrorism operations, VBSS (Visit, Board, Search & Seizure) drills, and parachute insertions. The MARCOS are among the few special forces in the world qualified in all three dimensions of warfare.",
        "url": "https://youtube.com/watch?v=IN_Navy_MARCOS_2026",
        "thumbnail": "https://img.youtube.com/vi/IN_Navy_MARCOS_2026/maxresdefault.jpg",
        "views": "5.1M views",
        "duration": "12:30",
        "category": "operations",
    },
]

_INSTAGRAM_SAMPLES = [
    {
        "title": "🇮🇳 BrahMos Supersonic Cruise Missile Fired from INS Chennai",
        "content": "Indian Navy successfully test-fires BrahMos supersonic cruise missile from stealth destroyer INS Chennai during operational exercise. The missile hit the target with pinpoint accuracy at a range of 290 km. #IndianNavy #BrahMos #CombatReady #IndianNavyOperations",
        "url": "https://instagram.com/p/indiannavy_brahmos_fire",
        "author": "@indiannavy",
        "likes": "245K likes",
        "category": "operations",
    },
    {
        "title": "INS Arnala Commissioning Ceremony at Naval Dockyard Mumbai",
        "content": "The Indian Navy commissioned INS Arnala — the first Anti-Submarine Warfare Shallow Water Craft built by @gaborseshipbuilders. A proud moment for Indian shipbuilding! Swipe for more photos from the ceremony 👉 #MakeInIndia #IndianNavy #AatmanirbharBharat",
        "url": "https://instagram.com/p/indiannavy_arnala_commissioning",
        "author": "@indiannavy",
        "likes": "189K likes",
        "category": "commissioning",
    },
    {
        "title": "Sunset Operations — INS Vikrant Carrier Group at Sea 🌅",
        "content": "Breathtaking sunset view as INS Vikrant carrier battle group operates in formation during the Operational Readiness Exercise. The group includes destroyers, frigates, submarine, and fleet tanker — demonstrating India's blue-water naval capability. 📸 by IN Photographer #IndianNavy #INSVikrant",
        "url": "https://instagram.com/p/indiannavy_vikrant_sunset",
        "author": "@indiannavy",
        "likes": "312K likes",
        "category": "operations",
    },
]


# ── Helper: Generate a random recent datetime ─────────────────

def _random_recent_date(max_days_ago: int = 14) -> str:
    """Generate a random ISO datetime within the last N days."""
    delta = timedelta(
        days=random.randint(0, max_days_ago),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
    )
    dt = datetime.utcnow() - delta
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


# ── Individual Source Fetchers ─────────────────────────────────

def fetch_pib_defence_news(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch defence news from PIB (Press Information Bureau).

    Production upgrade:
        import requests
        from bs4 import BeautifulSoup
        resp = requests.get("https://pib.gov.in/allRel.aspx?Ministry=Defence")
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Parse press release links and content
    """
    items = []
    for sample in _PIB_SAMPLES[:limit]:
        items.append({
            "id": f"pib_{uuid.uuid4().hex[:10]}",
            "source": "pib",
            "source_name": NAVY_SOURCES["pib"]["name"],
            "title": sample["title"],
            "content": sample["content"],
            "url": sample["url"],
            "category": sample["category"],
            "media_type": "article",
            "date": _random_recent_date(7),
        })
    return items


def fetch_mod_updates(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch updates from Ministry of Defence website.

    Production upgrade:
        import requests
        from bs4 import BeautifulSoup
        resp = requests.get("https://mod.gov.in/press-releases")
        soup = BeautifulSoup(resp.text, 'html.parser')
    """
    items = []
    for sample in _MOD_SAMPLES[:limit]:
        items.append({
            "id": f"mod_{uuid.uuid4().hex[:10]}",
            "source": "mod",
            "source_name": NAVY_SOURCES["mod"]["name"],
            "title": sample["title"],
            "content": sample["content"],
            "url": sample["url"],
            "category": sample["category"],
            "media_type": "article",
            "date": _random_recent_date(10),
        })
    return items


def fetch_navy_official(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch news from Indian Navy official website.

    Production upgrade:
        import requests
        from bs4 import BeautifulSoup
        resp = requests.get("https://indiannavy.nic.in/whats-new")
        soup = BeautifulSoup(resp.text, 'html.parser')
    """
    items = []
    for sample in _NAVY_OFFICIAL_SAMPLES[:limit]:
        items.append({
            "id": f"navy_{uuid.uuid4().hex[:10]}",
            "source": "navy_official",
            "source_name": NAVY_SOURCES["navy_official"]["name"],
            "title": sample["title"],
            "content": sample["content"],
            "url": sample["url"],
            "category": sample["category"],
            "media_type": "article",
            "date": _random_recent_date(5),
        })
    return items


def fetch_naval_command_updates(command: str = "enc", limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch updates from Eastern or Western Naval Command.

    Args:
        command: 'enc' for Eastern Naval Command, 'wnc' for Western Naval Command.

    Production upgrade:
        import requests
        from bs4 import BeautifulSoup
        resp = requests.get(f"https://indiannavy.nic.in/{command}/news")
        soup = BeautifulSoup(resp.text, 'html.parser')
    """
    samples = _ENC_SAMPLES if command == "enc" else _WNC_SAMPLES
    source_key = command

    items = []
    for sample in samples[:limit]:
        items.append({
            "id": f"{command}_{uuid.uuid4().hex[:10]}",
            "source": source_key,
            "source_name": NAVY_SOURCES[source_key]["name"],
            "title": sample["title"],
            "content": sample["content"],
            "url": sample["url"],
            "category": sample["category"],
            "media_type": "article",
            "date": _random_recent_date(8),
        })
    return items


def fetch_navy_twitter(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch Indian Navy tweets from X (Twitter).

    Production upgrade:
        import tweepy
        client = tweepy.Client(bearer_token=TWITTER_BEARER_TOKEN)
        tweets = client.get_users_tweets(
            id=INDIAN_NAVY_USER_ID,
            max_results=limit,
            tweet_fields=['created_at', 'public_metrics']
        )
    """
    items = []
    for sample in _TWITTER_SAMPLES[:limit]:
        items.append({
            "id": f"tw_{uuid.uuid4().hex[:10]}",
            "source": "twitter",
            "source_name": NAVY_SOURCES["twitter"]["name"],
            "title": sample["title"],
            "content": sample["content"],
            "url": sample["url"],
            "author": sample.get("author", "@indiannavy"),
            "category": sample["category"],
            "media_type": "tweet",
            "date": _random_recent_date(3),
        })
    return items


def fetch_navy_youtube(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch Indian Navy YouTube videos.

    Production upgrade:
        from googleapiclient.discovery import build
        youtube = build('youtube', 'v3', developerKey=API_KEY)
        request = youtube.search().list(
            part='snippet',
            channelId='UC_INDIAN_NAVY_CHANNEL_ID',
            maxResults=limit,
            order='date'
        )
        response = request.execute()
    """
    items = []
    for sample in _YOUTUBE_SAMPLES[:limit]:
        items.append({
            "id": f"yt_{uuid.uuid4().hex[:10]}",
            "source": "youtube",
            "source_name": NAVY_SOURCES["youtube"]["name"],
            "title": sample["title"],
            "content": sample["content"],
            "url": sample["url"],
            "thumbnail": sample.get("thumbnail"),
            "views": sample.get("views"),
            "duration": sample.get("duration"),
            "category": sample["category"],
            "media_type": "video",
            "date": _random_recent_date(5),
        })
    return items


def fetch_navy_instagram(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Fetch Indian Navy Instagram posts.

    Production upgrade:
        # Instagram scraping via instaloader or official Graph API
        import instaloader
        L = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(L.context, 'indiannavy')
        for post in profile.get_posts():
            ...
    """
    items = []
    for sample in _INSTAGRAM_SAMPLES[:limit]:
        items.append({
            "id": f"ig_{uuid.uuid4().hex[:10]}",
            "source": "instagram",
            "source_name": NAVY_SOURCES["instagram"]["name"],
            "title": sample["title"],
            "content": sample["content"],
            "url": sample["url"],
            "author": sample.get("author", "@indiannavy"),
            "likes": sample.get("likes"),
            "category": sample["category"],
            "media_type": "post",
            "date": _random_recent_date(4),
        })
    return items


# ── Master Aggregator ─────────────────────────────────────────

def fetch_all_navy_intel(
    source: Optional[str] = None,
    limit: int = 50,
) -> Dict[str, Any]:
    """
    Aggregate Indian Navy intelligence from all configured sources.

    Args:
        source: Optional source filter ('pib', 'mod', 'navy_official', 'enc', 'wnc',
                'twitter', 'youtube', 'instagram'). If None, fetches from all sources.
        limit: Maximum total items to return.

    Returns:
        Dict with keys: items (list), total_count (int), sources (dict of counts),
        last_updated (str).
    """
    all_items: List[Dict[str, Any]] = []

    fetchers = {
        "pib": lambda: fetch_pib_defence_news(limit=5),
        "mod": lambda: fetch_mod_updates(limit=5),
        "navy_official": lambda: fetch_navy_official(limit=5),
        "enc": lambda: fetch_naval_command_updates(command="enc", limit=5),
        "wnc": lambda: fetch_naval_command_updates(command="wnc", limit=5),
        "twitter": lambda: fetch_navy_twitter(limit=5),
        "youtube": lambda: fetch_navy_youtube(limit=5),
        "instagram": lambda: fetch_navy_instagram(limit=5),
    }

    if source and source in fetchers:
        all_items = fetchers[source]()
    else:
        for fetcher_fn in fetchers.values():
            all_items.extend(fetcher_fn())

    # Sort by date (most recent first)
    all_items.sort(key=lambda x: x.get("date", ""), reverse=True)

    # Apply limit
    all_items = all_items[:limit]

    # Source breakdown
    source_counts: Dict[str, int] = {}
    for item in all_items:
        src = item["source"]
        source_counts[src] = source_counts.get(src, 0) + 1

    return {
        "items": all_items,
        "total_count": len(all_items),
        "sources": source_counts,
        "source_metadata": NAVY_SOURCES,
        "last_updated": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
