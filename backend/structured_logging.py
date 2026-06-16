import json
import logging
from datetime import datetime, timezone
from flask import has_request_context, request
from flask_security import current_user

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "path": record.pathname,
            "line_number": record.lineno,
        }

        # If inside a Flask request, enrich with request context metadata
        if has_request_context():
            log_record["request_method"] = request.method
            log_record["request_path"] = request.path
            log_record["ip_address"] = request.remote_addr
            try:
                if current_user and current_user.is_authenticated:
                    log_record["user_id"] = current_user.id
                    log_record["user_role"] = current_user.role
            except Exception:
                pass

        # Check for any extra attributes passed to logger calls
        if hasattr(record, "extra") and isinstance(record.extra, dict):
            log_record.update(record.extra)

        # Include exception trace if present
        if record.exc_info:
            log_record["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_record)


def setup_structured_logging(app=None):
    # Configure root logger to output JSON
    root_logger = logging.getLogger()
    
    # Remove any existing handlers to avoid duplicate formats
    for h in list(root_logger.handlers):
        root_logger.removeHandler(h)
        
    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.INFO)

    # Let Flask logger propagate up to root logger
    if app:
        app.logger.setLevel(logging.INFO)
        app.logger.propagate = True
