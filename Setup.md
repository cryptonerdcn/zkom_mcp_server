```json
{
  "mcpServers": {
    "crypto-price": {
      "command": "python",
      "args": ["crypto_price_server.py"],
      "cwd": "/absolute/path/to/your/project/folder",
      "env": {
        "COINBASE_API_URL": "https://api.coinbase.com/v2/exchange-rates",
        "CACHE_TTL": "60"
      }
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