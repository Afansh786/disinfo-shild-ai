"""
Disinfo Shield AI 2026 — Base OPSEC & EXIF Sanitization Engine
--------------------------------------------------------------
Provides geospatial geofencing around strategic military bases,
EXIF inspection, telemetry proximity scoring, perceptual hashing,
and automated legal emergency takedown generation.
"""

import math
import hashlib
import time
import io
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
from PIL import Image

# ── Strategic Military Bases Registry ────────────────────────

STRATEGIC_BASES = [
    {
        "id": "AFB_PATHANKOT",
        "name": "Western Sector Air Force Station (Pathankot AFS)",
        "short_name": "Pathankot Airbase",
        "branch": "Indian Air Force",
        "type": "Forward Fighter Wing & Radar Command",
        "lat": 32.2333,
        "lon": 75.6344,
        "inner_radius_km": 2.5,
        "amber_radius_km": 6.0,
        "outer_radius_km": 15.0,
        "provost_office": "Air Provost Marshal, Western Air Command",
        "active_assets": ["MiG-21 Bison / Rafale detachment", "Air Defence Radar Array", "Ammo Storage Area 4"]
    },
    {
        "id": "LEH_SECTOR_4",
        "name": "Northern Command High-Altitude Forward Post (Leh Sector)",
        "short_name": "Leh Forward Airbase",
        "branch": "Tri-Service (Army & IAF)",
        "type": "Mountain Strike Logistics & High-Altitude Runway",
        "lat": 34.1359,
        "lon": 77.5465,
        "inner_radius_km": 3.0,
        "amber_radius_km": 8.0,
        "outer_radius_km": 20.0,
        "provost_office": "Corps Provost Marshal, 14 Corps (Fire & Fury)",
        "active_assets": ["Heavy Lift IL-76 / C-17 Ramp", "Artillery Transit Convoy Route NH-1D"]
    },
    {
        "id": "NAVY_INS_KADAMBA",
        "name": "Project Seabird Strategic Naval Base (INS Kadamba, Karwar)",
        "short_name": "INS Kadamba (Karwar)",
        "branch": "Indian Navy",
        "type": "Strategic Aircraft Carrier Dock & Submarine Pens",
        "lat": 14.7744,
        "lon": 74.1528,
        "inner_radius_km": 4.0,
        "amber_radius_km": 10.0,
        "outer_radius_km": 25.0,
        "provost_office": "Naval Provost Marshal, Western Naval Command",
        "active_assets": ["INS Vikramaditya Berthing Berth 2", "Submarine Shiplift Facility", "Naval Ammunition Depot"]
    },
    {
        "id": "ENC_VIZAG",
        "name": "Eastern Naval Command Headquarters & Dockyard (INS Dega, Vizag)",
        "short_name": "INS Dega & Vizag Dockyard",
        "branch": "Indian Navy",
        "type": "Nuclear Submarine Operational Base & Fleet HQ",
        "lat": 17.7212,
        "lon": 83.2245,
        "inner_radius_km": 3.0,
        "amber_radius_km": 7.0,
        "outer_radius_km": 18.0,
        "provost_office": "Command Provost Marshal, Eastern Naval Command",
        "active_assets": ["SSBN Dry Dock Area", "Anti-Submarine Warfare Command", "Naval Air Station Runways"]
    },
    {
        "id": "ARMY_WESTERN_HQ",
        "name": "Western Command Headquarters (Chandimandir Military Station)",
        "short_name": "Chandimandir Mil Station",
        "branch": "Indian Army",
        "type": "Theater Headquarters & Tactical Communications Hub",
        "lat": 30.7189,
        "lon": 76.8833,
        "inner_radius_km": 2.0,
        "amber_radius_km": 5.0,
        "outer_radius_km": 12.0,
        "provost_office": "Provost Marshal, Western Command",
        "active_assets": ["Corps Signals Center", "Forward Logistics Division Depot"]
    },
    {
        "id": "SILIGURI_SUKNA",
        "name": "Trishakti Corps Headquarters & Siliguri Corridor (Sukna Military Station)",
        "short_name": "Sukna (Siliguri Corridor)",
        "branch": "Indian Army",
        "type": "Strategic Chicken's Neck Chokepoint Defense Hub",
        "lat": 26.7820,
        "lon": 88.3560,
        "inner_radius_km": 3.0,
        "amber_radius_km": 7.5,
        "outer_radius_km": 20.0,
        "provost_office": "Provost Marshal, 33 Corps (Trishakti)",
        "active_assets": ["Armored Convoy Staging Ground", "NH-10 Strategic Transit Corridor"]
    },
    {
        "id": "SNC_INS_VENDURUTHY",
        "name": "Southern Naval Command Headquarters & Naval Base (INS Venduruthy, Kochi)",
        "short_name": "INS Venduruthy (Kochi)",
        "branch": "Indian Navy",
        "type": "Southern Naval Command HQ, Naval Aviation, Aircraft Carrier Training & Dockyard",
        "lat": 9.9575,
        "lon": 76.2730,
        "inner_radius_km": 3.0,
        "amber_radius_km": 8.0,
        "outer_radius_km": 20.0,
        "provost_office": "Command Provost Marshal, Southern Naval Command (SNC)",
        "active_assets": ["Aircraft Carrier Dry Dock & Berths", "Naval Air Station (INS Garuda)", "NPOL Underwater Sensor Labs"]
    }
]

