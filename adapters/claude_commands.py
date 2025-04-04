#!/usr/bin/env python
"""
Claude Desktop Custom Commands for Cryptocurrency Prices

This module defines custom commands for Claude Desktop to interact with
the ZKOM MCP Server for cryptocurrency price information.
"""
import re
import asyncio
import logging
from typing import Dict, List, Any, Optional, Tuple

from claude_desktop_plugin import ClaudeCryptoPlugin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("claude_commands")

# Initialize plugin
crypto_plugin = ClaudeCryptoPlugin()


async def initialize():
    """Initialize the commands module"""
    await crypto_plugin.start()
    logger.info("Initialized Claude Desktop crypto commands")


async def shutdown():
    """Shutdown the commands module"""
    await crypto_plugin.stop()
    logger.info("Shutdown Claude Desktop crypto commands")


async def process_crypto_price_command(command_text: str) -> str:
    """
    Process the /crypto-price command
    
    Format:
      /crypto-price [symbol1] [symbol2] ... [--currency XXX]
      
    Examples:
      /crypto-price BTC
      /crypto-price BTC ETH SOL
      /crypto-price BTC --currency EUR
    
    Args:
        command_text: The command text after the /crypto-price part
        
    Returns:
        Formatted response with price information
    """
    # Parse command arguments
    parts = command_text.strip().split()
    
    # Extract currency flag if present
    currency = None
    symbols = []
    
    i = 0
    while i < len(parts):
        if parts[i] == "--currency" and i + 1 < len(parts):
            currency = parts[i + 1]
            i += 2
        else:
            symbols.append(parts[i].upper())
            i += 1
    
    # If no symbols specified, use default watch list
    if not symbols:
        return await crypto_plugin.get_formatted_prices(currency=currency)
    
    # Get prices for specified symbols
    return await crypto_plugin.get_formatted_prices(symbols=symbols, currency=currency)


def parse_command(message: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse a command from a message
    
    Args:
        message: The message text
        
    Returns:
        Tuple of (command, arguments) or (None, None) if not a command
    """
    command_pattern = r"^/([a-zA-Z0-9_-]+)(?:\s+(.*))?$"
    match = re.match(command_pattern, message.strip())
    
    if match:
        command = match.group(1).lower()
        args = match.group(2) or ""
        return command, args
    
    return None, None


async def handle_message(message: str) -> Optional[str]:
    """
    Handle a message from Claude Desktop
    
    Args:
        message: The message text
        
    Returns:
        Response text if command was handled, None otherwise
    """
    command, args = parse_command(message)
    
    if not command:
        return None
        
    if command == "crypto-price":
        return await process_crypto_price_command(args)
        
    return None


async def test_commands():
    """Test the commands module"""
    await initialize()
    
    try:
        # Test basic command
        response = await handle_message("/crypto-price BTC")
        print(response)
        
        # Test multiple symbols
        response = await handle_message("/crypto-price BTC ETH SOL")
        print(response)
        
        # Test with currency
        response = await handle_message("/crypto-price BTC --currency EUR")
        print(response)
        
        # Test default watch list
        response = await handle_message("/crypto-price")
        print(response)
        
    finally:
        await shutdown()


if __name__ == "__main__":
    # Run test function
    asyncio.run(test_commands()) 