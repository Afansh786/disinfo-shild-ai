# Disinfo Shield AI 2026

AI-powered disinformation detection and coordinated campaign analysis across 8 digital platforms.

## Features

- **Multi-Platform Coverage**: WhatsApp, Instagram, TikTok, X/Twitter, Telegram, Reddit, Facebook, YouTube
- **AI Text Classifier**: Rule-based forensic NLP that scores text for disinformation signals
- **Campaign Clustering**: Groups posts into coordinated campaigns by keyword similarity
- **Interactive Network Graph**: vis.js force-directed graph with per-platform filtering
- **Temporal Analysis**: Cross-platform amplification charts and cascade lifecycle diagrams
- **Intercepted Feed**: Real-time table with CIB scores, platform badges, and CSV export
- **Desktop App Mode**: Launch in a frameless browser window via batch script

## Repository Structure

```
backend/
├── app.py               # FastAPI entry point (serves API + UI)
├── db.py                # SQLite persistence layer
├── pipeline.py          # 3-stage analysis pipeline
├── connectors/
│   ├── twitter.py       # Twitter/X data connector
│   └── reddit.py        # Reddit data connector
models/
├── disinfo_classifier.py  # Disinformation text classifier
└── campaign_cluster.py    # Campaign clustering engine
data/                      # SQLite database (auto-created)
desktop_app.html           # Self-contained analyst dashboard
Launch_Disinfo_App.bat     # Desktop launcher (Edge/Chrome --app mode)
```

## Quick Start

### Option A: Open the Dashboard Directly
Double-click `Launch_Disinfo_App.bat` — opens the dashboard in a frameless browser window.
The UI works standalone with built-in sample data.

### Option B: Run the Full Backend
```bash
# Create virtual environment
python -m venv venv
.\venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn backend.app:app --reload

# Open http://localhost:8000 in your browser
```

### Option C: Docker
```bash
docker-compose up --build
# Open http://localhost:8000
```

## API Endpoints

| Method | Endpoint    | Description                        |
|--------|-------------|------------------------------------|
| GET    | `/`         | Serve the desktop dashboard UI     |
| POST   | `/ingest`   | Submit a raw post for storage      |
| POST   | `/analyze`  | Run the full analysis pipeline     |
| GET    | `/campaigns`| Retrieve detected campaigns        |
| GET    | `/posts`    | List all stored posts              |
| GET    | `/search`   | Search posts by keyword & platform |

## Technology Stack

- **Backend**: Python 3.11 + FastAPI + SQLite
- **Frontend**: Vanilla HTML/CSS/JS (self-contained single file)
- **Visualization**: vis.js (network graph) + Chart.js (temporal charts)
- **Design**: Inter font, dark glassmorphism, CSS custom properties

## License

MIT