# ── Sample Intercepted OPSEC Leaks ───────────────────────────

SAMPLE_OPSEC_INTERCEPTS = [
    {
        "id": "OPSEC-LEAK-2026-081",
        "base_id": "AFB_PATHANKOT",
        "platform": "Instagram Public Reel",
        "author": "@aero_spotter_punjab",
        "timestamp": "12 mins ago",
        "source_type": "Civilian Smartphone (Apple iPhone 15 Pro)",
        "lat": 32.2341,
        "lon": 75.6350,
        "altitude_m": 312,
        "distance_km": 0.85,
        "zone": "CRITICAL_INNER",
        "zone_label": "Zone 1: Restricted Runway Perimeter (< 2 km)",
        "detected_assets": ["Su-30MKI Tail Fin #SB-142", "Active Radar Antenna", "Perimeter Blast Wall"],
        "caption": "Spotted these beasts taking off for night sorties! Sound is unreal #IndianAirForce #Pathankot #FighterJets",
        "risk_score": 96.4,
        "exif_status": "EXPOSED (Raw GPS & Altitude Embedded)",
        "p_hash": "pdq:9f2c817ea01944cb89a",
        "recommended_action": "Emergency Platform Section 69A IT Act Blocking Order & Base Alert",
        "status": "FLAGGED_FOR_TAKEDOWN"
    },
    {
        "id": "OPSEC-LEAK-2026-082",
        "base_id": "NAVY_INS_KADAMBA",
        "platform": "Telegram Public Channel",
        "author": "Maritime_Watch_Global",
        "timestamp": "42 mins ago",
        "source_type": "Commercial Drone Aerial Still (DJI Mavic 3)",
        "lat": 14.7758,
        "lon": 74.1542,
        "altitude_m": 120,
        "distance_km": 1.15,
        "zone": "CRITICAL_INNER",
        "zone_label": "Zone 1: Naval Shipyard & Berthing Basin (< 2 km)",
        "detected_assets": ["Kalvari-class Submarine Hull in Shiplift", "Berth Maintenance Rig"],
        "caption": "Exclusive satellite and drone views of Karwar Seabird base phase 2 construction and drydock operations.",
        "risk_score": 98.7,
        "exif_status": "EXPOSED (GPS Coordinates, Gimbal Pitch, Altitude)",
        "p_hash": "pdq:1a77e38c900fb2517aa",
        "recommended_action": "Anti-Drone Patrol Scramble & Immediate Hash Suppression Notice",
        "status": "FLAGGED_FOR_TAKEDOWN"
    },
    {
        "id": "OPSEC-LEAK-2026-083",
        "base_id": "LEH_SECTOR_4",
        "platform": "X (Twitter)",
        "author": "@himalayan_nomad_vlogs",
        "timestamp": "1 hr ago",
        "source_type": "Dashboard Camera Video (GoPro Hero 12)",
        "lat": 34.1412,
        "lon": 77.5580,
        "altitude_m": 3480,
        "distance_km": 3.42,
        "zone": "AMBER_BUFFER",
        "zone_label": "Zone 2: Forward Logistics Highway Corridor (2-6 km)",
        "detected_assets": ["8 Military Transport Trucks (Ashok Leyland Stallion)", "Fuel Bowser Fleet", "Regimental Unit Crest"],
        "caption": "Heavy military movement heading towards the pass today! Endless convoys on Leh highway.",
        "risk_score": 84.2,
        "exif_status": "PARTIAL (Geotag Tagged on Post)",
        "p_hash": "pdq:5b32f18077c91a4590d",
        "recommended_action": "Contact User for Voluntary Deletion / Advise Highway Traffic Cell",
        "status": "PENDING_REVIEW"
    }
]

