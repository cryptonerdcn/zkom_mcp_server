#!/usr/bin/env python
"""
Claude Desktop Plugin for Cryptocurrency Prices via MCP

This plugin connects Claude Desktop to the ZKOM MCP Server to provide
cryptocurrency price information within Claude's interface.
"""
import os
import json
import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

# Import the MCP adapter
from claude_desktop_adapter import ClaudeMCPAdapter, claude_mcp_adapter

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("claude_crypto_plugin")

# Load configuration
CONFIG_PATH = os.getenv("CLAUDE_CONFIG_PATH", "claude_desktop_config.json")


def load_config() -> Dict[str, Any]:
    """Load the configuration file"""
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading config: {e}")
        return {
            "mcp_server": {
                "url": "http://localhost:8000/api/v1/mcp"
            },
            "crypto_api": {
                "default_currency": "USD",
                "watch_list": ["BTC", "ETH"],
                "refresh_interval": 60
            }
        }


class ClaudeCryptoPlugin:
    """Plugin for Claude Desktop to display cryptocurrency prices"""
    
    def __init__(self):
        """Initialize the plugin"""
        self.config = load_config()
        
        # Initialize MCP adapter with configured URL
        server_url = self.config["mcp_server"].get("url")
        self.adapter = ClaudeMCPAdapter(server_url)
        
        # Load settings
        self.default_currency = self.config["crypto_api"].get("default_currency", "USD")
        self.watch_list = self.config["crypto_api"].get("watch_list", ["BTC", "ETH"])
        self.refresh_interval = self.config["crypto_api"].get("refresh_interval", 60)
        
        # State
        self.prices = {}
        self.last_update = None
        self.running = False
        
        logger.info(f"Initialized Claude Crypto Plugin with server: {server_url}")
    
    async def start(self):
        """Start the plugin"""
        self.running = True
        await self.update_prices()
        logger.info("Started Claude Crypto Plugin")
    
    async def stop(self):
        """Stop the plugin"""
        self.running = False
        await self.adapter.disconnect()
        logger.info("Stopped Claude Crypto Plugin")
    
    async def update_prices(self):
        """Update cryptocurrency prices"""
        try:
            response = await self.adapter.get_multiple_prices(
                self.watch_list, self.default_currency
            )
            
            price_data = self.adapter.extract_price_data(response)
            
            if price_data and "prices" in price_data:
                # Update prices dictionary
                self.prices = {
                    price["symbol"]: {
                        "price": price["price"],
                        "currency": price["base_currency"],
                        "timestamp": price["timestamp"]
                    }
                    for price in price_data["prices"]
                }
                
                self.last_update = datetime.now()
                logger.info(f"Updated prices for {len(self.prices)} cryptocurrencies")
            else:
                logger.warning("Failed to update prices: Invalid response data")
                
        except Exception as e:
            logger.error(f"Error updating prices: {e}")
    
    def format_price_message(self) -> str:
        """Format price information for display in Claude Desktop"""
        if not self.prices:
            return "No cryptocurrency price data available."
            
        lines = ["## Current Cryptocurrency Prices\n"]
        
        for symbol, data in self.prices.items():
            formatted_price = f"{data['price']:.2f}"
            lines.append(f"**{symbol}**: {formatted_price} {data['currency']}")
            
        if self.last_update:
            lines.append(f"\nLast updated: {self.last_update.strftime('%Y-%m-%d %H:%M:%S')}")
            
        return "\n".join(lines)
    
    async def get_formatted_prices(self, symbols: Optional[List[str]] = None, currency: Optional[str] = None) -> str:
        """
        Get formatted price information for specific symbols and currency
        
        Args:
            symbols: Optional list of cryptocurrency symbols
            currency: Optional currency for the prices
            
        Returns:
            Formatted price information as a string
        """
        # Use provided symbols or fallback to watch list
        symbols_to_fetch = symbols if symbols else self.watch_list
        currency_to_use = currency if currency else self.default_currency
        
        # Fetch prices for specified symbols and currency
        response = await self.adapter.get_multiple_prices(symbols_to_fetch, currency_to_use)
        price_data = self.adapter.extract_price_data(response)
        
        if not price_data or "prices" not in price_data:
            return "Unable to fetch cryptocurrency prices."
            
        lines = [f"## Cryptocurrency Prices in {currency_to_use}\n"]
        
        for price in price_data["prices"]:
            formatted_price = f"{price['price']:.2f}"
            lines.append(f"**{price['symbol']}**: {formatted_price} {price['base_currency']}")
            
        return "\n".join(lines)
    
    async def background_refresh(self):
        """Background task to periodically refresh prices"""
        while self.running:
            await self.update_prices()
            await asyncio.sleep(self.refresh_interval)


async def test_plugin():
    """Test the Claude Desktop plugin"""
    plugin = ClaudeCryptoPlugin()
    
    try:
        await plugin.start()
        
        # Display current prices
        print(plugin.format_price_message())
        
        # Get prices for specific coins
        custom_prices = await plugin.get_formatted_prices(
            symbols=["BTC", "ETH", "SOL"],
            currency="EUR"
        )
        print("\n" + custom_prices)
        
        await plugin.stop()
        
    except Exception as e:
        print(f"Error testing plugin: {e}")


if __name__ == "__main__":
    # Run test function
    asyncio.run(test_plugin()) 