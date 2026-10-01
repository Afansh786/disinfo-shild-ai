"""
Disinfo Shield AI 2026 — SQLite Persistence Layer
---------------------------------------------------
Lightweight local storage using SQLite. All data stays on the user's machine.
"""

import sqlite3
import json
from pathlib import Path
from typing import Any, Dict, List, Optional

DB_PATH = Path(__file__).resolve().parent.parent / "data" / "disinfo.db"


_initialized = False

def _connect() -> sqlite3.Connection:
    """Return a connection with row_factory set for dict-like access."""
    global _initialized
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def init_db() -> None:
    """Create tables if they don't already exist."""
    global _initialized
    conn = _connect()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            platform    TEXT    NOT NULL,
            post_id     TEXT    UNIQUE,
            author      TEXT,
            content     TEXT    NOT NULL,
            url         TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id     TEXT    NOT NULL,
            label       TEXT    NOT NULL,
            confidence  REAL    NOT NULL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (post_id) REFERENCES posts(post_id)
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    UNIQUE NOT NULL,
            description TEXT,
            severity    TEXT    DEFAULT 'medium',
            post_ids    TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seed initial defense and strategic campaigns if table is fresh
    initial_seeds = [
        ("Pakistan State-Backed Apparatus (DGISPR) Cyber-Ops", "Flagged by Indian Army: Pakistan DGISPR central cyber warfare & psychological operations distributing AI deepfakes of JCO, fabricated Punjab satellite imagery, and recycled 2021 MiG-21 crash clips claiming downed Rafale jet.", "critical", "tw_dgispr_01,tw_dgispr_02,wa_dgispr_leak"),
        ("Chinese State-Controlled Media & AI Networks", "Exposed by US Intel & Indian Embassy: Coordinated bot swarms and AI multimedia amplifying false reports of Indian Rafale losses to commercially market competing Chinese J-20 / J-35 stealth fighters.", "critical", "tw_china_01,rd_china_02"),
        ("Domestic Mainstream News Channels (Commercial Amplification)", "Flagged by CJP & Gen Anil Chauhan: Commercial TV news channels airing Arma 3 video game combat simulations as real-time airstrikes, generating 15% military operational debunking load during Op Sindoor.", "high", "yt_tv_01,yt_tv_02"),
        ("Hyper-Nationalistic Social Media Networks (Fog of War)", "Echo chambers on X and YouTube weaponizing the fog of war, defending fake news diffusion for morale, and attacking independent fact-checkers.", "high", "tw_fog_01,yt_fog_02"),
        ("PanicRun: Coordinated Bank Run", "Targeted financial panic campaign deploying fabricated screenshots, fake SBI/bank cash freeze alerts, and insider claims to induce ATM runs.", "critical", "tw_bank_01,wa_bank_02"),
        ("DeepClone: AI Voice & Executive Impersonation", "Coordinated AI audio synthesis and deepfake video campaign deploying cloned leadership voices to broadcast false emergency directives.", "critical", "tw_clone_01,tg_clone_02"),
        ("Operation Aurora: BioLab Conspiracy", "Cross-platform bio-weapon narrative propagating via coordinated bot networks, doctored hospital files, and dark web audio memos.", "critical", "tw_aurora_01,tg_aurora_02"),
        ("GridBlackout: Infrastructure Sabotage Panic", "Panic campaign distributing forged electricity board cutoff notices, smart meter disconnect threats, and grid breakdown rumors.", "high", "wa_blackout_01"),
        ("CivicDistort: Vehicle Ban & Voting FUD", "Astroturf campaign distributing forged City Hall municipal notices, precinct glitches, and artificial mobility bans across WhatsApp & X.", "high", "tw_civic_01,wa_civic_02"),
        ("MaritimeDisrupt: Indian Ocean OSINT FUD", "Coordinated OSINT distortion campaign weaponizing doctored AIS vessel tracking data and fabricated naval incident claims in the Bay of Bengal.", "high", "tw_navy_01"),
        ("HealthDisinfo: Suppressed Data Claims", "Health misinformation campaign claiming suppressed medical data, contaminated tap water, and institutional cover-ups.", "elevated", "tw_health_01")
    ]

    for name, desc, sev, pids in initial_seeds:
        cur.execute("""
            INSERT OR IGNORE INTO campaigns (name, description, severity, post_ids)
            VALUES (?, ?, ?, ?)
        """, (name, desc, sev, pids))

    conn.commit()
    conn.close()


# ── Post CRUD ──────────────────────────────────────────────

def insert_post(payload: Dict[str, Any]) -> None:
    """Insert a raw post into the database."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO posts (platform, post_id, author, content, url)
        VALUES (:platform, :post_id, :author, :content, :url)
    """, payload)
    conn.commit()
    conn.close()


def get_all_posts(limit: int = 200) -> List[Dict[str, Any]]:
    """Return all posts, most recent first."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts ORDER BY created_at DESC LIMIT ?", (limit,))
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


def search_posts(query: str, platform: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search posts by content keyword and optional platform filter."""
    conn = _connect()
    cur = conn.cursor()
    if platform:
        cur.execute(
            "SELECT * FROM posts WHERE content LIKE ? AND platform = ? ORDER BY created_at DESC LIMIT 100",
            (f"%{query}%", platform),
        )
    else:
        cur.execute(
            "SELECT * FROM posts WHERE content LIKE ? ORDER BY created_at DESC LIMIT 100",
            (f"%{query}%",),
        )
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


# ── Prediction CRUD ────────────────────────────────────────

def insert_prediction(post_id: str, label: str, confidence: float) -> None:
    """Store a classification result for a post."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO predictions (post_id, label, confidence)
        VALUES (?, ?, ?)
    """, (post_id, label, confidence))
    conn.commit()
    conn.close()


# ── Campaign CRUD ──────────────────────────────────────────

def upsert_campaign(name: str, description: str, severity: str, post_ids: List[str]) -> None:
    """Insert or update a detected campaign by name, merging post IDs and updating timestamp."""
    conn = _connect()
    cur = conn.cursor()
    new_ids = set([pid.strip() for pid in post_ids if pid and pid.strip()])

    cur.execute("SELECT id, post_ids FROM campaigns WHERE name = ?", (name,))
    row = cur.fetchone()

    if row:
        existing_ids = set(row["post_ids"].split(",")) if row["post_ids"] else set()
        merged_ids = ",".join(sorted(existing_ids.union(new_ids)))
        cur.execute("""
            UPDATE campaigns
            SET description = ?, severity = ?, post_ids = ?, created_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (description, severity, merged_ids, row["id"]))
    else:
        ids_str = ",".join(sorted(new_ids))
        cur.execute("""
            INSERT INTO campaigns (name, description, severity, post_ids)
            VALUES (?, ?, ?, ?)
        """, (name, description, severity, ids_str))

    conn.commit()
    conn.close()


def get_all_campaigns() -> List[Dict[str, Any]]:
    """Return all detected campaigns, strictly deduplicated by campaign name."""
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM campaigns ORDER BY created_at DESC, id DESC")
    seen_names = set()
    rows = []
    for r in cur.fetchall():
        row = dict(r)
        c_name = row["name"].strip()
        if c_name in seen_names:
            continue
        seen_names.add(c_name)
        row["post_ids"] = [pid for pid in (row["post_ids"] or "").split(",") if pid]
        rows.append(row)
    conn.close()
    return rows


# Ensure database and tables exist on module import
init_db()

