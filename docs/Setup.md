```json
{
  "mcpServers": {
    "crypto-price": {
      "command": "uv",
      "args": [
          "--directory",
          "/path/to/zkom_mcp_server",
          "run",
          "crypto_price_server.py"
      ]
    }
  }
}
```

```json
{
  "name": "compare_prices",
  "description": "Compare prices of cryptocurrencies against each other.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbols": {
        "type": "string",
        "description": "Comma-separated list of cryptocurrency symbols (e.g., \"BTC,ETH,SOL\")"
      },
      "currency": {
        "type": "string",
        "description": "Base currency for the comparison (e.g., USD, EUR)",
        "default": "USD"
      },
      "days_ago": {
        "type": "integer",
        "description": "How many days to look back (0 = current prices only)",
        "default": 0
      }
    },
    "required": ["symbols"]
  }
}
```

```json
{
  "name": "get_multiple_prices",
  "description": "Get prices for multiple cryptocurrencies.",
  "inputSchema": {
    "type": "object",
    "properties": {
      "symbols": {
        "type": "string",
        "description": "Comma-separated list of cryptocurrency symbols (e.g., \"BTC,ETH,SOL\")"
      },
      "currency": {
        "type": "string",
        "description": "Base currency for the prices (e.g., USD, EUR)",
        "default": "USD"
      }
    },
    "required": ["symbols"]
  }
}
```