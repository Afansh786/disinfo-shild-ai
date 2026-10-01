# Full‑Featured Desktop Disinformation Detection & Coordinated Campaign Analysis

## Goal Description

Create a self‑contained desktop application (Windows) that:
- Collects data from selected digital platforms (Twitter, Reddit, YouTube, RSS news feeds).
- Detects false or misleading content using a fine‑tuned LLM/fake‑news classifier.
- Finds coordinated misinformation campaigns via text‑embedding clustering and network analysis.
- Provides an interactive graphical dashboard for analysts (search, filters, network graph, export reports).
- Runs locally without requiring external cloud services (all dependencies bundled).

## User Review Required

> [!IMPORTANT]
> This design introduces several substantial components that may affect your machine resources and legal compliance. Please confirm the following before we proceed:
>
> - **Target platforms**: which of the following do you need? (Twitter, Reddit, YouTube, RSS news sites, others).
> - **Model choice**: use an open‑source transformer (e.g., `distilbert‑finetuned‑fake‑news`) that runs on CPU, or a larger GPU‑accelerated model (requires a compatible GPU).
> - **Data volume**: expected number of posts per day (e.g., <10k, 10‑100k, >100k). This determines storage and processing requirements.
> - **Privacy**: you must store only public content; confirm you accept GDPR/CCPA compliance responsibilities.
> - **UI framework**: prefer a native Windows UI (e.g., Electron + React) or a web‑based UI served locally (FastAPI + browser UI). Both can be packaged as a desktop executable.
> - **Distribution**: Do you want a single installer (e.g., using Inno Setup) or just a zip you can run?

## Open Questions

> [!QUESTION]
> 1. Which platforms should the initial version support?
> 2. Do you have a labeled dataset for fine‑tuning the fake‑news classifier, or should we use a pre‑trained public model?
> 3. Will you run the app on a GPU‑enabled machine or CPU‑only?
> 4. Desired UI stack – Electron + React, or FastAPI + Vue served locally?
> 5. Any specific visualizations (e.g., force‑directed network graph, timeline view) you want out of the box?
> 6. Preferred packaging format: Windows installer (`.exe`) or portable folder?

## Proposed Changes

---
### 1. Project Scaffold

#### [NEW] [project_root](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/project_root)
- Top‑level layout with `backend/`, `frontend/`, `models/`, `data/`, `desktop/`, `scripts/`.

---
### 2. Backend (FastAPI) – Core Logic

#### [NEW] [backend/app.py](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/backend/app.py)
- FastAPI server exposing `/ingest`, `/analyze`, `/campaigns`, `/search`.
- Includes CORS support for the local UI.

#### [NEW] [backend/pipeline.py](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/backend/pipeline.py)
- Orchestrates collection, classification, clustering, and persistence.
- Uses SQLite for local storage (lightweight, no external DB).

---
### 3. Data Connectors (Desktop‑friendly)

#### [NEW] [backend/connectors/twitter.py](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/backend/connectors/twitter.py)
- Implements recent tweet search via Twitter API v2 (Bearer token from env).

#### [NEW] [backend/connectors/reddit.py](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/backend/connectors/reddit.py)
- Uses PRAW to pull submissions/comments.

#### [NEW] [backend/connectors/youtube.py](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/backend/connectors/youtube.py)
- Pulls video titles / comments via YouTube Data API.

---
### 4. Model Integration

#### [NEW] [models/disinfo_classifier.py](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/models/disinfo_classifier.py)
- Wrapper around a HuggingFace transformer (`distilbert-base-uncased-finetuned-fake-news`).
- Supports CPU‑only inference; optional GPU path if `torch.cuda.is_available()`.

#### [NEW] [models/campaign_cluster.py](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/models/campaign_cluster.py)
- Uses `sentence‑transformers` SBERT to embed posts, then DBSCAN for clustering.
- Returns campaign IDs and basic graph metadata.

---
### 5. Persistence Layer (SQLite)

#### [NEW] [backend/db.py](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/backend/db.py)
- Creates tables `posts`, `predictions`, `campaigns`.
- Simple CRUD helpers used by the pipeline.

---
### 6. Desktop UI

#### Option A – Electron + React (single‑exe bundle)
- **Folder:** `desktop/electron/`
- `main.js` launches a Chromium window pointing to `http://localhost:8000`.
- React app lives in `frontend/` (already scaffolded) and is built with `npm run build`.
- Packaging via `electron‑builder` → Windows installer (`.exe`).

#### Option B – FastAPI + Vue (served locally, launched via batch script)
- `frontend/` is a Vue SPA that calls the local FastAPI server.
- A small batch script `run_app.bat` starts the backend (via Python) **and** opens the default browser to `http://localhost:8000`.
- This option produces a portable folder – no installer required.

---
### 7. Packaging Scripts

#### [NEW] [scripts/build_desktop.bat](file:///C:/Users/ss/.gemini/antigravity/brain/739978e9-e038-4c12-9c3d-358d54d68016/scripts/build_desktop.bat)
- Creates a virtual‑env, installs Python deps, builds the Vue frontend (`npm ci && npm run build`).
- If Electron is chosen, runs `npm install && npm run electron:build`.
- Copies the whole folder to `dist/DisinfoApp/` ready for distribution.

---
### 8. Tests & CI

- Unit tests for each connector (mock API responses).
- Model inference sanity tests.
- Integration tests exercising the full pipeline (SQLite DB, fake data).
- CI workflow (GitHub Actions) that runs the tests and produces an artifact zip.

---
### 9. Verification Plan

#### Automated Tests
- `pytest` suite covering connectors, model wrappers, pipeline logic.
- `httpx` tests for FastAPI endpoints.

#### Manual Verification
- Run the installer/batch script on a fresh Windows machine.
- Ingest a sample CSV of 100 tweets, verify that the UI shows flagged items and a network graph.
- Export a CSV report and confirm its contents.

---
## Timeline (suggested)
1. **Week 1** – Scaffold repo, set up SQLite, implement data connectors for Twitter & Reddit.
2. **Week 2** – Integrate classifier model (CPU‑only), add inference API.
3. **Week 3** – Implement SBERT clustering and campaign storage.
4. **Week 4** – Build Vue dashboard (search, list, simple graph).
5. **Week 5** – Choose UI packaging (Electron or batch‑script) and implement build script.
6. **Week 6** – Write test suite, CI, generate Windows installer/portable zip.
7. **Week 7** – Manual QA on a clean Windows VM, fix bugs, finalize docs.

---
**Next Steps**
- Please answer the **Open Questions** above so I can lock‑in the technology choices and generate the concrete code for each component.
- Once approved, I’ll start creating the files and wiring them together.
