# hcso-roma-mcp

MCP server for administering Huawei Cloud HCSO Roma Connect instances.

## Features

- List datasources, APIs, and Data APIs (custom backends)
- Dual transport: stdio + StreamableHTTP
- STS token support for federated auth

## Installation

```bash
uv pip install -e .
```

## Usage

### stdio (default)
```bash
hcso-roma-mcp
```

### StreamableHTTP
```bash
MCP_TRANSPORT=streamable-http MCP_PORT=8960 hcso-roma-mcp
```

## Configuration

| Variable | Required | Description |
|----------|----------|-------------|
| `HCSO_AK` | Yes | Access Key |
| `HCSO_SK` | Yes | Secret Key |
| `HCSO_PROJECT_ID` | Yes | Project ID |
| `HCSO_SECURITY_TOKEN` | No | STS token (for federated auth) |
| `HCSO_IAM_ENDPOINT` | No | IAM endpoint (default: Dataprev HCSO) |
| `HCSO_ROMA_ENDPOINT` | No | Roma endpoint (default: Dataprev HCSO) |

## License

Apache 2.0
