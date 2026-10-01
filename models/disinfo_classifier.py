"""
Disinfo Shield AI 2026 — Disinformation Text Classifier
---------------------------------------------------------
Rule-based heuristic classifier that scores text for disinformation signals.
Designed as a drop-in replacement for a HuggingFace transformer model.

To upgrade to ML:
    from transformers import pipeline
    classifier = pipeline("text-classification", model="your-model")
"""

import re
from typing import Tuple


# Pattern categories with associated weights
_URGENCY_PATTERNS = [
    (re.compile(r"(\*?breaking:?|emergency\s+alert|just\s+in:?|urgent:?|attention:?!*|warning:?!*|caution:?!*|alert:?!*|important\s+notice:?!*|notice:?!*)", re.I), 0.18),
    (re.compile(r"(blocked\s+today|frozen\s+today|suspended\s+today|deactivated\s+today|cut\s*off\s+today|closed\s+today|expires?\s+today)", re.I), 0.20),
    (re.compile(r"(share\s+before\s+(it\s+gets\s+)?(taken\s+down|deleted|censored)|forward\s+to\s+all|pass\s+this\s+on|spread\s+this|spread\s+the\s+word)", re.I), 0.14),
    (re.compile(r"(starting\s+(next\s+)?(monday|tomorrow)|effective\s+immediately|tonight\s+at\s+midnight|within\s+\d+\s+hours?|deadline\s+today)", re.I), 0.14),
    (re.compile(r"(immediate\s+action\s+required|act\s+now|time\s+is\s+running\s+out|claims?\s+(your|that)|avoid\s+(blocking|deactivation|penalty))", re.I), 0.14),
]

_AUTHORITY_PATTERNS = [
    (re.compile(r"(pentagon\s+confirms|government\s+secretly|leaked\s+classified|cdc\s+admits|rbi\s+ordered|ministry\s+confirmed)", re.I), 0.15),
    (re.compile(r"(whistleblower|insider\s+source|internal\s+memo|cover.?up|media\s+blackout|msm\s+won.t|hidden\s+agenda)", re.I), 0.13),
    (re.compile(r"(officials\s+are\s+hiding|they\s+don.t\s+want\s+you\s+to\s+know|secret\s+directive)", re.I), 0.12),
]

_MANDATE_PATTERNS = [
    (re.compile(r"(mandatory\s+(city-wide\s+)?ban|ban\s+on\s+all\s+(personal\s+)?vehicles|sweeping\s+ban)", re.I), 0.16),
    (re.compile(r"(martial\s+law|forced\s+lockdown|confiscation|curfew|power\s+cut\s+tonight)", re.I), 0.14),
]

_PANIC_PATTERNS = [
    # PAN / Aadhaar / KYC / YONO App expired or invalid fraud
    (re.compile(r"((sbi\s*yono|yono|pan|aadhaar|kyc|sim\s*card|debit\s*card|credit\s*card|atm\s*card|net\s*banking|bank\s*app|yono\s*sbi)\s+(card\s+|app\s+)?(is\s+|are\s+|will\s+be\s+|has\s+been\s+)?(expired|blocked|suspended|deactivated|invalid|unlinked|pending|not\s+updated|closed))", re.I), 0.24),
    # Accounts & services blocked or frozen
    (re.compile(r"((accounts?|cards?|savings?|access|services?|sim)\s+(is\s+|are\s+|will\s+be\s+|has\s+been\s+)?(blocked|frozen|locked|suspended|capped|deactivated|closed|restricted)(\s+today)?)", re.I), 0.22),
    # Cash transfer & transaction freezes
    (re.compile(r"((cash|money|wire|upi|online|bank|instant|imps|rtgs|neft)\s+transfers?\s+(is\s+|are\s+)?(frozen|blocked|suspended|halted|stopped|failed))", re.I), 0.22),
    # Banking institutions & digital platforms
    (re.compile(r"((sbi(\s+yono)?|yono|hdfc|icici|pnb|rbi|axis\s+bank|bank\s+of\s+baroda|canara\s+bank|union\s+bank|central\s+bank|regional\s+capital\s+bank))", re.I), 0.16),
    # Bank runs & systemic liquidity panic
    (re.compile(r"(bank\s+run|liquidity\s+(crisis|freeze)|bank\s+collapse|mass\s+withdrawals?|insolvency|bank\s+failure)", re.I), 0.18),
    # Coercive withdrawal / Phishing panic calls
    (re.compile(r"(get\s+your\s+(savings|money)\s+out|withdraw\s+(all\s+)?(now|immediately|your\s+savings|your\s+money)|update\s+(your\s+)?(pan|aadhaar|kyc|yono)|click\s+here\s+to\s+unblock)", re.I), 0.18),
    # AI voice clone & executive impersonation scams
    (re.compile(r"((deepfake|ai\s+voice|cloned\s+(audio|voice)|synthetic\s+video|audio\s+leak|audio\s+recording))", re.I), 0.22),
    # Power grid & critical infrastructure disconnection panic
    (re.compile(r"((electricity|power\s+supply|power\s+grid|smart\s+meter|power\s+cut)\s+(.*)?(cut\s*off|disconnected|shutdown|collapsed|blackout|imminent))", re.I), 0.22),
    # Maritime & naval collision / blockade rumors
    (re.compile(r"((warship|submarine|naval\s+carrier|fleet)\s+(collision|torpedo|sunk|blockade|incursion))", re.I), 0.20),
    # Bio-hazard / Chemical contamination panic
    (re.compile(r"(do\s+not\s+drink|water\s+supply\s+chemicals|bio.?weapon|vaccine\s+side\s+effects?\s+suppressed)", re.I), 0.18),
    # Viral threat hashtags (banking panic, KYC phishing, astroturf tags)
    (re.compile(r"#\b(sbibank\w*|yono\w*|pan(card)?\w*|aadhaar\w*|bank(freeze|alert|fraud|collapse)\w*|kyc\w*|liquidityfreeze|blackout\w*|govtaudioleak|navyblockade|biolab\w*)\b", re.I), 0.20),
]

