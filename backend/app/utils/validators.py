"""
Input Validation Utilities
"""

import re
from typing import Optional
from email_validator import validate_email, EmailNotValidError

from app.core.exceptions import ValidationError
from app.core.logging import get_logger

logger = get_logger(__name__)


class Validators:
    """Input validation utilities"""
    
    @staticmethod
    def validate_email_address(email: str) -> bool:
        """
        Validate email address format
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid
            
        Raises:
            ValidationError: If email is invalid
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError as e:
            raise ValidationError(f"Invalid email: {str(e)}")
    
    @staticmethod
    def validate_phone_number(phone: str) -> bool:
        """
        Validate phone number format
        
        Args:
            phone: Phone number to validate
            
        Returns:
            True if valid
        """
        # Basic phone validation (10-15 digits)
        pattern = r'^[\+]?[(]?[0-9]{1,4}[)]?[-\s\.]?[(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{1,4}[-\s\.]?[0-9]{1,9}$'
        if not re.match(pattern, phone):
            raise ValidationError("Invalid phone number format")
        return True
    
    @staticmethod
    def validate_job_role(role: str) -> bool:
        """
        Validate job role input
        
        Args:
            role: Job role to validate
            
        Returns:
            True if valid
        """
        if not role or len(role) < 2:
            raise ValidationError("Job role must be at least 2 characters")
        
        if len(role) > 100:
            raise ValidationError("Job role must be less than 100 characters")
        
        # Only allow alphanumeric, spaces, and basic punctuation
        if not re.match(r'^[a-zA-Z0-9\s\-\_\/]+$', role):
            raise ValidationError("Job role contains invalid characters")
        
        return True
    
    @staticmethod
    def validate_text_length(
        text: str,
        min_length: int = 1,
        max_length: int = 10000,
        field_name: str = "Text"
    ) -> bool:
        """
        Validate text length
        
        Args:
            text: Text to validate
            min_length: Minimum length
            max_length: Maximum length
            field_name: Name of field for error messages
            
        Returns:
            True if valid
        """
        if not text:
            raise ValidationError(f"{field_name} cannot be empty")
        
        length = len(text)
        
        if length < min_length:
            raise ValidationError(
                f"{field_name} must be at least {min_length} characters"
            )
        
        if length > max_length:
            raise ValidationError(
                f"{field_name} must be less than {max_length} characters"
            )
        
        return True
    
    @staticmethod
    def validate_score(score: float, min_val: float = 0.0, max_val: float = 100.0) -> bool:
        """
        Validate score is within range
        
        Args:
            score: Score to validate
            min_val: Minimum value
            max_val: Maximum value
            
        Returns:
            True if valid
        """
        if not isinstance(score, (int, float)):
            raise ValidationError("Score must be a number")
        
        if score < min_val or score > max_val:
            raise ValidationError(f"Score must be between {min_val} and {max_val}")
        
        return True
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        Sanitize filename to prevent path traversal
        
        Args:
            filename: Original filename
            
        Returns:
            Sanitized filename
        """
        # Remove path components
        filename = filename.replace('\\', '').replace('/', '')
        
        # Remove potentially dangerous characters
        filename = re.sub(r'[^\w\s\-\.]', '', filename)
        
        # Limit length
        if len(filename) > 255:
            name, ext = filename.rsplit('.', 1)
            filename = name[:250] + '.' + ext
        
        return filename
    
    @staticmethod
    def validate_object_id(obj_id: str) -> bool:
        """
        Validate MongoDB ObjectId format
        
        Args:
            obj_id: ObjectId string
            
        Returns:
            True if valid
        """
        if not re.match(r'^[0-9a-fA-F]{24}$', obj_id):
            raise ValidationError("Invalid ObjectId format")
        return True
