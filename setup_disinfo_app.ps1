Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Write-File($Path, [string]$Content) {
    $dir = Split-Path $Path -Parent
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }
    $Content | Set-Content -Path $Path -Encoding UTF8
    Write-Host "✔ Created $Path"
}

# --------------------------------------------------------------
# 1️⃣  Create the directory layout
# --------------------------------------------------------------
$folders = @(
    "backend",
    "backend\\connectors",
    "backend\\models",
    "frontend\\src",
    "frontend\\public",
    "data"
)
foreach ($f in $folders) {
    $full = Join-Path $PWD $f
    if (-not (Test-Path $full)) { New-Item -ItemType Directory -Force -Path $full | Out-Null }
}
Write-Host "`nFolder structure ready.`n"

# --------------------------------------------------------------
# 2️⃣  Backend – FastAPI entry point (backend/app.py)
# --------------------------------------------------------------
$backendApp = @"
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

from .pipeline import run_pipeline_for_job, generate_job_id
from .db import init_db, insert_post, get_all_campaigns

app = FastAPI(title=\"Disinfo Desktop Backend\")

# ---- CORS – allow the local UI to call the API ----
app.add_middleware(
    CORSMiddleware,
    allow_origins=[\"*\"],
    allow_credentials=True,
    allow_methods=[\"*\"],
    allow_headers=[\"*\"]
)

# ---- Initialise SQLite on startup ----
@app.on_event(\"startup\")
async def startup_event():
    init_db()

# ---- Payload model for a single raw post ----
class PostPayload(BaseModel):
    platform: str          # e.g. \"twitter\"
    post_id: str
    author: str
    content: str
    url: str | None = None

# ------------------------------------------------------------
# /ingest – store a raw post and get a job id back
# ------------------------------------------------------------
@app.post(\"/ingest\")
async def ingest(post: PostPayload):
    try:
        insert_post(post.dict())
        job_id = generate_job_id()
        return {\"status\": \"received\", \"job_id\": job_id}
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

# ------------------------------------------------------------
# /analyze – run the full pipeline for a job id
# ------------------------------------------------------------
@app.post(\"/analyze\")
async def analyze(job_id: str):
    result = run_pipeline_for_job(job_id)
    return {\"job_id\": job_id, \"result\": result}

# ------------------------------------------------------------
# /campaigns – retrieve all detected campaigns
# ------------------------------------------------------------
@app.get(\"/campaigns\")
async def campaigns():
    return {\"campaigns\": get_all_campaigns()}

if __name__ == \"__main__\":
    uvicorn.run(\"backend.app:app\", host=\"0.0.0.0\", port=8000, reload=True)
"@
Write-File "$PWD\\backend\\app.py" $backendApp

# --------------------------------------------------------------
# 3️⃣  Backend – SQLite helpers (backend/db.py)
# --------------------------------------------------------------
$backendDb = @"
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / \"data\" / \"disinfo.db\"

def _connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            platform TEXT,
            post_id TEXT,
            author TEXT,
            content TEXT,
            url TEXT
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            post_ids TEXT   -- comma‑separated list of post_id values
        )
    """)
    conn.commit()
    conn.close()

def insert_post(payload: dict):
    conn = _connect()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO posts (platform, post_id, author, content, url)
        VALUES (:platform, :post_id, :author, :content, :url)
    """, payload)
    conn.commit()
    conn.close()

def get_all_campaigns():
    conn = _connect()
    cur = conn.cursor()
    cur.execute("SELECT id, name, description, post_ids FROM campaigns")
    rows = cur.fetchall()
    conn.close()
    return [
        {\"id\": r[0], \"name\": r[1], \"description\": r[2], \"post_ids\": r[3].split(\",\") if r[3] else []}
        for r in rows
    ]
"@
Write-File "$PWD\\backend\\db.py" $backendDb

# --------------------------------------------------------------
# 4️⃣  Backend – Pipeline orchestration (backend/pipeline.py)
# --------------------------------------------------------------
$pipeline = @"
import uuid
from typing import List, Dict, Any
from .connectors.twitter import fetch_recent_tweets
from .connectors.reddit import fetch_recent_submissions
from .models.disinfo_classifier import classify_text
from .models.campaign_cluster import cluster_posts

def generate_job_id() -> str:
    return str(uuid.uuid4())

def _collect_posts(job_id: str) -> List[Dict[str, Any]]:
    tweets = fetch_recent_tweets(query=\"COVID\", max_results=20)
    reddit = fetch_recent_submissions(subreddit=\"worldnews\", limit=20)
    return tweets + reddit

def _run_classification(posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    for p in posts:
        label, conf = classify_text(p[\"content\"])
        p[\"label\"] = label
        p[\"confidence\"] = conf
    return posts

def _run_clustering(classified_posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return cluster_posts(classified_posts)

def run_pipeline_for_job(job_id: str) -> Dict[str, Any]:
    raw = _collect_posts(job_id)
    classified = _run_classification(raw)
    campaigns = _run_clustering(classified)
    return {
        \"job_id\": job_id,
        \"num_posts\": len(raw),
        \"num_campaigns\": len(campaigns),
        \"campaigns\": campaigns,
    }
"@
Write-File "$PWD\\backend\\pipeline.py" $pipeline

# --------------------------------------------------------------
# 5️⃣  Backend – Twitter connector stub (backend/connectors/twitter.py)
# --------------------------------------------------------------
$twitter = @"
def fetch_recent_tweets(query: str, max_results: int = 10):
    return [
        {
            \"platform\": \"twitter\",
            \"post_id\": f\"tw_{i}\",
            \"author\": f\"user_{i}\",
            \"content\": f\"Fake tweet about {query} #{i}\",
            \"url\": f\"https://twitter.com/user_{i}/status/{i}\"
        }
        for i in range(max_results)
    ]
"@
Write-File "$PWD\\backend\\connectors\\twitter.py" $twitter

# --------------------------------------------------------------
# 6️⃣  Backend – Reddit connector stub (backend/connectors/reddit.py)
# --------------------------------------------------------------
$reddit = @"
def fetch_recent_submissions(subreddit: str, limit: int = 10):
    return [
        {
            \"platform\": \"reddit\",
            \"post_id\": f\"rd_{i}\",
            \"author\": f\"redditor_{i}\",
            \"content\": f\"Fake Reddit post about {subreddit} #{i}\",
            \"url\": f\"https://reddit.com/r/{subreddit}/comments/{i}\"
        }
        for i in range(limit)
    ]
"@
Write-File "$PWD\\backend\\connectors\\reddit.py" $reddit

# --------------------------------------------------------------
# 7️⃣  Backend – Model wrappers (backend/models)
# --------------------------------------------------------------
# 7a – Fake‑news classifier (backend/models/disinfo_classifier.py)
$clf = @"
from typing import Tuple

def classify_text(text: str) -> Tuple[str, float]:
    if \"fake\" in text.lower():
        return (\"misinformation\", 0.95)
    return (\"real\", 0.99)
"@
Write-File "$PWD\\backend\\models\\disinfo_classifier.py" $clf

# 7b – Campaign clustering (backend/models/campaign_cluster.py)
$cluster = @"
from typing import List, Dict

def cluster_posts(posts: List[Dict]) -> List[Dict]:
    groups = {}
    for p in posts:
        key = p[\"content\"].split()[0]
        groups.setdefault(key, []).append(p[\"post_id\"])
    campaigns = []
    for i, (k, ids) in enumerate(groups.items(), start=1):
        campaigns.append({
            \"name\": f\"Campaign {i} (key={k})\",
            \"description\": f\"Posts that start with the word '{k}'\",
            \"post_ids\": ids
        })
    return campaigns
"@
Write-File "$PWD\\backend\\models\\campaign_cluster.py" $cluster

# --------------------------------------------------------------
# 8️⃣  Frontend – Minimal Vue 3 UI (frontend folder)
# --------------------------------------------------------------
# package.json
$frontendPkg = @"
{
  \"name\": \"disinfo-frontend\",
  \"version\": \"0.1.0\",
  \"private\": true,
  \"scripts\": {
    \"dev\": \"vite\",
    \"build\": \"vite build\",
    \"preview\": \"vite preview\"
  },
  \"dependencies\": {
    \"axios\": \"^1.7.2\",
    \"vue\": \"^3.4.27\"
  },
  \"devDependencies\": {
    \"@vitejs/plugin-vue\": \"^5.1.0\",
    \"vite\": \"^5.3.1\"
  }
}
"@
Write-File "$PWD\\frontend\\package.json" $frontendPkg

# vite.config.js
$viteCfg = @"
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\\/api/, '')
      }
    }
  }
})
"@
Write-File "$PWD\\frontend\\vite.config.js" $viteCfg

# src/main.js
$mainJs = @"
import { createApp } from 'vue'
import App from './App.vue'

createApp(App).mount('#app')
"@
Write-File "$PWD\\frontend\\src\\main.js" $mainJs

# src/App.vue (tiny dashboard)
$appVue = @"
<template>
  <div class=\"container\">
    <h1>Disinformation Detection Dashboard</h1>
    <button @click=\"runAnalysis\" :disabled=\"loading\">
      {{ loading ? 'Running…' : 'Run Full Analysis' }}
    </button>
    <section v-if=\"campaigns.length\">
      <h2>Detected Campaigns</h2>
      <ul>
        <li v-for=\"c in campaigns\" :key=\"c.id\">
          <strong>{{ c.name }}</strong> – {{ c.description }}<br/>
          Posts: {{ c.post_ids.join(', ') }}
        </li>
      </ul>
    </section>
    <section v-else-if=\"!loading\">
      <p>No campaigns yet. Click the button above to start.</p>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'

const loading = ref(false)
const campaigns = ref([])

async function runAnalysis() {
  loading.value = true
  try {
    await axios.post('/api/analyze', { job_id: "demo" })
    const res = await axios.get('/api/campaigns')
    campaigns.value = res.data.campaigns
  } catch (e) {
    console.error(e)
    alert('Error running analysis')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.container { max-width: 800px; margin: 2rem auto; font-family: Arial, sans-serif; }
button { padding: 0.5rem 1rem; margin: 1rem 0; }
</style>
"@
Write-File "$PWD\\frontend\\src\\App.vue" $appVue

# --------------------------------------------------------------
# 9️⃣  Create a simple batch file to run the whole app
# --------------------------------------------------------------
$runBat = @"
@echo off
cd /d "%~dp0"
rem Activate the Python venv (if it exists)
if exist .\\venv\\Scripts\\activate.bat (
    call .\\venv\\Scripts\\activate.bat
) else (
    python -m venv .\\venv
    call .\\venv\\Scripts\\activate.bat
    pip install fastapi uvicorn
)
rem Start the backend in a new window
start "backend" uvicorn backend.app:app --host 0.0.0.0 --port 8000
rem Give the server a moment to start
timeout /t 2 >nul
rem Launch the frontend dev server (will open a browser window)
cd frontend
npm install
npm run dev
"@
Write-File "$PWD\\run_app.bat" $runBat

# --------------------------------------------------------------
# Done – inform the user
# --------------------------------------------------------------
Write-Host "Bootstrap script and project skeleton have been generated as artifacts.\n\nTo use them, copy the files from the artifact directory to your workspace (d:\\Antigravjity workshowp) and then run the batch file."
