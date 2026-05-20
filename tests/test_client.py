"""Tests for Roma Connect MCP tools."""

from unittest.mock import MagicMock, patch

import pytest

from hcso_roma_mcp.client import RomaConnectClient


class TestRomaConnectClient:
    """Test client wrapper."""

    def test_missing_credentials_raises(self):
        client = RomaConnectClient(ak="", sk="", project_id="")
        with pytest.raises(ValueError, match="Missing credentials"):
            _ = client.client

    @patch.dict("os.environ", {"HCSO_AK": "ak", "HCSO_SK": "sk", "HCSO_PROJECT_ID": "proj"})
    @patch("hcso_roma_mcp.client.RomaClient")
    def test_build_client_with_env(self, mock_roma_class):
        mock_builder = MagicMock()
        mock_roma_class.new_builder.return_value = mock_builder
        mock_builder.with_credentials.return_value = mock_builder
        mock_builder.with_endpoint.return_value = mock_builder
        mock_builder.build.return_value = MagicMock()

        client = RomaConnectClient()
        result = client.client
        assert result is not None
        mock_builder.build.assert_called_once()

    @patch.dict("os.environ", {"HCSO_AK": "ak", "HCSO_SK": "sk", "HCSO_PROJECT_ID": "proj"})
    @patch("hcso_roma_mcp.client.RomaClient")
    def test_list_datasources(self, mock_roma_class):
        mock_client = MagicMock()
        mock_builder = MagicMock()
        mock_roma_class.new_builder.return_value = mock_builder
        mock_builder.with_credentials.return_value = mock_builder
        mock_builder.with_endpoint.return_value = mock_builder
        mock_builder.build.return_value = mock_client

        mock_ds = MagicMock()
        mock_ds.datasource_name = "dev-mir"
        mock_ds.datasource_type = "PostgreSQL"
        mock_ds.id = "ds-123"
        mock_resp = MagicMock()
        mock_resp.entities = [mock_ds]
        mock_client.list_datasources.return_value = mock_resp

        client = RomaConnectClient()
        result = client.list_datasources("instance-123")
        assert len(result) == 1
        assert result[0].datasource_name == "dev-mir"

    @patch.dict("os.environ", {"HCSO_AK": "ak", "HCSO_SK": "sk", "HCSO_PROJECT_ID": "proj"})
    @patch("hcso_roma_mcp.client.RomaClient")
    def test_list_apis(self, mock_roma_class):
        mock_client = MagicMock()
        mock_builder = MagicMock()
        mock_roma_class.new_builder.return_value = mock_builder
        mock_builder.with_credentials.return_value = mock_builder
        mock_builder.with_endpoint.return_value = mock_builder
        mock_builder.build.return_value = mock_client

        mock_api = MagicMock()
        mock_api.name = "cpf-cnpj"
        mock_api.req_method = "GET"
        mock_api.req_uri = "/mir/v1/cpf-cnpj"
        mock_api.status = 1
        mock_resp = MagicMock()
        mock_resp.apis = [mock_api]
        mock_client.list_apis_v2.return_value = mock_resp

        client = RomaConnectClient()
        result = client.list_apis("instance-123")
        assert len(result) == 1
        assert result[0].name == "cpf-cnpj"

    @patch.dict("os.environ", {"HCSO_AK": "ak", "HCSO_SK": "sk", "HCSO_PROJECT_ID": "proj"})
    @patch("hcso_roma_mcp.client.RomaClient")
    def test_list_data_apis(self, mock_roma_class):
        mock_client = MagicMock()
        mock_builder = MagicMock()
        mock_roma_class.new_builder.return_value = mock_builder
        mock_builder.with_credentials.return_value = mock_builder
        mock_builder.with_endpoint.return_value = mock_builder
        mock_builder.build.return_value = mock_client

        mock_data_api = MagicMock()
        mock_data_api.name = "query-imoveis"
        mock_data_api.path = "/query-imoveis/v1"
        mock_data_api.status = 1
        mock_resp = MagicMock()
        mock_resp.apis = [mock_data_api]
        mock_client.list_live_data_api_v2.return_value = mock_resp

        client = RomaConnectClient()
        result = client.list_data_apis("instance-123")
        assert len(result) == 1
        assert result[0].name == "query-imoveis"

    @patch.dict("os.environ", {"HCSO_AK": "ak", "HCSO_SK": "sk", "HCSO_PROJECT_ID": "proj"})
    @patch("hcso_roma_mcp.client.RomaClient")
    def test_list_datasources_empty(self, mock_roma_class):
        mock_client = MagicMock()
        mock_builder = MagicMock()
        mock_roma_class.new_builder.return_value = mock_builder
        mock_builder.with_credentials.return_value = mock_builder
        mock_builder.with_endpoint.return_value = mock_builder
        mock_builder.build.return_value = mock_client

        mock_resp = MagicMock()
        mock_resp.entities = []
        mock_client.list_datasources.return_value = mock_resp

        client = RomaConnectClient()
        result = client.list_datasources("instance-123")
        assert result == []

    def test_security_token_optional(self):
        client = RomaConnectClient(ak="ak", sk="sk", project_id="proj")
        assert client.security_token == ""
