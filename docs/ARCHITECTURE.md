# Architecture

## Overview

```
Kiro CLI / MCP Client
        │
        ▼ (stdio or HTTP)
┌─────────────────────┐
│  hcso-roma-mcp      │
│  (MCP Server)       │
│                     │
│  tools.py → client  │
└────────┬────────────┘
         │
         ▼ (HTTPS + AK/SK signing)
┌─────────────────────┐
│  Roma Connect API   │
│  (HCSO Dataprev)    │
└─────────────────────┘
```

## Components

- **server.py**: MCP server setup, transport selection (stdio/HTTP)
- **tools.py**: Tool definitions, formatting responses
- **client.py**: SDK wrapper, auth, API calls

## Auth Flow

1. User provides AK/SK/SecurityToken via env vars
2. Client builds `BasicCredentials` with IAM endpoint
3. SDK handles signing (AK/SK HMAC) per request
4. STS tokens expire — user must refresh externally
