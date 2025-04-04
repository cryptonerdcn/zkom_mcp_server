#!/usr/bin/env python
"""
Claude Desktop MCP Adapter for Cryptocurrency Price Service

This adapter allows Claude Desktop to connect to the ZKOM MCP Server
to retrieve cryptocurrency price information.
"""
import os
import json
import time
import uuid
import asyncio
import httpx
import logging
from typing import Dict, Any, List, Optional, Union

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("claude_mcp_adapter")

# MCP configuration
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8000/api/v1/mcp")
SERVICE_NAME = "claude.desktop.client"
DEFAULT_TIMEOUT = 30.0  # seconds


class ClaudeMCPAdapter:
    """Adapter for Claude Desktop to communicate with MCP Services"""
    
    def __init__(self, server_url: Optional[str] = None):
        """
        Initialize the adapter
        
        Args:
            server_url: Optional URL of the MCP server, defaults to MCP_SERVER_URL
        """
        self.server_url = server_url or MCP_SERVER_URL
        self.session = None
        logger.info(f"Initialized MCP adapter for server: {self.server_url}")
    
    def _create_context(self) -> Dict[str, Any]:
        """Create a context object for MCP requests"""
        return {
            "request_id": str(uuid.uuid4()),
            "timestamp": int(time.time() * 1000)
        }
    
    def _create_metadata(self) -> Dict[str, Any]:
        """Create metadata for MCP requests"""
        return {
            "version": "1.0",
            "service": SERVICE_NAME
        }
    
    def create_mcp_request(self, action: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create an MCP request message
        
        Args:
            action: The action to perform
            parameters: Parameters for the action
            
        Returns:
            Dictionary representing the MCP request
        """
        return {
            "type": "request",
            "context": self._create_context(),
            "metadata": self._create_metadata(),
            "action": action,
            "parameters": parameters
        }
    
    async def connect(self):
        """Initialize connection to the MCP server"""
        self.session = httpx.AsyncClient(timeout=DEFAULT_TIMEOUT)
        logger.info("Connected to MCP server")
    
    async def disconnect(self):
        """Close connection to the MCP server"""
        if self.session:
            await self.session.aclose()
            self.session = None
        logger.info("Disconnected from MCP server")
    
    async def send_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send an MCP request to the server
        
        Args:
            request: MCP request message
            
        Returns:
            MCP response message
        """
        if not self.session:
            await self.connect()
            
        headers = {
            "Content-Type": "application/json",
            "X-Request-ID": request["context"]["request_id"]
        }
        
        logger.debug(f"Sending request to {self.server_url}:\n{json.dumps(request, indent=2)}")
        
        try:
            response = await self.session.post(
                self.server_url,
                headers=headers,
                json=request
            )
            response.raise_for_status()
            return response.json()
            
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} - {e.response.text}")
            return {
                "type": "error",
                "context": request["context"],
                "metadata": request["metadata"],
                "error": {
                    "code": e.response.status_code,
                    "message": f"HTTP error: {e.response.reason_phrase}",
                    "details": {
                        "response": e.response.text
                    }
                }
            }
        except Exception as e:
            logger.error(f"Error sending request: {str(e)}")
            return {
                "type": "error",
                "context": request["context"],
                "metadata": request["metadata"],
                "error": {
                    "code": 1002,  # SERVICE_UNAVAILABLE
                    "message": f"Error sending request: {str(e)}"
                }
            }
    
    async def get_crypto_price(self, symbol: str, currency: str = "USD") -> Dict[str, Any]:
        """
        Get the price of a cryptocurrency
        
        Args:
            symbol: Symbol of the cryptocurrency (e.g., BTC)
            currency: Base currency for the price (e.g., USD)
            
        Returns:
            Price information
        """
        request = self.create_mcp_request(
            action="crypto.price.get",
            parameters={
                "symbol": symbol,
                "currency": currency
            }
        )
        
        response = await self.send_request(request)
        return response
    
    async def get_multiple_prices(
        self, symbols: List[str], currency: str = "USD"
    ) -> Dict[str, Any]:
        """
        Get prices for multiple cryptocurrencies
        
        Args:
            symbols: List of cryptocurrency symbols
            currency: Base currency for the prices
            
        Returns:
            Price information for multiple cryptocurrencies
        """
        request = self.create_mcp_request(
            action="crypto.prices.get",
            parameters={
                "symbols": symbols,
                "currency": currency
            }
        )
        
        response = await self.send_request(request)
        return response
    
    def extract_price_data(self, response: Dict[str, Any]) -> Union[Dict[str, Any], List[Dict[str, Any]], None]:
        """
        Extract price data from MCP response
        
        Args:
            response: MCP response message
            
        Returns:
            Price data or None if error
        """
        if response.get("type") == "error":
            logger.error(f"Error response: {response.get('error', {}).get('message')}")
            return None
            
        return response.get("data")


# Singleton instance
claude_mcp_adapter = ClaudeMCPAdapter()


async def main():
    """
    Main function for testing the adapter
    """
    try:
        adapter = ClaudeMCPAdapter()
        
        # Get price of Bitcoin in USD
        print("\n=== Getting price of BTC in USD ===")
        btc_response = await adapter.get_crypto_price("BTC", "USD")
        price_data = adapter.extract_price_data(btc_response)
        print(f"BTC price: {price_data.get('price') if price_data else 'Unknown'} USD")
        
        # Get prices of multiple cryptocurrencies
        print("\n=== Getting prices of multiple cryptocurrencies ===")
        multi_response = await adapter.get_multiple_prices(["BTC", "ETH", "SOL", "DOGE"], "USD")
        prices_data = adapter.extract_price_data(multi_response)
        
        if prices_data and "prices" in prices_data:
            for price in prices_data["prices"]:
                print(f"{price['symbol']} price: {price['price']} {price['base_currency']}")
        
        await adapter.disconnect()
        
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    # Run the test function
    asyncio.run(main()) 