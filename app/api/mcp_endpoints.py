"""
MCP-specific API endpoints
"""
import logging
from fastapi import APIRouter, Request, Depends, Header
from typing import Dict, Any, Optional

from app.mcp.protocol import MCPRequest, MCPResponse, MCPErrorResponse
from app.api.routes import extract_request_id, mcp_endpoint

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/mcp",
    summary="MCP standard endpoint",
    description="Standard MCP protocol endpoint following the MCP specification"
)
async def standard_mcp_endpoint(
    request: MCPRequest,
    request_id: Optional[str] = Depends(extract_request_id)
):
    """
    Standard MCP endpoint that follows the MCP protocol specification
    """
    logger.info(f"Received MCP request: {request.action}")
    
    # Process the MCP request using our existing mcp_endpoint
    return await mcp_endpoint(request, request_id) 