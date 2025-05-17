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
from backend.helpers import (
    db_connect,
    get_yc_companies,
    save_companies_to_db,
    get_companies,
)

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


@app.get("/yc")
async def yc_companies(
    category: str = "all",
    persist: bool = False,
):
    """Return YC companies list by *category*.

    If `persist=true`, rows are validated via Pydantic and upserted into the
    `yc_companies` Postgres table.
    """

    try:
        data = get_yc_companies(category)

        saved = None
        if persist:
            conn = get_db_conn()
            saved = save_companies_to_db(conn, data)
            conn.close()

        return {
            "category": category,
            "count": len(data),
            **({"saved": saved} if saved is not None else {}),
            "companies": data,
        }
    except ValueError as err:
        raise HTTPException(status_code=400, detail=str(err))
    except Exception as exc:  # pylint: disable=broad-except
        raise HTTPException(status_code=500, detail=f"Failed to fetch YC data: {exc}")


# ---------------------------------------------------------------------------
# DB inspect endpoint
# ---------------------------------------------------------------------------

@app.get("/yc/db")
async def yc_db(limit: int = 100):
    """Return *limit* YC company rows from the database."""

    conn = get_db_conn()
    rows = get_companies(conn, limit)
    conn.close()
    return {"count": len(rows), "companies": rows}


"""
cd backend &&
uv run -m uvicorn main:app --reload --host 0.0.0.0 --port 8000

http://127.0.0.1:8000/health
http://127.0.0.1:8000/scrape?url=https://www.ycombinator.com/


uv run -m uvicorn main:app --reload
# then
curl 'http://127.0.0.1:8000/yc?category=top' | jq '.count'


curl 'http://127.0.0.1:8000/yc?category=top' | jq '.count'
curl 'http://127.0.0.1:8000/yc?category=hiring&persist=true' | jq '.saved'
"""
