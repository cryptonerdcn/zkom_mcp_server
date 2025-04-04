"""
MCP Service Implementation for Cryptocurrency Price Service

This module implements the MCP protocol for the cryptocurrency price service.
"""
import time
import uuid
import logging
from typing import Dict, Any, List, Optional, Union

from app.mcp.protocol import (
    MCPContext,
    MCPMetadata,
    MCPResponse,
    MCPErrorResponse,
    MCPError,
    MCPErrorCode
)
from app.models.crypto import CryptoPrice, CryptoPriceListResponse
from app.services.coinbase import coinbase_client

logger = logging.getLogger(__name__)

# Service constants
SERVICE_NAME = "zkom.crypto.price"
DEFAULT_TTL = 60  # seconds


def create_context(request_id: Optional[str] = None) -> MCPContext:
    """
    Create a new MCP context
    
    Args:
        request_id: Optional request ID, will generate one if not provided
        
    Returns:
        MCPContext object
    """
    return MCPContext(
        request_id=request_id or str(uuid.uuid4()),
        timestamp=int(time.time() * 1000)
    )


def create_metadata() -> MCPMetadata:
    """
    Create metadata for MCP messages
    
    Returns:
        MCPMetadata object
    """
    return MCPMetadata(
        service=SERVICE_NAME,
        ttl=DEFAULT_TTL,
        cache_control="public, max-age=60"
    )


def create_error_response(
    error_code: MCPErrorCode,
    message: str,
    details: Optional[Dict[str, Any]] = None,
    request_id: Optional[str] = None
) -> MCPErrorResponse:
    """
    Create an MCP error response
    
    Args:
        error_code: Error code
        message: Error message
        details: Optional error details
        request_id: Optional request ID
        
    Returns:
        MCPErrorResponse object
    """
    return MCPErrorResponse(
        context=create_context(request_id),
        metadata=create_metadata(),
        error=MCPError(
            code=error_code,
            message=message,
            details=details
        )
    )


async def get_crypto_price(
    symbol: str, 
    base_currency: str = "USD",
    request_id: Optional[str] = None
) -> Union[MCPResponse, MCPErrorResponse]:
    """
    Get the price of a cryptocurrency
    
    Args:
        symbol: Symbol of the cryptocurrency
        base_currency: Base currency for the price
        request_id: Optional request ID
        
    Returns:
        MCPResponse with price data or MCPErrorResponse if error
    """
    try:
        price = await coinbase_client.get_crypto_price(symbol, base_currency)
        
        if not price:
            return create_error_response(
                MCPErrorCode.RESOURCE_NOT_FOUND,
                f"Price for {symbol}/{base_currency} not found",
                request_id=request_id
            )
        
        return MCPResponse(
            context=create_context(request_id),
            metadata=create_metadata(),
            data=price
        )
        
    except Exception as e:
        logger.error(f"Error getting crypto price: {e}")
        return create_error_response(
            MCPErrorCode.SERVICE_UNAVAILABLE,
            f"Error fetching price data: {str(e)}",
            request_id=request_id
        )


async def get_multiple_prices(
    symbols: List[str],
    base_currency: str = "USD",
    request_id: Optional[str] = None
) -> Union[MCPResponse, MCPErrorResponse]:
    """
    Get prices for multiple cryptocurrencies
    
    Args:
        symbols: List of cryptocurrency symbols
        base_currency: Base currency for the prices
        request_id: Optional request ID
        
    Returns:
        MCPResponse with price data or MCPErrorResponse if error
    """
    try:
        prices = await coinbase_client.get_multiple_prices(symbols, base_currency)
        
        if not prices:
            return create_error_response(
                MCPErrorCode.RESOURCE_NOT_FOUND,
                f"No prices found for the requested symbols",
                request_id=request_id
            )
        
        response_data = CryptoPriceListResponse(
            prices=prices,
            count=len(prices),
            timestamp=int(time.time() * 1000)
        )
        
        return MCPResponse(
            context=create_context(request_id),
            metadata=create_metadata(),
            data=response_data
        )
        
    except Exception as e:
        logger.error(f"Error getting multiple crypto prices: {e}")
        return create_error_response(
            MCPErrorCode.SERVICE_UNAVAILABLE,
            f"Error fetching price data: {str(e)}",
            request_id=request_id
        ) 