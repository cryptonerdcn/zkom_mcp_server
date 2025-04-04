#!/usr/bin/env python
"""
Cryptocurrency Price MCP Server

This server provides tools for retrieving cryptocurrency prices using the Coinbase API.
"""
from typing import Any, Dict, List, Optional
import os
import httpx
import time
import json
import logging
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("crypto_price_server")

# Initialize FastMCP server
mcp = FastMCP("crypto-price")

# Constants
COINBASE_API_URL = os.getenv("COINBASE_API_URL", "https://api.coinbase.com/v2/exchange-rates")
USER_AGENT = "crypto-price-app/1.0"
CACHE_TTL = int(os.getenv("CACHE_TTL", "60"))  # Cache time-to-live in seconds

# Cache for exchange rates
cache = {}
last_update = {}

async def fetch_exchange_rates(base_currency: str) -> Dict[str, Any]:
    """Fetch exchange rates from Coinbase API with proper caching."""
    # Check cache first
    current_time = time.time()
    if (
        base_currency in cache 
        and current_time - last_update.get(base_currency, 0) < CACHE_TTL
    ):
        logger.debug(f"Using cached exchange rates for {base_currency}")
        return cache[base_currency]
    
    # Make API request
    url = f"{COINBASE_API_URL}?currency={base_currency}"
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/json"
    }
    
    logger.info(f"Fetching exchange rates from Coinbase API: {url}")
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
            # Extract rates from response
            rates = data.get("data", {}).get("rates", {})
            
            # Update cache
            cache[base_currency] = rates
            last_update[base_currency] = current_time
            
            return rates
        except Exception as e:
            logger.error(f"Error fetching exchange rates: {e}")
            return {}

def format_price(symbol: str, price: float, base_currency: str) -> str:
    """Format a cryptocurrency price into a readable string."""
    return f"{symbol}: {price} {base_currency}"

@mcp.tool()
async def get_crypto_price(symbol: str, currency: str = "USD") -> str:
    """Get the current price of a cryptocurrency.
    
    Args:
        symbol: Symbol of the cryptocurrency (e.g., BTC, ETH, SOL)
        currency: Base currency for the price (e.g., USD, EUR)
    """
    try:
        # For Coinbase, we need to get the rates in terms of the crypto
        base_rates = await fetch_exchange_rates(symbol)
        
        if not base_rates or currency not in base_rates:
            return f"Unable to fetch price for {symbol} in {currency}."
            
        # The rate is how many currency units you get for 1 unit of symbol
        rate = float(base_rates[currency])
        
        # Calculate the price (inverse of the rate)
        price = 1.0 / rate if rate != 0 else 0
        
        return f"""
Current price for {symbol}:
{price:.2f} {currency}

Data source: Coinbase Exchange Rates API
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
"""
    except Exception as e:
        logger.error(f"Error getting price for {symbol}/{currency}: {e}")
        return f"Error retrieving price: {str(e)}"

@mcp.tool()
async def get_multiple_prices(symbols: str, currency: str = "USD") -> str:
    """Get prices for multiple cryptocurrencies.
    
    Args:
        symbols: Comma-separated list of cryptocurrency symbols (e.g., "BTC,ETH,SOL")
        currency: Base currency for the prices (e.g., USD, EUR)
    """
    symbols_list = [s.strip().upper() for s in symbols.split(",")]
    results = []
    
    for symbol in symbols_list:
        try:
            # Get rates for this symbol
            base_rates = await fetch_exchange_rates(symbol)
            
            if not base_rates or currency not in base_rates:
                results.append(f"{symbol}: Unable to fetch price in {currency}")
                continue
                
            # Calculate price
            rate = float(base_rates[currency])
            price = 1.0 / rate if rate != 0 else 0
            
            results.append(f"{symbol}: {price:.2f} {currency}")
        except Exception as e:
            logger.error(f"Error getting price for {symbol}/{currency}: {e}")
            results.append(f"{symbol}: Error - {str(e)}")
    
    if not results:
        return "No prices could be retrieved."
        
    return f"""
Cryptocurrency Prices:
{chr(10).join(results)}

Data source: Coinbase Exchange Rates API
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
"""

@mcp.tool()
async def compare_prices(symbols: str, currency: str = "USD", days_ago: int = 0) -> str:
    """Compare prices of cryptocurrencies against each other.
    
    Args:
        symbols: Comma-separated list of cryptocurrency symbols (e.g., "BTC,ETH,SOL")
        currency: Base currency for the comparison (e.g., USD, EUR)
        days_ago: How many days to look back (0 = current prices only)
    """
    # Note: This implementation only shows current prices
    # A full implementation would include historical data
    
    symbols_list = [s.strip().upper() for s in symbols.split(",")]
    results = []
    prices = {}
    
    # Get prices for all symbols
    for symbol in symbols_list:
        try:
            base_rates = await fetch_exchange_rates(symbol)
            
            if not base_rates or currency not in base_rates:
                results.append(f"{symbol}: Unable to fetch price in {currency}")
                continue
                
            rate = float(base_rates[currency])
            price = 1.0 / rate if rate != 0 else 0
            prices[symbol] = price
            results.append(f"{symbol}: {price:.2f} {currency}")
        except Exception as e:
            logger.error(f"Error getting price for {symbol}/{currency}: {e}")
            results.append(f"{symbol}: Error - {str(e)}")
    
    if len(prices) < 2:
        return "Not enough valid prices to compare.\n\n" + "\n".join(results)
        
    # Generate comparisons
    comparisons = []
    symbols_with_prices = list(prices.keys())
    
    for i in range(len(symbols_with_prices)):
        for j in range(i+1, len(symbols_with_prices)):
            sym1 = symbols_with_prices[i]
            sym2 = symbols_with_prices[j]
            ratio = prices[sym1] / prices[sym2] if prices[sym2] != 0 else 0
            comparisons.append(f"1 {sym1} = {ratio:.6f} {sym2}")
            comparisons.append(f"1 {sym2} = {1/ratio:.6f} {sym1}" if ratio != 0 else f"1 {sym2} = ∞ {sym1}")
    
    return f"""
Current Prices:
{chr(10).join(results)}

Price Comparisons:
{chr(10).join(comparisons)}

Data source: Coinbase Exchange Rates API
Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime())}
"""

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio') 