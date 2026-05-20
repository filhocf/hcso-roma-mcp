"""MCP server for Roma Connect administration."""

import logging
import os

from mcp.server.fastmcp import FastMCP

from .tools import register_tools

logger = logging.getLogger(__name__)

mcp = FastMCP("hcso-roma-mcp")
register_tools(mcp)


def main():
    """Entry point — select transport based on env."""
    logging.basicConfig(level=logging.INFO)

    transport = os.environ.get("MCP_TRANSPORT", "stdio")

    if transport == "streamable-http":
        host = os.environ.get("MCP_HOST", "127.0.0.1")
        port = int(os.environ.get("MCP_PORT", "8960"))
        mcp.settings.host = host
        mcp.settings.port = port
        mcp.run(transport="streamable-http")
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
