"""
Logging Configuration
Centralized logging setup with structured output
"""

import logging
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from app.config import settings


class ColoredFormatter(logging.Formatter):
    """Custom formatter with colors for console output"""
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record):
        """Format log record with colors"""
        if record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}"
                f"{self.COLORS['RESET']}"
            )
        return super().format(record)


def setup_logging(
    name: Optional[str] = None,
    level: Optional[str] = None,
    log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configure and return a logger instance
    
    Args:
        name: Logger name (default: root logger)
        level: Logging level (default: from settings)
        log_file: Path to log file (default: from settings)
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    
    # Set level
    log_level = level or settings.LOG_LEVEL
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Prevent duplicate handlers
    if logger.handlers:
        return logger
    
    # Console handler with colors
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_formatter = ColoredFormatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    file_path = log_file or settings.LOG_FILE
    if file_path:
        Path(file_path).parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(file_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get or create a logger for a module
    
    Args:
        name: Module name (typically __name__)
        
    Returns:
        Logger instance
    """
    return setup_logging(name)


# Create application-wide logger
app_logger = setup_logging("app")


def log_request(method: str, path: str, status_code: int, duration: float):
    """
    Log HTTP request details
    
    Args:
        method: HTTP method
        path: Request path
        status_code: Response status code
        duration: Request duration in seconds
    """
    logger = get_logger("app.request")
    
    # Color code based on status
    if status_code < 400:
        level = logging.INFO
    elif status_code < 500:
        level = logging.WARNING
    else:
        level = logging.ERROR
    
    logger.log(
        level,
        f"{method} {path} - {status_code} - {duration:.3f}s"
    )


def log_exception(exc: Exception, context: Optional[dict] = None):
    """
    Log exception with context
    
    Args:
        exc: Exception to log
        context: Additional context information
    """
    logger = get_logger("app.exception")
    
    context_str = ""
    if context:
        context_str = " | Context: " + ", ".join(
            f"{k}={v}" for k, v in context.items()
        )
    
    logger.error(
        f"{exc.__class__.__name__}: {str(exc)}{context_str}",
        exc_info=True
    )
