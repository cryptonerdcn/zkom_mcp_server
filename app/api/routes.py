"""
API routes for the cryptocurrency price service
"""
import logging
from typing import List, Optional, Dict, Any, Union
from fastapi import APIRouter, Query, Path, Depends, HTTPException, Header

from app.mcp.protocol import MCPResponse, MCPErrorResponse, MCPRequest
from app.mcp.service import get_crypto_price, get_multiple_prices
from app.models.crypto import CryptoPriceRequest

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/v1")


def extract_request_id(x_request_id: Optional[str] = Header(None)) -> Optional[str]:
    """
    Extract request ID from header if available
    """
    return x_request_id


@router.get(
    "/crypto/price",
    response_model=MCPResponse,
    summary="Get price of a cryptocurrency",
    description="Get the current price of a cryptocurrency in the specified base currency"
)
async def crypto_price(
    symbol: str = Query(..., description="Symbol of the cryptocurrency (e.g., BTC)"),
    currency: str = Query("USD", description="Base currency for the price"),
    request_id: Optional[str] = Depends(extract_request_id)
) -> Union[MCPResponse, MCPErrorResponse]:
    """
    Get the price of a cryptocurrency
    """
    logger.info(f"Getting price for {symbol} in {currency}")
    return await get_crypto_price(symbol, currency, request_id)


@router.post(
    "/crypto/price",
    response_model=MCPResponse,
    summary="Get price of a cryptocurrency (POST)",
    description="Get the current price of a cryptocurrency in the specified base currency"
)
async def crypto_price_post(
    request: CryptoPriceRequest,
    request_id: Optional[str] = Depends(extract_request_id)
) -> Union[MCPResponse, MCPErrorResponse]:
    """
    Get the price of a cryptocurrency (POST method)
    """
    logger.info(f"Getting price for {request.symbol} in {request.base_currency}")
    return await get_crypto_price(request.symbol, request.base_currency, request_id)


@router.post(
    "/mcp",
    response_model=Union[MCPResponse, MCPErrorResponse],
    summary="MCP protocol endpoint",
    description="General purpose MCP protocol endpoint for all cryptocurrency price operations"
)
async def mcp_endpoint(
    request: MCPRequest,
    request_id: Optional[str] = Depends(extract_request_id)
) -> Union[MCPResponse, MCPErrorResponse]:
    """
    Process an MCP protocol request
    """
    # Use the request_id from the MCP request if available
    req_id = request.context.request_id if request.context and request.context.request_id else request_id
    
    # Process the request based on the action
    if request.action == "crypto.price.get":
        symbol = request.parameters.get("symbol")
        currency = request.parameters.get("currency", "USD")
        
        if not symbol:
            logger.error("Missing required parameter: symbol")
            return MCPErrorResponse(
                context=request.context,
                metadata=request.metadata,
                error={
                    "code": 1005,  # INVALID_PARAMETER
                    "message": "Missing required parameter: symbol"
                }
            )
            
        return await get_crypto_price(symbol, currency, req_id)
        
    elif request.action == "crypto.prices.get":
        symbols = request.parameters.get("symbols", [])
        currency = request.parameters.get("currency", "USD")
        
        if not symbols or not isinstance(symbols, list):
            logger.error("Invalid or missing parameter: symbols")
            return MCPErrorResponse(
                context=request.context,
                metadata=request.metadata,
                error={
                    "code": 1005,  # INVALID_PARAMETER
                    "message": "Invalid or missing parameter: symbols (must be a list)"
                }
            )
            
        return await get_multiple_prices(symbols, currency, req_id)
        
    else:
        logger.error(f"Unknown action: {request.action}")
        return MCPErrorResponse(
            context=request.context,
            metadata=request.metadata,
            error={
                "code": 1001,  # INVALID_REQUEST
                "message": f"Unknown action: {request.action}"
            }
        ) 