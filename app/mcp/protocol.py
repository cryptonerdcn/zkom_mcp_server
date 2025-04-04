"""
MCP Protocol Definition for Cryptocurrency Price Service

This module defines the core MCP protocol structures for the cryptocurrency price service.
"""
from typing import Dict, Any, List, Optional, Union
from enum import Enum
from pydantic import BaseModel, Field


class MCPMessageType(str, Enum):
    """Message types for MCP Protocol"""
    REQUEST = "request"
    RESPONSE = "response"
    ERROR = "error"
    NOTIFICATION = "notification"


class MCPErrorCode(int, Enum):
    """Error codes for MCP Protocol"""
    UNKNOWN_ERROR = 1000
    INVALID_REQUEST = 1001
    SERVICE_UNAVAILABLE = 1002
    RESOURCE_NOT_FOUND = 1003
    RATE_LIMITED = 1004
    INVALID_PARAMETER = 1005
    AUTHENTICATION_ERROR = 1006


class MCPProtocolVersion(str, Enum):
    """MCP Protocol versions"""
    V1 = "1.0"


class MCPContext(BaseModel):
    """Context information for MCP messages"""
    request_id: str = Field(..., description="Unique identifier for the request")
    timestamp: int = Field(..., description="Unix timestamp in milliseconds")
    session_id: Optional[str] = Field(None, description="Session identifier if applicable")
    trace_id: Optional[str] = Field(None, description="Trace identifier for distributed tracing")


class MCPError(BaseModel):
    """Error information for MCP responses"""
    code: int = Field(..., description="Error code")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")


class MCPMetadata(BaseModel):
    """Metadata for MCP messages"""
    version: str = Field(default=MCPProtocolVersion.V1.value, description="MCP protocol version")
    service: str = Field(..., description="Service identifier")
    source: Optional[str] = Field(None, description="Source of the message")
    ttl: Optional[int] = Field(None, description="Time to live in seconds")
    cache_control: Optional[str] = Field(None, description="Cache control directives")


class MCPBaseMessage(BaseModel):
    """Base structure for all MCP messages"""
    type: MCPMessageType = Field(..., description="Message type")
    context: MCPContext = Field(..., description="Message context")
    metadata: MCPMetadata = Field(..., description="Message metadata")


class MCPRequest(MCPBaseMessage):
    """MCP Request message"""
    type: MCPMessageType = MCPMessageType.REQUEST
    action: str = Field(..., description="Requested action")
    parameters: Dict[str, Any] = Field(default_factory=dict, description="Request parameters")


class MCPResponse(MCPBaseMessage):
    """MCP Response message"""
    type: MCPMessageType = MCPMessageType.RESPONSE
    data: Any = Field(..., description="Response data")
    links: Optional[Dict[str, str]] = Field(None, description="Related resources")


class MCPErrorResponse(MCPBaseMessage):
    """MCP Error response message"""
    type: MCPMessageType = MCPMessageType.ERROR
    error: MCPError = Field(..., description="Error information")


class MCPNotification(MCPBaseMessage):
    """MCP Notification message"""
    type: MCPMessageType = MCPMessageType.NOTIFICATION
    event: str = Field(..., description="Event name")
    data: Any = Field(..., description="Notification data")


MCPMessage = Union[MCPRequest, MCPResponse, MCPErrorResponse, MCPNotification] 