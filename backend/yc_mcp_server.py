"""MCP server exposing YC batch company data using FastMCP.

Run with:

    uv run yc_mcp_server.py

Then connect from a compatible MCP client, e.g.:

    mcp-use --read mcp://yc/summer-2015.json --server "uv run yc_mcp_server.py"  # noqa: E501
"""

from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP

from helpers import get_yc_batch_companies


# ---------------------------------------------------------------------------
# FastMCP setup
# ---------------------------------------------------------------------------
mcp = FastMCP("YC Companies Server", version="0.1.0")


@mcp.resource("mcp://yc/{batch}.json", mime_type="application/json")
async def yc_batch_json(batch: str) -> str:  # noqa: D401
    """Return the list of YC companies for the given *batch*.

    The *batch* slug comes from the URI template and will look like
    "summer-2015" or "winter-2012".
    """

    human_readable = batch.replace("-", " ").title()  # e.g. Summer 2015
    companies = get_yc_batch_companies(human_readable)
    return json.dumps(companies, ensure_ascii=False, indent=2)


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    # The default transport "stdio" is what most MCP clients expect.
    mcp.run(transport="stdio")
