"""
Custom Exception Classes
Defines application-specific exceptions for better error handling
"""

from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class BaseAppException(Exception):
    """Base exception for all application errors"""
    
    def __init__(
        self,
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class FileProcessingError(BaseAppException):
    """Raised when file processing fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class InvalidFileTypeError(BaseAppException):
    """Raised when uploaded file type is invalid"""
    
    def __init__(self, file_type: str, allowed_types: list):
        message = f"Invalid file type: {file_type}. Allowed types: {', '.join(allowed_types)}"
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details={"file_type": file_type, "allowed_types": allowed_types}
        )


class FileSizeExceededError(BaseAppException):
    """Raised when file size exceeds limit"""
    
    def __init__(self, size: int, max_size: int):
        message = f"File size {size} bytes exceeds maximum {max_size} bytes"
        super().__init__(
            message=message,
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            details={"size": size, "max_size": max_size}
        )


class ResumeParsingError(BaseAppException):
    """Raised when resume parsing fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Resume parsing failed: {message}",
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            details=details
        )


class DatabaseError(BaseAppException):
    """Raised when database operation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Database error: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class ResourceNotFoundError(BaseAppException):
    """Raised when requested resource is not found"""
    
    def __init__(self, resource: str, identifier: str):
        message = f"{resource} with identifier '{identifier}' not found"
        super().__init__(
            message=message,
            status_code=status.HTTP_404_NOT_FOUND,
            details={"resource": resource, "identifier": identifier}
        )


class ValidationError(BaseAppException):
    """Raised when input validation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            status_code=status.HTTP_400_BAD_REQUEST,
            details=details
        )


class NLPModelError(BaseAppException):
    """Raised when NLP model operation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"NLP model error: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


class InterviewGenerationError(BaseAppException):
    """Raised when interview question generation fails"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"Interview generation failed: {message}",
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            details=details
        )


def convert_to_http_exception(exc: BaseAppException) -> HTTPException:
    """
    Convert application exception to FastAPI HTTPException
    
    Args:
        exc: Application exception
        
    Returns:
        HTTPException with proper status code and detail
    """
    return HTTPException(
        status_code=exc.status_code,
        detail={
            "message": exc.message,
            "details": exc.details
        }
    )
