"""
Common Response Schemas
"""

from pydantic import BaseModel
from typing import Optional, Any, Dict


class SuccessResponse(BaseModel):
    """Standard success response"""
    success: bool = True
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """Standard error response"""
    success: bool = False
    message: str
    error: Optional[str] = None
    details: Optional[Dict] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    database: str
    timestamp: str
