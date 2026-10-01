"""
Disinfo Shield AI 2026 — Campaign Clustering Engine
-----------------------------------------------------
Groups classified posts into coordinated campaigns by keyword similarity.
Designed as a drop-in replacement for SBERT + DBSCAN clustering.

To upgrade to ML:
    from sentence_transformers import SentenceTransformer
    from sklearn.cluster import DBSCAN
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode([p["content"] for p in posts])
    clusters = DBSCAN(eps=0.5, min_samples=3).fit_predict(embeddings)
"""

import re
from typing import Any, Dict, List
from collections import defaultdict


# Campaign signatures — keywords that map to known campaign archetypes
_CAMPAIGN_SIGNATURES = {
    "Pakistan State-Backed Apparatus (DGISPR) Cyber-Ops": {
        "keywords": ["dgispr", "deepfake", "jco", "air defence", "rafale", "mig-21", "punjab", "satellite", "operation sindoor", "downed jet", "air strike", "pakistan army", "negligence", "fabrication", "#opsindoor", "#dgispr"],
        "severity": "critical",
        "description": "Central cyber warfare and psychological operations network flagged by Indian Army weaponizing AI deepfakes, recycled MiG-21 crash clips, and forged satellite maps.",
    },
    "Chinese State-Controlled Media & AI Networks": {
        "keywords": ["chinese state media", "china", "rafale loss", "fighter aircraft", "j-20", "j-35", "fc-31", "commercial buyers", "ai video", "embassy expose", "international buyers", "#aviationosint", "#chinadisinfo"],
        "severity": "critical",
        "description": "State-backed network deploying fake account swarms and AI multimedia to amplify false reports of Indian Rafale losses for commercial fighter jet marketing.",
    },
    "Domestic Mainstream News Channels (Commercial Amplification)": {
        "keywords": ["prime time", "breaking news", "exclusive footage", "simulation graphics", "arma 3", "video game footage", "unverified strike", "anil chauhan", "cjp", "rating rush", "operation sindoor", "broadcast"],
        "severity": "high",
        "description": "Commercial TV news channels airing unverified rumors and video game simulations as real-time airstrikes, generating a 15% military operational debunking load.",
    },
    "Hyper-Nationalistic Social Media Networks (Fog of War)": {
        "keywords": ["fog of war", "morale boost", "fact check attack", "mass report", "echo chamber", "fake news justified", "adversary morale", "patriot swarm", "hashtag brigading", "#fogofwar"],
        "severity": "high",
        "description": "Hyper-active echo chambers systematically weaponizing the fog of war, defending fake news diffusion, and attacking independent fact-checking organisations.",
    },
    "PanicRun: Coordinated Bank Run": {
        "keywords": ["bank", "liquidity", "atm", "savings", "withdraw", "frozen", "collapse", "wire", "transfer", "sbi", "rbi", "account", "blocked", "funds", "kyc", "yono", "pan", "aadhaar", "#sbibankalert", "#yonoexpired", "#pancardblocked", "#aadhaarupdate", "#bankfraudalert", "#sbibankfreeze", "#bankcollapse26"],
        "severity": "critical",
        "description": "Targeted financial panic campaign deploying fabricated screenshots, fake freeze alerts, and insider claims.",
    },
    "DeepClone: AI Voice & Executive Impersonation": {
        "keywords": ["deepfake", "cloned", "voice", "audio leak", "ai video", "impersonation", "ceo", "minister", "scheme", "scam", "synthetic"],
        "severity": "critical",
        "description": "Coordinated AI voice cloning and synthetic video campaign distributing fake executive directives and urgent financial schemes.",
    },
    "Operation Aurora: BioLab Conspiracy": {
        "keywords": ["bio", "weapon", "lab", "pentagon", "hospital", "classified", "military", "chemical", "water", "pathogen"],
        "severity": "critical",
        "description": "Cross-platform bio-weapon narrative propagating via coordinated bot networks.",
    },
    "GridBlackout: Infrastructure Sabotage Panic": {
        "keywords": ["power grid", "electricity", "blackout", "substation", "transformer", "power cut", "power supply", "disconnection", "grid collapse"],
        "severity": "high",
        "description": "Panic campaign circulating fabricated electricity board cutoff notices, smart meter disconnect threats, and grid breakdown rumors.",
    },
    "CivicDistort: Vehicle Ban & Voting FUD": {
        "keywords": ["vehicle", "ban", "city hall", "mandatory", "precinct", "ballot", "voting", "curfew", "lockdown"],
        "severity": "high",
        "description": "Astroturf campaign distributing forged municipal notices and voting misinformation.",
    },
    "MaritimeDisrupt: Indian Ocean OSINT FUD": {
        "keywords": ["navy", "warship", "submarine", "blockade", "maritime", "carrier", "bay of bengal", "arabian sea", "ais", "collision", "false flag"],
        "severity": "high",
        "description": "Coordinated OSINT distortion campaign weaponizing doctored AIS tracking telemetry and fabricated naval incident claims.",
    },
    "HealthDisinfo: Suppressed Data Claims": {
        "keywords": ["vaccine", "side effect", "suppressed", "cdc", "admits", "cover", "who", "pharma"],
        "severity": "high",
        "description": "Health misinformation campaign claiming suppressed medical data and institutional cover-ups.",
    },
}


def cluster_posts(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Cluster classified posts into coordinated campaigns.

    Uses keyword-matching against known campaign signatures.
    Posts that don't match any signature are grouped into an 'Unclassified' bucket.

    Args:
        posts: List of post dicts. Each must have 'content' and 'post_id' keys.

    Returns:
        List of campaign dicts with keys: name, description, severity, post_ids, post_count.
    """
    campaign_buckets: Dict[str, List[str]] = defaultdict(list)

    for post in posts:
        content_lower = post.get("content", "").lower()
        matched = False

        for campaign_name, signature in _CAMPAIGN_SIGNATURES.items():
            hit_count = sum(1 for kw in signature["keywords"] if kw in content_lower)
            if hit_count >= 2:
                campaign_buckets[campaign_name].append(post.get("post_id", "unknown"))
                matched = True
                break

        if not matched:
            campaign_buckets["Unclassified"].append(post.get("post_id", "unknown"))

    campaigns = []
    for name, post_ids in campaign_buckets.items():
        if name == "Unclassified" and len(post_ids) == 0:
            continue
        sig = _CAMPAIGN_SIGNATURES.get(name, {})
        campaigns.append({
            "name": name,
            "description": sig.get("description", "Posts that did not match any known campaign signature."),
            "severity": sig.get("severity", "low"),
            "post_ids": post_ids,
            "post_count": len(post_ids),
        })

    # Sort by severity (critical first)
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    campaigns.sort(key=lambda c: severity_order.get(c["severity"], 99))

    return campaigns
