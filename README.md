# ZKOM MCP Server for Cryptocurrency Prices

A Model Context Protocol (MCP) server implementation for retrieving cryptocurrency prices from Coinbase.

## Features

- Get real-time exchange rates for cryptocurrencies
- MCP-compliant API responses
- Support for querying prices in various currencies
- Caching mechanism to reduce API calls

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/zkom_mcp_server.git
cd zkom_mcp_server
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the server:
```bash
python -m app.main
```

## Usage

Send requests to the MCP server endpoints:

```
GET /v1/crypto/price?symbol=BTC&currency=USD
```

## Environment Variables

Create a `.env` file with the following variables:
```
# Server configuration
PORT=8000
HOST=0.0.0.0

# Coinbase API configuration
COINBASE_API_URL=https://api.coinbase.com/v2/exchange-rates
```

## API Documentation

Once the server is running, access the API documentation at:

```
http://localhost:8000/docs
```

## License

MIT 