_LEGITIMATE_PATTERNS = [
    (re.compile(r"(according\s+to\s+a\s+spokesperson|reuters|associated\s+press|bloomberg|financial\s+times)", re.I), -0.18),
    (re.compile(r"(peer.?reviewed|the\s+lancet|department\s+of\s+labor|central\s+bureau\s+of\s+statistics)", re.I), -0.18),
    (re.compile(r"(\.gov|\.edu|scheduled\s+.*meeting|quarterly\s+forecast|press\s+release|official\s+statement)", re.I), -0.12),
]

ALL_PATTERNS = _URGENCY_PATTERNS + _AUTHORITY_PATTERNS + _MANDATE_PATTERNS + _PANIC_PATTERNS + _LEGITIMATE_PATTERNS


def classify_text(text: str) -> Tuple[str, float]:
    """
    Classify a text for disinformation probability.

    Args:
        text: The raw text content to analyze.

    Returns:
        Tuple of (label, confidence) where:
            label: "misinformation", "suspicious", or "legitimate"
            confidence: float between 0.0 and 1.0
    """
    score = 0.0
    urgency_hit = False
    panic_hit = False
    authority_hit = False
    mandate_hit = False

    for pattern, weight in _URGENCY_PATTERNS:
        if pattern.search(text):
            score += weight
            urgency_hit = True

    for pattern, weight in _PANIC_PATTERNS:
        if pattern.search(text):
            score += weight
            panic_hit = True

    for pattern, weight in _AUTHORITY_PATTERNS:
        if pattern.search(text):
            score += weight
            authority_hit = True

    for pattern, weight in _MANDATE_PATTERNS:
        if pattern.search(text):
            score += weight
            mandate_hit = True

    for pattern, weight in _LEGITIMATE_PATTERNS:
        if pattern.search(text):
            score += weight

    # Multi-vector amplification boost: Coordinated disinformation hallmark
    if (panic_hit and urgency_hit) or (mandate_hit and urgency_hit) or (authority_hit and panic_hit):
        score += 0.22

    # Uppercase density bonus (shouting / alarmism)
    letters = re.sub(r"[^A-Za-z]", "", text)
    if letters:
        upper_ratio = len(re.sub(r"[^A-Z]", "", text)) / len(letters)
        if upper_ratio > 0.18:
            score += 0.10

    # Exclamation density
    exclamation_count = text.count("!")
    if exclamation_count >= 1 and (urgency_hit or panic_hit):
        score += 0.06
    elif exclamation_count >= 3:
        score += 0.08

    # Base starts at 0.5; calculate confidence clamped to [0, 1]
    confidence = max(0.0, min(1.0, 0.5 + score))

    if confidence >= 0.75:
        return ("misinformation", round(confidence, 3))
    elif confidence >= 0.50:
        return ("suspicious", round(confidence, 3))
    else:
        return ("legitimate", round(1.0 - confidence, 3))
