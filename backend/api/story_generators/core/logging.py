"""
Logging configuration for story generators.
"""

import logging
import sys
from typing import Optional, Dict, Any
from pathlib import Path
import json
from datetime import datetime


class StoryGeneratorFormatter(logging.Formatter):
    """Custom formatter for story generator logs."""
    
    def format(self, record):
        # Add timestamp
        record.timestamp = datetime.utcnow().isoformat()
        
        # Create structured log entry
        log_entry = {
            "timestamp": record.timestamp,
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)
            
        # Add exception info if present
        if record.exc_info:
            log_entry["exception"] = self.formatException(record.exc_info)
            
        return json.dumps(log_entry, default=str)


class StoryGeneratorLogger:
    """Enhanced logger for story generators with structured logging."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self):
        """Setup logger with appropriate handlers and formatters."""
        if not self.logger.handlers:
            # Console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(console_formatter)
            
            # File handler for structured logs
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            file_handler = logging.FileHandler(log_dir / "story_generators.jsonl")
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(StoryGeneratorFormatter())
            
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)
            self.logger.setLevel(logging.DEBUG)
    
    def debug(self, message: str, **kwargs):
        """Log debug message with optional extra fields."""
        extra = {"extra_fields": kwargs} if kwargs else {}
        self.logger.debug(message, extra=extra)
    
    def info(self, message: str, **kwargs):
        """Log info message with optional extra fields."""
        extra = {"extra_fields": kwargs} if kwargs else {}
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with optional extra fields."""
        extra = {"extra_fields": kwargs} if kwargs else {}
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, **kwargs):
        """Log error message with optional extra fields."""
        extra = {"extra_fields": kwargs} if kwargs else {}
        self.logger.error(message, extra=extra, exc_info=kwargs.get('exc_info', False))
    
    def critical(self, message: str, **kwargs):
        """Log critical message with optional extra fields."""
        extra = {"extra_fields": kwargs} if kwargs else {}
        self.logger.critical(message, extra=extra)
    
    def log_generation_start(self, generator_type: str, request_data: Dict[str, Any]):
        """Log the start of a generation process."""
        self.info(
            f"Starting {generator_type} generation",
            generator_type=generator_type,
            request_size=len(str(request_data)),
            start_time=datetime.utcnow().isoformat()
        )
    
    def log_generation_progress(self, generator_type: str, progress: float, step: str):
        """Log generation progress."""
        self.info(
            f"{generator_type} generation progress: {progress:.1f}%",
            generator_type=generator_type,
            progress=progress,
            current_step=step
        )
    
    def log_generation_complete(self, generator_type: str, duration: float, success: bool):
        """Log generation completion."""
        level = "info" if success else "error"
        getattr(self, level)(
            f"{generator_type} generation {'completed' if success else 'failed'}",
            generator_type=generator_type,
            duration=duration,
            success=success,
            end_time=datetime.utcnow().isoformat()
        )
    
    def log_api_call(self, provider: str, model: str, tokens_used: Optional[int] = None):
        """Log API calls to external services."""
        self.info(
            f"API call to {provider}",
            provider=provider,
            model=model,
            tokens_used=tokens_used,
            call_time=datetime.utcnow().isoformat()
        )
    
    def log_error_with_context(self, error: Exception, context: Dict[str, Any]):
        """Log error with additional context."""
        self.error(
            f"Error occurred: {str(error)}",
            error_type=error.__class__.__name__,
            error_message=str(error),
            context=context,
            exc_info=True
        )


# Global logger instances
_loggers: Dict[str, StoryGeneratorLogger] = {}


def get_logger(name: str) -> StoryGeneratorLogger:
    """Get or create a logger instance."""
    if name not in _loggers:
        _loggers[name] = StoryGeneratorLogger(name)
    return _loggers[name]


def setup_logging():
    """Setup logging configuration for the application."""
    # Ensure logs directory exists
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Disable some noisy loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)