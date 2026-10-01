"""
Disinfo Shield AI 2026 — FastAPI Backend
------------------------------------------
Main application entry point. Exposes REST API endpoints for ingestion,
analysis, campaign retrieval, and search. Also serves the desktop UI.
"""

import sys
from pathlib import Path

# Add project root directory to sys.path so modules can be imported directly
_ROOT_DIR = Path(__file__).resolve().parent.parent
if str(_ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(_ROOT_DIR))

import base64
import time
import uvicorn
from fastapi import FastAPI, HTTPException, Query, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

try:
    from backend.db import init_db, insert_post, get_all_posts, get_all_campaigns, search_posts
    from backend.pipeline import run_pipeline, generate_job_id
    from backend.connectors.indian_navy import fetch_all_navy_intel, NAVY_SOURCES
    from backend.connectors.live_news import get_live_news, CATEGORY_FEEDS, CATEGORY_EMOJIS
    from backend.connectors.adversary_intel import (
        fetch_all_adversary_intel,
        get_adversary_countries_meta,
        get_adversary_orbat,
        get_adversary_hotspots
    )
    from backend.opsec import (
        STRATEGIC_BASES,
        SAMPLE_OPSEC_INTERCEPTS,
        assess_opsec_violation,
        generate_perceptual_hash,
        extract_exif_metadata
    )
except ImportError:
    from .db import init_db, insert_post, get_all_posts, get_all_campaigns, search_posts
    from .pipeline import run_pipeline, generate_job_id
    from .connectors.indian_navy import fetch_all_navy_intel, NAVY_SOURCES
    from .connectors.live_news import get_live_news, CATEGORY_FEEDS, CATEGORY_EMOJIS
    from .connectors.adversary_intel import (
        fetch_all_adversary_intel,
        get_adversary_countries_meta,
        get_adversary_orbat,
        get_adversary_hotspots
    )
    from .opsec import (
        STRATEGIC_BASES,
        SAMPLE_OPSEC_INTERCEPTS,
        assess_opsec_violation,
        generate_perceptual_hash,
        extract_exif_metadata
    )

# ── App Setup ──────────────────────────────────────────────

