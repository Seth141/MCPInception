#!/usr/bin/env python3

"""
uv run backend/template.py <url>
"""

import os
import sys
from dotenv import load_dotenv
import argparse
import psycopg2
from bs4 import BeautifulSoup
import requests
from pydantic import BaseModel

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append(PROJECT_ROOT)
sys.path.append(ROOT)
# load environment variables like PG_USER and PG_PASSWORD
load_dotenv()


def print_roots():
    """ just for debug """
    print(f'{PROJECT_ROOT=}')
    print(f'{ROOT=}')


def parse_args() -> argparse.Namespace:
    """
    take the url to scrape a site
    """
    parser = argparse.ArgumentParser(description="Take the site url as argument.")
    parser.add_argument("url", metavar="N", type=str, nargs=1)
    return parser.parse_args()


def db_create(DB_NAME: str = os.getenv("DB_NAME", "mcp")) -> None:
    """
    create the database if it doesn't exist already
    """
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database=DB_NAME,
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}")
        conn.commit()
        conn.close()
    except Exception as e:
        raise Exception(f"Failed to create database: {e}")


def db_connect(
    db_name: str = os.getenv("DB_NAME", "mcp")
) -> psycopg2.extensions.connection | None:
    """
    postgres db connection
    create the db if it doesn't exist already, and connect to it
    otherwise connect to the existing db right away
    """
    # brew services start postgresql
    # psql -U ${whoami} -d postgres
    # psql -U sudo -d postgres
    # CREATE DATABASE mcp;

    # check if database exists
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
        cursor = conn.cursor()
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        conn.close()

    except Exception as e:
        raise Exception(f"Failed to check database existence: {e}")

    if exists:
        # connect to existing db
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database=db_name,
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD"),
        )
    else:
        # create db and connect
        db_create(db_name)
        conn = db_connect(db_name)

    return conn


def fetch_url(url: str) -> BeautifulSoup:
    """
    fetch the url and return the soup object
    """
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def parse_url(url: str) -> None:
    """
    parse the url and print the soup object
    """
    soup = fetch_url(url)
    print(soup.prettify())


YC_API_BASE = "https://yc-oss.github.io/api/companies"

# map of supported categories to endpoint filenames
YC_CATEGORIES: dict[str, str] = {
    "all": "all.json",
    "top": "top.json",
    "hiring": "hiring.json",
    "nonprofit": "nonprofit.json",
}


def get_yc_companies(
    category: str = "all",
) -> list[dict]:
    """Return YC companies list for the requested *category*.

    Categories supported (case-insensitive):
        • all – all launched companies (default)
        • top – YC "Top Companies" list
        • hiring – companies currently hiring
        • nonprofit – non-profit companies
    """

    key = category.lower()
    endpoint = YC_CATEGORIES.get(key)
    if endpoint is None:
        raise ValueError(
            f"Unsupported category '{category}'. Allowed: {', '.join(YC_CATEGORIES)}"
        )

    url = f"{YC_API_BASE}/{endpoint}"
    response = requests.get(url, timeout=15)
    response.raise_for_status()
    return response.json()


# ---------------------------------------------------------------------------
# Pydantic model & DB helpers
# ---------------------------------------------------------------------------

class YCCompany(BaseModel):
    """Subset of YC company fields stored in DB."""

    id: int
    name: str
    slug: str | None = None
    website: str | None = None
    all_locations: str | None = None
    one_liner: str | None = None
    industry: str | None = None
    subindustry: str | None = None
    batch: str | None = None
    stage: str | None = None
    isHiring: bool | None = None
    nonprofit: bool | None = None

    class Config:
        extra = "allow"

    @property
    def classification(self) -> list[str]:
        """Return simple tags based on hiring/nonprofit/top."""
        tags: list[str] = []
        if self.isHiring:
            tags.append("hiring")
        if self.nonprofit:
            tags.append("nonprofit")
        return tags


def ensure_companies_table(conn: psycopg2.extensions.connection) -> None:
    """Create companies table if it doesn't exist."""

    with conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS yc_companies (
                id INTEGER PRIMARY KEY,
                name TEXT,
                slug TEXT,
                website TEXT,
                locations TEXT,
                one_liner TEXT,
                industry TEXT,
                subindustry TEXT,
                batch TEXT,
                stage TEXT,
                is_hiring BOOLEAN,
                nonprofit BOOLEAN,
                classification TEXT[]
            );
            """
        )
        conn.commit()


def upsert_company(conn: psycopg2.extensions.connection, company: YCCompany) -> None:
    """Insert or update a YCCompany row."""

    ensure_companies_table(conn)
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO yc_companies (
                id, name, slug, website, locations, one_liner,
                industry, subindustry, batch, stage,
                is_hiring, nonprofit, classification
            ) VALUES (
                %(id)s, %(name)s, %(slug)s, %(website)s, %(all_locations)s, %(one_liner)s,
                %(industry)s, %(subindustry)s, %(batch)s, %(stage)s,
                %(isHiring)s, %(nonprofit)s, %(classification)s
            )
            ON CONFLICT (id) DO UPDATE SET
                name = EXCLUDED.name,
                slug = EXCLUDED.slug,
                website = EXCLUDED.website,
                locations = EXCLUDED.locations,
                one_liner = EXCLUDED.one_liner,
                industry = EXCLUDED.industry,
                subindustry = EXCLUDED.subindustry,
                batch = EXCLUDED.batch,
                stage = EXCLUDED.stage,
                is_hiring = EXCLUDED.is_hiring,
                nonprofit = EXCLUDED.nonprofit,
                classification = EXCLUDED.classification;
            """,
            {
                **company.dict(),
                "classification": company.classification,
            },
        )
        conn.commit()


def save_companies_to_db(
    conn: psycopg2.extensions.connection,
    companies: list[dict],
) -> int:
    """Persist list of raw dict companies to DB, return count."""

    count = 0
    for item in companies:
        try:
            model = YCCompany(**item)
            upsert_company(conn, model)
            count += 1
        except Exception as exc:  # pylint: disable=broad-except
            print(f"Failed to store id={item.get('id')}: {exc}")
    return count


# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------

def get_companies(
    conn: psycopg2.extensions.connection,
    limit: int = 100,
) -> list[dict]:
    """Return up to *limit* companies currently stored in DB."""

    ensure_companies_table(conn)
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM yc_companies ORDER BY id LIMIT %s;", (limit,))
        cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, row)) for row in cur.fetchall()]


# ---------------------------------------------------------------------------
# Convenience CLI printing
# ---------------------------------------------------------------------------

def print_companies(limit: int = 20):
    """Print *limit* companies from DB to stdout."""

    conn = db_connect()
    if conn is None:
        print("DB connection failed")
        return
    rows = get_companies(conn, limit)
    conn.close()

    for row in rows:
        print(f"[{row['id']}] {row['name']} | {row['batch']} | {row['industry']}")


if __name__ == "__main__":

    import sys as _sys

    if len(_sys.argv) > 1 and _sys.argv[1] == "list":
        lim = int(_sys.argv[2]) if len(_sys.argv) > 2 else 20
        print_companies(lim)
        _sys.exit(0)

    args = parse_args()
    url = args.url[0]

    # conn = db_connect()
    conn = db_connect("mcp")
    if conn is None:
        raise Exception("Database connection failed.")

    parse_url(url)

    conn.close()
    print("Database connection closed.")



"""
# terminal 1
cd backend && uv run -m uvicorn main:app --reload

# terminal 2
cd backend && uv run helpers.py list 30
"""
