#!/usr/bin/env python
"""
Example MCP client for the cryptocurrency price service
"""
import os
import json
import time
import uuid
import asyncio
import httpx
from typing import Dict, Any, List, Optional

# MCP client configuration
SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/api/v1/mcp")
SERVICE_NAME = "zkom.crypto.price.client"


async def create_mcp_request(action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create an MCP request
    
    Args:
        action: The action to perform
        parameters: The parameters for the action
        
    Returns:
        Dictionary representing an MCP request
    """
    return {
        "type": "request",
        "context": {
            "request_id": str(uuid.uuid4()),
            "timestamp": int(time.time() * 1000)
        },
        "metadata": {
            "version": "1.0",
            "service": SERVICE_NAME
        },
        "action": action,
        "parameters": parameters
    }


async def send_mcp_request(request: Dict[str, Any]) -> Dict[str, Any]:
    """
    Send an MCP request to the server
    
    Args:
        request: MCP request dictionary
        
    Returns:
        MCP response dictionary
    """
    async with httpx.AsyncClient() as client:
        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": request["context"]["request_id"]
        }
        
        print(f"Sending request to {SERVER_URL}:")
        print(json.dumps(request, indent=2))
        
        response = await client.post(
            SERVER_URL,
            headers=headers,
            json=request,
            timeout=30.0
        )
        
        response.raise_for_status()
        return response.json()


async def get_crypto_price(symbol: str, currency: str = "USD") -> Dict[str, Any]:
    """
    Get the price of a cryptocurrency
    
    Args:
        symbol: Symbol of the cryptocurrency
        currency: Base currency for the price
        
    Returns:
        MCP response with price data
    """
    request = await create_mcp_request(
        action="crypto.price.get",
        parameters={
            "symbol": symbol,
            "currency": currency
        }
    )
    
    return await send_mcp_request(request)


async def get_multiple_prices(symbols: List[str], currency: str = "USD") -> Dict[str, Any]:
    """
    Get prices for multiple cryptocurrencies
    
    Args:
        symbols: List of cryptocurrency symbols
        currency: Base currency for the prices
        
    Returns:
        MCP response with price data
    """
    request = await create_mcp_request(
        action="crypto.prices.get",
        parameters={
            "symbols": symbols,
            "currency": currency
        }
    )
    
    return await send_mcp_request(request)


async def main():
    """
    Main function
    """
    try:
        # Get price of Bitcoin in USD
        print("\n=== Getting price of BTC in USD ===")
        btc_response = await get_crypto_price("BTC", "USD")
        print("Response:")
        print(json.dumps(btc_response, indent=2))
        
        # Get price of Ethereum in EUR
        print("\n=== Getting price of ETH in EUR ===")
        eth_response = await get_crypto_price("ETH", "EUR")
        print("Response:")
        print(json.dumps(eth_response, indent=2))
        
        # Get prices of multiple cryptocurrencies
        print("\n=== Getting prices of multiple cryptocurrencies ===")
        multi_response = await get_multiple_prices(["BTC", "ETH", "SOL", "DOGE"], "USD")
        print("Response:")
        print(json.dumps(multi_response, indent=2))
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main()) 