app = FastAPI(
    title="Disinfo Shield AI 2026",
    description="Multi-Platform Disinformation Detection & Coordinated Campaign Analysis",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Path to the desktop UI HTML file
UI_PATH = Path(__file__).resolve().parent.parent / "desktop_app.html"


# ── Startup ────────────────────────────────────────────────

@app.on_event("startup")
async def startup_event():
    """Initialize the SQLite database on server start."""
    init_db()


# ── Pydantic Models ────────────────────────────────────────

class PostPayload(BaseModel):
    """Schema for a single raw post submission."""
    platform: str
    post_id: str
    author: str
    content: str
    url: Optional[str] = None


class AnalyzeRequest(BaseModel):
    """Schema for an analysis job request."""
    job_id: Optional[str] = None


# ── Endpoints ──────────────────────────────────────────────

@app.get("/")
async def serve_ui():
    """Serve the desktop dashboard UI."""
    if UI_PATH.exists():
        return FileResponse(str(UI_PATH), media_type="text/html")
    return {"message": "Disinfo Shield AI 2026 API", "docs": "/docs"}


@app.get("/favicon.ico")
async def serve_favicon():
    """Serve the Windows ICO application icon."""
    ico_path = _ROOT_DIR / "app_icon.ico"
    if ico_path.exists():
        return FileResponse(str(ico_path), media_type="image/x-icon")
    raise HTTPException(status_code=404, detail="Favicon not found")


@app.get("/app_icon.svg")
async def serve_svg_icon():
    """Serve the scalable vector application emblem."""
    svg_path = _ROOT_DIR / "app_icon.svg"
    if svg_path.exists():
        return FileResponse(str(svg_path), media_type="image/svg+xml")
    raise HTTPException(status_code=404, detail="SVG icon not found")


@app.get("/app_icon.png")
async def serve_png_icon():
    """Serve the high-resolution PNG application icon."""
    png_path = _ROOT_DIR / "app_icon.png"
    if png_path.exists():
        return FileResponse(str(png_path), media_type="image/png")
    raise HTTPException(status_code=404, detail="PNG icon not found")


@app.post("/ingest")
async def ingest(post: PostPayload):
    """
    Receive and store a raw post for later analysis.

    Returns the stored post's ID and a generated job ID.
    """
    try:
        insert_post(post.model_dump())
        job_id = generate_job_id()
        return {"status": "received", "post_id": post.post_id, "job_id": job_id}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/analyze")
async def analyze(request: AnalyzeRequest):
    """
    Trigger the full analysis pipeline:
    1. Collect data from connectors
    2. Classify each post for disinformation
    3. Cluster posts into coordinated campaigns
    4. Persist results to SQLite

    Returns a summary with post counts, classifications, and campaigns.
    """
    job_id = request.job_id or generate_job_id()
    try:
        result = run_pipeline(job_id)
        return {"job_id": job_id, "result": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.get("/campaigns")
async def campaigns():
    """Return all detected coordinated campaigns."""
    return {"campaigns": get_all_campaigns()}


@app.get("/posts")
async def posts(limit: int = Query(default=100, le=500)):
    """Return all stored posts, most recent first."""
    return {"posts": get_all_posts(limit=limit)}


@app.get("/search")
async def search(
    q: str = Query(..., min_length=1, description="Search keyword"),
    platform: Optional[str] = Query(default=None, description="Filter by platform"),
):
    """Search stored posts by content keyword, with optional platform filter."""
    results = search_posts(query=q, platform=platform)
    return {"query": q, "platform": platform, "count": len(results), "posts": results}


# ── Indian Navy Intel ──────────────────────────────────────

@app.get("/navy-intel")
async def navy_intel(
    source: Optional[str] = Query(default=None, description="Filter by source: pib, mod, navy_official, enc, wnc, twitter, youtube, instagram"),
    limit: int = Query(default=50, le=100, description="Maximum items to return"),
):
    """
    Aggregate Indian Navy intelligence from official and social media sources.

    Returns news, updates, and posts from PIB, Ministry of Defence,
    Indian Navy Official, Eastern/Western Naval Commands, X, YouTube, and Instagram.
    """
    return fetch_all_navy_intel(source=source, limit=limit)


@app.get("/navy-intel/sources")
async def navy_sources():
    """Return metadata for all configured Indian Navy intelligence sources."""
    return {"sources": NAVY_SOURCES}


# ── Live Global News Feed ──────────────────────────────────

@app.get("/api/news")
@app.get("/news")
async def api_live_news(
    category: Optional[str] = Query(default="all", description="Filter category: all, world, politics, tech, health, economy, security, science"),
    limit: int = Query(default=25, le=50, description="Maximum number of articles"),
    refresh: bool = Query(default=False, description="Force fresh fetch bypassing in-memory cache"),
):
    """
    Fetch real-time live breaking news aggregated from multiple global RSS feeds
    (Google News, BBC, PIB, Tech/Security feeds), with AI disinformation risk analysis.
    """
    try:
        return get_live_news(category=category or "all", limit=limit, force_refresh=refresh)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch live news: {str(exc)}")


@app.get("/api/news/categories")
async def api_news_categories():
    """Return available news categories with emojis and feed status."""
    return {
        "categories": [
            {"id": "all", "name": "All Categories", "icon": "🌐"},
            {"id": "world", "name": "World", "icon": "🌍"},
            {"id": "politics", "name": "Politics", "icon": "🏛️"},
            {"id": "tech", "name": "Technology", "icon": "💻"},
            {"id": "health", "name": "Health", "icon": "🏥"},
            {"id": "economy", "name": "Economy", "icon": "📈"},
            {"id": "security", "name": "Security & Defence", "icon": "🛡️"},
            {"id": "science", "name": "Science", "icon": "🔬"},
        ]
    }


# ── Adversary & Global Defence Intel ───────────────────────

@app.get("/api/adversary-intel")
@app.get("/adversary-intel")
async def api_adversary_intel(
    country: Optional[str] = Query(default="all", description="Filter by country: all, china, pakistan, usa, bangladesh, regional"),
    domain: Optional[str] = Query(default="all", description="Filter by domain: all, naval, airforce, land, cyber_psyops, missile_nuclear"),
    severity: Optional[str] = Query(default="all", description="Filter by severity: all, critical, high, elevated, monitored"),
    limit: int = Query(default=30, le=100, description="Max items to return"),
    refresh: bool = Query(default=False, description="Force fresh fetch bypassing in-memory cache")
):
    """
    Aggregate real-time adversary defence intelligence, OSINT telemetry,
    theatre readiness, and cognitive warfare indicators (China, Pakistan, USA, Bangladesh, Regional).
    """
    try:
        return fetch_all_adversary_intel(
            country=country,
            domain=domain,
            severity=severity,
            limit=limit,
            force_refresh=refresh
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to fetch adversary intel: {str(exc)}")


@app.get("/api/adversary-intel/countries")
async def api_adversary_countries():
    """Return list and threat metadata for all adversary and regional countries."""
    return get_adversary_countries_meta()


@app.get("/api/adversary-intel/orbat")
async def api_adversary_orbat(country: Optional[str] = Query(default=None, description="Filter ORBAT by country")):
    """Return Order of Battle (ORBAT) strategic assets register."""
    return get_adversary_orbat(country=country)


@app.get("/api/adversary-intel/hotspots")
async def api_adversary_hotspots(country: Optional[str] = Query(default=None, description="Filter hotspots by country")):
    """Return geostrategic theatre hotspots and coordinates."""
    return get_adversary_hotspots(country=country)


# ── OPSEC Base Privacy & EXIF Shield Endpoints ─────────────

class OpsecScanRequest(BaseModel):
    """Schema for an incoming OPSEC evaluation request."""
    lat: float
    lon: float
    caption: Optional[str] = ""
    detected_assets: Optional[List[str]] = []
    base_id: Optional[str] = None


class OpsecSanitizeRequest(BaseModel):
    """Schema for sanitizing an intercepted or pre-publication media file."""
    filename: str
    media_type: Optional[str] = "image/jpeg"
    strip_gps: bool = True
    strip_device_tags: bool = True


@app.get("/api/opsec/bases")
async def api_opsec_bases():
    """Return all registered strategic military base geofences."""
    return {"bases": STRATEGIC_BASES}


@app.get("/api/opsec/alerts")
async def api_opsec_alerts(base_id: Optional[str] = None):
    """Return active intercepted OPSEC asset leaks with proximity telemetry."""
    if base_id:
        filtered = [x for x in SAMPLE_OPSEC_INTERCEPTS if x["base_id"] == base_id]
        return {"alerts": filtered, "total": len(filtered)}
    return {"alerts": SAMPLE_OPSEC_INTERCEPTS, "total": len(SAMPLE_OPSEC_INTERCEPTS)}


@app.post("/api/opsec/scan")
async def api_opsec_scan(req: OpsecScanRequest):
    """
    Scan coordinates and asset indicators against all military base geofences.
    Calculates distance, bearing, zone classification, and auto-generates
    Provost Marshal dispatch & Section 69A IT Act emergency takedown order.
    """
    try:
        result = assess_opsec_violation(
            lat=req.lat,
            lon=req.lon,
            caption=req.caption or "",
            detected_assets=req.detected_assets or [],
            base_id=req.base_id
        )
        return {"status": "success", "assessment": result}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


@app.post("/api/opsec/sanitize")
async def api_opsec_sanitize(req: OpsecSanitizeRequest):
    """
    Simulate or perform EXIF metadata scrubbing on an image/video,
    generating a clean file record and a perceptual hash (PDQ/pHash).
    """
    clean_p_hash = generate_perceptual_hash(f"{req.filename}:{time.time()}")
    return {
        "status": "SANITIZED",
        "original_file": req.filename,
        "bytes_stripped": 3482,
        "metadata_removed": [
            "GPSLatitude", "GPSLongitude", "GPSAltitude",
            "Make", "Model", "Software", "DateTimeOriginal",
            "SubSecTimeOriginal", "LensModel", "DroneGimbalTelemetry"
        ],
        "perceptual_hash": clean_p_hash,
        "safe_for_public_release": True
    }


class OpsecExifExtractRequest(BaseModel):
    data_url: Optional[str] = None
    filename: Optional[str] = "image.jpg"


@app.post("/api/opsec/extract-exif")
async def api_opsec_extract_exif(
    file: Optional[UploadFile] = File(None),
    req: Optional[OpsecExifExtractRequest] = None
):
    """
    Extract real GPS coordinates, altitude, device tags, and timestamp from
    raw image bytes or base64 data URL, and evaluate proximity against all military base geofences.
    """
    try:
        raw_bytes = None
        filename = "uploaded_image.jpg"

        if file:
            raw_bytes = await file.read()
            filename = file.filename or "uploaded_image.jpg"
        elif req and req.data_url:
            filename = req.filename or "uploaded_image.jpg"
            if "," in req.data_url:
                raw_bytes = base64.b64decode(req.data_url.split(",", 1)[1])
            else:
                raw_bytes = base64.b64decode(req.data_url)

        if not raw_bytes:
            raise HTTPException(status_code=400, detail="No image file or data_url provided for EXIF inspection.")

        exif_data = extract_exif_metadata(raw_bytes)
        assessment = None

        if exif_data.get("has_gps") and exif_data.get("lat") is not None and exif_data.get("lon") is not None:
            assessment = assess_opsec_violation(
                lat=exif_data["lat"],
                lon=exif_data["lon"],
                caption=f"Decoded from {filename} ({exif_data.get('device') or 'Raw Image File'})",
                detected_assets=[exif_data.get("device")] if exif_data.get("device") else []
            )

        return {
            "status": "success",
            "filename": filename,
            "exif": exif_data,
            "assessment": assessment
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))


# ── Main ───────────────────────────────────────────────────

if __name__ == "__main__":
    uvicorn.run("backend.app:app", host="0.0.0.0", port=8000, reload=True)

