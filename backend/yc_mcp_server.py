#!/usr/bin/env python3
"""YC batch list MCP server (stdio transport).

Expose each YC batch as an MCP *resource* whose URI matches
`mcp://yc/{batch}.json` (e.g. `mcp://yc/summer-2015.json`).

Run:
    uv -q run yc_mcp_server.py

Add to Claude/Windsurf config:
{
  "mcpServers": {
    "yc": {
      "command": "uv",
      "args": [
        "-q",                    # silence uv banner → keeps stdout clean
        "--directory", "/Users/sudo/CodeProjects/YC/MCPInception/backend",
        "run", "yc_mcp_server.py"
      ]
    }
  }
}

Dependencies:
  pip install "mcp[cli]" (>=1.8)  # or: uv add "mcp[cli]"

The helper `get_yc_batch_companies()` must return a JSON‑serialisable
Python object (dict/list) given a batch name like "Summer 2015".
"""

from __future__ import annotations

import logging
import os
import sys
from typing import Any
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP  # High‑level SDK interface

from helpers import get_yc_batch_companies  # your existing helper

# Load environment variables from .env file
load_dotenv()

# Get Claude API key from environment variables
CLAUDE_API_KEY = os.getenv("CLAUDE_API_KEY")
if not CLAUDE_API_KEY:
    print("Error: CLAUDE_API_KEY not found in environment variables", file=sys.stderr)
    sys.exit(1)

# ── configure logging to *stderr* so stdout remains protocol‑clean ───────────
logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    stream=sys.stderr,
)

# Configure the MCP server
mcp = FastMCP(
    "YC Companies Server",
    version="1.0.0",
    # Pass Claude API key to the server
    auth_token=CLAUDE_API_KEY
)

# Define available YC batches
AVAILABLE_BATCHES = [
    # Early batches
    "summer-2005",
    "winter-2006",
    "summer-2006",
    "winter-2007",
    "summer-2007",
    "winter-2008",
    "summer-2008",
    "winter-2009",
    "summer-2009",
    "winter-2010",
    "summer-2010",
    "winter-2011",
    "summer-2011",
    "winter-2012",
    "spring-2012",
    "summer-2012",
    "winter-2013",
    "summer-2013",
    "winter-2014",
    "summer-2014",
    "winter-2015",
    "summer-2015",
    "winter-2016",
    "summer-2016",
    "winter-2017",
    "summer-2017",
    "winter-2018",
    "summer-2018",
    "winter-2019",
    "summer-2019",
    "winter-2020",
    "summer-2020",
    "winter-2021",
    "summer-2021",
    "winter-2022",
    "summer-2022",
    "winter-2023",
    "summer-2023",
    "winter-2024",
    "summer-2024",
    "winter-2025",
    "summer-2025"
]

@mcp.tool()
def yc_batch(batch: str) -> list[dict[str, Any]]:
    """Return company list for a YC batch."""
    return get_yc_batch_companies(batch)

@mcp.tool()
def yc_all_batches() -> dict[str, list[dict[str, Any]]]:
    """Return company lists for all available YC batches."""
    all_batches = {}
    for batch_slug in AVAILABLE_BATCHES:
        try:
            human_name = batch_slug.replace("-", " ").title()
            logging.info(f"Fetching YC batch → {human_name}")
            companies = get_yc_batch_companies(human_name)
            all_batches[batch_slug] = companies
            logging.info(f"Successfully retrieved {len(companies)} companies for {human_name}")
        except Exception as e:
            logging.error(f"Error retrieving companies for {human_name}: {str(e)}")
            all_batches[batch_slug] = []
    return all_batches

@mcp.resource("mcp://yc/{batch}.json", mime_type="application/json")
def yc_batch_json(batch: str) -> list[dict[str, Any]]:
    """Return company list for a YC batch.

    Args:
        batch: slug like ``summer-2015`` or ``winter-2016`` (case‑insensitive).
    Returns:
        A JSON‑serialisable Python object (FastMCP will handle encoding).
    """
    human_name = batch.replace("-", " ").title()  # "summer-2015" → "Summer 2015"
    logging.info("Fetching YC batch → %s", human_name)

    try:
        companies = get_yc_batch_companies(human_name)
        logging.info(f"Successfully retrieved {len(companies)} companies for {human_name}")
        return companies
    except Exception as e:
        logging.error(f"Error retrieving companies for {human_name}: {str(e)}")
        # Return empty list in case of error
        return []


if __name__ == "__main__":
    # Claude/Windsurf uses stdio by default — keep it.
    mcp.run(transport="stdio")