# ── Geospatial Calculation Helpers ───────────────────────────

def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the great-circle distance between two points in kilometers."""
    R = 6371.0  # Earth's mean radius in km
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2.0) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2.0) ** 2)
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))
    return round(R * c, 2)


def calculate_azimuth_bearing(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate the initial azimuth compass bearing from point 1 to point 2 (0-360 degrees)."""
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    delta_lambda = math.radians(lon2 - lon1)

    x = math.sin(delta_lambda) * math.cos(phi2)
    y = math.cos(phi1) * math.sin(phi2) - (math.sin(phi1) * math.cos(phi2) * math.cos(delta_lambda))
    initial_bearing = math.atan2(x, y)
    compass_bearing = (math.degrees(initial_bearing) + 360.0) % 360.0
    return round(compass_bearing, 1)


def generate_perceptual_hash(content_seed: str) -> str:
    """Generate a simulated 64-bit PDQ-style perceptual media hash."""
    raw_hash = hashlib.sha256(content_seed.encode("utf-8")).hexdigest()
    return f"pdq:{raw_hash[:16]}"


# ── OPSEC Assessment Core ────────────────────────────────────

def assess_opsec_violation(
    lat: float,
    lon: float,
    caption: str = "",
    detected_assets: Optional[List[str]] = None,
    base_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Evaluate an intercepted post/photo against all defense base geofences.
    Calculates proximity, threat zone ring, risk score, and auto-drafts
    official Provost and platform legal blocking dispatches.
    """
    if detected_assets is None:
        detected_assets = []

    # Find closest base or match requested base
    closest_base = None
    min_dist = float("inf")

    for base in STRATEGIC_BASES:
        if base_id and base["id"] == base_id:
            closest_base = base
            min_dist = haversine_distance_km(lat, lon, base["lat"], base["lon"])
            break
        dist = haversine_distance_km(lat, lon, base["lat"], base["lon"])
        if dist < min_dist:
            min_dist = dist
            closest_base = base

    if not closest_base:
        closest_base = STRATEGIC_BASES[0]
        min_dist = haversine_distance_km(lat, lon, closest_base["lat"], closest_base["lon"])

    bearing = calculate_azimuth_bearing(closest_base["lat"], closest_base["lon"], lat, lon)

    # Classify Zone Ring
    if min_dist <= closest_base["inner_radius_km"]:
        zone = "CRITICAL_INNER"
        zone_label = f"Zone 1: Restricted Core Perimeter (< {closest_base['inner_radius_km']} km)"
        geo_risk = 100
    elif min_dist <= closest_base["amber_radius_km"]:
        zone = "AMBER_BUFFER"
        zone_label = f"Zone 2: Tactical Approach & Convoy Corridor ({closest_base['inner_radius_km']}-{closest_base['amber_radius_km']} km)"
        geo_risk = 75
    elif min_dist <= closest_base["outer_radius_km"]:
        zone = "OUTER_ADVISORY"
        zone_label = f"Zone 3: Strategic Transit Buffer ({closest_base['amber_radius_km']}-{closest_base['outer_radius_km']} km)"
        geo_risk = 40
    else:
        zone = "CLEAR_CIVILIAN"
        zone_label = "Civilian Non-Restricted Zone (> 25 km)"
        geo_risk = 10

    # Asset Weighting
    asset_risk = min(len(detected_assets) * 30, 95) if detected_assets else 15

    # Sensitive keyword check in caption
    sensitive_keywords = ["convoy", "night sortie", "takeoff", "submarine", "radar", "fighter", "missile", "depot", "runway", "hangar", "patrol"]
    caption_hits = [kw for kw in sensitive_keywords if kw in caption.lower()]
    caption_risk = min(len(caption_hits) * 25, 90)

    # Weighted aggregate score
    risk_score = round(0.45 * geo_risk + 0.35 * asset_risk + 0.20 * caption_risk, 1)

    # Generate Legal & Operational Dispatches
    p_hash = generate_perceptual_hash(f"{lat}:{lon}:{caption}:{time.time()}")
    timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S UTC")

    provost_dispatch = (
        f"🚨 [FLASH PRIORITY OPSEC SITREP]\n"
        f"TIME: {timestamp_str}\n"
        f"TO: {closest_base['provost_office']}\n"
        f"SECTOR: {closest_base['name']}\n"
        f"INCIDENT: Public Social Media Asset Leakage within {min_dist} km (Bearing {bearing}°)\n"
        f"RISK EVALUATION: {risk_score}% ({zone})\n"
        f"EXPOSED ASSETS: {', '.join(detected_assets) if detected_assets else 'Perimeter / Geotag'}\n"
        f"PERCEPTUAL HASH: {p_hash}\n"
        f"RECOMMENDED ACTION: Dispatch Base Provost patrol to azimuth {bearing}° and initiate Section 69A IT Act Platform Quarantine."
    )

    legal_takedown_notice = (
        f"STATUTORY DEFENCE EMERGENCY BLOCKING NOTICE\n"
        f"Issued pursuant to Section 69A of Information Technology Act & Official Secrets Act, 1923\n"
        f"RE: Emergency Suppression of Compromised Defence Infrastructure Imagery\n"
        f"Affected Facility: {closest_base['name']}\n"
        f"Coordinates: {lat}° N, {lon}° E (Proximity: {min_dist} km to restricted installations)\n"
        f"Perceptual Media Hash (pHash / PDQ): {p_hash}\n"
        f"DIRECTIVE: Hosting intermediaries and platforms (Meta/X/Google/Telegram) are instructed to "
        f"immediately block the URL and ingest the above perceptual hash into automated upload suppression filters."
    )

    return {
        "base_id": closest_base["id"],
        "base_name": closest_base["name"],
        "short_name": closest_base["short_name"],
        "branch": closest_base["branch"],
        "lat": lat,
        "lon": lon,
        "distance_km": min_dist,
        "bearing_deg": bearing,
        "zone": zone,
        "zone_label": zone_label,
        "risk_score": risk_score,
        "detected_assets": detected_assets,
        "p_hash": p_hash,
        "provost_office": closest_base["provost_office"],
        "provost_dispatch": provost_dispatch,
        "legal_takedown_notice": legal_takedown_notice,
        "status": "EVALUATED"
    }


def extract_exif_metadata(image_bytes: bytes) -> Dict[str, Any]:
    """
    Extract real GPS coordinates, altitude, camera make/model, and timestamp
    from raw image bytes using Pillow native EXIF IFD traversal.
    """
    result = {
        "has_gps": False,
        "lat": None,
        "lon": None,
        "altitude_m": None,
        "make": None,
        "model": None,
        "device": None,
        "datetime": None,
        "tags_count": 0
    }
    try:
        img = Image.open(io.BytesIO(image_bytes))
        exif = img.getexif()
        if not exif:
            return result

        result["tags_count"] = len(exif)

        # 0x010F: Make, 0x0110: Model, 0x0132: DateTime
        make = exif.get(0x010F)
        model = exif.get(0x0110)
        dt = exif.get(0x0132)
        if make:
            result["make"] = str(make).strip()
        if model:
            result["model"] = str(model).strip()
        if dt:
            result["datetime"] = str(dt).strip()

        dev_parts = [result["make"], result["model"]]
        result["device"] = " ".join([p for p in dev_parts if p]) if any(dev_parts) else None

        # GPS IFD is tag 0x8825
        gps_ifd = exif.get_ifd(0x8825)
        if gps_ifd:
            lat_ref = gps_ifd.get(1, "N")
            lat_raw = gps_ifd.get(2)
            lon_ref = gps_ifd.get(3, "E")
            lon_raw = gps_ifd.get(4)
            alt_ref = gps_ifd.get(5, 0)
            alt_raw = gps_ifd.get(6)

            def dms_to_deg(dms):
                if not dms:
                    return None
                if isinstance(dms, (int, float)):
                    return float(dms)
                if len(dms) >= 3:
                    d = float(dms[0])
                    m = float(dms[1])
                    s = float(dms[2])
                    return d + (m / 60.0) + (s / 3600.0)
                return None

            lat = dms_to_deg(lat_raw)
            lon = dms_to_deg(lon_raw)

            if lat is not None and str(lat_ref).upper().startswith("S"):
                lat = -lat
            if lon is not None and str(lon_ref).upper().startswith("W"):
                lon = -lon

            if lat is not None and lon is not None:
                result["lat"] = round(lat, 6)
                result["lon"] = round(lon, 6)
                result["has_gps"] = True

            if alt_raw is not None:
                alt = float(alt_raw) if isinstance(alt_raw, (int, float)) else float(alt_raw[0])
                if alt_ref == 1:
                    alt = -alt
                result["altitude_m"] = round(alt, 1)

    except Exception:
        pass

    return result

