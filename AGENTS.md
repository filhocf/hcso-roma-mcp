# AGENTS.md — hcso-roma-mcp

## O que é
MCP server para administrar Roma Connect (Huawei Cloud HCSO) via SDK. Permite listar/criar datasources, APIs, Data APIs, throttling.

## Stack
- Python 3.11+, uv
- MCP SDK (mcp>=1.0.0)
- huaweicloudsdkroma 3.1.191
- pytest + pytest-asyncio + ruff

## Comandos
```bash
uv venv .venv && uv pip install -e ".[dev]"
.venv/bin/pytest tests/ -v
.venv/bin/ruff check src/ tests/
```

## Convenções
- src layout (`src/hcso_roma_mcp/`)
- Testes com mocks do SDK (não depende de VPN/credenciais)
- Tools retornam texto formatado (não JSON bruto)
- Credenciais via env vars: HCSO_AK, HCSO_SK, HCSO_SECURITY_TOKEN, HCSO_PROJECT_ID

## Transport
- stdio (padrão): `hcso-roma-mcp`
- HTTP: `MCP_TRANSPORT=streamable-http MCP_PORT=8960 hcso-roma-mcp`
