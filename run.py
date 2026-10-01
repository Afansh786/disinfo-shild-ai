"""
Disinfo Shield AI 2026 — Master Application Runner
---------------------------------------------------
Starts the FastAPI backend server and opens the dashboard UI in your default browser.

Usage:
    py -3 run.py
    or
    python run.py
"""

import sys
import os
import time
import socket
import threading
import webbrowser
from pathlib import Path

# Configure UTF-8 console output for Windows cmd compatibility
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

# Add project root directory to sys.path
ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

def is_port_in_use(port: int, host: str = "127.0.0.1") -> bool:
    """Check if a TCP port is currently occupied."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((host, port)) == 0

def kill_stale_port_process(port: int = 8000):
    """If a zombie process is holding the port on Windows, terminate it cleanly."""
    if sys.platform == "win32" and is_port_in_use(port):
        try:
            import subprocess
            cmd = f'powershell -Command "Get-NetTCPConnection -LocalPort {port} -ErrorAction SilentlyContinue | ForEach-Object {{ Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue }}"'
            subprocess.run(cmd, shell=True, timeout=3, capture_output=True)
            time.sleep(0.5)
        except Exception:
            pass

import uvicorn
from backend.app import app


def open_browser():
    """Wait for server to boot and open the browser dashboard."""
    time.sleep(1.2)
    url = "http://127.0.0.1:8000"
    print(f"\n[*] Opening Disinfo Shield AI dashboard: {url}")
    try:
        webbrowser.open(url)
    except Exception as e:
        print(f"[!] Could not open browser automatically: {e}")


if __name__ == "__main__":
    kill_stale_port_process(8000)

    print("=" * 68)
    print("   Disinfo Shield AI 2026 -- Multi-Platform Threat Forensics")
    print("=" * 68)
    print("   Dashboard UI   : http://127.0.0.1:8000/")
    print("   Swagger Docs   : http://127.0.0.1:8000/docs")
    print("   Press Ctrl+C to stop the server.")
    print("=" * 68)

    # Launch browser in a background daemon thread
    threading.Thread(target=open_browser, daemon=True).start()

    # Start FastAPI server on port 8000
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
