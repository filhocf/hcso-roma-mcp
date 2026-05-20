"""MCP tool definitions for Roma Connect administration."""

from mcp.server.fastmcp import FastMCP

from .client import RomaConnectClient

_client: RomaConnectClient | None = None


def get_client() -> RomaConnectClient:
    global _client
    if _client is None:
        _client = RomaConnectClient()
    return _client


def register_tools(mcp: FastMCP) -> None:
    """Register all Roma Connect tools on the MCP server."""

    @mcp.tool()
    async def list_datasources(instance_id: str) -> str:
        """List datasources configured in a Roma Connect instance.

        Args:
            instance_id: Roma instance UUID (e.g. c1f54b28-1203-4b43-af21-dd276e0b39da)
        """
        client = get_client()
        datasources = client.list_datasources(instance_id)
        if not datasources:
            return "No datasources found."
        lines = []
        for ds in datasources:
            name = getattr(ds, "datasource_name", None) or getattr(ds, "name", "?")
            ds_type = getattr(ds, "datasource_type", "?")
            ds_id = getattr(ds, "id", "?")
            lines.append(f"- {name} (type={ds_type}, id={ds_id})")
        return f"Datasources ({len(lines)}):\n" + "\n".join(lines)

    @mcp.tool()
    async def list_apis(instance_id: str) -> str:
        """List published APIs in a Roma Connect instance.

        Args:
            instance_id: Roma instance UUID
        """
        client = get_client()
        apis = client.list_apis(instance_id)
        if not apis:
            return "No APIs found."
        lines = []
        for api in apis:
            name = getattr(api, "name", "?")
            method = getattr(api, "req_method", "?")
            uri = getattr(api, "req_uri", "?")
            status = getattr(api, "status", "?")
            lines.append(f"- {name}: {method} {uri} (status={status})")
        return f"APIs ({len(lines)}):\n" + "\n".join(lines)

    @mcp.tool()
    async def list_data_apis(instance_id: str) -> str:
        """List Data APIs (custom backends with SQL) in a Roma Connect instance.

        Args:
            instance_id: Roma instance UUID
        """
        client = get_client()
        data_apis = client.list_data_apis(instance_id)
        if not data_apis:
            return "No Data APIs found."
        lines = []
        for api in data_apis:
            name = getattr(api, "name", "?")
            path = getattr(api, "path", "?")
            status = getattr(api, "status", "?")
            lines.append(f"- {name}: {path} (status={status})")
        return f"Data APIs ({len(lines)}):\n" + "\n".join(lines)
