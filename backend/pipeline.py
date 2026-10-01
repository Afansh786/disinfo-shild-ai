"""
Disinfo Shield AI 2026 — Analysis Pipeline
--------------------------------------------
Orchestrates the three-stage analysis flow:
  1. Data Collection  → Platform connectors pull posts
  2. Classification   → Each post scored for disinformation
  3. Clustering       → Classified posts grouped into campaigns

Results are persisted to SQLite via the db module.
"""

import uuid
from typing import Any, Dict, List

from backend.connectors.twitter import fetch_recent_tweets
from backend.connectors.reddit import fetch_recent_submissions
from models.disinfo_classifier import classify_text
from models.campaign_cluster import cluster_posts
from backend.db import insert_post, insert_prediction, upsert_campaign


def generate_job_id() -> str:
    """Generate a unique job identifier."""
    return str(uuid.uuid4())


def _collect_data(job_id: str) -> List[Dict[str, Any]]:
    """
    Stage 1: Collect raw posts from all configured platform connectors.

    Returns a unified list of post dicts from Twitter and Reddit.
    """
    tweets = fetch_recent_tweets(query="disinfo", max_results=8)
    reddit_posts = fetch_recent_submissions(subreddit="worldnews", limit=6)
    return tweets + reddit_posts


def _run_classification(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Stage 2: Run the disinformation classifier on each post.

    Adds 'label' and 'confidence' keys to each post dict.
    """
    for post in posts:
        label, confidence = classify_text(post["content"])
        post["label"] = label
        post["confidence"] = confidence
    return posts


def _run_clustering(classified_posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Stage 3: Cluster posts into coordinated campaign groups.

    Returns a list of campaign summary dicts.
    """
    return cluster_posts(classified_posts)


def _persist_results(posts: List[Dict[str, Any]], campaigns: List[Dict[str, Any]]) -> None:
    """
    Persist all analysis results to SQLite.

    Stores each post, its prediction, and any detected campaigns.
    """
    for post in posts:
        try:
            insert_post({
                "platform": post["platform"],
                "post_id": post["post_id"],
                "author": post["author"],
                "content": post["content"],
                "url": post.get("url"),
            })
        except Exception:
            pass  # Skip duplicates silently

        if "label" in post:
            try:
                insert_prediction(post["post_id"], post["label"], post["confidence"])
            except Exception:
                pass

    for campaign in campaigns:
        if campaign["name"] != "Unclassified":
            try:
                upsert_campaign(
                    name=campaign["name"],
                    description=campaign["description"],
                    severity=campaign["severity"],
                    post_ids=campaign["post_ids"],
                )
            except Exception:
                pass


def run_pipeline(job_id: str) -> Dict[str, Any]:
    """
    Main pipeline entry point — called by the /analyze endpoint.

    Orchestrates collection → classification → clustering → persistence
    and returns a summary dict.
    """
    # Stage 1: Collect
    raw_posts = _collect_data(job_id)

    # Stage 2: Classify
    classified = _run_classification(raw_posts)

    # Stage 3: Cluster
    campaigns = _run_clustering(classified)

    # Persist everything
    _persist_results(classified, campaigns)

    # Build summary
    disinfo_count = sum(1 for p in classified if p.get("label") == "misinformation")
    suspicious_count = sum(1 for p in classified if p.get("label") == "suspicious")

    return {
        "job_id": job_id,
        "total_posts": len(raw_posts),
        "misinformation": disinfo_count,
        "suspicious": suspicious_count,
        "legitimate": len(raw_posts) - disinfo_count - suspicious_count,
        "campaigns_detected": len([c for c in campaigns if c["name"] != "Unclassified"]),
        "campaigns": campaigns,
        "posts": classified,
    }
