"""Tests for MCP tool functions."""

from unittest.mock import MagicMock, patch

import pytest
from mcp.server.fastmcp import FastMCP

from hcso_roma_mcp.tools import register_tools


class TestToolRegistration:
    """Test that tools register correctly."""

    def test_register_tools_no_error(self):
        mcp = FastMCP("test")
        register_tools(mcp)

    def test_tools_registered(self):
        mcp = FastMCP("test")
        register_tools(mcp)
        tool_names = [t.name for t in mcp._tool_manager._tools.values()]
        assert "list_datasources" in tool_names
        assert "list_apis" in tool_names
        assert "list_data_apis" in tool_names


class TestListDatasourcesTool:
    """Test tool output via direct invocation."""

    @patch("hcso_roma_mcp.tools._client", None)
    @patch("hcso_roma_mcp.tools.RomaConnectClient")
    @pytest.mark.asyncio
    async def test_list_datasources_output(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_ds = MagicMock()
        mock_ds.datasource_name = "dev-mir"
        mock_ds.datasource_type = "PostgreSQL"
        mock_ds.id = "ds-001"
        mock_client.list_datasources.return_value = [mock_ds]

        # Import after patching
        from hcso_roma_mcp import tools
        tools._client = None

        mcp = FastMCP("test")
        register_tools(mcp)

        # Call tool directly
        result = await mcp.call_tool("list_datasources", {"instance_id": "inst-123"})
        assert "dev-mir" in str(result)
        assert "PostgreSQL" in str(result)

    @patch("hcso_roma_mcp.tools._client", None)
    @patch("hcso_roma_mcp.tools.RomaConnectClient")
    @pytest.mark.asyncio
    async def test_list_datasources_empty(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client
        mock_client.list_datasources.return_value = []

        from hcso_roma_mcp import tools
        tools._client = None

        mcp = FastMCP("test")
        register_tools(mcp)

        result = await mcp.call_tool("list_datasources", {"instance_id": "inst-123"})
        assert "No datasources found" in str(result)

    @patch("hcso_roma_mcp.tools._client", None)
    @patch("hcso_roma_mcp.tools.RomaConnectClient")
    @pytest.mark.asyncio
    async def test_list_apis_output(self, mock_client_class):
        mock_client = MagicMock()
        mock_client_class.return_value = mock_client

        mock_api = MagicMock()
        mock_api.name = "cpf-cnpj"
        mock_api.req_method = "GET"
        mock_api.req_uri = "/mir/v1/cpf-cnpj"
        mock_api.status = 1
        mock_client.list_apis.return_value = [mock_api]

        from hcso_roma_mcp import tools
        tools._client = None

        mcp = FastMCP("test")
        register_tools(mcp)

        result = await mcp.call_tool("list_apis", {"instance_id": "inst-123"})
        assert "cpf-cnpj" in str(result)
        assert "GET" in str(result)
