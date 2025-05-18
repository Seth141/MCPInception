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

@mcp.tool()
def yc_companies_by_industry(industry: str) -> list[dict[str, Any]]:
    """Return all YC companies in a specific industry/sector.
    
    Args:
        industry: Industry/sector to filter by (e.g., "B2B", "Consumer", "Fintech")
    """
    logging.info(f"Searching for companies in industry: {industry}")
    matching_companies = []
    
    # Search through all batches
    for batch_slug in AVAILABLE_BATCHES:
        try:
            human_name = batch_slug.replace("-", " ").title()
            companies = get_yc_batch_companies(human_name)
            
            # Filter companies by industry
            for company in companies:
                # Check both the main industry field and the industries list
                main_industry = company.get("industry", "")
                industries_list = company.get("industries", [])
                
                if (industry.lower() in main_industry.lower() or 
                    any(industry.lower() in ind.lower() for ind in industries_list)):
                    matching_companies.append(company)
        except Exception as e:
            logging.error(f"Error processing batch {human_name}: {str(e)}")
    
    logging.info(f"Found {len(matching_companies)} companies in industry: {industry}")
    return matching_companies

@mcp.tool()
def yc_companies_by_status(status: str) -> list[dict[str, Any]]:
    """Return all YC companies with a specific status.
    
    Args:
        status: Company status to filter by (e.g., "Active", "Acquired", "Inactive")
    """
    logging.info(f"Searching for companies with status: {status}")
    matching_companies = []
    
    for batch_slug in AVAILABLE_BATCHES:
        try:
            human_name = batch_slug.replace("-", " ").title()
            companies = get_yc_batch_companies(human_name)
            
            # Filter companies by status
            for company in companies:
                company_status = company.get("status", "")
                if status.lower() in company_status.lower():
                    matching_companies.append(company)
        except Exception as e:
            logging.error(f"Error processing batch {human_name}: {str(e)}")
    
    logging.info(f"Found {len(matching_companies)} companies with status: {status}")
    return matching_companies

@mcp.tool()
def yc_companies_by_region(region: str) -> list[dict[str, Any]]:
    """Return all YC companies in a specific region.
    
    Args:
        region: Region to filter by (e.g., "United States", "Europe", "Asia")
    """
    logging.info(f"Searching for companies in region: {region}")
    matching_companies = []
    
    for batch_slug in AVAILABLE_BATCHES:
        try:
            human_name = batch_slug.replace("-", " ").title()
            companies = get_yc_batch_companies(human_name)
            
            # Filter companies by region
            for company in companies:
                regions_list = company.get("regions", [])
                if any(region.lower() in reg.lower() for reg in regions_list):
                    matching_companies.append(company)
        except Exception as e:
            logging.error(f"Error processing batch {human_name}: {str(e)}")
    
    logging.info(f"Found {len(matching_companies)} companies in region: {region}")
    return matching_companies

@mcp.tool()
def yc_search_companies(query: str) -> list[dict[str, Any]]:
    """Search for YC companies by name, description, or tags.
    
    Args:
        query: Search term to look for in company name, description, or tags
    """
    logging.info(f"Searching for companies matching query: {query}")
    matching_companies = []
    
    for batch_slug in AVAILABLE_BATCHES:
        try:
            human_name = batch_slug.replace("-", " ").title()
            companies = get_yc_batch_companies(human_name)
            
            # Search companies by name, description, or tags
            for company in companies:
                name = company.get("name", "")
                one_liner = company.get("one_liner", "")
                description = company.get("long_description", "")
                tags = company.get("tags", [])
                
                if (query.lower() in name.lower() or
                    query.lower() in one_liner.lower() or
                    query.lower() in description.lower() or
                    any(query.lower() in tag.lower() for tag in tags)):
                    matching_companies.append(company)
        except Exception as e:
            logging.error(f"Error processing batch {human_name}: {str(e)}")
    
    logging.info(f"Found {len(matching_companies)} companies matching query: {query}")
    return matching_companies

@mcp.tool()
def yc_advanced_search(industry: str = None, status: str = None, region: str = None, 
                       query: str = None, batch: str = None, 
                       min_team_size: int = None) -> list[dict[str, Any]]:
    """Advanced search for YC companies with multiple filters.
    
    Args:
        industry: Optional industry/sector filter (e.g., "B2B", "Consumer")
        status: Optional status filter (e.g., "Active", "Acquired")
        region: Optional region filter (e.g., "United States", "Europe")
        query: Optional text search in name, description, or tags
        batch: Optional batch filter (e.g., "Summer 2015")
        min_team_size: Optional minimum team size filter
    """
    logging.info(f"Advanced search with filters: industry={industry}, status={status}, "
                f"region={region}, query={query}, batch={batch}, min_team_size={min_team_size}")
    
    all_companies = []
    batch_slugs = []
    
    # If batch is specified, only search in that batch
    if batch:
        batch_slug = batch.lower().replace(" ", "-")
        if batch_slug in AVAILABLE_BATCHES:
            batch_slugs = [batch_slug]
        else:
            logging.error(f"Invalid batch: {batch}")
            return []
    else:
        batch_slugs = AVAILABLE_BATCHES
    
    # Collect all companies from relevant batches
    for batch_slug in batch_slugs:
        try:
            human_name = batch_slug.replace("-", " ").title()
            companies = get_yc_batch_companies(human_name)
            all_companies.extend(companies)
        except Exception as e:
            logging.error(f"Error processing batch {human_name}: {str(e)}")
    
    # Apply filters
    filtered_companies = all_companies
    
    # Industry filter
    if industry:
        filtered_companies = [
            company for company in filtered_companies
            if (industry.lower() in company.get("industry", "").lower() or
                any(industry.lower() in ind.lower() for ind in company.get("industries", [])))
        ]
    
    # Status filter
    if status:
        filtered_companies = [
            company for company in filtered_companies
            if status.lower() in company.get("status", "").lower()
        ]
    
    # Region filter
    if region:
        filtered_companies = [
            company for company in filtered_companies
            if any(region.lower() in reg.lower() for reg in company.get("regions", []))
        ]
    
    # Text search filter
    if query:
        filtered_companies = [
            company for company in filtered_companies
            if (query.lower() in company.get("name", "").lower() or
                query.lower() in company.get("one_liner", "").lower() or
                query.lower() in company.get("long_description", "").lower() or
                any(query.lower() in tag.lower() for tag in company.get("tags", [])))
        ]
    
    # Team size filter
    if min_team_size is not None:
        filtered_companies = [
            company for company in filtered_companies
            if company.get("team_size", 0) >= min_team_size
        ]
    
    logging.info(f"Found {len(filtered_companies)} companies matching all filters")
    return filtered_companies

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
