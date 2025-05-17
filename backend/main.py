#!/usr/bin/env python3
"""FastAPI backend entry point."""

import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

# load environment variables like PG_USER and PG_PASSWORD
load_dotenv()

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.extend([PROJECT_ROOT, ROOT])

app = FastAPI(title="MCPInception API")
from backend.helpers import db_connect

def get_db_conn():
    """Return a psycopg2 connection to configured DB."""
    try:
        return db_connect()
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=500, detail=f"Database connection failed: {exc}") from exc


@app.get("/health")
async def health_check():
    """Simple health endpoint."""
    return {"status": "ok"}


@app.get("/scrape")
async def scrape(url: str = "http://127.0.0.1:8000/scrape?url=https://www.ycombinator.com/"):
    """Scrape a URL and return its title."""
    import requests  # local import to keep top tidy
    from bs4 import BeautifulSoup

    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to fetch URL")
    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    return {"title": title}


"""
cd backend &&
uv run -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

http://127.0.0.1:8000/health
http://127.0.0.1:8000/scrape?url=https://www.ycombinator.com/
"""

